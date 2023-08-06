from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime
from xsdata_ech.e_ch_0006_2_0 import ResidencePermitType as ResidencePermitType
from xsdata_ech.e_ch_0008_3_0 import CountryType as CountryType
from xsdata_ech.e_ch_0010_6_0 import (
    AddressInformationType as AddressInformationType,
    MrMrsType as MrMrsType,
    PersonMailAddressType as PersonMailAddressType,
    SwissAddressInformationType as SwissAddressInformationType,
)
from xsdata_ech.e_ch_0044_4_1 import (
    DatePartiallyKnownType as DatePartiallyKnownType,
    NamedPersonIdType as NamedPersonIdType,
    SexType as SexType,
)

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0155/5"


@dataclass
class AnswerOptionIdentificationType:
    class Meta:
        name = "answerOptionIdentificationType"

    answer_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "answerIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    answer_sequence_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "answerSequenceNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    answer_text_information: List[
        "AnswerOptionIdentificationType.AnswerTextInformation"
    ] = field(
        default_factory=list,
        metadata={
            "name": "answerTextInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class AnswerTextInformation:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        answer_text_short: Optional[str] = field(
            default=None,
            metadata={
                "name": "answerTextShort",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 10,
            }
        )
        answer_text: Optional[str] = field(
            default=None,
            metadata={
                "name": "answerText",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 30,
            }
        )


class AnswerTypeType(Enum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7


@dataclass
class CandidateGroupDescriptionInformationType:
    class Meta:
        name = "candidateGroupDescriptionInformationType"

    candidate_group_description_info: List[
        "CandidateGroupDescriptionInformationType."
        "CandidateGroupDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "candidateGroupDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class CandidateGroupDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        candidate_group_description_short: Optional[str] = field(
            default=None,
            metadata={
                "name": "candidateGroupDescriptionShort",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 20,
            }
        )
        candidate_group_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "candidateGroupDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 100,
            }
        )


@dataclass
class CandidateTextInformationType:
    class Meta:
        name = "candidateTextInformationType"

    candidate_text_info: List[
        "CandidateTextInformationType.CandidateTextInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "candidateTextInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class CandidateTextInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        candidate_text: Optional[str] = field(
            default=None,
            metadata={
                "name": "candidateText",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 500,
            }
        )


@dataclass
class ContestDescriptionInformationType:
    class Meta:
        name = "contestDescriptionInformationType"

    contest_description_info: List[
        "ContestDescriptionInformationType.ContestDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "contestDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ContestDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        contest_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "contestDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 100,
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
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 50,
        }
    )
    counting_circle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "countingCircleName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 100,
        }
    )


class DomainOfInfluenceTypeType(Enum):
    CH = "CH"
    CT = "CT"
    BZ = "BZ"
    MU = "MU"
    SC = "SC"
    KI = "KI"
    OG = "OG"
    KO = "KO"
    SK = "SK"
    AN = "AN"


@dataclass
class EVotingPeriodType:
    class Meta:
        name = "eVotingPeriodType"

    e_voting_period_from: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "eVotingPeriodFrom",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    e_voting_period_till: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "eVotingPeriodTill",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )


@dataclass
class ElectionDescriptionInformationType:
    class Meta:
        name = "electionDescriptionInformationType"

    election_description_info: List[
        "ElectionDescriptionInformationType.ElectionDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "electionDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ElectionDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        election_description_short: Optional[str] = field(
            default=None,
            metadata={
                "name": "electionDescriptionShort",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 100,
            }
        )
        election_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "electionDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 255,
            }
        )


class ElectionRelationType(Enum):
    VALUE_1 = 1
    VALUE_2 = 2


