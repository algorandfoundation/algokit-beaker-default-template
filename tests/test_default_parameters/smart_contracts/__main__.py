import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from smart_contracts import config
from smart_contracts.helpers.build import build
from smart_contracts.helpers.deploy import deploy

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)-10s: %(message)s")
logger = logging.getLogger(__name__)
logger.info("Loading .env")
load_dotenv()
root_path = Path(__file__).parent


def main(action: str) -> None:
    artifact_path = root_path / "artifacts"
    match action:
        case "build":
            for app in config.contracts:
                logger.info(f"Building app {app.name}")
                build(artifact_path / app.name, app)

        case "deploy":
            for app in config.contracts:
                logger.info(f"Building app {app.name}")
                app_spec_path = artifact_path / app.name / "application.json"
                deploy(app_spec_path, config.deploy)
        case "all":
            for app in config.contracts:
                logger.info(f"Building app {app.name}")
                app_spec_path = build(artifact_path / app.name, app)
                logger.info(f"Deploying {app.name}")
                deploy(app_spec_path, config.deploy)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("all")
