from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgAddNodeRequest(_message.Message):
    __slots__ = ["address", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ..., **kwargs) -> None: ...

class MsgAddNodeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgAddRequest(_message.Message):
    __slots__ = ["bytes", "price", "validity"]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    bytes: str
    price: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    validity: _duration_pb2.Duration
    def __init__(self, price: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., validity: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., bytes: _Optional[str] = ..., **kwargs) -> None: ...

class MsgAddResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgRemoveNodeRequest(_message.Message):
    __slots__ = ["address", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ..., **kwargs) -> None: ...

class MsgRemoveNodeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgSetStatusRequest(_message.Message):
    __slots__ = ["id", "status"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    status: _status_pb2.Status
    def __init__(self, id: _Optional[int] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., **kwargs) -> None: ...

class MsgSetStatusResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
