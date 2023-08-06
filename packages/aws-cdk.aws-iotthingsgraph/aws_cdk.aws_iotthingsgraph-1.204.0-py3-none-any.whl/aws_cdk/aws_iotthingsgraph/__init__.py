'''
# AWS IoT Things Graph Construct Library

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
import aws_cdk.aws_iotthingsgraph as iotthingsgraph
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IoTThingsGraph construct libraries](https://constructs.dev/search?q=iotthingsgraph)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IoTThingsGraph resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTThingsGraph.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IoTThingsGraph](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTThingsGraph.html).

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
class CfnFlowTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotthingsgraph.CfnFlowTemplate",
):
    '''A CloudFormation ``AWS::IoTThingsGraph::FlowTemplate``.

    :cloudformationResource: AWS::IoTThingsGraph::FlowTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iotthingsgraph as iotthingsgraph
        
        cfn_flow_template = iotthingsgraph.CfnFlowTemplate(self, "MyCfnFlowTemplate",
            definition=iotthingsgraph.CfnFlowTemplate.DefinitionDocumentProperty(
                language="language",
                text="text"
            ),
        
            # the properties below are optional
            compatible_namespace_version=123
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        definition: typing.Union[typing.Union["CfnFlowTemplate.DefinitionDocumentProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        compatible_namespace_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::IoTThingsGraph::FlowTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: ``AWS::IoTThingsGraph::FlowTemplate.Definition``.
        :param compatible_namespace_version: ``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a55c29432fc6d309ea33f36b6b6e3fe83a1f3e1433cc4c03ee26d731b785cb5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowTemplateProps(
            definition=definition,
            compatible_namespace_version=compatible_namespace_version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b013964bc6199e425a48c2f7fa088b62453f881bbaeb6be93ccf05adc1c79ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0e48caa8fa880a25352a23bd5d08609df4a93951baef23670d3b1c65fd6d89)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(
        self,
    ) -> typing.Union["CfnFlowTemplate.DefinitionDocumentProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''``AWS::IoTThingsGraph::FlowTemplate.Definition``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-definition
        '''
        return typing.cast(typing.Union["CfnFlowTemplate.DefinitionDocumentProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "definition"))

    @definition.setter
    def definition(
        self,
        value: typing.Union["CfnFlowTemplate.DefinitionDocumentProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e472f3a73381485805b3b87baaaeee8043ec4eefec93488acd804c451a9958b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="compatibleNamespaceVersion")
    def compatible_namespace_version(self) -> typing.Optional[jsii.Number]:
        '''``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-compatiblenamespaceversion
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "compatibleNamespaceVersion"))

    @compatible_namespace_version.setter
    def compatible_namespace_version(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239af4753a04709eb0bbfb611ef122c5df4cec610956ba3f22ff5058504b1cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibleNamespaceVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotthingsgraph.CfnFlowTemplate.DefinitionDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"language": "language", "text": "text"},
    )
    class DefinitionDocumentProperty:
        def __init__(self, *, language: builtins.str, text: builtins.str) -> None:
            '''
            :param language: ``CfnFlowTemplate.DefinitionDocumentProperty.Language``.
            :param text: ``CfnFlowTemplate.DefinitionDocumentProperty.Text``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotthingsgraph-flowtemplate-definitiondocument.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotthingsgraph as iotthingsgraph
                
                definition_document_property = iotthingsgraph.CfnFlowTemplate.DefinitionDocumentProperty(
                    language="language",
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9d30bb31537517024c8c40082cc179ce79100aaa56a0e25e3d5301708db038d)
                check_type(argname="argument language", value=language, expected_type=type_hints["language"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "language": language,
                "text": text,
            }

        @builtins.property
        def language(self) -> builtins.str:
            '''``CfnFlowTemplate.DefinitionDocumentProperty.Language``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotthingsgraph-flowtemplate-definitiondocument.html#cfn-iotthingsgraph-flowtemplate-definitiondocument-language
            '''
            result = self._values.get("language")
            assert result is not None, "Required property 'language' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def text(self) -> builtins.str:
            '''``CfnFlowTemplate.DefinitionDocumentProperty.Text``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotthingsgraph-flowtemplate-definitiondocument.html#cfn-iotthingsgraph-flowtemplate-definitiondocument-text
            '''
            result = self._values.get("text")
            assert result is not None, "Required property 'text' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotthingsgraph.CfnFlowTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "compatible_namespace_version": "compatibleNamespaceVersion",
    },
)
class CfnFlowTemplateProps:
    def __init__(
        self,
        *,
        definition: typing.Union[typing.Union[CfnFlowTemplate.DefinitionDocumentProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        compatible_namespace_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnFlowTemplate``.

        :param definition: ``AWS::IoTThingsGraph::FlowTemplate.Definition``.
        :param compatible_namespace_version: ``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotthingsgraph as iotthingsgraph
            
            cfn_flow_template_props = iotthingsgraph.CfnFlowTemplateProps(
                definition=iotthingsgraph.CfnFlowTemplate.DefinitionDocumentProperty(
                    language="language",
                    text="text"
                ),
            
                # the properties below are optional
                compatible_namespace_version=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a97ab8556e8f4ff38fff19c06e27f636c1cfdf0829e3394ae13401defba994)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument compatible_namespace_version", value=compatible_namespace_version, expected_type=type_hints["compatible_namespace_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }
        if compatible_namespace_version is not None:
            self._values["compatible_namespace_version"] = compatible_namespace_version

    @builtins.property
    def definition(
        self,
    ) -> typing.Union[CfnFlowTemplate.DefinitionDocumentProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''``AWS::IoTThingsGraph::FlowTemplate.Definition``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-definition
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Union[CfnFlowTemplate.DefinitionDocumentProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def compatible_namespace_version(self) -> typing.Optional[jsii.Number]:
        '''``AWS::IoTThingsGraph::FlowTemplate.CompatibleNamespaceVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotthingsgraph-flowtemplate.html#cfn-iotthingsgraph-flowtemplate-compatiblenamespaceversion
        '''
        result = self._values.get("compatible_namespace_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFlowTemplate",
    "CfnFlowTemplateProps",
]

publication.publish()

def _typecheckingstub__3a55c29432fc6d309ea33f36b6b6e3fe83a1f3e1433cc4c03ee26d731b785cb5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    definition: typing.Union[typing.Union[CfnFlowTemplate.DefinitionDocumentProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    compatible_namespace_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b013964bc6199e425a48c2f7fa088b62453f881bbaeb6be93ccf05adc1c79ab(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0e48caa8fa880a25352a23bd5d08609df4a93951baef23670d3b1c65fd6d89(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e472f3a73381485805b3b87baaaeee8043ec4eefec93488acd804c451a9958b6(
    value: typing.Union[CfnFlowTemplate.DefinitionDocumentProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239af4753a04709eb0bbfb611ef122c5df4cec610956ba3f22ff5058504b1cb5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d30bb31537517024c8c40082cc179ce79100aaa56a0e25e3d5301708db038d(
    *,
    language: builtins.str,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a97ab8556e8f4ff38fff19c06e27f636c1cfdf0829e3394ae13401defba994(
    *,
    definition: typing.Union[typing.Union[CfnFlowTemplate.DefinitionDocumentProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    compatible_namespace_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
