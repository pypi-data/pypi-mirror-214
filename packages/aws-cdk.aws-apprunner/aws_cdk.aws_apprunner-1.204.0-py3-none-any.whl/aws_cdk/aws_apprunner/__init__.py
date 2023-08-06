'''
# AWS::AppRunner Construct Library

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
import aws_cdk.aws_apprunner as apprunner
```

## Introduction

AWS App Runner is a fully managed service that makes it easy for developers to quickly deploy containerized web applications and APIs, at scale and with no prior infrastructure experience required. Start with your source code or a container image. App Runner automatically builds and deploys the web application and load balances traffic with encryption. App Runner also scales up or down automatically to meet your traffic needs. With App Runner, rather than thinking about servers or scaling, you have more time to focus on your applications.

## Service

The `Service` construct allows you to create AWS App Runner services with `ECR Public`, `ECR` or `Github` with the `source` property in the following scenarios:

* `Source.fromEcr()` - To define the source repository from `ECR`.
* `Source.fromEcrPublic()` - To define the source repository from `ECR Public`.
* `Source.fromGitHub()` - To define the source repository from the `Github repository`.
* `Source.fromAsset()` - To define the source from local asset directory.

## ECR Public

To create a `Service` with ECR Public:

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    )
)
```

## ECR

To create a `Service` from an existing ECR repository:

```python
import aws_cdk.aws_ecr as ecr


apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr(
        image_configuration=apprunner.ImageConfiguration(port=80),
        repository=ecr.Repository.from_repository_name(self, "NginxRepository", "nginx"),
        tag_or_digest="latest"
    )
)
```

To create a `Service` from local docker image asset directory  built and pushed to Amazon ECR:

```python
import aws_cdk.aws_ecr_assets as assets


image_asset = assets.DockerImageAsset(self, "ImageAssets",
    directory=path.join(__dirname, "./docker.assets")
)
apprunner.Service(self, "Service",
    source=apprunner.Source.from_asset(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        asset=image_asset
    )
)
```

## GitHub

To create a `Service` from the GitHub repository, you need to specify an existing App Runner `Connection`.

See [Managing App Runner connections](https://docs.aws.amazon.com/apprunner/latest/dg/manage-connections.html) for more details.

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_git_hub(
        repository_url="https://github.com/aws-containers/hello-app-runner",
        branch="main",
        configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
        connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
    )
)
```

Use `codeConfigurationValues` to override configuration values with the `API` configuration source type.

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_git_hub(
        repository_url="https://github.com/aws-containers/hello-app-runner",
        branch="main",
        configuration_source=apprunner.ConfigurationSourceType.API,
        code_configuration_values=apprunner.CodeConfigurationValues(
            runtime=apprunner.Runtime.PYTHON_3,
            port="8000",
            start_command="python app.py",
            build_command="yum install -y pycairo && pip install -r requirements.txt"
        ),
        connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
    )
)
```

## IAM Roles

You are allowed to define `instanceRole` and `accessRole` for the `Service`.

`instanceRole` - The IAM role that provides permissions to your App Runner service. These are permissions that
your code needs when it calls any AWS APIs.

`accessRole` - The IAM role that grants the App Runner service access to a source repository. It's required for
ECR image repositories (but not for ECR Public repositories). If not defined, a new access role will be generated
when required.

See [App Runner IAM Roles](https://docs.aws.amazon.com/apprunner/latest/dg/security_iam_service-with-iam.html#security_iam_service-with-iam-roles) for more details.

## VPC Connector

To associate an App Runner service with a custom VPC, define `vpcConnector` for the service.

```python
import aws_cdk.aws_ec2 as ec2


vpc = ec2.Vpc(self, "Vpc",
    cidr="10.0.0.0/16"
)

vpc_connector = apprunner.VpcConnector(self, "VpcConnector",
    vpc=vpc,
    vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC),
    vpc_connector_name="MyVpcConnector"
)

apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    vpc_connector=vpc_connector
)
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_093ed842
import aws_cdk.aws_ecr_assets as _aws_cdk_aws_ecr_assets_ef09b699
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.AssetProps",
    jsii_struct_bases=[],
    name_mapping={"asset": "asset", "image_configuration": "imageConfiguration"},
)
class AssetProps:
    def __init__(
        self,
        *,
        asset: _aws_cdk_aws_ecr_assets_ef09b699.DockerImageAsset,
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the image repository for ``Source.fromAsset()``.

        :param asset: (experimental) Represents the docker image asset.
        :param image_configuration: (experimental) The image configuration for the image built from the asset. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecr_assets as assets
            
            
            image_asset = assets.DockerImageAsset(self, "ImageAssets",
                directory=path.join(__dirname, "./docker.assets")
            )
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_asset(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    asset=image_asset
                )
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddacc297fe93219c04d7e04ff6fab0a907f6ada139e1217128d76f52964517f1)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset": asset,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def asset(self) -> _aws_cdk_aws_ecr_assets_ef09b699.DockerImageAsset:
        '''(experimental) Represents the docker image asset.

        :stability: experimental
        '''
        result = self._values.get("asset")
        assert result is not None, "Required property 'asset' is missing"
        return typing.cast(_aws_cdk_aws_ecr_assets_ef09b699.DockerImageAsset, result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) The image configuration for the image built from the asset.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnObservabilityConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.CfnObservabilityConfiguration",
):
    '''A CloudFormation ``AWS::AppRunner::ObservabilityConfiguration``.

    Specify an AWS App Runner observability configuration by using the ``AWS::AppRunner::ObservabilityConfiguration`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::ObservabilityConfiguration`` resource is an AWS App Runner resource type that specifies an App Runner observability configuration.

    App Runner requires this resource when you specify App Runner services and you want to enable non-default observability features. You can share an observability configuration across multiple services.

    Create multiple revisions of a configuration by specifying this resource multiple times using the same ``ObservabilityConfigurationName`` . App Runner creates multiple resources with incremental ``ObservabilityConfigurationRevision`` values. When you specify a service and configure an observability configuration resource, the service uses the latest active revision of the observability configuration by default. You can optionally configure the service to use a specific revision.

    The observability configuration resource is designed to configure multiple features (currently one feature, tracing). This resource takes optional parameters that describe the configuration of these features (currently one parameter, ``TraceConfiguration`` ). If you don't specify a feature parameter, App Runner doesn't enable the feature.

    :cloudformationResource: AWS::AppRunner::ObservabilityConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        cfn_observability_configuration = apprunner.CfnObservabilityConfiguration(self, "MyCfnObservabilityConfiguration",
            observability_configuration_name="observabilityConfigurationName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trace_configuration=apprunner.CfnObservabilityConfiguration.TraceConfigurationProperty(
                vendor="vendor"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        observability_configuration_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trace_configuration: typing.Optional[typing.Union[typing.Union["CfnObservabilityConfiguration.TraceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::AppRunner::ObservabilityConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param observability_configuration_name: A name for the observability configuration. When you use it for the first time in an AWS Region , App Runner creates revision number ``1`` of this name. When you use the same name in subsequent calls, App Runner creates incremental revisions of the configuration. .. epigraph:: The name ``DefaultConfiguration`` is reserved. You can't use it to create a new observability configuration, and you can't create a revision of it. When you want to use your own observability configuration for your App Runner service, *create a configuration with a different name* , and then provide it when you create or update your service. If you don't specify a name, AWS CloudFormation generates a name for your observability configuration.
        :param tags: A list of metadata items that you can associate with your observability configuration resource. A tag is a key-value pair.
        :param trace_configuration: The configuration of the tracing feature within this observability configuration. If you don't specify it, App Runner doesn't enable tracing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91bbfa645cb60714a2cc00c1efcaedbd7a9160b03212ae6dbc26fc692f8c01a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnObservabilityConfigurationProps(
            observability_configuration_name=observability_configuration_name,
            tags=tags,
            trace_configuration=trace_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c1b0e41f3ac21fe5acd7a0c3529ed9631cb9028d12af611e5c878764796952)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbefce63b0c29dcc23e08d3f09d8bd70b44ac5ce6971e970872f0453f60bbed5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLatest")
    def attr_latest(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''It's set to ``true`` for the configuration with the highest ``Revision`` among all configurations that share the same ``ObservabilityConfigurationName`` .

        It's set to ``false`` otherwise.

        :cloudformationAttribute: Latest
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrLatest"))

    @builtins.property
    @jsii.member(jsii_name="attrObservabilityConfigurationArn")
    def attr_observability_configuration_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of this observability configuration.

        :cloudformationAttribute: ObservabilityConfigurationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrObservabilityConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrObservabilityConfigurationRevision")
    def attr_observability_configuration_revision(self) -> jsii.Number:
        '''The revision of this observability configuration.

        It's unique among all the active configurations ( ``"Status": "ACTIVE"`` ) that share the same ``ObservabilityConfigurationName`` .

        :cloudformationAttribute: ObservabilityConfigurationRevision
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrObservabilityConfigurationRevision"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of metadata items that you can associate with your observability configuration resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationName")
    def observability_configuration_name(self) -> typing.Optional[builtins.str]:
        '''A name for the observability configuration.

        When you use it for the first time in an AWS Region , App Runner creates revision number ``1`` of this name. When you use the same name in subsequent calls, App Runner creates incremental revisions of the configuration.
        .. epigraph::

           The name ``DefaultConfiguration`` is reserved. You can't use it to create a new observability configuration, and you can't create a revision of it.

           When you want to use your own observability configuration for your App Runner service, *create a configuration with a different name* , and then provide it when you create or update your service.

        If you don't specify a name, AWS CloudFormation generates a name for your observability configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-observabilityconfigurationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "observabilityConfigurationName"))

    @observability_configuration_name.setter
    def observability_configuration_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb8958ed80ab2db90c622cdd8bb62345d408fbd455aadc3b1f8b1762773e89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "observabilityConfigurationName", value)

    @builtins.property
    @jsii.member(jsii_name="traceConfiguration")
    def trace_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnObservabilityConfiguration.TraceConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The configuration of the tracing feature within this observability configuration.

        If you don't specify it, App Runner doesn't enable tracing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-traceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnObservabilityConfiguration.TraceConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "traceConfiguration"))

    @trace_configuration.setter
    def trace_configuration(
        self,
        value: typing.Optional[typing.Union["CfnObservabilityConfiguration.TraceConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2743192fe969ee1bf389f3351e4cb3d6f0ba7a1becf18c1a645c4a9a4583e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnObservabilityConfiguration.TraceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vendor": "vendor"},
    )
    class TraceConfigurationProperty:
        def __init__(self, *, vendor: builtins.str) -> None:
            '''Describes the configuration of the tracing feature within an AWS App Runner observability configuration.

            :param vendor: The implementation provider chosen for tracing App Runner services.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-observabilityconfiguration-traceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                trace_configuration_property = apprunner.CfnObservabilityConfiguration.TraceConfigurationProperty(
                    vendor="vendor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e688456285b4d056d4db1f6b320235066e4121351f5717a2a508558147bc701b)
                check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "vendor": vendor,
            }

        @builtins.property
        def vendor(self) -> builtins.str:
            '''The implementation provider chosen for tracing App Runner services.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-observabilityconfiguration-traceconfiguration.html#cfn-apprunner-observabilityconfiguration-traceconfiguration-vendor
            '''
            result = self._values.get("vendor")
            assert result is not None, "Required property 'vendor' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TraceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CfnObservabilityConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "observability_configuration_name": "observabilityConfigurationName",
        "tags": "tags",
        "trace_configuration": "traceConfiguration",
    },
)
class CfnObservabilityConfigurationProps:
    def __init__(
        self,
        *,
        observability_configuration_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trace_configuration: typing.Optional[typing.Union[typing.Union[CfnObservabilityConfiguration.TraceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnObservabilityConfiguration``.

        :param observability_configuration_name: A name for the observability configuration. When you use it for the first time in an AWS Region , App Runner creates revision number ``1`` of this name. When you use the same name in subsequent calls, App Runner creates incremental revisions of the configuration. .. epigraph:: The name ``DefaultConfiguration`` is reserved. You can't use it to create a new observability configuration, and you can't create a revision of it. When you want to use your own observability configuration for your App Runner service, *create a configuration with a different name* , and then provide it when you create or update your service. If you don't specify a name, AWS CloudFormation generates a name for your observability configuration.
        :param tags: A list of metadata items that you can associate with your observability configuration resource. A tag is a key-value pair.
        :param trace_configuration: The configuration of the tracing feature within this observability configuration. If you don't specify it, App Runner doesn't enable tracing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            cfn_observability_configuration_props = apprunner.CfnObservabilityConfigurationProps(
                observability_configuration_name="observabilityConfigurationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trace_configuration=apprunner.CfnObservabilityConfiguration.TraceConfigurationProperty(
                    vendor="vendor"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5006d9251a2bd9f94a7b3eb3f2d290856b70e1dff5c62653e6a2c90b98a09487)
            check_type(argname="argument observability_configuration_name", value=observability_configuration_name, expected_type=type_hints["observability_configuration_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trace_configuration", value=trace_configuration, expected_type=type_hints["trace_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if observability_configuration_name is not None:
            self._values["observability_configuration_name"] = observability_configuration_name
        if tags is not None:
            self._values["tags"] = tags
        if trace_configuration is not None:
            self._values["trace_configuration"] = trace_configuration

    @builtins.property
    def observability_configuration_name(self) -> typing.Optional[builtins.str]:
        '''A name for the observability configuration.

        When you use it for the first time in an AWS Region , App Runner creates revision number ``1`` of this name. When you use the same name in subsequent calls, App Runner creates incremental revisions of the configuration.
        .. epigraph::

           The name ``DefaultConfiguration`` is reserved. You can't use it to create a new observability configuration, and you can't create a revision of it.

           When you want to use your own observability configuration for your App Runner service, *create a configuration with a different name* , and then provide it when you create or update your service.

        If you don't specify a name, AWS CloudFormation generates a name for your observability configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-observabilityconfigurationname
        '''
        result = self._values.get("observability_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of metadata items that you can associate with your observability configuration resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def trace_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnObservabilityConfiguration.TraceConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The configuration of the tracing feature within this observability configuration.

        If you don't specify it, App Runner doesn't enable tracing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-traceconfiguration
        '''
        result = self._values.get("trace_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnObservabilityConfiguration.TraceConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnObservabilityConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnService(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.CfnService",
):
    '''A CloudFormation ``AWS::AppRunner::Service``.

    Specify an AWS App Runner service by using the ``AWS::AppRunner::Service`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::Service`` resource is an AWS App Runner resource type that specifies an App Runner service.

    :cloudformationResource: AWS::AppRunner::Service
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        cfn_service = apprunner.CfnService(self, "MyCfnService",
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn="accessRoleArn",
                    connection_arn="connectionArn"
                ),
                auto_deployments_enabled=False,
                code_repository=apprunner.CfnService.CodeRepositoryProperty(
                    repository_url="repositoryUrl",
                    source_code_version=apprunner.CfnService.SourceCodeVersionProperty(
                        type="type",
                        value="value"
                    ),
        
                    # the properties below are optional
                    code_configuration=apprunner.CfnService.CodeConfigurationProperty(
                        configuration_source="configurationSource",
        
                        # the properties below are optional
                        code_configuration_values=apprunner.CfnService.CodeConfigurationValuesProperty(
                            runtime="runtime",
        
                            # the properties below are optional
                            build_command="buildCommand",
                            port="port",
                            runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        )
                    )
                ),
                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier="imageIdentifier",
                    image_repository_type="imageRepositoryType",
        
                    # the properties below are optional
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="port",
                        runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        start_command="startCommand"
                    )
                )
            ),
        
            # the properties below are optional
            auto_scaling_configuration_arn="autoScalingConfigurationArn",
            encryption_configuration=apprunner.CfnService.EncryptionConfigurationProperty(
                kms_key="kmsKey"
            ),
            health_check_configuration=apprunner.CfnService.HealthCheckConfigurationProperty(
                healthy_threshold=123,
                interval=123,
                path="path",
                protocol="protocol",
                timeout=123,
                unhealthy_threshold=123
            ),
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                cpu="cpu",
                instance_role_arn="instanceRoleArn",
                memory="memory"
            ),
            network_configuration=apprunner.CfnService.NetworkConfigurationProperty(
                egress_configuration=apprunner.CfnService.EgressConfigurationProperty(
                    egress_type="egressType",
        
                    # the properties below are optional
                    vpc_connector_arn="vpcConnectorArn"
                ),
                ingress_configuration=apprunner.CfnService.IngressConfigurationProperty(
                    is_publicly_accessible=False
                )
            ),
            observability_configuration=apprunner.CfnService.ServiceObservabilityConfigurationProperty(
                observability_enabled=False,
        
                # the properties below are optional
                observability_configuration_arn="observabilityConfigurationArn"
            ),
            service_name="serviceName",
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
        source_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.HealthCheckConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.InstanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        observability_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.ServiceObservabilityConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppRunner::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param source_configuration: The source to deploy to the App Runner service. It can be a code or an image repository.
        :param auto_scaling_configuration_arn: The Amazon Resource Name (ARN) of an App Runner automatic scaling configuration resource that you want to associate with your service. If not provided, App Runner associates the latest revision of a default auto scaling configuration. Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3`` Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability``
        :param encryption_configuration: An optional custom encryption key that App Runner uses to encrypt the copy of your source repository that it maintains and your service logs. By default, App Runner uses an AWS managed key .
        :param health_check_configuration: The settings for the health check that AWS App Runner performs to monitor the health of the App Runner service.
        :param instance_configuration: The runtime configuration of instances (scaling units) of your service.
        :param network_configuration: Configuration settings related to network traffic of the web application that the App Runner service runs.
        :param observability_configuration: The observability configuration of your service.
        :param service_name: A name for the App Runner service. It must be unique across all the running App Runner services in your AWS account in the AWS Region . If you don't specify a name, AWS CloudFormation generates a name for your service.
        :param tags: An optional list of metadata items that you can associate with the App Runner service resource. A tag is a key-value pair.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca87c4c8a5746257f1f031ee66a2bfe0b8a2c7e9289c0d5b8b26d10936612be7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceProps(
            source_configuration=source_configuration,
            auto_scaling_configuration_arn=auto_scaling_configuration_arn,
            encryption_configuration=encryption_configuration,
            health_check_configuration=health_check_configuration,
            instance_configuration=instance_configuration,
            network_configuration=network_configuration,
            observability_configuration=observability_configuration,
            service_name=service_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547576c08be1741ea36e95890335fe2c9153bb9a6b515f44d3603dec97cbe3d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec349bad48c3086954344e9594ae3c14895d98d124287d1c058bed1bfd7715f4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceArn")
    def attr_service_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of this service.

        :cloudformationAttribute: ServiceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceId")
    def attr_service_id(self) -> builtins.str:
        '''An ID that App Runner generated for this service.

        It's unique within the AWS Region .

        :cloudformationAttribute: ServiceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceUrl")
    def attr_service_url(self) -> builtins.str:
        '''A subdomain URL that App Runner generated for this service.

        You can use this URL to access your service web application.

        :cloudformationAttribute: ServiceUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceUrl"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current state of the App Runner service. These particular values mean the following.

        - ``CREATE_FAILED`` – The service failed to create. To troubleshoot this failure, read the failure events and logs, change any parameters that need to be fixed, and retry the call to create the service.

        The failed service isn't usable, and still counts towards your service quota. When you're done analyzing the failure, delete the service.

        - ``DELETE_FAILED`` – The service failed to delete and can't be successfully recovered. Retry the service deletion call to ensure that all related resources are removed.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An optional list of metadata items that you can associate with the App Runner service resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="sourceConfiguration")
    def source_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.SourceConfigurationProperty"]:
        '''The source to deploy to the App Runner service.

        It can be a code or an image repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-sourceconfiguration
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.SourceConfigurationProperty"], jsii.get(self, "sourceConfiguration"))

    @source_configuration.setter
    def source_configuration(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.SourceConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04aa5ea8f4ead0e9147eafd0b549206a0a7878e1c67cee1a341049e9a20ce3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationArn")
    def auto_scaling_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an App Runner automatic scaling configuration resource that you want to associate with your service.

        If not provided, App Runner associates the latest revision of a default auto scaling configuration.

        Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3``

        Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-autoscalingconfigurationarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoScalingConfigurationArn"))

    @auto_scaling_configuration_arn.setter
    def auto_scaling_configuration_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75325d1dc127a3f83d249b5ddf1ecffe588776ee0037565d82575fa3d10b9778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.EncryptionConfigurationProperty"]]:
        '''An optional custom encryption key that App Runner uses to encrypt the copy of your source repository that it maintains and your service logs.

        By default, App Runner uses an AWS managed key .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-encryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.EncryptionConfigurationProperty"]], jsii.get(self, "encryptionConfiguration"))

    @encryption_configuration.setter
    def encryption_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.EncryptionConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f7f823c7e715271f924a6936d0e308dfeaf4add0b7b1d350bc64b9ae37ba04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckConfiguration")
    def health_check_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckConfigurationProperty"]]:
        '''The settings for the health check that AWS App Runner performs to monitor the health of the App Runner service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-healthcheckconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckConfigurationProperty"]], jsii.get(self, "healthCheckConfiguration"))

    @health_check_configuration.setter
    def health_check_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edfd79cd0489e028f07de9f7918aff6728ddb101dee5acad6ba14b7e8110fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="instanceConfiguration")
    def instance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.InstanceConfigurationProperty"]]:
        '''The runtime configuration of instances (scaling units) of your service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-instanceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.InstanceConfigurationProperty"]], jsii.get(self, "instanceConfiguration"))

    @instance_configuration.setter
    def instance_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.InstanceConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fb20e04cc7053efa05959e4b0607b8ffc7fcd567e18cc4281e9137bcdc72eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.NetworkConfigurationProperty"]]:
        '''Configuration settings related to network traffic of the web application that the App Runner service runs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-networkconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.NetworkConfigurationProperty"]], jsii.get(self, "networkConfiguration"))

    @network_configuration.setter
    def network_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.NetworkConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b0aa228b668fcd763ec6f282077b94f2d668acf7492cdb4652739248368318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="observabilityConfiguration")
    def observability_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ServiceObservabilityConfigurationProperty"]]:
        '''The observability configuration of your service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-observabilityconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ServiceObservabilityConfigurationProperty"]], jsii.get(self, "observabilityConfiguration"))

    @observability_configuration.setter
    def observability_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ServiceObservabilityConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7b43fb251c201d3b5ea62af96de0e94c815b748bdc0d578941b0c6cd5b95f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "observabilityConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> typing.Optional[builtins.str]:
        '''A name for the App Runner service.

        It must be unique across all the running App Runner services in your AWS account in the AWS Region .

        If you don't specify a name, AWS CloudFormation generates a name for your service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-servicename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5b37f8b1d7adda1b3a9146dbcdb07ab7eb9a60dff4003bca4e06fb8f70cb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.AuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_role_arn": "accessRoleArn",
            "connection_arn": "connectionArn",
        },
    )
    class AuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            access_role_arn: typing.Optional[builtins.str] = None,
            connection_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes resources needed to authenticate access to some source repositories.

            The specific resource depends on the repository provider.

            :param access_role_arn: The Amazon Resource Name (ARN) of the IAM role that grants the App Runner service access to a source repository. It's required for ECR image repositories (but not for ECR Public repositories).
            :param connection_arn: The Amazon Resource Name (ARN) of the App Runner connection that enables the App Runner service to connect to a source repository. It's required for GitHub code repositories.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-authenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                authentication_configuration_property = apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn="accessRoleArn",
                    connection_arn="connectionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3ff72239e8344d1f54c0457d22ea928fd2f4ff4064c7a83bd550e28292ca236)
                check_type(argname="argument access_role_arn", value=access_role_arn, expected_type=type_hints["access_role_arn"])
                check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_role_arn is not None:
                self._values["access_role_arn"] = access_role_arn
            if connection_arn is not None:
                self._values["connection_arn"] = connection_arn

        @builtins.property
        def access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that grants the App Runner service access to a source repository.

            It's required for ECR image repositories (but not for ECR Public repositories).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-authenticationconfiguration.html#cfn-apprunner-service-authenticationconfiguration-accessrolearn
            '''
            result = self._values.get("access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the App Runner connection that enables the App Runner service to connect to a source repository.

            It's required for GitHub code repositories.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-authenticationconfiguration.html#cfn-apprunner-service-authenticationconfiguration-connectionarn
            '''
            result = self._values.get("connection_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.CodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_source": "configurationSource",
            "code_configuration_values": "codeConfigurationValues",
        },
    )
    class CodeConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_source: builtins.str,
            code_configuration_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.CodeConfigurationValuesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration that AWS App Runner uses to build and run an App Runner service from a source code repository.

            :param configuration_source: The source of the App Runner configuration. Values are interpreted as follows:. - ``REPOSITORY`` – App Runner reads configuration values from the ``apprunner.yaml`` file in the source code repository and ignores ``CodeConfigurationValues`` . - ``API`` – App Runner uses configuration values provided in ``CodeConfigurationValues`` and ignores the ``apprunner.yaml`` file in the source code repository.
            :param code_configuration_values: The basic configuration for building and running the App Runner service. Use it to quickly launch an App Runner service without providing a ``apprunner.yaml`` file in the source code repository (or ignoring the file if it exists).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                code_configuration_property = apprunner.CfnService.CodeConfigurationProperty(
                    configuration_source="configurationSource",
                
                    # the properties below are optional
                    code_configuration_values=apprunner.CfnService.CodeConfigurationValuesProperty(
                        runtime="runtime",
                
                        # the properties below are optional
                        build_command="buildCommand",
                        port="port",
                        runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        start_command="startCommand"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46b629437d011e0488747601a2b36a41c997667dbb59b98ee4def4ab91e4888b)
                check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
                check_type(argname="argument code_configuration_values", value=code_configuration_values, expected_type=type_hints["code_configuration_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "configuration_source": configuration_source,
            }
            if code_configuration_values is not None:
                self._values["code_configuration_values"] = code_configuration_values

        @builtins.property
        def configuration_source(self) -> builtins.str:
            '''The source of the App Runner configuration. Values are interpreted as follows:.

            - ``REPOSITORY`` – App Runner reads configuration values from the ``apprunner.yaml`` file in the source code repository and ignores ``CodeConfigurationValues`` .
            - ``API`` – App Runner uses configuration values provided in ``CodeConfigurationValues`` and ignores the ``apprunner.yaml`` file in the source code repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html#cfn-apprunner-service-codeconfiguration-configurationsource
            '''
            result = self._values.get("configuration_source")
            assert result is not None, "Required property 'configuration_source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def code_configuration_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.CodeConfigurationValuesProperty"]]:
            '''The basic configuration for building and running the App Runner service.

            Use it to quickly launch an App Runner service without providing a ``apprunner.yaml`` file in the source code repository (or ignoring the file if it exists).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html#cfn-apprunner-service-codeconfiguration-codeconfigurationvalues
            '''
            result = self._values.get("code_configuration_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.CodeConfigurationValuesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.CodeConfigurationValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "runtime": "runtime",
            "build_command": "buildCommand",
            "port": "port",
            "runtime_environment_secrets": "runtimeEnvironmentSecrets",
            "runtime_environment_variables": "runtimeEnvironmentVariables",
            "start_command": "startCommand",
        },
    )
    class CodeConfigurationValuesProperty:
        def __init__(
            self,
            *,
            runtime: builtins.str,
            build_command: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            start_command: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the basic configuration needed for building and running an AWS App Runner service.

            This type doesn't support the full set of possible configuration options. Fur full configuration capabilities, use a ``apprunner.yaml`` file in the source code repository.

            :param runtime: A runtime environment type for building and running an App Runner service. It represents a programming language runtime.
            :param build_command: The command App Runner runs to build your application.
            :param port: The port that your application listens to in the container. Default: ``8080``
            :param runtime_environment_secrets: ``CfnService.CodeConfigurationValuesProperty.RuntimeEnvironmentSecrets``.
            :param runtime_environment_variables: The environment variables that are available to your running AWS App Runner service. An array of key-value pairs.
            :param start_command: The command App Runner runs to start your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                code_configuration_values_property = apprunner.CfnService.CodeConfigurationValuesProperty(
                    runtime="runtime",
                
                    # the properties below are optional
                    build_command="buildCommand",
                    port="port",
                    runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    start_command="startCommand"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8a924d82fad65a222b6da4bb5f29304a69e7ef2d58eaafd3ba9f599de11b7bf)
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
                check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument runtime_environment_secrets", value=runtime_environment_secrets, expected_type=type_hints["runtime_environment_secrets"])
                check_type(argname="argument runtime_environment_variables", value=runtime_environment_variables, expected_type=type_hints["runtime_environment_variables"])
                check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "runtime": runtime,
            }
            if build_command is not None:
                self._values["build_command"] = build_command
            if port is not None:
                self._values["port"] = port
            if runtime_environment_secrets is not None:
                self._values["runtime_environment_secrets"] = runtime_environment_secrets
            if runtime_environment_variables is not None:
                self._values["runtime_environment_variables"] = runtime_environment_variables
            if start_command is not None:
                self._values["start_command"] = start_command

        @builtins.property
        def runtime(self) -> builtins.str:
            '''A runtime environment type for building and running an App Runner service.

            It represents a programming language runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtime
            '''
            result = self._values.get("runtime")
            assert result is not None, "Required property 'runtime' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def build_command(self) -> typing.Optional[builtins.str]:
            '''The command App Runner runs to build your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-buildcommand
            '''
            result = self._values.get("build_command")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port that your application listens to in the container.

            Default: ``8080``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_environment_secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]]:
            '''``CfnService.CodeConfigurationValuesProperty.RuntimeEnvironmentSecrets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtimeenvironmentsecrets
            '''
            result = self._values.get("runtime_environment_secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]], result)

        @builtins.property
        def runtime_environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]]:
            '''The environment variables that are available to your running AWS App Runner service.

            An array of key-value pairs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtimeenvironmentvariables
            '''
            result = self._values.get("runtime_environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]], result)

        @builtins.property
        def start_command(self) -> typing.Optional[builtins.str]:
            '''The command App Runner runs to start your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-startcommand
            '''
            result = self._values.get("start_command")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeConfigurationValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.CodeRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "repository_url": "repositoryUrl",
            "source_code_version": "sourceCodeVersion",
            "code_configuration": "codeConfiguration",
        },
    )
    class CodeRepositoryProperty:
        def __init__(
            self,
            *,
            repository_url: builtins.str,
            source_code_version: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.SourceCodeVersionProperty", typing.Dict[builtins.str, typing.Any]]],
            code_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.CodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a source code repository.

            :param repository_url: The location of the repository that contains the source code.
            :param source_code_version: The version that should be used within the source code repository.
            :param code_configuration: Configuration for building and running the service from a source code repository. .. epigraph:: ``CodeConfiguration`` is required only for ``CreateService`` request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                code_repository_property = apprunner.CfnService.CodeRepositoryProperty(
                    repository_url="repositoryUrl",
                    source_code_version=apprunner.CfnService.SourceCodeVersionProperty(
                        type="type",
                        value="value"
                    ),
                
                    # the properties below are optional
                    code_configuration=apprunner.CfnService.CodeConfigurationProperty(
                        configuration_source="configurationSource",
                
                        # the properties below are optional
                        code_configuration_values=apprunner.CfnService.CodeConfigurationValuesProperty(
                            runtime="runtime",
                
                            # the properties below are optional
                            build_command="buildCommand",
                            port="port",
                            runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__374635dcd80b1052600a921ff860a5dc9cddf1f067dc7836330305298af2cc37)
                check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
                check_type(argname="argument source_code_version", value=source_code_version, expected_type=type_hints["source_code_version"])
                check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "repository_url": repository_url,
                "source_code_version": source_code_version,
            }
            if code_configuration is not None:
                self._values["code_configuration"] = code_configuration

        @builtins.property
        def repository_url(self) -> builtins.str:
            '''The location of the repository that contains the source code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-repositoryurl
            '''
            result = self._values.get("repository_url")
            assert result is not None, "Required property 'repository_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_code_version(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.SourceCodeVersionProperty"]:
            '''The version that should be used within the source code repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-sourcecodeversion
            '''
            result = self._values.get("source_code_version")
            assert result is not None, "Required property 'source_code_version' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.SourceCodeVersionProperty"], result)

        @builtins.property
        def code_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.CodeConfigurationProperty"]]:
            '''Configuration for building and running the service from a source code repository.

            .. epigraph::

               ``CodeConfiguration`` is required only for ``CreateService`` request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-codeconfiguration
            '''
            result = self._values.get("code_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.CodeConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.EgressConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "egress_type": "egressType",
            "vpc_connector_arn": "vpcConnectorArn",
        },
    )
    class EgressConfigurationProperty:
        def __init__(
            self,
            *,
            egress_type: builtins.str,
            vpc_connector_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes configuration settings related to outbound network traffic of an AWS App Runner service.

            :param egress_type: The type of egress configuration. Set to ``DEFAULT`` for access to resources hosted on public networks. Set to ``VPC`` to associate your service to a custom VPC specified by ``VpcConnectorArn`` .
            :param vpc_connector_arn: The Amazon Resource Name (ARN) of the App Runner VPC connector that you want to associate with your App Runner service. Only valid when ``EgressType = VPC`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-egressconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                egress_configuration_property = apprunner.CfnService.EgressConfigurationProperty(
                    egress_type="egressType",
                
                    # the properties below are optional
                    vpc_connector_arn="vpcConnectorArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fec5bd61d7e0974df6a89f0c9598d7a19e5d388769a755b8fbdd12c58f9e8eac)
                check_type(argname="argument egress_type", value=egress_type, expected_type=type_hints["egress_type"])
                check_type(argname="argument vpc_connector_arn", value=vpc_connector_arn, expected_type=type_hints["vpc_connector_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "egress_type": egress_type,
            }
            if vpc_connector_arn is not None:
                self._values["vpc_connector_arn"] = vpc_connector_arn

        @builtins.property
        def egress_type(self) -> builtins.str:
            '''The type of egress configuration.

            Set to ``DEFAULT`` for access to resources hosted on public networks.

            Set to ``VPC`` to associate your service to a custom VPC specified by ``VpcConnectorArn`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-egressconfiguration.html#cfn-apprunner-service-egressconfiguration-egresstype
            '''
            result = self._values.get("egress_type")
            assert result is not None, "Required property 'egress_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpc_connector_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the App Runner VPC connector that you want to associate with your App Runner service.

            Only valid when ``EgressType = VPC`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-egressconfiguration.html#cfn-apprunner-service-egressconfiguration-vpcconnectorarn
            '''
            result = self._values.get("vpc_connector_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(self, *, kms_key: builtins.str) -> None:
            '''Describes a custom encryption key that AWS App Runner uses to encrypt copies of the source repository and service logs.

            :param kms_key: The ARN of the KMS key that's used for encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                encryption_configuration_property = apprunner.CfnService.EncryptionConfigurationProperty(
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb220ec07370c696e17f8ad5c47a6aacc7ae57533a5b228597bf07621cb0b586)
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "kms_key": kms_key,
            }

        @builtins.property
        def kms_key(self) -> builtins.str:
            '''The ARN of the KMS key that's used for encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-encryptionconfiguration.html#cfn-apprunner-service-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            assert result is not None, "Required property 'kms_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.HealthCheckConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval": "interval",
            "path": "path",
            "protocol": "protocol",
            "timeout": "timeout",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckConfigurationProperty:
        def __init__(
            self,
            *,
            healthy_threshold: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            path: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            timeout: typing.Optional[jsii.Number] = None,
            unhealthy_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the settings for the health check that AWS App Runner performs to monitor the health of a service.

            :param healthy_threshold: The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Default: ``1``
            :param interval: The time interval, in seconds, between health checks. Default: ``5``
            :param path: The URL that health check requests are sent to. ``Path`` is only applicable when you set ``Protocol`` to ``HTTP`` . Default: ``"/"``
            :param protocol: The IP protocol that App Runner uses to perform health checks for your service. If you set ``Protocol`` to ``HTTP`` , App Runner sends health check requests to the HTTP path specified by ``Path`` . Default: ``TCP``
            :param timeout: The time, in seconds, to wait for a health check response before deciding it failed. Default: ``2``
            :param unhealthy_threshold: The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Default: ``5``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                health_check_configuration_property = apprunner.CfnService.HealthCheckConfigurationProperty(
                    healthy_threshold=123,
                    interval=123,
                    path="path",
                    protocol="protocol",
                    timeout=123,
                    unhealthy_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33c435d9b0fc5c3eb53afa0a4165fffd0bc5bd44df2d43b45ade3f645ef9f4a7)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if healthy_threshold is not None:
                self._values["healthy_threshold"] = healthy_threshold
            if interval is not None:
                self._values["interval"] = interval
            if path is not None:
                self._values["path"] = path
            if protocol is not None:
                self._values["protocol"] = protocol
            if timeout is not None:
                self._values["timeout"] = timeout
            if unhealthy_threshold is not None:
                self._values["unhealthy_threshold"] = unhealthy_threshold

        @builtins.property
        def healthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive checks that must succeed before App Runner decides that the service is healthy.

            Default: ``1``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The time interval, in seconds, between health checks.

            Default: ``5``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The URL that health check requests are sent to.

            ``Path`` is only applicable when you set ``Protocol`` to ``HTTP`` .

            Default: ``"/"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The IP protocol that App Runner uses to perform health checks for your service.

            If you set ``Protocol`` to ``HTTP`` , App Runner sends health check requests to the HTTP path specified by ``Path`` .

            Default: ``TCP``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The time, in seconds, to wait for a health check response before deciding it failed.

            Default: ``2``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive checks that must fail before App Runner decides that the service is unhealthy.

            Default: ``5``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.ImageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port": "port",
            "runtime_environment_secrets": "runtimeEnvironmentSecrets",
            "runtime_environment_variables": "runtimeEnvironmentVariables",
            "start_command": "startCommand",
        },
    )
    class ImageConfigurationProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[builtins.str] = None,
            runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            start_command: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration that AWS App Runner uses to run an App Runner service using an image pulled from a source image repository.

            :param port: The port that your application listens to in the container. Default: ``8080``
            :param runtime_environment_secrets: ``CfnService.ImageConfigurationProperty.RuntimeEnvironmentSecrets``.
            :param runtime_environment_variables: Environment variables that are available to your running App Runner service. An array of key-value pairs.
            :param start_command: An optional command that App Runner runs to start the application in the source image. If specified, this command overrides the Docker image’s default start command.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                image_configuration_property = apprunner.CfnService.ImageConfigurationProperty(
                    port="port",
                    runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    start_command="startCommand"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d01630e9ae8e9d018b18c37dbba5e9248590be83574b21ec31433b551883b51)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument runtime_environment_secrets", value=runtime_environment_secrets, expected_type=type_hints["runtime_environment_secrets"])
                check_type(argname="argument runtime_environment_variables", value=runtime_environment_variables, expected_type=type_hints["runtime_environment_variables"])
                check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if runtime_environment_secrets is not None:
                self._values["runtime_environment_secrets"] = runtime_environment_secrets
            if runtime_environment_variables is not None:
                self._values["runtime_environment_variables"] = runtime_environment_variables
            if start_command is not None:
                self._values["start_command"] = start_command

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port that your application listens to in the container.

            Default: ``8080``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_environment_secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]]:
            '''``CfnService.ImageConfigurationProperty.RuntimeEnvironmentSecrets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-runtimeenvironmentsecrets
            '''
            result = self._values.get("runtime_environment_secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]], result)

        @builtins.property
        def runtime_environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]]:
            '''Environment variables that are available to your running App Runner service.

            An array of key-value pairs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-runtimeenvironmentvariables
            '''
            result = self._values.get("runtime_environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.KeyValuePairProperty"]]]], result)

        @builtins.property
        def start_command(self) -> typing.Optional[builtins.str]:
            '''An optional command that App Runner runs to start the application in the source image.

            If specified, this command overrides the Docker image’s default start command.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-startcommand
            '''
            result = self._values.get("start_command")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.ImageRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_identifier": "imageIdentifier",
            "image_repository_type": "imageRepositoryType",
            "image_configuration": "imageConfiguration",
        },
    )
    class ImageRepositoryProperty:
        def __init__(
            self,
            *,
            image_identifier: builtins.str,
            image_repository_type: builtins.str,
            image_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.ImageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a source image repository.

            :param image_identifier: The identifier of an image. For an image in Amazon Elastic Container Registry (Amazon ECR), this is an image name. For the image name format, see `Pulling an image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html>`_ in the *Amazon ECR User Guide* .
            :param image_repository_type: The type of the image repository. This reflects the repository provider and whether the repository is private or public.
            :param image_configuration: Configuration for running the identified image.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                image_repository_property = apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier="imageIdentifier",
                    image_repository_type="imageRepositoryType",
                
                    # the properties below are optional
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="port",
                        runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        start_command="startCommand"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c71a33070cb9b5bbb6e9f771bdb2aabdf33e0faf15548869abe6dfd34e40037e)
                check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
                check_type(argname="argument image_repository_type", value=image_repository_type, expected_type=type_hints["image_repository_type"])
                check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "image_identifier": image_identifier,
                "image_repository_type": image_repository_type,
            }
            if image_configuration is not None:
                self._values["image_configuration"] = image_configuration

        @builtins.property
        def image_identifier(self) -> builtins.str:
            '''The identifier of an image.

            For an image in Amazon Elastic Container Registry (Amazon ECR), this is an image name. For the image name format, see `Pulling an image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html>`_ in the *Amazon ECR User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html#cfn-apprunner-service-imagerepository-imageidentifier
            '''
            result = self._values.get("image_identifier")
            assert result is not None, "Required property 'image_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def image_repository_type(self) -> builtins.str:
            '''The type of the image repository.

            This reflects the repository provider and whether the repository is private or public.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html#cfn-apprunner-service-imagerepository-imagerepositorytype
            '''
            result = self._values.get("image_repository_type")
            assert result is not None, "Required property 'image_repository_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def image_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ImageConfigurationProperty"]]:
            '''Configuration for running the identified image.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html#cfn-apprunner-service-imagerepository-imageconfiguration
            '''
            result = self._values.get("image_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ImageConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.IngressConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"is_publicly_accessible": "isPubliclyAccessible"},
    )
    class IngressConfigurationProperty:
        def __init__(
            self,
            *,
            is_publicly_accessible: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Network configuration settings for inbound network traffic.

            :param is_publicly_accessible: Specifies whether your App Runner service is publicly accessible. To make the service publicly accessible set it to ``True`` . To make the service privately accessible, from only within an Amazon VPC set it to ``False`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-ingressconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                ingress_configuration_property = apprunner.CfnService.IngressConfigurationProperty(
                    is_publicly_accessible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fe4078e36c2e7a9a71cafd7db3dd196480c0ef67164ff3ccc4072be96903722)
                check_type(argname="argument is_publicly_accessible", value=is_publicly_accessible, expected_type=type_hints["is_publicly_accessible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "is_publicly_accessible": is_publicly_accessible,
            }

        @builtins.property
        def is_publicly_accessible(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Specifies whether your App Runner service is publicly accessible.

            To make the service publicly accessible set it to ``True`` . To make the service privately accessible, from only within an Amazon VPC set it to ``False`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-ingressconfiguration.html#cfn-apprunner-service-ingressconfiguration-ispubliclyaccessible
            '''
            result = self._values.get("is_publicly_accessible")
            assert result is not None, "Required property 'is_publicly_accessible' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.InstanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu": "cpu",
            "instance_role_arn": "instanceRoleArn",
            "memory": "memory",
        },
    )
    class InstanceConfigurationProperty:
        def __init__(
            self,
            *,
            cpu: typing.Optional[builtins.str] = None,
            instance_role_arn: typing.Optional[builtins.str] = None,
            memory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the runtime configuration of an AWS App Runner service instance (scaling unit).

            :param cpu: The number of CPU units reserved for each instance of your App Runner service. Default: ``1 vCPU``
            :param instance_role_arn: The Amazon Resource Name (ARN) of an IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs.
            :param memory: The amount of memory, in MB or GB, reserved for each instance of your App Runner service. Default: ``2 GB``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                instance_configuration_property = apprunner.CfnService.InstanceConfigurationProperty(
                    cpu="cpu",
                    instance_role_arn="instanceRoleArn",
                    memory="memory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f3ebf4b817bcda9604c899ffa1984838dca0c5a3d1a28d6946fec06f6c299c7)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument instance_role_arn", value=instance_role_arn, expected_type=type_hints["instance_role_arn"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu is not None:
                self._values["cpu"] = cpu
            if instance_role_arn is not None:
                self._values["instance_role_arn"] = instance_role_arn
            if memory is not None:
                self._values["memory"] = memory

        @builtins.property
        def cpu(self) -> typing.Optional[builtins.str]:
            '''The number of CPU units reserved for each instance of your App Runner service.

            Default: ``1 vCPU``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role that provides permissions to your App Runner service.

            These are permissions that your code needs when it calls any AWS APIs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-instancerolearn
            '''
            result = self._values.get("instance_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory(self) -> typing.Optional[builtins.str]:
            '''The amount of memory, in MB or GB, reserved for each instance of your App Runner service.

            Default: ``2 GB``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.KeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class KeyValuePairProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a key-value pair, which is a string-to-string mapping.

            :param name: The key name string to map to a value.
            :param value: The value string to which the key name is mapped.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-keyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                key_value_pair_property = apprunner.CfnService.KeyValuePairProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5456e7d808e1c66f2f521c909f7c779ae5a6e91dc8a7a7ecfcefd1c568833785)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The key name string to map to a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-keyvaluepair.html#cfn-apprunner-service-keyvaluepair-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value string to which the key name is mapped.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-keyvaluepair.html#cfn-apprunner-service-keyvaluepair-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "egress_configuration": "egressConfiguration",
            "ingress_configuration": "ingressConfiguration",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            egress_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.EgressConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ingress_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.IngressConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes configuration settings related to network traffic of an AWS App Runner service.

            Consists of embedded objects for each configurable network feature.

            :param egress_configuration: Network configuration settings for outbound message traffic.
            :param ingress_configuration: Network configuration settings for inbound message traffic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                network_configuration_property = apprunner.CfnService.NetworkConfigurationProperty(
                    egress_configuration=apprunner.CfnService.EgressConfigurationProperty(
                        egress_type="egressType",
                
                        # the properties below are optional
                        vpc_connector_arn="vpcConnectorArn"
                    ),
                    ingress_configuration=apprunner.CfnService.IngressConfigurationProperty(
                        is_publicly_accessible=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59588ba677d357eacb99cc8b8467288391194ff592d620f28fcd13766d5330bd)
                check_type(argname="argument egress_configuration", value=egress_configuration, expected_type=type_hints["egress_configuration"])
                check_type(argname="argument ingress_configuration", value=ingress_configuration, expected_type=type_hints["ingress_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if egress_configuration is not None:
                self._values["egress_configuration"] = egress_configuration
            if ingress_configuration is not None:
                self._values["ingress_configuration"] = ingress_configuration

        @builtins.property
        def egress_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.EgressConfigurationProperty"]]:
            '''Network configuration settings for outbound message traffic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html#cfn-apprunner-service-networkconfiguration-egressconfiguration
            '''
            result = self._values.get("egress_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.EgressConfigurationProperty"]], result)

        @builtins.property
        def ingress_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.IngressConfigurationProperty"]]:
            '''Network configuration settings for inbound message traffic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html#cfn-apprunner-service-networkconfiguration-ingressconfiguration
            '''
            result = self._values.get("ingress_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.IngressConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.ServiceObservabilityConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "observability_enabled": "observabilityEnabled",
            "observability_configuration_arn": "observabilityConfigurationArn",
        },
    )
    class ServiceObservabilityConfigurationProperty:
        def __init__(
            self,
            *,
            observability_enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            observability_configuration_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the observability configuration of an AWS App Runner service.

            These are additional observability features, like tracing, that you choose to enable. They're configured in a separate resource that you associate with your service.

            :param observability_enabled: When ``true`` , an observability configuration resource is associated with the service, and an ``ObservabilityConfigurationArn`` is specified.
            :param observability_configuration_arn: The Amazon Resource Name (ARN) of the observability configuration that is associated with the service. Specified only when ``ObservabilityEnabled`` is ``true`` . Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing/3`` Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-serviceobservabilityconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                service_observability_configuration_property = apprunner.CfnService.ServiceObservabilityConfigurationProperty(
                    observability_enabled=False,
                
                    # the properties below are optional
                    observability_configuration_arn="observabilityConfigurationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dcd73b0f9c754b973a3d13c12b968f44cb18d6ef6062b4fcdbcf7087b6fcabb)
                check_type(argname="argument observability_enabled", value=observability_enabled, expected_type=type_hints["observability_enabled"])
                check_type(argname="argument observability_configuration_arn", value=observability_configuration_arn, expected_type=type_hints["observability_configuration_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "observability_enabled": observability_enabled,
            }
            if observability_configuration_arn is not None:
                self._values["observability_configuration_arn"] = observability_configuration_arn

        @builtins.property
        def observability_enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''When ``true`` , an observability configuration resource is associated with the service, and an ``ObservabilityConfigurationArn`` is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-serviceobservabilityconfiguration.html#cfn-apprunner-service-serviceobservabilityconfiguration-observabilityenabled
            '''
            result = self._values.get("observability_enabled")
            assert result is not None, "Required property 'observability_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def observability_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the observability configuration that is associated with the service.

            Specified only when ``ObservabilityEnabled`` is ``true`` .

            Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing/3``

            Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-serviceobservabilityconfiguration.html#cfn-apprunner-service-serviceobservabilityconfiguration-observabilityconfigurationarn
            '''
            result = self._values.get("observability_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceObservabilityConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.SourceCodeVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class SourceCodeVersionProperty:
        def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
            '''Identifies a version of code that AWS App Runner refers to within a source code repository.

            :param type: The type of version identifier. For a git-based repository, branches represent versions.
            :param value: A source code version. For a git-based repository, a branch name maps to a specific version. App Runner uses the most recent commit to the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                source_code_version_property = apprunner.CfnService.SourceCodeVersionProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ac0bf11494d0e05342639d2117f5e475562de331e737d92fef42a02994d4a79)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of version identifier.

            For a git-based repository, branches represent versions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html#cfn-apprunner-service-sourcecodeversion-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''A source code version.

            For a git-based repository, a branch name maps to a specific version. App Runner uses the most recent commit to the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html#cfn-apprunner-service-sourcecodeversion-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceCodeVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnService.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_configuration": "authenticationConfiguration",
            "auto_deployments_enabled": "autoDeploymentsEnabled",
            "code_repository": "codeRepository",
            "image_repository": "imageRepository",
        },
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.AuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            code_repository: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.CodeRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_repository: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.ImageRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the source deployed to an AWS App Runner service.

            It can be a code or an image repository.

            :param authentication_configuration: Describes the resources that are needed to authenticate access to some source repositories.
            :param auto_deployments_enabled: If ``true`` , continuous integration from the source repository is enabled for the App Runner service. Each repository change (including any source code commit or new image version) starts a deployment. Default: App Runner sets to ``false`` for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in. App Runner sets to ``true`` in all other cases (which currently include a source code repository or a source image using a same-account ECR repository).
            :param code_repository: The description of a source code repository. You must provide either this member or ``ImageRepository`` (but not both).
            :param image_repository: The description of a source image repository. You must provide either this member or ``CodeRepository`` (but not both).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                source_configuration_property = apprunner.CfnService.SourceConfigurationProperty(
                    authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                        access_role_arn="accessRoleArn",
                        connection_arn="connectionArn"
                    ),
                    auto_deployments_enabled=False,
                    code_repository=apprunner.CfnService.CodeRepositoryProperty(
                        repository_url="repositoryUrl",
                        source_code_version=apprunner.CfnService.SourceCodeVersionProperty(
                            type="type",
                            value="value"
                        ),
                
                        # the properties below are optional
                        code_configuration=apprunner.CfnService.CodeConfigurationProperty(
                            configuration_source="configurationSource",
                
                            # the properties below are optional
                            code_configuration_values=apprunner.CfnService.CodeConfigurationValuesProperty(
                                runtime="runtime",
                
                                # the properties below are optional
                                build_command="buildCommand",
                                port="port",
                                runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                start_command="startCommand"
                            )
                        )
                    ),
                    image_repository=apprunner.CfnService.ImageRepositoryProperty(
                        image_identifier="imageIdentifier",
                        image_repository_type="imageRepositoryType",
                
                        # the properties below are optional
                        image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                            port="port",
                            runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a782b24a566f8d8cd887c13fe77ad47eb5cf8381a5dc9e03186ab8ede7fa7d2b)
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument auto_deployments_enabled", value=auto_deployments_enabled, expected_type=type_hints["auto_deployments_enabled"])
                check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
                check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if auto_deployments_enabled is not None:
                self._values["auto_deployments_enabled"] = auto_deployments_enabled
            if code_repository is not None:
                self._values["code_repository"] = code_repository
            if image_repository is not None:
                self._values["image_repository"] = image_repository

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.AuthenticationConfigurationProperty"]]:
            '''Describes the resources that are needed to authenticate access to some source repositories.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.AuthenticationConfigurationProperty"]], result)

        @builtins.property
        def auto_deployments_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If ``true`` , continuous integration from the source repository is enabled for the App Runner service.

            Each repository change (including any source code commit or new image version) starts a deployment.

            Default: App Runner sets to ``false`` for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in. App Runner sets to ``true`` in all other cases (which currently include a source code repository or a source image using a same-account ECR repository).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-autodeploymentsenabled
            '''
            result = self._values.get("auto_deployments_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def code_repository(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.CodeRepositoryProperty"]]:
            '''The description of a source code repository.

            You must provide either this member or ``ImageRepository`` (but not both).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-coderepository
            '''
            result = self._values.get("code_repository")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.CodeRepositoryProperty"]], result)

        @builtins.property
        def image_repository(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ImageRepositoryProperty"]]:
            '''The description of a source image repository.

            You must provide either this member or ``CodeRepository`` (but not both).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-imagerepository
            '''
            result = self._values.get("image_repository")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.ImageRepositoryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "source_configuration": "sourceConfiguration",
        "auto_scaling_configuration_arn": "autoScalingConfigurationArn",
        "encryption_configuration": "encryptionConfiguration",
        "health_check_configuration": "healthCheckConfiguration",
        "instance_configuration": "instanceConfiguration",
        "network_configuration": "networkConfiguration",
        "observability_configuration": "observabilityConfiguration",
        "service_name": "serviceName",
        "tags": "tags",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        source_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.InstanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        observability_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.ServiceObservabilityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnService``.

        :param source_configuration: The source to deploy to the App Runner service. It can be a code or an image repository.
        :param auto_scaling_configuration_arn: The Amazon Resource Name (ARN) of an App Runner automatic scaling configuration resource that you want to associate with your service. If not provided, App Runner associates the latest revision of a default auto scaling configuration. Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3`` Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability``
        :param encryption_configuration: An optional custom encryption key that App Runner uses to encrypt the copy of your source repository that it maintains and your service logs. By default, App Runner uses an AWS managed key .
        :param health_check_configuration: The settings for the health check that AWS App Runner performs to monitor the health of the App Runner service.
        :param instance_configuration: The runtime configuration of instances (scaling units) of your service.
        :param network_configuration: Configuration settings related to network traffic of the web application that the App Runner service runs.
        :param observability_configuration: The observability configuration of your service.
        :param service_name: A name for the App Runner service. It must be unique across all the running App Runner services in your AWS account in the AWS Region . If you don't specify a name, AWS CloudFormation generates a name for your service.
        :param tags: An optional list of metadata items that you can associate with the App Runner service resource. A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            cfn_service_props = apprunner.CfnServiceProps(
                source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                    authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                        access_role_arn="accessRoleArn",
                        connection_arn="connectionArn"
                    ),
                    auto_deployments_enabled=False,
                    code_repository=apprunner.CfnService.CodeRepositoryProperty(
                        repository_url="repositoryUrl",
                        source_code_version=apprunner.CfnService.SourceCodeVersionProperty(
                            type="type",
                            value="value"
                        ),
            
                        # the properties below are optional
                        code_configuration=apprunner.CfnService.CodeConfigurationProperty(
                            configuration_source="configurationSource",
            
                            # the properties below are optional
                            code_configuration_values=apprunner.CfnService.CodeConfigurationValuesProperty(
                                runtime="runtime",
            
                                # the properties below are optional
                                build_command="buildCommand",
                                port="port",
                                runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                start_command="startCommand"
                            )
                        )
                    ),
                    image_repository=apprunner.CfnService.ImageRepositoryProperty(
                        image_identifier="imageIdentifier",
                        image_repository_type="imageRepositoryType",
            
                        # the properties below are optional
                        image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                            port="port",
                            runtime_environment_secrets=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner.CfnService.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        )
                    )
                ),
            
                # the properties below are optional
                auto_scaling_configuration_arn="autoScalingConfigurationArn",
                encryption_configuration=apprunner.CfnService.EncryptionConfigurationProperty(
                    kms_key="kmsKey"
                ),
                health_check_configuration=apprunner.CfnService.HealthCheckConfigurationProperty(
                    healthy_threshold=123,
                    interval=123,
                    path="path",
                    protocol="protocol",
                    timeout=123,
                    unhealthy_threshold=123
                ),
                instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                    cpu="cpu",
                    instance_role_arn="instanceRoleArn",
                    memory="memory"
                ),
                network_configuration=apprunner.CfnService.NetworkConfigurationProperty(
                    egress_configuration=apprunner.CfnService.EgressConfigurationProperty(
                        egress_type="egressType",
            
                        # the properties below are optional
                        vpc_connector_arn="vpcConnectorArn"
                    ),
                    ingress_configuration=apprunner.CfnService.IngressConfigurationProperty(
                        is_publicly_accessible=False
                    )
                ),
                observability_configuration=apprunner.CfnService.ServiceObservabilityConfigurationProperty(
                    observability_enabled=False,
            
                    # the properties below are optional
                    observability_configuration_arn="observabilityConfigurationArn"
                ),
                service_name="serviceName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5587a0445eccbc76b496d223ee67346c5608142f9bf680a413951ed4f0bdc392)
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
            check_type(argname="argument auto_scaling_configuration_arn", value=auto_scaling_configuration_arn, expected_type=type_hints["auto_scaling_configuration_arn"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument health_check_configuration", value=health_check_configuration, expected_type=type_hints["health_check_configuration"])
            check_type(argname="argument instance_configuration", value=instance_configuration, expected_type=type_hints["instance_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument observability_configuration", value=observability_configuration, expected_type=type_hints["observability_configuration"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_configuration": source_configuration,
        }
        if auto_scaling_configuration_arn is not None:
            self._values["auto_scaling_configuration_arn"] = auto_scaling_configuration_arn
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if health_check_configuration is not None:
            self._values["health_check_configuration"] = health_check_configuration
        if instance_configuration is not None:
            self._values["instance_configuration"] = instance_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if observability_configuration is not None:
            self._values["observability_configuration"] = observability_configuration
        if service_name is not None:
            self._values["service_name"] = service_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.SourceConfigurationProperty]:
        '''The source to deploy to the App Runner service.

        It can be a code or an image repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        assert result is not None, "Required property 'source_configuration' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.SourceConfigurationProperty], result)

    @builtins.property
    def auto_scaling_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an App Runner automatic scaling configuration resource that you want to associate with your service.

        If not provided, App Runner associates the latest revision of a default auto scaling configuration.

        Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3``

        Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-autoscalingconfigurationarn
        '''
        result = self._values.get("auto_scaling_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.EncryptionConfigurationProperty]]:
        '''An optional custom encryption key that App Runner uses to encrypt the copy of your source repository that it maintains and your service logs.

        By default, App Runner uses an AWS managed key .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.EncryptionConfigurationProperty]], result)

    @builtins.property
    def health_check_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckConfigurationProperty]]:
        '''The settings for the health check that AWS App Runner performs to monitor the health of the App Runner service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-healthcheckconfiguration
        '''
        result = self._values.get("health_check_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckConfigurationProperty]], result)

    @builtins.property
    def instance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.InstanceConfigurationProperty]]:
        '''The runtime configuration of instances (scaling units) of your service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-instanceconfiguration
        '''
        result = self._values.get("instance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.InstanceConfigurationProperty]], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.NetworkConfigurationProperty]]:
        '''Configuration settings related to network traffic of the web application that the App Runner service runs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.NetworkConfigurationProperty]], result)

    @builtins.property
    def observability_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.ServiceObservabilityConfigurationProperty]]:
        '''The observability configuration of your service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-observabilityconfiguration
        '''
        result = self._values.get("observability_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.ServiceObservabilityConfigurationProperty]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''A name for the App Runner service.

        It must be unique across all the running App Runner services in your AWS account in the AWS Region .

        If you don't specify a name, AWS CloudFormation generates a name for your service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-servicename
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An optional list of metadata items that you can associate with the App Runner service resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVpcConnector(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.CfnVpcConnector",
):
    '''A CloudFormation ``AWS::AppRunner::VpcConnector``.

    Specify an AWS App Runner VPC connector by using the ``AWS::AppRunner::VpcConnector`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::VpcConnector`` resource is an AWS App Runner resource type that specifies an App Runner VPC connector.

    App Runner requires this resource when you want to associate your App Runner service to a custom Amazon Virtual Private Cloud ( Amazon VPC ).

    :cloudformationResource: AWS::AppRunner::VpcConnector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        cfn_vpc_connector = apprunner.CfnVpcConnector(self, "MyCfnVpcConnector",
            subnets=["subnets"],
        
            # the properties below are optional
            security_groups=["securityGroups"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_connector_name="vpcConnectorName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        subnets: typing.Sequence[builtins.str],
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppRunner::VpcConnector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subnets: A list of IDs of subnets that App Runner should use when it associates your service with a custom Amazon VPC. Specify IDs of subnets of a single Amazon VPC. App Runner determines the Amazon VPC from the subnets you specify. .. epigraph:: App Runner currently only provides support for IPv4.
        :param security_groups: A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. If not specified, App Runner uses the default security group of the Amazon VPC. The default security group allows all outbound traffic.
        :param tags: A list of metadata items that you can associate with your VPC connector resource. A tag is a key-value pair.
        :param vpc_connector_name: A name for the VPC connector. If you don't specify a name, AWS CloudFormation generates a name for your VPC connector.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af4fc5c566e6a501dd5cd69657568a3f3a0a6b94fe08b794d6c5bb0a1a10077)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVpcConnectorProps(
            subnets=subnets,
            security_groups=security_groups,
            tags=tags,
            vpc_connector_name=vpc_connector_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd7fb5a970a4e2f1e820d2a469d51c9cefa584ed6f24f725bed22dcf7833ed5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed85011ee76f66ed953c2517825b0cb0f59ee7662b58618f7dc549a582a2be73)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcConnectorArn")
    def attr_vpc_connector_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of this VPC connector.

        :cloudformationAttribute: VpcConnectorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcConnectorRevision")
    def attr_vpc_connector_revision(self) -> jsii.Number:
        '''The revision of this VPC connector.

        It's unique among all the active connectors ( ``"Status": "ACTIVE"`` ) that share the same ``Name`` .
        .. epigraph::

           At this time, App Runner supports only one revision per name.

        :cloudformationAttribute: VpcConnectorRevision
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrVpcConnectorRevision"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of metadata items that you can associate with your VPC connector resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        '''A list of IDs of subnets that App Runner should use when it associates your service with a custom Amazon VPC.

        Specify IDs of subnets of a single Amazon VPC. App Runner determines the Amazon VPC from the subnets you specify.
        .. epigraph::

           App Runner currently only provides support for IPv4.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-subnets
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68027f308ff8dee0abf536a357c5bbd76e2e371a89a2e6278edae0e5dbf9a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets.

        If not specified, App Runner uses the default security group of the Amazon VPC. The default security group allows all outbound traffic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-securitygroups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9b75ab651052258b60a6945826f924094090cd4548566056d17231ba412c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> typing.Optional[builtins.str]:
        '''A name for the VPC connector.

        If you don't specify a name, AWS CloudFormation generates a name for your VPC connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-vpcconnectorname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectorName"))

    @vpc_connector_name.setter
    def vpc_connector_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58ff4b34c408832c8db1c1b10111216d147e0f259e037bd4de24c55535847bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectorName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CfnVpcConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnets": "subnets",
        "security_groups": "securityGroups",
        "tags": "tags",
        "vpc_connector_name": "vpcConnectorName",
    },
)
class CfnVpcConnectorProps:
    def __init__(
        self,
        *,
        subnets: typing.Sequence[builtins.str],
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnVpcConnector``.

        :param subnets: A list of IDs of subnets that App Runner should use when it associates your service with a custom Amazon VPC. Specify IDs of subnets of a single Amazon VPC. App Runner determines the Amazon VPC from the subnets you specify. .. epigraph:: App Runner currently only provides support for IPv4.
        :param security_groups: A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. If not specified, App Runner uses the default security group of the Amazon VPC. The default security group allows all outbound traffic.
        :param tags: A list of metadata items that you can associate with your VPC connector resource. A tag is a key-value pair.
        :param vpc_connector_name: A name for the VPC connector. If you don't specify a name, AWS CloudFormation generates a name for your VPC connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            cfn_vpc_connector_props = apprunner.CfnVpcConnectorProps(
                subnets=["subnets"],
            
                # the properties below are optional
                security_groups=["securityGroups"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_connector_name="vpcConnectorName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b0e09c2556562d90be152ede0eac5e1fe1a08fdd557a19fadad8678f0037040)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_connector_name", value=vpc_connector_name, expected_type=type_hints["vpc_connector_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnets": subnets,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if vpc_connector_name is not None:
            self._values["vpc_connector_name"] = vpc_connector_name

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''A list of IDs of subnets that App Runner should use when it associates your service with a custom Amazon VPC.

        Specify IDs of subnets of a single Amazon VPC. App Runner determines the Amazon VPC from the subnets you specify.
        .. epigraph::

           App Runner currently only provides support for IPv4.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-subnets
        '''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets.

        If not specified, App Runner uses the default security group of the Amazon VPC. The default security group allows all outbound traffic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of metadata items that you can associate with your VPC connector resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_connector_name(self) -> typing.Optional[builtins.str]:
        '''A name for the VPC connector.

        If you don't specify a name, AWS CloudFormation generates a name for your VPC connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-vpcconnectorname
        '''
        result = self._values.get("vpc_connector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVpcIngressConnection(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.CfnVpcIngressConnection",
):
    '''A CloudFormation ``AWS::AppRunner::VpcIngressConnection``.

    Specify an AWS App Runner VPC Ingress Connection by using the ``AWS::AppRunner::VpcIngressConnection`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::VpcIngressConnection`` resource is an AWS App Runner resource type that specifies an App Runner VPC Ingress Connection.

    App Runner requires this resource when you want to associate your App Runner service to an Amazon VPC endpoint.

    :cloudformationResource: AWS::AppRunner::VpcIngressConnection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        cfn_vpc_ingress_connection = apprunner.CfnVpcIngressConnection(self, "MyCfnVpcIngressConnection",
            ingress_vpc_configuration=apprunner.CfnVpcIngressConnection.IngressVpcConfigurationProperty(
                vpc_endpoint_id="vpcEndpointId",
                vpc_id="vpcId"
            ),
            service_arn="serviceArn",
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_ingress_connection_name="vpcIngressConnectionName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        ingress_vpc_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVpcIngressConnection.IngressVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        service_arn: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppRunner::VpcIngressConnection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ingress_vpc_configuration: Specifications for the customer’s Amazon VPC and the related AWS PrivateLink VPC endpoint that are used to create the VPC Ingress Connection resource.
        :param service_arn: The Amazon Resource Name (ARN) for this App Runner service that is used to create the VPC Ingress Connection resource.
        :param tags: An optional list of metadata items that you can associate with the VPC Ingress Connection resource. A tag is a key-value pair.
        :param vpc_ingress_connection_name: The customer-provided VPC Ingress Connection name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f63e90293c6cefaf129f4acfb1145d410a3eb3fe1fbd2e4c358eb1d2e0645df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVpcIngressConnectionProps(
            ingress_vpc_configuration=ingress_vpc_configuration,
            service_arn=service_arn,
            tags=tags,
            vpc_ingress_connection_name=vpc_ingress_connection_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05554c20d4fa2d5b40d761098f432cc1f355099f2c84e867b4f6f9c8db69da0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b29616e39086d3ac7cc643cb9c76fd6218c7c89934f0ba73c6bd3fed75fe66d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''The domain name associated with the VPC Ingress Connection resource.

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the VPC Ingress Connection.

        The VPC Ingress Connection displays one of the following statuses: ``AVAILABLE`` , ``PENDING_CREATION`` , ``PENDING_DELETION`` , ``FAILED_CREATION`` , ``FAILED_DELETION`` , ``PENDNG_UPDATE`` , ``FAILED_UPDATE`` , and ``DELETED`` .

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcIngressConnectionArn")
    def attr_vpc_ingress_connection_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the VPC Ingress Connection.

        :cloudformationAttribute: VpcIngressConnectionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcIngressConnectionArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An optional list of metadata items that you can associate with the VPC Ingress Connection resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ingressVpcConfiguration")
    def ingress_vpc_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVpcIngressConnection.IngressVpcConfigurationProperty"]:
        '''Specifications for the customer’s Amazon VPC and the related AWS PrivateLink VPC endpoint that are used to create the VPC Ingress Connection resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVpcIngressConnection.IngressVpcConfigurationProperty"], jsii.get(self, "ingressVpcConfiguration"))

    @ingress_vpc_configuration.setter
    def ingress_vpc_configuration(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVpcIngressConnection.IngressVpcConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e785c9e976adf3c4a38e184689c97bff495a038c0dbbd9b3f47cabf6fdffdce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressVpcConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for this App Runner service that is used to create the VPC Ingress Connection resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-servicearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @service_arn.setter
    def service_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeacc4594ffc457a32ca93fe5a904096b4676a75dc2f74e31fbc72f437341722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceArn", value)

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionName")
    def vpc_ingress_connection_name(self) -> typing.Optional[builtins.str]:
        '''The customer-provided VPC Ingress Connection name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-vpcingressconnectionname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIngressConnectionName"))

    @vpc_ingress_connection_name.setter
    def vpc_ingress_connection_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a1936f0c39135ee05fd1b4cabba85899d303fac95bb5e95368d8f2b7b0d283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcIngressConnectionName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apprunner.CfnVpcIngressConnection.IngressVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_endpoint_id": "vpcEndpointId", "vpc_id": "vpcId"},
    )
    class IngressVpcConfigurationProperty:
        def __init__(
            self,
            *,
            vpc_endpoint_id: builtins.str,
            vpc_id: builtins.str,
        ) -> None:
            '''Specifications for the customer’s VPC and related PrivateLink VPC endpoint that are used to associate with the VPC Ingress Connection resource.

            :param vpc_endpoint_id: The ID of the VPC endpoint that your App Runner service connects to.
            :param vpc_id: The ID of the VPC that is used for the VPC endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-vpcingressconnection-ingressvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_apprunner as apprunner
                
                ingress_vpc_configuration_property = apprunner.CfnVpcIngressConnection.IngressVpcConfigurationProperty(
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05d78ecdc42154c50562a7547110bc399b2dab45cc47ce01eeaebb7d8817be15)
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "vpc_endpoint_id": vpc_endpoint_id,
                "vpc_id": vpc_id,
            }

        @builtins.property
        def vpc_endpoint_id(self) -> builtins.str:
            '''The ID of the VPC endpoint that your App Runner service connects to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-vpcingressconnection-ingressvpcconfiguration.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            assert result is not None, "Required property 'vpc_endpoint_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpc_id(self) -> builtins.str:
            '''The ID of the VPC that is used for the VPC endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-vpcingressconnection-ingressvpcconfiguration.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            assert result is not None, "Required property 'vpc_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CfnVpcIngressConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_vpc_configuration": "ingressVpcConfiguration",
        "service_arn": "serviceArn",
        "tags": "tags",
        "vpc_ingress_connection_name": "vpcIngressConnectionName",
    },
)
class CfnVpcIngressConnectionProps:
    def __init__(
        self,
        *,
        ingress_vpc_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVpcIngressConnection.IngressVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        service_arn: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnVpcIngressConnection``.

        :param ingress_vpc_configuration: Specifications for the customer’s Amazon VPC and the related AWS PrivateLink VPC endpoint that are used to create the VPC Ingress Connection resource.
        :param service_arn: The Amazon Resource Name (ARN) for this App Runner service that is used to create the VPC Ingress Connection resource.
        :param tags: An optional list of metadata items that you can associate with the VPC Ingress Connection resource. A tag is a key-value pair.
        :param vpc_ingress_connection_name: The customer-provided VPC Ingress Connection name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            cfn_vpc_ingress_connection_props = apprunner.CfnVpcIngressConnectionProps(
                ingress_vpc_configuration=apprunner.CfnVpcIngressConnection.IngressVpcConfigurationProperty(
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                ),
                service_arn="serviceArn",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_ingress_connection_name="vpcIngressConnectionName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34d59903e82305f14cc0ca76fac816335ecfb7282c446b0b1d56d566de87a11)
            check_type(argname="argument ingress_vpc_configuration", value=ingress_vpc_configuration, expected_type=type_hints["ingress_vpc_configuration"])
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_ingress_connection_name", value=vpc_ingress_connection_name, expected_type=type_hints["vpc_ingress_connection_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingress_vpc_configuration": ingress_vpc_configuration,
            "service_arn": service_arn,
        }
        if tags is not None:
            self._values["tags"] = tags
        if vpc_ingress_connection_name is not None:
            self._values["vpc_ingress_connection_name"] = vpc_ingress_connection_name

    @builtins.property
    def ingress_vpc_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVpcIngressConnection.IngressVpcConfigurationProperty]:
        '''Specifications for the customer’s Amazon VPC and the related AWS PrivateLink VPC endpoint that are used to create the VPC Ingress Connection resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration
        '''
        result = self._values.get("ingress_vpc_configuration")
        assert result is not None, "Required property 'ingress_vpc_configuration' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVpcIngressConnection.IngressVpcConfigurationProperty], result)

    @builtins.property
    def service_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for this App Runner service that is used to create the VPC Ingress Connection resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-servicearn
        '''
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An optional list of metadata items that you can associate with the VPC Ingress Connection resource.

        A tag is a key-value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_ingress_connection_name(self) -> typing.Optional[builtins.str]:
        '''The customer-provided VPC Ingress Connection name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-vpcingressconnectionname
        '''
        result = self._values.get("vpc_ingress_connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcIngressConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CodeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_source": "configurationSource",
        "configuration_values": "configurationValues",
    },
)
class CodeConfiguration:
    def __init__(
        self,
        *,
        configuration_source: "ConfigurationSourceType",
        configuration_values: typing.Optional[typing.Union["CodeConfigurationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Describes the configuration that AWS App Runner uses to build and run an App Runner service from a source code repository.

        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param configuration_values: (experimental) The basic configuration for building and running the App Runner service. Use it to quickly launch an App Runner service without providing a apprunner.yaml file in the source code repository (or ignoring the file if it exists). Default: - not specified. Use ``apprunner.yaml`` instead.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            # runtime: apprunner.Runtime
            
            code_configuration = apprunner.CodeConfiguration(
                configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
            
                # the properties below are optional
                configuration_values=apprunner.CodeConfigurationValues(
                    runtime=runtime,
            
                    # the properties below are optional
                    build_command="buildCommand",
                    environment={
                        "environment_key": "environment"
                    },
                    port="port",
                    start_command="startCommand"
                )
            )
        '''
        if isinstance(configuration_values, dict):
            configuration_values = CodeConfigurationValues(**configuration_values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57836d0228b4fa780e201e91d29d6e1a3dece7d04b04fd7b5ecef894b938395c)
            check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_source": configuration_source,
        }
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values

    @builtins.property
    def configuration_source(self) -> "ConfigurationSourceType":
        '''(experimental) The source of the App Runner configuration.

        :stability: experimental
        '''
        result = self._values.get("configuration_source")
        assert result is not None, "Required property 'configuration_source' is missing"
        return typing.cast("ConfigurationSourceType", result)

    @builtins.property
    def configuration_values(self) -> typing.Optional["CodeConfigurationValues"]:
        '''(experimental) The basic configuration for building and running the App Runner service.

        Use it to quickly launch an App Runner service without providing a apprunner.yaml file in the
        source code repository (or ignoring the file if it exists).

        :default: - not specified. Use ``apprunner.yaml`` instead.

        :stability: experimental
        '''
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional["CodeConfigurationValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CodeConfigurationValues",
    jsii_struct_bases=[],
    name_mapping={
        "runtime": "runtime",
        "build_command": "buildCommand",
        "environment": "environment",
        "port": "port",
        "start_command": "startCommand",
    },
)
class CodeConfigurationValues:
    def __init__(
        self,
        *,
        runtime: "Runtime",
        build_command: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        port: typing.Optional[builtins.str] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Describes the basic configuration needed for building and running an AWS App Runner service.

        This type doesn't support the full set of possible configuration options. Fur full configuration capabilities,
        use a ``apprunner.yaml`` file in the source code repository.

        :param runtime: (experimental) A runtime environment type for building and running an App Runner service. It represents a programming language runtime.
        :param build_command: (experimental) The command App Runner runs to build your application. Default: - no build command.
        :param environment: (experimental) The environment variables that are available to your running App Runner service. Default: - no environment variables.
        :param port: (experimental) The port that your application listens to in the container. Default: 8080
        :param start_command: (experimental) The command App Runner runs to start your application. Default: - no start command.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apprunner.Service(self, "Service",
                source=apprunner.Source.from_git_hub(
                    repository_url="https://github.com/aws-containers/hello-app-runner",
                    branch="main",
                    configuration_source=apprunner.ConfigurationSourceType.API,
                    code_configuration_values=apprunner.CodeConfigurationValues(
                        runtime=apprunner.Runtime.PYTHON_3,
                        port="8000",
                        start_command="python app.py",
                        build_command="yum install -y pycairo && pip install -r requirements.txt"
                    ),
                    connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407f1df4984352b2f07cf5e067190bf527f6a24893df1306ab1c3f5300664999)
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime": runtime,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if environment is not None:
            self._values["environment"] = environment
        if port is not None:
            self._values["port"] = port
        if start_command is not None:
            self._values["start_command"] = start_command

    @builtins.property
    def runtime(self) -> "Runtime":
        '''(experimental) A runtime environment type for building and running an App Runner service.

        It represents
        a programming language runtime.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast("Runtime", result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The command App Runner runs to build your application.

        :default: - no build command.

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables that are available to your running App Runner service.

        :default: - no environment variables.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''(experimental) The port that your application listens to in the container.

        :default: 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The command App Runner runs to start your application.

        :default: - no start command.

        :stability: experimental
        '''
        result = self._values.get("start_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfigurationValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.CodeRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "code_configuration": "codeConfiguration",
        "connection": "connection",
        "repository_url": "repositoryUrl",
        "source_code_version": "sourceCodeVersion",
    },
)
class CodeRepositoryProps:
    def __init__(
        self,
        *,
        code_configuration: typing.Union[CodeConfiguration, typing.Dict[builtins.str, typing.Any]],
        connection: "GitHubConnection",
        repository_url: builtins.str,
        source_code_version: typing.Union["SourceCodeVersion", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties of the CodeRepository.

        :param code_configuration: (experimental) Configuration for building and running the service from a source code repository.
        :param connection: (experimental) The App Runner connection for GitHub.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param source_code_version: (experimental) The version that should be used within the source code repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            # git_hub_connection: apprunner.GitHubConnection
            # runtime: apprunner.Runtime
            
            code_repository_props = apprunner.CodeRepositoryProps(
                code_configuration=apprunner.CodeConfiguration(
                    configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
            
                    # the properties below are optional
                    configuration_values=apprunner.CodeConfigurationValues(
                        runtime=runtime,
            
                        # the properties below are optional
                        build_command="buildCommand",
                        environment={
                            "environment_key": "environment"
                        },
                        port="port",
                        start_command="startCommand"
                    )
                ),
                connection=git_hub_connection,
                repository_url="repositoryUrl",
                source_code_version=apprunner.SourceCodeVersion(
                    type="type",
                    value="value"
                )
            )
        '''
        if isinstance(code_configuration, dict):
            code_configuration = CodeConfiguration(**code_configuration)
        if isinstance(source_code_version, dict):
            source_code_version = SourceCodeVersion(**source_code_version)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12c1e8c5fc61104d338feb6d248e1e9598531ad8ca59392eeba3f5eef4d527a)
            check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument source_code_version", value=source_code_version, expected_type=type_hints["source_code_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code_configuration": code_configuration,
            "connection": connection,
            "repository_url": repository_url,
            "source_code_version": source_code_version,
        }

    @builtins.property
    def code_configuration(self) -> CodeConfiguration:
        '''(experimental) Configuration for building and running the service from a source code repository.

        :stability: experimental
        '''
        result = self._values.get("code_configuration")
        assert result is not None, "Required property 'code_configuration' is missing"
        return typing.cast(CodeConfiguration, result)

    @builtins.property
    def connection(self) -> "GitHubConnection":
        '''(experimental) The App Runner connection for GitHub.

        :stability: experimental
        '''
        result = self._values.get("connection")
        assert result is not None, "Required property 'connection' is missing"
        return typing.cast("GitHubConnection", result)

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''(experimental) The location of the repository that contains the source code.

        :stability: experimental
        '''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_code_version(self) -> "SourceCodeVersion":
        '''(experimental) The version that should be used within the source code repository.

        :stability: experimental
        '''
        result = self._values.get("source_code_version")
        assert result is not None, "Required property 'source_code_version' is missing"
        return typing.cast("SourceCodeVersion", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner.ConfigurationSourceType")
class ConfigurationSourceType(enum.Enum):
    '''(experimental) The source of the App Runner configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_git_hub(
                repository_url="https://github.com/aws-containers/hello-app-runner",
                branch="main",
                configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
                connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
            )
        )
    '''

    REPOSITORY = "REPOSITORY"
    '''(experimental) App Runner reads configuration values from ``the apprunner.yaml`` file in the source code repository and ignores ``configurationValues``.

    :stability: experimental
    '''
    API = "API"
    '''(experimental) App Runner uses configuration values provided in ``configurationValues`` and ignores the ``apprunner.yaml`` file in the source code repository.

    :stability: experimental
    '''


class Cpu(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apprunner.Cpu"):
    '''(experimental) The number of CPU units reserved for each instance of your App Runner service.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        cpu = apprunner.Cpu.of("unit")
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, unit: builtins.str) -> "Cpu":
        '''(experimental) Custom CPU unit.

        :param unit: custom CPU unit.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-cpu
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff0bc0a22798ed3d048ece60b474bfa3da74b53f2da10771c6e916a6bd73cd3)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        return typing.cast("Cpu", jsii.sinvoke(cls, "of", [unit]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ONE_VCPU")
    def ONE_VCPU(cls) -> "Cpu":
        '''(experimental) 1 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "ONE_VCPU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TWO_VCPU")
    def TWO_VCPU(cls) -> "Cpu":
        '''(experimental) 2 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "TWO_VCPU"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        '''(experimental) The unit of CPU.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "unit"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.EcrProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "image_configuration": "imageConfiguration",
        "tag": "tag",
        "tag_or_digest": "tagOrDigest",
    },
)
class EcrProps:
    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_ecr_093ed842.IRepository,
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[builtins.str] = None,
        tag_or_digest: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of the image repository for ``Source.fromEcr()``.

        :param repository: (experimental) Represents the ECR repository.
        :param image_configuration: (experimental) The image configuration for the image from ECR. Default: - no image configuration will be passed. The default ``port`` will be 8080.
        :param tag: (deprecated) Image tag. Default: - 'latest'
        :param tag_or_digest: (experimental) Image tag or digest (digests must start with ``sha256:``). Default: - 'latest'

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecr as ecr
            
            
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr(
                    image_configuration=apprunner.ImageConfiguration(port=80),
                    repository=ecr.Repository.from_repository_name(self, "NginxRepository", "nginx"),
                    tag_or_digest="latest"
                )
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdf56f2aad4b0f7b62d5d564af277dd6d79d40c8dcb1bf064bd9a05a2fde567)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument tag_or_digest", value=tag_or_digest, expected_type=type_hints["tag_or_digest"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration
        if tag is not None:
            self._values["tag"] = tag
        if tag_or_digest is not None:
            self._values["tag_or_digest"] = tag_or_digest

    @builtins.property
    def repository(self) -> _aws_cdk_aws_ecr_093ed842.IRepository:
        '''(experimental) Represents the ECR repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_aws_cdk_aws_ecr_093ed842.IRepository, result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) The image configuration for the image from ECR.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Image tag.

        :default: - 'latest'

        :deprecated: use ``tagOrDigest``

        :stability: deprecated
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_or_digest(self) -> typing.Optional[builtins.str]:
        '''(experimental) Image tag or digest (digests must start with ``sha256:``).

        :default: - 'latest'

        :stability: experimental
        '''
        result = self._values.get("tag_or_digest")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.EcrPublicProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_identifier": "imageIdentifier",
        "image_configuration": "imageConfiguration",
    },
)
class EcrPublicProps:
    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the image repository for ``Source.fromEcrPublic()``.

        :param image_identifier: (experimental) The ECR Public image URI.
        :param image_configuration: (experimental) The image configuration for the image from ECR Public. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                )
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c8aa11e62b90ac0f9e6cae051e42127d85d7ebdc709af86030ccf649c808fa)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_identifier": image_identifier,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def image_identifier(self) -> builtins.str:
        '''(experimental) The ECR Public image URI.

        :stability: experimental
        '''
        result = self._values.get("image_identifier")
        assert result is not None, "Required property 'image_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) The image configuration for the image from ECR Public.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrPublicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubConnection(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.GitHubConnection",
):
    '''(experimental) Represents the App Runner connection that enables the App Runner service to connect to a source repository.

    It's required for GitHub code repositories.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_git_hub(
                repository_url="https://github.com/aws-containers/hello-app-runner",
                branch="main",
                configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
                connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
            )
        )
    '''

    def __init__(self, arn: builtins.str) -> None:
        '''
        :param arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c0490d37453c4aa729e1a1c928d1e5e9f41add2de364fca0b42daee82f70b9)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        jsii.create(self.__class__, self, [arn])

    @jsii.member(jsii_name="fromConnectionArn")
    @builtins.classmethod
    def from_connection_arn(cls, arn: builtins.str) -> "GitHubConnection":
        '''(experimental) Using existing App Runner connection by specifying the connection ARN.

        :param arn: connection ARN.

        :return: Connection

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8b34d9b102d08d9d47babe93c141f5f95662aeb24b931bc5836dfaace7b461)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("GitHubConnection", jsii.sinvoke(cls, "fromConnectionArn", [arn]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Connection for App Runner service to connect to the repository.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.GithubRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_source": "configurationSource",
        "connection": "connection",
        "repository_url": "repositoryUrl",
        "branch": "branch",
        "code_configuration_values": "codeConfigurationValues",
    },
)
class GithubRepositoryProps:
    def __init__(
        self,
        *,
        configuration_source: ConfigurationSourceType,
        connection: GitHubConnection,
        repository_url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the Github repository for ``Source.fromGitHub()``.

        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param connection: (experimental) ARN of the connection to Github. Only required for Github source.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param branch: (experimental) The branch name that represents a specific version for the repository. Default: main
        :param code_configuration_values: (experimental) The code configuration values. Will be ignored if configurationSource is ``REPOSITORY``. Default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apprunner.Service(self, "Service",
                source=apprunner.Source.from_git_hub(
                    repository_url="https://github.com/aws-containers/hello-app-runner",
                    branch="main",
                    configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
                    connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
                )
            )
        '''
        if isinstance(code_configuration_values, dict):
            code_configuration_values = CodeConfigurationValues(**code_configuration_values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5e593ecb78c01bf7585d04557ee5d861fad7580f192a3b1c8270dc91d8695d)
            check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument code_configuration_values", value=code_configuration_values, expected_type=type_hints["code_configuration_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_source": configuration_source,
            "connection": connection,
            "repository_url": repository_url,
        }
        if branch is not None:
            self._values["branch"] = branch
        if code_configuration_values is not None:
            self._values["code_configuration_values"] = code_configuration_values

    @builtins.property
    def configuration_source(self) -> ConfigurationSourceType:
        '''(experimental) The source of the App Runner configuration.

        :stability: experimental
        '''
        result = self._values.get("configuration_source")
        assert result is not None, "Required property 'configuration_source' is missing"
        return typing.cast(ConfigurationSourceType, result)

    @builtins.property
    def connection(self) -> GitHubConnection:
        '''(experimental) ARN of the connection to Github.

        Only required for Github source.

        :stability: experimental
        '''
        result = self._values.get("connection")
        assert result is not None, "Required property 'connection' is missing"
        return typing.cast(GitHubConnection, result)

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''(experimental) The location of the repository that contains the source code.

        :stability: experimental
        '''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch name that represents a specific version for the repository.

        :default: main

        :stability: experimental
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_configuration_values(self) -> typing.Optional[CodeConfigurationValues]:
        '''(experimental) The code configuration values.

        Will be ignored if configurationSource is ``REPOSITORY``.

        :default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        '''
        result = self._values.get("code_configuration_values")
        return typing.cast(typing.Optional[CodeConfigurationValues], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner.IService")
class IService(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Represents the App Runner Service.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the service.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The Name of the service.

        :stability: experimental
        '''
        ...


class _IServiceProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner Service.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner.IService"

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The Name of the service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IService).__jsii_proxy_class__ = lambda : _IServiceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner.IVpcConnector")
class IVpcConnector(
    _aws_cdk_core_f4b25747.IResource,
    _aws_cdk_aws_ec2_67de8e8d.IConnectable,
    typing_extensions.Protocol,
):
    '''(experimental) Represents the App Runner VPC Connector.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The Name of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorRevision")
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IVpcConnectorProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_67de8e8d.IConnectable), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner VPC Connector.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner.IVpcConnector"

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The Name of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorName"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorRevision")
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "vpcConnectorRevision"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcConnector).__jsii_proxy_class__ = lambda : _IVpcConnectorProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.ImageConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "port": "port",
        "start_command": "startCommand",
    },
)
class ImageConfiguration:
    def __init__(
        self,
        *,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Describes the configuration that AWS App Runner uses to run an App Runner service using an image pulled from a source image repository.

        :param environment: (experimental) Environment variables that are available to your running App Runner service. Default: - no environment variables
        :param port: (experimental) The port that your application listens to in the container. Default: 8080
        :param start_command: (experimental) An optional command that App Runner runs to start the application in the source image. If specified, this command overrides the Docker image’s default start command. Default: - no start command

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecr_assets as assets
            
            
            image_asset = assets.DockerImageAsset(self, "ImageAssets",
                directory=path.join(__dirname, "./docker.assets")
            )
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_asset(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    asset=image_asset
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721b7a009a5ad7ddfaae7fb90ecc804b0ee6ed0d9721b8f6f42b54be5e941b18)
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if environment is not None:
            self._values["environment"] = environment
        if port is not None:
            self._values["port"] = port
        if start_command is not None:
            self._values["start_command"] = start_command

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables that are available to your running App Runner service.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port that your application listens to in the container.

        :default: 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional command that App Runner runs to start the application in the source image.

        If specified, this command overrides the Docker image’s default start command.

        :default: - no start command

        :stability: experimental
        '''
        result = self._values.get("start_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.ImageRepository",
    jsii_struct_bases=[],
    name_mapping={
        "image_identifier": "imageIdentifier",
        "image_repository_type": "imageRepositoryType",
        "image_configuration": "imageConfiguration",
    },
)
class ImageRepository:
    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_repository_type: "ImageRepositoryType",
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Describes a source image repository.

        :param image_identifier: (experimental) The identifier of the image. For ``ECR_PUBLIC`` imageRepositoryType, the identifier domain should always be ``public.ecr.aws``. For ``ECR``, the pattern should be ``([0-9]{12}.dkr.ecr.[a-z\\-]+-[0-9]{1}.amazonaws.com\\/.*)``.
        :param image_repository_type: (experimental) The type of the image repository. This reflects the repository provider and whether the repository is private or public.
        :param image_configuration: (experimental) Configuration for running the identified image. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            image_repository = apprunner.ImageRepository(
                image_identifier="imageIdentifier",
                image_repository_type=apprunner.ImageRepositoryType.ECR_PUBLIC,
            
                # the properties below are optional
                image_configuration=apprunner.ImageConfiguration(
                    environment={
                        "environment_key": "environment"
                    },
                    port=123,
                    start_command="startCommand"
                )
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09f0656dad9bc4b6712239ffc61583b19c82ea68337bd0b3e9ec0c409b8a7d2)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
            check_type(argname="argument image_repository_type", value=image_repository_type, expected_type=type_hints["image_repository_type"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_identifier": image_identifier,
            "image_repository_type": image_repository_type,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def image_identifier(self) -> builtins.str:
        '''(experimental) The identifier of the image.

        For ``ECR_PUBLIC`` imageRepositoryType, the identifier domain should
        always be ``public.ecr.aws``. For ``ECR``, the pattern should be
        ``([0-9]{12}.dkr.ecr.[a-z\\-]+-[0-9]{1}.amazonaws.com\\/.*)``.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html for more details.
        :stability: experimental
        '''
        result = self._values.get("image_identifier")
        assert result is not None, "Required property 'image_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_repository_type(self) -> "ImageRepositoryType":
        '''(experimental) The type of the image repository.

        This reflects the repository provider and whether
        the repository is private or public.

        :stability: experimental
        '''
        result = self._values.get("image_repository_type")
        assert result is not None, "Required property 'image_repository_type' is missing"
        return typing.cast("ImageRepositoryType", result)

    @builtins.property
    def image_configuration(self) -> typing.Optional[ImageConfiguration]:
        '''(experimental) Configuration for running the identified image.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional[ImageConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner.ImageRepositoryType")
class ImageRepositoryType(enum.Enum):
    '''(experimental) The image repository types.

    :stability: experimental
    '''

    ECR_PUBLIC = "ECR_PUBLIC"
    '''(experimental) Amazon ECR Public.

    :stability: experimental
    '''
    ECR = "ECR"
    '''(experimental) Amazon ECR.

    :stability: experimental
    '''


class Memory(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apprunner.Memory"):
    '''(experimental) The amount of memory reserved for each instance of your App Runner service.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        memory = apprunner.Memory.FOUR_GB
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, unit: builtins.str) -> "Memory":
        '''(experimental) Custom Memory unit.

        :param unit: custom Memory unit.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-memory
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120fc6ba6c8e00ca0f7260251656ab8eb399d5b60aed4e11cec9468cba7bb576)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        return typing.cast("Memory", jsii.sinvoke(cls, "of", [unit]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FOUR_GB")
    def FOUR_GB(cls) -> "Memory":
        '''(experimental) 4 GB(for 1 or 2 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "FOUR_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="THREE_GB")
    def THREE_GB(cls) -> "Memory":
        '''(experimental) 3 GB(for 1 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "THREE_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TWO_GB")
    def TWO_GB(cls) -> "Memory":
        '''(experimental) 2 GB(for 1 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "TWO_GB"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        '''(experimental) The unit of memory.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "unit"))


class Runtime(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apprunner.Runtime"):
    '''(experimental) The code runtimes.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_git_hub(
                repository_url="https://github.com/aws-containers/hello-app-runner",
                branch="main",
                configuration_source=apprunner.ConfigurationSourceType.API,
                code_configuration_values=apprunner.CodeConfigurationValues(
                    runtime=apprunner.Runtime.PYTHON_3,
                    port="8000",
                    start_command="python app.py",
                    build_command="yum install -y pycairo && pip install -r requirements.txt"
                ),
                connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
            )
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "Runtime":
        '''(experimental) Other runtimes.

        :param name: runtime name.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtime for all available runtimes.
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65318ceb91b5a31e50cd6992c6b6cb111240b82405c588a13c8cd8aa77abe4f6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("Runtime", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_12")
    def NODEJS_12(cls) -> "Runtime":
        '''(experimental) NodeJS 12.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "NODEJS_12"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_3")
    def PYTHON_3(cls) -> "Runtime":
        '''(experimental) Python 3.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "PYTHON_3"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The runtime name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Service(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.Service",
):
    '''(experimental) The App Runner Service.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ecr_assets as assets
        
        
        image_asset = assets.DockerImageAsset(self, "ImageAssets",
            directory=path.join(__dirname, "./docker.assets")
        )
        apprunner.Service(self, "Service",
            source=apprunner.Source.from_asset(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                asset=image_asset
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source: "Source",
        access_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        cpu: typing.Optional[Cpu] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        memory: typing.Optional[Memory] = None,
        service_name: typing.Optional[builtins.str] = None,
        vpc_connector: typing.Optional[IVpcConnector] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source: (experimental) The source of the repository for the service.
        :param access_role: (experimental) The IAM role that grants the App Runner service access to a source repository. It's required for ECR image repositories (but not for ECR Public repositories). The role must be assumable by the 'build.apprunner.amazonaws.com' service principal. Default: - generate a new access role.
        :param cpu: (experimental) The number of CPU units reserved for each instance of your App Runner service. Default: Cpu.ONE_VCPU
        :param instance_role: (experimental) The IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs. The role must be assumable by the 'tasks.apprunner.amazonaws.com' service principal. Default: - no instance role attached.
        :param memory: (experimental) The amount of memory reserved for each instance of your App Runner service. Default: Memory.TWO_GB
        :param service_name: (experimental) Name of the service. Default: - auto-generated if undefined.
        :param vpc_connector: (experimental) Settings for an App Runner VPC connector to associate with the service. Default: - no VPC connector, uses the DEFAULT egress type instead

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e95445a764306e1a04646bc54ded94177464dbeb8118a2b8cf813705bd46fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceProps(
            source=source,
            access_role=access_role,
            cpu=cpu,
            instance_role=instance_role,
            memory=memory,
            service_name=service_name,
            vpc_connector=vpc_connector,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServiceAttributes")
    @builtins.classmethod
    def from_service_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service_arn: builtins.str,
        service_name: builtins.str,
        service_status: builtins.str,
        service_url: builtins.str,
    ) -> IService:
        '''(experimental) Import from service attributes.

        :param scope: -
        :param id: -
        :param service_arn: (experimental) The ARN of the service.
        :param service_name: (experimental) The name of the service.
        :param service_status: (experimental) The status of the service.
        :param service_url: (experimental) The URL of the service.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a57150d74580b7163ab3fbeba11af31823fdbe7eb15b1070aa25d90db87e596)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ServiceAttributes(
            service_arn=service_arn,
            service_name=service_name,
            service_status=service_status,
            service_url=service_url,
        )

        return typing.cast(IService, jsii.sinvoke(cls, "fromServiceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromServiceName")
    @builtins.classmethod
    def from_service_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        service_name: builtins.str,
    ) -> IService:
        '''(experimental) Import from service name.

        :param scope: -
        :param id: -
        :param service_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88299d485a438eab2c9b8808181769ca3ebb024bec53c575590d8c276432e92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        return typing.cast(IService, jsii.sinvoke(cls, "fromServiceName", [scope, id, service_name]))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''(experimental) The ID of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The name of the service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="serviceStatus")
    def service_status(self) -> builtins.str:
        '''(experimental) The status of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceStatus"))

    @builtins.property
    @jsii.member(jsii_name="serviceUrl")
    def service_url(self) -> builtins.str:
        '''(experimental) The URL of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceUrl"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.ServiceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "service_arn": "serviceArn",
        "service_name": "serviceName",
        "service_status": "serviceStatus",
        "service_url": "serviceUrl",
    },
)
class ServiceAttributes:
    def __init__(
        self,
        *,
        service_arn: builtins.str,
        service_name: builtins.str,
        service_status: builtins.str,
        service_url: builtins.str,
    ) -> None:
        '''(experimental) Attributes for the App Runner Service.

        :param service_arn: (experimental) The ARN of the service.
        :param service_name: (experimental) The name of the service.
        :param service_status: (experimental) The status of the service.
        :param service_url: (experimental) The URL of the service.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            service_attributes = apprunner.ServiceAttributes(
                service_arn="serviceArn",
                service_name="serviceName",
                service_status="serviceStatus",
                service_url="serviceUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b652a2bcf979492b381c83f82aeb9df2f0e5cd065fe37837e06f2796c8e982f9)
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument service_status", value=service_status, expected_type=type_hints["service_status"])
            check_type(argname="argument service_url", value=service_url, expected_type=type_hints["service_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_arn": service_arn,
            "service_name": service_name,
            "service_status": service_status,
            "service_url": service_url,
        }

    @builtins.property
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the service.

        :stability: experimental
        '''
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''(experimental) The name of the service.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_status(self) -> builtins.str:
        '''(experimental) The status of the service.

        :stability: experimental
        '''
        result = self._values.get("service_status")
        assert result is not None, "Required property 'service_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_url(self) -> builtins.str:
        '''(experimental) The URL of the service.

        :stability: experimental
        '''
        result = self._values.get("service_url")
        assert result is not None, "Required property 'service_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.ServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "access_role": "accessRole",
        "cpu": "cpu",
        "instance_role": "instanceRole",
        "memory": "memory",
        "service_name": "serviceName",
        "vpc_connector": "vpcConnector",
    },
)
class ServiceProps:
    def __init__(
        self,
        *,
        source: "Source",
        access_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        cpu: typing.Optional[Cpu] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        memory: typing.Optional[Memory] = None,
        service_name: typing.Optional[builtins.str] = None,
        vpc_connector: typing.Optional[IVpcConnector] = None,
    ) -> None:
        '''(experimental) Properties of the AppRunner Service.

        :param source: (experimental) The source of the repository for the service.
        :param access_role: (experimental) The IAM role that grants the App Runner service access to a source repository. It's required for ECR image repositories (but not for ECR Public repositories). The role must be assumable by the 'build.apprunner.amazonaws.com' service principal. Default: - generate a new access role.
        :param cpu: (experimental) The number of CPU units reserved for each instance of your App Runner service. Default: Cpu.ONE_VCPU
        :param instance_role: (experimental) The IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs. The role must be assumable by the 'tasks.apprunner.amazonaws.com' service principal. Default: - no instance role attached.
        :param memory: (experimental) The amount of memory reserved for each instance of your App Runner service. Default: Memory.TWO_GB
        :param service_name: (experimental) Name of the service. Default: - auto-generated if undefined.
        :param vpc_connector: (experimental) Settings for an App Runner VPC connector to associate with the service. Default: - no VPC connector, uses the DEFAULT egress type instead

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecr_assets as assets
            
            
            image_asset = assets.DockerImageAsset(self, "ImageAssets",
                directory=path.join(__dirname, "./docker.assets")
            )
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_asset(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    asset=image_asset
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c18eaf004fbd3198c752c13217baff49a7b9e1a7f01070a45ed8996a64392be)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument vpc_connector", value=vpc_connector, expected_type=type_hints["vpc_connector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if access_role is not None:
            self._values["access_role"] = access_role
        if cpu is not None:
            self._values["cpu"] = cpu
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if memory is not None:
            self._values["memory"] = memory
        if service_name is not None:
            self._values["service_name"] = service_name
        if vpc_connector is not None:
            self._values["vpc_connector"] = vpc_connector

    @builtins.property
    def source(self) -> "Source":
        '''(experimental) The source of the repository for the service.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("Source", result)

    @builtins.property
    def access_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role that grants the App Runner service access to a source repository.

        It's required for ECR image repositories (but not for ECR Public repositories).

        The role must be assumable by the 'build.apprunner.amazonaws.com' service principal.

        :default: - generate a new access role.

        :see: https://docs.aws.amazon.com/apprunner/latest/dg/security_iam_service-with-iam.html#security_iam_service-with-iam-roles-service.access
        :stability: experimental
        '''
        result = self._values.get("access_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def cpu(self) -> typing.Optional[Cpu]:
        '''(experimental) The number of CPU units reserved for each instance of your App Runner service.

        :default: Cpu.ONE_VCPU

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[Cpu], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role that provides permissions to your App Runner service.

        These are permissions that your code needs when it calls any AWS APIs.

        The role must be assumable by the 'tasks.apprunner.amazonaws.com' service principal.

        :default: - no instance role attached.

        :see: https://docs.aws.amazon.com/apprunner/latest/dg/security_iam_service-with-iam.html#security_iam_service-with-iam-roles-service.instance
        :stability: experimental
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def memory(self) -> typing.Optional[Memory]:
        '''(experimental) The amount of memory reserved for each instance of your App Runner service.

        :default: Memory.TWO_GB

        :stability: experimental
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[Memory], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the service.

        :default: - auto-generated if undefined.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector(self) -> typing.Optional[IVpcConnector]:
        '''(experimental) Settings for an App Runner VPC connector to associate with the service.

        :default: - no VPC connector, uses the DEFAULT egress type instead

        :stability: experimental
        '''
        result = self._values.get("vpc_connector")
        return typing.cast(typing.Optional[IVpcConnector], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Source(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-apprunner.Source",
):
    '''(experimental) Represents the App Runner service source.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ecr_assets as assets
        
        
        image_asset = assets.DockerImageAsset(self, "ImageAssets",
            directory=path.join(__dirname, "./docker.assets")
        )
        apprunner.Service(self, "Service",
            source=apprunner.Source.from_asset(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                asset=image_asset
            )
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        *,
        asset: _aws_cdk_aws_ecr_assets_ef09b699.DockerImageAsset,
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "AssetSource":
        '''(experimental) Source from local assets.

        :param asset: (experimental) Represents the docker image asset.
        :param image_configuration: (experimental) The image configuration for the image built from the asset. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = AssetProps(asset=asset, image_configuration=image_configuration)

        return typing.cast("AssetSource", jsii.sinvoke(cls, "fromAsset", [props]))

    @jsii.member(jsii_name="fromEcr")
    @builtins.classmethod
    def from_ecr(
        cls,
        *,
        repository: _aws_cdk_aws_ecr_093ed842.IRepository,
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[builtins.str] = None,
        tag_or_digest: typing.Optional[builtins.str] = None,
    ) -> "EcrSource":
        '''(experimental) Source from the ECR repository.

        :param repository: (experimental) Represents the ECR repository.
        :param image_configuration: (experimental) The image configuration for the image from ECR. Default: - no image configuration will be passed. The default ``port`` will be 8080.
        :param tag: (deprecated) Image tag. Default: - 'latest'
        :param tag_or_digest: (experimental) Image tag or digest (digests must start with ``sha256:``). Default: - 'latest'

        :stability: experimental
        '''
        props = EcrProps(
            repository=repository,
            image_configuration=image_configuration,
            tag=tag,
            tag_or_digest=tag_or_digest,
        )

        return typing.cast("EcrSource", jsii.sinvoke(cls, "fromEcr", [props]))

    @jsii.member(jsii_name="fromEcrPublic")
    @builtins.classmethod
    def from_ecr_public(
        cls,
        *,
        image_identifier: builtins.str,
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "EcrPublicSource":
        '''(experimental) Source from the ECR Public repository.

        :param image_identifier: (experimental) The ECR Public image URI.
        :param image_configuration: (experimental) The image configuration for the image from ECR Public. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = EcrPublicProps(
            image_identifier=image_identifier, image_configuration=image_configuration
        )

        return typing.cast("EcrPublicSource", jsii.sinvoke(cls, "fromEcrPublic", [props]))

    @jsii.member(jsii_name="fromGitHub")
    @builtins.classmethod
    def from_git_hub(
        cls,
        *,
        configuration_source: ConfigurationSourceType,
        connection: GitHubConnection,
        repository_url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "GithubSource":
        '''(experimental) Source from the GitHub repository.

        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param connection: (experimental) ARN of the connection to Github. Only required for Github source.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param branch: (experimental) The branch name that represents a specific version for the repository. Default: main
        :param code_configuration_values: (experimental) The code configuration values. Will be ignored if configurationSource is ``REPOSITORY``. Default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        '''
        props = GithubRepositoryProps(
            configuration_source=configuration_source,
            connection=connection,
            repository_url=repository_url,
            branch=branch,
            code_configuration_values=code_configuration_values,
        )

        return typing.cast("GithubSource", jsii.sinvoke(cls, "fromGitHub", [props]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -

        :stability: experimental
        '''
        ...


class _SourceProxy(Source):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa4b0689345a798dc7c3f4d9b3205bd2a397c419f2adb941d2744d3d985a8a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Source).__jsii_proxy_class__ = lambda : _SourceProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.SourceCodeVersion",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SourceCodeVersion:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''(experimental) Identifies a version of code that AWS App Runner refers to within a source code repository.

        :param type: (experimental) The type of version identifier.
        :param value: (experimental) A source code version.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            
            source_code_version = apprunner.SourceCodeVersion(
                type="type",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222cb135de9127679ef3b50c5376a17e44146dd8755d4996eae326d082ec4485)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The type of version identifier.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) A source code version.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCodeVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "code_repository": "codeRepository",
        "ecr_repository": "ecrRepository",
        "image_repository": "imageRepository",
    },
)
class SourceConfig:
    def __init__(
        self,
        *,
        code_repository: typing.Optional[typing.Union[CodeRepositoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ecr_repository: typing.Optional[_aws_cdk_aws_ecr_093ed842.IRepository] = None,
        image_repository: typing.Optional[typing.Union[ImageRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Result of binding ``Source`` into a ``Service``.

        :param code_repository: (experimental) The code repository configuration (mutually exclusive with ``imageRepository``). Default: - no code repository.
        :param ecr_repository: (experimental) The ECR repository (required to grant the pull privileges for the iam role). Default: - no ECR repository.
        :param image_repository: (experimental) The image repository configuration (mutually exclusive with ``codeRepository``). Default: - no image repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            import aws_cdk.aws_ecr as ecr
            
            # git_hub_connection: apprunner.GitHubConnection
            # repository: ecr.Repository
            # runtime: apprunner.Runtime
            
            source_config = apprunner.SourceConfig(
                code_repository=apprunner.CodeRepositoryProps(
                    code_configuration=apprunner.CodeConfiguration(
                        configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
            
                        # the properties below are optional
                        configuration_values=apprunner.CodeConfigurationValues(
                            runtime=runtime,
            
                            # the properties below are optional
                            build_command="buildCommand",
                            environment={
                                "environment_key": "environment"
                            },
                            port="port",
                            start_command="startCommand"
                        )
                    ),
                    connection=git_hub_connection,
                    repository_url="repositoryUrl",
                    source_code_version=apprunner.SourceCodeVersion(
                        type="type",
                        value="value"
                    )
                ),
                ecr_repository=repository,
                image_repository=apprunner.ImageRepository(
                    image_identifier="imageIdentifier",
                    image_repository_type=apprunner.ImageRepositoryType.ECR_PUBLIC,
            
                    # the properties below are optional
                    image_configuration=apprunner.ImageConfiguration(
                        environment={
                            "environment_key": "environment"
                        },
                        port=123,
                        start_command="startCommand"
                    )
                )
            )
        '''
        if isinstance(code_repository, dict):
            code_repository = CodeRepositoryProps(**code_repository)
        if isinstance(image_repository, dict):
            image_repository = ImageRepository(**image_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5befb3618a58047faaf4f9108262e6b73ec835b48648503093fac8c162662bf)
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument ecr_repository", value=ecr_repository, expected_type=type_hints["ecr_repository"])
            check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if ecr_repository is not None:
            self._values["ecr_repository"] = ecr_repository
        if image_repository is not None:
            self._values["image_repository"] = image_repository

    @builtins.property
    def code_repository(self) -> typing.Optional[CodeRepositoryProps]:
        '''(experimental) The code repository configuration (mutually exclusive  with ``imageRepository``).

        :default: - no code repository.

        :stability: experimental
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional[CodeRepositoryProps], result)

    @builtins.property
    def ecr_repository(self) -> typing.Optional[_aws_cdk_aws_ecr_093ed842.IRepository]:
        '''(experimental) The ECR repository (required to grant the pull privileges for the iam role).

        :default: - no ECR repository.

        :stability: experimental
        '''
        result = self._values.get("ecr_repository")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_093ed842.IRepository], result)

    @builtins.property
    def image_repository(self) -> typing.Optional[ImageRepository]:
        '''(experimental) The image repository configuration (mutually exclusive  with ``codeRepository``).

        :default: - no image repository.

        :stability: experimental
        '''
        result = self._values.get("image_repository")
        return typing.cast(typing.Optional[ImageRepository], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVpcConnector)
class VpcConnector(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.VpcConnector",
):
    '''(experimental) The App Runner VPC Connector.

    :stability: experimental
    :resource: AWS::AppRunner::VpcConnector
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ec2 as ec2
        
        
        vpc = ec2.Vpc(self, "Vpc",
            cidr="10.0.0.0/16"
        )
        
        vpc_connector = apprunner.VpcConnector(self, "VpcConnector",
            vpc=vpc,
            vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC),
            vpc_connector_name="MyVpcConnector"
        )
        
        apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            vpc_connector=vpc_connector
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The VPC for the VPC Connector.
        :param security_groups: (experimental) A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. Default: - a new security group will be created in the specified VPC
        :param vpc_connector_name: (experimental) The name for the VpcConnector. Default: - a name generated by CloudFormation
        :param vpc_subnets: (experimental) Where to place the VPC Connector within the VPC. Default: - Private subnets.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f412d6d07ed819a4e970002e2c57abb6553e2cab5a947dfcf305603201473d64)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcConnectorProps(
            vpc=vpc,
            security_groups=security_groups,
            vpc_connector_name=vpc_connector_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromVpcConnectorAttributes")
    @builtins.classmethod
    def from_vpc_connector_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup],
        vpc_connector_arn: builtins.str,
        vpc_connector_name: builtins.str,
        vpc_connector_revision: jsii.Number,
    ) -> IVpcConnector:
        '''(experimental) Import from VPC connector attributes.

        :param scope: -
        :param id: -
        :param security_groups: (experimental) The security groups associated with the VPC connector.
        :param vpc_connector_arn: (experimental) The ARN of the VPC connector.
        :param vpc_connector_name: (experimental) The name of the VPC connector.
        :param vpc_connector_revision: (experimental) The revision of the VPC connector.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344f5a63efff7cf58ff92f08d6a7add57957549aad87ed4df0ef5437a98c1539)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = VpcConnectorAttributes(
            security_groups=security_groups,
            vpc_connector_arn=vpc_connector_arn,
            vpc_connector_name=vpc_connector_name,
            vpc_connector_revision=vpc_connector_revision,
        )

        return typing.cast(IVpcConnector, jsii.sinvoke(cls, "fromVpcConnectorAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_67de8e8d.Connections:
        '''(experimental) Allows specifying security group connections for the VPC connector.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The name of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorName"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorRevision")
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "vpcConnectorRevision"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.VpcConnectorAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "security_groups": "securityGroups",
        "vpc_connector_arn": "vpcConnectorArn",
        "vpc_connector_name": "vpcConnectorName",
        "vpc_connector_revision": "vpcConnectorRevision",
    },
)
class VpcConnectorAttributes:
    def __init__(
        self,
        *,
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup],
        vpc_connector_arn: builtins.str,
        vpc_connector_name: builtins.str,
        vpc_connector_revision: jsii.Number,
    ) -> None:
        '''(experimental) Attributes for the App Runner VPC Connector.

        :param security_groups: (experimental) The security groups associated with the VPC connector.
        :param vpc_connector_arn: (experimental) The ARN of the VPC connector.
        :param vpc_connector_name: (experimental) The name of the VPC connector.
        :param vpc_connector_revision: (experimental) The revision of the VPC connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner as apprunner
            import aws_cdk.aws_ec2 as ec2
            
            # security_group: ec2.SecurityGroup
            
            vpc_connector_attributes = apprunner.VpcConnectorAttributes(
                security_groups=[security_group],
                vpc_connector_arn="vpcConnectorArn",
                vpc_connector_name="vpcConnectorName",
                vpc_connector_revision=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f456c165dbc003d2d3c102de41d4efe2a1501f48bce1e1fc4851df09afc312)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc_connector_arn", value=vpc_connector_arn, expected_type=type_hints["vpc_connector_arn"])
            check_type(argname="argument vpc_connector_name", value=vpc_connector_name, expected_type=type_hints["vpc_connector_name"])
            check_type(argname="argument vpc_connector_revision", value=vpc_connector_revision, expected_type=type_hints["vpc_connector_revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_groups": security_groups,
            "vpc_connector_arn": vpc_connector_arn,
            "vpc_connector_name": vpc_connector_name,
            "vpc_connector_revision": vpc_connector_revision,
        }

    @builtins.property
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]:
        '''(experimental) The security groups associated with the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup], result)

    @builtins.property
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_arn")
        assert result is not None, "Required property 'vpc_connector_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The name of the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_name")
        assert result is not None, "Required property 'vpc_connector_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_revision")
        assert result is not None, "Required property 'vpc_connector_revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcConnectorAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner.VpcConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "security_groups": "securityGroups",
        "vpc_connector_name": "vpcConnectorName",
        "vpc_subnets": "vpcSubnets",
    },
)
class VpcConnectorProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the AppRunner VPC Connector.

        :param vpc: (experimental) The VPC for the VPC Connector.
        :param security_groups: (experimental) A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. Default: - a new security group will be created in the specified VPC
        :param vpc_connector_name: (experimental) The name for the VpcConnector. Default: - a name generated by CloudFormation
        :param vpc_subnets: (experimental) Where to place the VPC Connector within the VPC. Default: - Private subnets.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ec2 as ec2
            
            
            vpc = ec2.Vpc(self, "Vpc",
                cidr="10.0.0.0/16"
            )
            
            vpc_connector = apprunner.VpcConnector(self, "VpcConnector",
                vpc=vpc,
                vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC),
                vpc_connector_name="MyVpcConnector"
            )
            
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                ),
                vpc_connector=vpc_connector
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f035ede47254d6598c8e5c48757ead717f9a6da7eabac805a055d72cd77e152e)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc_connector_name", value=vpc_connector_name, expected_type=type_hints["vpc_connector_name"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc_connector_name is not None:
            self._values["vpc_connector_name"] = vpc_connector_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''(experimental) The VPC for the VPC Connector.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''(experimental) A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets.

        :default: - a new security group will be created in the specified VPC

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def vpc_connector_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the VpcConnector.

        :default: - a name generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''(experimental) Where to place the VPC Connector within the VPC.

        :default: - Private subnets.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssetSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.AssetSource",
):
    '''(experimental) Represents the source from local assets.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        import aws_cdk.aws_ecr_assets as ecr_assets
        
        # docker_image_asset: ecr_assets.DockerImageAsset
        
        asset_source = apprunner.AssetSource(
            asset=docker_image_asset,
        
            # the properties below are optional
            image_configuration=apprunner.ImageConfiguration(
                environment={
                    "environment_key": "environment"
                },
                port=123,
                start_command="startCommand"
            )
        )
    '''

    def __init__(
        self,
        *,
        asset: _aws_cdk_aws_ecr_assets_ef09b699.DockerImageAsset,
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param asset: (experimental) Represents the docker image asset.
        :param image_configuration: (experimental) The image configuration for the image built from the asset. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = AssetProps(asset=asset, image_configuration=image_configuration)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> SourceConfig:
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1c5e51e8f403029a75619b34597c17aaeda524af6467b9331d60acfe26e980)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(SourceConfig, jsii.invoke(self, "bind", [_scope]))


class EcrPublicSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.EcrPublicSource",
):
    '''(experimental) Represents the service source from ECR Public.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        ecr_public_source = apprunner.EcrPublicSource(
            image_identifier="imageIdentifier",
        
            # the properties below are optional
            image_configuration=apprunner.ImageConfiguration(
                environment={
                    "environment_key": "environment"
                },
                port=123,
                start_command="startCommand"
            )
        )
    '''

    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_identifier: (experimental) The ECR Public image URI.
        :param image_configuration: (experimental) The image configuration for the image from ECR Public. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = EcrPublicProps(
            image_identifier=image_identifier, image_configuration=image_configuration
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> SourceConfig:
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2cdb3323e3c5aa2139534bee556c6bce834ea663dc730079953d2938c206e8)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(SourceConfig, jsii.invoke(self, "bind", [_scope]))


class EcrSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.EcrSource",
):
    '''(experimental) Represents the service source from ECR.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        import aws_cdk.aws_ecr as ecr
        
        # repository: ecr.Repository
        
        ecr_source = apprunner.EcrSource(
            repository=repository,
        
            # the properties below are optional
            image_configuration=apprunner.ImageConfiguration(
                environment={
                    "environment_key": "environment"
                },
                port=123,
                start_command="startCommand"
            ),
            tag="tag",
            tag_or_digest="tagOrDigest"
        )
    '''

    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_ecr_093ed842.IRepository,
        image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[builtins.str] = None,
        tag_or_digest: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: (experimental) Represents the ECR repository.
        :param image_configuration: (experimental) The image configuration for the image from ECR. Default: - no image configuration will be passed. The default ``port`` will be 8080.
        :param tag: (deprecated) Image tag. Default: - 'latest'
        :param tag_or_digest: (experimental) Image tag or digest (digests must start with ``sha256:``). Default: - 'latest'

        :stability: experimental
        '''
        props = EcrProps(
            repository=repository,
            image_configuration=image_configuration,
            tag=tag,
            tag_or_digest=tag_or_digest,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> SourceConfig:
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bc83de2d76fcd0c4534fcfde9f309291903564c997dddb0c729b24e30f4b11)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(SourceConfig, jsii.invoke(self, "bind", [_scope]))


class GithubSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner.GithubSource",
):
    '''(experimental) Represents the service source from a Github repository.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner as apprunner
        
        # git_hub_connection: apprunner.GitHubConnection
        # runtime: apprunner.Runtime
        
        github_source = apprunner.GithubSource(
            configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
            connection=git_hub_connection,
            repository_url="repositoryUrl",
        
            # the properties below are optional
            branch="branch",
            code_configuration_values=apprunner.CodeConfigurationValues(
                runtime=runtime,
        
                # the properties below are optional
                build_command="buildCommand",
                environment={
                    "environment_key": "environment"
                },
                port="port",
                start_command="startCommand"
            )
        )
    '''

    def __init__(
        self,
        *,
        configuration_source: ConfigurationSourceType,
        connection: GitHubConnection,
        repository_url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param connection: (experimental) ARN of the connection to Github. Only required for Github source.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param branch: (experimental) The branch name that represents a specific version for the repository. Default: main
        :param code_configuration_values: (experimental) The code configuration values. Will be ignored if configurationSource is ``REPOSITORY``. Default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        '''
        props = GithubRepositoryProps(
            configuration_source=configuration_source,
            connection=connection,
            repository_url=repository_url,
            branch=branch,
            code_configuration_values=code_configuration_values,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> SourceConfig:
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457048dbbd1e4cbd9c429ac0008ec013a04c23f2a1cd4337e5c6c8a5d9434c27)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(SourceConfig, jsii.invoke(self, "bind", [_scope]))


__all__ = [
    "AssetProps",
    "AssetSource",
    "CfnObservabilityConfiguration",
    "CfnObservabilityConfigurationProps",
    "CfnService",
    "CfnServiceProps",
    "CfnVpcConnector",
    "CfnVpcConnectorProps",
    "CfnVpcIngressConnection",
    "CfnVpcIngressConnectionProps",
    "CodeConfiguration",
    "CodeConfigurationValues",
    "CodeRepositoryProps",
    "ConfigurationSourceType",
    "Cpu",
    "EcrProps",
    "EcrPublicProps",
    "EcrPublicSource",
    "EcrSource",
    "GitHubConnection",
    "GithubRepositoryProps",
    "GithubSource",
    "IService",
    "IVpcConnector",
    "ImageConfiguration",
    "ImageRepository",
    "ImageRepositoryType",
    "Memory",
    "Runtime",
    "Service",
    "ServiceAttributes",
    "ServiceProps",
    "Source",
    "SourceCodeVersion",
    "SourceConfig",
    "VpcConnector",
    "VpcConnectorAttributes",
    "VpcConnectorProps",
]

publication.publish()

def _typecheckingstub__ddacc297fe93219c04d7e04ff6fab0a907f6ada139e1217128d76f52964517f1(
    *,
    asset: _aws_cdk_aws_ecr_assets_ef09b699.DockerImageAsset,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91bbfa645cb60714a2cc00c1efcaedbd7a9160b03212ae6dbc26fc692f8c01a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    observability_configuration_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trace_configuration: typing.Optional[typing.Union[typing.Union[CfnObservabilityConfiguration.TraceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c1b0e41f3ac21fe5acd7a0c3529ed9631cb9028d12af611e5c878764796952(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbefce63b0c29dcc23e08d3f09d8bd70b44ac5ce6971e970872f0453f60bbed5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb8958ed80ab2db90c622cdd8bb62345d408fbd455aadc3b1f8b1762773e89d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2743192fe969ee1bf389f3351e4cb3d6f0ba7a1becf18c1a645c4a9a4583e6(
    value: typing.Optional[typing.Union[CfnObservabilityConfiguration.TraceConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e688456285b4d056d4db1f6b320235066e4121351f5717a2a508558147bc701b(
    *,
    vendor: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5006d9251a2bd9f94a7b3eb3f2d290856b70e1dff5c62653e6a2c90b98a09487(
    *,
    observability_configuration_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trace_configuration: typing.Optional[typing.Union[typing.Union[CfnObservabilityConfiguration.TraceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca87c4c8a5746257f1f031ee66a2bfe0b8a2c7e9289c0d5b8b26d10936612be7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    source_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.InstanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    observability_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.ServiceObservabilityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547576c08be1741ea36e95890335fe2c9153bb9a6b515f44d3603dec97cbe3d9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec349bad48c3086954344e9594ae3c14895d98d124287d1c058bed1bfd7715f4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04aa5ea8f4ead0e9147eafd0b549206a0a7878e1c67cee1a341049e9a20ce3ac(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.SourceConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75325d1dc127a3f83d249b5ddf1ecffe588776ee0037565d82575fa3d10b9778(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f7f823c7e715271f924a6936d0e308dfeaf4add0b7b1d350bc64b9ae37ba04(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.EncryptionConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edfd79cd0489e028f07de9f7918aff6728ddb101dee5acad6ba14b7e8110fdb(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fb20e04cc7053efa05959e4b0607b8ffc7fcd567e18cc4281e9137bcdc72eb(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.InstanceConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b0aa228b668fcd763ec6f282077b94f2d668acf7492cdb4652739248368318(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.NetworkConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7b43fb251c201d3b5ea62af96de0e94c815b748bdc0d578941b0c6cd5b95f8(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.ServiceObservabilityConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5b37f8b1d7adda1b3a9146dbcdb07ab7eb9a60dff4003bca4e06fb8f70cb31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ff72239e8344d1f54c0457d22ea928fd2f4ff4064c7a83bd550e28292ca236(
    *,
    access_role_arn: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b629437d011e0488747601a2b36a41c997667dbb59b98ee4def4ab91e4888b(
    *,
    configuration_source: builtins.str,
    code_configuration_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.CodeConfigurationValuesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a924d82fad65a222b6da4bb5f29304a69e7ef2d58eaafd3ba9f599de11b7bf(
    *,
    runtime: builtins.str,
    build_command: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374635dcd80b1052600a921ff860a5dc9cddf1f067dc7836330305298af2cc37(
    *,
    repository_url: builtins.str,
    source_code_version: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.SourceCodeVersionProperty, typing.Dict[builtins.str, typing.Any]]],
    code_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.CodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec5bd61d7e0974df6a89f0c9598d7a19e5d388769a755b8fbdd12c58f9e8eac(
    *,
    egress_type: builtins.str,
    vpc_connector_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb220ec07370c696e17f8ad5c47a6aacc7ae57533a5b228597bf07621cb0b586(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c435d9b0fc5c3eb53afa0a4165fffd0bc5bd44df2d43b45ade3f645ef9f4a7(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d01630e9ae8e9d018b18c37dbba5e9248590be83574b21ec31433b551883b51(
    *,
    port: typing.Optional[builtins.str] = None,
    runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71a33070cb9b5bbb6e9f771bdb2aabdf33e0faf15548869abe6dfd34e40037e(
    *,
    image_identifier: builtins.str,
    image_repository_type: builtins.str,
    image_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.ImageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe4078e36c2e7a9a71cafd7db3dd196480c0ef67164ff3ccc4072be96903722(
    *,
    is_publicly_accessible: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3ebf4b817bcda9604c899ffa1984838dca0c5a3d1a28d6946fec06f6c299c7(
    *,
    cpu: typing.Optional[builtins.str] = None,
    instance_role_arn: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5456e7d808e1c66f2f521c909f7c779ae5a6e91dc8a7a7ecfcefd1c568833785(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59588ba677d357eacb99cc8b8467288391194ff592d620f28fcd13766d5330bd(
    *,
    egress_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.EgressConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingress_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.IngressConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dcd73b0f9c754b973a3d13c12b968f44cb18d6ef6062b4fcdbcf7087b6fcabb(
    *,
    observability_enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    observability_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac0bf11494d0e05342639d2117f5e475562de331e737d92fef42a02994d4a79(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a782b24a566f8d8cd887c13fe77ad47eb5cf8381a5dc9e03186ab8ede7fa7d2b(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    code_repository: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.CodeRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_repository: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.ImageRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5587a0445eccbc76b496d223ee67346c5608142f9bf680a413951ed4f0bdc392(
    *,
    source_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.InstanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    observability_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.ServiceObservabilityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af4fc5c566e6a501dd5cd69657568a3f3a0a6b94fe08b794d6c5bb0a1a10077(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    subnets: typing.Sequence[builtins.str],
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd7fb5a970a4e2f1e820d2a469d51c9cefa584ed6f24f725bed22dcf7833ed5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed85011ee76f66ed953c2517825b0cb0f59ee7662b58618f7dc549a582a2be73(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68027f308ff8dee0abf536a357c5bbd76e2e371a89a2e6278edae0e5dbf9a3a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9b75ab651052258b60a6945826f924094090cd4548566056d17231ba412c91(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58ff4b34c408832c8db1c1b10111216d147e0f259e037bd4de24c55535847bd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0e09c2556562d90be152ede0eac5e1fe1a08fdd557a19fadad8678f0037040(
    *,
    subnets: typing.Sequence[builtins.str],
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f63e90293c6cefaf129f4acfb1145d410a3eb3fe1fbd2e4c358eb1d2e0645df(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    ingress_vpc_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVpcIngressConnection.IngressVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    service_arn: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05554c20d4fa2d5b40d761098f432cc1f355099f2c84e867b4f6f9c8db69da0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b29616e39086d3ac7cc643cb9c76fd6218c7c89934f0ba73c6bd3fed75fe66d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e785c9e976adf3c4a38e184689c97bff495a038c0dbbd9b3f47cabf6fdffdce1(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVpcIngressConnection.IngressVpcConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeacc4594ffc457a32ca93fe5a904096b4676a75dc2f74e31fbc72f437341722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a1936f0c39135ee05fd1b4cabba85899d303fac95bb5e95368d8f2b7b0d283(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d78ecdc42154c50562a7547110bc399b2dab45cc47ce01eeaebb7d8817be15(
    *,
    vpc_endpoint_id: builtins.str,
    vpc_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34d59903e82305f14cc0ca76fac816335ecfb7282c446b0b1d56d566de87a11(
    *,
    ingress_vpc_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVpcIngressConnection.IngressVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    service_arn: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57836d0228b4fa780e201e91d29d6e1a3dece7d04b04fd7b5ecef894b938395c(
    *,
    configuration_source: ConfigurationSourceType,
    configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407f1df4984352b2f07cf5e067190bf527f6a24893df1306ab1c3f5300664999(
    *,
    runtime: Runtime,
    build_command: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    port: typing.Optional[builtins.str] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12c1e8c5fc61104d338feb6d248e1e9598531ad8ca59392eeba3f5eef4d527a(
    *,
    code_configuration: typing.Union[CodeConfiguration, typing.Dict[builtins.str, typing.Any]],
    connection: GitHubConnection,
    repository_url: builtins.str,
    source_code_version: typing.Union[SourceCodeVersion, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff0bc0a22798ed3d048ece60b474bfa3da74b53f2da10771c6e916a6bd73cd3(
    unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdf56f2aad4b0f7b62d5d564af277dd6d79d40c8dcb1bf064bd9a05a2fde567(
    *,
    repository: _aws_cdk_aws_ecr_093ed842.IRepository,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tag: typing.Optional[builtins.str] = None,
    tag_or_digest: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c8aa11e62b90ac0f9e6cae051e42127d85d7ebdc709af86030ccf649c808fa(
    *,
    image_identifier: builtins.str,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c0490d37453c4aa729e1a1c928d1e5e9f41add2de364fca0b42daee82f70b9(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8b34d9b102d08d9d47babe93c141f5f95662aeb24b931bc5836dfaace7b461(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5e593ecb78c01bf7585d04557ee5d861fad7580f192a3b1c8270dc91d8695d(
    *,
    configuration_source: ConfigurationSourceType,
    connection: GitHubConnection,
    repository_url: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    code_configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721b7a009a5ad7ddfaae7fb90ecc804b0ee6ed0d9721b8f6f42b54be5e941b18(
    *,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    port: typing.Optional[jsii.Number] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09f0656dad9bc4b6712239ffc61583b19c82ea68337bd0b3e9ec0c409b8a7d2(
    *,
    image_identifier: builtins.str,
    image_repository_type: ImageRepositoryType,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120fc6ba6c8e00ca0f7260251656ab8eb399d5b60aed4e11cec9468cba7bb576(
    unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65318ceb91b5a31e50cd6992c6b6cb111240b82405c588a13c8cd8aa77abe4f6(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e95445a764306e1a04646bc54ded94177464dbeb8118a2b8cf813705bd46fb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source: Source,
    access_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    cpu: typing.Optional[Cpu] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    memory: typing.Optional[Memory] = None,
    service_name: typing.Optional[builtins.str] = None,
    vpc_connector: typing.Optional[IVpcConnector] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a57150d74580b7163ab3fbeba11af31823fdbe7eb15b1070aa25d90db87e596(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service_arn: builtins.str,
    service_name: builtins.str,
    service_status: builtins.str,
    service_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88299d485a438eab2c9b8808181769ca3ebb024bec53c575590d8c276432e92(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b652a2bcf979492b381c83f82aeb9df2f0e5cd065fe37837e06f2796c8e982f9(
    *,
    service_arn: builtins.str,
    service_name: builtins.str,
    service_status: builtins.str,
    service_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c18eaf004fbd3198c752c13217baff49a7b9e1a7f01070a45ed8996a64392be(
    *,
    source: Source,
    access_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    cpu: typing.Optional[Cpu] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    memory: typing.Optional[Memory] = None,
    service_name: typing.Optional[builtins.str] = None,
    vpc_connector: typing.Optional[IVpcConnector] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa4b0689345a798dc7c3f4d9b3205bd2a397c419f2adb941d2744d3d985a8a7(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222cb135de9127679ef3b50c5376a17e44146dd8755d4996eae326d082ec4485(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5befb3618a58047faaf4f9108262e6b73ec835b48648503093fac8c162662bf(
    *,
    code_repository: typing.Optional[typing.Union[CodeRepositoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ecr_repository: typing.Optional[_aws_cdk_aws_ecr_093ed842.IRepository] = None,
    image_repository: typing.Optional[typing.Union[ImageRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f412d6d07ed819a4e970002e2c57abb6553e2cab5a947dfcf305603201473d64(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344f5a63efff7cf58ff92f08d6a7add57957549aad87ed4df0ef5437a98c1539(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup],
    vpc_connector_arn: builtins.str,
    vpc_connector_name: builtins.str,
    vpc_connector_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f456c165dbc003d2d3c102de41d4efe2a1501f48bce1e1fc4851df09afc312(
    *,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup],
    vpc_connector_arn: builtins.str,
    vpc_connector_name: builtins.str,
    vpc_connector_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f035ede47254d6598c8e5c48757ead717f9a6da7eabac805a055d72cd77e152e(
    *,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1c5e51e8f403029a75619b34597c17aaeda524af6467b9331d60acfe26e980(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2cdb3323e3c5aa2139534bee556c6bce834ea663dc730079953d2938c206e8(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bc83de2d76fcd0c4534fcfde9f309291903564c997dddb0c729b24e30f4b11(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457048dbbd1e4cbd9c429ac0008ec013a04c23f2a1cd4337e5c6c8a5d9434c27(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass
