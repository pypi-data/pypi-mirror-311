"""Generic login page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement


class LoginPage(BasePage):
    """Page class containing elements specific to a login interface."""

    url = "https://govservices.dentaquest.com/Logon.jsp"
    user_id_input = InputElement("//input[@id='USERSXUSERNAME']")
    password_input = InputElement("//input[@id='USERSXPASSWORD']")
    login_in_button = ButtonElement("//input[@value='Login']")

    verification_element = user_id_input
