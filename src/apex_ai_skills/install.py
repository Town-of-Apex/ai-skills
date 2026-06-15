"""Install Apex AI skills into a project."""

from __future__ import annotations

import sys
from pathlib import Path

from apex_ai_skills.constants import SKILLS_SUBPATH
from apex_ai_skills.fetch import SkillsFetchError, copy_skills_to_project, fetch_skills_source


def install_skills(project_path: Path, *, force: bool = False) -> None:
    destination = project_path / SKILLS_SUBPATH

    if destination.exists() and not force:
        print(
            f"ERROR: {destination} already exists.\n"
            "Run `apex-skills install --force` to replace it, "
            "or `apex-skills update` if you want the latest version."
        )
        sys.exit(1)

    print("Fetching latest Apex AI skills from GitHub...")
    try:
        with fetch_skills_source() as source:
            copy_skills_to_project(source, destination)
    except SkillsFetchError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    except OSError as exc:
        print(f"ERROR: Failed to install skills: {exc}")
        sys.exit(1)

    print("Installation complete.")
    print(f"Installed to: {destination}")
