"""Download skills and version metadata from the ai-skills GitHub repository."""

from __future__ import annotations

import json
import shutil
import tarfile
import tempfile
import tomllib
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import requests
from packaging.version import InvalidVersion, Version

from apex_ai_skills.constants import (
    MANIFEST_FILENAME,
    PYPROJECT_FILENAME,
    RAW_MANIFEST_URL,
    RAW_PYPROJECT_URL,
    SKILLS_SUBPATH,
    TARBALL_URL,
)


class SkillsFetchError(RuntimeError):
    """Raised when skills cannot be fetched from GitHub."""


def fetch_remote_manifest() -> dict:
    response = requests.get(RAW_MANIFEST_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_remote_version() -> Version:
    response = requests.get(RAW_PYPROJECT_URL, timeout=30)
    response.raise_for_status()
    return parse_pyproject_version(response.text)


def parse_pyproject_version(pyproject_text: str) -> Version:
    data = tomllib.loads(pyproject_text)
    raw = data.get("project", {}).get("version")
    if not raw:
        raise SkillsFetchError("pyproject.toml is missing project.version")
    try:
        return Version(str(raw))
    except InvalidVersion as exc:
        raise SkillsFetchError(f"Invalid pyproject.toml version: {raw!r}") from exc


def read_repo_version(repo_root: Path) -> Version:
    pyproject_path = repo_root / PYPROJECT_FILENAME
    if not pyproject_path.exists():
        raise SkillsFetchError(f"pyproject.toml not found at {pyproject_path}")
    return parse_pyproject_version(pyproject_path.read_text(encoding="utf-8"))


def read_repo_manifest(repo_root: Path) -> dict:
    manifest_path = repo_root / MANIFEST_FILENAME
    if not manifest_path.exists():
        return {"latest_updated_skills": []}
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def read_local_manifest(skills_dir: Path) -> dict | None:
    manifest_path = skills_dir / MANIFEST_FILENAME
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def parse_installed_version(manifest: dict) -> Version:
    raw = manifest.get("version")
    if not raw:
        raise SkillsFetchError("Installed manifest.json is missing version")
    try:
        return Version(str(raw))
    except InvalidVersion as exc:
        raise SkillsFetchError(f"Invalid installed version: {raw!r}") from exc


@contextmanager
def fetch_skills_source() -> Iterator[tuple[Path, Path]]:
    """Yield (skills_dir, repo_root) from GitHub or a local development checkout."""
    local_repo_root = _find_local_repo_root()
    if local_repo_root is not None:
        yield local_repo_root / SKILLS_SUBPATH, local_repo_root
        return

    with tempfile.TemporaryDirectory(prefix="apex-skills-") as temp_dir:
        archive_path = Path(temp_dir) / "ai-skills.tar.gz"
        extract_dir = Path(temp_dir) / "extract"

        _download_tarball(archive_path)
        extract_dir.mkdir()
        _extract_tarball(archive_path, extract_dir)

        repo_root = _find_repo_root_in_extract(extract_dir)
        if repo_root is None:
            raise SkillsFetchError("Downloaded archive is missing .agents/skills/apex")

        yield repo_root / SKILLS_SUBPATH, repo_root


def _find_local_repo_root() -> Path | None:
    """Use the local repo when running from a development checkout."""
    repo_root = Path(__file__).resolve().parents[2]
    skills_dir = repo_root / SKILLS_SUBPATH
    if skills_dir.is_dir() and any(skills_dir.iterdir()):
        return repo_root
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


def _find_repo_root_in_extract(extract_dir: Path) -> Path | None:
    for root in extract_dir.iterdir():
        if not root.is_dir():
            continue
        if (root / SKILLS_SUBPATH).is_dir():
            return root
    return None


def copy_skills_to_project(source: Path, repo_root: Path, destination: Path) -> None:
    """Copy apex skills into a project and write an installed manifest."""
    if destination.exists():
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    _write_installed_manifest(destination, repo_root)


def _write_installed_manifest(destination: Path, repo_root: Path) -> None:
    repo_manifest = read_repo_manifest(repo_root)
    installed_manifest = {
        "version": str(read_repo_version(repo_root)),
        "latest_updated_skills": repo_manifest.get("latest_updated_skills", []),
    }
    manifest_path = destination / MANIFEST_FILENAME
    manifest_path.write_text(
        json.dumps(installed_manifest, indent=4) + "\n",
        encoding="utf-8",
    )
