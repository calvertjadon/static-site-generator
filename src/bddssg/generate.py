from pathlib import Path

from bddssg.convert import markdown_to_html_node


def extract_title(md: str) -> str:
    for line in md.split("\n"):
        try:
            level, other = line.split(" ", 1)
            if level == "#":
                return other.strip()
        except ValueError:
            continue

    raise Exception("no title found")


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    assert from_path.is_file()
    assert template_path.exists()
    assert not dest_path.exists()

    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    md = from_path.read_text()
    template = template_path.read_text()

    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    result = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    dest_path.write_text(result)


def generate_pages_recursive(
    content_dir: Path, template_path: Path, dest_dir: Path
) -> None:
    for child in content_dir.glob("*"):
        if child.is_file():
            dest_path = dest_dir / f"{child.stem}.html"
            generate_page(child, template_path, dest_path)
        else:
            (dest_dir / child.name).mkdir()
            generate_pages_recursive(child, template_path, dest_dir / child.name)
