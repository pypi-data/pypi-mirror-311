"""Generic home page for web app."""

from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement

from t_pom_dentaquest.elements.select_dropdown_element import SelectDropdownElement


class HomePage(BasePage):
    """Page class containing elements specific to a home page interface."""

    url = "https://govservices.dentaquest.com/Logon.jsp"

    patient_tab = ButtonElement('//*[@id="Link003"]')
    member_eligibility_search = ButtonElement('//*[@id="003"]/li[2]/a')
    select_dropdown_option = SelectDropdownElement('//select[@name="PROV_AFFILIATIONXPROV_AFFILIATION_ID"]')
    verification_element = patient_tab
