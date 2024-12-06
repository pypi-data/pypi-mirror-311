"""Class for container elements."""
from ..base_element import BaseElement
from t_object import ThoughtfulObject  # type: ignore
from typing import Type, TypeVar

TO = TypeVar("TO", bound=ThoughtfulObject)


class ContainerElement:
    """Container element. Used to hold multiple text elements."""

    def __init__(self, *args: BaseElement) -> None:
        """Initializes a container element with list of text elements.

        Args:
            *args (list[TextElement]): List of text elements

        """
        self.elements: tuple[BaseElement, ...] = args

    def get_text_values(self, cls: Type[TO]) -> Type[TO]:
        """Get text for each element with id matching class attribute.

        Args:
            cls (Type[TO]): The class to use for the object.

        Returns:
            Instance of input class with text values.
        """
        kwargs = {}
        for k, _ in cls.__annotations__.items():
            for element in self.elements:
                if element.id == k:
                    text = element.get_text()
                    kwargs[k] = "" if not text else text
        return cls(**kwargs)

    def set_text_values(self, cls: Type[TO]) -> None:
        """Sets text for each element with id matching class attribute.

        Args:
            cls (Type[TO]): The object to use for the text values.
        """
        for k, _ in cls.__annotations__.items():
            for element in self.elements:
                if element.id == k:
                    element.click_and_input_text(cls.__dict__[k])
