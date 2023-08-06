import os

from redis import Redis


def main():
    redis = Redis.from_url(os.environ['REDIS_URL'])
    # receive new tasks from redis queue (list)
    # run subprocess wrappers (which push to done queue after finishing)

    redis.lpush('audio', '1')
    redis.lpush('audio', '2')


if __name__ == '__main__':
    main()
