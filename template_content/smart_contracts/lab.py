from pathlib import Path
from shutil import rmtree
from typing import Sequence

from beaker.application import Application

from smart_contracts.helloworld import HelloWorld


class Lab:
    def __init__(self, apps: Sequence[Application]) -> None:
        self.apps = apps

    def distill(self, output_dir: Path) -> None:
        output_dir = output_dir.resolve()
        if output_dir.exists():
            rmtree(output_dir)
        output_dir.mkdir(exist_ok=False)
        for app in self.apps:
            cls = app.__class__
            module_name = cls.__module__.removeprefix("smart_contracts.")
            qualified_app_name = f"{module_name}.{cls.__qualname__}"
            app_output_dir = output_dir / qualified_app_name
            print(f"Compiling {qualified_app_name} to {app_output_dir}")
            app.dump(str(app_output_dir))


my_lab = Lab(
    apps=[HelloWorld()],
)
