# Pending.ai CLI

Owner: @JBercich

Command-line tool for using the Pending.ai Cheminformatics Platform.

- [`retro`](#retrosynthesis-platform) - Molecule retrosynthesis using machine-learning MCTS inference for generating synthesis routes.

## Getting Started

> [!NOTE]
> The pending.ai CLI will soon be available on PyPi.

### Build from Source

The CLI tool can be built using the `poetry` build tool. Clone the repository locally
and install the package for immediate use.

```shell
git clone https://github.com/pendingai/pendingai-cli.git
cd pendingai-cli
pip install poetry
poetry build
poetry install
```

The CLI can be used by now running `pendingai --help` to display the available commands.

```shell
pendingai --version
> 0.0.1
```

### Authenticating the Client

> [!WARNING]
> To authenticate against different environments, use `pendingai --env <envname> login`
> to generate access tokens for different authenticate tenants.

Authorised platform access requires a valid set of user credentials. You can register a
device code using `pendingai login` to retrieve and cache an access token to use the
different services.

### Retrosynthesis Platform

```shell
pendingai retro --help
```

The Pending.ai retrosynthesis service requires authentication credentials with attached
billing information to submit query molecules for synthesis. You will be notified if the
billed `query` request fails with no charge.

Below are some typical use cases:

```shell
# Inspect available engines and libraries for synthesis requests
pendingai retro engines
pendingai retro libraies

# Submit a query molecule and inspect the results
pendingai retro query --smi <molecule>
pendingai retro status --id <query-id>
pendingai retro view --id <query-id> --json > result.json

# Submit a file batch of results
pendingai retro query --batch-file <smi-filepath>
pendingai retro status --batch-file <ids-filepath>
pendingai retro view --batch-file <ids-filepath> --json > results.json
```
