import json

from googlesecretdump.platforms.base.google_secrets_generator import (
    GoogleSecretsGenerator,
)
from googlesecretdump.platforms.youtubemusic.youtube_music_secrets_context import (
    YoutubeMusicSecretsContext,
)
from googlesecretdump.platforms.utils.navigation_utils import human_like_sleep
from googlesecretdump.platforms.base.cookie import Cookie


class YoutubeMusicSecretsGenerator(GoogleSecretsGenerator):
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
        """Fetches the YouTube Music secrets.

        Returns:
            YoutubeMusicSecretsContext: The context containing the cookies, API key, and phone number.
        """
        cookies = self._driver.get_cookies()

        return YoutubeMusicSecretsContext(
            cookies=cookies
        )

    def login(self):
        """Login into the google account and navigate to the YouTube Music page."""
        super().login()
        human_like_sleep(3, 0.5)
        self._navigate_to_youtube_music()

    def is_signed_in(self):
        """Checks if the user is signed in.

        Returns:
            bool: True if signed in. False otherwise.
        """
        self._navigate_to_youtube_music()
        return "music.youtube.com" in self._driver.current_url

    def load_cookies(self, cookies: list[Cookie]):
        """Loads the cookies into a new session.

        Args:
            cookies (list): list of cookies to load.
        """
        super().load_cookies(cookies)
        self.load_youtube_music_cookies(cookies)

    def load_youtube_music_cookies(self, cookies: list[Cookie]):
        """Loads the YouTube Music cookies into a new session.

        Args:
            youtube_music_cookies (list): list of YouTube Music cookies to load.
        """
        self._navigate_to_youtube_music()
        youtube_music_cookies = [
            cookie
            for cookie in cookies
            if ".music.youtube.com" == cookie.domain or ".youtube.com" == cookie.domain
        ]
        for cookie in youtube_music_cookies:
            self._driver.add_cookie(cookie.model_dump())

    def refresh(self):
        """Refreshes the cookies for the current session."""
        self._navigate_to_youtube_music()

    def ensure_signed_in(self):
        if not self.is_signed_in():
            self.login()

    def _navigate_to_youtube_music(self):
        """Navigates to the YouTube Music page."""
        self._driver.get("https://music.youtube.com/library")
        human_like_sleep(3, 0.5)

    def get_auth_headers(self):
        self._navigate_to_youtube_music()
        human_like_sleep(3, 0.5)

        logs = self._driver.get_log("performance")
        request_headers = None
        for entry in logs:
            log_data = json.loads(entry["message"])["message"]
            method = log_data.get("method")
            params = log_data.get("params", {})
            if method != "Network.requestWillBeSent":
                continue

            request = params.get("request", {})
            url = request.get("url", "")
            if "https://music.youtube.com/youtubei/v1/browse" not in url:
                continue

            request_headers = request.get("headers")
            break

        if request_headers is None:
            raise Exception("Failed to find the request headers for YouTube Music.")

        return request_headers
