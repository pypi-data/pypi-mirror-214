from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgAddQuotaRequest(_message.Message):
    __slots__ = ["address", "bytes", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    bytes: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ..., bytes: _Optional[str] = ..., **kwargs) -> None: ...

class MsgAddQuotaResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgCancelRequest(_message.Message):
    __slots__ = ["id"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ..., **kwargs) -> None: ...

class MsgCancelResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgSubscribeToNodeRequest(_message.Message):
    __slots__ = ["address", "deposit"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    address: str
    deposit: _coin_pb2.Coin
    def __init__(self, address: _Optional[str] = ..., deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., **kwargs) -> None: ...

class MsgSubscribeToNodeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgSubscribeToPlanRequest(_message.Message):
    __slots__ = ["denom", "id"]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    denom: str
    id: int
    def __init__(self, id: _Optional[int] = ..., denom: _Optional[str] = ..., **kwargs) -> None: ...

class MsgSubscribeToPlanResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgUpdateQuotaRequest(_message.Message):
    __slots__ = ["address", "bytes", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    bytes: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ..., bytes: _Optional[str] = ..., **kwargs) -> None: ...

class MsgUpdateQuotaResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
