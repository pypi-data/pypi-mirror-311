#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import typing

import httpx
import typer
from rich.console import Console

from pendingai import Command
from pendingai.client import Client, ClientEnvironment

std: Console = Console()


def add_client_callback(ctx: typer.Context):
    """
    Auxiliary callback method for calling command callback methods with
    a static service domain determined by the `Command` set in `main.py`
    and verified access permission by hitting the service `/alive`.

    Args:
        ctx (typer.Context): App runtime context.
    """
    command: Command = Command._value2member_map_[ctx.command.name]  # type: ignore
    ctx.obj.client = Client(
        domain=ClientEnvironment.DOMAIN[ctx.obj.environment],
        service_domain=ClientEnvironment.SERVICE_DOMAIN[command],
        access_token=ctx.obj.access_token,
    )
    response: httpx.Reponse = ctx.obj.client.get("/alive")
    if response.status_code != 200:
        std.print(
            f"User is not authorized for the '{ctx.command.name}' Platform. "
            + "Try logging in again. If the problem is unexpected, contact support "
            + "services (see <pendingai --help>).",
            width=90,
            highlight=False,
        )
        raise typer.Exit(2)


__all__: typing.List[str] = ["add_client_callback"]
