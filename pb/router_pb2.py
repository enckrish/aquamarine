# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb/router.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0fpb/router.proto\"K\n\x11InitRequest_Type0\x12\x10\n\x08streamId\x18\x01 \x01(\t\x12\x0f\n\x07service\x18\x02 \x01(\t\x12\x13\n\x0bhistorySize\x18\x03 \x01(\r\"&\n\x12InitResponse_Type0\x12\x10\n\x08streamId\x18\x01 \x01(\t\"J\n\x15\x41nalyzerRequest_Type0\x12\x10\n\x08streamId\x18\x01 \x01(\t\x12\x11\n\tmessageId\x18\x02 \x01(\t\x12\x0c\n\x04logs\x18\x03 \x03(\t\"%\n\x10\x41nalyzerResponse\x12\x11\n\tcommitted\x18\x01 \x01(\x08\x32\x84\x01\n\x06Router\x12\x37\n\ninit_Type0\x12\x12.InitRequest_Type0\x1a\x13.InitResponse_Type0\"\x00\x12\x41\n\x0erouteLog_Type0\x12\x16.AnalyzerRequest_Type0\x1a\x11.AnalyzerResponse\"\x00(\x01\x30\x01\x42\x06Z\x04./pbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pb.router_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z\004./pb'
    _globals['_INITREQUEST_TYPE0']._serialized_start = 19
    _globals['_INITREQUEST_TYPE0']._serialized_end = 94
    _globals['_INITRESPONSE_TYPE0']._serialized_start = 96
    _globals['_INITRESPONSE_TYPE0']._serialized_end = 134
    _globals['_ANALYZERREQUEST_TYPE0']._serialized_start = 136
    _globals['_ANALYZERREQUEST_TYPE0']._serialized_end = 210
    _globals['_ANALYZERRESPONSE']._serialized_start = 212
    _globals['_ANALYZERRESPONSE']._serialized_end = 249
    _globals['_ROUTER']._serialized_start = 252
    _globals['_ROUTER']._serialized_end = 384
# @@protoc_insertion_point(module_scope)
