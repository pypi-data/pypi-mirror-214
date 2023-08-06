import os
import sys

import requests
from redis import Redis

from webhooklib import config
from webhooklib import exceptions
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult

ENV_PREFIX = 'WEBHOOK_ENV_'


def wait_message(channel: str, redis: Redis) -> None:
    p = redis.pubsub()
    p.subscribe(channel)
    while not (message := p.get_message(ignore_subscribe_messages=True)):
        pass
    print(message)


def wait_max_jobs_quota(redis):
    n_jobs_key = os.environ['WEBHOOK_N_JOBS_KEY']
    n_jobs = redis.get(n_jobs_key)
    max_jobs = int(os.environ['WEBHOOK_MAX_JOBS'])
    if n_jobs is None:
        return
    if int(n_jobs) <= max_jobs:
        return

    print(f'{n_jobs=}, {max_jobs=}, waiting...')
    wait_message(os.environ['WEBHOOK_JOB_STOP_CHANNEL'], redis)
    wait_max_jobs_quota(redis)


def main():
    redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    wait_max_jobs_quota(redis)
    redis.incr(os.environ['WEBHOOK_N_JOBS_KEY'])

    url = os.environ['WEBHOOK_URL']
    payload = {
        'cmd': sys.argv[1:],
    }
    if 'WEBHOOK_CWD' in os.environ:
        payload['cwd'] = os.environ['WEBHOOK_CWD']
    if 'WEBHOOK_TIMEOUT' in os.environ:
        payload['timeout'] = float(os.environ['WEBHOOK_TIMEOUT'])

    env = {
        k.removeprefix(ENV_PREFIX): v
        for k, v in os.environ.items()
        if k.startswith(ENV_PREFIX)
    }
    print(env)
    print(payload)
    command = ShellCommand(**payload)
    headers = {'token': os.environ['WEBHOOK_TOKEN']}
    response = requests.post(url, headers=headers, json=command.dict())

    if not response.ok:
        print(response.status_code)
        print(response.text)
        raise SystemExit(1)

    if response.json() != {'process-created': 'ok'}:
        raise exceptions.ProcessCreateError(response.text)

    print(response.json())
    key = f'{config.PROCESS_DONE}:{command.id}'
    print(key)

    stdout_key = f'{config.LOGS}:{command.id}:stdout'
    stderr_key = f'{config.LOGS}:{command.id}:stderr'

    # TODO: iterate over logs here
    result = None

    # while stdput_line or stderr_line or result is None:
    while result is None:
        pipeline = redis.pipeline()
        pipeline.rpop(stdout_key)
        pipeline.rpop(stderr_key)
        pipeline.rpop(key)
        stdput_line, stderr_line, result = pipeline.execute()


        if stdput_line:
            print(stdput_line)
        if stderr_line:
            print(stderr_line)
        if result:
            break


    # _, message = redis.brpop(key)
    # result = ShellResult.parse_raw(message)
    result = ShellResult.parse_raw(result)
    result.pprint()
    if result.returncode != 0:
        raise exceptions.ProcessResultError
    redis.delete(key)
    redis.decr(os.environ['WEBHOOK_N_JOBS_KEY'])


if __name__ == '__main__':
    main()
