from typing import Optional

def ask_text(prompt: str, default: Optional[str] = None) -> str:
    if default is None:
        value = input(f"{prompt}: ").strip()
    else:
        value = input(f"{prompt} [{default}]: ").strip()
    return value if value else (default or "")

def ask_int(prompt: str, default: Optional[int] = None) -> int:
    while True:
        text = ask_text(prompt, str(default) if default is not None else None)
        try:
            return int(text)
        except ValueError:
            print("Please enter a whole number.")

def pause() -> None:
    input("\nPress Enter to continue...")
