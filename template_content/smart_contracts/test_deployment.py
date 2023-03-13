from pathlib import Path

from algokit_utils.account import get_account
from algokit_utils.app import OnUpdate, deploy_app
from algokit_utils.logic_error import LogicException
from algokit_utils.network_clients import get_algod_client, get_indexer_client
from dotenv import load_dotenv

from smart_contracts.helloworld import app


def test_deployment() -> None:
    # locate deployment settings
    root_path = Path(__file__).parent / ".."
    env_path = root_path / "smart_contracts" / ".env"
    # load .env into process environment variables
    load_dotenv(env_path)

    # get clients
    # by default client configuration is loaded from environment variables
    algod_client = get_algod_client()
    indexer_client = get_indexer_client()

    app_spec = app.build(algod_client)

    # get creator account by name
    creator_name = "helloworld_creator"
    creator = get_account(algod_client, creator_name)

    # deploy the app
    deploy_app(
        algod_client,
        indexer_client,
        app_spec,
        creator,
        version="1",
        allow_delete=True,
        allow_update=True,
    )

    # redeploy the app, but now make it immutable
    deploy_app(
        algod_client,
        indexer_client,
        app_spec,
        creator,
        version="2",
        allow_delete=True,
        allow_update=False,
    )

    # this will fail
    try:
        # try to make it updatable again
        deploy_app(
            algod_client,
            indexer_client,
            app_spec,
            creator,
            version="3",
            allow_delete=True,
            allow_update=True,
        )
    except LogicException:
        pass

    # deploy with OnUpdate.DeleteApp so we can replace it
    deploy_app(
        algod_client,
        indexer_client,
        app_spec,
        creator,
        version="4",
        on_update=OnUpdate.DeleteApp,
        allow_delete=True,
        allow_update=True,
    )
