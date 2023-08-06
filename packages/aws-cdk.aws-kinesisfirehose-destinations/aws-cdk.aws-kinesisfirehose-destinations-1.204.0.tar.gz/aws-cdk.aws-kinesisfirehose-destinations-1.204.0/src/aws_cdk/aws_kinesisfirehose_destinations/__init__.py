'''
# Amazon Kinesis Data Firehose Destinations Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This library provides constructs for adding destinations to a Amazon Kinesis Data Firehose
delivery stream. Destinations can be added by specifying the `destinations` prop when
defining a delivery stream.

See [Amazon Kinesis Data Firehose module README](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-kinesisfirehose-readme.html) for usage examples.

```python
import aws_cdk.aws_kinesisfirehose_destinations as destinations
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_f1d7a572
import aws_cdk.aws_kms as _aws_cdk_aws_kms_e491a92b
import aws_cdk.aws_logs as _aws_cdk_aws_logs_6c4320fb
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.BackupMode")
class BackupMode(enum.Enum):
    '''(experimental) Options for S3 record backup of a delivery stream.

    :stability: experimental
    :exampleMetadata: lit=../aws-kinesisfirehose-destinations/test/integ.s3-bucket.lit.ts infused

    Example::

        import path as path
        import aws_cdk.aws_kinesisfirehose as firehose
        import aws_cdk.aws_kms as kms
        import aws_cdk.aws_lambda_nodejs as lambdanodejs
        import aws_cdk.aws_logs as logs
        import aws_cdk.aws_s3 as s3
        import aws_cdk.core as cdk
        import aws_cdk.aws_kinesisfirehose_destinations as destinations
        
        app = cdk.App()
        
        stack = cdk.Stack(app, "aws-cdk-firehose-delivery-stream-s3-all-properties")
        
        bucket = s3.Bucket(stack, "Bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        
        backup_bucket = s3.Bucket(stack, "BackupBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        log_group = logs.LogGroup(stack, "LogGroup",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        data_processor_function = lambdanodejs.NodejsFunction(stack, "DataProcessorFunction",
            entry=path.join(__dirname, "lambda-data-processor.js"),
            timeout=cdk.Duration.minutes(1)
        )
        
        processor = firehose.LambdaFunctionProcessor(data_processor_function,
            buffer_interval=cdk.Duration.seconds(60),
            buffer_size=cdk.Size.mebibytes(1),
            retries=1
        )
        
        key = kms.Key(stack, "Key",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        backup_key = kms.Key(stack, "BackupKey",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        firehose.DeliveryStream(stack, "Delivery Stream",
            destinations=[destinations.S3Bucket(bucket,
                logging=True,
                log_group=log_group,
                processor=processor,
                compression=destinations.Compression.GZIP,
                data_output_prefix="regularPrefix",
                error_output_prefix="errorPrefix",
                buffering_interval=cdk.Duration.seconds(60),
                buffering_size=cdk.Size.mebibytes(1),
                encryption_key=key,
                s3_backup=destinations.DestinationS3BackupProps(
                    mode=destinations.BackupMode.ALL,
                    bucket=backup_bucket,
                    compression=destinations.Compression.ZIP,
                    data_output_prefix="backupPrefix",
                    error_output_prefix="backupErrorPrefix",
                    buffering_interval=cdk.Duration.seconds(60),
                    buffering_size=cdk.Size.mebibytes(1),
                    encryption_key=backup_key
                )
            )]
        )
        
        app.synth()
    '''

    ALL = "ALL"
    '''(experimental) All records are backed up.

    :stability: experimental
    '''
    FAILED = "FAILED"
    '''(experimental) Only records that failed to deliver or transform are backed up.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.CommonDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "logging": "logging",
        "log_group": "logGroup",
        "processor": "processor",
        "role": "role",
        "s3_backup": "s3Backup",
    },
)
class CommonDestinationProps:
    def __init__(
        self,
        *,
        logging: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        processor: typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        s3_backup: typing.Optional[typing.Union["DestinationS3BackupProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Generic properties for defining a delivery stream destination.

        :param logging: (experimental) If true, log errors when data transformation or data delivery fails. If ``logGroup`` is provided, this will be implicitly set to ``true``. Default: true - errors are logged.
        :param log_group: (experimental) The CloudWatch log group where log streams will be created to hold error logs. Default: - if ``logging`` is set to ``true``, a log group will be created for you.
        :param processor: (experimental) The data transformation that should be performed on the data before writing to the destination. Default: - no data transformation will occur.
        :param role: (experimental) The IAM role associated with this destination. Assumed by Kinesis Data Firehose to invoke processors and write to destinations Default: - a role will be created with default permissions.
        :param s3_backup: (experimental) The configuration for backing up source records to S3. Default: - source records will not be backed up to S3.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_kinesisfirehose as kinesisfirehose
            import aws_cdk.aws_kinesisfirehose_destinations as kinesisfirehose_destinations
            import aws_cdk.aws_kms as kms
            import aws_cdk.aws_logs as logs
            import aws_cdk.aws_s3 as s3
            import aws_cdk.core as cdk
            
            # bucket: s3.Bucket
            # compression: kinesisfirehose_destinations.Compression
            # data_processor: kinesisfirehose.IDataProcessor
            # key: kms.Key
            # log_group: logs.LogGroup
            # role: iam.Role
            # size: cdk.Size
            
            common_destination_props = kinesisfirehose_destinations.CommonDestinationProps(
                logging=False,
                log_group=log_group,
                processor=data_processor,
                role=role,
                s3_backup=kinesisfirehose_destinations.DestinationS3BackupProps(
                    bucket=bucket,
                    buffering_interval=cdk.Duration.minutes(30),
                    buffering_size=size,
                    compression=compression,
                    data_output_prefix="dataOutputPrefix",
                    encryption_key=key,
                    error_output_prefix="errorOutputPrefix",
                    logging=False,
                    log_group=log_group,
                    mode=kinesisfirehose_destinations.BackupMode.ALL
                )
            )
        '''
        if isinstance(s3_backup, dict):
            s3_backup = DestinationS3BackupProps(**s3_backup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23bf83dfb39c481a8582ce297c1b33440065bf45fa3b161e76318a617785b961)
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument processor", value=processor, expected_type=type_hints["processor"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_backup", value=s3_backup, expected_type=type_hints["s3_backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logging is not None:
            self._values["logging"] = logging
        if log_group is not None:
            self._values["log_group"] = log_group
        if processor is not None:
            self._values["processor"] = processor
        if role is not None:
            self._values["role"] = role
        if s3_backup is not None:
            self._values["s3_backup"] = s3_backup

    @builtins.property
    def logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, log errors when data transformation or data delivery fails.

        If ``logGroup`` is provided, this will be implicitly set to ``true``.

        :default: true - errors are logged.

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''(experimental) The CloudWatch log group where log streams will be created to hold error logs.

        :default: - if ``logging`` is set to ``true``, a log group will be created for you.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    @builtins.property
    def processor(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor]:
        '''(experimental) The data transformation that should be performed on the data before writing to the destination.

        :default: - no data transformation will occur.

        :stability: experimental
        '''
        result = self._values.get("processor")
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role associated with this destination.

        Assumed by Kinesis Data Firehose to invoke processors and write to destinations

        :default: - a role will be created with default permissions.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def s3_backup(self) -> typing.Optional["DestinationS3BackupProps"]:
        '''(experimental) The configuration for backing up source records to S3.

        :default: - source records will not be backed up to S3.

        :stability: experimental
        '''
        result = self._values.get("s3_backup")
        return typing.cast(typing.Optional["DestinationS3BackupProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.CommonDestinationS3Props",
    jsii_struct_bases=[],
    name_mapping={
        "buffering_interval": "bufferingInterval",
        "buffering_size": "bufferingSize",
        "compression": "compression",
        "data_output_prefix": "dataOutputPrefix",
        "encryption_key": "encryptionKey",
        "error_output_prefix": "errorOutputPrefix",
    },
)
class CommonDestinationS3Props:
    def __init__(
        self,
        *,
        buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
        compression: typing.Optional["Compression"] = None,
        data_output_prefix: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Common properties for defining a backup, intermediary, or final S3 destination for a Kinesis Data Firehose delivery stream.

        :param buffering_interval: (experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket. Minimum: Duration.seconds(60) Maximum: Duration.seconds(900) Default: Duration.seconds(300)
        :param buffering_size: (experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket. Minimum: Size.mebibytes(1) Maximum: Size.mebibytes(128) Default: Size.mebibytes(5)
        :param compression: (experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift destinations because they are not supported by the Amazon Redshift COPY operation that reads from the S3 bucket. Default: - UNCOMPRESSED
        :param data_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param encryption_key: (experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket. Default: - Data is not encrypted.
        :param error_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_destinations as kinesisfirehose_destinations
            import aws_cdk.aws_kms as kms
            import aws_cdk.core as cdk
            
            # compression: kinesisfirehose_destinations.Compression
            # key: kms.Key
            # size: cdk.Size
            
            common_destination_s3_props = kinesisfirehose_destinations.CommonDestinationS3Props(
                buffering_interval=cdk.Duration.minutes(30),
                buffering_size=size,
                compression=compression,
                data_output_prefix="dataOutputPrefix",
                encryption_key=key,
                error_output_prefix="errorOutputPrefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e8530b4a2f43e6263237162efc95401a7bba66e023a9d6ed00d8785e8598b3)
            check_type(argname="argument buffering_interval", value=buffering_interval, expected_type=type_hints["buffering_interval"])
            check_type(argname="argument buffering_size", value=buffering_size, expected_type=type_hints["buffering_size"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument data_output_prefix", value=data_output_prefix, expected_type=type_hints["data_output_prefix"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buffering_interval is not None:
            self._values["buffering_interval"] = buffering_interval
        if buffering_size is not None:
            self._values["buffering_size"] = buffering_size
        if compression is not None:
            self._values["compression"] = compression
        if data_output_prefix is not None:
            self._values["data_output_prefix"] = data_output_prefix
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix

    @builtins.property
    def buffering_interval(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket.

        Minimum: Duration.seconds(60)
        Maximum: Duration.seconds(900)

        :default: Duration.seconds(300)

        :stability: experimental
        '''
        result = self._values.get("buffering_interval")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def buffering_size(self) -> typing.Optional[_aws_cdk_core_f4b25747.Size]:
        '''(experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket.

        Minimum: Size.mebibytes(1)
        Maximum: Size.mebibytes(128)

        :default: Size.mebibytes(5)

        :stability: experimental
        '''
        result = self._values.get("buffering_size")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Size], result)

    @builtins.property
    def compression(self) -> typing.Optional["Compression"]:
        '''(experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket.

        The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift
        destinations because they are not supported by the Amazon Redshift COPY operation
        that reads from the S3 bucket.

        :default: - UNCOMPRESSED

        :stability: experimental
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional["Compression"], result)

    @builtins.property
    def data_output_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3.

        This prefix appears immediately following the bucket name.

        :default: "YYYY/MM/DD/HH"

        :see: https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html
        :stability: experimental
        '''
        result = self._values.get("data_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''(experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket.

        :default: - Data is not encrypted.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3.

        This prefix appears immediately following the bucket name.

        :default: "YYYY/MM/DD/HH"

        :see: https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html
        :stability: experimental
        '''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonDestinationS3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Compression(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.Compression",
):
    '''(experimental) Possible compression options Kinesis Data Firehose can use to compress data on delivery.

    :stability: experimental
    :exampleMetadata: lit=../aws-kinesisfirehose-destinations/test/integ.s3-bucket.lit.ts infused

    Example::

        import path as path
        import aws_cdk.aws_kinesisfirehose as firehose
        import aws_cdk.aws_kms as kms
        import aws_cdk.aws_lambda_nodejs as lambdanodejs
        import aws_cdk.aws_logs as logs
        import aws_cdk.aws_s3 as s3
        import aws_cdk.core as cdk
        import aws_cdk.aws_kinesisfirehose_destinations as destinations
        
        app = cdk.App()
        
        stack = cdk.Stack(app, "aws-cdk-firehose-delivery-stream-s3-all-properties")
        
        bucket = s3.Bucket(stack, "Bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        
        backup_bucket = s3.Bucket(stack, "BackupBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        log_group = logs.LogGroup(stack, "LogGroup",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        data_processor_function = lambdanodejs.NodejsFunction(stack, "DataProcessorFunction",
            entry=path.join(__dirname, "lambda-data-processor.js"),
            timeout=cdk.Duration.minutes(1)
        )
        
        processor = firehose.LambdaFunctionProcessor(data_processor_function,
            buffer_interval=cdk.Duration.seconds(60),
            buffer_size=cdk.Size.mebibytes(1),
            retries=1
        )
        
        key = kms.Key(stack, "Key",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        backup_key = kms.Key(stack, "BackupKey",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        firehose.DeliveryStream(stack, "Delivery Stream",
            destinations=[destinations.S3Bucket(bucket,
                logging=True,
                log_group=log_group,
                processor=processor,
                compression=destinations.Compression.GZIP,
                data_output_prefix="regularPrefix",
                error_output_prefix="errorPrefix",
                buffering_interval=cdk.Duration.seconds(60),
                buffering_size=cdk.Size.mebibytes(1),
                encryption_key=key,
                s3_backup=destinations.DestinationS3BackupProps(
                    mode=destinations.BackupMode.ALL,
                    bucket=backup_bucket,
                    compression=destinations.Compression.ZIP,
                    data_output_prefix="backupPrefix",
                    error_output_prefix="backupErrorPrefix",
                    buffering_interval=cdk.Duration.seconds(60),
                    buffering_size=cdk.Size.mebibytes(1),
                    encryption_key=backup_key
                )
            )]
        )
        
        app.synth()
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, value: builtins.str) -> "Compression":
        '''(experimental) Creates a new Compression instance with a custom value.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f909e61836aa78811dfa6fbb13ea8f22164104e6dc8857cecf89625f352940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Compression", jsii.sinvoke(cls, "of", [value]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GZIP")
    def GZIP(cls) -> "Compression":
        '''(experimental) gzip.

        :stability: experimental
        '''
        return typing.cast("Compression", jsii.sget(cls, "GZIP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HADOOP_SNAPPY")
    def HADOOP_SNAPPY(cls) -> "Compression":
        '''(experimental) Hadoop-compatible Snappy.

        :stability: experimental
        '''
        return typing.cast("Compression", jsii.sget(cls, "HADOOP_SNAPPY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SNAPPY")
    def SNAPPY(cls) -> "Compression":
        '''(experimental) Snappy.

        :stability: experimental
        '''
        return typing.cast("Compression", jsii.sget(cls, "SNAPPY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ZIP")
    def ZIP(cls) -> "Compression":
        '''(experimental) ZIP.

        :stability: experimental
        '''
        return typing.cast("Compression", jsii.sget(cls, "ZIP"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) the string value of the Compression.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.DestinationS3BackupProps",
    jsii_struct_bases=[CommonDestinationS3Props],
    name_mapping={
        "buffering_interval": "bufferingInterval",
        "buffering_size": "bufferingSize",
        "compression": "compression",
        "data_output_prefix": "dataOutputPrefix",
        "encryption_key": "encryptionKey",
        "error_output_prefix": "errorOutputPrefix",
        "bucket": "bucket",
        "logging": "logging",
        "log_group": "logGroup",
        "mode": "mode",
    },
)
class DestinationS3BackupProps(CommonDestinationS3Props):
    def __init__(
        self,
        *,
        buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
        compression: typing.Optional[Compression] = None,
        data_output_prefix: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        bucket: typing.Optional[_aws_cdk_aws_s3_55f001a5.IBucket] = None,
        logging: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        mode: typing.Optional[BackupMode] = None,
    ) -> None:
        '''(experimental) Properties for defining an S3 backup destination.

        S3 backup is available for all destinations, regardless of whether the final destination is S3 or not.

        :param buffering_interval: (experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket. Minimum: Duration.seconds(60) Maximum: Duration.seconds(900) Default: Duration.seconds(300)
        :param buffering_size: (experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket. Minimum: Size.mebibytes(1) Maximum: Size.mebibytes(128) Default: Size.mebibytes(5)
        :param compression: (experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift destinations because they are not supported by the Amazon Redshift COPY operation that reads from the S3 bucket. Default: - UNCOMPRESSED
        :param data_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param encryption_key: (experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket. Default: - Data is not encrypted.
        :param error_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param bucket: (experimental) The S3 bucket that will store data and failed records. Default: - If ``mode`` is set to ``BackupMode.ALL`` or ``BackupMode.FAILED``, a bucket will be created for you.
        :param logging: (experimental) If true, log errors when data transformation or data delivery fails. If ``logGroup`` is provided, this will be implicitly set to ``true``. Default: true - errors are logged.
        :param log_group: (experimental) The CloudWatch log group where log streams will be created to hold error logs. Default: - if ``logging`` is set to ``true``, a log group will be created for you.
        :param mode: (experimental) Indicates the mode by which incoming records should be backed up to S3, if any. If ``bucket`` is provided, this will be implicitly set to ``BackupMode.ALL``. Default: - If ``bucket`` is provided, the default will be ``BackupMode.ALL``. Otherwise, source records are not backed up to S3.

        :stability: experimental
        :exampleMetadata: lit=../aws-kinesisfirehose-destinations/test/integ.s3-bucket.lit.ts infused

        Example::

            import path as path
            import aws_cdk.aws_kinesisfirehose as firehose
            import aws_cdk.aws_kms as kms
            import aws_cdk.aws_lambda_nodejs as lambdanodejs
            import aws_cdk.aws_logs as logs
            import aws_cdk.aws_s3 as s3
            import aws_cdk.core as cdk
            import aws_cdk.aws_kinesisfirehose_destinations as destinations
            
            app = cdk.App()
            
            stack = cdk.Stack(app, "aws-cdk-firehose-delivery-stream-s3-all-properties")
            
            bucket = s3.Bucket(stack, "Bucket",
                removal_policy=cdk.RemovalPolicy.DESTROY,
                auto_delete_objects=True
            )
            
            backup_bucket = s3.Bucket(stack, "BackupBucket",
                removal_policy=cdk.RemovalPolicy.DESTROY,
                auto_delete_objects=True
            )
            log_group = logs.LogGroup(stack, "LogGroup",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
            
            data_processor_function = lambdanodejs.NodejsFunction(stack, "DataProcessorFunction",
                entry=path.join(__dirname, "lambda-data-processor.js"),
                timeout=cdk.Duration.minutes(1)
            )
            
            processor = firehose.LambdaFunctionProcessor(data_processor_function,
                buffer_interval=cdk.Duration.seconds(60),
                buffer_size=cdk.Size.mebibytes(1),
                retries=1
            )
            
            key = kms.Key(stack, "Key",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
            
            backup_key = kms.Key(stack, "BackupKey",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
            
            firehose.DeliveryStream(stack, "Delivery Stream",
                destinations=[destinations.S3Bucket(bucket,
                    logging=True,
                    log_group=log_group,
                    processor=processor,
                    compression=destinations.Compression.GZIP,
                    data_output_prefix="regularPrefix",
                    error_output_prefix="errorPrefix",
                    buffering_interval=cdk.Duration.seconds(60),
                    buffering_size=cdk.Size.mebibytes(1),
                    encryption_key=key,
                    s3_backup=destinations.DestinationS3BackupProps(
                        mode=destinations.BackupMode.ALL,
                        bucket=backup_bucket,
                        compression=destinations.Compression.ZIP,
                        data_output_prefix="backupPrefix",
                        error_output_prefix="backupErrorPrefix",
                        buffering_interval=cdk.Duration.seconds(60),
                        buffering_size=cdk.Size.mebibytes(1),
                        encryption_key=backup_key
                    )
                )]
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4726aca1375da7f9742b1c054ad7ac6b3a14cd9f130714f95b6b85b9772b2eaf)
            check_type(argname="argument buffering_interval", value=buffering_interval, expected_type=type_hints["buffering_interval"])
            check_type(argname="argument buffering_size", value=buffering_size, expected_type=type_hints["buffering_size"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument data_output_prefix", value=data_output_prefix, expected_type=type_hints["data_output_prefix"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buffering_interval is not None:
            self._values["buffering_interval"] = buffering_interval
        if buffering_size is not None:
            self._values["buffering_size"] = buffering_size
        if compression is not None:
            self._values["compression"] = compression
        if data_output_prefix is not None:
            self._values["data_output_prefix"] = data_output_prefix
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if bucket is not None:
            self._values["bucket"] = bucket
        if logging is not None:
            self._values["logging"] = logging
        if log_group is not None:
            self._values["log_group"] = log_group
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def buffering_interval(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket.

        Minimum: Duration.seconds(60)
        Maximum: Duration.seconds(900)

        :default: Duration.seconds(300)

        :stability: experimental
        '''
        result = self._values.get("buffering_interval")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def buffering_size(self) -> typing.Optional[_aws_cdk_core_f4b25747.Size]:
        '''(experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket.

        Minimum: Size.mebibytes(1)
        Maximum: Size.mebibytes(128)

        :default: Size.mebibytes(5)

        :stability: experimental
        '''
        result = self._values.get("buffering_size")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Size], result)

    @builtins.property
    def compression(self) -> typing.Optional[Compression]:
        '''(experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket.

        The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift
        destinations because they are not supported by the Amazon Redshift COPY operation
        that reads from the S3 bucket.

        :default: - UNCOMPRESSED

        :stability: experimental
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[Compression], result)

    @builtins.property
    def data_output_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3.

        This prefix appears immediately following the bucket name.

        :default: "YYYY/MM/DD/HH"

        :see: https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html
        :stability: experimental
        '''
        result = self._values.get("data_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''(experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket.

        :default: - Data is not encrypted.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3.

        This prefix appears immediately following the bucket name.

        :default: "YYYY/MM/DD/HH"

        :see: https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html
        :stability: experimental
        '''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> typing.Optional[_aws_cdk_aws_s3_55f001a5.IBucket]:
        '''(experimental) The S3 bucket that will store data and failed records.

        :default: - If ``mode`` is set to ``BackupMode.ALL`` or ``BackupMode.FAILED``, a bucket will be created for you.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_55f001a5.IBucket], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, log errors when data transformation or data delivery fails.

        If ``logGroup`` is provided, this will be implicitly set to ``true``.

        :default: true - errors are logged.

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''(experimental) The CloudWatch log group where log streams will be created to hold error logs.

        :default: - if ``logging`` is set to ``true``, a log group will be created for you.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    @builtins.property
    def mode(self) -> typing.Optional[BackupMode]:
        '''(experimental) Indicates the mode by which incoming records should be backed up to S3, if any.

        If ``bucket`` is provided, this will be implicitly set to ``BackupMode.ALL``.

        :default:

        - If ``bucket`` is provided, the default will be ``BackupMode.ALL``. Otherwise,
        source records are not backed up to S3.

        :stability: experimental
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[BackupMode], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DestinationS3BackupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_kinesisfirehose_f1d7a572.IDestination)
class S3Bucket(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.S3Bucket",
):
    '''(experimental) An S3 bucket destination for data from a Kinesis Data Firehose delivery stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # bucket: s3.Bucket
        # Provide a Lambda function that will transform records before delivery, with custom
        # buffering and retry configuration
        lambda_function = lambda_.Function(self, "Processor",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
        )
        lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
            buffer_interval=Duration.minutes(5),
            buffer_size=Size.mebibytes(5),
            retries=5
        )
        s3_destination = destinations.S3Bucket(bucket,
            processor=lambda_processor
        )
        firehose.DeliveryStream(self, "Delivery Stream",
            destinations=[s3_destination]
        )
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        *,
        buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
        compression: typing.Optional[Compression] = None,
        data_output_prefix: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        logging: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        processor: typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        s3_backup: typing.Optional[typing.Union[DestinationS3BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: -
        :param buffering_interval: (experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket. Minimum: Duration.seconds(60) Maximum: Duration.seconds(900) Default: Duration.seconds(300)
        :param buffering_size: (experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket. Minimum: Size.mebibytes(1) Maximum: Size.mebibytes(128) Default: Size.mebibytes(5)
        :param compression: (experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift destinations because they are not supported by the Amazon Redshift COPY operation that reads from the S3 bucket. Default: - UNCOMPRESSED
        :param data_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param encryption_key: (experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket. Default: - Data is not encrypted.
        :param error_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param logging: (experimental) If true, log errors when data transformation or data delivery fails. If ``logGroup`` is provided, this will be implicitly set to ``true``. Default: true - errors are logged.
        :param log_group: (experimental) The CloudWatch log group where log streams will be created to hold error logs. Default: - if ``logging`` is set to ``true``, a log group will be created for you.
        :param processor: (experimental) The data transformation that should be performed on the data before writing to the destination. Default: - no data transformation will occur.
        :param role: (experimental) The IAM role associated with this destination. Assumed by Kinesis Data Firehose to invoke processors and write to destinations Default: - a role will be created with default permissions.
        :param s3_backup: (experimental) The configuration for backing up source records to S3. Default: - source records will not be backed up to S3.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb933a9da58150723f942d84e7ceb3beb308e4a8cb0873db3b41e6b45b82a9fb)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        props = S3BucketProps(
            buffering_interval=buffering_interval,
            buffering_size=buffering_size,
            compression=compression,
            data_output_prefix=data_output_prefix,
            encryption_key=encryption_key,
            error_output_prefix=error_output_prefix,
            logging=logging,
            log_group=log_group,
            processor=processor,
            role=role,
            s3_backup=s3_backup,
        )

        jsii.create(self.__class__, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_kinesisfirehose_f1d7a572.DestinationConfig:
        '''(experimental) Binds this destination to the Kinesis Data Firehose delivery stream.

        Implementers should use this method to bind resources to the stack and initialize values using the provided stream.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf05e83e0e950141fb355c3170a93164b1b54a802b6b51100b3f025bc769fcb9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        _options = _aws_cdk_aws_kinesisfirehose_f1d7a572.DestinationBindOptions()

        return typing.cast(_aws_cdk_aws_kinesisfirehose_f1d7a572.DestinationConfig, jsii.invoke(self, "bind", [scope, _options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-destinations.S3BucketProps",
    jsii_struct_bases=[CommonDestinationS3Props, CommonDestinationProps],
    name_mapping={
        "buffering_interval": "bufferingInterval",
        "buffering_size": "bufferingSize",
        "compression": "compression",
        "data_output_prefix": "dataOutputPrefix",
        "encryption_key": "encryptionKey",
        "error_output_prefix": "errorOutputPrefix",
        "logging": "logging",
        "log_group": "logGroup",
        "processor": "processor",
        "role": "role",
        "s3_backup": "s3Backup",
    },
)
class S3BucketProps(CommonDestinationS3Props, CommonDestinationProps):
    def __init__(
        self,
        *,
        buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
        compression: typing.Optional[Compression] = None,
        data_output_prefix: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        logging: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        processor: typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        s3_backup: typing.Optional[typing.Union[DestinationS3BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Props for defining an S3 destination of a Kinesis Data Firehose delivery stream.

        :param buffering_interval: (experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket. Minimum: Duration.seconds(60) Maximum: Duration.seconds(900) Default: Duration.seconds(300)
        :param buffering_size: (experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket. Minimum: Size.mebibytes(1) Maximum: Size.mebibytes(128) Default: Size.mebibytes(5)
        :param compression: (experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift destinations because they are not supported by the Amazon Redshift COPY operation that reads from the S3 bucket. Default: - UNCOMPRESSED
        :param data_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param encryption_key: (experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket. Default: - Data is not encrypted.
        :param error_output_prefix: (experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3. This prefix appears immediately following the bucket name. Default: "YYYY/MM/DD/HH"
        :param logging: (experimental) If true, log errors when data transformation or data delivery fails. If ``logGroup`` is provided, this will be implicitly set to ``true``. Default: true - errors are logged.
        :param log_group: (experimental) The CloudWatch log group where log streams will be created to hold error logs. Default: - if ``logging`` is set to ``true``, a log group will be created for you.
        :param processor: (experimental) The data transformation that should be performed on the data before writing to the destination. Default: - no data transformation will occur.
        :param role: (experimental) The IAM role associated with this destination. Assumed by Kinesis Data Firehose to invoke processors and write to destinations Default: - a role will be created with default permissions.
        :param s3_backup: (experimental) The configuration for backing up source records to S3. Default: - source records will not be backed up to S3.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # bucket: s3.Bucket
            # Provide a Lambda function that will transform records before delivery, with custom
            # buffering and retry configuration
            lambda_function = lambda_.Function(self, "Processor",
                runtime=lambda_.Runtime.NODEJS_14_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
            )
            lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
                buffer_interval=Duration.minutes(5),
                buffer_size=Size.mebibytes(5),
                retries=5
            )
            s3_destination = destinations.S3Bucket(bucket,
                processor=lambda_processor
            )
            firehose.DeliveryStream(self, "Delivery Stream",
                destinations=[s3_destination]
            )
        '''
        if isinstance(s3_backup, dict):
            s3_backup = DestinationS3BackupProps(**s3_backup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c037464d0db87f53f84b3b04f023d822403536eb3f0354efaa81e784f9f8f0)
            check_type(argname="argument buffering_interval", value=buffering_interval, expected_type=type_hints["buffering_interval"])
            check_type(argname="argument buffering_size", value=buffering_size, expected_type=type_hints["buffering_size"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument data_output_prefix", value=data_output_prefix, expected_type=type_hints["data_output_prefix"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument processor", value=processor, expected_type=type_hints["processor"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_backup", value=s3_backup, expected_type=type_hints["s3_backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buffering_interval is not None:
            self._values["buffering_interval"] = buffering_interval
        if buffering_size is not None:
            self._values["buffering_size"] = buffering_size
        if compression is not None:
            self._values["compression"] = compression
        if data_output_prefix is not None:
            self._values["data_output_prefix"] = data_output_prefix
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if logging is not None:
            self._values["logging"] = logging
        if log_group is not None:
            self._values["log_group"] = log_group
        if processor is not None:
            self._values["processor"] = processor
        if role is not None:
            self._values["role"] = role
        if s3_backup is not None:
            self._values["s3_backup"] = s3_backup

    @builtins.property
    def buffering_interval(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) The length of time that Firehose buffers incoming data before delivering it to the S3 bucket.

        Minimum: Duration.seconds(60)
        Maximum: Duration.seconds(900)

        :default: Duration.seconds(300)

        :stability: experimental
        '''
        result = self._values.get("buffering_interval")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def buffering_size(self) -> typing.Optional[_aws_cdk_core_f4b25747.Size]:
        '''(experimental) The size of the buffer that Kinesis Data Firehose uses for incoming data before delivering it to the S3 bucket.

        Minimum: Size.mebibytes(1)
        Maximum: Size.mebibytes(128)

        :default: Size.mebibytes(5)

        :stability: experimental
        '''
        result = self._values.get("buffering_size")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Size], result)

    @builtins.property
    def compression(self) -> typing.Optional[Compression]:
        '''(experimental) The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket.

        The compression formats SNAPPY or ZIP cannot be specified for Amazon Redshift
        destinations because they are not supported by the Amazon Redshift COPY operation
        that reads from the S3 bucket.

        :default: - UNCOMPRESSED

        :stability: experimental
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[Compression], result)

    @builtins.property
    def data_output_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A prefix that Kinesis Data Firehose evaluates and adds to records before writing them to S3.

        This prefix appears immediately following the bucket name.

        :default: "YYYY/MM/DD/HH"

        :see: https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html
        :stability: experimental
        '''
        result = self._values.get("data_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''(experimental) The AWS KMS key used to encrypt the data that it delivers to your Amazon S3 bucket.

        :default: - Data is not encrypted.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3.

        This prefix appears immediately following the bucket name.

        :default: "YYYY/MM/DD/HH"

        :see: https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html
        :stability: experimental
        '''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, log errors when data transformation or data delivery fails.

        If ``logGroup`` is provided, this will be implicitly set to ``true``.

        :default: true - errors are logged.

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''(experimental) The CloudWatch log group where log streams will be created to hold error logs.

        :default: - if ``logging`` is set to ``true``, a log group will be created for you.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    @builtins.property
    def processor(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor]:
        '''(experimental) The data transformation that should be performed on the data before writing to the destination.

        :default: - no data transformation will occur.

        :stability: experimental
        '''
        result = self._values.get("processor")
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role associated with this destination.

        Assumed by Kinesis Data Firehose to invoke processors and write to destinations

        :default: - a role will be created with default permissions.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def s3_backup(self) -> typing.Optional[DestinationS3BackupProps]:
        '''(experimental) The configuration for backing up source records to S3.

        :default: - source records will not be backed up to S3.

        :stability: experimental
        '''
        result = self._values.get("s3_backup")
        return typing.cast(typing.Optional[DestinationS3BackupProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BackupMode",
    "CommonDestinationProps",
    "CommonDestinationS3Props",
    "Compression",
    "DestinationS3BackupProps",
    "S3Bucket",
    "S3BucketProps",
]

publication.publish()

def _typecheckingstub__23bf83dfb39c481a8582ce297c1b33440065bf45fa3b161e76318a617785b961(
    *,
    logging: typing.Optional[builtins.bool] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    processor: typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    s3_backup: typing.Optional[typing.Union[DestinationS3BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e8530b4a2f43e6263237162efc95401a7bba66e023a9d6ed00d8785e8598b3(
    *,
    buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
    compression: typing.Optional[Compression] = None,
    data_output_prefix: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f909e61836aa78811dfa6fbb13ea8f22164104e6dc8857cecf89625f352940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4726aca1375da7f9742b1c054ad7ac6b3a14cd9f130714f95b6b85b9772b2eaf(
    *,
    buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
    compression: typing.Optional[Compression] = None,
    data_output_prefix: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[_aws_cdk_aws_s3_55f001a5.IBucket] = None,
    logging: typing.Optional[builtins.bool] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    mode: typing.Optional[BackupMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb933a9da58150723f942d84e7ceb3beb308e4a8cb0873db3b41e6b45b82a9fb(
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    *,
    buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
    compression: typing.Optional[Compression] = None,
    data_output_prefix: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    logging: typing.Optional[builtins.bool] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    processor: typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    s3_backup: typing.Optional[typing.Union[DestinationS3BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf05e83e0e950141fb355c3170a93164b1b54a802b6b51100b3f025bc769fcb9(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c037464d0db87f53f84b3b04f023d822403536eb3f0354efaa81e784f9f8f0(
    *,
    buffering_interval: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    buffering_size: typing.Optional[_aws_cdk_core_f4b25747.Size] = None,
    compression: typing.Optional[Compression] = None,
    data_output_prefix: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    logging: typing.Optional[builtins.bool] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    processor: typing.Optional[_aws_cdk_aws_kinesisfirehose_f1d7a572.IDataProcessor] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    s3_backup: typing.Optional[typing.Union[DestinationS3BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
