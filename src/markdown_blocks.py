import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown_block):
    heading_match = re.search(r"^#{1,6} ", markdown_block)
    if heading_match is not None:
        return block_type_heading

    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return block_type_code

    lines = markdown_block.split("\n")

    is_quote_block = False
    for line in lines:
        if line.startswith(">"):
            is_quote_block = True
        else:
            is_quote_block = False
            break
    if is_quote_block:
        return block_type_quote

    is_unordered_list_block = False
    for line in lines:
        if line.startswith("* ") or line.startswith("- "):
            is_unordered_list_block = True
        else:
            is_unordered_list_block = False
            break
    if is_unordered_list_block:
        return block_type_ulist

    is_ordered_list_block = False
    for line in lines:
        if re.search(r"^\d+\. ", line) is not None:
            is_ordered_list_block = True
        else:
            is_ordered_list_block = False
            break
    if is_ordered_list_block:
        return block_type_olist

    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    block_split = block.split(" ", 1)
    if len(block_split) != 2:
        raise ValueError(f"Invalid heading text: {block}")
    level = len(block_split[0])
    if level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    text = block_split[1]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.split(" ", 1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.split(" ", 1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
