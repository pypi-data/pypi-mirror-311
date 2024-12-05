# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from chalk._gen.chalk.server.v1 import team_pb2 as chalk_dot_server_dot_v1_dot_team__pb2


class TeamServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetEnv = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetEnv",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvResponse.FromString,
        )
        self.GetEnvironments = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetEnvironments",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvironmentsRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvironmentsResponse.FromString,
        )
        self.GetAgent = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetAgent",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAgentRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAgentResponse.FromString,
        )
        self.GetDisplayAgent = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetDisplayAgent",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetDisplayAgentRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetDisplayAgentResponse.FromString,
        )
        self.GetTeam = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetTeam",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamResponse.FromString,
        )
        self.CreateTeam = channel.unary_unary(
            "/chalk.server.v1.TeamService/CreateTeam",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateTeamRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateTeamResponse.FromString,
        )
        self.CreateProject = channel.unary_unary(
            "/chalk.server.v1.TeamService/CreateProject",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateProjectRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateProjectResponse.FromString,
        )
        self.CreateEnvironment = channel.unary_unary(
            "/chalk.server.v1.TeamService/CreateEnvironment",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateEnvironmentRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateEnvironmentResponse.FromString,
        )
        self.GetAvailablePermissions = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetAvailablePermissions",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAvailablePermissionsRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAvailablePermissionsResponse.FromString,
        )
        self.CreateServiceToken = channel.unary_unary(
            "/chalk.server.v1.TeamService/CreateServiceToken",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateServiceTokenRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateServiceTokenResponse.FromString,
        )
        self.DeleteServiceToken = channel.unary_unary(
            "/chalk.server.v1.TeamService/DeleteServiceToken",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.DeleteServiceTokenRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.DeleteServiceTokenResponse.FromString,
        )
        self.ListServiceTokens = channel.unary_unary(
            "/chalk.server.v1.TeamService/ListServiceTokens",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.ListServiceTokensRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.ListServiceTokensResponse.FromString,
        )
        self.UpdateServiceToken = channel.unary_unary(
            "/chalk.server.v1.TeamService/UpdateServiceToken",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateServiceTokenRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateServiceTokenResponse.FromString,
        )
        self.InviteTeamMember = channel.unary_unary(
            "/chalk.server.v1.TeamService/InviteTeamMember",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.InviteTeamMemberRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.InviteTeamMemberResponse.FromString,
        )
        self.ExpireTeamInvite = channel.unary_unary(
            "/chalk.server.v1.TeamService/ExpireTeamInvite",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.ExpireTeamInviteRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.ExpireTeamInviteResponse.FromString,
        )
        self.ListTeamInvites = channel.unary_unary(
            "/chalk.server.v1.TeamService/ListTeamInvites",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.ListTeamInvitesRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.ListTeamInvitesResponse.FromString,
        )
        self.UpsertFeaturePermissions = channel.unary_unary(
            "/chalk.server.v1.TeamService/UpsertFeaturePermissions",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.UpsertFeaturePermissionsRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.UpsertFeaturePermissionsResponse.FromString,
        )
        self.UpdateScimGroupSettings = channel.unary_unary(
            "/chalk.server.v1.TeamService/UpdateScimGroupSettings",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateScimGroupSettingsRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateScimGroupSettingsResponse.FromString,
        )
        self.GetTeamPermissions = channel.unary_unary(
            "/chalk.server.v1.TeamService/GetTeamPermissions",
            request_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamPermissionsRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamPermissionsResponse.FromString,
        )


class TeamServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetEnv(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetEnvironments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetAgent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetDisplayAgent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetTeam(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateTeam(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateProject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateEnvironment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetAvailablePermissions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateServiceToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteServiceToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListServiceTokens(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateServiceToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def InviteTeamMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ExpireTeamInvite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListTeamInvites(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpsertFeaturePermissions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateScimGroupSettings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetTeamPermissions(self, request, context):
        """rpc SetEnvironmentVariables(SetEnvironmentVariablesRequest) returns
        (SetEnvironmentVariablesResponse) {
        option (chalk.auth.v1.permission) = PERMISSION_DEPLOY_CREATE;
        }

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TeamServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetEnv": grpc.unary_unary_rpc_method_handler(
            servicer.GetEnv,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvResponse.SerializeToString,
        ),
        "GetEnvironments": grpc.unary_unary_rpc_method_handler(
            servicer.GetEnvironments,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvironmentsRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetEnvironmentsResponse.SerializeToString,
        ),
        "GetAgent": grpc.unary_unary_rpc_method_handler(
            servicer.GetAgent,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAgentRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAgentResponse.SerializeToString,
        ),
        "GetDisplayAgent": grpc.unary_unary_rpc_method_handler(
            servicer.GetDisplayAgent,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetDisplayAgentRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetDisplayAgentResponse.SerializeToString,
        ),
        "GetTeam": grpc.unary_unary_rpc_method_handler(
            servicer.GetTeam,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamResponse.SerializeToString,
        ),
        "CreateTeam": grpc.unary_unary_rpc_method_handler(
            servicer.CreateTeam,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateTeamRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateTeamResponse.SerializeToString,
        ),
        "CreateProject": grpc.unary_unary_rpc_method_handler(
            servicer.CreateProject,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateProjectRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateProjectResponse.SerializeToString,
        ),
        "CreateEnvironment": grpc.unary_unary_rpc_method_handler(
            servicer.CreateEnvironment,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateEnvironmentRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateEnvironmentResponse.SerializeToString,
        ),
        "GetAvailablePermissions": grpc.unary_unary_rpc_method_handler(
            servicer.GetAvailablePermissions,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAvailablePermissionsRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetAvailablePermissionsResponse.SerializeToString,
        ),
        "CreateServiceToken": grpc.unary_unary_rpc_method_handler(
            servicer.CreateServiceToken,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateServiceTokenRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.CreateServiceTokenResponse.SerializeToString,
        ),
        "DeleteServiceToken": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteServiceToken,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.DeleteServiceTokenRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.DeleteServiceTokenResponse.SerializeToString,
        ),
        "ListServiceTokens": grpc.unary_unary_rpc_method_handler(
            servicer.ListServiceTokens,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.ListServiceTokensRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.ListServiceTokensResponse.SerializeToString,
        ),
        "UpdateServiceToken": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateServiceToken,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateServiceTokenRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateServiceTokenResponse.SerializeToString,
        ),
        "InviteTeamMember": grpc.unary_unary_rpc_method_handler(
            servicer.InviteTeamMember,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.InviteTeamMemberRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.InviteTeamMemberResponse.SerializeToString,
        ),
        "ExpireTeamInvite": grpc.unary_unary_rpc_method_handler(
            servicer.ExpireTeamInvite,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.ExpireTeamInviteRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.ExpireTeamInviteResponse.SerializeToString,
        ),
        "ListTeamInvites": grpc.unary_unary_rpc_method_handler(
            servicer.ListTeamInvites,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.ListTeamInvitesRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.ListTeamInvitesResponse.SerializeToString,
        ),
        "UpsertFeaturePermissions": grpc.unary_unary_rpc_method_handler(
            servicer.UpsertFeaturePermissions,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.UpsertFeaturePermissionsRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.UpsertFeaturePermissionsResponse.SerializeToString,
        ),
        "UpdateScimGroupSettings": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateScimGroupSettings,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateScimGroupSettingsRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.UpdateScimGroupSettingsResponse.SerializeToString,
        ),
        "GetTeamPermissions": grpc.unary_unary_rpc_method_handler(
            servicer.GetTeamPermissions,
            request_deserializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamPermissionsRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_team__pb2.GetTeamPermissionsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("chalk.server.v1.TeamService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class TeamService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetEnv(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetEnv",
            chalk_dot_server_dot_v1_dot_team__pb2.GetEnvRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetEnvResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetEnvironments(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetEnvironments",
            chalk_dot_server_dot_v1_dot_team__pb2.GetEnvironmentsRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetEnvironmentsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetAgent(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetAgent",
            chalk_dot_server_dot_v1_dot_team__pb2.GetAgentRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetAgentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetDisplayAgent(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetDisplayAgent",
            chalk_dot_server_dot_v1_dot_team__pb2.GetDisplayAgentRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetDisplayAgentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetTeam(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetTeam",
            chalk_dot_server_dot_v1_dot_team__pb2.GetTeamRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetTeamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateTeam(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/CreateTeam",
            chalk_dot_server_dot_v1_dot_team__pb2.CreateTeamRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.CreateTeamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateProject(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/CreateProject",
            chalk_dot_server_dot_v1_dot_team__pb2.CreateProjectRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.CreateProjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateEnvironment(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/CreateEnvironment",
            chalk_dot_server_dot_v1_dot_team__pb2.CreateEnvironmentRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.CreateEnvironmentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetAvailablePermissions(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetAvailablePermissions",
            chalk_dot_server_dot_v1_dot_team__pb2.GetAvailablePermissionsRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetAvailablePermissionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateServiceToken(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/CreateServiceToken",
            chalk_dot_server_dot_v1_dot_team__pb2.CreateServiceTokenRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.CreateServiceTokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def DeleteServiceToken(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/DeleteServiceToken",
            chalk_dot_server_dot_v1_dot_team__pb2.DeleteServiceTokenRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.DeleteServiceTokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ListServiceTokens(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/ListServiceTokens",
            chalk_dot_server_dot_v1_dot_team__pb2.ListServiceTokensRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.ListServiceTokensResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateServiceToken(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/UpdateServiceToken",
            chalk_dot_server_dot_v1_dot_team__pb2.UpdateServiceTokenRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.UpdateServiceTokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def InviteTeamMember(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/InviteTeamMember",
            chalk_dot_server_dot_v1_dot_team__pb2.InviteTeamMemberRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.InviteTeamMemberResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ExpireTeamInvite(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/ExpireTeamInvite",
            chalk_dot_server_dot_v1_dot_team__pb2.ExpireTeamInviteRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.ExpireTeamInviteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ListTeamInvites(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/ListTeamInvites",
            chalk_dot_server_dot_v1_dot_team__pb2.ListTeamInvitesRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.ListTeamInvitesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpsertFeaturePermissions(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/UpsertFeaturePermissions",
            chalk_dot_server_dot_v1_dot_team__pb2.UpsertFeaturePermissionsRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.UpsertFeaturePermissionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateScimGroupSettings(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/UpdateScimGroupSettings",
            chalk_dot_server_dot_v1_dot_team__pb2.UpdateScimGroupSettingsRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.UpdateScimGroupSettingsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetTeamPermissions(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.TeamService/GetTeamPermissions",
            chalk_dot_server_dot_v1_dot_team__pb2.GetTeamPermissionsRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_team__pb2.GetTeamPermissionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
