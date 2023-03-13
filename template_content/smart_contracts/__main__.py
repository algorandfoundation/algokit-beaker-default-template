import logging
import sys
from pathlib import Path
from shutil import rmtree

from beaker import Application
from dotenv import load_dotenv
from smart_contracts.helloworld import app as helloworld_app
from smart_contracts.deployment import deploy

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)-10s: %(message)s")
logger = logging.getLogger(__name__)
logger.info("Loading .env")
load_dotenv()
root_path = Path(__file__).parent


def build(output_dir: Path, app: Application) -> Path:
    output_dir = output_dir.resolve()
    if output_dir.exists():
        rmtree(output_dir)
    output_dir.mkdir(exist_ok=False)
    logger.info(f"Exporting {app.name} to {output_dir}")
    specification = app.build()
    specification.export(output_dir)


def main(action: str) -> None:
    app_spec_path = root_path / "artifacts" / helloworld_app.name
    match action:
        case "build":
            logger.info(f"Building app {helloworld_app.name}")
            build(app_spec_path, helloworld_app)
        case "deploy":
            logger.info(f"Deploying {helloworld_app.name}")
            deploy(app_spec_path / "application.json")
        case "all":
            logger.info(f"Building app {helloworld_app.name}")
            build(app_spec_path, helloworld_app)
            logger.info(f"Deploying {helloworld_app.name}")
            deploy(app_spec_path / "application.json")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("all")
