"""Checkbox element module."""
from ..base_element import BaseElement


class CheckboxElement(BaseElement):
    """Checkbox element."""

    def select(self) -> None:
        """Selects the checkbox element."""
        self.click_element_when_visible()
