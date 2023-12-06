import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from smart_contracts.config import contracts
from smart_contracts.helpers.build import build

# # Uncomment the following lines to enable auto generation of AVM Debugger compliant sourceMap and simulation trace file.
# # Learn more about using AlgoKit AVM Debugger to debug your TEAL source codes and inspect varioud kidns of Algorand transactions in atomic groups -> https://github.com/algorandfoundation/algokit-avm-vscode-debugger
# from algokit_utils.config import config
# config.configure(debug=True, trace_all=True)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)-10s: %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Loading .env")
load_dotenv()
root_path = Path(__file__).parent


def main(action: str) -> None:
    artifact_path = root_path / "artifacts"
    match action:
        case "build":
            for contract in contracts:
                logger.info(f"Building app {contract.app.name}")
                build(artifact_path / contract.app.name, contract.app)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("build")
