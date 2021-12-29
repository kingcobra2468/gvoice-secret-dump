from secrets.gvoice_secret import GVoiceSecret
from os import getcwd, environ


def get_secrets(email, password):
    """Fetches the secrets for Google Voice.

    Args:
        email (str): Google email.
        password (str): Google password.
    """
    g_secrets = GVoiceSecret(email, password)

    g_secrets.login()
    g_secrets.dump_secrets(True, getcwd())


if __name__ == "__main__":
    email = environ.get('GVOICE_EMAIL', None)
    password = environ.get('GVOICE_PASSWORD', None)

    # check if the environment variables are set
    if None in (email, password):
        raise ValueError(
            'Both GVOICE_EMAIL and GVOICE_PASSWORD environment variables need to be set.')

    get_secrets(email, password)
