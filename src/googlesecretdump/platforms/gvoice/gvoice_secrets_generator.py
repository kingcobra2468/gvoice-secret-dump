import re

from googlesecretdump.platforms.base.google_secrets_generator import GoogleSecretsGenerator
from googlesecretdump.platforms.utils.navigation_utils import human_like_sleep
from googlesecretdump.platforms.base.cookie import Cookie
from googlesecretdump.platforms.gvoice.gvoice_secrets_context import GvoiceSecretsContext


class GvoiceSecretsGenerator(GoogleSecretsGenerator):
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
        super().__init__(email, password, chrome_version=chrome_version)

    def get_secrets(self):
        """Fetches the Google Voice secrets.

        Returns:
            GvoiceSecretsContext: The context containing the cookies, API key, and phone number.
        """
        cookies = self._driver.get_cookies()
        gvoice_key = self.__get_key(self._driver.page_source)
        phone_number = self.__get_phone_number(self._driver.page_source)

        return GvoiceSecretsContext(
            cookies=cookies, gvoice_key=gvoice_key, phone_number=phone_number
        )

    def __get_key(self, gvoice_source):
        """Extracts the Google voice API key from the page source.

        Args:
            gvoice_source (str): source for the Google voice page.

        Raises:
            ValueError: raised if the secret cannot be found.

        Returns:
            str: the api key secret.
        """
        matches = re.search(
            r'https://www.googleapis.com","(.*?)"', gvoice_source, re.MULTILINE
        )
        if not matches:
            raise ValueError("Unable to find GVoice key.")
        key = matches.groups()[0]

        return key

    def __get_phone_number(self, gvoice_source):
        """Extracts the Google voice number for the given account

        Args:
            gvoice_source (str): source for the Google voice page.

        Raises:
            ValueError: raised if phone number not found.

        Returns:
            str: the google voice phone number.
        """
        matches = re.search(r'phnnmbr.*"\+(1[0-9]{10})"', gvoice_source, re.MULTILINE)
        if not matches:
            raise ValueError(
                "Unable to find GVoice phone number. Have you added a number for this account?"
            )
        key = matches.groups()[0]

        return key

    def login(self):
        """Login into the google account and navigate to the Google voice page."""
        super().login()
        human_like_sleep(3, 0.5)
        self._navigate_to_gvoice()

    def is_signed_in(self):
        """Checks if the user is signed in.

        Returns:
            bool: True if signed in. False otherwise.
        """
        self._navigate_to_gvoice()
        return "voice.google.com" in self._driver.current_url

    def load_cookies(self, cookies: list[Cookie]):
        """Loads the cookies into a new session.

        Args:
            cookies (list): list of cookies to load.
        """
        super().load_cookies(cookies)
        self.load_google_voice_cookies(cookies)

    def load_google_voice_cookies(self, cookies: list[Cookie]):
        """Loads the Google voice cookies into a new session.

        Args:
            google_voice_cookies (list): list of Google voice cookies to load.
        """
        self._navigate_to_gvoice()
        google_voice_cookies = [
            cookie
            for cookie in cookies
            if ".voice.google.com" == cookie.domain
        ]
        for cookie in google_voice_cookies:
            self._driver.add_cookie(cookie.model_dump())

    def refresh(self):
        """Refreshes the cookies for the current session."""
        self._navigate_to_gvoice()

    def ensure_signed_in(self):
        if not self.is_signed_in():
            self.login()

    def _navigate_to_gvoice(self):
        """Navigates to the Google voice page."""
        self._driver.get("https://voice.google.com/u/0/")
        human_like_sleep(3, 0.5)
