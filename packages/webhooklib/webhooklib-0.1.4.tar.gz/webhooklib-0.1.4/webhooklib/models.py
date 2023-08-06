import uuid
from pathlib import Path

from pydantic import BaseModel
from pydantic import Field


class ShellCommand(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    cmd: list[str]
    env: dict[str, str] | None = None
    cwd: str = str(Path.home())
    timeout: float | None = None


class ShellResult(BaseModel):
    status: str
    returncode: int
    stdout: str
    stderr: str
