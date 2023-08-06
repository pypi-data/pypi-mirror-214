'''
# @aws-cdk/aws-dynamodb-global

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

## NOTICE: This module has been deprecated in favor of `@aws-cdk/aws-dynamodb.Table.replicationRegions`

---


Global Tables builds upon DynamoDB’s global footprint to provide you with a fully managed, multi-region, and multi-master database that provides fast, local, read and write performance for massively scaled, global applications. Global Tables replicates your Amazon DynamoDB tables automatically across your choice of AWS regions.

Here is a minimal deployable Global DynamoDB tables definition:

```python
from aws_cdk.aws_dynamodb import Attribute
from aws_cdk.aws_dynamodb import AttributeType
from aws_cdk.aws_dynamodb_global import GlobalTable
from aws_cdk.core import App

app = App()
GlobalTable(app, "globdynamodb",
    partition_key=Attribute(name="hashKey", type=AttributeType.STRING),
    table_name="GlobalTable",
    regions=["us-east-1", "us-east-2", "us-west-2"]
)
app.synth()
```

## Implementation Notes

AWS Global DynamoDB Tables is an odd case currently.  The way this package works -

* Creates a DynamoDB table in a separate stack in each `DynamoDBGlobalStackProps.region` specified
* Deploys a CFN Custom Resource to your stack's specified region that calls a lambda that runs the aws cli which calls `createGlobalTable()`

### Notes

GlobalTable() will set `dynamoProps.stream` to be `NEW_AND_OLD_IMAGES` since this is a required attribute for AWS Global DynamoDB tables to work.  The package will throw an error if any other `stream` specification is set in `DynamoDBGlobalStackProps`.
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

import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_eb1dc53b
import aws_cdk.aws_kms as _aws_cdk_aws_kms_e491a92b
import aws_cdk.core as _aws_cdk_core_f4b25747


class GlobalTable(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dynamodb-global.GlobalTable",
):
    '''(deprecated) This class works by deploying an AWS DynamoDB table into each region specified in  GlobalTableProps.regions[], then triggering a CloudFormation Custom Resource Lambda to link them all together to create linked AWS Global DynamoDB tables.

    :deprecated: use ``@aws-cdk/aws-dynamodb.Table.replicationRegions`` instead

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_dynamodb import Attribute
        from aws_cdk.aws_dynamodb import AttributeType
        from aws_cdk.aws_dynamodb_global import GlobalTable
        from aws_cdk.core import App
        
        app = App()
        GlobalTable(app, "globdynamodb",
            partition_key=Attribute(name="hashKey", type=AttributeType.STRING),
            table_name="GlobalTable",
            regions=["us-east-1", "us-east-2", "us-west-2"]
        )
        app.synth()
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        regions: typing.Sequence[builtins.str],
        table_name: builtins.str,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_core_f4b25747.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        billing_mode: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        server_side_encryption: typing.Optional[builtins.bool] = None,
        stream: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.StreamViewType] = None,
        table_class: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableClass] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        partition_key: typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param regions: (deprecated) Array of environments to create DynamoDB tables in. The tables will all be created in the same account.
        :param table_name: (deprecated) Name of the DynamoDB table to use across all regional tables. This is required for global tables.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. .. epigraph:: **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not specified, the key that the Tablet generates for you will be created with default permissions. If you are using CDKv2, these permissions will be sufficient to enable the key for use with DynamoDB tables. If you are using CDKv1, make sure the feature flag ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param server_side_encryption: (deprecated) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param table_class: Specify the table class. Default: STANDARD
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param partition_key: Partition key attribute definition.
        :param sort_key: Sort key attribute definition. Default: no sort key

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fda1e72709e01a71f21e98c510b9e2e160fc50dceec9bdc6e6a810597d2326)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GlobalTableProps(
            regions=regions,
            table_name=table_name,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
            billing_mode=billing_mode,
            contributor_insights_enabled=contributor_insights_enabled,
            encryption=encryption,
            encryption_key=encryption_key,
            point_in_time_recovery=point_in_time_recovery,
            read_capacity=read_capacity,
            removal_policy=removal_policy,
            replication_regions=replication_regions,
            replication_timeout=replication_timeout,
            server_side_encryption=server_side_encryption,
            stream=stream,
            table_class=table_class,
            time_to_live_attribute=time_to_live_attribute,
            wait_for_replication_to_finish=wait_for_replication_to_finish,
            write_capacity=write_capacity,
            partition_key=partition_key,
            sort_key=sort_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="regionalTables")
    def regional_tables(self) -> typing.List[_aws_cdk_aws_dynamodb_eb1dc53b.Table]:
        '''(deprecated) Obtain tables deployed in other each region.

        :stability: deprecated
        '''
        return typing.cast(typing.List[_aws_cdk_aws_dynamodb_eb1dc53b.Table], jsii.get(self, "regionalTables"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dynamodb-global.GlobalTableProps",
    jsii_struct_bases=[
        _aws_cdk_core_f4b25747.StackProps, _aws_cdk_aws_dynamodb_eb1dc53b.TableOptions
    ],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "partition_key": "partitionKey",
        "sort_key": "sortKey",
        "billing_mode": "billingMode",
        "contributor_insights_enabled": "contributorInsightsEnabled",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "point_in_time_recovery": "pointInTimeRecovery",
        "read_capacity": "readCapacity",
        "removal_policy": "removalPolicy",
        "replication_regions": "replicationRegions",
        "replication_timeout": "replicationTimeout",
        "server_side_encryption": "serverSideEncryption",
        "stream": "stream",
        "table_class": "tableClass",
        "time_to_live_attribute": "timeToLiveAttribute",
        "wait_for_replication_to_finish": "waitForReplicationToFinish",
        "write_capacity": "writeCapacity",
        "regions": "regions",
        "table_name": "tableName",
    },
)
class GlobalTableProps(
    _aws_cdk_core_f4b25747.StackProps,
    _aws_cdk_aws_dynamodb_eb1dc53b.TableOptions,
):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_core_f4b25747.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        partition_key: typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
        billing_mode: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        server_side_encryption: typing.Optional[builtins.bool] = None,
        stream: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.StreamViewType] = None,
        table_class: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableClass] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        regions: typing.Sequence[builtins.str],
        table_name: builtins.str,
    ) -> None:
        '''(deprecated) Properties for the multiple DynamoDB tables to mash together into a global table.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param partition_key: Partition key attribute definition.
        :param sort_key: Sort key attribute definition. Default: no sort key
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. .. epigraph:: **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not specified, the key that the Tablet generates for you will be created with default permissions. If you are using CDKv2, these permissions will be sufficient to enable the key for use with DynamoDB tables. If you are using CDKv1, make sure the feature flag ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param server_side_encryption: (deprecated) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param table_class: Specify the table class. Default: STANDARD
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param regions: (deprecated) Array of environments to create DynamoDB tables in. The tables will all be created in the same account.
        :param table_name: (deprecated) Name of the DynamoDB table to use across all regional tables. This is required for global tables.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_dynamodb import Attribute
            from aws_cdk.aws_dynamodb import AttributeType
            from aws_cdk.aws_dynamodb_global import GlobalTable
            from aws_cdk.core import App
            
            app = App()
            GlobalTable(app, "globdynamodb",
                partition_key=Attribute(name="hashKey", type=AttributeType.STRING),
                table_name="GlobalTable",
                regions=["us-east-1", "us-east-2", "us-west-2"]
            )
            app.synth()
        '''
        if isinstance(env, dict):
            env = _aws_cdk_core_f4b25747.Environment(**env)
        if isinstance(partition_key, dict):
            partition_key = _aws_cdk_aws_dynamodb_eb1dc53b.Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = _aws_cdk_aws_dynamodb_eb1dc53b.Attribute(**sort_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cc5c5641dcfb68ac202cdab6742c6b3f914d8d87f99b8d3d3f285137906315)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument contributor_insights_enabled", value=contributor_insights_enabled, expected_type=type_hints["contributor_insights_enabled"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument point_in_time_recovery", value=point_in_time_recovery, expected_type=type_hints["point_in_time_recovery"])
            check_type(argname="argument read_capacity", value=read_capacity, expected_type=type_hints["read_capacity"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replication_regions", value=replication_regions, expected_type=type_hints["replication_regions"])
            check_type(argname="argument replication_timeout", value=replication_timeout, expected_type=type_hints["replication_timeout"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
            check_type(argname="argument time_to_live_attribute", value=time_to_live_attribute, expected_type=type_hints["time_to_live_attribute"])
            check_type(argname="argument wait_for_replication_to_finish", value=wait_for_replication_to_finish, expected_type=type_hints["wait_for_replication_to_finish"])
            check_type(argname="argument write_capacity", value=write_capacity, expected_type=type_hints["write_capacity"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
            "regions": regions,
            "table_name": table_name,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if contributor_insights_enabled is not None:
            self._values["contributor_insights_enabled"] = contributor_insights_enabled
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replication_regions is not None:
            self._values["replication_regions"] = replication_regions
        if replication_timeout is not None:
            self._values["replication_timeout"] = replication_timeout
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if stream is not None:
            self._values["stream"] = stream
        if table_class is not None:
            self._values["table_class"] = table_class
        if time_to_live_attribute is not None:
            self._values["time_to_live_attribute"] = time_to_live_attribute
        if wait_for_replication_to_finish is not None:
            self._values["wait_for_replication_to_finish"] = wait_for_replication_to_finish
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_core_f4b25747.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            # Use a concrete account and region to deploy this stack to:
            # `.account` and `.region` will simply return these values.
            Stack(app, "Stack1",
                env=Environment(
                    account="123456789012",
                    region="us-east-1"
                )
            )
            
            # Use the CLI's current credentials to determine the target environment:
            # `.account` and `.region` will reflect the account+region the CLI
            # is configured to use (based on the user CLI credentials)
            Stack(app, "Stack2",
                env=Environment(
                    account=process.env.CDK_DEFAULT_ACCOUNT,
                    region=process.env.CDK_DEFAULT_REGION
                )
            )
            
            # Define multiple stacks stage associated with an environment
            my_stage = Stage(app, "MyStage",
                env=Environment(
                    account="123456789012",
                    region="us-east-1"
                )
            )
            
            # both of these stacks will use the stage's account/region:
            # `.account` and `.region` will resolve to the concrete values as above
            MyStack(my_stage, "Stack1")
            YourStack(my_stage, "Stack2")
            
            # Define an environment-agnostic stack:
            # `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            # which will only resolve to actual values by CloudFormation during deployment.
            MyStack(app, "Stack1")
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_core_f4b25747.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def partition_key(self) -> _aws_cdk_aws_dynamodb_eb1dc53b.Attribute:
        '''Partition key attribute definition.'''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, result)

    @builtins.property
    def sort_key(self) -> typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute]:
        '''Sort key attribute definition.

        :default: no sort key
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute], result)

    @builtins.property
    def billing_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.BillingMode]:
        '''Specify how you are charged for read and write throughput and how you manage capacity.

        :default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.BillingMode], result)

    @builtins.property
    def contributor_insights_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether CloudWatch contributor insights is enabled.

        :default: false
        '''
        result = self._values.get("contributor_insights_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableEncryption]:
        '''Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``serverSideEncryption`` is set.
        .. epigraph::

           **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not
           specified, the key that the Tablet generates for you will be created with
           default permissions. If you are using CDKv2, these permissions will be
           sufficient to enable the key for use with DynamoDB tables.  If you are
           using CDKv1, make sure the feature flag
           ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``.

        :default: - server-side encryption is enabled with an AWS owned customer master key
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''External KMS key to use for table encryption.

        This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``.

        :default:

        - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this
        property is undefined, a new KMS key will be created and associated with this table.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[builtins.bool]:
        '''Whether point-in-time recovery is enabled.

        :default: - point-in-time recovery is disabled
        '''
        result = self._values.get("point_in_time_recovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        '''The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5
        '''
        result = self._values.get("read_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy]:
        '''The removal policy to apply to the DynamoDB Table.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy], result)

    @builtins.property
    def replication_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Regions where replica tables will be created.

        :default: - no replica tables are created
        '''
        result = self._values.get("replication_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_timeout(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The timeout for a table replication operation in a single region.

        :default: Duration.minutes(30)
        '''
        result = self._values.get("replication_timeout")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set.

        :default: - server-side encryption is enabled with an AWS owned customer master key

        :deprecated:

        This property is deprecated. In order to obtain the same behavior as
        enabling this, set the ``encryption`` property to ``TableEncryption.AWS_MANAGED`` instead.

        :stability: deprecated
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stream(self) -> typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.StreamViewType]:
        '''When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        :default: - streams are disabled unless ``replicationRegions`` is specified
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.StreamViewType], result)

    @builtins.property
    def table_class(self) -> typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableClass]:
        '''Specify the table class.

        :default: STANDARD
        '''
        result = self._values.get("table_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableClass], result)

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[builtins.str]:
        '''The name of TTL attribute.

        :default: - TTL is disabled
        '''
        result = self._values.get("time_to_live_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_replication_to_finish(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether CloudFormation stack waits for replication to finish.

        If set to false, the CloudFormation resource will mark the resource as
        created and replication will be completed asynchronously. This property is
        ignored if replicationRegions property is not set.

        DO NOT UNSET this property if adding/removing multiple replicationRegions
        in one deployment, as CloudFormation only supports one region replication
        at a time. CDK overcomes this limitation by waiting for replication to
        finish before starting new replicationRegion.

        :default: true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        '''
        result = self._values.get("wait_for_replication_to_finish")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        '''The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5
        '''
        result = self._values.get("write_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def regions(self) -> typing.List[builtins.str]:
        '''(deprecated) Array of environments to create DynamoDB tables in.

        The tables will all be created in the same account.

        :stability: deprecated
        '''
        result = self._values.get("regions")
        assert result is not None, "Required property 'regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''(deprecated) Name of the DynamoDB table to use across all regional tables.

        This is required for global tables.

        :stability: deprecated
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GlobalTable",
    "GlobalTableProps",
]

