#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import enum
import io
import logging
import re
import typing

import httpx
import typer
from rich.console import Console
from rich.table import Table, box
from typing_extensions import Annotated

from pendingai import __appname__

logger: logging.Logger = logging.getLogger(__appname__)

cli: typer.Typer = typer.Typer()
std: Console = Console()

# ----------------------------------------------------------------------

# Shared callback methods and command parameters are defined to be used
# across multiple commands with similar logic. Any help messages are now
# connected at this top-level.


def _query_list_callback(ctx: typer.Context, query_list: typing.Any) -> typing.Any:
    """
    Validate a list of query molecules.

    Args:
        ctx (typer.Context): App context
        query_list (typing.Any): List of query molecule values.

    Raises:
        typer.BadParameter: Query molecule has invalid format.

    Returns:
        typing.Any: Given query molecule list.
    """
    if query_list is not None and isinstance(query_list, typing.List):
        for query in query_list:
            if re.match(r"^[A-Za-z0-9\(\)+-=#%+@\/\\\[\]]+$", query) is None:
                raise typer.BadParameter(f"Invalid format: {query}", param_hint="--smi")
        return query_list
    return []


def _query_file_callback(ctx: typer.Context, query_file: typing.Any) -> typing.Any:
    """
    Validate a file of query molecules.

    Args:
        ctx (typer.Context): App context
        query_id_list (typing.Any): File of query molecule values.

    Raises:
        typer.BadParameter: Query molecule has invalid format.

    Returns:
        typing.Any: Parsed file of query molecules into a list.
    """
    if query_file is not None and isinstance(query_file, io.TextIOWrapper):
        query_file = [q.strip() for q in query_file]
        for query in query_file:
            if re.match(r"^[A-Za-z0-9\(\)+-=#%+@\/\\\[\]]+$", query) is None:
                raise typer.BadParameter(f"Invalid format: {query}", param_hint="--smi")
        return query_file
    return []


def _query_id_list_callback(ctx: typer.Context, query_id_list: typing.Any) -> typing.Any:
    """
    Validate a lList of query ids.

    Args:
        ctx (typer.Context): App context
        query_id_list (typing.Any): list of query id values.

    Raises:
        typer.BadParameter: Query id has invalid format.

    Returns:
        typing.Any: Given query id list.
    """
    if query_id_list is not None and isinstance(query_id_list, typing.List):
        for query in query_id_list:
            if re.match(r"^[a-f\d]{24}$", query) is None:
                raise typer.BadParameter(f"Invalid format: {query}", param_hint="--id")
        return query_id_list
    return []


def _query_id_file_callback(ctx: typer.Context, query_id_file: typing.Any) -> typing.Any:
    """
    Validate a file of query ids.

    Args:
        ctx (typer.Context): App context
        query_id_l"List (typing.Any): File of query id values.

    Raises:
        typer.BadParameter: Query id has invalid format.

    Returns:
        typing.Any: Parsed file of query ids into a l"List.
    """
    if query_id_file is not None and isinstance(query_id_file, io.TextIOWrapper):
        query_id_file = [q.strip() for q in query_id_file]
        for query in query_id_file:
            if re.match(r"^[a-f\d]{24}$", query) is None:
                raise typer.BadParameter(f"Invalid format: {query}", param_hint="--id")
        return query_id_file
    return []


QueryList = Annotated[
    typing.Optional[typing.List[str]],
    typer.Option(
        "--smi",
        help="""Collection of command-line query molecules.""",
        callback=_query_list_callback,
    ),
]
QueryFile = Annotated[
    typing.Optional[typer.FileText],
    typer.Option(
        "--batch-file",
        help="""File (UTF-8 encoded) with line-delimited query molecules.""",
        readable=True,
        encoding="utf-8",
        callback=_query_file_callback,
    ),
]

QueryIdList = Annotated[
    typing.Optional[typing.List[str]],
    typer.Option(
        "--id",
        help="""Collection of command-line query ids.""",
        callback=_query_id_list_callback,
    ),
]
QueryIdFile = Annotated[
    typing.Optional[typer.FileText],
    typer.Option(
        "--batch-file",
        help="""File (UTF-8 encoded) with line-delimited query ids.""",
        readable=True,
        encoding="utf-8",
        callback=_query_id_file_callback,
    ),
]
OutputJson = Annotated[
    typing.Optional[bool],
    typer.Option(
        "--json",
        is_flag=True,
        help="""Output results in a JSON-readable format.""",
    ),
]


# ----------------------------------------------------------------------


