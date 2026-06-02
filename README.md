# ai-skills
Repository of Apex Innovations-specific AI agent skills for using across the organization



## How to Use
We recommend installing skills at the *project* level for the time being, as each developer may be working on projects for themselves, the Town, and other organizations, and we cannot guarantee that our (Apex's) development standards or AI skills will be compatible or aligned with best practices or expectations from other organizations or personal preference. 

For each Town project, we recommend installing these skills to the project directory on your machine and regularly checking the repository for updates (updating will be a CLI-enabled feature eventually). 

### Install Town Skills
To install the latest Apex Town skills into your project, run the following commands from your project root:

```bash
git clone https://github.com/Town-of-Apex/ai-skills temp-skills
uv run temp_skills/install.py . --force
# or if not using uv
python temp_skills/install.py . --force
# on Unix/MacOS systems
rm -rf temp-skills
# on Windows/Powershell systems
rm -r -fo temp-skills
```
This will copy the most recent skill files into your project's `.agents/skills/apex` folder.

> NOTE: You may need to add the requests package to your project venv. Using uv is the fastest and simplest method, allowing `uv add requests` to handle venv and dependency management tasks near-instantly. 


### Update Your Copy of Town Skills
This repo will be updated on a batch basis, meaning that changing a single skill document will result in the entire repository being marked with an new version number. This means that when you update your skills, many documents may not look like they have changed at all. 

To update your local skills, you can reinstall the skills manually or use the included `.agents/skills/apex/update.py` script. This script requires Python 3.11+ and should run inside your project's virtual environment (managed by [uv](https://github.com/astral-sh/uv) or `venv`).

From your project root, run:

```bash
# If you use uv (recommended and much faster):
uv run python .agents/skills/apex/update.py

# If you do not use uv, you can run it with simple python:
python .agents/skills/apex/update.py
```

> Make sure you always activate your virtual environment before running or updating skills.

> Note that you must update your skills for `each` project on your machine.


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
1. In the root of your project directory, find or create a .agents/ folder
2. In the /.agents folder, create a /skills subfolder
3. Each skill file (and other files to reference or provide as examples) should belong to its own folder, either directly or indirectly within the skills/ subfolder. Folders in /skills can be created to group skills by category or style; Cursor will recursively hunt for 'SKILL.md' files in all folders within /skills. NOTE: Any skills in the /apex folder will be REPLACED by the contents of the latest version of this repository upun running .agents/skills/apex/update.py. Therefore, use the /.agents/skills/custom folder for any skills you wish to add, modify, and persist while updating official Town of Apex-maintained skills. 
4. An individual skill should look like this, with only a SKILL.md file being required: 
```
skills/ 
    skill-name/
        SKILL.md
        script-to-reference.py
        template-thing.json
```


Example Directory (including subject-level groupings): 
```
.cursor/
└── skills/
    ├── shipping/
    │   ├── land-it/
    │   │   └── SKILL.md
    │   └── careful-merge-conflicts/
    │       └── SKILL.md
    ├── debugging/
    │   └── using-datadog-mcp/
    │       └── SKILL.md
    └── workflow/
        └── tdd/
            └── SKILL.md
```


## Updating Town Skills
When upcating the skills in this repository, a few steps must be taken to maintain the functionality of this system and ensure that update and maintenance scripts continue to function as intended. 
1. Update the skills themselves: create, edit, and modify skills in their correct folders. ALWAYS use the /apex folder, do not add any skills to the /custom folder for any reason. 
2. Update the manifest.json file: 
- Major modifications (creating >1 new skill) warrants a whole-number update (X.0.0)
Substantial modifications or single-skill additions warrant decimal-updates (1.X.0)
- Spelling, grammar, or readability error-correction warrants tertiary decimal updates (1.0.X)
- Replace the latest_updated_skills field with a list of the names of the skills you have modified or added. 
