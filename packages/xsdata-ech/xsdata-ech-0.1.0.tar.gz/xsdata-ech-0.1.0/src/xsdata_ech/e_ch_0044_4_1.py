from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlPeriod

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0044/4"


@dataclass
class DatePartiallyKnownType:
    class Meta:
        name = "datePartiallyKnownType"

    year_month_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "yearMonthDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    year_month: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "name": "yearMonth",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    year: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )


@dataclass
class NamedPersonIdType:
    class Meta:
        name = "namedPersonIdType"

    person_id_category: Optional[str] = field(
        default=None,
        metadata={
            "name": "personIdCategory",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
            "min_length": 1,
            "max_length": 20,
        }
    )
    person_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "personId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )


class SexType(Enum):
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"


@dataclass
class PersonIdentificationKeyOnlyType:
    class Meta:
        name = "personIdentificationKeyOnlyType"

    vn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "min_inclusive": 7560000000001,
            "max_inclusive": 7569999999999,
        }
    )
    local_person_id: Optional[NamedPersonIdType] = field(
        default=None,
        metadata={
            "name": "localPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
        }
    )
    other_person_id: List[NamedPersonIdType] = field(
        default_factory=list,
        metadata={
            "name": "otherPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    eu_person_id: List[NamedPersonIdType] = field(
        default_factory=list,
        metadata={
            "name": "euPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )


@dataclass
class PersonIdentificationLightType:
    class Meta:
        name = "personIdentificationLightType"

    vn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "min_inclusive": 7560000000001,
            "max_inclusive": 7569999999999,
        }
    )
    local_person_id: Optional[NamedPersonIdType] = field(
        default=None,
        metadata={
            "name": "localPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    other_person_id: List[NamedPersonIdType] = field(
        default_factory=list,
        metadata={
            "name": "otherPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    official_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "officialName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "firstName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    original_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "originalName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "min_length": 1,
            "max_length": 100,
        }
    )
    sex: Optional[SexType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    date_of_birth: Optional[DatePartiallyKnownType] = field(
        default=None,
        metadata={
            "name": "dateOfBirth",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )


@dataclass
class PersonIdentificationType:
    class Meta:
        name = "personIdentificationType"

    vn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "min_inclusive": 7560000000001,
            "max_inclusive": 7569999999999,
        }
    )
    local_person_id: Optional[NamedPersonIdType] = field(
        default=None,
        metadata={
            "name": "localPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
        }
    )
    other_person_id: List[NamedPersonIdType] = field(
        default_factory=list,
        metadata={
            "name": "otherPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    eu_person_id: List[NamedPersonIdType] = field(
        default_factory=list,
        metadata={
            "name": "euPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
        }
    )
    official_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "officialName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "firstName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    original_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "originalName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "min_length": 1,
            "max_length": 100,
        }
    )
    sex: Optional[SexType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
        }
    )
    date_of_birth: Optional[DatePartiallyKnownType] = field(
        default=None,
        metadata={
            "name": "dateOfBirth",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0044/4",
            "required": True,
        }
    )


@dataclass
class PersonIdentificationRoot:
    class Meta:
        name = "personIdentificationRoot"
        namespace = "http://www.ech.ch/xmlns/eCH-0044/4"

    person_identification: Optional[PersonIdentificationType] = field(
        default=None,
        metadata={
            "name": "personIdentification",
            "type": "Element",
            "required": True,
        }
    )
