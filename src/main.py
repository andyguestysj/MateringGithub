"""Entry point for the TTRPG Campaign Manager GUI.

Works both ways:

    python -m src.main
    python src/main.py

The second form is useful because VS Code's debugger often launches a file
rather than a module.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path
from tkinter import messagebox

# When VS Code runs this file directly, relative imports such as `.app` do not
# work because Python does not treat the file as part of the `src` package.
# Adding the project root to sys.path lets us use the absolute import below.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app import run_app


def main() -> None:
    print("Running main() in src/main.py")
    print(f"Current working directory: {Path.cwd()}")
    """Start the GUI and show useful errors if startup fails."""
    try:
        print("Starting the TTRPG Campaign Manager...")
        run_app()
        print("The TTRPG Campaign Manager has exited.")
    except Exception as error:  # pragma: no cover - defensive startup handling
        print("The TTRPG Campaign Manager could not start.", file=sys.stderr)
        print(str(error), file=sys.stderr)
        traceback.print_exc()

        try:
            messagebox.showerror(
                "TTRPG Campaign Manager startup error",
                f"The application could not start.\n\n{error}\n\nSee the terminal for details.",
            )
        except Exception:
            pass

        raise SystemExit(1) from error


if __name__ == "__main__":
    print("Running main.py directly. This is expected when using VS Code's debugger.")
    main()
