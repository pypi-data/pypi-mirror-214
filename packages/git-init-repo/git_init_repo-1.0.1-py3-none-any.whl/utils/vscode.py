import json
import os

def vscode_tasks() -> None:
    """Writes the tasks.json file for vscode.
    """
    dict_tasks = {}
    
    dict_tasks['version'] = '2.0.0'
    dict_tasks['tasks'] = [{
            "command": "python -m venv .venv",
            "label": "Create virtual environment",
            "type": "shell",
            "problemMatcher": []
        },
        {
            "command": "python -m pip install --upgrade pip",
            "label": "Upgrade pip",
            "type": "shell",
            "problemMatcher": [],
            "dependsOn": [
                "Create virtual environment",
            ]
        },
        {
            "command": "pip install -r requirements.txt",
            "label": "Install dependencies",
            "type": "shell",
            "problemMatcher": [],
            "dependsOn": [
                "Upgrade pip"
            ]
        },
        {
            "command": "pip install -r requirements-dev.txt",
            "label": "Install dev dependencies",
            "type": "shell",
            "problemMatcher": [],
            "dependsOn": [
                "Install dependencies"
            ]
        },
        {
            "label": "Build environment",
            "dependsOn": [
                "Install dev dependencies"
            ]
        }]
    
    os.mkdir('.vscode')
    with open(r'.vscode/tasks.json', 'w') as f:
        json.dump(dict_tasks, f, indent=4)