"""Generic login page member eligibility list web app."""
from t_page_object.base_page import BasePage

from t_pom_dentaquest.elements.text_element import TextElement


class MemberEligibilityListPage(BasePage):
    """Page class containing elements specific to a member eligibility list page interface."""

    url = "https://govservices.dentaquest.com/Logon.jsp"

    is_table_contain_data = TextElement('//th[text()="Plan"]/ancestor::thead/following-sibling::tbody//tr//th')
    is_active_table_populated = TextElement('//caption[@class="tableCaption"]')
    verification_element = is_active_table_populated
