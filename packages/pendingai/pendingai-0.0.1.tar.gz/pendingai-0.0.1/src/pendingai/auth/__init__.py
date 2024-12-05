#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import typing

from pendingai import Environment
from pendingai.auth.device_code import DeviceCode, DeviceCodeAuthorization

# Environment-dependent constants are stored in dictionaries as runtime
# app logic uses an environment input optional to control access to the
# different resorce authentication tenants.


class AuthenticationEnvironment:
    """Container class for environment-dependent module constants."""

    DOMAIN: typing.Dict[Environment, str] = {
        Environment.DEVELOPMENT: "pendingai-dev.au.auth0.com",
        Environment.STAGING: "pendingai-stage.au.auth0.com",
        Environment.PRODUCTION: "pendingai.us.auth0.com",
    }
    CLIENT_ID: typing.Dict[Environment, str] = {
        Environment.DEVELOPMENT: "GM1gfvGCnokIySbVO7vjmkRy4tVx5WYm",
        Environment.STAGING: "PDWKoudtiP4WZV7aQt5YZbb5xlcmN6ju",
        Environment.PRODUCTION: "dH69BCxGo4MyCcMWi64ZBq2YZx3UIoh1",
    }
    AUDIENCE: typing.Dict[Environment, str] = {
        Environment.DEVELOPMENT: "api.dev.pending.ai/external-api",
        Environment.STAGING: "api.stage.pending.ai/external-api",
        Environment.PRODUCTION: "api.pending.ai/external-api",
    }


__all__: typing.List[str] = [
    "AuthenticationEnvironment",
    "DeviceCodeAuthorization",
    "DeviceCode",
]
