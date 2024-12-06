"""Generic member detail page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement

from t_pom_dentaquest.elements.table_element import TableElement


class MemberDetailPage(BasePage):
    """Page class containing elements specific to a login interface."""

    url = "https://govservices.dentaquest.com/Logon.jsp"

    member_name_button = ButtonElement('(//table[@class="results"]//tbody//td)[4]')
    plan_button = ButtonElement(
        '//table[@class="results"]//caption[contains(text(), ' '"Eligibility Information")]/following::tbody[1]//th//a',
    )
    eligibility_list_button = ButtonElement('//a[text()="Member Eligibility List"]')
    service_history_button = ButtonElement('//table[@class="sectiontitle"]/tbody/tr/td/a[3]')
    benefit_detail_table = TableElement('//table[@class="results"]')

    verification_element = member_name_button
