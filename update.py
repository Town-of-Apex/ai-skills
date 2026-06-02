# update.py
# This script will update the skills in the .agents/skills/apex folder to the latest versions
# It will do this by cloning the skills repository and copying the latest skills to the .agents/skills/apex folder
# It will then remove the temporary skills repository

import os
import shutil
import json
import requests

TEMP_SKILLS_FOLDER = 'temp-skills'
GITHUB_REPO_URL = "https://github.com/Town-of-Apex/ai-skills"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Town-of-Apex/ai-skills/main"

# Get the latest info from the manifest.json file
def get_latest_skills_manifest():
    response = requests.get(f'{GITHUB_RAW_BASE}/manifest.json')
    response.raise_for_status()
    return response.json()

# Get the current info from the manifest.json file in the local skills folder
def get_current_skills_version():
    with open('manifest.json', 'r') as f:
        return json.load(f)['metadata']['version']

def update_skills():

    print('Getting latest skills manifest...')
    latest_version = get_latest_skills_manifest()['metadata']['version']
    current_version = get_current_skills_version()

    if latest_version > current_version:
        print(f'Updating skills from {current_version} to {latest_version}')
        print(f'Latest updated skills: {latest_skills_manifest["latest_updated_skills"]}')
        # clone the skills repository into a temporary folder
        os.system(f'git clone {GITHUB_REPO_URL} {TEMP_SKILLS_FOLDER}')
        # copy the skills from the temporary folder to the local skills folder
        shutil.copytree(f'{TEMP_SKILLS_FOLDER}/.agents/skills/apex', '.agents/skills/apex', dirs_exist_ok=True)
        # remove the temporary folder
        shutil.rmtree(TEMP_SKILLS_FOLDER, ignore_errors=True)
    else:
        print(f'Skills are up to date at {current_version}')
        return

if __name__ == '__main__':
    update_skills()