@cli.command(
    "engines",
    help="""List the collection of available retrosynthesis engines.""",
)
def engines(ctx: typer.Context, output_json: OutputJson = False) -> None:
    """
    List the collection of available retrosynthesis engines.

    Args:
        ctx (typer.Context): App context.
        output_json (OutputJson, typing.Optional): Flag for STDOUT data to be
            in a JSON-readable format.
    """

    logger.debug("Requesting available retrosynthesis engines")
    response: httpx.Response = ctx.obj.client.get("/engines")

    if response.status_code == 200:
        if output_json:
            std.print_json(response.text)
        else:
            table: Table = Table("Engine ID", "Timestamp", "Name", box=box.ASCII)
            [table.add_row(x["id"], x["created"], x["name"]) for x in response.json()]
            std.print(table)
    else:
        logger.debug(f"Failed with status ({response.status_code}): {response.text}")
        std.print("Your request failed, please wait and try again shortly.")
        raise typer.Exit(1)


# ----------------------------------------------------------------------


@cli.command(
    "libraries",
    help="""List the collection of available building block libraries.""",
)
def libraries(ctx: typer.Context, output_json: OutputJson = False) -> None:
    """
    List the collection of available building block libraries.

    Args:
        ctx (typer.Context): App context.
        output_json (OutputJson, typing.Optional): Flag for STDOUT data to be
            in a JSON-readable format.
    """

    logger.debug("Requesting available building block libraries")
    response: httpx.Response = ctx.obj.client.get("/libraries")

    if response.status_code == 200:
        if output_json:
            std.print_json(response.text)
        else:
            table: Table = Table("Library ID", "Timestamp", "Name", box=box.ASCII)
            [table.add_row(x["id"], x["created"], x["name"]) for x in response.json()]
            std.print(table)
    else:
        logger.debug(f"Failed with status ({response.status_code}): {response.text}")
        std.print("Your request failed, please wait and try again shortly.")
        raise typer.Exit(1)


# ----------------------------------------------------------------------


@enum.unique
class _SynthesisType(str, enum.Enum):
    """Options for the `type_of_plan` parameter."""

    FULL_ROUTE = "FullRoute"
    SINGLE_STEP = "SingleStep"


def _lib_callback(ctx: typer.Context, lib: typing.Any) -> typing.Any:
    """
    Check all building block library ids are valid.

    Args:
        ctx (typer.Context): App context.
        lib (typing.Any, typing.Optional): Building block library ids.

    Raises:
        typer.BadParameter: Library id has invalid format.

    Returns:
        typing.Any: Given library id parameter value.
    """
    if lib is not None and isinstance(lib, str):
        response: httpx.Response = ctx.obj.client.get("/libraries")
        if response.status_code == 200:
            for x in lib:
                if x not in [resp["id"] for resp in response.json()]:
                    raise typer.BadParameter(f"Not found: {x}", param_hint="--library")
        else:
            logger.warning("Unable to retrieve building block library")
            logger.debug(f"Failed with status ({response.status_code}): {response.text}")
            raise typer.Exit(1)
        return lib
    return []


def _eng_callback(ctx: typer.Context, eng: typing.Any) -> typing.Any:
    """
    Check a retrosynthesis engine id is valid.

    Args:
        ctx (typer.Context): App context.
        eng (typing.Any, typing.Optional): Retrosynthesis engine id.

    Raises:
        typer.BadParameter: Engine id has invalid format.

    Returns:
        typing.Any: Given engine id parameter value.
    """
    if eng is not None and isinstance(eng, str):
        if re.match(r"^eng_[\w]*$", eng) is None:
            raise typer.BadParameter(f"Invalid format: {eng}", param_hint="--engine")
        response: httpx.Response = ctx.obj.client.get("/engines")
        if response.status_code == 200:
            if eng not in [x["id"] for x in response.json()]:
                raise typer.BadParameter(f"Not found: {eng}", param_hint="--engine")
        else:
            logger.warning("Unable to retrieve retrosynthesis engines")
            logger.debug(f"Failed with status ({response.status_code}): {response.text}")
            raise typer.Exit(1)
        return eng
    return None


