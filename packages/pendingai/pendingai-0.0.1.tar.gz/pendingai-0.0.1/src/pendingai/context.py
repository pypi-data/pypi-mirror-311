#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import pathlib
import typing

import pydantic
import typer

from pendingai import Environment
from pendingai.auth import AuthenticationEnvironment, DeviceCode
from pendingai.client import Client


class _AuthenticationContext(pydantic.BaseModel):
    """Authentication context data model."""

    domain: str
    client_id: str
    audience: str


class Context(pydantic.BaseModel):
    """Runtime application context data model."""

    app_name: str
    environment: Environment
    api_key: typing.Optional[str] = None
    client: typing.Optional[Client] = None

    model_config = {"arbitrary_types_allowed": True}

    @pydantic.computed_field  # type: ignore
    @property
    def authentication(self) -> _AuthenticationContext:
        """Computed field for `authentication`."""
        return _AuthenticationContext(
            domain=AuthenticationEnvironment.DOMAIN[self.environment],
            client_id=AuthenticationEnvironment.CLIENT_ID[self.environment],
            audience=AuthenticationEnvironment.AUDIENCE[self.environment],
        )

    @authentication.setter
    def authentication(self, environment: Environment) -> None:
        """Setter for `authentication`. Takes `environment`."""
        self.environment = environment

    @pydantic.computed_field  # type: ignore
    @property
    def app_dir(self) -> pathlib.Path:
        """Computed field for `app_dir`."""
        pth: str = typer.get_app_dir(self.app_name, force_posix=True)
        pathlib.Path(pth).mkdir(parents=True, exist_ok=True)
        return pathlib.Path(pth)

    @app_dir.setter
    def app_dir(self, app_name: str) -> None:
        """Setter for `app_dir`. Takes `app_name`."""
        self.app_name = app_name

    @pydantic.computed_field  # type: ignore
    @property
    def cache_pth(self) -> pathlib.Path:
        """Computed field for `cache_pth`."""
        return self.app_dir / f".{self.environment.value}.cache"

    @cache_pth.setter
    def cache_pth(
        self, new_value: typing.Tuple[typing.Optional[str], typing.Optional[Environment]]
    ) -> None:
        """Setter for `cache_pth`. Takes `(app_name, environment)`."""
        app_name, environment = new_value
        self.app_name = app_name if app_name else self.app_name
        self.environment = environment if environment else self.environment

    @pydantic.computed_field  # type: ignore
    @property
    def device_code(self) -> typing.Optional[DeviceCode]:
        """Computed field for `device_code`."""
        try:
            if self.cache_pth.exists() and self.cache_pth.is_file():
                contents: typing.Any = json.load(self.cache_pth.open("r"))
                device_code: DeviceCode = DeviceCode.model_validate(contents)
                return device_code
        except (json.JSONDecodeError, pydantic.ValidationError):
            return None

    @pydantic.computed_field  # type: ignore
    @property
    def access_token(self) -> typing.Optional[str]:
        """Computed field for `access_token`."""
        if self.api_key is not None:
            return self.api_key
        if self.device_code is not None:
            return self.device_code.access_token
        return None


__all__: typing.List[str] = ["Context"]
