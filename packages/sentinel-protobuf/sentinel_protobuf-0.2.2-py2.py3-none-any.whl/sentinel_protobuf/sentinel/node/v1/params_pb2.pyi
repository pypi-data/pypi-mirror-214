from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ["deposit", "inactive_duration", "max_price", "min_price", "staking_share"]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    INACTIVE_DURATION_FIELD_NUMBER: _ClassVar[int]
    MAX_PRICE_FIELD_NUMBER: _ClassVar[int]
    MIN_PRICE_FIELD_NUMBER: _ClassVar[int]
    STAKING_SHARE_FIELD_NUMBER: _ClassVar[int]
    deposit: _coin_pb2.Coin
    inactive_duration: _duration_pb2.Duration
    max_price: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    min_price: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    staking_share: str
    def __init__(self, deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., inactive_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., max_price: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., min_price: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., staking_share: _Optional[str] = ...) -> None: ...
