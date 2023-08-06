import logging
import subprocess

from redis import Redis

from webhooklib import config
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_subprocess(
    command: ShellCommand,
    redis: Redis,
) -> None:
    logger.info('start')
    print('run_subprocess:', command)
    p = subprocess.Popen(
        command.cmd,
        env=command.env,
        cwd=command.cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    logger.info('Popen done')

    try:
        stdout, stderr = p.communicate(timeout=command.timeout)
        logger.info('inside try')
    except subprocess.TimeoutExpired:
        p.kill()
        stdout, stderr = p.communicate()
        _status = 'subprocess.TimeoutExpired'
        logger.info(_status)
    else:
        _status = 'success'

    logger.info('before result')

    result = ShellResult(
        status=_status,
        returncode=p.returncode,
        stdout=stdout,
        stderr=stderr,
    )
    logger.info('after result')
    logger.info(f'{config.PROCESS_DONE}:{command.id}')
    redis.lpush(f'{config.PROCESS_DONE}:{command.id}', result.json())
    logger.info('lpush done')
