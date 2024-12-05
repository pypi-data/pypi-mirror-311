#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import logging
import pathlib
import typing
from datetime import datetime

import click
import typer
from rich.console import Console
from typing_extensions import Annotated

from pendingai import Command, Environment, __appname__, __version__
from pendingai.auth import DeviceCode, DeviceCodeAuthorization
from pendingai.commands import add_client_callback, retro
from pendingai.context import Context

logger: logging.Logger = logging.getLogger(__appname__)
console: Console = Console()


# Global callback methods are defined which are used in this top-level
# typer application. They execute either prior to (taking arguments in-
# front of a command) or after an application command.


@click.pass_context
def _result_callback(ctx: typer.Context, result: typing.Any, *_, **__) -> None:
    """
    Cleanup actions for the completed command that does not exit.

    Args:
        ctx (typer.Context): App context.
        result (typing.Any): Return result from the executing command.
    """
    raise typer.Exit(0)


def _clear_cache_callback(clear_cache: typing.Optional[bool]) -> None:
    """
    Variable callback for the `--clear-cache` callback optional. Delete
    the cache file and exit.

    Args:
        clear_cache (typing.Optional[bool]): Callback optional.
    """
    if clear_cache:
        app_dir: str = typer.get_app_dir(__appname__, force_posix=True)
        for cache_filepath in pathlib.Path(app_dir).iterdir():
            if cache_filepath.is_file():
                logger.debug(f"Deleting cache file: {cache_filepath}")
                cache_filepath.unlink(missing_ok=True)
        raise typer.Exit(0)


def _version_callback(version: typing.Optional[bool]) -> None:
    """
    Variable callback for the `--version` callback optional. Print the
    application version to stdout and exit.

    Args:
        version (typing.Optional[bool]): Callback optional.
    """
    if version:
        console.print(__version__)
        raise typer.Exit(0)


def _callback(
    ctx: typer.Context,
    environment: Annotated[
        Environment,
        typer.Option(
            "--env",
            show_default=False,
            envvar="PENDINGAI_ENVIRONMENT",
            help="""Environment used for executing the command. The environment matches
                the authenticating service request and connected HTTP client domain.""",
        ),
    ] = Environment.PRODUCTION,
    clear_cache: Annotated[
        typing.Optional[bool],
        typer.Option(
            "--clear-cache",
            is_eager=True,
            callback=_clear_cache_callback,
            help="""Clear the application cache and exit.""",
        ),
    ] = None,
    version: Annotated[
        typing.Optional[bool],
        typer.Option(
            "--version",
            is_eager=True,
            callback=_version_callback,
            help="""Show the application version and exit.""",
        ),
    ] = None,
    api_key: Annotated[
        typing.Optional[str],
        typer.Option(
            "--api-key",
            help="""Override cached access tokens for platform access.""",
        ),
    ] = None,
    debug: Annotated[
        typing.Optional[bool],
        typer.Option(
            "--debug",
            is_flag=True,
            envvar="PENDINGAI_DEBUG",
            help="""Output debug logging.""",
        ),
    ] = False,
) -> None:
    """
    Main application callback prior to executing commands. Responsible
    for setting up the global app context. Handles authetication logic
    by catching whether an access token if provided for requests.

    Args:
        ctx (typer.Context): App context.
        environment (Environment, optional): Runtime environment used to
            authenticate requests, select the matching domain name for
            routing HTTP requests and storing cached data.
        clear_cache (bool, optional): Flag to clear the cache using the
            attached callback method and then exit early from the app.
        version (bool, optional): Flag to display the app version
            attached callback method and then exit early from the app.
        api_key (str, optional): API access token to override any cached
            local values generated with the <pendingai login> command.
        debug (bool, optional): Set the debug level logging to DEBUG for
            the runtime environment.
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Runtime debug profiling enabled")
    ctx.obj = Context(app_name=__appname__, environment=environment)
    if api_key is not None:
        logger.debug("Using provided api-key for authorized platform access")
        ctx.obj.api_key = api_key
    if ctx.obj.access_token is None and ctx.invoked_subcommand != "login":
        logger.debug("Access to the Pending.ai Platform requires the user to login")
        console.print("No authenticated profile found. Try <pendingai login>")

        raise typer.Exit(1)


# Typer application definition uses the above callback methods prior to
# executing a command routine. Imported command typer arguments are also
# appended to the main runtime CLI.

cli: typer.Typer = typer.Typer(
    name=__appname__,
    help="""Pending.ai Cheminformatics Platform CLI tool. Access to Pending.ai services
        requires users to have a registered account. Visit https://lab.pending.ai/ to
        sign up now. For more information about our platform, see
        https://docs.pending.ai/.""",
    epilog="""If you encounter any problems using the Pending.ai CLI tool, please submit
        a support ticket at https://pendingai.atlassian.net/servicedesk/ or contact a
        service representative via email to contact@pending.ai. Feature requests can be
        submitted at https://github.com/pendingai/pendingai-cli.""",
    callback=_callback,
    result_callback=_result_callback,
    add_completion=False,
    pretty_exceptions_enable=False,
    rich_markup_mode=None,
    no_args_is_help=True,
)
cli.add_typer(
    retro.cli,
    name=Command.RETRO.value,
    callback=add_client_callback,
    no_args_is_help=True,
    short_help="""Access to Pending.ai Retrosynthesis Platform commands.""",
    help="""Pending.ai Retrosynthesis Platform. The tool provides a collection of engines
        and building block libraries available for submitting and viewing synthesis
        queries.""",
    epilog="""See https://docs.pending.ai/readme/retrosynthesis for more information
        about the Retrosynthesis Platform.""",
)


