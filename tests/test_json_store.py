from src.data.json_store import JsonStore


def test_add_and_load_entry(tmp_path):
    store = JsonStore(tmp_path / "characters.json")
    created = store.add({"name": "Test Hero", "class": "Bard", "level": "1", "description": "A test character"})
    assert created["id"] == 1
    assert store.load_all()[0]["name"] == "Test Hero"


def test_update_entry(tmp_path):
    store = JsonStore(tmp_path / "characters.json")
    created = store.add({"name": "Old Name"})
    result = store.update(created["id"], {"name": "New Name"})
    assert result is True
    assert store.find_by_id(created["id"])["name"] == "New Name"


def test_delete_entry(tmp_path):
    store = JsonStore(tmp_path / "characters.json")
    created = store.add({"name": "Temporary NPC"})
    result = store.delete(created["id"])
    assert result is True
    assert store.load_all() == []
