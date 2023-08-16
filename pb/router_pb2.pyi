from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor


class InitRequest_Type0(_message.Message):
    __slots__ = ["streamId", "service", "historySize"]
    STREAMID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    HISTORYSIZE_FIELD_NUMBER: _ClassVar[int]
    streamId: str
    service: str
    historySize: int

    def __init__(self, streamId: _Optional[str] = ..., service: _Optional[str] = ...,
                 historySize: _Optional[int] = ...) -> None: ...


class InitResponse_Type0(_message.Message):
    __slots__ = ["streamId"]
    STREAMID_FIELD_NUMBER: _ClassVar[int]
    streamId: str

    def __init__(self, streamId: _Optional[str] = ...) -> None: ...


class AnalyzerRequest_Type0(_message.Message):
    __slots__ = ["streamId", "messageId", "logs"]
    STREAMID_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    streamId: str
    messageId: str
    logs: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, streamId: _Optional[str] = ..., messageId: _Optional[str] = ...,
                 logs: _Optional[_Iterable[str]] = ...) -> None: ...


class AnalyzerResponse(_message.Message):
    __slots__ = ["committed"]
    COMMITTED_FIELD_NUMBER: _ClassVar[int]
    committed: bool

    def __init__(self, committed: bool = ...) -> None: ...
