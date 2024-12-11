from pathlib import Path

from bddssg.generate import generate_page, generate_pages_recursive
from bddssg.static import copy_static_files, empty_dir


def main():
    source = Path("static/")
    dest = Path("public/")

    empty_dir(dest)
    copy_static_files(source, dest)

    content_dir = Path("content")
    template_path = Path("template.html")

    generate_pages_recursive(content_dir, template_path, dest)


if __name__ == "__main__":
    main()
