"""
Main Application Entry Point.

Hospital Bed Allocation & Patient Record System
Run with:
    python main.py
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.services.hospital_system import HospitalBedAllocationSystem
from src.cli.menu import HospitalCLI


def main() -> None:
    db_file = BASE_DIR / "hospital.db"
    print(f"Initializing Hospital Database at: {db_file}")
    system = HospitalBedAllocationSystem(db_path=db_file)
    cli = HospitalCLI(system)
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user. Safely shutting down...")
        system.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
