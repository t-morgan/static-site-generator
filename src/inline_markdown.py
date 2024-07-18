from textnode import TextNode, text_type_text, text_type_image, text_type_link, text_type_bold, text_type_italic, text_type_code
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: closing delimiter ({delimiter}) missing in {old_node.text}"
            )
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        text_remaining = old_node.text
        for (alt_text, url) in matches:
            sections = text_remaining.split(f"![{alt_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(alt_text, text_type_image, url))
            text_remaining = sections[1]
        if text_remaining != "":
            new_nodes.append(TextNode(text_remaining, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        text_remaining = old_node.text
        for link_text, url in matches:
            sections = text_remaining.split(f"[{link_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link_text, text_type_link, url))
            text_remaining = sections[1]
        if text_remaining != "":
            new_nodes.append(TextNode(text_remaining, text_type_text))
    return new_nodes

delimiters = {
    text_type_bold: '**', text_type_italic: '*', text_type_code: '`'
}
def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    for delimiter in [text_type_bold, text_type_italic, text_type_code]:
        nodes = split_nodes_delimiter(nodes, delimiters[delimiter], delimiter)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes