from pathlib import Path
from typing import Callable, Type

from algosdk.abi.contract import Contract
from beaker.application import Application

from .helloworld.helloworld import HelloWorld

BASE_DIR = Path(__file__).parent

CONTRACTS: dict[str, dict[str, Callable[[], str | tuple[str, str, Contract]] | type[Application]]] = {
    "helloworld": {"helloworld": HelloWorld},
}
