from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    t0: _ClassVar[Type]
    t1: _ClassVar[Type]
t0: Type
t1: Type

class UUID(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class InitRequest_Type0(_message.Message):
    __slots__ = ["service", "historySize"]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    HISTORYSIZE_FIELD_NUMBER: _ClassVar[int]
    service: str
    historySize: int
    def __init__(self, service: _Optional[str] = ..., historySize: _Optional[int] = ...) -> None: ...

class InitRequest_Type1(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedCompositeFieldContainer[UUID]
    def __init__(self, ids: _Optional[_Iterable[_Union[UUID, _Mapping]]] = ...) -> None: ...

class InitResponse_Type0(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: UUID
    def __init__(self, id: _Optional[_Union[UUID, _Mapping]] = ...) -> None: ...

class LogInstance_Type0(_message.Message):
    __slots__ = ["logs"]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, logs: _Optional[_Iterable[str]] = ...) -> None: ...

class AnalyzerRequest_Type0(_message.Message):
    __slots__ = ["id", "logs"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    id: UUID
    logs: LogInstance_Type0
    def __init__(self, id: _Optional[_Union[UUID, _Mapping]] = ..., logs: _Optional[_Union[LogInstance_Type0, _Mapping]] = ...) -> None: ...

class AnalyzerResponse(_message.Message):
    __slots__ = ["id", "rating", "actionsInsights", "review", "citation"]
    ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    ACTIONSINSIGHTS_FIELD_NUMBER: _ClassVar[int]
    REVIEW_FIELD_NUMBER: _ClassVar[int]
    CITATION_FIELD_NUMBER: _ClassVar[int]
    id: UUID
    rating: int
    actionsInsights: _containers.RepeatedScalarFieldContainer[str]
    review: str
    citation: int
    def __init__(self, id: _Optional[_Union[UUID, _Mapping]] = ..., rating: _Optional[int] = ..., actionsInsights: _Optional[_Iterable[str]] = ..., review: _Optional[str] = ..., citation: _Optional[int] = ...) -> None: ...

class String(_message.Message):
    __slots__ = ["str"]
    STR_FIELD_NUMBER: _ClassVar[int]
    str: str
    def __init__(self, str: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
