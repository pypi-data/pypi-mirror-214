'''
# AWS Resource Access Manager Construct Library

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
import aws_cdk.aws_ram as ram
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for RAM construct libraries](https://constructs.dev/search?q=ram)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::RAM resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RAM](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html).

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
class CfnPermission(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ram.CfnPermission",
):
    '''A CloudFormation ``AWS::RAM::Permission``.

    Creates a customer managed permission for a specified resource type that you can attach to resource shares. It is created in the AWS Region in which you call the operation.

    :cloudformationResource: AWS::RAM::Permission
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ram as ram
        
        # policy_template: Any
        
        cfn_permission = ram.CfnPermission(self, "MyCfnPermission",
            name="name",
            policy_template=policy_template,
            resource_type="resourceType",
        
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
        name: builtins.str,
        policy_template: typing.Any,
        resource_type: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RAM::Permission``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Specifies the name of the customer managed permission. The name must be unique within the AWS Region .
        :param policy_template: A string in JSON format string that contains the following elements of a resource-based policy:. - *Effect* : must be set to ``ALLOW`` . - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* . - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* . This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.
        :param resource_type: Specifies the name of the resource type that this customer managed permission applies to. The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.
        :param tags: Specifies a list of one or more tag key and value pairs to attach to the permission.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89addd51607d731afb57835ff3dcb233ae09110dc91764f83fca52acef14428b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPermissionProps(
            name=name,
            policy_template=policy_template,
            resource_type=resource_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63f3de02c25b28fb2f099d9d63994207f94ea45349eec0d5bdc367ae88f8a10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a48886e654c57754b325a05336aad13fe4faa9c2cc8df58770b291d58ee3d999)
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
        '''The Amazon Resource Name (ARN) of the new permission.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrIsResourceTypeDefault")
    def attr_is_resource_type_default(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''Specifies whether this permission is the default for new resource shares that include resources of the associated resource type.

        :cloudformationAttribute: IsResourceTypeDefault
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrIsResourceTypeDefault"))

    @builtins.property
    @jsii.member(jsii_name="attrPermissionType")
    def attr_permission_type(self) -> builtins.str:
        '''The type of managed permission. This can be one of the following values:.

        - *AWS_MANAGED_PERMISSION* – AWS created and manages this managed permission. You can associate it with your resource shares, but you can't modify it.
        - *CUSTOMER_MANAGED_PERMISSION* – You, or another principal in your account created this managed permission. You can associate it with your resource shares and create new versions that have different permissions.

        :cloudformationAttribute: PermissionType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPermissionType"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number for this version of the permission.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies a list of one or more tag key and value pairs to attach to the permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Specifies the name of the customer managed permission.

        The name must be unique within the AWS Region .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5ca13dca5facd9a950e3415895504ef5a01e832fcdb87189715c05c38c0e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policyTemplate")
    def policy_template(self) -> typing.Any:
        '''A string in JSON format string that contains the following elements of a resource-based policy:.

        - *Effect* : must be set to ``ALLOW`` .
        - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* .
        - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* .

        This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-policytemplate
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyTemplate"))

    @policy_template.setter
    def policy_template(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0974e6a75c3f2856bdace9d49d5cc2ba64bc3d7cbdb2689071b39b1b99c64a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        '''Specifies the name of the resource type that this customer managed permission applies to.

        The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-resourcetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb61421b305d18fa75dfed25b6eeada1c4dd897bdedc8425cf8e9a8e6bf9c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ram.CfnPermissionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "policy_template": "policyTemplate",
        "resource_type": "resourceType",
        "tags": "tags",
    },
)
class CfnPermissionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        policy_template: typing.Any,
        resource_type: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPermission``.

        :param name: Specifies the name of the customer managed permission. The name must be unique within the AWS Region .
        :param policy_template: A string in JSON format string that contains the following elements of a resource-based policy:. - *Effect* : must be set to ``ALLOW`` . - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* . - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* . This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.
        :param resource_type: Specifies the name of the resource type that this customer managed permission applies to. The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.
        :param tags: Specifies a list of one or more tag key and value pairs to attach to the permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ram as ram
            
            # policy_template: Any
            
            cfn_permission_props = ram.CfnPermissionProps(
                name="name",
                policy_template=policy_template,
                resource_type="resourceType",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea578b6bfdc4ec5ff8a8906265923f049495d9c55441d8af1a6f865290ce859)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_template", value=policy_template, expected_type=type_hints["policy_template"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_template": policy_template,
            "resource_type": resource_type,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the customer managed permission.

        The name must be unique within the AWS Region .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_template(self) -> typing.Any:
        '''A string in JSON format string that contains the following elements of a resource-based policy:.

        - *Effect* : must be set to ``ALLOW`` .
        - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* .
        - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* .

        This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-policytemplate
        '''
        result = self._values.get("policy_template")
        assert result is not None, "Required property 'policy_template' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Specifies the name of the resource type that this customer managed permission applies to.

        The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-resourcetype
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies a list of one or more tag key and value pairs to attach to the permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceShare(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ram.CfnResourceShare",
):
    '''A CloudFormation ``AWS::RAM::ResourceShare``.

    Creates a resource share. You can provide a list of the Amazon Resource Names (ARNs) for the resources that you want to share, a list of principals you want to share the resources with, and the permissions to grant those principals.
    .. epigraph::

       Sharing a resource makes it available for use by principals outside of the AWS account that created the resource. Sharing doesn't change any permissions or quotas that apply to the resource in the account that created it.

    :cloudformationResource: AWS::RAM::ResourceShare
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ram as ram
        
        cfn_resource_share = ram.CfnResourceShare(self, "MyCfnResourceShare",
            name="name",
        
            # the properties below are optional
            allow_external_principals=False,
            permission_arns=["permissionArns"],
            principals=["principals"],
            resource_arns=["resourceArns"],
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
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RAM::ResourceShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Specifies the name of the resource share.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .
        :param permission_arns: Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param principals: Specifies the principals to associate with the resource share. The possible values are:. - An AWS account ID - An Amazon Resource Name (ARN) of an organization in AWS Organizations - An ARN of an organizational unit (OU) in AWS Organizations - An ARN of an IAM role - An ARN of an IAM user .. epigraph:: Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .
        :param resource_arns: Specifies a list of one or more ARNs of the resources to associate with the resource share.
        :param tags: Specifies one or more tags to attach to the resource share itself. It doesn't attach the tags to the resources associated with the resource share.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df83174c0749f41780f29abb75aa194e56b20b9e8984257f93e6afa5dcc2fb42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceShareProps(
            name=name,
            allow_external_principals=allow_external_principals,
            permission_arns=permission_arns,
            principals=principals,
            resource_arns=resource_arns,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59eee294d8da025a5ea03ff11f5876abd395990d7589f48bcc9c153e76b67018)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bfce98aaaa42e715ff7c188f425e322a0fa7b31281257eb0a83c85613849304)
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
        '''The Amazon Resource Name (ARN) of the resource share.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies one or more tags to attach to the resource share itself.

        It doesn't attach the tags to the resources associated with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb2217c101fe754afea1b13f5e4e908d303994b314f84323fe7c75b9c4b7aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="allowExternalPrincipals")
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "allowExternalPrincipals"))

    @allow_external_principals.setter
    def allow_external_principals(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddfb5c23d8cd0048a50936428b34bdad89c5ee6ae055f31efc4546e52e927df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowExternalPrincipals", value)

    @builtins.property
    @jsii.member(jsii_name="permissionArns")
    def permission_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-permissionarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permissionArns"))

    @permission_arns.setter
    def permission_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6602b146702228b224b3413b8726b0bf71e87a6a0ab691ebcb5c8088e883a8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionArns", value)

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the principals to associate with the resource share. The possible values are:.

        - An AWS account ID
        - An Amazon Resource Name (ARN) of an organization in AWS Organizations
        - An ARN of an organizational unit (OU) in AWS Organizations
        - An ARN of an IAM role
        - An ARN of an IAM user

        .. epigraph::

           Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49abfff066fb85a69ff2aa8b6e2a6dbf8dd333171684d66412848e05ba444639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more ARNs of the resources to associate with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2348004a6619f8a8a75a6c35b829d8b406167fd1b35d94f5ee058e72576b5ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ram.CfnResourceShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_external_principals": "allowExternalPrincipals",
        "permission_arns": "permissionArns",
        "principals": "principals",
        "resource_arns": "resourceArns",
        "tags": "tags",
    },
)
class CfnResourceShareProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceShare``.

        :param name: Specifies the name of the resource share.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .
        :param permission_arns: Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param principals: Specifies the principals to associate with the resource share. The possible values are:. - An AWS account ID - An Amazon Resource Name (ARN) of an organization in AWS Organizations - An ARN of an organizational unit (OU) in AWS Organizations - An ARN of an IAM role - An ARN of an IAM user .. epigraph:: Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .
        :param resource_arns: Specifies a list of one or more ARNs of the resources to associate with the resource share.
        :param tags: Specifies one or more tags to attach to the resource share itself. It doesn't attach the tags to the resources associated with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ram as ram
            
            cfn_resource_share_props = ram.CfnResourceShareProps(
                name="name",
            
                # the properties below are optional
                allow_external_principals=False,
                permission_arns=["permissionArns"],
                principals=["principals"],
                resource_arns=["resourceArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb4e9d070ec31824f9b78b67b3a01d82a2625fae0bc9a142e1856bb04d0e5a0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument permission_arns", value=permission_arns, expected_type=type_hints["permission_arns"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if permission_arns is not None:
            self._values["permission_arns"] = permission_arns
        if principals is not None:
            self._values["principals"] = principals
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        '''
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def permission_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-permissionarns
        '''
        result = self._values.get("permission_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the principals to associate with the resource share. The possible values are:.

        - An AWS account ID
        - An Amazon Resource Name (ARN) of an organization in AWS Organizations
        - An ARN of an organizational unit (OU) in AWS Organizations
        - An ARN of an IAM role
        - An ARN of an IAM user

        .. epigraph::

           Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more ARNs of the resources to associate with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        '''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies one or more tags to attach to the resource share itself.

        It doesn't attach the tags to the resources associated with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPermission",
    "CfnPermissionProps",
    "CfnResourceShare",
    "CfnResourceShareProps",
]

publication.publish()

def _typecheckingstub__89addd51607d731afb57835ff3dcb233ae09110dc91764f83fca52acef14428b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    policy_template: typing.Any,
    resource_type: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63f3de02c25b28fb2f099d9d63994207f94ea45349eec0d5bdc367ae88f8a10(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48886e654c57754b325a05336aad13fe4faa9c2cc8df58770b291d58ee3d999(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5ca13dca5facd9a950e3415895504ef5a01e832fcdb87189715c05c38c0e7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0974e6a75c3f2856bdace9d49d5cc2ba64bc3d7cbdb2689071b39b1b99c64a2(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb61421b305d18fa75dfed25b6eeada1c4dd897bdedc8425cf8e9a8e6bf9c3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea578b6bfdc4ec5ff8a8906265923f049495d9c55441d8af1a6f865290ce859(
    *,
    name: builtins.str,
    policy_template: typing.Any,
    resource_type: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df83174c0749f41780f29abb75aa194e56b20b9e8984257f93e6afa5dcc2fb42(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    allow_external_principals: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59eee294d8da025a5ea03ff11f5876abd395990d7589f48bcc9c153e76b67018(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfce98aaaa42e715ff7c188f425e322a0fa7b31281257eb0a83c85613849304(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb2217c101fe754afea1b13f5e4e908d303994b314f84323fe7c75b9c4b7aa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddfb5c23d8cd0048a50936428b34bdad89c5ee6ae055f31efc4546e52e927df(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6602b146702228b224b3413b8726b0bf71e87a6a0ab691ebcb5c8088e883a8a8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49abfff066fb85a69ff2aa8b6e2a6dbf8dd333171684d66412848e05ba444639(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2348004a6619f8a8a75a6c35b829d8b406167fd1b35d94f5ee058e72576b5ed6(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb4e9d070ec31824f9b78b67b3a01d82a2625fae0bc9a142e1856bb04d0e5a0(
    *,
    name: builtins.str,
    allow_external_principals: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