@dataclass
class ElectronicBallotDescriptionInformationType:
    class Meta:
        name = "electronicBallotDescriptionInformationType"

    electronic_ballot_description_info: List[
        "ElectronicBallotDescriptionInformationType."
        "ElectronicBallotDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "electronicBallotDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ElectronicBallotDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        electronic_ballot_description_long: Optional[str] = field(
            default=None,
            metadata={
                "name": "electronicBallotDescriptionLong",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 255,
            }
        )
        electronic_ballot_description_short: Optional[str] = field(
            default=None,
            metadata={
                "name": "electronicBallotDescriptionShort",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 100,
            }
        )


@dataclass
class ElectronicBallotQuestionType:
    class Meta:
        name = "electronicBallotQuestionType"

    electronic_ballot_question_info: List[
        "ElectronicBallotQuestionType.ElectronicBallotQuestionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "electronicBallotQuestionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ElectronicBallotQuestionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        electronic_ballot_question_title: Optional[str] = field(
            default=None,
            metadata={
                "name": "electronicBallotQuestionTitle",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 100,
            }
        )
        electronic_ballot_question: Optional[str] = field(
            default=None,
            metadata={
                "name": "electronicBallotQuestion",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 700,
            }
        )


class EligibilityType(Enum):
    IMPLICITLY_ELIGIBLE = "implicitly eligible"
    EXPLICITLY_REPORTED = "explicitly reported"


@dataclass
class ExtensionType:
    class Meta:
        name = "extensionType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        }
    )


@dataclass
class ListDescriptionInformationType:
    class Meta:
        name = "listDescriptionInformationType"

    list_description_info: List[
        "ListDescriptionInformationType.ListDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "listDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ListDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        list_description_short: Optional[str] = field(
            default=None,
            metadata={
                "name": "listDescriptionShort",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 20,
            }
        )
        list_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "listDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 100,
            }
        )


class ListRelationType(Enum):
    VALUE_1 = 1
    VALUE_2 = 2


@dataclass
class ListUnionBallotTextType:
    class Meta:
        name = "listUnionBallotTextType"

    list_union_ballot_text_info: List[
        "ListUnionBallotTextType.ListUnionBallotTextInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "listUnionBallotTextInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ListUnionBallotTextInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        list_union_ballot_text: Optional[str] = field(
            default=None,
            metadata={
                "name": "listUnionBallotText",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 500,
            }
        )


@dataclass
class ListUnionDescriptionType:
    class Meta:
        name = "listUnionDescriptionType"

    list_union_description_info: List[
        "ListUnionDescriptionType.ListUnionDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "listUnionDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class ListUnionDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        list_union_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "listUnionDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 255,
            }
        )


@dataclass
class OccupationalTitleInformationType:
    class Meta:
        name = "occupationalTitleInformationType"

    occupational_title_info: List[
        "OccupationalTitleInformationType.OccupationalTitleInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "occupationalTitleInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class OccupationalTitleInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        occupational_title: Optional[str] = field(
            default=None,
            metadata={
                "name": "occupationalTitle",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 250,
            }
        )


@dataclass
class PartyAffiliationInformationType:
    class Meta:
        name = "partyAffiliationInformationType"

    party_affiliation_info: List[
        "PartyAffiliationInformationType.PartyAffiliationInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "partyAffiliationInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class PartyAffiliationInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        party_affiliation_short: Optional[str] = field(
            default=None,
            metadata={
                "name": "partyAffiliationShort",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 12,
            }
        )
        party_affiliation_long: Optional[str] = field(
            default=None,
            metadata={
                "name": "partyAffiliationLong",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 100,
            }
        )


@dataclass
class RoleInformationType:
    class Meta:
        name = "roleInformationType"

    role_info: List["RoleInformationType.RoleInfo"] = field(
        default_factory=list,
        metadata={
            "name": "roleInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class RoleInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        role: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 100,
            }
        )


@dataclass
class TieBreakQuestionType:
    class Meta:
        name = "tieBreakQuestionType"

    tie_break_question_info: List[
        "TieBreakQuestionType.TieBreakQuestionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "tieBreakQuestionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class TieBreakQuestionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        tie_break_question_title: Optional[str] = field(
            default=None,
            metadata={
                "name": "tieBreakQuestionTitle",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 100,
            }
        )
        tie_break_question: Optional[str] = field(
            default=None,
            metadata={
                "name": "tieBreakQuestion",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 700,
            }
        )
        tie_break_question2: Optional[str] = field(
            default=None,
            metadata={
                "name": "tieBreakQuestion2",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 700,
            }
        )


class TypeOfElectionType(Enum):
    VALUE_1 = 1
    VALUE_2 = 2


@dataclass
class VoteDescriptionInformationType:
    class Meta:
        name = "voteDescriptionInformationType"

    vote_description_info: List[
        "VoteDescriptionInformationType.VoteDescriptionInfo"
    ] = field(
        default_factory=list,
        metadata={
            "name": "voteDescriptionInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
        }
    )

    @dataclass
    class VoteDescriptionInfo:
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "length": 2,
            }
        )
        vote_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "voteDescription",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 100,
            }
        )


