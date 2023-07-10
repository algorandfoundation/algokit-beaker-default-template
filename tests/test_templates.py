import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest
import yaml

commit_pattern = re.compile(r"^_commit: .*", flags=re.MULTILINE)
src_path_pattern = re.compile(r"_src_path: .*")
tests_path = Path(__file__).parent
root = tests_path.parent
generated_folder = "tests_generated"
generated_root = root / generated_folder
DEFAULT_PARAMETERS = {
    "author_name": "None",
    "author_email": "None",
}
config_path = Path(__file__).parent.parent / "pyproject.toml"
BLACK_ARGS = ["black", "--check", "--diff", "--config", str(config_path), "."]
RUFF_ARGS = ["ruff", "--diff", "--config", str(config_path), "."]
MYPY_ARGS = [
    "mypy",
    "--ignore-missing-imports",  # TODO: only ignore missing typed clients in config.py
    ".",
]


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

        for src_dir in working_generated_root.iterdir():
            if not src_dir.is_dir():
                continue

            dest_dir = generated_root / src_dir.stem
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
        "--verbose",
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
    answers = {**DEFAULT_PARAMETERS, **(answers or {})}

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

    if result.returncode:
        return result
    # if successful, normalize .copier-answers.yml to make observing diffs easier
    copier_answers = Path(copy_to / ".copier-answers.yml")
    content = copier_answers.read_text("utf-8")
    content = commit_pattern.sub("_commit: <commit>", content)
    content = src_path_pattern.sub("_src_path: <src>", content)
    copier_answers.write_text(content, "utf-8")

    for check_args in [BLACK_ARGS, RUFF_ARGS, MYPY_ARGS]:
        result = subprocess.run(
            check_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=copy_to,
        )
        if result.returncode:
            break

    return result


def run_init_kwargs(
    working_dir: Path, **kwargs: str | bool
) -> subprocess.CompletedProcess:
    answers = {k: str(v) for k, v in kwargs.items()}
    name_suffix = "_".join(f"{k}-{v}" for k, v in answers.items())
    return run_init(working_dir, f"test_{name_suffix}", answers=answers)


def get_questions_from_copier_yaml(
    allowed_questions: list[str] | None = None,
) -> Iterator[tuple[str, str | bool]]:
    copier_yaml = root / "copier.yaml"
    ignored_keys = {
        "_subdirectory",  # copier setting
        # the following are ignored as they are passed automatically by algokit
        "project_name",
        "algod_token",
        "algod_server",
        "algod_port",
        "indexer_token",
        "indexer_server",
        "indexer_port",
    }
    ignored_keys.update(DEFAULT_PARAMETERS)

    with copier_yaml.open("r", encoding="utf-8") as stream:
        questions = yaml.safe_load(stream)
        for question_name, details in questions.items():
            if question_name in ignored_keys:
                continue
            if allowed_questions and question_name not in allowed_questions:
                continue
            match details["type"]:
                case "str":
                    if "choices" not in details:
                        continue

                    for choice in details["choices"].values():
                        yield question_name, choice
                case "bool":
                    yield question_name, False
                    yield question_name, True


@pytest.mark.parametrize(("question_name", "answer"), get_questions_from_copier_yaml())
def test_parameters(working_dir: Path, question_name: str, answer: str | bool) -> None:
    response = run_init_kwargs(working_dir, **{question_name: answer})

    assert response.returncode == 0, response.stdout


def test_default_parameters(working_dir: Path) -> None:
    response = run_init(working_dir, "test_default_parameters")

    assert response.returncode == 0, response.stdout


@pytest.mark.parametrize(
    ("question_name", "answer"),
    get_questions_from_copier_yaml(
        [
            "deployment_language",
            "python_linter",
            "use_python_black",
            "use_python_mypy",
            "use_python_pytest",
            "use_python_pip_audit",
        ]
    ),
)
def test_parameters_with_github(
    working_dir: Path, question_name: str, answer: str | bool
) -> None:
    response = run_init_kwargs(
        working_dir, **{"use_github_actions": True, question_name: answer}
    )

    assert response.returncode == 0, response.stdout


def test_typescript_deploy_without_github(working_dir: Path) -> None:
    response = run_init_kwargs(
        working_dir, use_github_actions=False, deployment_language="typescript"
    )

    assert response.returncode == 0, response.stdout
