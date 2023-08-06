from dataclasses import dataclass, field
from typing import List, Optional
from xsdata_ech.e_ch_0058_5_0 import HeaderType as HeaderType
from xsdata_ech.e_ch_0155_5_0 import (
    ContestType as ContestType,
    ElectronicBallotType as ElectronicBallotType,
    ExtensionType as ExtensionType,
    VoteType as VoteType,
)

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0159/5"


@dataclass
class EventInitialDelivery:
    class Meta:
        name = "eventInitialDelivery"

    contest: Optional[ContestType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0159/5",
            "required": True,
        }
    )
    vote_information: List["EventInitialDelivery.VoteInformation"] = field(
        default_factory=list,
        metadata={
            "name": "voteInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0159/5",
            "min_occurs": 1,
        }
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0159/5",
        }
    )

    @dataclass
    class VoteInformation:
        vote: Optional[VoteType] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0159/5",
                "required": True,
            }
        )
        electronic_ballot: List[ElectronicBallotType] = field(
            default_factory=list,
            metadata={
                "name": "electronicBallot",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0159/5",
                "min_occurs": 1,
            }
        )


@dataclass
class Delivery:
    class Meta:
        name = "delivery"
        namespace = "http://www.ech.ch/xmlns/eCH-0159/5"

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
            "namespace": "http://www.ech.ch/xmlns/eCH-0159/5",
        }
    )
