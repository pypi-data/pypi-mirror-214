'''
# AWS::EMRContainers Construct Library

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
import aws_cdk.aws_emrcontainers as emrcontainers
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for EMRContainers construct libraries](https://constructs.dev/search?q=emrcontainers)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::EMRContainers resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMRContainers.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::EMRContainers](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMRContainers.html).

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
class CfnVirtualCluster(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-emrcontainers.CfnVirtualCluster",
):
    '''A CloudFormation ``AWS::EMRContainers::VirtualCluster``.

    The ``AWS::EMRContainers::VirtualCluster`` resource specifies a virtual cluster. A virtual cluster is a managed entity on Amazon EMR on EKS. You can create, describe, list, and delete virtual clusters. They do not consume any additional resources in your system. A single virtual cluster maps to a single Kubernetes namespace. Given this relationship, you can model virtual clusters the same way you model Kubernetes namespaces to meet your requirements.

    :cloudformationResource: AWS::EMRContainers::VirtualCluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_emrcontainers as emrcontainers
        
        cfn_virtual_cluster = emrcontainers.CfnVirtualCluster(self, "MyCfnVirtualCluster",
            container_provider=emrcontainers.CfnVirtualCluster.ContainerProviderProperty(
                id="id",
                info=emrcontainers.CfnVirtualCluster.ContainerInfoProperty(
                    eks_info=emrcontainers.CfnVirtualCluster.EksInfoProperty(
                        namespace="namespace"
                    )
                ),
                type="type"
            ),
            name="name",
        
            # the properties below are optional
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
        container_provider: typing.Union[typing.Union["CfnVirtualCluster.ContainerProviderProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::EMRContainers::VirtualCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param container_provider: The container provider of the virtual cluster.
        :param name: The name of the virtual cluster.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539fc8802e61c095150d53c18a6d2b0e46ba5318236aecd63f4db53bf430120b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVirtualClusterProps(
            container_provider=container_provider, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7129029071575bc70d8907fe62fd43af06768284aea8b12a1b631cc416a4cea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b06da1344434582adb28132efb5e7345c6f5fb77653f9d80c93a9f87946f99f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the project, such as ``arn:aws:emr-containers:us-east-1:123456789012:/virtualclusters/ab4rp1abcs8xz47n3x0example`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the virtual cluster, such as ``ab4rp1abcs8xz47n3x0example`` .

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

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html#cfn-emrcontainers-virtualcluster-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="containerProvider")
    def container_provider(
        self,
    ) -> typing.Union["CfnVirtualCluster.ContainerProviderProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The container provider of the virtual cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html#cfn-emrcontainers-virtualcluster-containerprovider
        '''
        return typing.cast(typing.Union["CfnVirtualCluster.ContainerProviderProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "containerProvider"))

    @container_provider.setter
    def container_provider(
        self,
        value: typing.Union["CfnVirtualCluster.ContainerProviderProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdd3812e5c95fc14207253f1dc889c5bf600594a544994af071cf655e3f2626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerProvider", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the virtual cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html#cfn-emrcontainers-virtualcluster-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b50f192e5a364c39706d2da59c9a6ac585768ffbae782540a8d478e05e5c2c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrcontainers.CfnVirtualCluster.ContainerInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"eks_info": "eksInfo"},
    )
    class ContainerInfoProperty:
        def __init__(
            self,
            *,
            eks_info: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVirtualCluster.EksInfoProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The information about the container used for a job run or a managed endpoint.

            :param eks_info: The information about the Amazon EKS cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-containerinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrcontainers as emrcontainers
                
                container_info_property = emrcontainers.CfnVirtualCluster.ContainerInfoProperty(
                    eks_info=emrcontainers.CfnVirtualCluster.EksInfoProperty(
                        namespace="namespace"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a29184930fc20b88930967b2d71976335b27cfb87f149f33efcdf443bb53d298)
                check_type(argname="argument eks_info", value=eks_info, expected_type=type_hints["eks_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "eks_info": eks_info,
            }

        @builtins.property
        def eks_info(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVirtualCluster.EksInfoProperty"]:
            '''The information about the Amazon EKS cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-containerinfo.html#cfn-emrcontainers-virtualcluster-containerinfo-eksinfo
            '''
            result = self._values.get("eks_info")
            assert result is not None, "Required property 'eks_info' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVirtualCluster.EksInfoProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrcontainers.CfnVirtualCluster.ContainerProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "info": "info", "type": "type"},
    )
    class ContainerProviderProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            info: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVirtualCluster.ContainerInfoProperty", typing.Dict[builtins.str, typing.Any]]],
            type: builtins.str,
        ) -> None:
            '''The information about the container provider.

            :param id: The ID of the container cluster. *Minimum* : 1 *Maximum* : 100 *Pattern* : ``^[0-9A-Za-z][A-Za-z0-9\\-_]*``
            :param info: The information about the container cluster.
            :param type: The type of the container provider. Amazon EKS is the only supported type as of now.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-containerprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrcontainers as emrcontainers
                
                container_provider_property = emrcontainers.CfnVirtualCluster.ContainerProviderProperty(
                    id="id",
                    info=emrcontainers.CfnVirtualCluster.ContainerInfoProperty(
                        eks_info=emrcontainers.CfnVirtualCluster.EksInfoProperty(
                            namespace="namespace"
                        )
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__baae8cb233f903176a79e1df7ebb5dfc5d124dbb7b666bb41737a0d7d603e680)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument info", value=info, expected_type=type_hints["info"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "info": info,
                "type": type,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''The ID of the container cluster.

            *Minimum* : 1

            *Maximum* : 100

            *Pattern* : ``^[0-9A-Za-z][A-Za-z0-9\\-_]*``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-containerprovider.html#cfn-emrcontainers-virtualcluster-containerprovider-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def info(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVirtualCluster.ContainerInfoProperty"]:
            '''The information about the container cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-containerprovider.html#cfn-emrcontainers-virtualcluster-containerprovider-info
            '''
            result = self._values.get("info")
            assert result is not None, "Required property 'info' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVirtualCluster.ContainerInfoProperty"], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of the container provider.

            Amazon EKS is the only supported type as of now.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-containerprovider.html#cfn-emrcontainers-virtualcluster-containerprovider-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrcontainers.CfnVirtualCluster.EksInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"namespace": "namespace"},
    )
    class EksInfoProperty:
        def __init__(self, *, namespace: builtins.str) -> None:
            '''The information about the Amazon EKS cluster.

            :param namespace: The namespaces of the EKS cluster. *Minimum* : 1 *Maximum* : 63 *Pattern* : ``[a-z0-9]([-a-z0-9]*[a-z0-9])?``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-eksinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrcontainers as emrcontainers
                
                eks_info_property = emrcontainers.CfnVirtualCluster.EksInfoProperty(
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__143c340c46942c6c77f9b5263ca915f9e875932f2adf00a2c19b9d7d00e302f0)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "namespace": namespace,
            }

        @builtins.property
        def namespace(self) -> builtins.str:
            '''The namespaces of the EKS cluster.

            *Minimum* : 1

            *Maximum* : 63

            *Pattern* : ``[a-z0-9]([-a-z0-9]*[a-z0-9])?``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrcontainers-virtualcluster-eksinfo.html#cfn-emrcontainers-virtualcluster-eksinfo-namespace
            '''
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-emrcontainers.CfnVirtualClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_provider": "containerProvider",
        "name": "name",
        "tags": "tags",
    },
)
class CfnVirtualClusterProps:
    def __init__(
        self,
        *,
        container_provider: typing.Union[typing.Union[CfnVirtualCluster.ContainerProviderProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVirtualCluster``.

        :param container_provider: The container provider of the virtual cluster.
        :param name: The name of the virtual cluster.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_emrcontainers as emrcontainers
            
            cfn_virtual_cluster_props = emrcontainers.CfnVirtualClusterProps(
                container_provider=emrcontainers.CfnVirtualCluster.ContainerProviderProperty(
                    id="id",
                    info=emrcontainers.CfnVirtualCluster.ContainerInfoProperty(
                        eks_info=emrcontainers.CfnVirtualCluster.EksInfoProperty(
                            namespace="namespace"
                        )
                    ),
                    type="type"
                ),
                name="name",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347d72a3c7115957bb99f81e764f22eb4d1423f91ca765d8d8bed5daa04ebf1e)
            check_type(argname="argument container_provider", value=container_provider, expected_type=type_hints["container_provider"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_provider": container_provider,
            "name": name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def container_provider(
        self,
    ) -> typing.Union[CfnVirtualCluster.ContainerProviderProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The container provider of the virtual cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html#cfn-emrcontainers-virtualcluster-containerprovider
        '''
        result = self._values.get("container_provider")
        assert result is not None, "Required property 'container_provider' is missing"
        return typing.cast(typing.Union[CfnVirtualCluster.ContainerProviderProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the virtual cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html#cfn-emrcontainers-virtualcluster-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrcontainers-virtualcluster.html#cfn-emrcontainers-virtualcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnVirtualCluster",
    "CfnVirtualClusterProps",
]

publication.publish()

def _typecheckingstub__539fc8802e61c095150d53c18a6d2b0e46ba5318236aecd63f4db53bf430120b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    container_provider: typing.Union[typing.Union[CfnVirtualCluster.ContainerProviderProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7129029071575bc70d8907fe62fd43af06768284aea8b12a1b631cc416a4cea(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b06da1344434582adb28132efb5e7345c6f5fb77653f9d80c93a9f87946f99f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdd3812e5c95fc14207253f1dc889c5bf600594a544994af071cf655e3f2626(
    value: typing.Union[CfnVirtualCluster.ContainerProviderProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b50f192e5a364c39706d2da59c9a6ac585768ffbae782540a8d478e05e5c2c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29184930fc20b88930967b2d71976335b27cfb87f149f33efcdf443bb53d298(
    *,
    eks_info: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVirtualCluster.EksInfoProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baae8cb233f903176a79e1df7ebb5dfc5d124dbb7b666bb41737a0d7d603e680(
    *,
    id: builtins.str,
    info: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVirtualCluster.ContainerInfoProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143c340c46942c6c77f9b5263ca915f9e875932f2adf00a2c19b9d7d00e302f0(
    *,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347d72a3c7115957bb99f81e764f22eb4d1423f91ca765d8d8bed5daa04ebf1e(
    *,
    container_provider: typing.Union[typing.Union[CfnVirtualCluster.ContainerProviderProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
