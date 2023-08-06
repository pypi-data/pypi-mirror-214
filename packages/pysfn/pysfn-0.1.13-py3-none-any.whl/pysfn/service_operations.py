import typing
from aws_cdk import (
    aws_dynamodb as ddb,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_iam as iam,
)
from aws_cdk.aws_stepfunctions import JsonPath


def s3_write_json(
    obj: typing.Union[dict, typing.List],
    bucket: typing.Union[s3.IBucket, str],
    key: str,
) -> str:
    pass


def build_s3_write_json_step(
    stack,
    id_: str,
    obj: typing.Union[dict, list, str],
    bucket: typing.Union[str, s3.Bucket],
    key: typing.Union[str, JsonPath],
):
    if not isinstance(bucket, str):
        bucket = bucket.bucket_name
    return tasks.CallAwsService(
        stack,
        id_,
        service="s3",
        action="putObject",
        iam_resources=["*"],
        input_path="$.register",
        result_path="$.register.out",
        result_selector={"ETag.$": "States.StringToJson($.ETag)"},
        parameters={
            "Bucket": bucket,
            "Key": JsonPath.string_at(key) if not key.startswith("${") else key,
            "Body": JsonPath.string_at(obj),
            "ContentType": "application/json",
        },
    )


def s3_read_json(
    bucket: typing.Union[s3.Bucket, str], key: str
) -> (typing.Union[dict, typing.List], str, str):
    pass


def build_s3_read_json_step(
    stack,
    id_: str,
    bucket: typing.Union[str, s3.Bucket],
    key: typing.Union[str, JsonPath],
):
    return tasks.CallAwsService(
        stack,
        id_,
        service="s3",
        action="getObject",
        iam_resources=["*"],
        input_path="$.register",
        result_path="$.register.out",
        result_selector={
            "Body.$": "States.StringToJson($.Body)",
            "LastModified.$": "$.LastModified",
            "ETag.$": "States.StringToJson($.ETag)",
        },
        parameters={
            "Bucket": JsonPath.string_at(bucket)
            if isinstance(bucket, str)
            else bucket.bucket_name,
            "Key": JsonPath.string_at(key) if not key.startswith("${") else key,
        },
    )


def sqs_send_message(
    queue: typing.Union[sqs.Queue, str],
    message: typing.Union[typing.Dict, str],
    message_deduplication_id: str = None,
    message_group_id: str = None,
):
    pass


def build_sqs_send_message_step(
    stack,
    id_: str,
    queue: typing.Union[sqs.Queue, str],
    message: typing.Union[typing.Dict, str],
    message_deduplication_id: str = None,
    message_group_id: str = None,
):
    return tasks.SqsSendMessage(
        stack,
        id_,
        input_path="$.register",
        result_path="$.register.out",
        result_selector={"MessageId.$": "$.MessageId"},
        queue=queue,
        message_body=sfn.TaskInput.from_json_path_at(message),
        message_deduplication_id=JsonPath.string_at(message_deduplication_id)
        if message_deduplication_id
        else None,
        message_group_id=JsonPath.string_at(message_group_id)
        if message_group_id
        else None,
    )


def sqs_receive_message(
    queue: sqs.IQueue,
    max_number_of_messages: int = None,
    visibility_timeout: int = None,
    wait_time_seconds: int = None,
):
    pass


def build_sqs_receive_message_step(
    stack,
    id_: str,
    queue: sqs.IQueue,
    max_number_of_messages: int = None,
    visibility_timeout: int = None,
    wait_time_seconds: int = None,
):
    params = {"QueueUrl": queue.queue_url}
    if max_number_of_messages is not None:
        params["MaxNumberOfMessages"] = max_number_of_messages
    if visibility_timeout is not None:
        params["VisibilityTimeout"] = visibility_timeout
    if wait_time_seconds is not None:
        params["WaitTimeSeconds"] = wait_time_seconds

    return tasks.CallAwsService(
        stack,
        id_,
        service="sqs",
        action="receiveMessage",
        iam_resources=["*"],
        input_path="$.register",
        result_path="$.register.out",
        result_selector={"Messages.$": "$.Messages",},
        parameters=params,
    )


