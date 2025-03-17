from typing import Optional


from src.models.base_struc import BaseStruct
from src.models.contact_object import ContactObject
from src.models.license_object import LicenseObject


class InfoObject(BaseStruct):
    """
    Provides metadata about the API. The metadata MAY be used by tooling as required.
    """

    title: str
    version: str
    summary: Optional[str] = None
    description: Optional[str] = None
    termsOfService: Optional[str] = None
    contact: Optional[ContactObject] = None
    license: Optional[LicenseObject] = None
