# TTRPG Campaign Manager

A simple Python project for learning Git and GitHub through a small tabletop role-playing game campaign manager.

The application now includes a basic Tkinter GUI. It stores campaign data in JSON files so students can see how code and data change over time in Git.

## Features

* Switch between campaigns
* Manage characters, locations, monsters, rules and adventures
* Add entries
* Edit entries
* Delete entries
* View selected entry details
* Store each campaign in its own folder
* Keep campaign data in JSON files

## How to Run

From the project root:

```bash
python -m src.main
```

This launches the GUI.

## Optional CLI Version

The original command-line version is still available:

```bash
python -m src.main_cli
```

## VS Code Debugging

This project includes `.vscode/launch.json` with two configurations:

* `Run TTRPG Campaign Manager GUI`
* `Run TTRPG Campaign Manager CLI`

Open the Run and Debug panel in VS Code and choose the configuration you want.

## Project Structure

```text
ttrpg-campaign-manager/
├── src/
│   ├── main.py
│   ├── main_cli.py
│   ├── app.py
│   ├── cli_app.py
│   ├── data/
│   ├── gui/
│   ├── menus/
│   ├── models/
│   └── utils/
├── campaigns/
│   ├── starter_campaign/
│   └── haunted_valley/
├── tests/
├── .vscode/
├── .gitignore
├── requirements.txt
└── README.md
```

## Why This Is Useful for GitHub Learning

Students can create branches for features such as:

* `feature/gui-search`
* `feature/add-items`
* `feature/session-notes`
* `feature/new-campaign-button`
* `feature-export-markdown`

The campaign JSON files are useful for demonstrating commits, diffs, merge conflicts and pull requests.

## Running the GUI on Windows

From the project root, run:

```bash
python -m src.main
```

You can also double-click:

```text
run_gui.bat
```

If the app cannot start, the terminal will now stay open and show the error.
