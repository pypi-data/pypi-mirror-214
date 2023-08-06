import argparse
import os

from redis import Redis


def main():
    redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'stop'])
    args = parser.parse_args()
    n_pipelines_key = os.environ['WEBHOOK_N_PIPELINES_KEY']
    pipeline_stop_channel = os.environ['WEBHOOK_PIPELINE_STOP_CHANNEL']
    if args.action == 'start':
        redis.incr(n_pipelines_key)
    elif args.action == 'stop':
        redis.decr(n_pipelines_key)
        redis.publish(pipeline_stop_channel, 'stop')


if __name__ == '__main__':
    main()
