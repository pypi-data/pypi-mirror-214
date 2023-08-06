from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from xsdata_ech.e_ch_0044_4_1 import SexType
from xsdata_ech.e_ch_0058_5_0 import HeaderType
from xsdata_ech.e_ch_0155_5_0 import (
    DomainOfInfluenceType as DomainOfInfluenceType,
    DomainOfInfluenceTypeType as DomainOfInfluenceTypeType,
    ExtensionType as ExtensionType,
    VoterTypeType as VoterTypeType,
)

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0252/1"


class DecisiveMajorityType(Enum):
    VALUE_1 = 1  # Mehrheit der Stimmen
    VALUE_2 = 2  # Mehrheit der Gemeinden
    VALUE_3 = 3  # Alle Gemeinden / einstimmig
    VALUE_4 = 4  # Mehrheit der Stimmen und der Gemeinden
    VALUE_5 = 5  # Volks- und Ständemehr


@dataclass
class NamedElementType:
    class Meta:
        name = "namedElementType"

    element_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "elementName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    count_of: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOf",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    percent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": Decimal("0.00"),
            "max_inclusive": Decimal("100.00"),
            "total_digits": 5,
            "fraction_digits": 2,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_length": 1,
            "max_length": 500,
        }
    )


@dataclass
class NamedIdType:
    class Meta:
        name = "namedIdType"

    id_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "idName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_length": 1,
            "max_length": 20,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )


class VoteSubTypeType(Enum):
    VALUE_1 = 1  # Vorlage / Hauptvorlage (A)
    VALUE_2 = 2  # Variante / Gegenvorschlag (B)
    VALUE_3 = 3  # Stichfrage (A oder B)
    VALUE_4 = 4  # weitere Variante / weiterer Gegenvorschlag (C)
    VALUE_5 = 5  # Stichfrage (A oder C)
    VALUE_6 = 6  # Stichfrage (B oder C)


@dataclass
class VoteTitleInformationType:
    class Meta:
        name = "voteTitleInformationType"

    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "length": 2,
        }
    )
    vote_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "voteTitle",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_length": 1,
            "max_length": 700,
        }
    )
    vote_title_short: Optional[str] = field(
        default=None,
        metadata={
            "name": "voteTitleShort",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_length": 1,
            "max_length": 300,
        }
    )


@dataclass
class VotingCardInformationType:
    class Meta:
        name = "votingCardInformationType"

    count_of_voting_cards_received_in_ballotbox: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedInBallotbox",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    count_of_voting_cards_received_prematurely_in_ballotbox: Optional[
        int
    ] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedPrematurelyInBallotbox",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    count_of_voting_cards_received_by_mail: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedByMail",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    count_of_voting_cards_received_by_evoting: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedByEvoting",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )


@dataclass
class CountOfVotersInformationType:
    class Meta:
        name = "countOfVotersInformationType"

    count_of_voters_total: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotersTotal",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    subtotal_info: List["CountOfVotersInformationType.SubtotalInfo"] = field(
        default_factory=list,
        metadata={
            "name": "subtotalInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )

    @dataclass
    class SubtotalInfo:
        count_of_voters: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfVoters",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            }
        )
        voter_type: Optional[VoterTypeType] = field(
            default=None,
            metadata={
                "name": "voterType",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            }
        )
        sex: Optional[SexType] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            }
        )


