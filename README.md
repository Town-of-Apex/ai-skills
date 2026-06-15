# ai-skills
Repository of Apex Innovations-specific AI agent skills for using across the organization

## How to Use

We recommend installing skills at the *project* level, as each developer may be working on projects for themselves, the Town, and other organizations. Town-maintained skills live in `.agents/skills/apex/`. Put your own custom skills in any other folder under `.agents/skills/` (for example `.agents/skills/custom/`). The `apex-skills` tool only ever touches the `apex/` folder.

### One-time setup (each developer)

Install [uv](https://docs.astral.sh/uv/), then install the CLI tool:

```bash
uv tool install 'apex-ai-skills @ git+https://github.com/Town-of-Apex/ai-skills.git'
uv tool update-shell   # if `apex-skills` is not found on your PATH
```

To upgrade the CLI itself after tool changes:

```bash
uv tool upgrade apex-ai-skills
```

### Install skills in a project

From your project root:

```bash
apex-skills install
```

This fetches the latest skills from GitHub and copies them to `.agents/skills/apex/`, including a `manifest.json` for version tracking.

To replace an existing installation:

```bash
apex-skills install --force
```

### Update skills in a project

When this repository releases a new skills version (see `manifest.json`), update each Town project from its root:

```bash
apex-skills update
```

Check whether an update is available:

```bash
apex-skills status
```

Commit the updated `.agents/skills/apex/` folder so the rest of your team stays in sync.

## Skill Files

Skill files should be simple, concise, text-based instructions or explanations about a specific aspect of the task or process that it will be invoked for. It is recommended not to exceed two pages' worth of text.
Follow this format for the contents of a SKILL.md file:

---
name: my-skill
description: Short description of what this skill does and when to use it.
---
# My Skill
Detailed instructions for the agent.
## When to Use
- Use this skill when...
- This skill is helpful for...
## Instructions
- Step-by-step guidance for the agent
- Domain-specific conventions
- Best practices and patterns
- Use the ask questions tool if you need to clarify requirements with the user

## How to Deploy Skills

### Cursor
1. In the root of your project directory, find or create a `.agents/` folder
2. In the `.agents/` folder, create a `skills/` subfolder
3. Each skill file (and other files to reference or provide as examples) should belong to its own folder, either directly or indirectly within the `skills/` subfolder. Folders in `skills/` can be created to group skills by category or style; Cursor will recursively hunt for `SKILL.md` files in all folders within `skills/`. Any skills in the `apex/` folder will be replaced when you run `apex-skills update`. Use `.agents/skills/custom/` (or any other non-`apex/` folder) for skills you want to keep while updating official Town of Apex-maintained skills.
4. An individual skill should look like this, with only a `SKILL.md` file being required:
```
skills/
    skill-name/
        SKILL.md
        script-to-reference.py
        template-thing.json
```

Example Directory (including subject-level groupings):
```
.agents/
└── skills/
    ├── apex/
    │   └── App-Architecture/
    │       └── SKILL.md
    └── custom/
        └── my-team-skill/
            └── SKILL.md
```

## Updating Town Skills (maintainers)

When updating the skills in this repository:

1. Update the skills themselves: create, edit, and modify skills in `.agents/skills/apex/`. Do not add official skills to the `custom/` folder.
2. Update `manifest.json`:
   - Major modifications (creating >1 new skill) warrants a whole-number update (X.0.0)
   - Substantial modifications or single-skill additions warrant decimal updates (1.X.0)
   - Spelling, grammar, or readability corrections warrant tertiary decimal updates (1.0.X)
   - Replace the `latest_updated_skills` field with a list of the names of the skills you have modified or added
3. Bump the version in `pyproject.toml` when the CLI package changes

## Development

From a checkout of this repository:

```bash
uv sync
uv run apex-skills install /path/to/test-project
uv run apex-skills update /path/to/test-project
uv run apex-skills status /path/to/test-project
```

Install locally as a tool while developing:

```bash
uv tool install . --force
```
