import logging

from algokit_utils.account import Account
from algokit_utils.app import DeployAction, OnSchemaBreak, OnUpdate, deploy_app
from algokit_utils.application_specification import ApplicationSpecification
from algokit_utils.network_clients import is_sandbox
from algokit_utils.transfer import TransferParameters, transfer
from algosdk.util import algos_to_microalgos
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.helloworld import app as helloworld_app

logger = logging.getLogger(__name__)

# define contracts to build and/or deploy
contracts = [helloworld_app]


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: ApplicationSpecification,
    deployer: Account,
) -> None:
    # TODO: function that returns environment
    is_localnet = is_sandbox(algod_client)
    match app_spec.contract.name:
        case "HelloWorldApp":
            deploy_response = deploy_app(
                algod_client,
                indexer_client,
                app_spec,
                deployer,
                version="v1.0",
                on_schema_break=OnSchemaBreak.ReplaceApp,
                on_update=OnUpdate.UpdateApp,
                allow_delete=is_localnet,
                allow_update=is_localnet,
            )
            app_client = deploy_response.client

            # if only just created, fund smart contract account
            if deploy_response.action_taken in [
                DeployAction.Created,
                DeployAction.Replaced,
            ]:
                transfer_parameters = TransferParameters(
                    deployer, app_client.app_address, amount=algos_to_microalgos(10)
                )
                logger.info(
                    f"New app created, funding with {transfer_parameters.amount}µ algos"
                )
                transfer(transfer_parameters, algod_client)
