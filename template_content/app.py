from beaker import *
from pyteal import *

app = Application("HelloWorld")


@app.external(read_only=True)
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.delete(authorize=Authorize.only(Global.creator_address()))
def delete() -> Expr:
    return Approve()


app.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_client.create()
return_value = app_client.call(hello, name="Beaker").return_value
print(return_value)
