"""Generic plan benefits summary page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement

from t_pom_dentaquest.elements.table_element import TableElement


class PlanBenefitSummaryPage(BasePage):
    """Page class containing elements specific to a plan benefits summary page interface."""

    url = "https://govservices.dentaquest.com/Logon.jsp"

    eligibility_list_button = ButtonElement('//a[text()="Member Eligibility List"]')
    benefit_summary_table = TableElement('//table[@class="results"]')
    verification_element = eligibility_list_button
