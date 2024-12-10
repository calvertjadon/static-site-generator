from pathlib import Path


def copy_static_files(source: Path, dest: Path) -> None:
    if not dest.exists():
        dest.mkdir()

    for child in source.glob("*"):
        if child.is_dir():
            copy_static_files(child, dest / child.name)
        else:
            copy = dest / child.name
            copy.write_bytes(child.read_bytes())


def empty_dir(dir: Path) -> None:
    if not dir.exists():
        return

    if not dir.is_dir():
        raise Exception("destination is not a directory", dir)

    for child in dir.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            empty_dir(child)
            child.rmdir()
