from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0010/6"


@dataclass
class CountryType:
    class Meta:
        name = "countryType"

    country_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "countryId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "min_inclusive": 1000,
            "max_inclusive": 9999,
        }
    )
    country_id_iso2: Optional[str] = field(
        default=None,
        metadata={
            "name": "countryIdISO2",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "min_length": 2,
            "max_length": 2,
        }
    )
    country_name_short: Optional[str] = field(
        default=None,
        metadata={
            "name": "countryNameShort",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
            "max_length": 50,
        }
    )


class MrMrsType(Enum):
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"


@dataclass
class AddressInformationType:
    class Meta:
        name = "addressInformationType"

    address_line1: Optional[str] = field(
        default=None,
        metadata={
            "name": "addressLine1",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    address_line2: Optional[str] = field(
        default=None,
        metadata={
            "name": "addressLine2",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    street: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    house_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "houseNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 12,
        }
    )
    dwelling_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "dwellingNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 10,
        }
    )
    post_office_box_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "postOfficeBoxNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_inclusive": 99999999,
        }
    )
    post_office_box_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "postOfficeBoxText",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 15,
        }
    )
    locality: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 40,
        }
    )
    town: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
            "max_length": 40,
        }
    )
    swiss_zip_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "swissZipCode",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "min_inclusive": 1000,
            "max_inclusive": 9999,
        }
    )
    swiss_zip_code_add_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "swissZipCodeAddOn",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 2,
        }
    )
    swiss_zip_code_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "swissZipCodeId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
        }
    )
    foreign_zip_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "foreignZipCode",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 15,
        }
    )
    country: Optional[CountryType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )


@dataclass
class OrganisationMailAddressInfoType:
    class Meta:
        name = "organisationMailAddressInfoType"

    organisation_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "organisationName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
            "max_length": 60,
        }
    )
    organisation_name_add_on1: Optional[str] = field(
        default=None,
        metadata={
            "name": "organisationNameAddOn1",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    organisation_name_add_on2: Optional[str] = field(
        default=None,
        metadata={
            "name": "organisationNameAddOn2",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    mr_mrs: Optional[MrMrsType] = field(
        default=None,
        metadata={
            "name": "mrMrs",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 50,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "firstName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 30,
        }
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 30,
        }
    )


@dataclass
class PersonMailAddressInfoType:
    class Meta:
        name = "personMailAddressInfoType"

    mr_mrs: Optional[MrMrsType] = field(
        default=None,
        metadata={
            "name": "mrMrs",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 50,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "firstName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 30,
        }
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
            "max_length": 30,
        }
    )


@dataclass
class SwissAddressInformationType:
    class Meta:
        name = "swissAddressInformationType"

    address_line1: Optional[str] = field(
        default=None,
        metadata={
            "name": "addressLine1",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    address_line2: Optional[str] = field(
        default=None,
        metadata={
            "name": "addressLine2",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    street: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 60,
        }
    )
    house_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "houseNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 12,
        }
    )
    dwelling_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "dwellingNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 10,
        }
    )
    locality: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 40,
        }
    )
    town: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
            "max_length": 40,
        }
    )
    swiss_zip_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "swissZipCode",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
            "min_inclusive": 1000,
            "max_inclusive": 9999,
        }
    )
    swiss_zip_code_add_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "swissZipCodeAddOn",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "max_length": 2,
        }
    )
    swiss_zip_code_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "swissZipCodeId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
        }
    )
    country: Optional[CountryType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )


@dataclass
class MailAddressType:
    class Meta:
        name = "mailAddressType"

    organisation: Optional[OrganisationMailAddressInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
        }
    )
    person: Optional[PersonMailAddressInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
        }
    )
    address_information: Optional[AddressInformationType] = field(
        default=None,
        metadata={
            "name": "addressInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )


@dataclass
class OrganisationMailAddressType:
    class Meta:
        name = "organisationMailAddressType"

    organisation: Optional[OrganisationMailAddressInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )
    address_information: Optional[AddressInformationType] = field(
        default=None,
        metadata={
            "name": "addressInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )


@dataclass
class PersonMailAddressType:
    class Meta:
        name = "personMailAddressType"

    person: Optional[PersonMailAddressInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )
    address_information: Optional[AddressInformationType] = field(
        default=None,
        metadata={
            "name": "addressInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0010/6",
            "required": True,
        }
    )


@dataclass
class MailAddress(MailAddressType):
    class Meta:
        name = "mailAddress"
        namespace = "http://www.ech.ch/xmlns/eCH-0010/6"


@dataclass
class OrganisationMailAdress(OrganisationMailAddressType):
    class Meta:
        name = "organisationMailAdress"
        namespace = "http://www.ech.ch/xmlns/eCH-0010/6"


@dataclass
class PersonMailAddress(PersonMailAddressType):
    class Meta:
        name = "personMailAddress"
        namespace = "http://www.ech.ch/xmlns/eCH-0010/6"