def sqs_delete_message(queue: sqs.IQueue, receipt_handle: str):
    pass


def build_sqs_delete_message_step(
    stack, id_: str, queue: sqs.IQueue, receipt_handle: str
):
    return tasks.CallAwsService(
        stack,
        id_,
        service="sqs",
        action="deleteMessage",
        iam_resources=["*"],
        input_path="$.register",
        result_path="$.register.out",
        parameters={
            "QueueUrl": queue.queue_url,
            "ReceiptHandle": JsonPath.string_at(receipt_handle),
        },
    )


def dynamo_write_item(table: ddb.Table, item: dict):
    pass


def dynamo_read_item(table: ddb.Table, key: dict):
    pass


def dynamo_delete_item(table: ddb.Table, key: dict):
    pass


def dynamo_update_item(table: ddb.Table, key: dict, attribute_updates: dict):
    pass


def dynamo_export(
    bucket: typing.Union[s3.IBucket, str],
    table: typing.Union[ddb.Table, str],
    export_format: str = "DYNAMODB_JSON",
) -> dict:
    pass


def build_dynamo_export_step(
    stack,
    id_: str,
    bucket: typing.Union[s3.IBucket, str],
    table: typing.Union[ddb.Table, str],
    export_format: str = "DYNAMODB_JSON",
):
    return tasks.CallAwsService(
        stack,
        id_,
        service="dynamodb",
        action="exportTableToPointInTime",
        iam_resources=["*"],
        input_path="$.register",
        result_path="$.register.out",
        parameters={
            "S3Bucket": JsonPath.string_at(bucket)
            if isinstance(bucket, str)
            else bucket.bucket_name,
            "TableArn": table.table_arn
            if isinstance(table, ddb.Table)
            else JsonPath.string_at(table),
            "ExportFormat": export_format,
        },
    )


def dynamo_describe_export(export_arn: str) -> dict:
    pass


def build_dynamo_describe_export(
    stack, id_: str, export_arn: str,
):
    return tasks.CallAwsService(
        stack,
        id_,
        service="dynamodb",
        action="describeExport",
        iam_resources=["*"],
        input_path="$.register",
        result_path="$.register.out",
        parameters={"ExportArn": JsonPath.string_at(export_arn)},
    )


service_operations = []


def register_operation(
    method: typing.Callable,
    builder: typing.Callable,
    step_name: str,
    return_vars: typing.List[str],
    additional_policies: typing.Optional[typing.List[iam.PolicyStatement]] = None,
):
    method.builder = builder
    method.step_name = step_name
    method.return_vars = return_vars
    method.additional_policies = additional_policies
    service_operations.append(method)


register_operation(s3_write_json, build_s3_write_json_step, "S3 Write JSON", ["ETag"])
register_operation(
    s3_read_json,
    build_s3_read_json_step,
    "S3 Read JSON",
    ["Body", "LastModified", "ETag"],
)
register_operation(
    sqs_send_message, build_sqs_send_message_step, "Send SQS Message", ["MessageId"]
)
register_operation(
    sqs_receive_message,
    build_sqs_receive_message_step,
    "Receive SQS Message",
    ["Messages"],
)
register_operation(
    sqs_delete_message, build_sqs_delete_message_step, "Delete SQS Message", [],
)
register_operation(
    dynamo_export,
    build_dynamo_export_step,
    "Export Table",
    ["ExportDescription"],
    [iam.PolicyStatement(actions=["s3:PutObject"], resources=["*"])],
)
register_operation(
    dynamo_describe_export,
    build_dynamo_describe_export,
    "Describe Table Export",
    ["ExportDescription"],
)
