# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/server/v1/named_query.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.auth.v1 import permissions_pb2 as chalk_dot_auth_dot_v1_dot_permissions__pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as chalk_dot_graph_dot_v1_dot_graph__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n!chalk/server/v1/named_query.proto\x12\x0f\x63halk.server.v1\x1a\x1f\x63halk/auth/v1/permissions.proto\x1a\x1a\x63halk/graph/v1/graph.proto"@\n\x19GetAllNamedQueriesRequest\x12#\n\rdeployment_id\x18\x01 \x01(\tR\x0c\x64\x65ploymentId"0\n\x1aGetNamedQueryByNameRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name"^\n\x1bGetNamedQueryByNameResponse\x12?\n\rnamed_queries\x18\x01 \x03(\x0b\x32\x1a.chalk.graph.v1.NamedQueryR\x0cnamedQueries"]\n\x1aGetAllNamedQueriesResponse\x12?\n\rnamed_queries\x18\x01 \x03(\x0b\x32\x1a.chalk.graph.v1.NamedQueryR\x0cnamedQueries"+\n)GetAllNamedQueriesActiveDeploymentRequest"m\n*GetAllNamedQueriesActiveDeploymentResponse\x12?\n\rnamed_queries\x18\x01 \x03(\x0b\x32\x1a.chalk.graph.v1.NamedQueryR\x0cnamedQueries2\xac\x03\n\x11NamedQueryService\x12u\n\x12GetAllNamedQueries\x12*.chalk.server.v1.GetAllNamedQueriesRequest\x1a+.chalk.server.v1.GetAllNamedQueriesResponse"\x06\x90\x02\x01\x80}\x0b\x12\xa5\x01\n"GetAllNamedQueriesActiveDeployment\x12:.chalk.server.v1.GetAllNamedQueriesActiveDeploymentRequest\x1a;.chalk.server.v1.GetAllNamedQueriesActiveDeploymentResponse"\x06\x90\x02\x01\x80}\x0b\x12x\n\x13GetNamedQueryByName\x12+.chalk.server.v1.GetNamedQueryByNameRequest\x1a,.chalk.server.v1.GetNamedQueryByNameResponse"\x06\x90\x02\x01\x80}\x0b\x42\x98\x01\n\x13\x63om.chalk.server.v1B\x0fNamedQueryProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43SX\xaa\x02\x0f\x43halk.Server.V1\xca\x02\x0f\x43halk\\Server\\V1\xe2\x02\x1b\x43halk\\Server\\V1\\GPBMetadata\xea\x02\x11\x43halk::Server::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.server.v1.named_query_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.server.v1B\017NamedQueryProtoP\001Z\022server/v1;serverv1\242\002\003CSX\252\002\017Chalk.Server.V1\312\002\017Chalk\\Server\\V1\342\002\033Chalk\\Server\\V1\\GPBMetadata\352\002\021Chalk::Server::V1"
    _globals["_NAMEDQUERYSERVICE"].methods_by_name["GetAllNamedQueries"]._options = None
    _globals["_NAMEDQUERYSERVICE"].methods_by_name["GetAllNamedQueries"]._serialized_options = b"\220\002\001\200}\013"
    _globals["_NAMEDQUERYSERVICE"].methods_by_name["GetAllNamedQueriesActiveDeployment"]._options = None
    _globals["_NAMEDQUERYSERVICE"].methods_by_name[
        "GetAllNamedQueriesActiveDeployment"
    ]._serialized_options = b"\220\002\001\200}\013"
    _globals["_NAMEDQUERYSERVICE"].methods_by_name["GetNamedQueryByName"]._options = None
    _globals["_NAMEDQUERYSERVICE"].methods_by_name["GetNamedQueryByName"]._serialized_options = b"\220\002\001\200}\013"
    _globals["_GETALLNAMEDQUERIESREQUEST"]._serialized_start = 115
    _globals["_GETALLNAMEDQUERIESREQUEST"]._serialized_end = 179
    _globals["_GETNAMEDQUERYBYNAMEREQUEST"]._serialized_start = 181
    _globals["_GETNAMEDQUERYBYNAMEREQUEST"]._serialized_end = 229
    _globals["_GETNAMEDQUERYBYNAMERESPONSE"]._serialized_start = 231
    _globals["_GETNAMEDQUERYBYNAMERESPONSE"]._serialized_end = 325
    _globals["_GETALLNAMEDQUERIESRESPONSE"]._serialized_start = 327
    _globals["_GETALLNAMEDQUERIESRESPONSE"]._serialized_end = 420
    _globals["_GETALLNAMEDQUERIESACTIVEDEPLOYMENTREQUEST"]._serialized_start = 422
    _globals["_GETALLNAMEDQUERIESACTIVEDEPLOYMENTREQUEST"]._serialized_end = 465
    _globals["_GETALLNAMEDQUERIESACTIVEDEPLOYMENTRESPONSE"]._serialized_start = 467
    _globals["_GETALLNAMEDQUERIESACTIVEDEPLOYMENTRESPONSE"]._serialized_end = 576
    _globals["_NAMEDQUERYSERVICE"]._serialized_start = 579
    _globals["_NAMEDQUERYSERVICE"]._serialized_end = 1007
# @@protoc_insertion_point(module_scope)
