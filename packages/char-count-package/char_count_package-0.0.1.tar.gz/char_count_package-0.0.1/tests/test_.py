""""
Tests to test the script.
"""

from unittest.mock import mock_open, patch
import sys
import pytest
from src import char_count_package


def test_read_file():
    """Test the read file function"""
    mock_file_content = "mocked_content"
    mocked_file_obj = mock_open(read_data=mock_file_content)

    with patch("builtins.open", mocked_file_obj) as mocked_file:
        result = char_count_package.read_file("text.txt")

        assert result == mock_file_content
        mocked_file.assert_called_once_with("text.txt", "r", encoding="utf-8")


def test_process_parameter_string():
    """Test processing a string"""
    mocked_data = "abbbccdfk"
    test_args = ["task.py", "--string", mocked_data]

    with patch("sys.argv", test_args):
        result = char_count_package.process_parameter()
        assert result == 4


def test_process_parameter_filepath(monkeypatch):
    """Test processing a file through a filepath"""
    mocked_file_path = "files\\text.txt"
    mocked_args = ["task.py", "--filepath", mocked_file_path]

    monkeypatch.setattr(sys, "argv", mocked_args)
    result = char_count_package.process_parameter()
    assert result == 3


def test_process_parameter_with_wrong_filepath(capsys, monkeypatch):
    """Test wrong file path input"""
    mocked_filepath = "files\\t.txt"
    mocked_args = ["task.py", "--filepath", mocked_filepath]

    monkeypatch.setattr(sys, "argv", mocked_args)
    with pytest.raises(SystemExit) as exit_info:
        char_count_package.process_parameter()
    captured = capsys.readouterr()

    assert "Please review your parameter:" in captured.err
    assert "it is not a file path" in captured.err
    assert exit_info.value.code == 2


def test_process_parameter_missing_required_arg(capsys, monkeypatch):
    """Test missing requirement argument"""
    mocked_param = None
    mocked_args = ["task.py", mocked_param]

    monkeypatch.setattr(sys, "argv", mocked_args)
    with pytest.raises(SystemExit):
        char_count_package.process_parameter()
    captured = capsys.readouterr()
    assert "Error: Required arguments are missing." in captured.err
