from __future__ import annotations

import shlex, subprocess
from pathlib import Path
from pydantic import BaseModel

from rts2prosa.config import RocqConfig


class CompileResult(BaseModel):
    success: bool
    returncode: int
    stdout: str
    stderr: str
    command: str


class RocqCompiler:
    def __init__(self,cfg:RocqConfig):self.cfg=cfg

    def compile(self,file:str|Path)->CompileResult:
        file=Path(file).resolve(); cmd=self.cfg.command.format(file=shlex.quote(str(file)))
        try:
            p=subprocess.run(cmd,shell=True,cwd=str(self.cfg.cwd) if self.cfg.cwd else None,capture_output=True,text=True,timeout=self.cfg.timeout_seconds)
            return CompileResult(success=p.returncode==0,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,command=cmd)
        except subprocess.TimeoutExpired as e:
            return CompileResult(success=False,returncode=124,stdout=e.stdout or "",stderr=(e.stderr or "")+"\nTIMEOUT",command=cmd)
