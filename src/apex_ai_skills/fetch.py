"""Download skills and manifest from the ai-skills GitHub repository."""

from __future__ import annotations

import json
import shutil
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import requests
from packaging.version import InvalidVersion, Version

from apex_ai_skills.constants import (
    MANIFEST_FILENAME,
    RAW_MANIFEST_URL,
    SKILLS_SUBPATH,
    TARBALL_URL,
)


class SkillsFetchError(RuntimeError):
    """Raised when skills cannot be fetched from GitHub."""


def fetch_remote_manifest() -> dict:
    response = requests.get(RAW_MANIFEST_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_version(manifest: dict) -> Version:
    raw = manifest.get("metadata", {}).get("version")
    if not raw:
        raise SkillsFetchError("Manifest is missing metadata.version")
    try:
        return Version(str(raw))
    except InvalidVersion as exc:
        raise SkillsFetchError(f"Invalid manifest version: {raw!r}") from exc


def read_local_manifest(skills_dir: Path) -> dict | None:
    manifest_path = skills_dir / MANIFEST_FILENAME
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


@contextmanager
def fetch_skills_source() -> Iterator[Path]:
    """Yield a path to the apex skills directory fetched from GitHub."""
    local_source = _find_local_repo_skills()
    if local_source is not None:
        yield local_source
        return

    with tempfile.TemporaryDirectory(prefix="apex-skills-") as temp_dir:
        archive_path = Path(temp_dir) / "ai-skills.tar.gz"
        extract_dir = Path(temp_dir) / "extract"

        _download_tarball(archive_path)
        extract_dir.mkdir()
        _extract_tarball(archive_path, extract_dir)

        source = _find_skills_in_extract(extract_dir)
        if source is None:
            raise SkillsFetchError(
                "Downloaded archive does not contain .agents/skills/apex"
            )

        yield source


def _find_local_repo_skills() -> Path | None:
    """Use the local repo when running from a development checkout."""
    candidate = Path(__file__).resolve().parents[2] / SKILLS_SUBPATH
    if candidate.is_dir() and any(candidate.iterdir()):
        return candidate
    return None


def _download_tarball(destination: Path) -> None:
    response = requests.get(TARBALL_URL, timeout=60, stream=True)
    response.raise_for_status()
    with destination.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            if chunk:
                handle.write(chunk)


def _extract_tarball(archive_path: Path, extract_dir: Path) -> None:
    with tarfile.open(archive_path, "r:gz") as archive:
        archive.extractall(extract_dir, filter="data")


def _find_skills_in_extract(extract_dir: Path) -> Path | None:
    for root in extract_dir.iterdir():
        if not root.is_dir():
            continue
        candidate = root / SKILLS_SUBPATH
        if candidate.is_dir():
            return candidate
    return None


def copy_skills_to_project(source: Path, destination: Path) -> None:
    """Copy apex skills into a project, including manifest.json."""
    if destination.exists():
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)

    manifest_source = _find_manifest_source(source)
    if manifest_source is not None:
        shutil.copy2(manifest_source, destination / MANIFEST_FILENAME)


def _find_manifest_source(skills_source: Path) -> Path | None:
    local_manifest = skills_source / MANIFEST_FILENAME
    if local_manifest.exists():
        return local_manifest

    repo_root = skills_source.parents[2]
    root_manifest = repo_root / MANIFEST_FILENAME
    if root_manifest.exists():
        return root_manifest

    return None
