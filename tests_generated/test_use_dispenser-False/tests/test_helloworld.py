import pytest
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient

from smart_contracts import helloworld


@pytest.fixture(scope="session")
def helloworld_app_spec(algod_client: AlgodClient) -> ApplicationSpecification:
    return helloworld.app.build(algod_client)


@pytest.fixture(scope="session")
def helloworld_client(
    algod_client: AlgodClient, helloworld_app_spec: ApplicationSpecification
) -> ApplicationClient:
    client = ApplicationClient(
        algod_client,
        app_spec=helloworld_app_spec,
        signer=get_localnet_default_account(algod_client),
        template_values={"UPDATABLE": 1, "DELETABLE": 1},
    )
    client.create()
    return client


def test_says_hello(helloworld_client: ApplicationClient) -> None:
    result = helloworld_client.call(helloworld.hello, name="World")

    assert result.return_value == "Hello, World"
