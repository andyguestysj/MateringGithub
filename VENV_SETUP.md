# Python Virtual Environment (venv) Setup Guide

This project uses a Python virtual environment to manage dependencies.

---

## What is a Virtual Environment?

A virtual environment (venv) is an isolated Python environment for a project.

It allows you to:
* install packages without affecting other projects
* keep dependencies organised
* avoid version conflicts

---

## 1. Create the Virtual Environment

Open a terminal in the project root folder and run:

### Windows
```bash
python -m venv .venv
```

### macOS / Linux
```bash
python3 -m venv .venv
```

---

## 2. Activate the Virtual Environment

### Windows (PowerShell)
```bash
.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)
```bash
.venv\Scripts\activate.bat
```

### macOS / Linux
```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

If a `requirements.txt` file exists, run:

```bash
pip install -r requirements.txt
```

---

## 4. Verify It’s Working

You should see `(.venv)` at the start of your terminal prompt.

Check Python path:

```bash
where python     # Windows
which python     # macOS/Linux
```

It should point to `.venv`.

---

## 5. Running the Project

Run the project using module mode:

```bash
python -m src.main
```

---

## 6. Deactivate the Environment

When finished:

```bash
deactivate
```

---

## 7. Important Notes

* Do NOT commit `.venv/` to Git
* It should already be in `.gitignore`
* Each student should create their own venv locally

---

## 8. Troubleshooting

### Execution policy error (Windows PowerShell)

If activation fails, run:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then try activating again.

---

### Wrong Python version

Check your Python version:

```bash
python --version
```

If needed, install a newer version and recreate the venv.

---

## 9. Recommended VS Code Setup

Make sure VS Code is using the venv interpreter:

* Press `Ctrl + Shift + P`
* Select: `Python: Select Interpreter`
* Choose `.venv`

---

## Summary

```bash
python -m venv .venv
# activate it
pip install -r requirements.txt
python -m src.main
```
