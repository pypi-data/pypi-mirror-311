"""Generic member eligibility search page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement

from t_pom_dentaquest.elements.container_element import ContainerElement


class MemberEligibilitySearchPage(BasePage):
    """Page class containing elements specific to a member eligibility search page interface."""

    url = "https://govservices.dentaquest.com/Logon.jsp"

    service_date_input = InputElement('//*[@id="Q061MEMBER0memberSearchDate"]')
    dob_input = InputElement('//*[@id="Q061MEMBER0dob"]')
    member_number = InputElement('//*[@id="Q061MEMBER0memberNo"]')
    search_button = ButtonElement('//input[@name="Search"]')
    search_again_button = ButtonElement('//input[@name="SearchAgain"]')

    verification_inputs = ContainerElement(dob_input, member_number)
    verification_element = service_date_input
