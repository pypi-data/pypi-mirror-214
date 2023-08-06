import logging
import subprocess
import selectors
import time
import sys
import signal
from redis import Redis

from webhooklib import config
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_rest_of_lines(p, redis, stdout_key, stderr_key) -> None:
    for line in p.stdout:
        redis.lpush(stdout_key, line)
    for line in p.stderr:
        redis.lpush(stderr_key, line)


def non_blocking_process(command: ShellCommand, redis: Redis):
    print('non_blocking_process:', command)
    
    stdout_key = f'{config.LOGS}:{command.id}:stdout'
    stderr_key = f'{config.LOGS}:{command.id}:stderr'

    # create empty line to set ttl before logs are written
    pipeline = redis.pipeline()
    pipeline.lpush(stdout_key, '')
    pipeline.lpush(stderr_key, '') 
    pipeline.expire(stdout_key, config.LOGS_TTL)
    pipeline.expire(stderr_key, config.LOGS_TTL)
    pipeline.execute()

    t_start = time.time()
    p = subprocess.Popen(
        command.cmd,
        env=command.env,
        cwd=command.cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    logger.info('Popen done')

    # Create the default selector
    sel = selectors.DefaultSelector()

    # Register the subprocess's stdout and stderr for monitoring 
    # route them to current process's stdout and stderr
    sel.register(p.stdout, selectors.EVENT_READ, data='stdout')
    sel.register(p.stderr, selectors.EVENT_READ, data='stderr')

    while p.poll() is None:  # While the process is still running...
        if command.timeout is not None and time.time() - t_start > command.timeout:
            print('timeout: killing the proccess')
            p.kill()
            read_rest_of_lines(p, redis, stdout_key)
            return ShellResult(
                status='killed by timeout',
                returncode=signal.SIGKILL,
                stdout=redis.lrange(stdout_key, 0, -1),
                stderr=redis.lrange(stderr_key, 0, -1),
            )
        for key, _ in sel.select():  # Wait until stdout or stderr has data
            line = key.fileobj.readline()  # Read a line from the pipe
            if line:  # If the line is not empty...
                if key.data == 'stdout':
                    redis.lpush(stdout_key, line)
                elif key.data == 'stderr':
                    redis.lpush(stderr_key, line)
    return ShellResult(
        status='success',
        returncode=p.returncode,
        stdout=redis.lrange(stdout_key, 0, -1),
        stderr=redis.lrange(stderr_key, 0, -1),
    )

def run_subprocess(
    command: ShellCommand,
    redis: Redis,
) -> None:
    logger.info('start')
    result = non_blocking_process(command, redis)
    # p = subprocess.Popen(
    #     command.cmd,
    #     env=command.env,
    #     cwd=command.cwd,
    #     text=True,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    # )

    # logger.info('Popen done')

    # try:
    #     stdout, stderr = p.communicate(timeout=command.timeout)
    #     logger.info('inside try')
    # except subprocess.TimeoutExpired:
    #     p.kill()
    #     stdout, stderr = p.communicate()
    #     _status = 'subprocess.TimeoutExpired'
    #     logger.info(_status)
    # else:
    #     _status = 'success'

    # logger.info('before result')

    # result = ShellResult(
    #     status=_status,
    #     returncode=p.returncode,
    #     stdout=stdout,
    #     stderr=stderr,
    # )
    logger.info('after result')
    logger.info(f'{config.PROCESS_DONE}:{command.id}')
    redis.lpush(f'{config.PROCESS_DONE}:{command.id}', result.json())
    logger.info('lpush done')
