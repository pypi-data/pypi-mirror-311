"""Generic base class for web app."""
from RPA.Browser.Selenium import Selenium
from t_page_object.base_app import BaseApp
from t_page_object.selenium_manager import SeleniumManager
from pathlib import Path
from t_pom_dentaquest.pages.home_page import HomePage
from t_pom_dentaquest.pages.login_page import LoginPage
from t_pom_dentaquest.pages.member_detail_page import MemberDetailPage
from t_pom_dentaquest.pages.member_eligibility_list_page import MemberEligibilityListPage
from t_pom_dentaquest.pages.member_eligibility_search_page import MemberEligibilitySearchPage
from t_pom_dentaquest.pages.plan_benefit_summary_page import PlanBenefitSummaryPage


class TDentaQuest(BaseApp):
    """Main application class managing pages and providing direct access to Selenium."""

    browser: Selenium = None
    login_page: LoginPage = LoginPage()
    home_page: HomePage = HomePage()
    member_eligibility_search_page: MemberEligibilitySearchPage = MemberEligibilitySearchPage()
    member_eligibility_list_page: MemberEligibilityListPage = MemberEligibilityListPage()
    member_detail_page: MemberDetailPage = MemberDetailPage()
    benefit_summary_page: PlanBenefitSummaryPage = PlanBenefitSummaryPage()
    wait_time: int = 15
    download_directory: str = str(Path().cwd() / Path("temp"))

    def __init__(self, **config) -> None:
        """Initilise DentaQuest class with default configuration."""
        super().__init__(**config)
        self.browser = SeleniumManager.get_instance()
