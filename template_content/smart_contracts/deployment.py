import logging
from pathlib import Path

from algokit_utils.account import get_account
from algokit_utils.app import DeployAction, OnSchemaBreak, OnUpdate, deploy_app
from algokit_utils.application_specification import ApplicationSpecification
from algokit_utils.network_clients import get_algod_client, get_indexer_client
from algosdk.util import algos_to_microalgos

logger = logging.getLogger(__name__)


def deploy(app_spec_path: Path) -> None:
    # get clients
    # by default client configuration is loaded from environment variables
    algod_client = get_algod_client()
    indexer_client = get_indexer_client()

    # get app spec
    app_spec = ApplicationSpecification.from_json(app_spec_path.read_text())

    # get deployer account by name
    deployer = get_account(algod_client, "deployer", fund_with=10000)

    # deploy the app
    deploy_response = deploy_app(
        algod_client,
        indexer_client,
        app_spec,
        deployer,
        version="1",
        on_schema_break=OnSchemaBreak.ReplaceApp,
        on_update=OnUpdate.UpdateApp,
        allow_delete=True,
        allow_update=True,
    )
    app_client = deploy_response.client

    # if only just created, fund smart contract account
    if deploy_response.action_taken in [DeployAction.Created, DeployAction.Replaced]:
        amount = algos_to_microalgos(10)
        logger.info(f"New app created, funding with {amount}µ algos")
        fund_response = app_client.fund(amount)
        logging.info(
            f"Transfer of {amount}µ algos to {app_client.app_id} successful: {fund_response.tx_ids[0]}"
        )