@cli.command(
    "query",
    help="""Submit one or more query molecules to a synthesis engine. When a query is
        submitted, it requires a single synthesis engine, collection of building block
        libraries, and parameters to control synthesis expansion logic. For batched query
        submissions, parameters will be shared by all synthesis procedures.""",
    no_args_is_help=True,
)
def query(
    ctx: typer.Context,
    query_list: QueryList = None,
    query_file: QueryFile = None,
    output_json: OutputJson = False,
    retrosynthesis_engine: Annotated[
        typing.Optional[str],
        typer.Option(
            "--engine",
            help="""Specified synthesis engine used for retrosynthesis MCTS inference. By
                default a random will be selected. See <pendingai retro engines> for all
                available engines.""",
            callback=_eng_callback,
        ),
    ] = None,
    building_block_libraries: Annotated[
        typing.Optional[typing.List[str]],
        typer.Option(
            "--library",
            help="""Specified building block libraries used for constructing synthetic
                routes. By default all libraries will be selected. See <pendingai retro
                libraries> for all available libraries.""",
            callback=_lib_callback,
        ),
    ] = None,
    type_of_plan: Annotated[
        _SynthesisType,
        typer.Option(
            "--plan",
            help="""Type of synthesis plan generated by the query. A `FullRoute` query
                returns a collection of complete synthetic routes, a `SingleStep` query
                returns one synthetic route.""",
        ),
    ] = _SynthesisType.FULL_ROUTE,
    number_of_routes: Annotated[
        int,
        typer.Option(
            "--max-routes",
            help="""Maximum number of routes for the engine to return. The engine may
                return fewer routes if a time limit is met or less than the expected
                number are found.""",
            min=1,
            max=50,
        ),
    ] = 25,
    processing_time: Annotated[
        int,
        typer.Option(
            "--max-time",
            help="""Maximum allowable time for the engine to run for generating the
                requested number of routes.""",
            min=60,
            max=900,
        ),
    ] = 300,
    reaction_limit: Annotated[
        int,
        typer.Option(
            "--reaction-limit",
            help="""Maximum number of times a reaction SMILES can appear within the
                generated synthetic routes.""",
            min=1,
            max=25,
        ),
    ] = 3,
    building_block_limit: Annotated[
        int,
        typer.Option(
            "--block-limit",
            help="""Maximum number of times a building block molecule can appear within
                the generated synthetic routes.""",
            min=1,
            max=25,
        ),
    ] = 3,
) -> None:
    """
    Submit one or more query molecules to a synthesis engine.

    Args:
        ctx (typer.Context): App context.
        query_list (QueryList, typing.Optional): Collection of validated query
            molecules given by the command-line.
        query_file (QueryFile, typing.Optional): Collection of validated query
            molecules given a readable filepath.
        retrosynthesis_engine (str, typing.Optional): Query parameter for the
            retrosynthesis engine.
        building_block_libraries (typing.List[str], typing.Optional): Query parameter
            for the building block libraries.
        type_of_plan (TypeOfPlan, typing.Optional): Query parameter for the
            type of plan.
        number_of_routes (int, typing.Optional): Query parameter for the number
            of routes.
        processing_time (int, typing.Optional): Query parameter for the
            processing time.
        reaction_limit (int, typing.Optional): Query parameter for the reaction
            limit.
        building_block_limit (int, typing.Optional): Query parameter for the
            building block limit.
        output_json (OutputJson, typing.Optional): Flag for STDOUT data to be
            in a JSON-readable format.
    """

    # Build the query parameter body
    queries: typing.List[str] = []
    if query_list is not None:
        queries.extend(query_list)
    if query_file is not None:
        queries.extend(query_file)
    if len(queries) == 0:
        raise typer.BadParameter("At least one molecule is required", param_hint="--smi")
    query_parameters: typing.Dict[str, typing.Any] = {}
    if retrosynthesis_engine:
        query_parameters["retrosynthesis_engine"] = retrosynthesis_engine
    if building_block_libraries:
        query_parameters["building_block_libraries"] = building_block_libraries
    if type_of_plan:
        query_parameters["type_of_plan"] = type_of_plan.value
    if number_of_routes:
        query_parameters["number_of_routes"] = number_of_routes
    if processing_time:
        query_parameters["processing_time"] = processing_time
    if reaction_limit:
        query_parameters["reaction_limit"] = reaction_limit
    if building_block_limit:
        query_parameters["building_block_limit"] = building_block_limit
    body: typing.Dict[str, typing.Any] = {
        "query": queries,
        "parameters": query_parameters,
    }

    # Make the request to the api server and handle by response status
    logger.debug(f"Requesting {len(queries)} query molecules")
    response: httpx.Response = ctx.obj.client.post("/queries", json=body)

    if response.status_code == 200:
        logger.debug("Batch query submission completed successfully")
        if output_json:
            std.print_json(response.text)
        else:
            table: Table = Table("Query", "Molecule", box=box.ASCII)
            [table.add_row(row["id"], row["query"]) for row in response.json()]
            std.print(table)

    elif response.status_code == 202:
        logger.debug("Single query submission completed successfully")
        query_id: str = response.headers.get("Location").split("/")[-2]
        if output_json:
            std.print_json(data={"id": query_id, "molecule": queries[0]})
        else:
            table = Table("Query", "Molecule", box=box.ASCII)
            table.add_row(query_id, queries[0])
            std.print(table)

    elif response.status_code == 400:
        logger.debug(f"Query request contained invalid parameters: {response.text}")
        std.print("Failed to submit thequery, for more information use --help.")
        raise typer.Exit(1)

    elif response.status_code in [402, 429, 503, 401]:
        logger.debug(f"Failed to process the transaction: {response.text}")
        std.print("Billing transaction failed, this may occur for several reasons:")
        std.print("\t• No billing account is attached for this user")
        std.print("\t• Provided billing data is not valid")
        std.print("\t• Billing servers have received too many requests")
        std.print("If the problem persists, please contact service support.")
        raise typer.Exit(1)

    else:
        logger.debug(f"Failed with status ({response.status_code}): {response.text}")
        std.print("Your request failed, please wait and try again shortly.")
        raise typer.Exit(1)