publication.publish()

def _typecheckingstub__51fda1e72709e01a71f21e98c510b9e2e160fc50dceec9bdc6e6a810597d2326(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    regions: typing.Sequence[builtins.str],
    table_name: builtins.str,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_core_f4b25747.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    billing_mode: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.BillingMode] = None,
    contributor_insights_enabled: typing.Optional[builtins.bool] = None,
    encryption: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    point_in_time_recovery: typing.Optional[builtins.bool] = None,
    read_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    server_side_encryption: typing.Optional[builtins.bool] = None,
    stream: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.StreamViewType] = None,
    table_class: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableClass] = None,
    time_to_live_attribute: typing.Optional[builtins.str] = None,
    wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
    write_capacity: typing.Optional[jsii.Number] = None,
    partition_key: typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cc5c5641dcfb68ac202cdab6742c6b3f914d8d87f99b8d3d3f285137906315(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_core_f4b25747.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    partition_key: typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[_aws_cdk_aws_dynamodb_eb1dc53b.Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_mode: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.BillingMode] = None,
    contributor_insights_enabled: typing.Optional[builtins.bool] = None,
    encryption: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    point_in_time_recovery: typing.Optional[builtins.bool] = None,
    read_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    server_side_encryption: typing.Optional[builtins.bool] = None,
    stream: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.StreamViewType] = None,
    table_class: typing.Optional[_aws_cdk_aws_dynamodb_eb1dc53b.TableClass] = None,
    time_to_live_attribute: typing.Optional[builtins.str] = None,
    wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
    write_capacity: typing.Optional[jsii.Number] = None,
    regions: typing.Sequence[builtins.str],
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
