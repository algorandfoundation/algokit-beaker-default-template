import logging
import subprocess
from pathlib import Path
from shutil import rmtree

import beaker

logger = logging.getLogger(__name__)
deployment_extension = "ts"


def build(output_dir: Path, app: beaker.Application) -> Path:
    output_dir = output_dir.resolve()
    if output_dir.exists():
        rmtree(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    logger.info(f"Exporting {app.name} to {output_dir}")
    specification = app.build()
    specification.export(output_dir)

    try:
        subprocess.run(
            [
                "algokit",
                "generate",
                "client",
                output_dir / "application.json",
                "--output",
                output_dir / f"client.{deployment_extension}",
            ]
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Build process failed with error code {e.returncode}")
        raise e

    return output_dir / "application.json"
