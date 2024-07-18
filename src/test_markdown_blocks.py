import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_block(self):
        block_type = block_to_block_type("This is a paragraph.\nOf text.")
        self.assertEqual(block_type, "paragraph")
    
    def test_heading_one_block(self):
        block_type = block_to_block_type("# Heading One")
        self.assertEqual(block_type, "heading")
    
    def test_heading_six_block(self):
        block_type = block_to_block_type("###### Heading Six")
        self.assertEqual(block_type, "heading")
    
    def test_heading_more_than_six(self):
        block_type = block_to_block_type("####### Heading Bad")
        self.assertEqual(block_type, "paragraph")
    
    def test_hash_no_space(self):
        block_type = block_to_block_type("#######Heading Bad")
        self.assertEqual(block_type, "paragraph")
    
    def test_code(self):
        block_type = block_to_block_type("```def code_block(self):\n    print('Hello world!')```")
        self.assertEqual(block_type, "code")
    
    def test_code_no_closing_ticks(self):
        block_type = block_to_block_type(
            "```def code_block(self):\n    print('Hello world!')"
        )
        self.assertEqual(block_type, "paragraph")
    
    def test_quote(self):
        block_type = block_to_block_type(
            ">Quote block"
        )
        self.assertEqual(block_type, "quote")
    
    def test_quote_multiline(self):
        block_type = block_to_block_type(">Quote block\n>Another line\n>Third line")
        self.assertEqual(block_type, "quote")
    
    def test_unordered_list_asterisk(self):
        block_type = block_to_block_type("* Unordered list asterisk")
        self.assertEqual(block_type, "unordered_list")
    
    def test_unordered_list_dash(self):
        block_type = block_to_block_type("- Unordered list dash")
        self.assertEqual(block_type, "unordered_list")
    
    def test_unordered_list_mixed(self):
        block_type = block_to_block_type("* Unordered list asterisk\n- Unordered list dash\n- Third item\n* Fourth item")
        self.assertEqual(block_type, "unordered_list")
    
    def test_ordered_list(self):
        block_type = block_to_block_type("1. Ordered list")
        self.assertEqual(block_type, "ordered_list")
    
    def test_ordered_list_multiline(self):
        block_type = block_to_block_type("1. Ordered list\n1. Second item\n3. Third")
        self.assertEqual(block_type, "ordered_list")


if __name__ == "__main__":
    unittest.main()