class VoterTypeType(Enum):
    VALUE_1 = 1  # Schweizer
    VALUE_2 = 2  # Auslandschweizer
    VALUE_3 = 3  # Ausländer


class VotingChannelType(Enum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4


@dataclass
class AnswerInformationType:
    class Meta:
        name = "answerInformationType"

    answer_type: Optional[AnswerTypeType] = field(
        default=None,
        metadata={
            "name": "answerType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    answer_option_identification: List[AnswerOptionIdentificationType] = field(
        default_factory=list,
        metadata={
            "name": "answerOptionIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class CandidateGroupType:
    class Meta:
        name = "candidateGroupType"

    candidate_group_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "candidateGroupIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    sort_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "sortID",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    candidate_group_description: Optional[
        CandidateGroupDescriptionInformationType
    ] = field(
        default=None,
        metadata={
            "name": "candidateGroupDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )


@dataclass
class CandidatePositionInformationType:
    class Meta:
        name = "candidatePositionInformationType"

    position_on_list: Optional[int] = field(
        default=None,
        metadata={
            "name": "positionOnList",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    candidate_reference_on_position: Optional[str] = field(
        default=None,
        metadata={
            "name": "candidateReferenceOnPosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 10,
        }
    )
    candidate_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "candidateIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    candidate_text_on_position: Optional[CandidateTextInformationType] = field(
        default=None,
        metadata={
            "name": "candidateTextOnPosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    checking_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "checkingNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class ContestType:
    class Meta:
        name = "contestType"

    contest_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "contestIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    contest_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "contestDate",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    contest_description: Optional[ContestDescriptionInformationType] = field(
        default=None,
        metadata={
            "name": "contestDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    e_voting_period: Optional[EVotingPeriodType] = field(
        default=None,
        metadata={
            "name": "eVotingPeriod",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class CountingCircle(CountingCircleType):
    class Meta:
        name = "countingCircle"
        namespace = "http://www.ech.ch/xmlns/eCH-0155/5"


@dataclass
class DomainOfInfluenceType:
    class Meta:
        name = "domainOfInfluenceType"
        namespace = "http://www.ech.ch/xmlns/eCH-0155/5"

    domain_of_influence_type: Optional[DomainOfInfluenceTypeType] = field(
        default=None,
        metadata={
            "name": "domainOfInfluenceType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    domain_of_influence_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "domainOfInfluenceIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    domain_of_influence_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "domainOfInfluenceName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    domain_of_influence_shortname: Optional[str] = field(
        default=None,
        metadata={
            "name": "domainOfInfluenceShortname",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 5,
        }
    )


@dataclass
class ElectionGroupDescriptionType(ElectionDescriptionInformationType):
    class Meta:
        name = "electionGroupDescriptionType"


@dataclass
class ListUnionType:
    class Meta:
        name = "listUnionType"

    list_union_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "listUnionIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    list_union_description: Optional[ListUnionDescriptionType] = field(
        default=None,
        metadata={
            "name": "listUnionDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    list_union_type: Optional[ListRelationType] = field(
        default=None,
        metadata={
            "name": "listUnionType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    referenced_list: List[str] = field(
        default_factory=list,
        metadata={
            "name": "referencedList",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_occurs": 1,
            "min_length": 1,
            "max_length": 50,
        }
    )
    referenced_list_union: Optional[str] = field(
        default=None,
        metadata={
            "name": "referencedListUnion",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 50,
        }
    )


@dataclass
class PoliticalAddressInfoType:
    class Meta:
        name = "politicalAddressInfoType"

    political_address: Optional[SwissAddressInformationType] = field(
        default=None,
        metadata={
            "name": "politicalAddress",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    municipality_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "municipalityId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 9999,
            "total_digits": 4,
        }
    )


@dataclass
class ReferencedElectionInformationType:
    class Meta:
        name = "referencedElectionInformationType"

    referenced_election: Optional[str] = field(
        default=None,
        metadata={
            "name": "referencedElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    election_relation: Optional[ElectionRelationType] = field(
        default=None,
        metadata={
            "name": "electionRelation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )


@dataclass
class VotingPersonIdentificationType:
    class Meta:
        name = "votingPersonIdentificationType"

    vn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_inclusive": 7560000000001,
            "max_inclusive": 7569999999999,
        }
    )
    local_person_id: Optional[NamedPersonIdType] = field(
        default=None,
        metadata={
            "name": "localPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    other_person_id: List[NamedPersonIdType] = field(
        default_factory=list,
        metadata={
            "name": "otherPersonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    official_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "officialName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 100,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "firstName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 100,
        }
    )
    sex: Optional[SexType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    date_of_birth: Optional[DatePartiallyKnownType] = field(
        default=None,
        metadata={
            "name": "dateOfBirth",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class CandidateGroup(CandidateGroupType):
    class Meta:
        name = "candidateGroup"
        namespace = "http://www.ech.ch/xmlns/eCH-0155/5"


@dataclass
class CandidateType:
    class Meta:
        name = "candidateType"

    vn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_inclusive": 7560000000001,
            "max_inclusive": 7569999999999,
        }
    )
    candidate_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "candidateIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    bf_snumber_canton: Optional[int] = field(
        default=None,
        metadata={
            "name": "BfSNumberCanton",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_inclusive": 1,
            "max_inclusive": 26,
        }
    )
    family_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "familyName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
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
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 100,
        }
    )
    call_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "callName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        }
    )
    candidate_text: Optional[CandidateTextInformationType] = field(
        default=None,
        metadata={
            "name": "candidateText",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    date_of_birth: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "dateOfBirth",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    sex: Optional[SexType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    occupational_title: Optional[OccupationalTitleInformationType] = field(
        default=None,
        metadata={
            "name": "occupationalTitle",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    contact_address: Optional[PersonMailAddressType] = field(
        default=None,
        metadata={
            "name": "contactAddress",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    political_address: Optional[PoliticalAddressInfoType] = field(
        default=None,
        metadata={
            "name": "politicalAddress",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    dwelling_address: Optional[AddressInformationType] = field(
        default=None,
        metadata={
            "name": "dwellingAddress",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    swiss: Optional["CandidateType.Swiss"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    foreigner: Optional["CandidateType.Foreigner"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    mr_mrs: Optional[MrMrsType] = field(
        default=None,
        metadata={
            "name": "mrMrs",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "max_length": 50,
        }
    )
    language_of_correspondence: Optional[str] = field(
        default=None,
        metadata={
            "name": "languageOfCorrespondence",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "length": 2,
        }
    )
    incumbent_yes_no: Optional[bool] = field(
        default=None,
        metadata={
            "name": "incumbentYesNo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    candidate_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "candidateReference",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 10,
        }
    )
    role: Optional[RoleInformationType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    party_affiliation: Optional[PartyAffiliationInformationType] = field(
        default=None,
        metadata={
            "name": "partyAffiliation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    eligibility: Optional[EligibilityType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    sort_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "sortID",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    candidate_group_identification: List[str] = field(
        default_factory=list,
        metadata={
            "name": "candidateGroupIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 50,
        }
    )

    @dataclass
    class Swiss:
        origin: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 80,
            }
        )

    @dataclass
    class Foreigner:
        residence_permit: Optional[ResidencePermitType] = field(
            default=None,
            metadata={
                "name": "residencePermit",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "nillable": True,
            }
        )
        dwelling_address: Optional[SwissAddressInformationType] = field(
            default=None,
            metadata={
                "name": "dwellingAddress",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
            }
        )
        in_canton_since: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "inCantonSince",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
            }
        )
        nationality: Optional[CountryType] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
            }
        )


@dataclass
class Contest(ContestType):
    class Meta:
        name = "contest"
        namespace = "http://www.ech.ch/xmlns/eCH-0155/5"


@dataclass
class ElectionType:
    class Meta:
        name = "electionType"

    election_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "electionIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    type_of_election: Optional[TypeOfElectionType] = field(
        default=None,
        metadata={
            "name": "typeOfElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    election_position: Optional[int] = field(
        default=None,
        metadata={
            "name": "electionPosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    election_description: Optional[ElectionDescriptionInformationType] = field(
        default=None,
        metadata={
            "name": "electionDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    number_of_mandates: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfMandates",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    referenced_election: List[ReferencedElectionInformationType] = field(
        default_factory=list,
        metadata={
            "name": "referencedElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class ListType:
    class Meta:
        name = "listType"

    list_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "listIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    list_indenture_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "listIndentureNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 6,
        }
    )
    list_description: Optional[ListDescriptionInformationType] = field(
        default=None,
        metadata={
            "name": "listDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    is_empty_list: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isEmptyList",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    list_order_of_precedence: Optional[int] = field(
        default=None,
        metadata={
            "name": "listOrderOfPrecedence",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    total_positions_on_list: Optional[int] = field(
        default=None,
        metadata={
            "name": "totalPositionsOnList",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    candidate_position: List[CandidatePositionInformationType] = field(
        default_factory=list,
        metadata={
            "name": "candidatePosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    empty_list_positions: Optional[int] = field(
        default=None,
        metadata={
            "name": "emptyListPositions",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    list_union_ballot_text: Optional[ListUnionBallotTextType] = field(
        default=None,
        metadata={
            "name": "listUnionBallotText",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class QuestionInformationType:
    class Meta:
        name = "questionInformationType"

    question_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "questionIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    electronic_ballot_question_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "electronicBallotQuestionNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 15,
        }
    )
    question_position: Optional[int] = field(
        default=None,
        metadata={
            "name": "questionPosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    answer_information: Optional[AnswerInformationType] = field(
        default=None,
        metadata={
            "name": "answerInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    electronic_ballot_question: Optional[ElectronicBallotQuestionType] = field(
        default=None,
        metadata={
            "name": "electronicBallotQuestion",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )


@dataclass
class TieBreakInformationType:
    class Meta:
        name = "tieBreakInformationType"

    answer_information: Optional[AnswerInformationType] = field(
        default=None,
        metadata={
            "name": "answerInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    question_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "questionIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    tie_break_question_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "tieBreakQuestionNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 15,
        }
    )
    question_position: Optional[int] = field(
        default=None,
        metadata={
            "name": "questionPosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    tie_break_question: Optional[TieBreakQuestionType] = field(
        default=None,
        metadata={
            "name": "tieBreakQuestion",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    referenced_question1: Optional[str] = field(
        default=None,
        metadata={
            "name": "referencedQuestion1",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 50,
        }
    )
    referenced_question2: Optional[str] = field(
        default=None,
        metadata={
            "name": "referencedQuestion2",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 50,
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
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    domain_of_influence: Optional[DomainOfInfluenceType] = field(
        default=None,
        metadata={
            "name": "domainOfInfluence",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    vote_description: Optional[VoteDescriptionInformationType] = field(
        default=None,
        metadata={
            "name": "voteDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class VotingCardType:
    class Meta:
        name = "votingCardType"

    voting_card_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "votingCardNumber",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 50,
        }
    )
    voting_person_identification: Optional[
        VotingPersonIdentificationType
    ] = field(
        default=None,
        metadata={
            "name": "votingPersonIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    domain_of_influence: List[DomainOfInfluenceType] = field(
        default_factory=list,
        metadata={
            "name": "domainOfInfluence",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    voter_type: Optional[VoterTypeType] = field(
        default=None,
        metadata={
            "name": "voterType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    voting_channel: Optional[VotingChannelType] = field(
        default=None,
        metadata={
            "name": "votingChannel",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    date_of_voting: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "dateOfVoting",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    time_of_voting: Optional[XmlTime] = field(
        default=None,
        metadata={
            "name": "timeOfVoting",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    place_of_voting: Optional[str] = field(
        default=None,
        metadata={
            "name": "placeOfVoting",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "min_length": 1,
            "max_length": 100,
        }
    )
    electronic_voting_card_yes_no: Optional[bool] = field(
        default=None,
        metadata={
            "name": "electronicVotingCardYesNo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )


@dataclass
class Candidate(CandidateType):
    class Meta:
        name = "candidate"
        namespace = "http://www.ech.ch/xmlns/eCH-0155/5"


@dataclass
class Election(ElectionType):
    class Meta:
        name = "election"
        namespace = "http://www.ech.ch/xmlns/eCH-0155/5"


@dataclass
class ElectronicBallotType:
    class Meta:
        name = "electronicBallotType"

    electronic_ballot_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "electronicBallotIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    electronic_ballot_position: Optional[int] = field(
        default=None,
        metadata={
            "name": "electronicBallotPosition",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            "required": True,
        }
    )
    electronic_ballot_description: Optional[
        ElectronicBallotDescriptionInformationType
    ] = field(
        default=None,
        metadata={
            "name": "electronicBallotDescription",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    electronic_ballot_group: Optional[
        ElectronicBallotDescriptionInformationType
    ] = field(
        default=None,
        metadata={
            "name": "electronicBallotGroup",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    standard_electronic_ballot: Optional[
        "ElectronicBallotType.StandardElectronicBallot"
    ] = field(
        default=None,
        metadata={
            "name": "standardElectronicBallot",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    variant_electronic_ballot: Optional[
        "ElectronicBallotType.VariantElectronicBallot"
    ] = field(
        default=None,
        metadata={
            "name": "variantElectronicBallot",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
        }
    )

    @dataclass
    class StandardElectronicBallot:
        question_identification: Optional[str] = field(
            default=None,
            metadata={
                "name": "questionIdentification",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
                "min_length": 1,
                "max_length": 50,
            }
        )
        electronic_ballot_question_number: Optional[str] = field(
            default=None,
            metadata={
                "name": "electronicBallotQuestionNumber",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_length": 1,
                "max_length": 15,
            }
        )
        answer_information: Optional[AnswerInformationType] = field(
            default=None,
            metadata={
                "name": "answerInformation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            }
        )
        electronic_ballot_question: Optional[
            ElectronicBallotQuestionType
        ] = field(
            default=None,
            metadata={
                "name": "electronicBallotQuestion",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "required": True,
            }
        )

    @dataclass
    class VariantElectronicBallot:
        question_information: List[
            "ElectronicBallotType.VariantElectronicBallot.QuestionInformation"
        ] = field(
            default_factory=list,
            metadata={
                "name": "questionInformation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                "min_occurs": 2,
            }
        )
        tie_break_information: List[
            "ElectronicBallotType.VariantElectronicBallot.TieBreakInformation"
        ] = field(
            default_factory=list,
            metadata={
                "name": "tieBreakInformation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
            }
        )

        @dataclass
        class QuestionInformation(QuestionInformationType):
            question_group_number: Optional[str] = field(
                default=None,
                metadata={
                    "name": "questionGroupNumber",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                    "min_length": 1,
                    "max_length": 15,
                }
            )

        @dataclass
        class TieBreakInformation(TieBreakInformationType):
            question_group_number: Optional[str] = field(
                default=None,
                metadata={
                    "name": "questionGroupNumber",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0155/5",
                    "min_length": 1,
                    "max_length": 15,
                }
            )
