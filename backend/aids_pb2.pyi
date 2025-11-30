from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Chunk(_message.Message):
    __slots__ = ("content", "file_name")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    file_name: str
    def __init__(self, content: _Optional[bytes] = ..., file_name: _Optional[str] = ...) -> None: ...

class UploadResponse(_message.Message):
    __slots__ = ("id", "message")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    message: str
    def __init__(self, id: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class DatasetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SummaryResponse(_message.Message):
    __slots__ = ("summary_data",)
    SUMMARY_DATA_FIELD_NUMBER: _ClassVar[int]
    summary_data: str
    def __init__(self, summary_data: _Optional[str] = ...) -> None: ...

class DatasetInfo(_message.Message):
    __slots__ = ("id", "name", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    created_at: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class DatasetListResponse(_message.Message):
    __slots__ = ("datasets",)
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[DatasetInfo]
    def __init__(self, datasets: _Optional[_Iterable[_Union[DatasetInfo, _Mapping]]] = ...) -> None: ...

class ChartRequest(_message.Message):
    __slots__ = ("id", "x_axis", "y_axis")
    ID_FIELD_NUMBER: _ClassVar[int]
    X_AXIS_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_FIELD_NUMBER: _ClassVar[int]
    id: int
    x_axis: str
    y_axis: str
    def __init__(self, id: _Optional[int] = ..., x_axis: _Optional[str] = ..., y_axis: _Optional[str] = ...) -> None: ...

class ChartResponse(_message.Message):
    __slots__ = ("svg",)
    SVG_FIELD_NUMBER: _ClassVar[int]
    svg: str
    def __init__(self, svg: _Optional[str] = ...) -> None: ...
