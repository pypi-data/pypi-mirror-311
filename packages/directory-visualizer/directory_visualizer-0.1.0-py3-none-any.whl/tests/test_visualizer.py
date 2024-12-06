# Unit tests for your visualizer functions

from visualizer.visualizer import generate_markdown, generate_mermaid

def test_generate_markdown(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("test")
    output_file = tmp_path / "output.md"
    generate_markdown(str(test_dir), str(output_file))
    assert output_file.read_text().startswith("# Directory Structure")

def test_generate_mermaid(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("test")
    output_file = tmp_path / "output.mmd"
    generate_mermaid(str(test_dir), str(output_file))
    assert "graph TD" in output_file.read_text()

