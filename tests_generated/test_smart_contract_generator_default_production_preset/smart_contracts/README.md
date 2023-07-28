## How to add new smart contracts?

By the default the template creates a single `HelloWorld` contract under hello_world folder in the `smart_contracts` directory. To add a new contract:

1. Create a new folder under `smart_contracts` directory and add define your new contract in `contract.py` file.
2. Each contract has potentially has different creation parameters and deployment steps. Hence, you need to define your deployment logic in `deploy_config.py`file.
3. Reference your contract in `config.py` file. This will tell instruct the helper scripts on which exact contracts require building and generation of typed clients.

> Please note, above is just a suggested convention tailored for the base configuration and structure of this template. You are free to modify the structure and naming conventions as you see fit.
