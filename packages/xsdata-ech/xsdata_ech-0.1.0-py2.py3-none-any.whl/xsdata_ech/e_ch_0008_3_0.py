from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0008/3"


@dataclass
class CountryShortType:
    class Meta:
        name = "countryShortType"

    country_name_short: Optional[str] = field(
        default=None,
        metadata={
            "name": "countryNameShort",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0008/3",
            "required": True,
            "max_length": 50,
        }
    )


@dataclass
class CountryType:
    class Meta:
        name = "countryType"

    country_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "countryId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0008/3",
            "min_inclusive": 1000,
            "max_inclusive": 9999,
        }
    )
    country_id_iso2: Optional[str] = field(
        default=None,
        metadata={
            "name": "countryIdISO2",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0008/3",
            "max_length": 2,
        }
    )
    country_name_short: Optional[str] = field(
        default=None,
        metadata={
            "name": "countryNameShort",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0008/3",
            "required": True,
            "max_length": 50,
        }
    )


@dataclass
class CountryRoot:
    class Meta:
        name = "countryRoot"
        namespace = "http://www.ech.ch/xmlns/eCH-0008/3"

    country: Optional[CountryType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
