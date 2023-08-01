import dataclasses
from collections.abc import Callable

from algokit_utils import Account, ApplicationSpecification
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from beaker import Application

from smart_contracts.hello_world.contract import app as hello_world_app
from smart_contracts.hello_world.deploy_config import deploy as hello_world_deploy


@dataclasses.dataclass
class SmartContract:
    app: Application
    deploy: Callable[
        [AlgodClient, IndexerClient, ApplicationSpecification, Account], None
    ] | None = None


# define contracts to build and/or deploy
contracts = [SmartContract(app=hello_world_app, deploy=hello_world_deploy)]
