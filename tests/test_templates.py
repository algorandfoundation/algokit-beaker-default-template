import shutil
import subprocess
from pathlib import Path


def run_init(
    test_name: str,
    *args: str,
    template_url: str | None = None,
    template_branch: str | None = None,
) -> subprocess.CompletedProcess:
    tests_path = Path(__file__).parent
    root = tests_path.parent
    copy_to = tests_path / test_name
    shutil.rmtree(copy_to, ignore_errors=True)
    if template_url is None:
        template_url = str(root)

        if template_branch is None:
            git_output = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=root,
                stdout=subprocess.PIPE,
            )
            template_branch = git_output.stdout.decode("utf-8").strip()

    init_args = [
        "algokit",
        "init",
        "--name",
        str(copy_to.stem),
        "--template-url",
        template_url,
        "--UNSAFE-SECURITY-accept-template-url",
        "--defaults",
        "--no-ide",
        "--no-git",
        "--no-bootstrap",
    ]
    if template_branch:
        init_args.extend(["--template-url-ref", template_branch])
    init_args.extend(args)

    return subprocess.run(
        init_args,
        input="y",  # acknowledge that input is not a tty
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=copy_to.parent,
    )


def test_default_parameters() -> None:
    response = run_init("test_default_parameters")

    assert response.returncode == 0
