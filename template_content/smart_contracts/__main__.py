from pathlib import Path

from smart_contracts.lab import my_lab

my_lab.distill(
    output_dir=(Path(__file__).parent / "artifacts"),
)
