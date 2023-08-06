import uuid

from pydantic import BaseModel
from pydantic import Field


class ShellCommand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cmd: list[str]
    env: dict[str, str] | None = None
    cwd: str | None = None
    timeout: float | None = None


class ShellResult(BaseModel):
    status: str
    returncode: int
    stdout: str
    stderr: str

    def pprint(self):
        print('status:', self.status)
        print('returncode:', self.returncode)
        print('stdout:', '=' * 50)
        print(self.stdout)
        print('stderr:', '=' * 50)
        print(self.stderr)
