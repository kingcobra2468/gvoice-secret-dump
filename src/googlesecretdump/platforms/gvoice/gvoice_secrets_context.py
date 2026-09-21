from googlesecretdump.platforms.base.google_secrets_context import GoogleSecretsContext


class GvoiceSecretsContext(GoogleSecretsContext):
    gvoice_key: str = ""
    phone_number: str = ""

    def get_google_voice_cookies(self):
        """Returns the cookies for the Google Voice domain.

        Returns:
            list: A list of cookies for the Google Voice domain.
        """
        return [
            cookie
            for cookie in self.cookies
            if ".voice.google.com" == cookie.domain
        ]
