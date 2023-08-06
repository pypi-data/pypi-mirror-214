from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0006/2"


class InhabitantControlType(Enum):
    VALUE_0102 = "0102"
    VALUE_0201 = "0201"
    VALUE_0202 = "0202"
    VALUE_0301 = "0301"
    VALUE_0302 = "0302"
    VALUE_0401 = "0401"
    VALUE_0402 = "0402"
    VALUE_0503 = "0503"
    VALUE_0601 = "0601"
    VALUE_0602 = "0602"
    VALUE_0701 = "0701"
    VALUE_0702 = "0702"
    VALUE_0804 = "0804"
    VALUE_0905 = "0905"
    VALUE_1006 = "1006"
    VALUE_1108 = "1108"
    VALUE_1208 = "1208"
    VALUE_1300 = "1300"


class ResidencePermitBorderType(Enum):
    VALUE_01 = "01"
    VALUE_02 = "02"


class ResidencePermitCategoryType(Enum):
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"


class ResidencePermitDetailedType(Enum):
    VALUE_0102 = "0102"
    VALUE_0201 = "0201"
    VALUE_0202 = "0202"
    VALUE_0301 = "0301"
    VALUE_0302 = "0302"
    VALUE_0401 = "0401"
    VALUE_0402 = "0402"
    VALUE_0503 = "0503"
    VALUE_0601 = "0601"
    VALUE_0602 = "0602"
    VALUE_060101 = "060101"
    VALUE_060201 = "060201"
    VALUE_060102 = "060102"
    VALUE_060202 = "060202"
    VALUE_0701 = "0701"
    VALUE_0702 = "0702"
    VALUE_070101 = "070101"
    VALUE_070201 = "070201"
    VALUE_070102 = "070102"
    VALUE_070202 = "070202"
    VALUE_070103 = "070103"
    VALUE_070104 = "070104"
    VALUE_070204 = "070204"
    VALUE_070105 = "070105"
    VALUE_070205 = "070205"
    VALUE_070206 = "070206"
    VALUE_070907 = "070907"
    VALUE_0804 = "0804"
    VALUE_0905 = "0905"
    VALUE_1006 = "1006"
    VALUE_100601 = "100601"
    VALUE_100602 = "100602"
    VALUE_100603 = "100603"
    VALUE_1107 = "1107"
    VALUE_1208 = "1208"
    VALUE_1300 = "1300"


class ResidencePermitRulingType(Enum):
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"


class ResidencePermitShortType(Enum):
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"


class ResidencePermitToBeRegisteredType(Enum):
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"


class ResidencePermitType(Enum):
    VALUE_01 = "01"
    VALUE_0102 = "0102"
    VALUE_02 = "02"
    VALUE_0201 = "0201"
    VALUE_0202 = "0202"
    VALUE_03 = "03"
    VALUE_0301 = "0301"
    VALUE_0302 = "0302"
    VALUE_04 = "04"
    VALUE_0401 = "0401"
    VALUE_0402 = "0402"
    VALUE_05 = "05"
    VALUE_0503 = "0503"
    VALUE_06 = "06"
    VALUE_0601 = "0601"
    VALUE_0602 = "0602"
    VALUE_060101 = "060101"
    VALUE_060201 = "060201"
    VALUE_060102 = "060102"
    VALUE_060202 = "060202"
    VALUE_07 = "07"
    VALUE_0701 = "0701"
    VALUE_0702 = "0702"
    VALUE_070101 = "070101"
    VALUE_070201 = "070201"
    VALUE_070102 = "070102"
    VALUE_070202 = "070202"
    VALUE_070103 = "070103"
    VALUE_070104 = "070104"
    VALUE_070204 = "070204"
    VALUE_070105 = "070105"
    VALUE_070205 = "070205"
    VALUE_070206 = "070206"
    VALUE_070907 = "070907"
    VALUE_08 = "08"
    VALUE_0804 = "0804"
    VALUE_09 = "09"
    VALUE_0905 = "0905"
    VALUE_10 = "10"
    VALUE_1006 = "1006"
    VALUE_100601 = "100601"
    VALUE_100602 = "100602"
    VALUE_100603 = "100603"
    VALUE_11 = "11"
    VALUE_1107 = "1107"
    VALUE_12 = "12"
    VALUE_1208 = "1208"
    VALUE_1300 = "1300"


@dataclass
class PermitRoot:
    class Meta:
        name = "permitRoot"
        namespace = "http://www.ech.ch/xmlns/eCH-0006/2"

    residence_permit_category: Optional[ResidencePermitCategoryType] = field(
        default=None,
        metadata={
            "name": "residencePermitCategory",
            "type": "Element",
        }
    )
    residence_permit_ruling: Optional[ResidencePermitRulingType] = field(
        default=None,
        metadata={
            "name": "residencePermitRuling",
            "type": "Element",
        }
    )
    residence_permit_border: Optional[ResidencePermitBorderType] = field(
        default=None,
        metadata={
            "name": "residencePermitBorder",
            "type": "Element",
        }
    )
    residence_permit_short_type: Optional[ResidencePermitShortType] = field(
        default=None,
        metadata={
            "name": "residencePermitShortType",
            "type": "Element",
        }
    )
    residence_permit: Optional[ResidencePermitType] = field(
        default=None,
        metadata={
            "name": "residencePermit",
            "type": "Element",
        }
    )
    inhabitant_control: Optional[InhabitantControlType] = field(
        default=None,
        metadata={
            "name": "inhabitantControl",
            "type": "Element",
        }
    )
    residence_permit_detailed_type: Optional[
        ResidencePermitDetailedType
    ] = field(
        default=None,
        metadata={
            "name": "residencePermitDetailedType",
            "type": "Element",
        }
    )
    residence_permit_to_be_registered_type: Optional[
        ResidencePermitToBeRegisteredType
    ] = field(
        default=None,
        metadata={
            "name": "residencePermitToBeRegisteredType",
            "type": "Element",
        }
    )