# ----------------------------------------------------------------------


@cli.command(
    "delete",
    help="""Delete one or more retrosynthesis queries by id. If a query does not
        exist, it will be skipped and the remaining queries will be deleted.""",
    no_args_is_help=True,
)
def delete(
    ctx: typer.Context,
    query_id_list: QueryIdList = None,
    query_id_file: QueryIdFile = None,
    output_json: OutputJson = False,
) -> None:
    """
    Delete one or more retrosynthesis queries by id.

    Args:
        ctx (typer.Context): App context.
        query_id_list (QueryIdList, typing.Optional): Collection of validated
            BSON ObjectId query ids given by the command-line.
        query_id_file (QueryIdFile, typing.Optional): Collection of validated
            BSON ObjectId query ids given a readable filepath.
        output_json (OutputJson, typing.Optional): Flag for STDOUT data to be
            in a JSON-readable format.
    """

    # Prepare collection of query ids to process
    query_ids: typing.List[str] = []
    if query_id_list is not None:
        query_ids.extend(query_id_list)
    if query_id_file is not None:
        query_ids.extend(query_id_file)
    if len(query_ids) == 0:
        raise typer.BadParameter("At least one query is required.", param_hint="--id")

    # Iterate over ids, try to delete each, collect results of request
    deletion_success_ids: typing.List[str] = []
    deletion_missing_ids: typing.List[str] = []
    deletion_failure_ids: typing.List[str] = []
    for query_id in query_ids:
        logger.debug(f"Requesting deletion for query with id: {query_id}")
        response: httpx.Response = ctx.obj.client.delete(f"/queries/{query_id}")
        if response.status_code == 204:
            logger.debug(f"Successfully deleted query with id: {query_id}")
            deletion_success_ids.append(query_id)
        elif response.status_code == 404:
            logger.debug(f"Unable to find query with id: {query_id}")
            deletion_missing_ids.append(query_id)
        else:
            logger.warning(f"Request to delete query failed: {query_id}")
            logger.debug(f"Failed with status ({response.status_code}): {response.text}")
            deletion_failure_ids.append(query_id)

    # Output results of the deletion
    if output_json:
        std.print_json(
            data={
                "success": deletion_success_ids,
                "missing": deletion_missing_ids,
                "failure": deletion_failure_ids,
            }
        )
    else:
        table: Table = Table("Query", "Deleted", box=box.ASCII)
        [table.add_row(query_id, "success") for query_id in deletion_success_ids]
        [table.add_row(query_id, "missing") for query_id in deletion_missing_ids]
        [table.add_row(query_id, "failure") for query_id in deletion_failure_ids]
        std.print(table)


# ----------------------------------------------------------------------


