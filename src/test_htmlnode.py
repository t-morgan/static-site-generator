import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode()
        actual = node.props_to_html()
        expected = ''
        self.assertEqual(actual, expected)
        
    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
            }
        )
        actual = node.props_to_html()
        expected = ' href="https://www.google.com"'
        self.assertEqual(actual, expected)

    def test_props_to_html_separation(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        actual = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(actual, expected)
        
    def test_leafnod_to_htmle_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        actual = node.to_html()
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(actual, expected)

    def test_leafnode_to_html_with_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        actual = node.to_html()
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(actual, expected)
    
    def test_leafnode_to_html_no_tag(self):
        node = LeafNode(None, "No Tag!")
        self.assertEqual(node.to_html(), "No Tag!")

    def test_leafnode_to_html_no_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parentnode_with_mixed_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        actual = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(actual, expected)
        
    def test_parentnode_with_grandchildren(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Header text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        actual = node.to_html()
        expected = "<div><h1>Header text</h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
