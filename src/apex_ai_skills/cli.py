"""Command-line interface for apex-skills."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from apex_ai_skills import __version__
from apex_ai_skills.install import install_skills
from apex_ai_skills.status import show_status
from apex_ai_skills.update import update_skills


def _resolve_project_path(raw: str | None) -> Path:
    project_path = Path(raw or ".").resolve()
    if not project_path.exists():
        print(f"ERROR: Project path does not exist: {project_path}")
        sys.exit(1)
    return project_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apex-skills",
        description="Install and update Town of Apex AI agent skills for Cursor projects.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser(
        "install",
        help="Install Apex skills into a project (default: current directory)",
    )
    install_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to the target project root (default: current directory)",
    )
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing .agents/skills/apex installation",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Update Apex skills from GitHub (default: current directory)",
    )
    update_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to the target project root (default: current directory)",
    )
    update_parser.add_argument(
        "--force",
        action="store_true",
        help="Reinstall skills even if the local version is current",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Show installed vs remote skill versions",
    )
    status_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to the target project root (default: current directory)",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    project_path = _resolve_project_path(args.project_path)

    if args.command == "install":
        install_skills(project_path, force=args.force)
    elif args.command == "update":
        update_skills(project_path, force=args.force)
    elif args.command == "status":
        show_status(project_path)
