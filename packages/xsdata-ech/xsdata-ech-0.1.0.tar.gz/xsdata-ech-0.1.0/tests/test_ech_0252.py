from decimal import Decimal
from pytest import fixture
from typing import Iterator
from xsdata_ech.e_ch_0252_1_0 import (
    CountingCircleInfoType,
    CountingCircleType,
    CountOfVotersInformationType,
    DecisiveMajorityType,
    Delivery,
    DomainOfInfluenceType,
    DomainOfInfluenceTypeType,
    EventVoteBaseDeliveryType,
    NamedIdType,
    ResultDataType,
    VoteInfoType,
    VoterTypeType,
    VoteSubTypeType,
    VoteTitleInformationType,
    VoteType
)
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import JsonParser, XmlParser
from xsdata.formats.dataclass.serializers import JsonSerializer, XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate


SubtotalInfo = CountOfVotersInformationType.SubtotalInfo


@fixture()
def delivery() -> Iterator[Delivery]:
    yield Delivery(
        vote_base_delivery=EventVoteBaseDeliveryType(
            canton_id=1,
            polling_day=XmlDate(2023, 1, 1),
            vote_info=[
                VoteInfoType(
                    vote=VoteType(
                        vote_identification='external-id',
                        main_vote_identification='external-id',
                        other_identification=[
                            NamedIdType(
                                id_name='onegov',
                                id='vote-id'
                            )
                        ],
                        domain_of_influence=DomainOfInfluenceType(
                            domain_of_influence_type=DomainOfInfluenceTypeType(
                                DomainOfInfluenceTypeType.CT
                            ),
                            domain_of_influence_identification='GR',
                            domain_of_influence_name='Kanton Graubünden'
                        ),
                        polling_day=XmlDate(2023, 1, 1),
                        vote_title_information=[
                            VoteTitleInformationType(
                                language='de',
                                vote_title='Title de',
                                vote_title_short='Short Title de'
                            ),
                            VoteTitleInformationType(
                                language='fr',
                                vote_title='Title fr',
                                vote_title_short='Short Title fr'
                            ),
                            VoteTitleInformationType(
                                language='it',
                                vote_title='Title it',
                                vote_title_short='Short Title it'
                            ),
                            VoteTitleInformationType(
                                language='rm',
                                vote_title='Title rm',
                                vote_title_short='Short Title rm'
                            ),
                        ],
                        decisive_majority=DecisiveMajorityType.VALUE_1,
                        vote_sub_type=VoteSubTypeType.VALUE_1
                    ),
                    counting_circle_info=[
                        CountingCircleInfoType(
                            counting_circle=CountingCircleType(
                                counting_circle_id='3901',
                                counting_circle_name='Chur',
                            ),
                            result_data=ResultDataType(
                                count_of_voters_information=(
                                    CountOfVotersInformationType(
                                        count_of_voters_total=100,
                                        subtotal_info=[
                                            SubtotalInfo(
                                                count_of_voters=100,
                                                voter_type=(
                                                    VoterTypeType.VALUE_2
                                                ),
                                            )
                                        ]
                                    )
                                ),
                                fully_counted_true=True,
                                voter_turnout=Decimal('10.03'),
                                received_votes=100,
                                received_invalid_votes=100,
                                received_blank_votes=100,
                                received_valid_votes=100,
                                count_of_yes_votes=100,
                                count_of_no_votes=100,
                                count_of_votes_without_answer=100
                            )
                        )
                    ]
                )
            ],
            number_of_entries=1
        )
    )


def test_ech_0252_xml(delivery: Delivery) -> None:
    # to xml
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    xml = serializer.render(delivery)

    # from xml
    parser = XmlParser(context=XmlContext())
    parsed: Delivery = parser.from_string(xml)
    assert delivery == parsed


def test_ech_0252_json(delivery: Delivery) -> None:
    # to json
    config = SerializerConfig(pretty_print=True)
    serializer = JsonSerializer(config=config)
    json = serializer.render(delivery)

    # from json
    parser = JsonParser(context=XmlContext())
    parsed: Delivery = parser.from_string(json)
    assert delivery == parsed
