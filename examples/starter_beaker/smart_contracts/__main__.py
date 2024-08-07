import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from smart_contracts._helpers.build import build
from smart_contracts._helpers.config import contracts
from smart_contracts._helpers.deploy import deploy

# Uncomment the following lines to enable auto generation of AVM Debugger compliant sourcemap and simulation trace file.
# Learn more about using AlgoKit AVM Debugger to debug your TEAL source codes and inspect various kinds of
# Algorand transactions in atomic groups -> https://github.com/algorandfoundation/algokit-avm-vscode-debugger
# from algokit_utils.config import config
# config.configure(debug=True, trace_all=True)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)-10s: %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Loading .env")
# For manual script execution (bypassing `algokit project deploy`) with a custom .env,
# modify `load_dotenv()` accordingly. For example, `load_dotenv('.env.localnet')`.
load_dotenv()
root_path = Path(__file__).parent


def main(action: str) -> None:
    artifact_path = root_path / "artifacts"
    match action:
        case "build":
            for contract in contracts:
                logger.info(f"Building app {contract.app.name}")
                build(artifact_path / contract.app.name, contract.app)
        case "deploy":
            for contract in contracts:
                logger.info(f"Deploying app {contract.app.name}")
                app_spec_path = artifact_path / contract.app.name / "application.json"
                if contract.deploy:
                    deploy(app_spec_path, contract.deploy)
        case "all":
            for contract in contracts:
                logger.info(f"Building app {contract.app.name}")
                app_spec_path = build(artifact_path / contract.app.name, contract.app)
                logger.info(f"Deploying {contract.app.name}")
                if contract.deploy:
                    deploy(app_spec_path, contract.deploy)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("all")