@dataclass
class CountingCircleType:
    class Meta:
        name = "countingCircleType"

    counting_circle_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "countingCircleId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_length": 1,
            "max_length": 50,
        }
    )
    counting_circle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "countingCircleName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_length": 1,
            "max_length": 100,
        }
    )
    domain_of_influence_type: Optional[DomainOfInfluenceTypeType] = field(
        default=None,
        metadata={
            "name": "domainOfInfluenceType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )


@dataclass
class VoteType:
    class Meta:
        name = "voteType"

    vote_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "voteIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    main_vote_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainVoteIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_length": 1,
            "max_length": 50,
        }
    )
    other_identification: List[NamedIdType] = field(
        default_factory=list,
        metadata={
            "name": "otherIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )
    domain_of_influence: Optional[DomainOfInfluenceType] = field(
        default=None,
        metadata={
            "name": "domainOfInfluence",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    superior_authority: Optional[DomainOfInfluenceType] = field(
        default=None,
        metadata={
            "name": "superiorAuthority",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )
    polling_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "pollingDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    vote_title_information: List[VoteTitleInformationType] = field(
        default_factory=list,
        metadata={
            "name": "voteTitleInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_occurs": 1,
        }
    )
    decisive_majority: Optional[DecisiveMajorityType] = field(
        default=None,
        metadata={
            "name": "decisiveMajority",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    vote_sub_type: Optional[VoteSubTypeType] = field(
        default=None,
        metadata={
            "name": "voteSubType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    sequence: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 1,
            "max_inclusive": 999,
        }
    )
    grouping: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_length": 1,
            "max_length": 50,
        }
    )


@dataclass
class ResultDataType:
    class Meta:
        name = "resultDataType"

    count_of_voters_information: Optional[
        CountOfVotersInformationType
    ] = field(
        default=None,
        metadata={
            "name": "countOfVotersInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    voting_card_information_type: Optional[VotingCardInformationType] = field(
        default=None,
        metadata={
            "name": "votingCardInformationType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )
    fully_counted_true: Optional[bool] = field(
        default=None,
        metadata={
            "name": "fullyCountedTrue",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    released_time_stamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "releasedTimeStamp",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )
    lockout_time_stamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lockoutTimeStamp",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )
    voter_turnout: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "voterTurnout",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": Decimal("0.00"),
            "max_inclusive": Decimal("100.00"),
            "total_digits": 5,
            "fraction_digits": 2,
        }
    )
    received_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    received_invalid_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedInvalidVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    received_blank_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedBlankVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    received_valid_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedValidVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    count_of_yes_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfYesVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    count_of_no_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfNoVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    count_of_votes_without_answer: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotesWithoutAnswer",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        }
    )
    named_element: List[NamedElementType] = field(
        default_factory=list,
        metadata={
            "name": "namedElement",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )


@dataclass
class CountingCircleInfoType:
    class Meta:
        name = "countingCircleInfoType"

    counting_circle: Optional[CountingCircleType] = field(
        default=None,
        metadata={
            "name": "countingCircle",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    result_data: Optional[ResultDataType] = field(
        default=None,
        metadata={
            "name": "resultData",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )


@dataclass
class VoteInfoType:
    class Meta:
        name = "voteInfoType"

    vote: Optional[VoteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    counting_circle_info: List[CountingCircleInfoType] = field(
        default_factory=list,
        metadata={
            "name": "countingCircleInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_occurs": 1,
        }
    )


@dataclass
class EventVoteBaseDeliveryType:
    class Meta:
        name = "eventVoteBaseDeliveryType"

    canton_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "cantonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 26,
        }
    )
    polling_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "pollingDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
        }
    )
    vote_info: List[VoteInfoType] = field(
        default_factory=list,
        metadata={
            "name": "voteInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "min_occurs": 1,
        }
    )
    number_of_entries: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfEntries",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 999,
        }
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )


@dataclass
class Delivery:
    class Meta:
        name = "delivery"
        namespace = "http://www.ech.ch/xmlns/eCH-0252/1"

    delivery_header: Optional[HeaderType] = field(
        default=None,
        metadata={
            "name": "deliveryHeader",
            "type": "Element",
            "required": True,
        }
    )
    vote_base_delivery: Optional[EventVoteBaseDeliveryType] = field(
        default=None,
        metadata={
            "name": "voteBaseDelivery",
            "type": "Element",
            "required": True,
        }
    )
    minor_version: Optional[int] = field(
        default=None,
        metadata={
            "name": "minorVersion",
            "type": "Attribute",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/1",
        }
    )
