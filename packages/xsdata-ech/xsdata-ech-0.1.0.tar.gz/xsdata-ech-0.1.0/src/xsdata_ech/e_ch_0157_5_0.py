from dataclasses import dataclass, field
from typing import List, Optional
from xsdata_ech.e_ch_0058_5_0 import HeaderType as HeaderType
from xsdata_ech.e_ch_0155_5_0 import (
    CandidateType as CandidateType,
    ContestType as ContestType,
    DomainOfInfluenceType as DomainOfInfluenceType,
    ElectionGroupDescriptionType as ElectionGroupDescriptionType,
    ElectionType as ElectionType,
    ExtensionType as ExtensionType,
    ListType as ListType,
    ListUnionType as ListUnionType,
)

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0157/5"


@dataclass
class EventInitialDelivery:
    class Meta:
        name = "eventInitialDelivery"

    contest: Optional[ContestType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
            "required": True,
        }
    )
    election_group: List["EventInitialDelivery.ElectionGroup"] = field(
        default_factory=list,
        metadata={
            "name": "electionGroup",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
            "min_occurs": 1,
        }
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
        }
    )

    @dataclass
    class ElectionGroup:
        election_group_identification: Optional[str] = field(
            default=None,
            metadata={
                "name": "electionGroupIdentification",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                "min_length": 1,
                "max_length": 50,
            }
        )
        election_group_description: Optional[
            ElectionGroupDescriptionType
        ] = field(
            default=None,
            metadata={
                "name": "electionGroupDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
            }
        )
        domain_of_influence: Optional[DomainOfInfluenceType] = field(
            default=None,
            metadata={
                "name": "domainOfInfluence",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                "required": True,
            }
        )
        election_group_position: Optional[int] = field(
            default=None,
            metadata={
                "name": "electionGroupPosition",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
            }
        )
        election_information: List[
            "EventInitialDelivery.ElectionGroup.ElectionInformation"
        ] = field(
            default_factory=list,
            metadata={
                "name": "electionInformation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                "min_occurs": 1,
            }
        )

        @dataclass
        class ElectionInformation:
            election: Optional[ElectionType] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                    "required": True,
                }
            )
            candidate: List[CandidateType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                }
            )
            list_value: List[ListType] = field(
                default_factory=list,
                metadata={
                    "name": "list",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                }
            )
            list_union: List[ListUnionType] = field(
                default_factory=list,
                metadata={
                    "name": "listUnion",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                }
            )
            extension: Optional[ExtensionType] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
                }
            )


@dataclass
class Delivery:
    class Meta:
        name = "delivery"
        namespace = "http://www.ech.ch/xmlns/eCH-0157/5"

    delivery_header: Optional[HeaderType] = field(
        default=None,
        metadata={
            "name": "deliveryHeader",
            "type": "Element",
            "required": True,
        }
    )
    initial_delivery: Optional[EventInitialDelivery] = field(
        default=None,
        metadata={
            "name": "initialDelivery",
            "type": "Element",
            "required": True,
        }
    )
    minor_version: Optional[int] = field(
        default=None,
        metadata={
            "name": "minorVersion",
            "type": "Attribute",
            "namespace": "http://www.ech.ch/xmlns/eCH-0157/5",
        }
    )
