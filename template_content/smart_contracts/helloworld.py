from beaker import Application, Authorize
from pyteal import Approve, Bytes, Concat, Expr, Global, abi

app = Application("HelloWorld")


@app.external(read_only=True)
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))


@app.delete(authorize=Authorize.only(Global.creator_address()))
def delete() -> Expr:
    return Approve()
