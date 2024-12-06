from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatabaseSourceReference(_message.Message):
    __slots__ = ("source_type", "name")
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    def __init__(self, source_type: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DatabaseSource(_message.Message):
    __slots__ = ("source_type", "name", "options")
    class OptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    options: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        source_type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class StreamSourceReference(_message.Message):
    __slots__ = ("source_type", "name")
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    def __init__(self, source_type: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class StreamSource(_message.Message):
    __slots__ = ("source_type", "name", "options")
    class OptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    options: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        source_type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...
