import os
import shutil
import sys
from pathlib import Path
from tkinter import E


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

        os.chdir(project_dir.parent)
        if project_dir.exists():
            try:
                shutil.rmtree(project_dir)
            except Exception as e:
                print(f"Error deleting project directory: {e}")
                pass

        sys.exit(1)

    # If we get here, template was approved to be used
    print("Proceeding with deprecated template generation...")


if __name__ == "__main__":
    main()
