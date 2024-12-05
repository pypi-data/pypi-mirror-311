# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: api-contracts/workflows/workflows.proto
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
    'api-contracts/workflows/workflows.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'api-contracts/workflows/workflows.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"D\n\x12PutWorkflowRequest\x12.\n\x04opts\x18\x01 \x01(\x0b\x32\x1a.CreateWorkflowVersionOptsR\x04opts\"\xe7\x05\n\x19\x43reateWorkflowVersionOpts\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription\x12\x18\n\x07version\x18\x03 \x01(\tR\x07version\x12%\n\x0e\x65vent_triggers\x18\x04 \x03(\tR\reventTriggers\x12#\n\rcron_triggers\x18\x05 \x03(\tR\x0c\x63ronTriggers\x12I\n\x12scheduled_triggers\x18\x06 \x03(\x0b\x32\x1a.google.protobuf.TimestampR\x11scheduledTriggers\x12*\n\x04jobs\x18\x07 \x03(\x0b\x32\x16.CreateWorkflowJobOptsR\x04jobs\x12:\n\x0b\x63oncurrency\x18\x08 \x01(\x0b\x32\x18.WorkflowConcurrencyOptsR\x0b\x63oncurrency\x12.\n\x10schedule_timeout\x18\t \x01(\tH\x00R\x0fscheduleTimeout\x88\x01\x01\x12\"\n\ncron_input\x18\n \x01(\tH\x01R\tcronInput\x88\x01\x01\x12\x41\n\x0eon_failure_job\x18\x0b \x01(\x0b\x32\x16.CreateWorkflowJobOptsH\x02R\x0conFailureJob\x88\x01\x01\x12,\n\x06sticky\x18\x0c \x01(\x0e\x32\x0f.StickyStrategyH\x03R\x06sticky\x88\x01\x01\x12&\n\x04kind\x18\r \x01(\x0e\x32\r.WorkflowKindH\x04R\x04kind\x88\x01\x01\x12.\n\x10\x64\x65\x66\x61ult_priority\x18\x0e \x01(\x05H\x05R\x0f\x64\x65\x66\x61ultPriority\x88\x01\x01\x42\x13\n\x11_schedule_timeoutB\r\n\x0b_cron_inputB\x11\n\x0f_on_failure_jobB\t\n\x07_stickyB\x07\n\x05_kindB\x13\n\x11_default_priority\"\xfc\x01\n\x17WorkflowConcurrencyOpts\x12\x1b\n\x06\x61\x63tion\x18\x01 \x01(\tH\x00R\x06\x61\x63tion\x88\x01\x01\x12\x1e\n\x08max_runs\x18\x02 \x01(\x05H\x01R\x07maxRuns\x88\x01\x01\x12\x45\n\x0elimit_strategy\x18\x03 \x01(\x0e\x32\x19.ConcurrencyLimitStrategyH\x02R\rlimitStrategy\x88\x01\x01\x12#\n\nexpression\x18\x04 \x01(\tH\x03R\nexpression\x88\x01\x01\x42\t\n\x07_actionB\x0b\n\t_max_runsB\x11\n\x0f_limit_strategyB\r\n\x0b_expression\"\x82\x01\n\x15\x43reateWorkflowJobOpts\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription\x12-\n\x05steps\x18\x04 \x03(\x0b\x32\x17.CreateWorkflowStepOptsR\x05stepsJ\x04\x08\x03\x10\x04\"\x93\x02\n\x13\x44\x65siredWorkerLabels\x12\x1f\n\x08strValue\x18\x01 \x01(\tH\x00R\x08strValue\x88\x01\x01\x12\x1f\n\x08intValue\x18\x02 \x01(\x05H\x01R\x08intValue\x88\x01\x01\x12\x1f\n\x08required\x18\x03 \x01(\x08H\x02R\x08required\x88\x01\x01\x12;\n\ncomparator\x18\x04 \x01(\x0e\x32\x16.WorkerLabelComparatorH\x03R\ncomparator\x88\x01\x01\x12\x1b\n\x06weight\x18\x05 \x01(\x05H\x04R\x06weight\x88\x01\x01\x42\x0b\n\t_strValueB\x0b\n\t_intValueB\x0b\n\t_requiredB\r\n\x0b_comparatorB\t\n\x07_weight\"\xb2\x03\n\x16\x43reateWorkflowStepOpts\x12\x1f\n\x0breadable_id\x18\x01 \x01(\tR\nreadableId\x12\x16\n\x06\x61\x63tion\x18\x02 \x01(\tR\x06\x61\x63tion\x12\x18\n\x07timeout\x18\x03 \x01(\tR\x07timeout\x12\x16\n\x06inputs\x18\x04 \x01(\tR\x06inputs\x12\x18\n\x07parents\x18\x05 \x03(\tR\x07parents\x12\x1b\n\tuser_data\x18\x06 \x01(\tR\x08userData\x12\x18\n\x07retries\x18\x07 \x01(\x05R\x07retries\x12\x35\n\x0brate_limits\x18\x08 \x03(\x0b\x32\x14.CreateStepRateLimitR\nrateLimits\x12N\n\rworker_labels\x18\t \x03(\x0b\x32).CreateWorkflowStepOpts.WorkerLabelsEntryR\x0cworkerLabels\x1aU\n\x11WorkerLabelsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x14.DesiredWorkerLabelsR\x05value:\x02\x38\x01\"\xb5\x02\n\x13\x43reateStepRateLimit\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x19\n\x05units\x18\x02 \x01(\x05H\x00R\x05units\x88\x01\x01\x12\x1e\n\x08key_expr\x18\x03 \x01(\tH\x01R\x07keyExpr\x88\x01\x01\x12\"\n\nunits_expr\x18\x04 \x01(\tH\x02R\tunitsExpr\x88\x01\x01\x12/\n\x11limit_values_expr\x18\x05 \x01(\tH\x03R\x0flimitValuesExpr\x88\x01\x01\x12\x33\n\x08\x64uration\x18\x06 \x01(\x0e\x32\x12.RateLimitDurationH\x04R\x08\x64uration\x88\x01\x01\x42\x08\n\x06_unitsB\x0b\n\t_key_exprB\r\n\x0b_units_exprB\x14\n\x12_limit_values_exprB\x0b\n\t_duration\"\x16\n\x14ListWorkflowsRequest\"\xaa\x03\n\x17ScheduleWorkflowRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x38\n\tschedules\x18\x02 \x03(\x0b\x32\x1a.google.protobuf.TimestampR\tschedules\x12\x14\n\x05input\x18\x03 \x01(\tR\x05input\x12 \n\tparent_id\x18\x04 \x01(\tH\x00R\x08parentId\x88\x01\x01\x12\x30\n\x12parent_step_run_id\x18\x05 \x01(\tH\x01R\x0fparentStepRunId\x88\x01\x01\x12$\n\x0b\x63hild_index\x18\x06 \x01(\x05H\x02R\nchildIndex\x88\x01\x01\x12 \n\tchild_key\x18\x07 \x01(\tH\x03R\x08\x63hildKey\x88\x01\x01\x12\x34\n\x13\x61\x64\x64itional_metadata\x18\x08 \x01(\tH\x04R\x12\x61\x64\x64itionalMetadata\x88\x01\x01\x42\x0c\n\n_parent_idB\x15\n\x13_parent_step_run_idB\x0e\n\x0c_child_indexB\x0c\n\n_child_keyB\x16\n\x14_additional_metadata\"^\n\x11ScheduledWorkflow\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x39\n\ntrigger_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ttriggerAt\"\xad\x02\n\x0fWorkflowVersion\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x39\n\ncreated_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\nupdated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tupdatedAt\x12\x18\n\x07version\x18\x05 \x01(\tR\x07version\x12\x14\n\x05order\x18\x06 \x01(\x03R\x05order\x12\x1f\n\x0bworkflow_id\x18\x07 \x01(\tR\nworkflowId\x12\x43\n\x13scheduled_workflows\x18\x08 \x03(\x0b\x32\x12.ScheduledWorkflowR\x12scheduledWorkflows\"S\n\x17WorkflowTriggerEventRef\x12\x1b\n\tparent_id\x18\x01 \x01(\tR\x08parentId\x12\x1b\n\tevent_key\x18\x02 \x01(\tR\x08\x65ventKey\"I\n\x16WorkflowTriggerCronRef\x12\x1b\n\tparent_id\x18\x01 \x01(\tR\x08parentId\x12\x12\n\x04\x63ron\x18\x02 \x01(\tR\x04\x63ron\"S\n\x1a\x42ulkTriggerWorkflowRequest\x12\x35\n\tworkflows\x18\x01 \x03(\x0b\x32\x17.TriggerWorkflowRequestR\tworkflows\"G\n\x1b\x42ulkTriggerWorkflowResponse\x12(\n\x10workflow_run_ids\x18\x01 \x03(\tR\x0eworkflowRunIds\"\xe4\x03\n\x16TriggerWorkflowRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x14\n\x05input\x18\x02 \x01(\tR\x05input\x12 \n\tparent_id\x18\x03 \x01(\tH\x00R\x08parentId\x88\x01\x01\x12\x30\n\x12parent_step_run_id\x18\x04 \x01(\tH\x01R\x0fparentStepRunId\x88\x01\x01\x12$\n\x0b\x63hild_index\x18\x05 \x01(\x05H\x02R\nchildIndex\x88\x01\x01\x12 \n\tchild_key\x18\x06 \x01(\tH\x03R\x08\x63hildKey\x88\x01\x01\x12\x34\n\x13\x61\x64\x64itional_metadata\x18\x07 \x01(\tH\x04R\x12\x61\x64\x64itionalMetadata\x88\x01\x01\x12/\n\x11\x64\x65sired_worker_id\x18\x08 \x01(\tH\x05R\x0f\x64\x65siredWorkerId\x88\x01\x01\x12\x1f\n\x08priority\x18\t \x01(\x05H\x06R\x08priority\x88\x01\x01\x42\x0c\n\n_parent_idB\x15\n\x13_parent_step_run_idB\x0e\n\x0c_child_indexB\x0c\n\n_child_keyB\x16\n\x14_additional_metadataB\x14\n\x12_desired_worker_idB\x0b\n\t_priority\"A\n\x17TriggerWorkflowResponse\x12&\n\x0fworkflow_run_id\x18\x01 \x01(\tR\rworkflowRunId\"m\n\x13PutRateLimitRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05limit\x18\x02 \x01(\x05R\x05limit\x12.\n\x08\x64uration\x18\x03 \x01(\x0e\x32\x12.RateLimitDurationR\x08\x64uration\"\x16\n\x14PutRateLimitResponse*$\n\x0eStickyStrategy\x12\x08\n\x04SOFT\x10\x00\x12\x08\n\x04HARD\x10\x01*2\n\x0cWorkflowKind\x12\x0c\n\x08\x46UNCTION\x10\x00\x12\x0b\n\x07\x44URABLE\x10\x01\x12\x07\n\x03\x44\x41G\x10\x02*l\n\x18\x43oncurrencyLimitStrategy\x12\x16\n\x12\x43\x41NCEL_IN_PROGRESS\x10\x00\x12\x0f\n\x0b\x44ROP_NEWEST\x10\x01\x12\x10\n\x0cQUEUE_NEWEST\x10\x02\x12\x15\n\x11GROUP_ROUND_ROBIN\x10\x03*\x85\x01\n\x15WorkerLabelComparator\x12\t\n\x05\x45QUAL\x10\x00\x12\r\n\tNOT_EQUAL\x10\x01\x12\x10\n\x0cGREATER_THAN\x10\x02\x12\x19\n\x15GREATER_THAN_OR_EQUAL\x10\x03\x12\r\n\tLESS_THAN\x10\x04\x12\x16\n\x12LESS_THAN_OR_EQUAL\x10\x05*]\n\x11RateLimitDuration\x12\n\n\x06SECOND\x10\x00\x12\n\n\x06MINUTE\x10\x01\x12\x08\n\x04HOUR\x10\x02\x12\x07\n\x03\x44\x41Y\x10\x03\x12\x08\n\x04WEEK\x10\x04\x12\t\n\x05MONTH\x10\x05\x12\x08\n\x04YEAR\x10\x06\x32\xdc\x02\n\x0fWorkflowService\x12\x34\n\x0bPutWorkflow\x12\x13.PutWorkflowRequest\x1a\x10.WorkflowVersion\x12>\n\x10ScheduleWorkflow\x12\x18.ScheduleWorkflowRequest\x1a\x10.WorkflowVersion\x12\x44\n\x0fTriggerWorkflow\x12\x17.TriggerWorkflowRequest\x1a\x18.TriggerWorkflowResponse\x12P\n\x13\x42ulkTriggerWorkflow\x12\x1b.BulkTriggerWorkflowRequest\x1a\x1c.BulkTriggerWorkflowResponse\x12;\n\x0cPutRateLimit\x12\x14.PutRateLimitRequest\x1a\x15.PutRateLimitResponseBEB\x0eWorkflowsProtoP\x01Z1github.com/codeh007/gomtm/api-contracts/workflowsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_contracts.workflows.workflows_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'B\016WorkflowsProtoP\001Z1github.com/codeh007/gomtm/api-contracts/workflows'
  _globals['_CREATEWORKFLOWSTEPOPTS_WORKERLABELSENTRY']._loaded_options = None
  _globals['_CREATEWORKFLOWSTEPOPTS_WORKERLABELSENTRY']._serialized_options = b'8\001'
  _globals['_STICKYSTRATEGY']._serialized_start=4167
  _globals['_STICKYSTRATEGY']._serialized_end=4203
  _globals['_WORKFLOWKIND']._serialized_start=4205
  _globals['_WORKFLOWKIND']._serialized_end=4255
  _globals['_CONCURRENCYLIMITSTRATEGY']._serialized_start=4257
  _globals['_CONCURRENCYLIMITSTRATEGY']._serialized_end=4365
  _globals['_WORKERLABELCOMPARATOR']._serialized_start=4368
  _globals['_WORKERLABELCOMPARATOR']._serialized_end=4501
  _globals['_RATELIMITDURATION']._serialized_start=4503
  _globals['_RATELIMITDURATION']._serialized_end=4596
  _globals['_PUTWORKFLOWREQUEST']._serialized_start=76
  _globals['_PUTWORKFLOWREQUEST']._serialized_end=144
  _globals['_CREATEWORKFLOWVERSIONOPTS']._serialized_start=147
  _globals['_CREATEWORKFLOWVERSIONOPTS']._serialized_end=890
  _globals['_WORKFLOWCONCURRENCYOPTS']._serialized_start=893
  _globals['_WORKFLOWCONCURRENCYOPTS']._serialized_end=1145
  _globals['_CREATEWORKFLOWJOBOPTS']._serialized_start=1148
  _globals['_CREATEWORKFLOWJOBOPTS']._serialized_end=1278
  _globals['_DESIREDWORKERLABELS']._serialized_start=1281
  _globals['_DESIREDWORKERLABELS']._serialized_end=1556
  _globals['_CREATEWORKFLOWSTEPOPTS']._serialized_start=1559
  _globals['_CREATEWORKFLOWSTEPOPTS']._serialized_end=1993
  _globals['_CREATEWORKFLOWSTEPOPTS_WORKERLABELSENTRY']._serialized_start=1908
  _globals['_CREATEWORKFLOWSTEPOPTS_WORKERLABELSENTRY']._serialized_end=1993
  _globals['_CREATESTEPRATELIMIT']._serialized_start=1996
  _globals['_CREATESTEPRATELIMIT']._serialized_end=2305
  _globals['_LISTWORKFLOWSREQUEST']._serialized_start=2307
  _globals['_LISTWORKFLOWSREQUEST']._serialized_end=2329
  _globals['_SCHEDULEWORKFLOWREQUEST']._serialized_start=2332
  _globals['_SCHEDULEWORKFLOWREQUEST']._serialized_end=2758
  _globals['_SCHEDULEDWORKFLOW']._serialized_start=2760
  _globals['_SCHEDULEDWORKFLOW']._serialized_end=2854
  _globals['_WORKFLOWVERSION']._serialized_start=2857
  _globals['_WORKFLOWVERSION']._serialized_end=3158
  _globals['_WORKFLOWTRIGGEREVENTREF']._serialized_start=3160
  _globals['_WORKFLOWTRIGGEREVENTREF']._serialized_end=3243
  _globals['_WORKFLOWTRIGGERCRONREF']._serialized_start=3245
  _globals['_WORKFLOWTRIGGERCRONREF']._serialized_end=3318
  _globals['_BULKTRIGGERWORKFLOWREQUEST']._serialized_start=3320
  _globals['_BULKTRIGGERWORKFLOWREQUEST']._serialized_end=3403
  _globals['_BULKTRIGGERWORKFLOWRESPONSE']._serialized_start=3405
  _globals['_BULKTRIGGERWORKFLOWRESPONSE']._serialized_end=3476
  _globals['_TRIGGERWORKFLOWREQUEST']._serialized_start=3479
  _globals['_TRIGGERWORKFLOWREQUEST']._serialized_end=3963
  _globals['_TRIGGERWORKFLOWRESPONSE']._serialized_start=3965
  _globals['_TRIGGERWORKFLOWRESPONSE']._serialized_end=4030
  _globals['_PUTRATELIMITREQUEST']._serialized_start=4032
  _globals['_PUTRATELIMITREQUEST']._serialized_end=4141
  _globals['_PUTRATELIMITRESPONSE']._serialized_start=4143
  _globals['_PUTRATELIMITRESPONSE']._serialized_end=4165
  _globals['_WORKFLOWSERVICE']._serialized_start=4599
  _globals['_WORKFLOWSERVICE']._serialized_end=4947
# @@protoc_insertion_point(module_scope)
