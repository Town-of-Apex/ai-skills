"""Update Apex AI skills in a project from GitHub."""

from __future__ import annotations

import sys
from pathlib import Path

from apex_ai_skills.constants import SKILLS_SUBPATH
from apex_ai_skills.fetch import (
    SkillsFetchError,
    copy_skills_to_project,
    fetch_remote_manifest,
    fetch_remote_version,
    fetch_skills_source,
    parse_installed_version,
    read_local_manifest,
)


def update_skills(project_path: Path, *, force: bool = False) -> None:
    destination = project_path / SKILLS_SUBPATH

    if not destination.exists():
        print(
            f"ERROR: No Apex skills found at {destination}.\n"
            "Run `apex-skills install` first."
        )
        sys.exit(1)

    print("Checking for Apex AI skills updates...")
    try:
        remote_version = fetch_remote_version()
        remote_manifest = fetch_remote_manifest()
    except (SkillsFetchError, OSError) as exc:
        print(f"ERROR: Could not fetch remote version: {exc}")
        sys.exit(1)

    local_manifest = read_local_manifest(destination)
    if local_manifest is None:
        print("No local manifest found; installing latest skills...")
        _replace_skills(destination)
        _print_update_complete(destination, remote_version, remote_manifest)
        return

    local_version = parse_installed_version(local_manifest)

    if not force and remote_version <= local_version:
        print(f"Skills are up to date at {local_version}.")
        return

    if force and remote_version <= local_version:
        print(f"Reinstalling skills (--force) at version {remote_version}...")
    else:
        print(f"Updating skills from {local_version} to {remote_version}...")

    _replace_skills(destination)
    _print_update_complete(destination, remote_version, remote_manifest)


def _replace_skills(destination: Path) -> None:
    try:
        with fetch_skills_source() as (source, repo_root):
            copy_skills_to_project(source, repo_root, destination)
    except SkillsFetchError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    except OSError as exc:
        print(f"ERROR: Failed to update skills: {exc}")
        sys.exit(1)


def _print_update_complete(
    destination: Path, remote_version, remote_manifest: dict
) -> None:
    updated = remote_manifest.get("latest_updated_skills", [])
    if updated:
        print(f"Updated skills: {', '.join(updated)}")
    print(f"Skills updated to version {remote_version}.")
    print(f"Installed to: {destination}")
