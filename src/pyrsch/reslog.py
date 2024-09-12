from os import getenv
from typing import IO, Any
from sys import stdout, stderr

RES_LOGGERS: dict[str, "ResLogger"] = {}


class ResLogger:
    name: str
    target: IO[Any] | None

    @staticmethod
    def get(name: str) -> "ResLogger":
        if name not in RES_LOGGERS:
            RES_LOGGERS[name] = ResLogger(name)
        return RES_LOGGERS[name]

    @staticmethod
    def __call__(name: str) -> "ResLogger":
        return ResLogger.get(name)

    def __init__(self, name: str, config: str | None = None):
        if config is None:
            config = getenv(f"LOG_{name}") or ""
        self.name = name
        if config == "stdout":
            self.target = stdout
        elif config == "stderr":
            self.target = stderr
        elif config.isspace() or len(config) == 0:
            self.target = None
        else:
            tokens = config.split(":")
            filename = tokens[0]
            filemode = tokens[1] if len(tokens) >= 2 else "w"
            self.target = open(filename, filemode, encoding="utf-8")
        RES_LOGGERS[name] = self

    def print(
        self,
        *values: object,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False,
    ):
        if self.target is not None:
            print(*values, file=self.target, sep=sep, end=end, flush=flush)

    def __nonzero__(self):
        return self.target is not None

RL = ResLogger
