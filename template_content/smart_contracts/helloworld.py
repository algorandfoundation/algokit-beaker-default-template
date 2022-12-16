from beaker.application import Application
from beaker.decorators import Authorize, delete, external
from pyteal import Approve, Bytes, Concat, Expr, Global
from pyteal.ast import abi


class HelloWorld(Application):
    @external(read_only=True)
    def hello(self, name: abi.String, *, output: abi.String) -> Expr:
        return output.set(Concat(Bytes("Hello, "), name.get()))

    @delete(authorize=Authorize.only(Global.creator_address()))
    def delete(self) -> Expr:
        return Approve()
