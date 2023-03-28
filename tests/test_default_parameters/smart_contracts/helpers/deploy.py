import logging
from collections.abc import Callable
from pathlib import Path

from algokit_utils import (
    Account,
    ApplicationSpecification,
    get_account,
    get_algod_client,
    get_indexer_client,
)
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

logger = logging.getLogger(__name__)


def deploy(
    app_spec_path: Path,
    deploy_callback: Callable[[AlgodClient, IndexerClient, ApplicationSpecification, Account], None],
    deployer_initial_funds: int = 10000,
) -> None:
    # get clients
    # by default client configuration is loaded from environment variables
    algod_client = get_algod_client()
    indexer_client = get_indexer_client()

    # get app spec
    app_spec = ApplicationSpecification.from_json(app_spec_path.read_text())

    # get deployer account by name, and fund if necessary
    deployer = get_account(algod_client, "DEPLOYER", fund_with_algos=deployer_initial_funds)

    # use provided callback to deploy the app
    deploy_callback(algod_client, indexer_client, app_spec, deployer)
