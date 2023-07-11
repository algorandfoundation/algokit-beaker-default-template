import dataclasses
import logging
import sys
from collections.abc import Callable
from pathlib import Path

from algokit_utils import Account, ApplicationSpecification
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from beaker import Application
from smart_contracts.hello_world import deploy_config, hello_world
from smart_contracts.helpers.build import build
from smart_contracts.helpers.deploy import deploy


@dataclasses.dataclass
class SmartContract:
    app: Application
    deploy: Callable[
        [AlgodClient, IndexerClient, ApplicationSpecification, Account], None
    ] | None = None


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)-10s: %(message)s"
)
logger = logging.getLogger(__name__)
root_path = Path(__file__).parent


def main(action: str) -> None:
    # define contracts to build and/or deploy
    contracts = [SmartContract(app=hello_world.app, deploy=deploy_config.deploy)]
    artifact_path = root_path / "artifacts"
    match action:
        case "build":
            for contract in contracts:
                logger.info(f"Building app {contract.app.name}")
                build(artifact_path / contract.app.name, contract.app)
        case "deploy":
            for contract in contracts:
                logger.info(f"Deploying app {contract.app.name}")
                app_spec_path = artifact_path / contract.app.name / "application.json"
                deploy(app_spec_path, contract.deploy)
        case "all":
            for contract in contracts:
                logger.info(f"Building app {contract.app.name}")
                app_spec_path = build(artifact_path / contract.app.name, contract.app)
                logger.info(f"Deploying {contract.app.name}")
                deploy(app_spec_path, contract.deploy)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("all")
