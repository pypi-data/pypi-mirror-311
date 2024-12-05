# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/server/v1/environment.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n!chalk/server/v1/environment.proto\x12\x0f\x63halk.server.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto"S\n\x13\x41WSCloudWatchConfig\x12)\n\x0elog_group_path\x18\x01 \x01(\tH\x00R\x0clogGroupPath\x88\x01\x01\x42\x11\n\x0f_log_group_path"\xab\x02\n\x16\x41WSSecretManagerConfig\x12)\n\x0esecret_kms_arn\x18\x01 \x01(\tH\x00R\x0csecretKmsArn\x88\x01\x01\x12X\n\x0bsecret_tags\x18\x02 \x03(\x0b\x32\x37.chalk.server.v1.AWSSecretManagerConfig.SecretTagsEntryR\nsecretTags\x12(\n\rsecret_prefix\x18\x03 \x01(\tH\x01R\x0csecretPrefix\x88\x01\x01\x1a=\n\x0fSecretTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x11\n\x0f_secret_kms_arnB\x10\n\x0e_secret_prefix"\xad\x01\n\x13GCPWorkloadIdentity\x12,\n\x12gcp_project_number\x18\x01 \x01(\tR\x10gcpProjectNumber\x12.\n\x13gcp_service_account\x18\x02 \x01(\tR\x11gcpServiceAccount\x12\x17\n\x07pool_id\x18\x03 \x01(\tR\x06poolId\x12\x1f\n\x0bprovider_id\x18\x04 \x01(\tR\nproviderId"\x88\x02\n\x11\x44ockerBuildConfig\x12\x18\n\x07\x62uilder\x18\x01 \x01(\tR\x07\x62uilder\x12,\n\x12push_registry_type\x18\x02 \x01(\tR\x10pushRegistryType\x12\x37\n\x18push_registry_tag_prefix\x18\x03 \x01(\tR\x15pushRegistryTagPrefix\x12\x43\n\x1eregistry_credentials_secret_id\x18\x04 \x01(\tR\x1bregistryCredentialsSecretId\x12-\n\x12notification_topic\x18\x05 \x01(\tR\x11notificationTopic"l\n\x16\x45lasticsearchLogConfig\x12\x1a\n\x08username\x18\x01 \x01(\tR\x08username\x12\x1a\n\x08password\x18\x02 \x01(\tR\x08password\x12\x1a\n\x08\x65ndpoint\x18\x03 \x01(\tR\x08\x65ndpoint"\xa7\x07\n\x0e\x41WSCloudConfig\x12\x1d\n\naccount_id\x18\x01 \x01(\tR\taccountId\x12.\n\x13management_role_arn\x18\x02 \x01(\tR\x11managementRoleArn\x12\x16\n\x06region\x18\x03 \x01(\tR\x06region\x12$\n\x0b\x65xternal_id\x18\x04 \x01(\tH\x00R\nexternalId\x88\x01\x01\x12k\n\x1d\x64\x65precated_cloud_watch_config\x18\x05 \x01(\x0b\x32$.chalk.server.v1.AWSCloudWatchConfigB\x02\x18\x01R\x1a\x64\x65precatedCloudWatchConfig\x12t\n deprecated_secret_manager_config\x18\x06 \x01(\x0b\x32\'.chalk.server.v1.AWSSecretManagerConfigB\x02\x18\x01R\x1d\x64\x65precatedSecretManagerConfig\x12U\n\x11workload_identity\x18\x07 \x01(\x0b\x32$.chalk.server.v1.GCPWorkloadIdentityB\x02\x18\x01R\x10workloadIdentity\x12R\n\x13\x64ocker_build_config\x18\x08 \x01(\x0b\x32".chalk.server.v1.DockerBuildConfigR\x11\x64ockerBuildConfig\x12\x61\n\x18\x65lasticsearch_log_config\x18\t \x01(\x0b\x32\'.chalk.server.v1.ElasticsearchLogConfigR\x16\x65lasticsearchLogConfig\x12Q\n\x11\x63loudwatch_config\x18\n \x01(\x0b\x32$.chalk.server.v1.AWSCloudWatchConfigR\x10\x63loudwatchConfig\x12Z\n\x14secretmanager_config\x18\x0b \x01(\x0b\x32\'.chalk.server.v1.AWSSecretManagerConfigR\x13secretmanagerConfig\x12X\n\x15gcp_workload_identity\x18\x0c \x01(\x0b\x32$.chalk.server.v1.GCPWorkloadIdentityR\x13gcpWorkloadIdentityB\x0e\n\x0c_external_id"\xfd\x01\n\x0eGCPCloudConfig\x12\x1d\n\nproject_id\x18\x01 \x01(\tR\tprojectId\x12\x16\n\x06region\x18\x02 \x01(\tR\x06region\x12\x41\n\x1amanagement_service_account\x18\x03 \x01(\tH\x00R\x18managementServiceAccount\x88\x01\x01\x12R\n\x13\x64ocker_build_config\x18\x04 \x01(\x0b\x32".chalk.server.v1.DockerBuildConfigR\x11\x64ockerBuildConfigB\x1d\n\x1b_management_service_account"\x81\x01\n\x0b\x43loudConfig\x12\x33\n\x03\x61ws\x18\x01 \x01(\x0b\x32\x1f.chalk.server.v1.AWSCloudConfigH\x00R\x03\x61ws\x12\x33\n\x03gcp\x18\x02 \x01(\x0b\x32\x1f.chalk.server.v1.GCPCloudConfigH\x00R\x03gcpB\x08\n\x06\x63onfig"\xa7\x01\n\x1e\x45nvironmentObjectStorageConfig\x12%\n\x0e\x64\x61taset_bucket\x18\x01 \x01(\tR\rdatasetBucket\x12,\n\x12plan_stages_bucket\x18\x02 \x01(\tR\x10planStagesBucket\x12\x30\n\x14source_bundle_bucket\x18\x03 \x01(\tR\x12sourceBundleBucket"\x83!\n\x0b\x45nvironment\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x1d\n\nproject_id\x18\x02 \x01(\tR\tprojectId\x12\x0e\n\x02id\x18\x03 \x01(\tR\x02id\x12\x17\n\x07team_id\x18\x04 \x01(\tR\x06teamId\x12\x35\n\x14\x61\x63tive_deployment_id\x18\x05 \x01(\tH\x00R\x12\x61\x63tiveDeploymentId\x88\x01\x01\x12"\n\nworker_url\x18\x06 \x01(\tH\x01R\tworkerUrl\x88\x01\x01\x12$\n\x0bservice_url\x18\x07 \x01(\tH\x02R\nserviceUrl\x88\x01\x01\x12"\n\nbranch_url\x18\x08 \x01(\tH\x03R\tbranchUrl\x88\x01\x01\x12\x35\n\x14offline_store_secret\x18\t \x01(\tH\x04R\x12offlineStoreSecret\x88\x01\x01\x12\x33\n\x13online_store_secret\x18\n \x01(\tH\x05R\x11onlineStoreSecret\x88\x01\x01\x12\x35\n\x14\x66\x65\x61ture_store_secret\x18\x0b \x01(\tH\x06R\x12\x66\x65\x61tureStoreSecret\x88\x01\x01\x12,\n\x0fpostgres_secret\x18\x0c \x01(\tH\x07R\x0epostgresSecret\x88\x01\x01\x12/\n\x11online_store_kind\x18\r \x01(\tH\x08R\x0fonlineStoreKind\x88\x01\x01\x12\x1c\n\x07\x65mq_uri\x18\x0e \x01(\tH\tR\x06\x65mqUri\x88\x01\x01\x12\x31\n\x12vpc_connector_name\x18\x0f \x01(\tH\nR\x10vpcConnectorName\x88\x01\x01\x12/\n\x11kube_cluster_name\x18\x10 \x01(\tH\x0bR\x0fkubeClusterName\x88\x01\x01\x12<\n\x18\x62ranch_kube_cluster_name\x18\x11 \x01(\tH\x0cR\x15\x62ranchKubeClusterName\x88\x01\x01\x12<\n\x18\x65ngine_kube_cluster_name\x18\x12 \x01(\tH\rR\x15\x65ngineKubeClusterName\x88\x01\x01\x12I\n\x1fshadow_engine_kube_cluster_name\x18\x13 \x01(\tH\x0eR\x1bshadowEngineKubeClusterName\x88\x01\x01\x12\x31\n\x12kube_job_namespace\x18\x14 \x01(\tH\x0fR\x10kubeJobNamespace\x88\x01\x01\x12\x39\n\x16kube_preview_namespace\x18\x15 \x01(\tH\x10R\x14kubePreviewNamespace\x88\x01\x01\x12>\n\x19kube_service_account_name\x18\x16 \x01(\tH\x11R\x16kubeServiceAccountName\x88\x01\x01\x12\x42\n\x1bstreaming_query_service_uri\x18\x17 \x01(\tH\x12R\x18streamingQueryServiceUri\x88\x01\x01\x12`\n.skip_offline_writes_for_online_cached_features\x18\x18 \x01(\x08R(skipOfflineWritesForOnlineCachedFeatures\x12-\n\x10result_bus_topic\x18\x19 \x01(\tH\x13R\x0eresultBusTopic\x88\x01\x01\x12;\n\x17online_persistence_mode\x18\x1a \x01(\tH\x14R\x15onlinePersistenceMode\x88\x01\x01\x12/\n\x11metrics_bus_topic\x18\x1b \x01(\tH\x15R\x0fmetricsBusTopic\x88\x01\x01\x12\x39\n\x16\x62igtable_instance_name\x18\x1c \x01(\tH\x16R\x14\x62igtableInstanceName\x88\x01\x01\x12\x33\n\x13\x62igtable_table_name\x18\x1d \x01(\tH\x17R\x11\x62igtableTableName\x88\x01\x01\x12\x37\n\x15\x63loud_account_locator\x18\x1e \x01(\tH\x18R\x13\x63loudAccountLocator\x88\x01\x01\x12&\n\x0c\x63loud_region\x18\x1f \x01(\tH\x19R\x0b\x63loudRegion\x88\x01\x01\x12-\n\x10\x63loud_tenancy_id\x18  \x01(\tH\x1aR\x0e\x63loudTenancyId\x88\x01\x01\x12\x35\n\x14source_bundle_bucket\x18! \x01(\tH\x1bR\x12sourceBundleBucket\x88\x01\x01\x12\x42\n\x1b\x65ngine_docker_registry_path\x18" \x01(\tH\x1cR\x18\x65ngineDockerRegistryPath\x88\x01\x01\x12,\n\x0f\x64\x65\x66\x61ult_planner\x18# \x01(\tH\x1dR\x0e\x64\x65\x66\x61ultPlanner\x88\x01\x01\x12\x63\n\x13\x61\x64\x64itional_env_vars\x18$ \x03(\x0b\x32\x33.chalk.server.v1.Environment.AdditionalEnvVarsEntryR\x11\x61\x64\x64itionalEnvVars\x12p\n\x18\x61\x64\x64itional_cron_env_vars\x18% \x03(\x0b\x32\x37.chalk.server.v1.Environment.AdditionalCronEnvVarsEntryR\x15\x61\x64\x64itionalCronEnvVars\x12=\n\x18private_pip_repositories\x18& \x01(\tH\x1eR\x16privatePipRepositories\x88\x01\x01\x12\x1d\n\nis_sandbox\x18\' \x01(\x08R\tisSandbox\x12I\n\x0e\x63loud_provider\x18) \x01(\x0e\x32".chalk.server.v1.CloudProviderKindR\rcloudProvider\x12\x44\n\x0c\x63loud_config\x18* \x01(\x0b\x32\x1c.chalk.server.v1.CloudConfigH\x1fR\x0b\x63loudConfig\x88\x01\x01\x12Z\n\x10spec_config_json\x18( \x03(\x0b\x32\x30.chalk.server.v1.Environment.SpecConfigJsonEntryR\x0especConfigJson\x12@\n\x0b\x61rchived_at\x18+ \x01(\x0b\x32\x1a.google.protobuf.TimestampH R\narchivedAt\x88\x01\x01\x12S\n$metadata_server_metrics_store_secret\x18, \x01(\tH!R metadataServerMetricsStoreSecret\x88\x01\x01\x12M\n!query_server_metrics_store_secret\x18- \x01(\tH"R\x1dqueryServerMetricsStoreSecret\x88\x01\x01\x12/\n\x11pinned_base_image\x18. \x01(\tH#R\x0fpinnedBaseImage\x88\x01\x01\x12\x31\n\x12\x63luster_gateway_id\x18/ \x01(\tH$R\x10\x63lusterGatewayId\x88\x01\x01\x12\x39\n\x16\x63luster_timescaledb_id\x18\x30 \x01(\tH%R\x14\x63lusterTimescaledbId\x88\x01\x01\x12T\n$background_persistence_deployment_id\x18\x31 \x01(\tH&R!backgroundPersistenceDeploymentId\x88\x01\x01\x12\x65\n\x13\x65nvironment_buckets\x18\x32 \x01(\x0b\x32/.chalk.server.v1.EnvironmentObjectStorageConfigH\'R\x12\x65nvironmentBuckets\x88\x01\x01\x12\x41\n\x1a\x63luster_timescaledb_secret\x18\x33 \x01(\tH(R\x18\x63lusterTimescaledbSecret\x88\x01\x01\x1a\x44\n\x16\x41\x64\x64itionalEnvVarsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1aH\n\x1a\x41\x64\x64itionalCronEnvVarsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1aY\n\x13SpecConfigJsonEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.ValueR\x05value:\x02\x38\x01\x42\x17\n\x15_active_deployment_idB\r\n\x0b_worker_urlB\x0e\n\x0c_service_urlB\r\n\x0b_branch_urlB\x17\n\x15_offline_store_secretB\x16\n\x14_online_store_secretB\x17\n\x15_feature_store_secretB\x12\n\x10_postgres_secretB\x14\n\x12_online_store_kindB\n\n\x08_emq_uriB\x15\n\x13_vpc_connector_nameB\x14\n\x12_kube_cluster_nameB\x1b\n\x19_branch_kube_cluster_nameB\x1b\n\x19_engine_kube_cluster_nameB"\n _shadow_engine_kube_cluster_nameB\x15\n\x13_kube_job_namespaceB\x19\n\x17_kube_preview_namespaceB\x1c\n\x1a_kube_service_account_nameB\x1e\n\x1c_streaming_query_service_uriB\x13\n\x11_result_bus_topicB\x1a\n\x18_online_persistence_modeB\x14\n\x12_metrics_bus_topicB\x19\n\x17_bigtable_instance_nameB\x16\n\x14_bigtable_table_nameB\x18\n\x16_cloud_account_locatorB\x0f\n\r_cloud_regionB\x13\n\x11_cloud_tenancy_idB\x17\n\x15_source_bundle_bucketB\x1e\n\x1c_engine_docker_registry_pathB\x12\n\x10_default_plannerB\x1b\n\x19_private_pip_repositoriesB\x0f\n\r_cloud_configB\x0e\n\x0c_archived_atB\'\n%_metadata_server_metrics_store_secretB$\n"_query_server_metrics_store_secretB\x14\n\x12_pinned_base_imageB\x15\n\x13_cluster_gateway_idB\x19\n\x17_cluster_timescaledb_idB\'\n%_background_persistence_deployment_idB\x16\n\x14_environment_bucketsB\x1d\n\x1b_cluster_timescaledb_secret*\x93\x01\n\x11\x43loudProviderKind\x12#\n\x1f\x43LOUD_PROVIDER_KIND_UNSPECIFIED\x10\x00\x12\x1f\n\x1b\x43LOUD_PROVIDER_KIND_UNKNOWN\x10\x01\x12\x1b\n\x17\x43LOUD_PROVIDER_KIND_GCP\x10\x02\x12\x1b\n\x17\x43LOUD_PROVIDER_KIND_AWS\x10\x03\x42\x99\x01\n\x13\x63om.chalk.server.v1B\x10\x45nvironmentProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43SX\xaa\x02\x0f\x43halk.Server.V1\xca\x02\x0f\x43halk\\Server\\V1\xe2\x02\x1b\x43halk\\Server\\V1\\GPBMetadata\xea\x02\x11\x43halk::Server::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.server.v1.environment_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.server.v1B\020EnvironmentProtoP\001Z\022server/v1;serverv1\242\002\003CSX\252\002\017Chalk.Server.V1\312\002\017Chalk\\Server\\V1\342\002\033Chalk\\Server\\V1\\GPBMetadata\352\002\021Chalk::Server::V1"
    _globals["_AWSSECRETMANAGERCONFIG_SECRETTAGSENTRY"]._options = None
    _globals["_AWSSECRETMANAGERCONFIG_SECRETTAGSENTRY"]._serialized_options = b"8\001"
    _globals["_AWSCLOUDCONFIG"].fields_by_name["deprecated_cloud_watch_config"]._options = None
    _globals["_AWSCLOUDCONFIG"].fields_by_name["deprecated_cloud_watch_config"]._serialized_options = b"\030\001"
    _globals["_AWSCLOUDCONFIG"].fields_by_name["deprecated_secret_manager_config"]._options = None
    _globals["_AWSCLOUDCONFIG"].fields_by_name["deprecated_secret_manager_config"]._serialized_options = b"\030\001"
    _globals["_AWSCLOUDCONFIG"].fields_by_name["workload_identity"]._options = None
    _globals["_AWSCLOUDCONFIG"].fields_by_name["workload_identity"]._serialized_options = b"\030\001"
    _globals["_ENVIRONMENT_ADDITIONALENVVARSENTRY"]._options = None
    _globals["_ENVIRONMENT_ADDITIONALENVVARSENTRY"]._serialized_options = b"8\001"
    _globals["_ENVIRONMENT_ADDITIONALCRONENVVARSENTRY"]._options = None
    _globals["_ENVIRONMENT_ADDITIONALCRONENVVARSENTRY"]._serialized_options = b"8\001"
    _globals["_ENVIRONMENT_SPECCONFIGJSONENTRY"]._options = None
    _globals["_ENVIRONMENT_SPECCONFIGJSONENTRY"]._serialized_options = b"8\001"
    _globals["_CLOUDPROVIDERKIND"]._serialized_start = 6784
    _globals["_CLOUDPROVIDERKIND"]._serialized_end = 6931
    _globals["_AWSCLOUDWATCHCONFIG"]._serialized_start = 117
    _globals["_AWSCLOUDWATCHCONFIG"]._serialized_end = 200
    _globals["_AWSSECRETMANAGERCONFIG"]._serialized_start = 203
    _globals["_AWSSECRETMANAGERCONFIG"]._serialized_end = 502
    _globals["_AWSSECRETMANAGERCONFIG_SECRETTAGSENTRY"]._serialized_start = 404
    _globals["_AWSSECRETMANAGERCONFIG_SECRETTAGSENTRY"]._serialized_end = 465
    _globals["_GCPWORKLOADIDENTITY"]._serialized_start = 505
    _globals["_GCPWORKLOADIDENTITY"]._serialized_end = 678
    _globals["_DOCKERBUILDCONFIG"]._serialized_start = 681
    _globals["_DOCKERBUILDCONFIG"]._serialized_end = 945
    _globals["_ELASTICSEARCHLOGCONFIG"]._serialized_start = 947
    _globals["_ELASTICSEARCHLOGCONFIG"]._serialized_end = 1055
    _globals["_AWSCLOUDCONFIG"]._serialized_start = 1058
    _globals["_AWSCLOUDCONFIG"]._serialized_end = 1993
    _globals["_GCPCLOUDCONFIG"]._serialized_start = 1996
    _globals["_GCPCLOUDCONFIG"]._serialized_end = 2249
    _globals["_CLOUDCONFIG"]._serialized_start = 2252
    _globals["_CLOUDCONFIG"]._serialized_end = 2381
    _globals["_ENVIRONMENTOBJECTSTORAGECONFIG"]._serialized_start = 2384
    _globals["_ENVIRONMENTOBJECTSTORAGECONFIG"]._serialized_end = 2551
    _globals["_ENVIRONMENT"]._serialized_start = 2554
    _globals["_ENVIRONMENT"]._serialized_end = 6781
    _globals["_ENVIRONMENT_ADDITIONALENVVARSENTRY"]._serialized_start = 5526
    _globals["_ENVIRONMENT_ADDITIONALENVVARSENTRY"]._serialized_end = 5594
    _globals["_ENVIRONMENT_ADDITIONALCRONENVVARSENTRY"]._serialized_start = 5596
    _globals["_ENVIRONMENT_ADDITIONALCRONENVVARSENTRY"]._serialized_end = 5668
    _globals["_ENVIRONMENT_SPECCONFIGJSONENTRY"]._serialized_start = 5670
    _globals["_ENVIRONMENT_SPECCONFIGJSONENTRY"]._serialized_end = 5759
# @@protoc_insertion_point(module_scope)
