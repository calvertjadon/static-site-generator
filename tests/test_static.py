from pathlib import Path

from bddssg.static import copy_static_files, empty_dir


def test_empty(tmp_path: Path):
    dest = tmp_path / "source"
    dest.mkdir()

    file = dest / "file"
    file.touch()

    dir = dest / "dir"
    dir.mkdir()

    nested = dir / "nested"
    nested.touch()

    empty_dir(dest)
    assert not list(dest.glob("*"))


def test_static(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()

    dest = tmp_path / "dest"

    file = source / "file"
    file.touch()

    dir = source / "dir"
    dir.mkdir()

    nested = dir / "nested"
    nested.touch()

    copy_static_files(source, dest)

    assert dest.exists()
    assert dest.is_dir()
    assert (dest / "file").exists()
    assert (dest / "dir").exists()
    assert (dest / "dir/nested").exists()
