from typing import overload
import abc
import typing

import QuantConnect.Notifications
import System
import System.Collections.Concurrent
import System.Collections.Generic

JsonConverter = typing.Any


class Notification(System.Object, metaclass=abc.ABCMeta):
    """Local/desktop implementation of messaging system for Lean Engine."""

    def Send(self) -> None:
        """Method for sending implementations of notification object types."""
        ...


class NotificationWeb(QuantConnect.Notifications.Notification):
    """Web Notification Class"""

    @property
    def Headers(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Optional email headers"""
        ...

    @Headers.setter
    def Headers(self, value: System.Collections.Generic.Dictionary[str, str]):
        """Optional email headers"""
        ...

    @property
    def Address(self) -> str:
        """Send a notification message to this web address"""
        ...

    @Address.setter
    def Address(self, value: str):
        """Send a notification message to this web address"""
        ...

    @property
    def Data(self) -> System.Object:
        """Object data to send."""
        ...

    @Data.setter
    def Data(self, value: System.Object):
        """Object data to send."""
        ...

    def __init__(self, address: str, data: typing.Any = None, headers: System.Collections.Generic.Dictionary[str, str] = None) -> None:
        """
        Constructor for sending a notification SMS to a specified phone number
        
        :param address: Address to send to
        :param data: Data to send
        :param headers: Optional headers to use
        """
        ...


class NotificationSms(QuantConnect.Notifications.Notification):
    """Sms Notification Class"""

    @property
    def PhoneNumber(self) -> str:
        """Send a notification message to this phone number"""
        ...

    @PhoneNumber.setter
    def PhoneNumber(self, value: str):
        """Send a notification message to this phone number"""
        ...

    @property
    def Message(self) -> str:
        """Message to send. Limited to 160 characters"""
        ...

    @Message.setter
    def Message(self, value: str):
        """Message to send. Limited to 160 characters"""
        ...

    def __init__(self, number: str, message: str) -> None:
        """Constructor for sending a notification SMS to a specified phone number"""
        ...


class NotificationEmail(QuantConnect.Notifications.Notification):
    """Email notification data."""

    @property
    def Headers(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Optional email headers"""
        ...

    @Headers.setter
    def Headers(self, value: System.Collections.Generic.Dictionary[str, str]):
        """Optional email headers"""
        ...

    @property
    def Address(self) -> str:
        """Send to address:"""
        ...

    @Address.setter
    def Address(self, value: str):
        """Send to address:"""
        ...

    @property
    def Subject(self) -> str:
        """Email subject"""
        ...

    @Subject.setter
    def Subject(self, value: str):
        """Email subject"""
        ...

    @property
    def Message(self) -> str:
        """Message to send."""
        ...

    @Message.setter
    def Message(self, value: str):
        """Message to send."""
        ...

    @property
    def Data(self) -> str:
        """Email Data"""
        ...

    @Data.setter
    def Data(self, value: str):
        """Email Data"""
        ...

    def __init__(self, address: str, subject: str = ..., message: str = ..., data: str = ..., headers: System.Collections.Generic.Dictionary[str, str] = None) -> None:
        """
        Default constructor for sending an email notification
        
        :param address: Address to send to. Will throw ArgumentException if invalid Validate.EmailAddress
        :param subject: Subject of the email. Will set to string.Empty if null
        :param message: Message body of the email. Will set to string.Empty if null
        :param data: Data to attach to the email. Will set to string.Empty if null
        :param headers: Optional email headers to use
        """
        ...


class NotificationTelegram(QuantConnect.Notifications.Notification):
    """Telegram notification data"""

    @property
    def Id(self) -> str:
        """
        Send a notification message to this user on Telegram
        Can be either a personal ID or Group ID.
        """
        ...

    @Id.setter
    def Id(self, value: str):
        """
        Send a notification message to this user on Telegram
        Can be either a personal ID or Group ID.
        """
        ...

    @property
    def Message(self) -> str:
        """Message to send. Limited to 4096 characters"""
        ...

    @Message.setter
    def Message(self, value: str):
        """Message to send. Limited to 4096 characters"""
        ...

    @property
    def Token(self) -> str:
        """Token to use"""
        ...

    @Token.setter
    def Token(self, value: str):
        """Token to use"""
        ...

    def __init__(self, id: str, message: str, token: str = None) -> None:
        """
        Constructor for sending a telegram notification to a specific User ID
        or group ID. Note: The bot must have an open chat with the user or be
        added to the group for messages to deliver.
        
        :param id: User Id or Group Id to send the message too
        :param message: Message to send
        :param token: Bot token to use, if null defaults to "telegram-token" in config on send
        """
        ...


class NotificationJsonConverter(JsonConverter):
    """Defines a JsonConverter to be used when deserializing to the Notification class."""

    @property
    def CanWrite(self) -> bool:
        """Use default implementation to write the json"""
        ...

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: typing.Type, existingValue: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param objectType: Type of the object.
        :param existingValue: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class TemplateType(System.Enum):
    """This class has no documentation."""

    PriceDropAlert = 0
    """警告，{1}账户{2}的{3}的价格为{4}，几乎快要回落到0.98倍的上线{5}"""

    SystemAlert = 1
    """服务器{1}紧急状态，{2}"""

    MarginCall = 2
    """{1}账户保证金不足"""


class NotificationSlack(QuantConnect.Notifications.Notification):
    """Slack notification data."""

    @property
    def Token(self) -> str:
        """Send to address:"""
        ...

    @Token.setter
    def Token(self, value: str):
        """Send to address:"""
        ...

    @property
    def Message(self) -> str:
        """Message to send. Limited to 160 characters"""
        ...

    @Message.setter
    def Message(self, value: str):
        """Message to send. Limited to 160 characters"""
        ...

    def __init__(self, token: str, message: str) -> None:
        """
        Default constructor for sending an email notification
        
        :param message: Message body of the email
        """
        ...

    def Send(self) -> None:
        ...


class NotificationSlackCall(QuantConnect.Notifications.Notification):
    """Slack notification data."""

    PerservedTokens: System.Collections.Generic.IList[str]

    @property
    def ImmediateTokens(self) -> System.Collections.Generic.IList[str]:
        ...

    @ImmediateTokens.setter
    def ImmediateTokens(self, value: System.Collections.Generic.IList[str]):
        ...

    @overload
    def __init__(self) -> None:
        """Default constructor for sending an slack phone call notification"""
        ...

    @overload
    def __init__(self, token: str) -> None:
        """
        Default constructor for sending an slack phone call notification
        
        :param token: Token endpoint for this slack call
        """
        ...

    @overload
    def __init__(self, tokens: System.Collections.Generic.IList[str]) -> None:
        """Default constructor for sending an slack phone call notification"""
        ...

    @staticmethod
    def ResetPerservedTokens(inputTokens: System.Collections.Generic.IList[str]) -> None:
        ...

    def Send(self) -> None:
        ...


class NotificationVoiceCall(QuantConnect.Notifications.Notification):
    """Voice call notification data."""

    PerservedNumbers: System.Collections.Generic.IList[str]

    @property
    def TemplateId(self) -> str:
        ...

    @TemplateId.setter
    def TemplateId(self, value: str):
        ...

    @property
    def PlayTimes(self) -> str:
        ...

    @PlayTimes.setter
    def PlayTimes(self, value: str):
        ...

    @property
    def TemplateParams(self) -> System.Collections.Generic.List[str]:
        ...

    @TemplateParams.setter
    def TemplateParams(self, value: System.Collections.Generic.List[str]):
        ...

    @property
    def ImmediateNumbers(self) -> System.Collections.Generic.List[str]:
        ...

    @ImmediateNumbers.setter
    def ImmediateNumbers(self, value: System.Collections.Generic.List[str]):
        ...

    @overload
    def __init__(self, templateId: str, templateParams: System.Collections.Generic.IList[str]) -> None:
        """Default constructor for sending an voice call notification"""
        ...

    @overload
    def __init__(self, phoneNumber: str, templateId: str, templateParams: System.Collections.Generic.IEnumerable[str]) -> None:
        """Default constructor for sending an voice call notification"""
        ...

    @overload
    def __init__(self, phoneNumbers: System.Collections.Generic.IEnumerable[str], templateId: str, templateParams: System.Collections.Generic.IEnumerable[str]) -> None:
        """Default constructor for sending an voice call notification"""
        ...

    @staticmethod
    def ResetPerservedNumbers(inputNumbers: System.Collections.Generic.IList[str]) -> None:
        ...

    def Send(self) -> None:
        ...


class NotificationDingDing(QuantConnect.Notifications.Notification):
    """Dingding message notification data."""

    @property
    def Endpoint(self) -> str:
        ...

    @Endpoint.setter
    def Endpoint(self, value: str):
        ...

    @property
    def Keyword(self) -> str:
        ...

    @Keyword.setter
    def Keyword(self, value: str):
        ...

    @property
    def Content(self) -> str:
        ...

    @Content.setter
    def Content(self, value: str):
        ...

    def __init__(self, endpoint: str, keyword: str = ..., content: str = ...) -> None:
        ...

    def Send(self) -> None:
        ...


class NotificationManager(System.Object):
    """Local/desktop implementation of messaging system for Lean Engine."""

    @property
    def Messages(self) -> System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Notifications.Notification]:
        """Public access to the messages"""
        ...

    @Messages.setter
    def Messages(self, value: System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Notifications.Notification]):
        """Public access to the messages"""
        ...

    def __init__(self, liveMode: bool) -> None:
        """Initialize the messaging system"""
        ...

    def DingDing(self, token: str, keyword: str = ..., message: str = ...) -> bool:
        ...

    @overload
    def Email(self, address: str, subject: str, message: str, data: str, headers: typing.Any) -> bool:
        """
        Send an email to the address specified for live trading notifications.
        
        :param address: Email address to send to
        :param subject: Subject of the email
        :param message: Message body, up to 10kb
        :param data: Data attachment (optional)
        :param headers: Optional email headers to use
        """
        ...

    @overload
    def Email(self, address: str, subject: str, message: str, data: str = ..., headers: System.Collections.Generic.Dictionary[str, str] = None) -> bool:
        """
        Send an email to the address specified for live trading notifications.
        
        :param address: Email address to send to
        :param subject: Subject of the email
        :param message: Message body, up to 10kb
        :param data: Data attachment (optional)
        :param headers: Optional email headers to use
        """
        ...

    @staticmethod
    def GetTemplateId(type: QuantConnect.Notifications.TemplateType) -> str:
        """This method is protected."""
        ...

    @overload
    def Slack(self, token: str, message: str) -> bool:
        """
        Send a slack message to the user specified
        
        :param message: Message to send
        """
        ...

    @overload
    def Slack(self, message: str) -> bool:
        ...

    @overload
    def SlackCall(self, token: str) -> bool:
        ...

    @overload
    def SlackCall(self, tokens: System.Collections.Generic.IList[str]) -> bool:
        ...

    @overload
    def SlackCall(self) -> bool:
        ...

    @overload
    def SlackCallSaved(self) -> bool:
        ...

    @overload
    def SlackCallSaved(self, tokens: System.Collections.Generic.IList[str]) -> bool:
        ...

    def Sms(self, phoneNumber: str, message: str) -> bool:
        """
        Send an SMS to the phone number specified
        
        :param phoneNumber: Phone number to send to
        :param message: Message to send
        """
        ...

    def Telegram(self, id: str, message: str, token: str = None) -> bool:
        """
        Send a telegram message to the chat ID specified, supply token for custom bot.
        Note: Requires bot to have chat with user or be in the group specified by ID.
        
        :param message: Message to send
        :param token: Bot token to use for this message
        """
        ...

    @overload
    def VoiceCall(self, phoneNumber: str, type: QuantConnect.Notifications.TemplateType, *templateParams: str) -> bool:
        """Send a voice notification over phone to a restful endpoint."""
        ...

    @overload
    def VoiceCall(self, phoneNumbers: typing.List[str], type: QuantConnect.Notifications.TemplateType, *templateParams: str) -> bool:
        ...

    @overload
    def VoiceCall(self, type: QuantConnect.Notifications.TemplateType, *templateParams: str) -> bool:
        ...

    @overload
    def VoiceCallSaved(self, type: QuantConnect.Notifications.TemplateType, *templateParams: str) -> bool:
        ...

    @overload
    def VoiceCallSaved(self, phoneNumbers: typing.List[str], type: QuantConnect.Notifications.TemplateType, *templateParams: str) -> bool:
        ...

    @overload
    def Web(self, address: str, data: typing.Any, headers: typing.Any) -> bool:
        """
        Place REST POST call to the specified address with the specified DATA.
        Python overload for Headers parameter.
        
        :param address: Endpoint address
        :param data: Data to send in body JSON encoded
        :param headers: Optional headers to use
        """
        ...

    @overload
    def Web(self, address: str, data: typing.Any = None, headers: System.Collections.Generic.Dictionary[str, str] = None) -> bool:
        """
        Place REST POST call to the specified address with the specified DATA.
        
        :param address: Endpoint address
        :param data: Data to send in body JSON encoded (optional)
        :param headers: Optional headers to use
        """
        ...


