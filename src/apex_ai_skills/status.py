"""Report installed vs remote Apex AI skills versions."""

from __future__ import annotations

import sys
from pathlib import Path

from apex_ai_skills.constants import SKILLS_SUBPATH
from apex_ai_skills.fetch import (
    SkillsFetchError,
    fetch_remote_manifest,
    parse_version,
    read_local_manifest,
)


def show_status(project_path: Path) -> None:
    destination = project_path / SKILLS_SUBPATH

    if not destination.exists():
        print(f"No Apex skills installed at {destination}.")
        print("Run `apex-skills install` to add them.")
        sys.exit(1)

    try:
        remote_manifest = fetch_remote_manifest()
        remote_version = parse_version(remote_manifest)
    except (SkillsFetchError, OSError) as exc:
        print(f"ERROR: Could not fetch remote manifest: {exc}")
        sys.exit(1)

    local_manifest = read_local_manifest(destination)
    if local_manifest is None:
        print(f"Apex skills installed at {destination}")
        print("Local version: unknown (manifest.json missing)")
        print(f"Remote version: {remote_version}")
        print("Run `apex-skills update` to sync.")
        return

    local_version = parse_version(local_manifest)
    print(f"Apex skills at {destination}")
    print(f"Local version:  {local_version}")
    print(f"Remote version: {remote_version}")

    if remote_version > local_version:
        print("Update available. Run `apex-skills update`.")
    else:
        print("Up to date.")
