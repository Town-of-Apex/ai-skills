#!/usr/bin/env python3
"""
Install Apex AI Skills into an existing project.

Usage:
    python install.py <project_path>
    python install.py <project_path> --force
"""

import argparse
import shutil
import sys
from pathlib import Path


def install_skills(project_path: Path, force: bool = False) -> None:
    repo_root = Path(__file__).resolve().parent

    source_skills = repo_root / ".agents" / "skills" / "apex"
    destination_skills = project_path / ".agents" / "skills" / "apex"

    if not source_skills.exists():
        print(f"ERROR: Source skills folder not found: {source_skills}")
        sys.exit(1)

    destination_skills.parent.mkdir(parents=True, exist_ok=True)

    if destination_skills.exists():
        if not force:
            print(
                f"ERROR: {destination_skills} already exists.\n"
                f"Use --force to replace it."
            )
            sys.exit(1)

        print(f"Removing existing installation: {destination_skills}")
        shutil.rmtree(destination_skills)

    print(f"Installing Apex AI Skills...")
    shutil.copytree(source_skills, destination_skills)

    print("Installation complete.")
    print(f"Installed to: {destination_skills}")


def main():
    parser = argparse.ArgumentParser(
        description="Install Apex AI Skills into a project."
    )

    parser.add_argument(
        "project_path",
        help="Path to the target project root"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing Apex skills installation"
    )

    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"ERROR: Project path does not exist: {project_path}")
        sys.exit(1)

    install_skills(project_path, args.force)


if __name__ == "__main__":
    main()