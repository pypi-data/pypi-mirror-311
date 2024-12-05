#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import enum
import logging
import logging.config
import typing

import httpx
from rich.logging import RichHandler

__appname__: str = "pendingai"
__version__: str = "0.0.1"

logging.basicConfig(
    level=logging.WARNING,
    format="%(name)s %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(tracebacks_suppress=[httpx])],
)
logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


@enum.unique
class Environment(str, enum.Enum):
    """
    Deployment environment used for building client connection strings,
    authentication flows for the device or refresh tokens, and controls
    cached state data between different environments
    """

    DEVELOPMENT = "dev"
    STAGING = "stage"
    PRODUCTION = "prod"


@enum.unique
class Command(str, enum.Enum):
    """
    Runtime command used for naming commands and linking the client
    service domain prefix.
    """

    DOCKING = "docking"
    GENERATOR = "generator"
    RETRO = "retro"
    RETROGRAPH = "retrograph"


__all__: typing.List[str] = ["__appname__", "__version_", "Environment", "Command"]
