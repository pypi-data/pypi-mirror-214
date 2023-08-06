'''
# Include CloudFormation templates in the CDK

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module contains a set of classes whose goal is to facilitate working
with existing CloudFormation templates in the CDK.
It can be thought of as an extension of the capabilities of the
[`CfnInclude` class](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.CfnInclude.html).

## Basic usage

Assume we have a file with an existing template.
It could be in JSON format, in a file `my-template.json`:

```json
{
  "Resources": {
    "Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      }
    }
  }
}
```

Or it could by in YAML format, in a file `my-template.yaml`:

```yaml
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: some-bucket-name
```

It can be included in a CDK application with the following code:

```python
cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.json"
)
```

Or, if your template uses YAML:

```python
cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.yaml"
)
```

**Note**: different YAML parsers sometimes don't agree on what exactly constitutes valid YAML.
If you get a YAML exception when including your template,
try converting it to JSON, and including that file instead.
If you're downloading your template from the CloudFormation AWS Console,
you can easily get it in JSON format by clicking the 'View in Designer'
button on the 'Template' tab -
once in Designer, select JSON in the "Choose template language"
radio buttons on the bottom pane.

This will add all resources from `my-template.json` / `my-template.yaml` into the CDK application,
preserving their original logical IDs from the template file.

Note that this including process will *not* execute any
[CloudFormation transforms](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html) -
including the [Serverless transform](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-aws-serverless.html).

Any resource from the included template can be retrieved by referring to it by its logical ID from the template.
If you know the class of the CDK object that corresponds to that resource,
you can cast the returned object to the correct type:

```python
# cfn_template: cfn_inc.CfnInclude

cfn_bucket = cfn_template.get_resource("Bucket")
```

Note that any resources not present in the latest version of the CloudFormation schema
at the time of publishing the version of this module that you depend on,
including [Custom Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html),
will be returned as instances of the class `CfnResource`,
and so cannot be cast to a different resource type.

Any modifications made to that resource will be reflected in the resulting CDK template;
for example, the name of the bucket can be changed:

```python
# cfn_template: cfn_inc.CfnInclude

cfn_bucket = cfn_template.get_resource("Bucket")
cfn_bucket.bucket_name = "my-bucket-name"
```

You can also refer to the resource when defining other constructs,
including the higher-level ones
(those whose name does not start with `Cfn`),
for example:

```python
# cfn_template: cfn_inc.CfnInclude

cfn_bucket = cfn_template.get_resource("Bucket")

role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)
role.add_to_policy(iam.PolicyStatement(
    actions=["s3:*"],
    resources=[cfn_bucket.attr_arn]
))
```

### Converting L1 resources to L2

The resources the `getResource` method returns are what the CDK calls
[Layer 1 resources](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html#cfn_layer_cfn)
(like `CfnBucket`).
However, in many places in the Construct Library,
the CDK requires so-called Layer 2 resources, like `IBucket`.
There are two ways of going from an L1 to an L2 resource.

#### Using`fromCfn*()` methods

This is the preferred method of converting an L1 resource to an L2.
It works by invoking a static method of the class of the L2 resource
whose name starts with `fromCfn` -
for example, for KMS Keys, that would be the `Kms.fromCfnKey()` method -
and passing the L1 instance as an argument:

```python
# cfn_template: cfn_inc.CfnInclude

cfn_key = cfn_template.get_resource("Key")
key = kms.Key.from_cfn_key(cfn_key)
```

This returns an instance of the `kms.IKey` type that can be passed anywhere in the CDK an `IKey` is expected.
What is more, that `IKey` instance will be mutable -
which means calling any mutating methods on it,
like `addToResourcePolicy()`,
will be reflected in the resulting template.

Note that, in some cases, the `fromCfn*()` method might not be able to create an L2 from the underlying L1.
This can happen when the underlying L1 heavily uses CloudFormation functions.
For example, if you tried to create an L2 `IKey`
from an L1 represented as this CloudFormation template:

```json
{
  "Resources": {
    "Key": {
      "Type": "AWS::KMS::Key",
      "Properties": {
        "KeyPolicy": {
          "Statement": [
            {
              "Fn::If": [
                "Condition",
                {
                  "Action": "kms:if-action",
                  "Resource": "*",
                  "Principal": "*",
                  "Effect": "Allow"
                },
                {
                  "Action": "kms:else-action",
                  "Resource": "*",
                  "Principal": "*",
                  "Effect": "Allow"
                }
              ]
            }
          ],
          "Version": "2012-10-17"
        }
      }
    }
  }
}
```

The `Key.fromCfnKey()` method does not know how to translate that into CDK L2 concepts,
and would throw an exception.

In those cases, you need the use the second method of converting an L1 to an L2.

#### Using `from*Name/Arn/Attributes()` methods

If the resource you need does not have a `fromCfn*()` method,
or if it does, but it throws an exception for your particular L1,
you need to use the second method of converting an L1 resource to L2.

Each L2 class has static factory methods with names like `from*Name()`,
`from*Arn()`, and/or `from*Attributes()`.
You can obtain an L2 resource from an L1 by passing the correct properties of the L1 as the arguments to those methods:

```python
# cfn_template: cfn_inc.CfnInclude

# using from*Attributes()
# private_cfn_subnet1: ec2.CfnSubnet
# private_cfn_subnet2: ec2.CfnSubnet


# using from*Name()
cfn_bucket = cfn_template.get_resource("Bucket")
bucket = s3.Bucket.from_bucket_name(self, "L2Bucket", cfn_bucket.ref)

# using from*Arn()
cfn_key = cfn_template.get_resource("Key")
key = kms.Key.from_key_arn(self, "L2Key", cfn_key.attr_arn)
cfn_vpc = cfn_template.get_resource("Vpc")
vpc = ec2.Vpc.from_vpc_attributes(self, "L2Vpc",
    vpc_id=cfn_vpc.ref,
    availability_zones=core.Fn.get_azs(),
    private_subnet_ids=[private_cfn_subnet1.ref, private_cfn_subnet2.ref]
)
```

As long as they just need to be referenced,
and not changed in any way, everything should work;
however, note that resources returned from those methods,
unlike those returned by `fromCfn*()` methods,
are immutable, which means calling any mutating methods on them will have no effect.
You will have to mutate the underlying L1 in order to change them.

## Non-resource template elements

In addition to resources,
you can also retrieve and mutate all other template elements:

* [Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html):

  ```python
  # cfn_template: cfn_inc.CfnInclude

  param = cfn_template.get_parameter("MyParameter")

  # mutating the parameter
  param.default = "MyDefault"
  ```
* [Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html):

  ```python
  # cfn_template: cfn_inc.CfnInclude

  condition = cfn_template.get_condition("MyCondition")

  # mutating the condition
  condition.expression = core.Fn.condition_equals(1, 2)
  ```
* [Mappings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html):

  ```python
  # cfn_template: cfn_inc.CfnInclude

  mapping = cfn_template.get_mapping("MyMapping")

  # mutating the mapping
  mapping.set_value("my-region", "AMI", "ami-04681a1dbd79675a5")
  ```
* [Service Catalog template Rules](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html):

  ```python
  # cfn_template: cfn_inc.CfnInclude

  # mutating the rule
  # my_parameter: core.CfnParameter

  rule = cfn_template.get_rule("MyRule")
  rule.add_assertion(core.Fn.condition_contains(["m1.small"], my_parameter.value_as_string), "MyParameter has to be m1.small")
  ```
* [Outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html):

  ```python
  # cfn_template: cfn_inc.CfnInclude

  # mutating the output
  # cfn_bucket: s3.CfnBucket

  output = cfn_template.get_output("MyOutput")
  output.value = cfn_bucket.attr_arn
  ```
* [Hooks for blue-green deployments](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html):

  ```python
  # cfn_template: cfn_inc.CfnInclude

  # mutating the hook
  # my_role: iam.Role

  hook = cfn_template.get_hook("MyOutput")
  code_deploy_hook = hook
  code_deploy_hook.service_role = my_role.role_arn
  ```

## Parameter replacement

If your existing template uses CloudFormation Parameters,
you may want to remove them in favor of build-time values.
You can do that using the `parameters` property:

```python
cfn_inc.CfnInclude(self, "includeTemplate",
    template_file="path/to/my/template",
    parameters={
        "MyParam": "my-value"
    }
)
```

This will replace all references to `MyParam` with the string `'my-value'`,
and `MyParam` will be removed from the 'Parameters' section of the resulting template.

## Nested Stacks

This module also supports templates that use [nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html).

For example, if you have the following parent template:

```json
{
  "Resources": {
    "ChildStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": "https://my-s3-template-source.s3.amazonaws.com/child-stack.json"
      }
    }
  }
}
```

where the child template pointed to by `https://my-s3-template-source.s3.amazonaws.com/child-stack.json` is:

```json
{
  "Resources": {
    "MyBucket": {
      "Type": "AWS::S3::Bucket"
    }
  }
}
```

You can include both the parent stack,
and the nested stack in your CDK application as follows:

```python
parent_template = cfn_inc.CfnInclude(self, "ParentStack",
    template_file="path/to/my-parent-template.json",
    load_nested_stacks={
        "ChildStack": cfn_inc.CfnIncludeProps(
            template_file="path/to/my-nested-template.json"
        )
    }
)
```

Here, `path/to/my-nested-template.json`
represents the path on disk to the downloaded template file from the original template URL of the nested stack
(`https://my-s3-template-source.s3.amazonaws.com/child-stack.json`).
In the CDK application,
this file will be turned into an [Asset](https://docs.aws.amazon.com/cdk/latest/guide/assets.html),
and the `TemplateURL` property of the nested stack resource
will be modified to point to that asset.

The included nested stack can be accessed with the `getNestedStack` method:

```python
# parent_template: cfn_inc.CfnInclude


included_child_stack = parent_template.get_nested_stack("ChildStack")
child_stack = included_child_stack.stack
child_template = included_child_stack.included_template
```

Now you can reference resources from `ChildStack`,
and modify them like any other included template:

```python
# child_template: cfn_inc.CfnInclude


cfn_bucket = child_template.get_resource("MyBucket")
cfn_bucket.bucket_name = "my-new-bucket-name"

role = iam.Role(self, "MyRole",
    assumed_by=iam.AccountRootPrincipal()
)

role.add_to_policy(iam.PolicyStatement(
    actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"
    ],
    resources=[cfn_bucket.attr_arn]
))
```

You can also include the nested stack after the `CfnInclude` object was created,
instead of doing it on construction:

```python
# parent_template: cfn_inc.CfnInclude

included_child_stack = parent_template.load_nested_stack("ChildTemplate",
    template_file="path/to/my-nested-template.json"
)
```

## Vending CloudFormation templates as Constructs

In many cases, there are existing CloudFormation templates that are not entire applications,
but more like specialized fragments, implementing a particular pattern or best practice.
If you have templates like that,
you can use the `CfnInclude` class to vend them as CDK Constructs:

```python
from constructs import Construct
import aws_cdk.cloudformation_include as cfn_inc
import path as path

class MyConstruct(Construct):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        # include a template inside the Construct
        cfn_inc.CfnInclude(self, "MyConstruct",
            template_file=path.join(__dirname, "my-template.json"),
            preserve_logical_ids=False
        )
```

Notice the `preserveLogicalIds` parameter -
it makes sure the logical IDs of all the included template elements are re-named using CDK's algorithm,
guaranteeing they are unique within your application.
Without that parameter passed,
instantiating `MyConstruct` twice in the same Stack would result in duplicated logical IDs.
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
import constructs as _constructs_77d1e7e8


class CfnInclude(
    _aws_cdk_core_f4b25747.CfnElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/cloudformation-include.CfnInclude",
):
    '''Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    :exampleMetadata: infused

    Example::

        cfn_template = cfn_inc.CfnInclude(self, "Template",
            template_file="my-template.json"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, typing.Union["CfnIncludeProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3bb4e628f0f7d9dc75fd726d376ac771922ab3819ff8f99c9ddb68dd59f12d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIncludeProps(
            template_file=template_file,
            load_nested_stacks=load_nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getCondition")
    def get_condition(
        self,
        condition_name: builtins.str,
    ) -> _aws_cdk_core_f4b25747.CfnCondition:
        '''Returns the CfnCondition object from the 'Conditions' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Condition with the given name is not present in the template,
        throws an exception.

        :param condition_name: the name of the Condition in the CloudFormation template file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5a0c7f41eaa1a8f191291aa9de40c89d46ac733246c896e86e480269324f97)
            check_type(argname="argument condition_name", value=condition_name, expected_type=type_hints["condition_name"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnCondition, jsii.invoke(self, "getCondition", [condition_name]))

    @jsii.member(jsii_name="getHook")
    def get_hook(self, hook_logical_id: builtins.str) -> _aws_cdk_core_f4b25747.CfnHook:
        '''Returns the CfnHook object from the 'Hooks' section of the included CloudFormation template with the given logical ID.

        Any modifications performed on the returned object will be reflected in the resulting CDK template.

        If a Hook with the given logical ID is not present in the template,
        an exception will be thrown.

        :param hook_logical_id: the logical ID of the Hook in the included CloudFormation template's 'Hooks' section.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35991c2bf1db192aae4fc779c6651fae41c9f8fba40faebafd3294897a859c65)
            check_type(argname="argument hook_logical_id", value=hook_logical_id, expected_type=type_hints["hook_logical_id"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnHook, jsii.invoke(self, "getHook", [hook_logical_id]))

    @jsii.member(jsii_name="getMapping")
    def get_mapping(
        self,
        mapping_name: builtins.str,
    ) -> _aws_cdk_core_f4b25747.CfnMapping:
        '''Returns the CfnMapping object from the 'Mappings' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Mapping with the given name is not present in the template,
        an exception will be thrown.

        :param mapping_name: the name of the Mapping in the template to retrieve.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f696ec50b8ce04c683df8ddfd925f5b0ffce9afb6ec36455ec2b0aca689f501)
            check_type(argname="argument mapping_name", value=mapping_name, expected_type=type_hints["mapping_name"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnMapping, jsii.invoke(self, "getMapping", [mapping_name]))

    @jsii.member(jsii_name="getNestedStack")
    def get_nested_stack(self, logical_id: builtins.str) -> "IncludedNestedStack":
        '''Returns a loaded NestedStack with name logicalId.

        For a nested stack to be returned by this method,
        it must be specified either in the {@link CfnIncludeProps.loadNestedStacks} property,
        or through the {@link loadNestedStack} method.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03477ec6b0fd7fb319f4bc742a91b8f1834203a87e61e19a049e71c55252915)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast("IncludedNestedStack", jsii.invoke(self, "getNestedStack", [logical_id]))

    @jsii.member(jsii_name="getOutput")
    def get_output(self, logical_id: builtins.str) -> _aws_cdk_core_f4b25747.CfnOutput:
        '''Returns the CfnOutput object from the 'Outputs' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If an Output with the given name is not present in the template,
        throws an exception.

        :param logical_id: the name of the output to retrieve.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7eee5c7f3c872ccd683ae10076118756e8f70c7093e76a8d63c120293ea5e4)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnOutput, jsii.invoke(self, "getOutput", [logical_id]))

    @jsii.member(jsii_name="getParameter")
    def get_parameter(
        self,
        parameter_name: builtins.str,
    ) -> _aws_cdk_core_f4b25747.CfnParameter:
        '''Returns the CfnParameter object from the 'Parameters' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e99811ea229129b46b10e08a7a66a93ea766f59ba1332ccce1e64f4b45022da)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnParameter, jsii.invoke(self, "getParameter", [parameter_name]))

    @jsii.member(jsii_name="getResource")
    def get_resource(
        self,
        logical_id: builtins.str,
    ) -> _aws_cdk_core_f4b25747.CfnResource:
        '''Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93208b7203cebcef1fa9f571222ea54df52ca58042bec07fd8dd5cb50ab82b53)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnResource, jsii.invoke(self, "getResource", [logical_id]))

    @jsii.member(jsii_name="getRule")
    def get_rule(self, rule_name: builtins.str) -> _aws_cdk_core_f4b25747.CfnRule:
        '''Returns the CfnRule object from the 'Rules' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Rule with the given name is not present in the template,
        an exception will be thrown.

        :param rule_name: the name of the Rule in the CloudFormation template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48eee6dc74dc264a4c970bb8d086f1011d13ca50be72b14d47b3d50167442648)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
        return typing.cast(_aws_cdk_core_f4b25747.CfnRule, jsii.invoke(self, "getRule", [rule_name]))

    @jsii.member(jsii_name="loadNestedStack")
    def load_nested_stack(
        self,
        logical_id: builtins.str,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, typing.Union["CfnIncludeProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> "IncludedNestedStack":
        '''Includes a template for a child stack inside of this parent template.

        A child with this logical ID must exist in the template,
        and be of type AWS::CloudFormation::Stack.
        This is equivalent to specifying the value in the {@link CfnIncludeProps.loadNestedStacks}
        property on object construction.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.
        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :return: the same {@link IncludedNestedStack} object that {@link getNestedStack} returns for this logical ID
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d1cbbba7e43a3b6b1fb8b1221a4774f9456c0de52ce500a517f75a54396ea1)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        nested_stack_props = CfnIncludeProps(
            template_file=template_file,
            load_nested_stacks=load_nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        return typing.cast("IncludedNestedStack", jsii.invoke(self, "loadNestedStack", [logical_id, nested_stack_props]))


@jsii.data_type(
    jsii_type="@aws-cdk/cloudformation-include.CfnIncludeProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "load_nested_stacks": "loadNestedStacks",
        "parameters": "parameters",
        "preserve_logical_ids": "preserveLogicalIds",
    },
)
class CfnIncludeProps:
    def __init__(
        self,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, typing.Union["CfnIncludeProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Construction properties of {@link CfnInclude}.

        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :exampleMetadata: infused

        Example::

            parent_template = cfn_inc.CfnInclude(self, "ParentStack",
                template_file="path/to/my-parent-template.json",
                load_nested_stacks={
                    "ChildStack": cfn_inc.CfnIncludeProps(
                        template_file="path/to/my-nested-template.json"
                    )
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d91be4b5ebdd2a0b22442e458721e46776a703286cd2130d5a8f1928a38333c)
            check_type(argname="argument template_file", value=template_file, expected_type=type_hints["template_file"])
            check_type(argname="argument load_nested_stacks", value=load_nested_stacks, expected_type=type_hints["load_nested_stacks"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument preserve_logical_ids", value=preserve_logical_ids, expected_type=type_hints["preserve_logical_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_file": template_file,
        }
        if load_nested_stacks is not None:
            self._values["load_nested_stacks"] = load_nested_stacks
        if parameters is not None:
            self._values["parameters"] = parameters
        if preserve_logical_ids is not None:
            self._values["preserve_logical_ids"] = preserve_logical_ids

    @builtins.property
    def template_file(self) -> builtins.str:
        '''Path to the template file.

        Both JSON and YAML template formats are supported.
        '''
        result = self._values.get("template_file")
        assert result is not None, "Required property 'template_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_nested_stacks(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]]:
        '''Specifies the template files that define nested stacks that should be included.

        If your template specifies a stack that isn't included here, it won't be created as a NestedStack
        resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method
        (but will still be accessible from the {@link CfnInclude.getResource} method).

        If you include a stack here with an ID that isn't in the template,
        or is in the template but is not a nested stack,
        template creation will fail and an error will be thrown.

        :default: - no nested stacks will be included
        '''
        result = self._values.get("load_nested_stacks")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Specifies parameters to be replaced by the values in this mapping.

        Any parameters in the template that aren't specified here will be left unmodified.
        If you include a parameter here with an ID that isn't in the template,
        template creation will fail and an error will be thrown.

        :default: - no parameters will be replaced
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def preserve_logical_ids(self) -> typing.Optional[builtins.bool]:
        '''Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file.

        If you're vending a Construct using an existing CloudFormation template,
        make sure to pass this as ``false``.

        **Note**: regardless of whether this option is true or false,
        the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element,
        as specified in the template file.

        :default: true
        '''
        result = self._values.get("preserve_logical_ids")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIncludeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloudformation-include.IncludedNestedStack",
    jsii_struct_bases=[],
    name_mapping={"included_template": "includedTemplate", "stack": "stack"},
)
class IncludedNestedStack:
    def __init__(
        self,
        *,
        included_template: CfnInclude,
        stack: _aws_cdk_core_f4b25747.NestedStack,
    ) -> None:
        '''The type returned from {@link CfnInclude.getNestedStack}. Contains both the NestedStack object and CfnInclude representations of the child stack.

        :param included_template: The CfnInclude that represents the template, which can be used to access Resources and other template elements.
        :param stack: The NestedStack object which represents the scope of the template.

        :exampleMetadata: infused

        Example::

            # parent_template: cfn_inc.CfnInclude
            
            
            included_child_stack = parent_template.get_nested_stack("ChildStack")
            child_stack = included_child_stack.stack
            child_template = included_child_stack.included_template
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122f65bf630474418ab80b6e6d19758d8ea5d4afa18a0e74a2f2edd6cdb33e53)
            check_type(argname="argument included_template", value=included_template, expected_type=type_hints["included_template"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "included_template": included_template,
            "stack": stack,
        }

    @builtins.property
    def included_template(self) -> CfnInclude:
        '''The CfnInclude that represents the template, which can be used to access Resources and other template elements.'''
        result = self._values.get("included_template")
        assert result is not None, "Required property 'included_template' is missing"
        return typing.cast(CfnInclude, result)

    @builtins.property
    def stack(self) -> _aws_cdk_core_f4b25747.NestedStack:
        '''The NestedStack object which represents the scope of the template.'''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_aws_cdk_core_f4b25747.NestedStack, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludedNestedStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
    "IncludedNestedStack",
]

publication.publish()

def _typecheckingstub__2f3bb4e628f0f7d9dc75fd726d376ac771922ab3819ff8f99c9ddb68dd59f12d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    template_file: builtins.str,
    load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, typing.Union[CfnIncludeProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    preserve_logical_ids: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5a0c7f41eaa1a8f191291aa9de40c89d46ac733246c896e86e480269324f97(
    condition_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35991c2bf1db192aae4fc779c6651fae41c9f8fba40faebafd3294897a859c65(
    hook_logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f696ec50b8ce04c683df8ddfd925f5b0ffce9afb6ec36455ec2b0aca689f501(
    mapping_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03477ec6b0fd7fb319f4bc742a91b8f1834203a87e61e19a049e71c55252915(
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7eee5c7f3c872ccd683ae10076118756e8f70c7093e76a8d63c120293ea5e4(
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e99811ea229129b46b10e08a7a66a93ea766f59ba1332ccce1e64f4b45022da(
    parameter_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93208b7203cebcef1fa9f571222ea54df52ca58042bec07fd8dd5cb50ab82b53(
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48eee6dc74dc264a4c970bb8d086f1011d13ca50be72b14d47b3d50167442648(
    rule_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d1cbbba7e43a3b6b1fb8b1221a4774f9456c0de52ce500a517f75a54396ea1(
    logical_id: builtins.str,
    *,
    template_file: builtins.str,
    load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, typing.Union[CfnIncludeProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    preserve_logical_ids: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d91be4b5ebdd2a0b22442e458721e46776a703286cd2130d5a8f1928a38333c(
    *,
    template_file: builtins.str,
    load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, typing.Union[CfnIncludeProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    preserve_logical_ids: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122f65bf630474418ab80b6e6d19758d8ea5d4afa18a0e74a2f2edd6cdb33e53(
    *,
    included_template: CfnInclude,
    stack: _aws_cdk_core_f4b25747.NestedStack,
) -> None:
    """Type checking stubs"""
    pass
