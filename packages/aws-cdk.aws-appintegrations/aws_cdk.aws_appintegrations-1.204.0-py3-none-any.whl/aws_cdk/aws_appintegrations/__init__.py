'''
# AWS::AppIntegrations Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_appintegrations as appintegrations
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AppIntegrations construct libraries](https://constructs.dev/search?q=appintegrations)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AppIntegrations resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppIntegrations.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AppIntegrations](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppIntegrations.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDataIntegration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appintegrations.CfnDataIntegration",
):
    '''A CloudFormation ``AWS::AppIntegrations::DataIntegration``.

    Creates and persists a DataIntegration resource.

    :cloudformationResource: AWS::AppIntegrations::DataIntegration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appintegrations as appintegrations
        
        # filters: Any
        # object_configuration: Any
        
        cfn_data_integration = appintegrations.CfnDataIntegration(self, "MyCfnDataIntegration",
            kms_key="kmsKey",
            name="name",
            schedule_config=appintegrations.CfnDataIntegration.ScheduleConfigProperty(
                schedule_expression="scheduleExpression",
        
                # the properties below are optional
                first_execution_from="firstExecutionFrom",
                object="object"
            ),
            source_uri="sourceUri",
        
            # the properties below are optional
            description="description",
            file_configuration=appintegrations.CfnDataIntegration.FileConfigurationProperty(
                folders=["folders"],
        
                # the properties below are optional
                filters=filters
            ),
            object_configuration=object_configuration,
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        kms_key: builtins.str,
        name: builtins.str,
        schedule_config: typing.Union[typing.Union["CfnDataIntegration.ScheduleConfigProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        source_uri: builtins.str,
        description: typing.Optional[builtins.str] = None,
        file_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDataIntegration.FileConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        object_configuration: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppIntegrations::DataIntegration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param kms_key: The KMS key for the DataIntegration.
        :param name: The name of the DataIntegration.
        :param schedule_config: The name of the data and how often it should be pulled from the source.
        :param source_uri: The URI of the data source.
        :param description: A description of the DataIntegration.
        :param file_configuration: ``AWS::AppIntegrations::DataIntegration.FileConfiguration``.
        :param object_configuration: ``AWS::AppIntegrations::DataIntegration.ObjectConfiguration``.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d06bd649f098d385b0b732d41ce2118c1ae9068fa34e923b740a93fda330c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataIntegrationProps(
            kms_key=kms_key,
            name=name,
            schedule_config=schedule_config,
            source_uri=source_uri,
            description=description,
            file_configuration=file_configuration,
            object_configuration=object_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67090d7a2b5625071e47c01a1292d6a34be0c0a7e268710a6604d9c5b0087c3)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2263721541917e29803cff29b6644067a2f60f62c906bea92d19a0156b3decc4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDataIntegrationArn")
    def attr_data_integration_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the DataIntegration.

        :cloudformationAttribute: DataIntegrationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataIntegrationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''A unique identifier.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        '''The KMS key for the DataIntegration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-kmskey
        '''
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6e6c876b6264881013ed525ee568276df0cb01a8b0a10a4b1a5ba93b003d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the DataIntegration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1771d33e828c9c0b2faac006071d085c5986746ad2579dd086d840f794bf1613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="objectConfiguration")
    def object_configuration(self) -> typing.Any:
        '''``AWS::AppIntegrations::DataIntegration.ObjectConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-objectconfiguration
        '''
        return typing.cast(typing.Any, jsii.get(self, "objectConfiguration"))

    @object_configuration.setter
    def object_configuration(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d920c0a87bb07b7074c3efc895d3311253b2ed288a85b17d5c15b8396c8b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="scheduleConfig")
    def schedule_config(
        self,
    ) -> typing.Union["CfnDataIntegration.ScheduleConfigProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The name of the data and how often it should be pulled from the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-scheduleconfig
        '''
        return typing.cast(typing.Union["CfnDataIntegration.ScheduleConfigProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "scheduleConfig"))

    @schedule_config.setter
    def schedule_config(
        self,
        value: typing.Union["CfnDataIntegration.ScheduleConfigProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648e6138d4b47035f3ac1cceac674de724fb8fc1e92f3e8a23329c3a4132ef85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleConfig", value)

    @builtins.property
    @jsii.member(jsii_name="sourceUri")
    def source_uri(self) -> builtins.str:
        '''The URI of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-sourceuri
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceUri"))

    @source_uri.setter
    def source_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65154f816186464c5ec1cb0b09bb65668062e70e5a1ff359143691e108bc7fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the DataIntegration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716b65080d32cff8063c87e2f4d3f4dd22bdc60d6593c1b18b2c448337457435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="fileConfiguration")
    def file_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataIntegration.FileConfigurationProperty"]]:
        '''``AWS::AppIntegrations::DataIntegration.FileConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-fileconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataIntegration.FileConfigurationProperty"]], jsii.get(self, "fileConfiguration"))

    @file_configuration.setter
    def file_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataIntegration.FileConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2743338d5a9a09c1580e735a8d3232edb709476fc0590335f3d8821f3f567dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appintegrations.CfnDataIntegration.FileConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"folders": "folders", "filters": "filters"},
    )
    class FileConfigurationProperty:
        def __init__(
            self,
            *,
            folders: typing.Sequence[builtins.str],
            filters: typing.Any = None,
        ) -> None:
            '''
            :param folders: ``CfnDataIntegration.FileConfigurationProperty.Folders``.
            :param filters: ``CfnDataIntegration.FileConfigurationProperty.Filters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-fileconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_appintegrations as appintegrations
                
                # filters: Any
                
                file_configuration_property = appintegrations.CfnDataIntegration.FileConfigurationProperty(
                    folders=["folders"],
                
                    # the properties below are optional
                    filters=filters
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e812e4d0eb5c32e3d5831f129d2385a30fe6a4312bef60d0319267cad980c9f6)
                check_type(argname="argument folders", value=folders, expected_type=type_hints["folders"])
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "folders": folders,
            }
            if filters is not None:
                self._values["filters"] = filters

        @builtins.property
        def folders(self) -> typing.List[builtins.str]:
            '''``CfnDataIntegration.FileConfigurationProperty.Folders``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-fileconfiguration.html#cfn-appintegrations-dataintegration-fileconfiguration-folders
            '''
            result = self._values.get("folders")
            assert result is not None, "Required property 'folders' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def filters(self) -> typing.Any:
            '''``CfnDataIntegration.FileConfigurationProperty.Filters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-fileconfiguration.html#cfn-appintegrations-dataintegration-fileconfiguration-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appintegrations.CfnDataIntegration.ScheduleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule_expression": "scheduleExpression",
            "first_execution_from": "firstExecutionFrom",
            "object": "object",
        },
    )
    class ScheduleConfigProperty:
        def __init__(
            self,
            *,
            schedule_expression: builtins.str,
            first_execution_from: typing.Optional[builtins.str] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the data and how often it should be pulled from the source.

            :param schedule_expression: How often the data should be pulled from data source.
            :param first_execution_from: The start date for objects to import in the first flow run as an Unix/epoch timestamp in milliseconds or in ISO-8601 format.
            :param object: The name of the object to pull from the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_appintegrations as appintegrations
                
                schedule_config_property = appintegrations.CfnDataIntegration.ScheduleConfigProperty(
                    schedule_expression="scheduleExpression",
                
                    # the properties below are optional
                    first_execution_from="firstExecutionFrom",
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2052553c976a3c37ab1d5cca7d75eb1e7ee10f4b91947b84f6c66d1717100a3)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
                check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }
            if first_execution_from is not None:
                self._values["first_execution_from"] = first_execution_from
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''How often the data should be pulled from data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html#cfn-appintegrations-dataintegration-scheduleconfig-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def first_execution_from(self) -> typing.Optional[builtins.str]:
            '''The start date for objects to import in the first flow run as an Unix/epoch timestamp in milliseconds or in ISO-8601 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html#cfn-appintegrations-dataintegration-scheduleconfig-firstexecutionfrom
            '''
            result = self._values.get("first_execution_from")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The name of the object to pull from the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html#cfn-appintegrations-dataintegration-scheduleconfig-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appintegrations.CfnDataIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key": "kmsKey",
        "name": "name",
        "schedule_config": "scheduleConfig",
        "source_uri": "sourceUri",
        "description": "description",
        "file_configuration": "fileConfiguration",
        "object_configuration": "objectConfiguration",
        "tags": "tags",
    },
)
class CfnDataIntegrationProps:
    def __init__(
        self,
        *,
        kms_key: builtins.str,
        name: builtins.str,
        schedule_config: typing.Union[typing.Union[CfnDataIntegration.ScheduleConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        source_uri: builtins.str,
        description: typing.Optional[builtins.str] = None,
        file_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataIntegration.FileConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        object_configuration: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataIntegration``.

        :param kms_key: The KMS key for the DataIntegration.
        :param name: The name of the DataIntegration.
        :param schedule_config: The name of the data and how often it should be pulled from the source.
        :param source_uri: The URI of the data source.
        :param description: A description of the DataIntegration.
        :param file_configuration: ``AWS::AppIntegrations::DataIntegration.FileConfiguration``.
        :param object_configuration: ``AWS::AppIntegrations::DataIntegration.ObjectConfiguration``.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_appintegrations as appintegrations
            
            # filters: Any
            # object_configuration: Any
            
            cfn_data_integration_props = appintegrations.CfnDataIntegrationProps(
                kms_key="kmsKey",
                name="name",
                schedule_config=appintegrations.CfnDataIntegration.ScheduleConfigProperty(
                    schedule_expression="scheduleExpression",
            
                    # the properties below are optional
                    first_execution_from="firstExecutionFrom",
                    object="object"
                ),
                source_uri="sourceUri",
            
                # the properties below are optional
                description="description",
                file_configuration=appintegrations.CfnDataIntegration.FileConfigurationProperty(
                    folders=["folders"],
            
                    # the properties below are optional
                    filters=filters
                ),
                object_configuration=object_configuration,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c679e068281dad4a2c893acb213356ace74d87fddc2d3994b40d987ca770713)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule_config", value=schedule_config, expected_type=type_hints["schedule_config"])
            check_type(argname="argument source_uri", value=source_uri, expected_type=type_hints["source_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument file_configuration", value=file_configuration, expected_type=type_hints["file_configuration"])
            check_type(argname="argument object_configuration", value=object_configuration, expected_type=type_hints["object_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
            "name": name,
            "schedule_config": schedule_config,
            "source_uri": source_uri,
        }
        if description is not None:
            self._values["description"] = description
        if file_configuration is not None:
            self._values["file_configuration"] = file_configuration
        if object_configuration is not None:
            self._values["object_configuration"] = object_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''The KMS key for the DataIntegration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-kmskey
        '''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the DataIntegration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule_config(
        self,
    ) -> typing.Union[CfnDataIntegration.ScheduleConfigProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The name of the data and how often it should be pulled from the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-scheduleconfig
        '''
        result = self._values.get("schedule_config")
        assert result is not None, "Required property 'schedule_config' is missing"
        return typing.cast(typing.Union[CfnDataIntegration.ScheduleConfigProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def source_uri(self) -> builtins.str:
        '''The URI of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-sourceuri
        '''
        result = self._values.get("source_uri")
        assert result is not None, "Required property 'source_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the DataIntegration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDataIntegration.FileConfigurationProperty]]:
        '''``AWS::AppIntegrations::DataIntegration.FileConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-fileconfiguration
        '''
        result = self._values.get("file_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDataIntegration.FileConfigurationProperty]], result)

    @builtins.property
    def object_configuration(self) -> typing.Any:
        '''``AWS::AppIntegrations::DataIntegration.ObjectConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-objectconfiguration
        '''
        result = self._values.get("object_configuration")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEventIntegration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appintegrations.CfnEventIntegration",
):
    '''A CloudFormation ``AWS::AppIntegrations::EventIntegration``.

    Creates an event integration. You provide a name, description, and a reference to an Amazon EventBridge bus in your account and a partner event source that will push events to that bus. No objects are created in your account, only metadata that is persisted on the EventIntegration control plane.

    :cloudformationResource: AWS::AppIntegrations::EventIntegration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appintegrations as appintegrations
        
        cfn_event_integration = appintegrations.CfnEventIntegration(self, "MyCfnEventIntegration",
            event_bridge_bus="eventBridgeBus",
            event_filter=appintegrations.CfnEventIntegration.EventFilterProperty(
                source="source"
            ),
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        event_bridge_bus: builtins.str,
        event_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEventIntegration.EventFilterProperty", typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppIntegrations::EventIntegration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param event_bridge_bus: The Amazon EventBridge bus for the event integration.
        :param event_filter: The event integration filter.
        :param name: The name of the event integration.
        :param description: The event integration description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09604e2d8a930a44021ae27d853278c7e5171c7247d31b638ffedb53a2fa38dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventIntegrationProps(
            event_bridge_bus=event_bridge_bus,
            event_filter=event_filter,
            name=name,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97ecafd91d3b6f89c7bc5e1c07a256be63154fb2cc571191e2107a06f80f72f)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324d4a62d51fdd4d56680e6c303c9c03d8d4325e33ce5ec632c534eeaf5dcb5d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEventIntegrationArn")
    def attr_event_integration_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the event integration.

        :cloudformationAttribute: EventIntegrationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEventIntegrationArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeBus")
    def event_bridge_bus(self) -> builtins.str:
        '''The Amazon EventBridge bus for the event integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-eventbridgebus
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBridgeBus"))

    @event_bridge_bus.setter
    def event_bridge_bus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d214dd9ecb90eed9dc5fbfc1bd39f39ead0bb7d67a0fcfb0cd748c3b3a5539c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBridgeBus", value)

    @builtins.property
    @jsii.member(jsii_name="eventFilter")
    def event_filter(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventIntegration.EventFilterProperty"]:
        '''The event integration filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-eventfilter
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventIntegration.EventFilterProperty"], jsii.get(self, "eventFilter"))

    @event_filter.setter
    def event_filter(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventIntegration.EventFilterProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d0bf87995e8b933afd3dc934578f102d661a7a271fd3b5f3dfc72b0b487a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventFilter", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the event integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877fa05b337e15ee3b25b9f0f453663d329ef2d4de035aa16e63771fcab8c9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The event integration description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1295f0e4ca121ea43d3a13b2c5b4a49e3eb4df56b4cb1ff2f7f0830f87f116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appintegrations.CfnEventIntegration.EventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class EventFilterProperty:
        def __init__(self, *, source: builtins.str) -> None:
            '''The event integration filter.

            :param source: The source of the events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-eventintegration-eventfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_appintegrations as appintegrations
                
                event_filter_property = appintegrations.CfnEventIntegration.EventFilterProperty(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2abd76c23fc2e5228d1a4352ba7a92d26b07f1df182e6f4d6b932f980ae76df5)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source": source,
            }

        @builtins.property
        def source(self) -> builtins.str:
            '''The source of the events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-eventintegration-eventfilter.html#cfn-appintegrations-eventintegration-eventfilter-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appintegrations.CfnEventIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bridge_bus": "eventBridgeBus",
        "event_filter": "eventFilter",
        "name": "name",
        "description": "description",
        "tags": "tags",
    },
)
class CfnEventIntegrationProps:
    def __init__(
        self,
        *,
        event_bridge_bus: builtins.str,
        event_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventIntegration.EventFilterProperty, typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEventIntegration``.

        :param event_bridge_bus: The Amazon EventBridge bus for the event integration.
        :param event_filter: The event integration filter.
        :param name: The name of the event integration.
        :param description: The event integration description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_appintegrations as appintegrations
            
            cfn_event_integration_props = appintegrations.CfnEventIntegrationProps(
                event_bridge_bus="eventBridgeBus",
                event_filter=appintegrations.CfnEventIntegration.EventFilterProperty(
                    source="source"
                ),
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786eaf5d72389ac0421c2927abdc38ae37e6e939e22fd68e2a157c4850165203)
            check_type(argname="argument event_bridge_bus", value=event_bridge_bus, expected_type=type_hints["event_bridge_bus"])
            check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bridge_bus": event_bridge_bus,
            "event_filter": event_filter,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def event_bridge_bus(self) -> builtins.str:
        '''The Amazon EventBridge bus for the event integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-eventbridgebus
        '''
        result = self._values.get("event_bridge_bus")
        assert result is not None, "Required property 'event_bridge_bus' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_filter(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventIntegration.EventFilterProperty]:
        '''The event integration filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-eventfilter
        '''
        result = self._values.get("event_filter")
        assert result is not None, "Required property 'event_filter' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventIntegration.EventFilterProperty], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the event integration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The event integration description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataIntegration",
    "CfnDataIntegrationProps",
    "CfnEventIntegration",
    "CfnEventIntegrationProps",
]

publication.publish()

def _typecheckingstub__75d06bd649f098d385b0b732d41ce2118c1ae9068fa34e923b740a93fda330c7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    kms_key: builtins.str,
    name: builtins.str,
    schedule_config: typing.Union[typing.Union[CfnDataIntegration.ScheduleConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    source_uri: builtins.str,
    description: typing.Optional[builtins.str] = None,
    file_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataIntegration.FileConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_configuration: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67090d7a2b5625071e47c01a1292d6a34be0c0a7e268710a6604d9c5b0087c3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2263721541917e29803cff29b6644067a2f60f62c906bea92d19a0156b3decc4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6e6c876b6264881013ed525ee568276df0cb01a8b0a10a4b1a5ba93b003d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1771d33e828c9c0b2faac006071d085c5986746ad2579dd086d840f794bf1613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d920c0a87bb07b7074c3efc895d3311253b2ed288a85b17d5c15b8396c8b3f(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648e6138d4b47035f3ac1cceac674de724fb8fc1e92f3e8a23329c3a4132ef85(
    value: typing.Union[CfnDataIntegration.ScheduleConfigProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65154f816186464c5ec1cb0b09bb65668062e70e5a1ff359143691e108bc7fcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716b65080d32cff8063c87e2f4d3f4dd22bdc60d6593c1b18b2c448337457435(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2743338d5a9a09c1580e735a8d3232edb709476fc0590335f3d8821f3f567dc7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDataIntegration.FileConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e812e4d0eb5c32e3d5831f129d2385a30fe6a4312bef60d0319267cad980c9f6(
    *,
    folders: typing.Sequence[builtins.str],
    filters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2052553c976a3c37ab1d5cca7d75eb1e7ee10f4b91947b84f6c66d1717100a3(
    *,
    schedule_expression: builtins.str,
    first_execution_from: typing.Optional[builtins.str] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c679e068281dad4a2c893acb213356ace74d87fddc2d3994b40d987ca770713(
    *,
    kms_key: builtins.str,
    name: builtins.str,
    schedule_config: typing.Union[typing.Union[CfnDataIntegration.ScheduleConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    source_uri: builtins.str,
    description: typing.Optional[builtins.str] = None,
    file_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataIntegration.FileConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_configuration: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09604e2d8a930a44021ae27d853278c7e5171c7247d31b638ffedb53a2fa38dc(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    event_bridge_bus: builtins.str,
    event_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventIntegration.EventFilterProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97ecafd91d3b6f89c7bc5e1c07a256be63154fb2cc571191e2107a06f80f72f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324d4a62d51fdd4d56680e6c303c9c03d8d4325e33ce5ec632c534eeaf5dcb5d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d214dd9ecb90eed9dc5fbfc1bd39f39ead0bb7d67a0fcfb0cd748c3b3a5539c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d0bf87995e8b933afd3dc934578f102d661a7a271fd3b5f3dfc72b0b487a66(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventIntegration.EventFilterProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877fa05b337e15ee3b25b9f0f453663d329ef2d4de035aa16e63771fcab8c9fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1295f0e4ca121ea43d3a13b2c5b4a49e3eb4df56b4cb1ff2f7f0830f87f116(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abd76c23fc2e5228d1a4352ba7a92d26b07f1df182e6f4d6b932f980ae76df5(
    *,
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786eaf5d72389ac0421c2927abdc38ae37e6e939e22fd68e2a157c4850165203(
    *,
    event_bridge_bus: builtins.str,
    event_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventIntegration.EventFilterProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
