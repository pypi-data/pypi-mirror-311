# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/server/v1/status.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.auth.v1 import permissions_pb2 as chalk_dot_auth_dot_v1_dot_permissions__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1c\x63halk/server/v1/status.proto\x12\x0f\x63halk.server.v1\x1a\x1f\x63halk/auth/v1/permissions.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto"\x9c\x03\n\x0bHealthCheck\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12:\n\x06status\x18\x02 \x01(\x0e\x32".chalk.server.v1.HealthCheckStatusR\x06status\x12\x1d\n\x07message\x18\x03 \x01(\tH\x00R\x07message\x88\x01\x01\x12\x38\n\x07latency\x18\x04 \x01(\x0b\x32\x19.google.protobuf.DurationH\x01R\x07latency\x88\x01\x01\x12\x39\n\tkube_data\x18\x05 \x01(\x0b\x32\x17.google.protobuf.StructH\x02R\x08kubeData\x88\x01\x01\x12\x46\n\x08metadata\x18\x06 \x03(\x0b\x32*.chalk.server.v1.HealthCheck.MetadataEntryR\x08metadata\x1a;\n\rMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\n\n\x08_messageB\n\n\x08_latencyB\x0c\n\n_kube_data"d\n\x12HealthCheckFilters\x12\x12\n\x04name\x18\x01 \x03(\tR\x04name\x12:\n\x06status\x18\x02 \x03(\x0e\x32".chalk.server.v1.HealthCheckStatusR\x06status"d\n\x12\x43heckHealthRequest\x12\x42\n\x07\x66ilters\x18\x01 \x01(\x0b\x32#.chalk.server.v1.HealthCheckFiltersH\x00R\x07\x66ilters\x88\x01\x01\x42\n\n\x08_filters"K\n\x13\x43heckHealthResponse\x12\x34\n\x06\x63hecks\x18\x01 \x03(\x0b\x32\x1c.chalk.server.v1.HealthCheckR\x06\x63hecks"b\n\x10GetHealthRequest\x12\x42\n\x07\x66ilters\x18\x01 \x01(\x0b\x32#.chalk.server.v1.HealthCheckFiltersH\x00R\x07\x66ilters\x88\x01\x01\x42\n\n\x08_filters"I\n\x11GetHealthResponse\x12\x34\n\x06\x63hecks\x18\x01 \x03(\x0b\x32\x1c.chalk.server.v1.HealthCheckR\x06\x63hecks*u\n\x11HealthCheckStatus\x12#\n\x1fHEALTH_CHECK_STATUS_UNSPECIFIED\x10\x00\x12\x1a\n\x16HEALTH_CHECK_STATUS_OK\x10\x01\x12\x1f\n\x1bHEALTH_CHECK_STATUS_FAILING\x10\x02\x32\xcd\x01\n\rHealthService\x12`\n\x0b\x43heckHealth\x12#.chalk.server.v1.CheckHealthRequest\x1a$.chalk.server.v1.CheckHealthResponse"\x06\x90\x02\x01\x80}\x01\x12Z\n\tGetHealth\x12!.chalk.server.v1.GetHealthRequest\x1a".chalk.server.v1.GetHealthResponse"\x06\x90\x02\x01\x80}\x02\x42\x94\x01\n\x13\x63om.chalk.server.v1B\x0bStatusProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43SX\xaa\x02\x0f\x43halk.Server.V1\xca\x02\x0f\x43halk\\Server\\V1\xe2\x02\x1b\x43halk\\Server\\V1\\GPBMetadata\xea\x02\x11\x43halk::Server::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.server.v1.status_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.server.v1B\013StatusProtoP\001Z\022server/v1;serverv1\242\002\003CSX\252\002\017Chalk.Server.V1\312\002\017Chalk\\Server\\V1\342\002\033Chalk\\Server\\V1\\GPBMetadata\352\002\021Chalk::Server::V1"
    _globals["_HEALTHCHECK_METADATAENTRY"]._options = None
    _globals["_HEALTHCHECK_METADATAENTRY"]._serialized_options = b"8\001"
    _globals["_HEALTHSERVICE"].methods_by_name["CheckHealth"]._options = None
    _globals["_HEALTHSERVICE"].methods_by_name["CheckHealth"]._serialized_options = b"\220\002\001\200}\001"
    _globals["_HEALTHSERVICE"].methods_by_name["GetHealth"]._options = None
    _globals["_HEALTHSERVICE"].methods_by_name["GetHealth"]._serialized_options = b"\220\002\001\200}\002"
    _globals["_HEALTHCHECKSTATUS"]._serialized_start = 1015
    _globals["_HEALTHCHECKSTATUS"]._serialized_end = 1132
    _globals["_HEALTHCHECK"]._serialized_start = 145
    _globals["_HEALTHCHECK"]._serialized_end = 557
    _globals["_HEALTHCHECK_METADATAENTRY"]._serialized_start = 460
    _globals["_HEALTHCHECK_METADATAENTRY"]._serialized_end = 519
    _globals["_HEALTHCHECKFILTERS"]._serialized_start = 559
    _globals["_HEALTHCHECKFILTERS"]._serialized_end = 659
    _globals["_CHECKHEALTHREQUEST"]._serialized_start = 661
    _globals["_CHECKHEALTHREQUEST"]._serialized_end = 761
    _globals["_CHECKHEALTHRESPONSE"]._serialized_start = 763
    _globals["_CHECKHEALTHRESPONSE"]._serialized_end = 838
    _globals["_GETHEALTHREQUEST"]._serialized_start = 840
    _globals["_GETHEALTHREQUEST"]._serialized_end = 938
    _globals["_GETHEALTHRESPONSE"]._serialized_start = 940
    _globals["_GETHEALTHRESPONSE"]._serialized_end = 1013
    _globals["_HEALTHSERVICE"]._serialized_start = 1135
    _globals["_HEALTHSERVICE"]._serialized_end = 1340
# @@protoc_insertion_point(module_scope)
