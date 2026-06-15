#!/usr/bin/env python3
"""Legacy entry point. Prefer the apex-skills CLI: `apex-skills update`."""

from apex_ai_skills.cli import main

if __name__ == "__main__":
    main(["update", *__import__("sys").argv[1:]])
