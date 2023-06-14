import logging

from algokit_utils import (
    Account,
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

from smart_contracts import helloworld

logger = logging.getLogger(__name__)

# define contracts to build and/or deploy
contracts = [helloworld.app]

# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: ApplicationSpecification,
    deployer: Account,
) -> None:
    is_local = is_localnet(algod_client)
    is_main = is_mainnet(algod_client)
    is_test = is_testnet(algod_client)
    match app_spec.contract.name:
        case "HelloWorldApp":
            from smart_contracts.artifacts.HelloWorldApp.client import (
                HelloWorldAppClient,
            )

            app_client = HelloWorldAppClient(
                algod_client,
                creator=deployer,
                indexer_client=indexer_client,
            )
            deploy_response = app_client.deploy(
                on_schema_break=(
                    OnSchemaBreak.AppendApp if is_main else OnSchemaBreak.ReplaceApp
                ),
                on_update=OnUpdate.AppendApp if is_main else OnUpdate.UpdateApp,
                allow_delete=is_main,
                allow_update=is_main,
            )

            # if only just created, fund smart contract account
            if deploy_response.action_taken in [
                OperationPerformed.Create,
                OperationPerformed.Replace,
            ]:
                transfer_parameters = TransferParameters(
                    from_account=deployer,
                    to_address=app_client.app_address,
                    micro_algos=algos_to_microalgos(1),
                )
                logger.info(
                    f"New app created, funding with "
                    f"{transfer_parameters.micro_algos}µ algos"
                )
                transfer(algod_client, transfer_parameters)

            name = "world"
            response = app_client.hello(name=name)
            logger.info(
                f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
                f"with name={name}, received: {response.return_value}"
            )
        case _:
            raise Exception(
                f"Attempt to deploy unknown contract {app_spec.contract.name}"
            )
