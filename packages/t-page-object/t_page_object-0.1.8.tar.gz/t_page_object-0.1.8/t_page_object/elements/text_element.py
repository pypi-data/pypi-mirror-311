"""This module contains the TextElement class for the text element model."""
from ..base_element import BaseElement


class TextElement(BaseElement):
    """Input element."""

    def get_clean_text(self):
        """Get text from element and clean."""
        text = self.get_text().strip().lower()
        return text
