# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service_types_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service_types_v1.proto',
  package='service.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16service_types_v1.proto\x12\nservice.v1\"/\n\x0cGreetRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\twithError\x18\x02 \x01(\x08\"\x1c\n\x0bGreetResult\x12\r\n\x05reply\x18\x02 \x01(\tb\x06proto3'
)




_GREETREQUEST = _descriptor.Descriptor(
  name='GreetRequest',
  full_name='service.v1.GreetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='service.v1.GreetRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='withError', full_name='service.v1.GreetRequest.withError', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=85,
)


_GREETRESULT = _descriptor.Descriptor(
  name='GreetResult',
  full_name='service.v1.GreetResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='reply', full_name='service.v1.GreetResult.reply', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=115,
)

DESCRIPTOR.message_types_by_name['GreetRequest'] = _GREETREQUEST
DESCRIPTOR.message_types_by_name['GreetResult'] = _GREETRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GreetRequest = _reflection.GeneratedProtocolMessageType('GreetRequest', (_message.Message,), {
  'DESCRIPTOR' : _GREETREQUEST,
  '__module__' : 'service_types_v1_pb2'
  # @@protoc_insertion_point(class_scope:service.v1.GreetRequest)
  })
_sym_db.RegisterMessage(GreetRequest)

GreetResult = _reflection.GeneratedProtocolMessageType('GreetResult', (_message.Message,), {
  'DESCRIPTOR' : _GREETRESULT,
  '__module__' : 'service_types_v1_pb2'
  # @@protoc_insertion_point(class_scope:service.v1.GreetResult)
  })
_sym_db.RegisterMessage(GreetResult)


# @@protoc_insertion_point(module_scope)