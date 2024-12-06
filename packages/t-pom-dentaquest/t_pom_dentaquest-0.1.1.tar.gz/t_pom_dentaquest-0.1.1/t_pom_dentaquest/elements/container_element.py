"""Select container element module."""
from t_page_object.elements.input_element import InputElement


class ContainerElement:
    """Class for container elements."""

    def __init__(self, *args: InputElement) -> None:
        """Container element constructor."""
        self.elements: list[InputElement] = list(args)

    def check_if_all_elements_contain_value(self) -> object:
        """Get text for each attribute in object with matching id."""
        all_filled = all(element.get_element_attribute("value") for element in self.elements)
        return all_filled
