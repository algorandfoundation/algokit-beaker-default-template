from beaker.application import Application
from beaker.decorators import delete, external
from pyteal import Approve, Bytes, Concat, Cond, Expr, Global, Tmpl, Txn
from pyteal.ast import abi


class HelloWorld(Application):
    @external(read_only=True)
    def hello(self, name: abi.String, *, output: abi.String) -> Expr:
        return output.set(Concat(Tmpl.Bytes("TMPL_GREETING"), Bytes(", "), name.get()))

    @delete
    def delete(self) -> Expr:
        return Cond([Txn.sender() == Global.creator_address(), Approve()])
