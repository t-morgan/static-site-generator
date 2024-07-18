import os
import pathlib
import shutil

from markdown_blocks import markdown_to_html_node


def main():
    copy_contents()
    generate_pages_recursive("content", "template.html", "public")


def copy_contents(source="static", destination="public"):
    if os.path.isdir(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    for item in os.listdir(source):
        sub_source = os.path.join(source, item)
        sub_destination = os.path.join(destination, item)
        if os.path.isfile(sub_source):
            shutil.copy(sub_source, sub_destination)
        else:
            os.mkdir(sub_destination)
            copy_contents(sub_source, sub_destination)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# ") and len(line) > 2:
            return line[2:].strip()
    raise ValueError("No title found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        content = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    full_html = template.replace("{{ Title }}", title)
    full_html = template.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        print(full_html, file=f)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path="public"):
    for item in os.listdir(dir_path_content):
        item_source = os.path.join(dir_path_content, item)
        item_dest = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_source):
            item_path = pathlib.Path(item)
            item_name = item.replace(item_path.suffix, "")
            item_dest = os.path.join(dest_dir_path, f"{item_name}.html")
            generate_page(item_source, template_path, item_dest)
        else:
            generate_pages_recursive(item_source, template_path, item_dest)


if __name__ == "__main__":
    main()
