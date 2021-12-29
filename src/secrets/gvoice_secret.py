from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os.path
from time import sleep
import undetected_chromedriver as uc
import json
import re


class GVoiceSecret:
    """Selenium-based client for pulling key and cookie secrets for
    Google Voice.
    """

    def __init__(self, email, password):
        """Constructor.

        Args:
            email (str): Google email.
            password (str): Google password;
        """
        self._email = email
        self._password = password
        self._driver = None

        self._init_driver()

    def _init_driver(self):
        """Initialize the Chrome webdriver.
        """
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')

        self._driver = uc.Chrome(options=options)

    def dump_secrets(self, to_file=False, dir=None):
        """Fetches the cookie and gvoice key secrets.

        Args:
            to_file (bool, optional): Whether to save the secrets to a file.
            Defaults to False.
            dir (str, optional): Directory where to dump the secrets if saving
            to a file. Defaults to None.

        Returns:
            dict: dictionary containing cookies and gvoice_key for cookie and
            gvoice secrets respectively.
        """
        secrets = dict()
        secrets['cookies'] = self._driver.get_cookies()
        secrets['gvoice_key'] = self.__get_key(self._driver.page_source)

        if to_file:
            with open(os.path.join(dir, 'secrets.json'), 'w') as fd:
                fd.write(json.dumps(secrets, indent=4, sort_keys=True))

        return secrets

    def __get_key(self, gvoice_source):
        """Extracts the Google voice API key from the page source.

        Args:
            gvoice_source (str): source for the Google voice page. 

        Raises:
            ValueError: raised if the secret cannot be found.

        Returns:
            str: the api key secret.
        """
        matches = re.search(r'https://www.googleapis.com","(.*?)"',
                            gvoice_source, re.MULTILINE)
        if not matches:
            raise ValueError('Unable to find GVoice key.')
        key = matches.groups()[0]

        return key

    def login(self):
        """Login into the google account and navigate to the Google voice page.
        """
        self._driver.get('https://www.google.com/')
        self._driver.find_element_by_link_text("Sign in").click()
        email_entry = self._driver.find_element_by_id('identifierId')
        email_entry.send_keys(self._email)
        sleep(2)
        email_entry.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER)
        sleep(2)
        ActionChains(self._driver).send_keys(self._password +
                                             Keys.TAB + Keys.TAB + Keys.ENTER).perform()
        sleep(2)
        self._driver.get('https://voice.google.com/u/0/')
