from os import environ
import argparse

from googlesecretdump.platforms.gvoice.gvoice_secrets_generator import (
    GvoiceSecretsGenerator,
)
from googlesecretdump.platforms.youtubemusic.youtube_music_secrets_generator import (
    YoutubeMusicSecretsGenerator,
)
from googlesecretdump.platforms.gvoice.gvoice_secrets_context import (
    GvoiceSecretsContext,
)
from googlesecretdump.platforms.youtubemusic.youtube_music_secrets_context import (
    YoutubeMusicSecretsContext,
)


def _get_credentials():
    """Returns credentials from environment and validates they are present."""
    email = environ.get("GVOICE_EMAIL", None)
    password = environ.get("GVOICE_PASSWORD", None)

    if None in (email, password):
        raise ValueError(
            "Both GVOICE_EMAIL and GVOICE_PASSWORD environment variables need to be set."
        )

    return email, password


def handle_login(args):
    """Handles the login command.

    Args:
        args (argparse.Namespace): Parsed command line arguments.
    """
    email, password = _get_credentials()

    if args.service == "ytmusic":
        generator = YoutubeMusicSecretsGenerator(email, password, args.chrome_version)
    elif args.service == "gvoice":
        generator = GvoiceSecretsGenerator(email, password, args.chrome_version)

    generator.login()
    secrets = generator.get_secrets()
    secrets.save_secrets_to_json(f"{args.service}_secrets.json")
    secrets.save_cookies_to_cookies_txt(f"{args.service}_cookies.txt")


def handle_refresh(args):
    """Handles the refresh command.

    Args:
        args (argparse.Namespace): Parsed command line arguments.
    """
    email, password = _get_credentials()

    if args.service == "ytmusic":
        generator = YoutubeMusicSecretsGenerator(email, password, args.chrome_version)
        secrets_context = YoutubeMusicSecretsContext().read_secrets_from_json(
            f"{args.service}_secrets.json"
        )
        generator.load_cookies(secrets_context.get_cookies())
    elif args.service == "gvoice":
        generator = GvoiceSecretsGenerator(email, password, args.chrome_version)
        secrets_context = GvoiceSecretsContext().read_secrets_from_json(
            f"{args.service}_secrets.json"
        )

    generator.load_cookies(secrets_context.get_cookies())
    generator.refresh()

    secrets_context.save_secrets_to_json(f"{args.service}_secrets.json")
    secrets_context.save_cookies_to_cookies_txt(f"{args.service}_cookies.txt")


if __name__ == "__main__":
    _get_credentials()

    parser = argparse.ArgumentParser(description="Google Voice Secret Dumper")
    parser.add_argument(
        "--chrome-version",
        type=int,
        help="Chrome version to use for undetected-chromedriver",
    )

    service_subparsers = parser.add_subparsers(
        dest="service", required=True, help="Target service"
    )

    for service in ("gvoice", "ytmusic"):
        service_parser = service_subparsers.add_parser(
            service, help=f"Commands for {service}"
        )
        command_subparsers = service_parser.add_subparsers(
            dest="command", required=True, help="Available commands"
        )

        parser_login = command_subparsers.add_parser(
            "login", help=f"Login to {service} and dump secrets"
        )
        parser_login.set_defaults(func=handle_login, service=service)

        parser_refresh = command_subparsers.add_parser(
            "refresh", help=f"Refresh {service} secrets"
        )
        parser_refresh.set_defaults(func=handle_refresh, service=service)

    args = parser.parse_args()
    args.func(args)
