from pathlib import Path

from smart_contracts.lab import my_lab

print("Compiling Beaker smart contracts...")
my_lab.distill(
    output_dir=(Path(__file__).parent / "artifacts"),
)
