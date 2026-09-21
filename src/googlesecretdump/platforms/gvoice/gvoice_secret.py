from pydantic import Field

from googlesecretdump.platforms.base.secret import Secret


class GvoiceSecret(Secret):
    gvoice_key: str = Field(default="")
    phone_number: str = Field(default="")
