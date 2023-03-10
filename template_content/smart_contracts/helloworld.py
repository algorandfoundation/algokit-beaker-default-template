import beaker
import pyteal as pt

app = beaker.Application("HelloWorld")


@app.external(read_only=True)
def hello(name: pt.abi.String, *, output: pt.abi.String) -> pt.Expr:
    return output.set(pt.Concat(pt.Bytes("Hello, "), name.get()))


@app.delete(authorize=beaker.Authorize.only_creator())
def delete() -> pt.Expr:
    return pt.Approve()

