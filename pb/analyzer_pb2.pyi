from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParseMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Parsed: _ClassVar[ParseMode]
    Unparsed: _ClassVar[ParseMode]
Parsed: ParseMode
Unparsed: ParseMode

class UUID(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class LogInstance(_message.Message):
    __slots__ = ["id", "servName", "log"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SERVNAME_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    id: UUID
    servName: str
    log: str
    def __init__(self, id: _Optional[_Union[UUID, _Mapping]] = ..., servName: _Optional[str] = ..., log: _Optional[str] = ...) -> None: ...

class AnalyzerRequest(_message.Message):
    __slots__ = ["id", "parseMode", "recent", "history"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PARSEMODE_FIELD_NUMBER: _ClassVar[int]
    RECENT_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    id: UUID
    parseMode: ParseMode
    recent: _containers.RepeatedCompositeFieldContainer[LogInstance]
    history: _containers.RepeatedCompositeFieldContainer[LogInstance]
    def __init__(self, id: _Optional[_Union[UUID, _Mapping]] = ..., parseMode: _Optional[_Union[ParseMode, str]] = ..., recent: _Optional[_Iterable[_Union[LogInstance, _Mapping]]] = ..., history: _Optional[_Iterable[_Union[LogInstance, _Mapping]]] = ...) -> None: ...

class AnalyzerResponse(_message.Message):
    __slots__ = ["id", "rating", "review", "insight", "citation"]
    ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    REVIEW_FIELD_NUMBER: _ClassVar[int]
    INSIGHT_FIELD_NUMBER: _ClassVar[int]
    CITATION_FIELD_NUMBER: _ClassVar[int]
    id: UUID
    rating: int
    review: str
    insight: str
    citation: str
    def __init__(self, id: _Optional[_Union[UUID, _Mapping]] = ..., rating: _Optional[int] = ..., review: _Optional[str] = ..., insight: _Optional[str] = ..., citation: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Prompt(_message.Message):
    __slots__ = ["tmp", "pmt"]
    TMP_FIELD_NUMBER: _ClassVar[int]
    PMT_FIELD_NUMBER: _ClassVar[int]
    tmp: str
    pmt: str
    def __init__(self, tmp: _Optional[str] = ..., pmt: _Optional[str] = ...) -> None: ...
