# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nbase.proto\x12\x07project\"#\n\x06\x43lient\x12\x0b\n\x03\x43ID\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"$\n\x07Product\x12\x0b\n\x03PID\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"/\n\x05Order\x12\x0b\n\x03OID\x18\x01 \x01(\t\x12\x0b\n\x03\x43ID\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\t\"@\n\x05Reply\x12\r\n\x05\x65rror\x18\x01 \x01(\x05\x12\x18\n\x0b\x64\x65scription\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_description\"\x10\n\x02ID\x12\n\n\x02ID\x18\x01 \x01(\t2\xa2\x03\n\x0b\x41\x64minPortal\x12\x31\n\x0c\x43reateClient\x12\x0f.project.Client\x1a\x0e.project.Reply\"\x00\x12\x30\n\x0eRetrieveClient\x12\x0b.project.ID\x1a\x0f.project.Client\"\x00\x12\x31\n\x0cUpdateClient\x12\x0f.project.Client\x1a\x0e.project.Reply\"\x00\x12-\n\x0c\x44\x65leteClient\x12\x0b.project.ID\x1a\x0e.project.Reply\"\x00\x12\x33\n\rCreateProduct\x12\x10.project.Product\x1a\x0e.project.Reply\"\x00\x12\x32\n\x0fRetrieveProduct\x12\x0b.project.ID\x1a\x10.project.Product\"\x00\x12\x33\n\rUpdateProduct\x12\x10.project.Product\x1a\x0e.project.Reply\"\x00\x12.\n\rDeleteProduct\x12\x0b.project.ID\x1a\x0e.project.Reply\"\x00\x32\x86\x02\n\x0bOrderPortal\x12/\n\x0b\x43reateOrder\x12\x0e.project.Order\x1a\x0e.project.Reply\"\x00\x12.\n\rRetrieveOrder\x12\x0b.project.ID\x1a\x0e.project.Order\"\x00\x12/\n\x0bUpdateOrder\x12\x0e.project.Order\x1a\x0e.project.Reply\"\x00\x12,\n\x0b\x44\x65leteOrder\x12\x0b.project.ID\x1a\x0e.project.Reply\"\x00\x12\x37\n\x14RetrieveClientOrders\x12\x0b.project.ID\x1a\x0e.project.Order\"\x00\x30\x01\x42\x1f\n\x1b\x62r.ufu.facom.gbc074.projectP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'base_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033br.ufu.facom.gbc074.projectP\001'
  _CLIENT._serialized_start=23
  _CLIENT._serialized_end=58
  _PRODUCT._serialized_start=60
  _PRODUCT._serialized_end=96
  _ORDER._serialized_start=98
  _ORDER._serialized_end=145
  _REPLY._serialized_start=147
  _REPLY._serialized_end=211
  _ID._serialized_start=213
  _ID._serialized_end=229
  _ADMINPORTAL._serialized_start=232
  _ADMINPORTAL._serialized_end=650
  _ORDERPORTAL._serialized_start=653
  _ORDERPORTAL._serialized_end=915
# @@protoc_insertion_point(module_scope)
