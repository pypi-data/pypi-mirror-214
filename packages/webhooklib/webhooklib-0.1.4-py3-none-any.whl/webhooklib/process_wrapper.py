import subprocess

from redis import Redis

from webhooklib import config
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult


def run_subprocess(
    command: ShellCommand,
    redis: Redis,
) -> None:
    p = subprocess.Popen(
        command.cmd,
        env=command.env,
        cwd=command.cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        stdout, stderr = p.communicate(timeout=command.timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        stdout, stderr = p.communicate()
        _status = 'subprocess.TimeoutExpired'
    else:
        _status = 'success'

    result = ShellResult(
        status=_status,
        returncode=p.returncode,
        stdout=stdout,
        stderr=stderr,
    )
    redis.lpush(f'{config.PROCESS_DONE}:{command.id}', result.json())
