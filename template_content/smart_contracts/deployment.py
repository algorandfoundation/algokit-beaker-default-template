import logging
from pathlib import Path

from algokit_utils.account import get_account
from algokit_utils.app import OnSchemaBreak, OnUpdate, deploy_app, get_creator_apps
from algokit_utils.application_specification import ApplicationSpecification
from algokit_utils.network_clients import get_algod_client, get_indexer_client


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
    round_before_deploy = indexer_client.health()["round"]  # type: ignore[no-untyped-call]

    # deploy the app
    app_client = deploy_app(
        algod_client,
        indexer_client,
        app_spec,
        deployer,
        version="1",
        on_schema_break=OnSchemaBreak.DeleteApp,
        on_update=OnUpdate.UpdateApp,
        allow_delete=True,
        allow_update=True,
    )

    # TODO: get algokit-utils to provide this
    apps = get_creator_apps(indexer_client, deployer)
    app = apps.get(app_spec.contract.name)
    # if only just created, fund smart contract account
    if app.created_at_round > round_before_deploy:
        amount = 10
        logger.info(f"New app created, funding with {amount}")
        fund_response = app_client.fund(amount)
        logging.info(f"Transfer of {amount} to {app_client.app_id} successful: {fund_response.tx_ids[0]}")

