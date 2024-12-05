#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import typing

from pendingai import Command, Environment
from pendingai.client.client import Client

# Environment-dependent constants are stored in dictionaries as runtime
# app logic uses an environment input optional to control access to the
# different resorce client domains.


class ClientEnvironment:
    """Container class for environment-dependent module constants."""

    DOMAIN: typing.Dict[Environment, str] = {
        Environment.DEVELOPMENT: "https://api.dev.pending.ai/",
        Environment.STAGING: "https://api.stage.pending.ai/",
        Environment.PRODUCTION: "https://api.pending.ai/",
    }
    SERVICE_DOMAIN: typing.Dict[Command, str] = {
        Command.DOCKING: "/docking/v1/",
        Command.GENERATOR: "/generator/v1/",
        Command.RETRO: "/retro/v2/",
        Command.RETROGRAPH: "/retrograph/v1/",
    }


__all__: typing.List[str] = ["ClientEnvironment", "Client"]
