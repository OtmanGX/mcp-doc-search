import re
from selectolax.parser import HTMLParser, Node


class DocParser:
    @staticmethod
    def clean_html(tree: HTMLParser):
        """Conservative cleaning - only obvious noise."""
        selectors = [
            "nav", "footer", "aside", "script", "style", "noscript",
            "[class*='sidebar']", "[id*='sidebar']",
            "[class*='advert']", "[class*='ad-']",
            ".sp-wrapper", "[class*='sandpack']"
        ]
        # Clean AFTER finding content to avoid breaking structure
        for sel in selectors:
            for node in tree.css(sel):
                node.decompose()

    @staticmethod
    def find_content(tree: HTMLParser) -> Node:
        """Generic main content detection - multiple fallbacks."""
        selectors = [
            "main", "article", "[role='main']",
            ".content", "#content", ".main-content",
            ".post-content", ".entry-content",
            ".markdown-body", ".prose", ".mdx-content",
            "div[data-page]", "[class*='content']"
        ]
        for sel in selectors:
            if node := tree.css_first(sel):
                return node

        # Fallback: largest text container
        max_text = 0
        best_node = tree.body or tree.root
        for div in tree.css("div"):
            text_len = len(div.text(strip=True))
            if text_len > max_text and text_len > 200:
                max_text = text_len
                best_node = div
        return best_node

    @staticmethod
    def to_markdown(node: Node) -> str:
        """Generic text extraction with broad tag support."""
        parts = []
        for n in node.traverse():
            text = n.text(separator=' ', strip=True)
            if not text or len(text) < 3:
                continue

            tag = n.tag
            if tag.startswith('h') and len(tag) == 2 and tag[1].isdigit():
                level = int(tag[1])
                parts.append(f"\n{'#' * level} {text}\n")
            elif tag in ('p', 'div', 'span'):  # div catches non-semantic content
                parts.append(f"\n{text}\n")
            elif tag == 'li':
                parts.append(f"- {text}\n")
            elif tag == 'pre':
                parts.append(f"\n``````\n")
            elif tag == 'code' and n.parent.tag != 'pre':
                parts.append(f"`{text}` ")

        result = "".join(parts)
        return re.sub(r'\n{3,}', '\n\n', result).strip()

    def parse(self, html: str) -> str:
        tree = HTMLParser(html)
        content = self.find_content(tree)  # Find FIRST
        self.clean_html(tree)  # Clean AFTER
        markdown = self.to_markdown(content)
        return markdown if len(markdown) > 50 else "No content found"
