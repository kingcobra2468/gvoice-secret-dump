from abc import ABC, abstractmethod

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from googlesecretdump.platforms.utils.navigation_utils import human_like_sleep
from googlesecretdump.platforms.base.cookie import Cookie


class GoogleSecretsGenerator(ABC):
    """Selenium-based secret generator for Google cookies and API key."""

    def __init__(self, email, password, chrome_version=None):
        """Constructor.

        Args:
            email (str): Google email.
            password (str): Google password.
            chrome_version (str, optional): Chrome version to use. In the case of this
            error: https://github.com/ultrafunkamsterdam/undetected-chromedriver#words-of-wisdom ,
            pass in the Chrome version that is already installed.
        """
        self._email = email
        self._password = password
        self._chrome_version = chrome_version
        self._driver = None

        self._init_driver()

    def _init_driver(self):
        """Initialize the Chrome webdriver."""
        options = uc.ChromeOptions()
        # Improve Chrome stability in constrained container environments.
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-features=VizDisplayCompositor")

        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )

        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        self._driver = uc.Chrome(options=options, version_main=self._chrome_version)

    def ensure_signed_in(self):
        if not self.is_signed_in():
            self.login()

    @abstractmethod
    def is_signed_in(self):
        pass

    def login(self):
        """Login into the google account and navigate to the Google voice page."""
        self._driver.get("https://www.google.com/")
        self._driver.find_element(By.LINK_TEXT, "Sign in").click()
        email_entry = self._driver.find_element(By.ID, "identifierId")
        email_entry.send_keys(self._email)
        human_like_sleep(3, 0.5)
        email_entry.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER)
        human_like_sleep(3, 0.5)
        ActionChains(self._driver).send_keys(
            self._password + Keys.TAB + Keys.TAB + Keys.ENTER
        ).perform()
        human_like_sleep(3, 0.5)

    @abstractmethod
    def get_secrets(self):
        pass

    def _load_google_cookies(self, cookies: list[Cookie]):
        """Loads the cookies into a new session.

        Args:
            cookies (list): list of Google cookies to load.
        """
        self._driver.get("https://www.google.com/")
        google_cookies = [
            cookie for cookie in cookies if ".google.com" == cookie.domain
        ]

        for cookie in google_cookies:
            self._driver.add_cookie(cookie.model_dump())

    def load_cookies(self, cookies: list[Cookie]):
        self._load_google_cookies(cookies)

    @abstractmethod
    def refresh(self):
        pass
