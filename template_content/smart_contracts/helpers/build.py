import logging
from pathlib import Path
from shutil import rmtree

from beaker import Application

logger = logging.getLogger(__name__)


def build(output_dir: Path, app: Application) -> Path:
    output_dir = output_dir.resolve()
    if output_dir.exists():
        rmtree(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    logger.info(f"Exporting {app.name} to {output_dir}")
    specification = app.build()
    specification.export(output_dir)
    return output_dir / "application.json"
