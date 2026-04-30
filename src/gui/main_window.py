import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Dict, List

from ..data.campaign_loader import CampaignLoader


class EntryEditor(tk.Toplevel):
    """Small modal window used for adding or editing an entry."""

    def __init__(self, parent: tk.Widget, title: str, fields: List[str], existing: Dict[str, Any] | None = None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result: Dict[str, Any] | None = None
        self.fields = fields
        self.inputs: Dict[str, tk.Text | ttk.Entry] = {}
        existing = existing or {}

        self.columnconfigure(1, weight=1)

        for row, field in enumerate(fields):
            label_text = field.replace("_", " ").title()
            ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="nw", padx=10, pady=6)

            if field == "description":
                widget = tk.Text(self, width=50, height=7, wrap="word")
                widget.insert("1.0", str(existing.get(field, "")))
            else:
                widget = ttk.Entry(self, width=50)
                widget.insert(0, str(existing.get(field, "")))

            widget.grid(row=row, column=1, sticky="ew", padx=10, pady=6)
            self.inputs[field] = widget

        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(fields), column=0, columnspan=2, sticky="e", padx=10, pady=10)

        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(button_frame, text="Save", command=self.save).pack(side="right")

        self.transient(parent)
        self.grab_set()
        self.wait_visibility()
        self.focus()

    def save(self) -> None:
        entry: Dict[str, Any] = {}
        for field, widget in self.inputs.items():
            if isinstance(widget, tk.Text):
                entry[field] = widget.get("1.0", "end").strip()
            else:
                entry[field] = widget.get().strip()

        if not entry.get("name"):
            messagebox.showerror("Missing name", "Please enter a name.", parent=self)
            return

        self.result = entry
        self.destroy()


