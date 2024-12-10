from pathlib import Path

from bddssg.static import copy_static_files, empty_dir
from bddssg.textnode import TextNode, TextType


def main():
    source = Path("static/")
    dest = Path("public/")

    empty_dir(dest)
    copy_static_files(source, dest)


if __name__ == "__main__":
    main()
