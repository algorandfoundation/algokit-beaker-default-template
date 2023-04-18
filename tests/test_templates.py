import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

commit_pattern = re.compile(r"_commit: .*")
src_path_pattern = re.compile(r"_src_path: .*")
tests_path = Path(__file__).parent
root = tests_path.parent
generated_folder = "tests_generated"
generated_root = root / generated_folder


@pytest.fixture(autouse=True, scope="module")
def working_dir() -> Iterator[Path]:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp:
        working_dir = Path(temp) / "template"
        working_generated_root = working_dir / generated_folder
        shutil.copytree(root, working_dir)
        subprocess.run(["git", "add", "-A"], cwd=working_dir)
        subprocess.run(
            ["git", "commit", "-m", "draft changes", "--no-verify"], cwd=working_dir
        )

        yield working_dir

        for dir_name in os.listdir(working_generated_root):
            src_dir = working_generated_root / dir_name
            dest_dir = generated_root / dir_name
            shutil.rmtree(dest_dir, ignore_errors=True)
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)


def run_init(
    working_dir: Path,
    test_name: str,
    *args: str,
    template_url: str | None = None,
    template_branch: str | None = None,
    answers: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    copy_to = working_dir / generated_folder / test_name
    shutil.rmtree(copy_to, ignore_errors=True)
    if template_url is None:
        template_url = str(working_dir)

        if template_branch is None:
            git_output = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=working_dir,
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
    answers = dict(answers or {})
    answers.setdefault("author_name", "None")
    answers.setdefault("author_email", "None")

    for question, answer in answers.items():
        init_args.extend(["-a", question, answer])
    if template_branch:
        init_args.extend(["--template-url-ref", template_branch])
    init_args.extend(args)

    result = subprocess.run(
        init_args,
        input="y",  # acknowledge that input is not a tty
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=copy_to.parent,
    )

    if (
        result.returncode == 0
    ):  # if successful, normalize .copier-answers.yml to make observing diffs easier
        copier_answers = Path(copy_to / ".copier-answers.yml")
        content = copier_answers.read_text("utf-8")
        content = commit_pattern.sub("_commit: <commit>", content)
        content = src_path_pattern.sub("_src_path: <src>", content)
        copier_answers.write_text(content, "utf-8")

    return result


def test_default_parameters(working_dir: Path) -> None:
    response = run_init(working_dir, "test_default_parameters")

    assert response.returncode == 0


def run_init_kwargs(working_dir: Path, **kwargs: str | bool) -> None:
    answers = {k: str(v) for k, v in kwargs.items()}
    name_suffix = "_".join(f"{k}-{v}" for k, v in answers.items())
    response = run_init(working_dir, f"test_{name_suffix}", answers=answers)

    assert response.returncode == 0


@pytest.mark.parametrize("ide_vscode", [True, False])
def test_ide_vscode(working_dir: Path, *, ide_vscode: bool) -> None:
    run_init_kwargs(working_dir, ide_vscode=ide_vscode)


@pytest.mark.parametrize("use_python_black", [True, False])
def test_use_python_black(working_dir: Path, *, use_python_black: bool) -> None:
    run_init_kwargs(working_dir, use_python_black=use_python_black)


@pytest.mark.parametrize("use_python_mypy", [True, False])
def test_use_python_mypy(working_dir: Path, *, use_python_mypy: bool) -> None:
    run_init_kwargs(working_dir, use_python_mypy=use_python_mypy)


@pytest.mark.parametrize("use_python_pytest", [True, False])
def test_use_python_pytest(working_dir: Path, *, use_python_pytest: bool) -> None:
    run_init_kwargs(working_dir, use_python_pytest=use_python_pytest)


@pytest.mark.parametrize("use_python_pip_audit", [True, False])
def test_use_python_pip_audit(working_dir: Path, *, use_python_pip_audit: bool) -> None:
    run_init_kwargs(working_dir, use_python_pip_audit=use_python_pip_audit)


@pytest.mark.parametrize("deployment_language", ["python", "typescript"])
def test_deployment_language(working_dir: Path, *, deployment_language: str) -> None:
    run_init_kwargs(working_dir, deployment_language=deployment_language)


@pytest.mark.parametrize("python_linter", ["ruff", "flake8", "none"])
def test_python_linter(working_dir: Path, *, python_linter: str) -> None:
    run_init_kwargs(working_dir, python_linter=python_linter)