class MainWindow(ttk.Frame):
    MENU_CONFIG = {
        "characters": ["name", "class", "level", "description"],
        "locations": ["name", "region", "description"],
        "monsters": ["name", "challenge_rating", "description"],
        "rules": ["name", "category", "description"],
        "adventures": ["name", "status", "description"],
    }

    DISPLAY_NAMES = {
        "characters": "Characters",
        "locations": "Locations",
        "monsters": "Monsters",
        "rules": "Rules",
        "adventures": "Adventures",
    }

    def __init__(self, root: tk.Tk, loader: CampaignLoader):
        super().__init__(root, padding=10)
        self.root = root
        self.loader = loader
        self.campaign_name = loader.get_default_campaign_name()
        self.data_type = "characters"
        self.entries: List[Dict[str, Any]] = []

        self.root.title("TTRPG Campaign Manager")
        self.root.geometry("900x560")
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.refresh_campaigns()
        self.refresh_entries()

    def create_widgets(self) -> None:
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(0, 10))

        ttk.Label(top_bar, text="Campaign:").pack(side="left")
        self.campaign_var = tk.StringVar()
        self.campaign_select = ttk.Combobox(top_bar, textvariable=self.campaign_var, state="readonly", width=28)
        self.campaign_select.pack(side="left", padx=(6, 18))
        self.campaign_select.bind("<<ComboboxSelected>>", self.on_campaign_changed)

        ttk.Label(top_bar, text="Data:").pack(side="left")
        self.data_var = tk.StringVar(value=self.data_type)
        self.data_select = ttk.Combobox(
            top_bar,
            textvariable=self.data_var,
            values=list(self.MENU_CONFIG.keys()),
            state="readonly",
            width=20,
        )
        self.data_select.pack(side="left", padx=(6, 18))
        self.data_select.bind("<<ComboboxSelected>>", self.on_data_type_changed)

        ttk.Button(top_bar, text="Refresh", command=self.refresh_entries).pack(side="right")

        main_area = ttk.PanedWindow(self, orient="horizontal")
        main_area.pack(fill="both", expand=True)

        left_panel = ttk.Frame(main_area, padding=(0, 0, 10, 0))
        right_panel = ttk.Frame(main_area)
        main_area.add(left_panel, weight=1)
        main_area.add(right_panel, weight=2)

        self.entry_list = tk.Listbox(left_panel, height=20)
        self.entry_list.pack(fill="both", expand=True)
        self.entry_list.bind("<<ListboxSelect>>", self.on_entry_selected)

        button_row = ttk.Frame(left_panel)
        button_row.pack(fill="x", pady=(10, 0))
        ttk.Button(button_row, text="Add", command=self.add_entry).pack(side="left")
        ttk.Button(button_row, text="Edit", command=self.edit_entry).pack(side="left", padx=6)
        ttk.Button(button_row, text="Delete", command=self.delete_entry).pack(side="left")

        ttk.Label(right_panel, text="Selected Entry").pack(anchor="w")
        self.details = tk.Text(right_panel, wrap="word", state="disabled")
        self.details.pack(fill="both", expand=True, pady=(6, 0))

        status_bar = ttk.Frame(self)
        status_bar.pack(fill="x", pady=(10, 0))
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(status_bar, textvariable=self.status_var).pack(side="left")

    def refresh_campaigns(self) -> None:
        campaigns = self.loader.list_campaigns()
        self.campaign_select["values"] = campaigns

        if not campaigns:
            self.campaign_name = None
            self.campaign_var.set("")
            messagebox.showwarning("No campaigns", "No campaign folders were found in campaigns/.")
            return

        if self.campaign_name not in campaigns:
            self.campaign_name = campaigns[0]
        self.campaign_var.set(self.campaign_name)

    def get_store(self):
        if self.campaign_name is None:
            return None
        return self.loader.get_store(self.campaign_name, self.data_type)

    def refresh_entries(self) -> None:
        self.entry_list.delete(0, "end")
        self.clear_details()

        store = self.get_store()
        if store is None:
            self.entries = []
            self.status_var.set("No campaign selected")
            return

        try:
            self.entries = store.load_all()
        except Exception as error:
            messagebox.showerror("Could not load data", str(error))
            self.entries = []

        for entry in self.entries:
            self.entry_list.insert("end", f'{entry.get("id", "?")}: {entry.get("name", "Unnamed")}')

        label = self.DISPLAY_NAMES.get(self.data_type, self.data_type)
        self.status_var.set(f"Loaded {len(self.entries)} {label.lower()} from {self.campaign_name}")

    def selected_entry(self) -> Dict[str, Any] | None:
        selection = self.entry_list.curselection()
        if not selection:
            return None
        return self.entries[selection[0]]

    def on_campaign_changed(self, _event=None) -> None:
        self.campaign_name = self.campaign_var.get()
        self.refresh_entries()

    def on_data_type_changed(self, _event=None) -> None:
        self.data_type = self.data_var.get()
        self.refresh_entries()

    def on_entry_selected(self, _event=None) -> None:
        entry = self.selected_entry()
        if entry is None:
            self.clear_details()
            return

        lines = []
        for key, value in entry.items():
            label = key.replace("_", " ").title()
            lines.append(f"{label}: {value}")
        self.set_details("\n\n".join(lines))

    def clear_details(self) -> None:
        self.set_details("")

    def set_details(self, text: str) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text)
        self.details.configure(state="disabled")

    def add_entry(self) -> None:
        store = self.get_store()
        if store is None:
            return

        editor = EntryEditor(self.root, f"Add {self.DISPLAY_NAMES[self.data_type][:-1]}", self.MENU_CONFIG[self.data_type])
        self.root.wait_window(editor)

        if editor.result is not None:
            store.add(editor.result)
            self.refresh_entries()

    def edit_entry(self) -> None:
        store = self.get_store()
        entry = self.selected_entry()
        if store is None or entry is None:
            messagebox.showinfo("No selection", "Please select an entry to edit.")
            return

        editor = EntryEditor(
            self.root,
            f"Edit {entry.get('name', 'Entry')}",
            self.MENU_CONFIG[self.data_type],
            existing=entry,
        )
        self.root.wait_window(editor)

        if editor.result is not None:
            store.update(int(entry["id"]), editor.result)
            self.refresh_entries()

    def delete_entry(self) -> None:
        store = self.get_store()
        entry = self.selected_entry()
        if store is None or entry is None:
            messagebox.showinfo("No selection", "Please select an entry to delete.")
            return

        confirmed = messagebox.askyesno(
            "Delete entry",
            f"Delete {entry.get('name', 'this entry')}?",
        )
        if confirmed:
            store.delete(int(entry["id"]))
            self.refresh_entries()


def run_gui(loader: CampaignLoader) -> None:
    root = tk.Tk()
    MainWindow(root, loader)
    root.mainloop()
