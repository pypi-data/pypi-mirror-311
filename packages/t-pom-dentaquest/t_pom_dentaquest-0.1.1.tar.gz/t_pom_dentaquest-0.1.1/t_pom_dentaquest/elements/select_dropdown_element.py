"""Select dropdown element module."""
from t_page_object.base_element import BaseElement


class SelectDropdownElement(BaseElement):
    """Class for select dropdown elements."""

    def select_options(self, option: str) -> None:
        """Select options from the dropdown list."""
        self.select_from_list_by_value(option)