@cli.command(
    "status",
    help="""Get the status of one or more retrosynthesis queries by id.""",
    no_args_is_help=True,
)
def status(
    ctx: typer.Context,
    query_id_list: QueryIdList = None,
    query_id_file: QueryIdFile = None,
    output_json: OutputJson = False,
) -> None:
    """
    Get the status of one or more retrosynthesis queries by id.

    Args:
        ctx (typer.Context): App context.
        query_id_list (QueryIdList, typing.Optional): Collection of validated
            BSON ObjectId query ids given by the command-line.
        query_id_file (QueryIdFile, typing.Optional): Collection of validated
            BSON ObjectId query ids given a readable filepath.
        output_json (OutputJson, typing.Optional): Flag for STDOUT data to be
            in a JSON-readable format.
    """

    # Prepare collection of query ids to process
    query_ids: typing.List[str] = []
    if query_id_list is not None:
        query_ids.extend(query_id_list)
    if query_id_file is not None:
        query_ids.extend(query_id_file)
    if len(query_ids) == 0:
        raise typer.BadParameter("At least one query is required.", param_hint="--id")

    # Iterate over ids, try to request each, collect results of request
    results: typing.List[typing.Dict] = []
    for query_id in query_ids:
        logger.debug(f"Requesting status for query with id: {query_id}")
        response: httpx.Response = ctx.obj.client.get(f"/queries/{query_id}/status")
        if response.status_code == 200:
            logger.debug(f"Status retrieved for query with id: {query_id}")
            results.append({"id": query_id, "status": response.json()["status"]})
        elif response.status_code == 303:
            logger.debug(f"Status retrieved for query with id: {query_id}")
            results.append({"id": query_id, "status": "completed"})
        elif response.status_code == 404:
            logger.debug(f"Unable to find query with id: {query_id}")
            results.append({"id": query_id, "status": "not_found"})
        else:
            logger.warning(f"Request for query status failed: {query_id}")
            logger.debug(f"Failed with status ({response.status_code}): {response.text}")
            results.append({"id": query_id, "status": "unknown"})

    # Output results of the requests
    results = sorted(results, key=lambda result: result["status"])
    if output_json:
        std.print_json(data=results)
    else:
        table: Table = Table("Query", "Status", box=box.ASCII)
        [table.add_row(query_id["id"], query_id["status"]) for query_id in results]
        std.print(table)


# ----------------------------------------------------------------------


@cli.command(
    "view",
    help="""Get the results of a one of more retrosynthesis queries by id. Only JSON data
        can be returned from this command. If a query has no results or does not exist,
        the field in the JSON list will be null.""",
    no_args_is_help=True,
)
def view(
    ctx: typer.Context,
    query_id_list: QueryIdList = None,
    query_id_file: QueryIdFile = None,
) -> None:
    """
    Get the results of a one of more retrosynthesis queries by id.

    Args:
        ctx (typer.Context): App context.
        query_id_l (QueryIdList, typing.Optional): Collection of validated
            BSON ObjectId query ids given by the command-line.
        query_id_file (QueryIdFile, typing.Optional): Collection of validated
            BSON ObjectId query ids given a readable filepath.
    """

    # Prepare collection of query ids to process
    query_ids: typing.List[str] = []
    if query_id_list is not None:
        query_ids.extend(query_id_list)
    if query_id_file is not None:
        query_ids.extend(query_id_file)
    if len(query_ids) == 0:
        raise typer.BadParameter("At least one query is required.", param_hint="--id")

    # Iterate over ids, try to request each, collect results of request
    results: typing.List[typing.Dict] = []
    for query_id in query_ids:
        logger.debug(f"Requesting results for query with id: {query_id}")
        response: httpx.Response = ctx.obj.client.get(f"/queries/{query_id}")
        result: typing.Dict[str, typing.Any] = {"id": query_id}
        if response.status_code == 200:
            logger.debug(f"Results retrieved for query with id: {query_id}")
            results.append({**result, **response.json()})
        elif response.status_code == 404:
            logger.debug(f"Unable to find query with id: {query_id}")
            results.append({**result, **{"result": None}})
        else:
            logger.warning(f"Request for query results failed: {query_id}")
            logger.debug(f"Failed with status ({response.status_code}): {response.text}")
            results.append({**result, **{"result": None}})

    # Output results of the requests (json-only)
    std.print_json(data=results)


# ----------------------------------------------------------------------


@cli.command(
    "list",
    help="""Summarise results for one of more retrosynthesis queries by id.""",
    no_args_is_help=True,
)
def summary(
    ctx: typer.Context,
    query_id_list: QueryIdList = None,
    query_id_file: QueryIdFile = None,
) -> None:
    """
    Summarise results for one of more retrosynthesis queries by id.

    Args:
        ctx (typer.Context): App context.
        query_id_list (QueryIdList, typing.Optional): Collection of validated
            BSON ObjectId query ids given by the command-line.
        query_id_file (QueryIdFile, typing.Optional): Collection of validated
            BSON ObjectId query ids given a readable filepath.
    """

    # Prepare collection of query ids to process
    query_ids: typing.List[str] = []
    if query_id_list is not None:
        query_ids.extend(query_id_list)
    if query_id_file is not None:
        query_ids.extend(query_id_file)
    if len(query_ids) == 0:
        raise typer.BadParameter("At least one query is required.", param_hint="--id")

    raise NotImplementedError
