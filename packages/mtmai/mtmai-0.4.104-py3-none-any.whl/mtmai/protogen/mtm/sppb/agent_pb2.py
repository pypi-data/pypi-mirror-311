# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mtm/sppb/agent.proto
# Protobuf Python Version: 5.28.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    3,
    '',
    'mtm/sppb/agent.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14mtm/sppb/agent.proto\x12\x04sppb\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a google/protobuf/descriptor.proto\x1a google/protobuf/field_mask.proto\x1a\x1b\x62uf/validate/validate.proto\"\x93\x01\n\x0bRunAgentReq\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x35\n\x06params\x18\x03 \x03(\x0b\x32\x1d.sppb.RunAgentReq.ParamsEntryR\x06params\x1a\x39\n\x0bParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"0\n\rRunAgentReply\x12\x1f\n\x0bmessage_chn\x18\x01 \x01(\tR\nmessageChn2D\n\x0c\x41gentService\x12\x34\n\x08RunAgent\x12\x11.sppb.RunAgentReq\x1a\x13.sppb.RunAgentReply\"\x00\x42j\n\x08\x63om.sppbB\nAgentProtoP\x01Z\"github.com/codeh007/gomtm/mtm/sppb\xa2\x02\x03SXX\xaa\x02\x04Sppb\xca\x02\x04Sppb\xe2\x02\x10Sppb\\GPBMetadata\xea\x02\x04Sppbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mtm.sppb.agent_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\010com.sppbB\nAgentProtoP\001Z\"github.com/codeh007/gomtm/mtm/sppb\242\002\003SXX\252\002\004Sppb\312\002\004Sppb\342\002\020Sppb\\GPBMetadata\352\002\004Sppb'
  _globals['_RUNAGENTREQ_PARAMSENTRY']._loaded_options = None
  _globals['_RUNAGENTREQ_PARAMSENTRY']._serialized_options = b'8\001'
  _globals['_RUNAGENTREQ']._serialized_start=188
  _globals['_RUNAGENTREQ']._serialized_end=335
  _globals['_RUNAGENTREQ_PARAMSENTRY']._serialized_start=278
  _globals['_RUNAGENTREQ_PARAMSENTRY']._serialized_end=335
  _globals['_RUNAGENTREPLY']._serialized_start=337
  _globals['_RUNAGENTREPLY']._serialized_end=385
  _globals['_AGENTSERVICE']._serialized_start=387
  _globals['_AGENTSERVICE']._serialized_end=455
# @@protoc_insertion_point(module_scope)
