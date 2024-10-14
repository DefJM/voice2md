import pytest
from pathlib import Path
import shutil
import os
from copy_voice_memos import get_voice_memos

# helper function to create temporary directories
@pytest.fixture
def temp_dirs(tmp_path):
    """
    Create temporary directories for testing.
    """
    source_dir = tmp_path / "source"
    destination_dir = tmp_path / "destination"
    source_dir.mkdir()
    destination_dir.mkdir()
    return source_dir, destination_dir

# helper function to create test files
def create_test_file(path, size_mb, content=""):
    """
    Create a test file with the given size in MB.
    """
    with open(path, "wb") as f:
        f.write(b"0" * int(size_mb * 1024 * 1024))
        f.write(content.encode())


def test_get_voice_memos(temp_dirs):
    """
    Test the get_voice_memos function with various scenarios.
    """
    source_dir, destination_dir = temp_dirs
    
    # Create test files
    create_test_file(source_dir / "small_file.m4a", 0.1)
    create_test_file(source_dir / "large_file.m4a", 150)
    create_test_file(source_dir / "medium_file.m4a", 50)
    
    result = get_voice_memos(source_dir, destination_dir, "m4a", 100.0)
    
    assert result["total_files"] == 3
    assert result["copied_files"] == 2
    assert result["skipped_files"] == 1
    assert "small_file.m4a" in result["copied_file_names"]
    assert "medium_file.m4a" in result["copied_file_names"]
    assert "large_file.m4a" in result["skipped_file_names"]
    
    assert (destination_dir / "small_file.m4a").exists()
    assert (destination_dir / "medium_file.m4a").exists()
    assert not (destination_dir / "large_file.m4a").exists()

def test_get_voice_memos_unchanged_files(temp_dirs):
    """
    Test the get_voice_memos function with unchanged files.
    """
    source_dir, destination_dir = temp_dirs
    
    # Create a file in both source and destination
    create_test_file(source_dir / "unchanged.m4a", 0.1, "test content")
    shutil.copy2(source_dir / "unchanged.m4a", destination_dir / "unchanged.m4a")
    
    result = get_voice_memos(source_dir, destination_dir, "m4a", 100.0)
    
    assert result["total_files"] == 1
    assert result["unchanged_files"] == 1
    assert "unchanged.m4a" in result["unchanged_file_names"]

def test_get_voice_memos_empty_source(temp_dirs):
    """
    Test the get_voice_memos function with an empty source directory.
    """
    source_dir, destination_dir = temp_dirs
    
    result = get_voice_memos(source_dir, destination_dir, "m4a", 100.0)
    
    assert result["total_files"] == 0
    assert result["copied_files"] == 0
    assert result["skipped_files"] == 0
    assert result["unchanged_files"] == 0
