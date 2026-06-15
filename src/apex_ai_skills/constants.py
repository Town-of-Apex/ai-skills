from pathlib import Path

GITHUB_REPO = "Town-of-Apex/ai-skills"
DEFAULT_BRANCH = "main"

MANIFEST_FILENAME = "manifest.json"
SKILLS_SUBPATH = Path(".agents") / "skills" / "apex"

RAW_MANIFEST_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_REPO}/{DEFAULT_BRANCH}/manifest.json"
)
TARBALL_URL = (
    f"https://github.com/{GITHUB_REPO}/archive/refs/heads/{DEFAULT_BRANCH}.tar.gz"
)
