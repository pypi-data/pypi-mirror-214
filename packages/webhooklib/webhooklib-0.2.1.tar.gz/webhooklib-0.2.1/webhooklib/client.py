import os
import sys

import requests
from redis import Redis

from webhooklib import config
from webhooklib import exceptions
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult

ENV_PREFIX = 'WEBHOOK_ENV_'


def main():
    redis = Redis.from_url(os.environ['REDIS_URL'])

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
    _, message = redis.brpop(key)
    result = ShellResult.parse_raw(message)
    result.pprint()
    if result.returncode != 0:
        raise exceptions.ProcessResultError
    redis.delete(key)


if __name__ == '__main__':
    main()
