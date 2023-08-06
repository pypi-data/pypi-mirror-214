from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventAdd(_message.Message):
    __slots__ = ["id", "provider"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    id: int
    provider: str
    def __init__(self, id: _Optional[int] = ..., provider: _Optional[str] = ...) -> None: ...

class EventAddNode(_message.Message):
    __slots__ = ["id", "node", "provider"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    id: int
    node: str
    provider: str
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., provider: _Optional[str] = ...) -> None: ...

class EventRemoveNode(_message.Message):
    __slots__ = ["id", "node", "provider"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    id: int
    node: str
    provider: str
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., provider: _Optional[str] = ...) -> None: ...

class EventSetStatus(_message.Message):
    __slots__ = ["id", "provider", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    provider: str
    status: _status_pb2.Status
    def __init__(self, id: _Optional[int] = ..., provider: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ...) -> None: ...
