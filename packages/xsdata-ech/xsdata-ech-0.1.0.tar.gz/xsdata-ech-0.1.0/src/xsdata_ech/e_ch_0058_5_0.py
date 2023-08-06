from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0058/5"


class ActionType(Enum):
    VALUE_1 = "1"
    VALUE_3 = "3"
    VALUE_4 = "4"
    VALUE_5 = "5"
    VALUE_6 = "6"
    VALUE_8 = "8"
    VALUE_9 = "9"
    VALUE_10 = "10"
    VALUE_12 = "12"


@dataclass
class InfoType:
    class Meta:
        name = "infoType"

    positive_report: Optional["InfoType.PositiveReport"] = field(
        default=None,
        metadata={
            "name": "positiveReport",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    negative_report: Optional["InfoType.NegativeReport"] = field(
        default=None,
        metadata={
            "name": "negativeReport",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )

    @dataclass
    class PositiveReport:
        notice: Optional[object] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            }
        )
        data: Optional[object] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            }
        )

    @dataclass
    class NegativeReport:
        notice: Optional[object] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            }
        )
        data: Optional[object] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            }
        )


@dataclass
class NamedMetaDataType:
    class Meta:
        name = "namedMetaDataType"

    meta_data_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "metaDataName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 20,
        }
    )
    meta_data_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "metaDataValue",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )


@dataclass
class PartialDeliveryType:
    class Meta:
        name = "partialDeliveryType"

    unique_id_delivery: Optional[str] = field(
        default=None,
        metadata={
            "name": "uniqueIdDelivery",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    total_number_of_packages: Optional[int] = field(
        default=None,
        metadata={
            "name": "totalNumberOfPackages",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 9999,
        }
    )
    number_of_actual_package: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfActualPackage",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 9999,
        }
    )


@dataclass
class SendingApplicationType:
    class Meta:
        name = "sendingApplicationType"

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    product: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    product_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "productVersion",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 10,
        }
    )


@dataclass
class HeaderType:
    class Meta:
        name = "headerType"

    sender_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "senderId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
        }
    )
    original_sender_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "originalSenderId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    declaration_local_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "declarationLocalReference",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 100,
        }
    )
    recipient_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "recipientId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    message_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    reference_message_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "referenceMessageId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 36,
        }
    )
    business_process_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "businessProcessId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 128,
        }
    )
    our_business_reference_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ourBusinessReferenceId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 50,
        }
    )
    your_business_reference_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "yourBusinessReferenceId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 50,
        }
    )
    unique_id_business_transaction: Optional[str] = field(
        default=None,
        metadata={
            "name": "uniqueIdBusinessTransaction",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 50,
        }
    )
    message_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
        }
    )
    sub_message_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "subMessageType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 36,
        }
    )
    sending_application: Optional[SendingApplicationType] = field(
        default=None,
        metadata={
            "name": "sendingApplication",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
        }
    )
    partial_delivery: Optional[PartialDeliveryType] = field(
        default=None,
        metadata={
            "name": "partialDelivery",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    subject: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 100,
        }
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "min_length": 1,
            "max_length": 250,
        }
    )
    message_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "messageDate",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
        }
    )
    initial_message_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "initialMessageDate",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    event_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "eventDate",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    modification_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "modificationDate",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    action: Optional[ActionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
        }
    )
    attachment: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    test_delivery_flag: Optional[bool] = field(
        default=None,
        metadata={
            "name": "testDeliveryFlag",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
            "required": True,
        }
    )
    response_expected: Optional[bool] = field(
        default=None,
        metadata={
            "name": "responseExpected",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    business_case_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "businessCaseClosed",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    named_meta_data: List[NamedMetaDataType] = field(
        default_factory=list,
        metadata={
            "name": "namedMetaData",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )
    extension: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0058/5",
        }
    )


@dataclass
class EventReport:
    class Meta:
        name = "eventReport"
        namespace = "http://www.ech.ch/xmlns/eCH-0058/5"

    header: Optional[HeaderType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    info: Optional[InfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Header(HeaderType):
    class Meta:
        name = "header"
        namespace = "http://www.ech.ch/xmlns/eCH-0058/5"
