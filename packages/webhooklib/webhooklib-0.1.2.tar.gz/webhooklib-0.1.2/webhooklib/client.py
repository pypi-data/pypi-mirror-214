import os
import sys

import requests
from redis import Redis

ENV_PREFIX = 'WEBHOOK_ENV_'


def main():
    Redis.from_url(os.environ['REDIS_URL'])

    url = os.environ['WEBHOOK_URL']
    payload = {'cmd': sys.argv[1:]}
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
    headers = {'token': os.environ['WEBHOOK_TOKEN']}
    response = requests.post(url, headers=headers, json=payload)

    if not response.ok:
        print(response.status_code)
        print(response.text)
        raise SystemExit(1)

    print(response.json())


redis.lpush('audio', '1')
redis.lpush('audio', '2')


if __name__ == '__main__':
    main()
