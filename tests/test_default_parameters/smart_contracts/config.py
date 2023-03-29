import logging

from algokit_utils import (
    Account,
    ApplicationClient,
    ApplicationSpecification,
    OnSchemaBreak,
    OnUpdate,
    OperationPerformed,
    TransferParameters,
    is_localnet,
    transfer,
)
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
    is_local = is_localnet(algod_client)
    match app_spec.contract.name:
        case "HelloWorldApp":
            app_client = ApplicationClient(
                algod_client,
                app_spec,
                creator=deployer,
                indexer_client=indexer_client,
            )
            deploy_response = app_client.deploy(
                on_schema_break=OnSchemaBreak.ReplaceApp if is_local else OnSchemaBreak.Fail,
                on_update=OnUpdate.UpdateApp if is_local else OnUpdate.Fail,
                allow_delete=is_local,
                allow_update=is_local,
            )

            # if only just created, fund smart contract account
            if deploy_response.action_taken in [
                OperationPerformed.Create,
                OperationPerformed.Replace,
            ]:
                transfer_parameters = TransferParameters(
                    from_account=deployer,
                    to_address=app_client.app_address,
                    micro_algos=algos_to_microalgos(10),
                )
                logger.info(f"New app created, funding with {transfer_parameters.micro_algos}µ algos")
                transfer(algod_client, transfer_parameters)

            name = "world"
            response = app_client.call("hello", name=name)
            logger.info(
                f"Called hello on {app_spec.contract.name} ({app_client.app_id}) with name={name}, received: {response.return_value}"
            )
        case _:
            raise Exception(f"Attempt to deploy unknown contract {app_spec.contract.name}")
