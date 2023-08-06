import logging
import os
import secrets
import shutil
from pathlib import Path
from threading import Thread

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from redis import Redis

from webhooklib.dependencies import get_redis_sync
from webhooklib.models import ShellCommand
from webhooklib.process_wrapper import run_subprocess

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get('/')
def health():
    return {'health': 'success'}


@app.post('/')
def run(
    command: ShellCommand, token=Header(),
    redis: Redis = Depends(get_redis_sync),
):
    logger.info(command.json(indent=2))
    if not secrets.compare_digest(token, os.environ['WEBHOOK_TOKEN']):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='access denied: invalid token',
        )
    if shutil.which(command.cmd[0]) is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'command {command.cmd[0]} not found',
        )
    if command.cwd is not None:
        cwd = Path(command.cwd)
        if not (cwd.is_dir() and cwd.exists()):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'directory {command.cwd} not found',
            )

    t = Thread(target=run_subprocess, args=(command, redis))
    t.start()
    return {'process-created': 'ok'}
