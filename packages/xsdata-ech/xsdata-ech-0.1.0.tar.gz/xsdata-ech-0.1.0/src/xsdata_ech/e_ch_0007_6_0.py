from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0007/6"


class CantonAbbreviationType(Enum):
    ZH = "ZH"
    BE = "BE"
    LU = "LU"
    UR = "UR"
    SZ = "SZ"
    OW = "OW"
    NW = "NW"
    GL = "GL"
    ZG = "ZG"
    FR = "FR"
    SO = "SO"
    BS = "BS"
    BL = "BL"
    SH = "SH"
    AR = "AR"
    AI = "AI"
    SG = "SG"
    GR = "GR"
    AG = "AG"
    TG = "TG"
    TI = "TI"
    VD = "VD"
    VS = "VS"
    NE = "NE"
    GE = "GE"
    JU = "JU"


class CantonFlAbbreviationType(Enum):
    ZH = "ZH"
    BE = "BE"
    LU = "LU"
    UR = "UR"
    SZ = "SZ"
    OW = "OW"
    NW = "NW"
    GL = "GL"
    ZG = "ZG"
    FR = "FR"
    SO = "SO"
    BS = "BS"
    BL = "BL"
    SH = "SH"
    AR = "AR"
    AI = "AI"
    SG = "SG"
    GR = "GR"
    AG = "AG"
    TG = "TG"
    TI = "TI"
    VD = "VD"
    VS = "VS"
    NE = "NE"
    GE = "GE"
    JU = "JU"
    FL = "FL"


@dataclass
class SwissAndFlMunicipalityType:
    class Meta:
        name = "swissAndFlMunicipalityType"

    municipality_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "municipalityId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 9999,
            "total_digits": 4,
        }
    )
    municipality_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "municipalityName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "required": True,
            "max_length": 40,
        }
    )
    canton_fl_abbreviation: Optional[CantonFlAbbreviationType] = field(
        default=None,
        metadata={
            "name": "cantonFlAbbreviation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "required": True,
        }
    )
    history_municipality_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "historyMunicipalityId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "min_inclusive": 10001,
            "max_inclusive": 99999,
        }
    )


@dataclass
class SwissMunicipalityType:
    class Meta:
        name = "swissMunicipalityType"

    municipality_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "municipalityId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "min_inclusive": 1,
            "max_inclusive": 9999,
            "total_digits": 4,
        }
    )
    municipality_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "municipalityName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "required": True,
            "max_length": 40,
        }
    )
    canton_abbreviation: Optional[CantonAbbreviationType] = field(
        default=None,
        metadata={
            "name": "cantonAbbreviation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
        }
    )
    history_municipality_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "historyMunicipalityId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0007/6",
            "min_inclusive": 10001,
            "max_inclusive": 99999,
        }
    )


@dataclass
class MunicipalityRoot:
    class Meta:
        name = "municipalityRoot"
        namespace = "http://www.ech.ch/xmlns/eCH-0007/6"

    swiss_municipality: Optional[SwissMunicipalityType] = field(
        default=None,
        metadata={
            "name": "swissMunicipality",
            "type": "Element",
        }
    )
    swiss_and_fl_municipality: Optional[SwissAndFlMunicipalityType] = field(
        default=None,
        metadata={
            "name": "swissAndFlMunicipality",
            "type": "Element",
        }
    )
