from pydantic import BaseModel, Field

from googlesecretdump.platforms.base.cookie import Cookie


class GoogleSecretsContext(BaseModel):
    cookies: list[Cookie] = Field(default_factory=list)

    def get_cookies(self):
        """Returns the list of cookies.

        Returns:
            list: A list of cookies.
        """
        return self.cookies

    def get_google_cookies(self):
        """Returns the cookies for the Google domain.

        Returns:
            list: A list of cookies for the Google domain.
        """
        return [
            cookie
            for cookie in self.cookies
            if ".google.com" == cookie.domain
        ]

    def save_cookies_to_cookies_txt(self, file_path):
        """Dumps active browser cookies in Netscape cookies.txt format.

        Args:
            file_path (str): path to the file where to save the cookies.
        """
        netscape_string = self._to_netscape_string(self.cookies)
        with open(file_path, "w") as file:
            file.write(netscape_string)

    def _to_netscape_string(self, cookies):
        result = []
        for cookie in cookies:
            domain = cookie.domain or ""
            expiration_date = cookie.expiry
            path = cookie.path or ""
            secure = cookie.secure or False
            name = cookie.name or ""
            value = cookie.value or ""

            include_sub_domain = domain.startswith(".") if domain else False
            expiry = str(int(expiration_date)) if expiration_date else "0"

            result.append(
                [
                    domain,
                    str(include_sub_domain).upper(),
                    path,
                    str(secure).upper(),
                    expiry,
                    name,
                    value,
                ]
            )

        return "\n".join("\t".join(cookie_parts) for cookie_parts in result)

    def save_secrets_to_json(self, file_path):
        """Saves the secrets to a JSON file.

        Args:
            file_path (str): path to the file where to save the secrets.
        """
        with open(file_path, "w") as file:
            file.write(self.model_dump_json(indent=2))

    @classmethod
    def read_secrets_from_json(cls, file_path):
        """Reads the secrets from a JSON file.

        Args:
            file_path (str): path to the file where to read the secrets.
        """
        with open(file_path, "r") as file:
            json_data = file.read()

        return cls.model_validate_json(json_data)
