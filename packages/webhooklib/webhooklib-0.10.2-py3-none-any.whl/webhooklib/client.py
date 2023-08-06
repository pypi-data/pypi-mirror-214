import os
import sys

import requests
from redis import Redis

from webhooklib import config
from webhooklib import exceptions
from webhooklib.models import Resource
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult

ENV_PREFIX = 'WEBHOOK_ENV_'


def red(obj):
    return f'\033[31m{obj}\033[0m'


def get_job_resources() -> frozenset[str]:
    res_string = os.environ.get('WEBHOOK_JOB_RESOURCES')
    if res_string is None:
        return []
    return frozenset(res_string.split(','))


def get_all_resources(resources_key: str, redis: Redis) -> dict[str, Resource]:
    pipeline = redis.pipeline()
    keys = redis.keys(f'{resources_key}:*')
    names = []
    for key in keys:
        pipeline.hgetall(key)
        _, name = key.rsplit(':', maxsplit=1)
        names.append(name)
    resources = pipeline.execute()
    resources = {name: Resource(**r, key=k, name=name) for r, k, name in zip(resources, keys, names, strict=True)}
    return resources


def get_wait_resources(redis: Redis) -> dict[str, Resource]:
    job_resources = get_job_resources()
    all_resources = get_all_resources(os.environ['WEBHOOK_RESOURCES_KEY'], redis)
    out = {}
    for name, resource in all_resources.items():
        if name not in job_resources or name != 'job':
            continue
        out[name] = resource
    return out


def wait_message(channel: str, redis: Redis) -> None:
    p = redis.pubsub()
    p.subscribe(channel)
    while not (message := p.get_message(ignore_subscribe_messages=True)):
        pass
    print(message)


def wait_resource_semaphore(
    resource: Resource,
    job_stop_channel: str,
    redis: Redis,
) -> None:
    if resource.usage_current < resource.usage_limit:
        return
    print('resource busy, waiting... :', resource)
    wait_message(job_stop_channel, redis)
    wait_resources_semaphore(resource, job_stop_channel, redis)


def wait_resources_semaphore(
    resources: list[Resource],
    job_stop_channel: str,
    redis: Redis,
) -> None:
    for resource in resources:
        wait_resource_semaphore(resource, job_stop_channel, redis)
        # if resource.usage_current >= resource.usage_limit:
        #     print('resource busy, waiting... :', resource)
        #     wait_message(job_stop_channel, redis)
        #     wait_resources_semaphore(resources, job_stop_channel, redis)
        #     return


# def wait_max_jobs_quota(redis):
#     n_jobs_key = os.environ['WEBHOOK_N_JOBS_KEY']
#     n_jobs = redis.get(n_jobs_key)
#     max_jobs = int(os.environ.get('WEBHOOK_MAX_JOBS', 10))
#     if n_jobs is None:
#         return
#     if int(n_jobs) <= max_jobs:
#         return
#     print(f'{n_jobs=}, {max_jobs=}, waiting...')
#     wait_message(os.environ['WEBHOOK_JOB_STOP_CHANNEL'], redis)
#     wait_max_jobs_quota(redis)


def read_rest_logs(redis: Redis, stdout_key: str, stderr_key: str) -> None:
    pipeline = redis.pipeline()
    pipeline.lrange(stdout_key, 1, -1)
    pipeline.lrange(stderr_key, 1, -1)
    stdout, stderr = pipeline.execute()
    for line in stdout:
        print(line, end='')
    for line in stderr:
        print(red(line), end='')


def main(line_buffer_size: int = 100):
    redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)

    # delete_resources = {'pipeline'}
    # for k, r in resources.items():
    # if k not in job_resources:
    # continue
    # del resources['pipeline']
    resources = get_wait_resources(redis)
    wait_resources_semaphore(list(resources.values()), os.environ['WEBHOOK_JOB_STOP_CHANNEL'], redis)

    # wait_max_jobs_quota(redis)
    # redis.incr(os.environ['WEBHOOK_N_JOBS_KEY'])
    redis.hincrby(resources['job'].key, 'usage_current')

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

    print('loc 1')
    # while stdout_line or stderr_line or result is None:
    while result is None:
        pipeline = redis.pipeline()
        # pipeline.rpop(stdout_key)
        # pipeline.rpop(stderr_key)
        pipeline.rpop(stdout_key, line_buffer_size)
        pipeline.rpop(stderr_key, line_buffer_size)
        pipeline.rpop(key)
        stdout_line, stderr_line, result = pipeline.execute()

        if stdout_line:
            for line in stdout_line:
                print(line, end='')
        if stderr_line:
            for line in stderr_line:
                print(red(line), end='')

        # stdout_line = redis.rpop(stdout_key)
        # if stdout_line:
            # print(stdout_line, end='')
        # stderr_line= redis.rpop(stderr_key)
        # if stderr_line:
            # print(red(stderr_line), end='')
        # result = redis.rpop(key)

    read_rest_logs(redis, stdout_key, stderr_key)

    # _, message = redis.brpop(key)
    # result = ShellResult.parse_raw(message)
    result = ShellResult.parse_raw(result)
    # result.pprint()
    if result.returncode != 0:
        raise exceptions.ProcessResultError
    redis.delete(key)
    # redis.decr(os.environ['WEBHOOK_N_JOBS_KEY'])
    redis.hincrby(resources['job'].key, 'usage_current', -1)


if __name__ == '__main__':
    main()
