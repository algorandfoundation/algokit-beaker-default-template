import shutil
import sys
from pathlib import Path
import os


def main():
    # Get the use_deprecated_template argument
    use_deprecated_template = sys.argv[1].lower() in ("true", "yes", "1", "t", "y")
    use_workspace = sys.argv[2].lower() in ("true", "yes", "1", "t", "y")

    if not use_deprecated_template:
        # Get the parent directory of this script which should be the generated project root
        project_dir = Path(__file__).parent
        project_dir = project_dir.parent.parent if use_workspace else project_dir

        # Print warning
        print("WARNING: Template generation cancelled!\n")
        print(
            "This template is deprecated. Use Algorand Python instead: https://github.com/algorandfoundation/algokit-python-template\n"
        )

        if project_dir.exists():
            try:
                os.chdir(project_dir.parent)
                shutil.rmtree(project_dir)
            except Exception as e:
                print(
                    f"Failed to clean up {project_dir}. You will have to manually delete the project folder. Error: {str(e)}",
                    file=sys.stderr,
                )

        sys.exit(1)

    # If we get here, template was approved to be used
    print("Proceeding with deprecated template generation...")


if __name__ == "__main__":
    main()
