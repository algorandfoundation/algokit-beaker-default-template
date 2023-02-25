from beaker import Application, Authorize
from beaker.client import ApplicationClient
from beaker.sandbox import get_algod_client
from beaker.sandbox.kmd import get_accounts
from pyteal import Approve, Bytes, Concat, Expr, Global, abi

app = Application("HelloWorld")


@app.external(read_only=True)
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.delete(authorize=Authorize.only(Global.creator_address()))
def delete() -> Expr:
    return Approve()


app.build().export("./artifacts")

accounts = get_accounts()
sender = accounts[0]

app_client = ApplicationClient(
    client=get_algod_client(), app=app, sender=sender.address, signer=sender.signer
)

app_client.create()
return_value = app_client.call(hello, name="Beaker").return_value
print(return_value)
