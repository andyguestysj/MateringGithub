from src.data.file_manager import FileManager


def test_list_folders(tmp_path):
    (tmp_path / "campaign_a").mkdir()
    (tmp_path / "campaign_b").mkdir()
    (tmp_path / "not_a_campaign.txt").write_text("ignore me")
    assert FileManager.list_folders(tmp_path) == ["campaign_a", "campaign_b"]
