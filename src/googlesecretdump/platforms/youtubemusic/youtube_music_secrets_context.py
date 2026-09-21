from googlesecretdump.platforms.base.google_secrets_context import GoogleSecretsContext


class YoutubeMusicSecretsContext(GoogleSecretsContext):

    def get_youtube_music_cookies(self):
        """Returns the cookies for the YouTube Music domain.

        Returns:
            list: A list of cookies for the YouTube Music domain.
        """
        return [
            cookie
            for cookie in self.cookies
            if ".youtube.com" == cookie.domain
        ]
