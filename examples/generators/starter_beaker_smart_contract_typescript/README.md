# starter_beaker_smart_contract_typescript

This project has been generated using AlgoKit. See below for default getting started instructions.

# Setup

### Pre-requisites

- [Python 3.10+](https://www.python.org/downloads/) (we recommended 3.12+)
- [Docker](https://www.docker.com/) (for LocalNet only)

> For interactive tour over the codebase, download [vsls-contrib.codetour](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) extension for VS Code, then open the [`.codetour.json`](./.tours/getting-started-with-your-algokit-project.tour) file in code tour extension.

### Initial Setup

#### 1. Clone the Repository
Start by cloning this repository to your local machine.

#### 2. Install Pre-requisites
Ensure the following pre-requisites are installed and properly configured:

- **Docker**: Required for running a local Algorand network. [Install Docker](https://www.docker.com/).
- **AlgoKit CLI**: Essential for project setup and operations. Install the latest version from [AlgoKit CLI Installation Guide](https://github.com/algorandfoundation/algokit-cli#install). Verify installation with `algokit --version`, expecting `2.0.0` or later.

#### 3. Bootstrap Your Local Environment
Run the following commands within the project folder:

- **Install Poetry**: Required for Python dependency management. [Installation Guide](https://python-poetry.org/docs/#installation). Verify with `poetry -V` to see version `1.2`+.
- **Setup Project**: Execute `algokit project bootstrap all` to install dependencies and setup a Python virtual environment in `.venv`.
- **Configure environment**: Execute `algokit generate env-file -a target_network localnet` to create a `.env.localnet` file with default configuration for `localnet`.
- **Start LocalNet**: Use `algokit localnet start` to initiate a local Algorand network.

### Development Workflow

#### Terminal
Directly manage and interact with your project using AlgoKit commands:

1. **Build Contracts**: `algokit project run build` compiles all smart contracts.
2. **Deploy**: Use `algokit project deploy localnet` to deploy contracts to the local network.

#### VS Code 
For a seamless experience with breakpoint debugging and other features:

1. **Open Project**: In VS Code, open the repository root.
2. **Install Extensions**: Follow prompts to install recommended extensions.
3. **Debugging**:
   - Use `F5` to start debugging.
   - **Windows Users**: Select the Python interpreter at `./.venv/Scripts/python.exe` via `Ctrl/Cmd + Shift + P` > `Python: Select Interpreter` before the first run.

#### JetBrains IDEs
While primarily optimized for VS Code, JetBrains IDEs are supported:

1. **Open Project**: In your JetBrains IDE, open the repository root.
2. **Automatic Setup**: The IDE should configure the Python interpreter and virtual environment.
3. **Debugging**: Use `Shift+F10` or `Ctrl+R` to start debugging. Note: Windows users may encounter issues with pre-launch tasks due to a known bug. See [JetBrains forums](https://youtrack.jetbrains.com/issue/IDEA-277486/Shell-script-configuration-cannot-run-as-before-launch-task) for workarounds.

## AlgoKit Workspaces and Project Management
This project supports both standalone and monorepo setups through AlgoKit workspaces. Leverage [`algokit project run`](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/project/run.md) commands for efficient monorepo project orchestration and management across multiple projects within a workspace.

## AlgoKit Generators

This template provides a set of [algokit generators](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/generate.md) that allow you to further modify the project instantiated from the template to fit your needs, as well as giving you a base to build your own extensions to invoke via the `algokit generate` command.

### Generate Smart Contract 

By default the template creates a single `HelloWorld` contract under hello_world folder in the `smart_contracts` directory. To add a new contract:

1. From the root of the project (`../`) execute `algokit generate smart-contract`. This will create a new starter smart contract and deployment configuration file under `{your_contract_name}` subfolder in the `smart_contracts` directory.
2. Each contract potentially has different creation parameters and deployment steps. Hence, you need to define your deployment logic in `deploy-config.ts`file.
3. `config.py` file will automatically build all contracts in the `smart_contracts` directory. If you want to build specific contracts manually, modify the default code provided by the template in `config.py` file.
4. Since you are generating a TypeScript client, you also need to reference your contract deployment logic in `index.ts` file. However, similar to config.py, by default, `index.ts` will auto import all TypeScript deployment files under `smart_contracts` directory. If you want to manually import specific contracts, modify the default code provided by the template in `index.ts` file.

> Please note, above is just a suggested convention tailored for the base configuration and structure of this template. The default code supplied by the template in `config.py` and `index.ts` (if using ts clients) files are tailored for the suggested convention. You are free to modify the structure and naming conventions as you see fit.

### Generate '.env' files

By default the template instance does not contain any env files. Using [`algokit project deploy`](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/project/deploy.md) against `localnet` | `testnet` | `mainnet` will use default values for `algod` and `indexer` unless overwritten via `.env` or `.env.{target_network}`. 

To generate a new `.env` or `.env.{target_network}` file, run `algokit generate env-file`

# Tools

This project makes use of Python to build Algorand smart contracts. The following tools are in use:

- [Algorand](https://www.algorand.com/) - Layer 1 Blockchain; [Developer portal](https://developer.algorand.org/), [Why Algorand?](https://developer.algorand.org/docs/get-started/basics/why_algorand/)
- [AlgoKit](https://github.com/algorandfoundation/algokit-cli) - One-stop shop tool for developers building on the Algorand network; [docs](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md), [intro tutorial](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/tutorials/intro.md)
- [Beaker](https://github.com/algorand-devrel/beaker) - Smart contract development framework for PyTeal; [docs](https://beaker.algo.xyz), [examples](https://github.com/algorand-devrel/beaker/tree/master/examples)
- [PyTEAL](https://github.com/algorand/pyteal) - Python language binding for Algorand smart contracts; [docs](https://pyteal.readthedocs.io/en/stable/)
- [AlgoKit Utils](https://github.com/algorandfoundation/algokit-utils-ts) - A set of core Algorand utilities that make it easier to build solutions on Algorand.
- [Poetry](https://python-poetry.org/): Python packaging and dependency management.
- [npm](https://www.npmjs.com/): Node.js package manager.
- [TypeScript](https://www.typescriptlang.org/): Strongly typed programming language that builds on JavaScript.
- [ts-node-dev](https://github.com/wclr/ts-node-dev): TypeScript development execution environment.

It has also been configured to have a productive dev experience out of the box in [VS Code](https://code.visualstudio.com/), see the [.vscode](./.vscode) folder.
- [AlgoKit Tealer Integration](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/tasks/analyze.md): AlgoKit Tealer Integration is a feature in the CLI that allows you to run [Tealer](https://github.com/crytic/tealer) static analyzer on your TEAL
source code. The invocation of this command is included in:
- The github actions workflow file.
- A VSCode task ('Shift+CMD|CTRL+P' and search for 'Tasks: Run Task' and select 'Analyze TEAL contracts with AlgoKit Tealer integration').
- A `pre-commit` hook (if you have enabled `pre-commit` in your project). 
