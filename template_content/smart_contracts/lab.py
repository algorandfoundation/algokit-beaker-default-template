from pathlib import Path
from shutil import rmtree
from typing import Sequence

from beaker import Application
from smart_contracts.helloworld import HelloWorld


class Lab:
    def __init__(self, apps: Sequence[Application]) -> None:
        self.apps = apps

    def distill(self) -> None:
        this_dir = Path(__file__).parent
        output_dir = (this_dir / "artifacts").resolve()
        if output_dir.exists():
            rmtree(output_dir)
        output_dir.mkdir(exist_ok=False)
        for app in self.apps:
            cls = app.__class__
            module_name = cls.__module__.removeprefix("smart_contracts.")
            qualified_app_name = f"{module_name}.{cls.__name__}"
            app_output_dir = output_dir / qualified_app_name
            app.dump(str(app_output_dir))


my_lab = Lab(
    apps=[HelloWorld()],
)