@cli.command(
    name="login",
    help="""Login to the Pending.ai Cheminformatics Platform. Cached access information
        will be stored locally. Clear your cache with <pendingai --clear-cache> to reset
        your stored access data.""",
)
def login(
    ctx: typer.Context,
    override_cache: Annotated[
        bool,
        typer.Option(
            "--override-cache",
            is_flag=True,
            help="""Flag to override cached access data for authenticated service access.
                The device will be authenticated if no api-key if provided.""",
        ),
    ] = False,
) -> None:
    """
    Authenticate the device if there is no cached access token available
    or no api-key is given. Attempt to refresh the access token if the
    expiry time is met.

    Args:
        ctx (typer.Context): App context.
        override_cache (bool): Flag to override the cached access token.
    """
    authorizer: DeviceCodeAuthorization = DeviceCodeAuthorization(
        domain=ctx.obj.authentication.domain,
        client_id=ctx.obj.authentication.client_id,
        audience=ctx.obj.authentication.audience,
    )
    if ctx.obj.access_token is not None:
        logger.debug("Autheticated api-key provided, skipping authentication")
        return

    # Check for available user data for the access tokens on the device
    logger.debug(f"Accessing cached access token for user: {ctx.obj.environment.value}")
    try:
        device_code: DeviceCode
        if ctx.obj.device_code is None:
            logger.debug("No cached access token exists for the user")
            device_code = authorizer.execute_flow()
        elif override_cache:
            logger.debug("Overriding cached access token for the user")
            device_code = authorizer.execute_flow()
        elif ctx.obj.device_code.is_expired():
            ts: datetime = datetime.fromtimestamp(ctx.obj.device_code.expires_at)
            logger.debug(f"Found expired cached user token for user with expiry: {ts}")
            try:
                logger.debug("Attempting user access token refresh")
                device_code = authorizer.refresh_token(ctx.obj.device_code.refresh_token)
            except Exception as _:
                logger.warning("Failed to refresh access token, requesting new code")
                device_code = authorizer.execute_flow()
        else:
            ts = datetime.fromtimestamp(ctx.obj.device_code.expires_at)
            logger.debug(f"Existing cached access token found with expiry: {ts}")
            device_code = ctx.obj.device_code
        # Save device code to cache file
        with open(ctx.obj.cache_pth, "w") as cache_fp:
            logger.debug(f"Saving access token to cache file: {ctx.obj.cache_pth}")
            json.dump(device_code.model_dump(), cache_fp)
    except RuntimeError as _:
        typer.Exit(1)


if __appname__ == "__main__":
    cli()
