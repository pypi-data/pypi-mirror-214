import argparse
import os

from redis import Redis

from webhooklib.client import get_all_resources


def main():
    redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'stop'])
    args = parser.parse_args()
    resources = get_all_resources(os.environ['WEBHOOK_RESOURCES_KEY'], redis)
    if args.action == 'start':
        redis.hincrby(resources['pipeline'].key, 'usage_current')
    elif args.action == 'stop':
        redis.hincrby(resources['pipeline'].key, 'usage_current', -1)
        redis.publish(os.environ['WEBHOOK_PIPELINE_STOP_CHANNEL'], 'stop')


if __name__ == '__main__':
    main()
