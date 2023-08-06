'''
# AWS::LicenseManager Construct Library

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
import aws_cdk.aws_licensemanager as licensemanager
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for LicenseManager construct libraries](https://constructs.dev/search?q=licensemanager)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::LicenseManager resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManager.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::LicenseManager](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManager.html).

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
class CfnGrant(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-licensemanager.CfnGrant",
):
    '''A CloudFormation ``AWS::LicenseManager::Grant``.

    Specifies a grant.

    A grant shares the use of license entitlements with specific AWS accounts . For more information, see `Granted licenses <https://docs.aws.amazon.com/license-manager/latest/userguide/granted-licenses.html>`_ in the *AWS License Manager User Guide* .

    :cloudformationResource: AWS::LicenseManager::Grant
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_licensemanager as licensemanager
        
        cfn_grant = licensemanager.CfnGrant(self, "MyCfnGrant",
            allowed_operations=["allowedOperations"],
            grant_name="grantName",
            home_region="homeRegion",
            license_arn="licenseArn",
            principals=["principals"],
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        grant_name: typing.Optional[builtins.str] = None,
        home_region: typing.Optional[builtins.str] = None,
        license_arn: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::LicenseManager::Grant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param allowed_operations: Allowed operations for the grant.
        :param grant_name: Grant name.
        :param home_region: Home Region of the grant.
        :param license_arn: License ARN.
        :param principals: The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):. - An AWS account, which includes only the account specified. - An organizational unit (OU), which includes all accounts in the OU. - An organization, which will include all accounts across your organization.
        :param status: Granted license status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cfb01eaf2e60f6d86118f6a67a9ca1f909c856f4a1df234e7cf60cc3bc4f052)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGrantProps(
            allowed_operations=allowed_operations,
            grant_name=grant_name,
            home_region=home_region,
            license_arn=license_arn,
            principals=principals,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d58eca7fd6f15ce9ba5f9055106a7cd57d8b5e73bc36f6eb0b0cd73a66ec494)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5abc50cebfd23c96cdca11ee7bad500dcd66654bf98fc8a4b5d8fe4f4f1257b6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGrantArn")
    def attr_grant_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the grant.

        :cloudformationAttribute: GrantArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGrantArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The grant version.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="allowedOperations")
    def allowed_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allowed operations for the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-allowedoperations
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOperations"))

    @allowed_operations.setter
    def allowed_operations(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42210aafe4071d70a83c3ad694f6cbcff6d70522b6bcf275fc8231999c3e51bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOperations", value)

    @builtins.property
    @jsii.member(jsii_name="grantName")
    def grant_name(self) -> typing.Optional[builtins.str]:
        '''Grant name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grantName"))

    @grant_name.setter
    def grant_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44355f69624bc48c1a72c3f00697478fdbe47d01b17e493c3f7715228b0f365c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantName", value)

    @builtins.property
    @jsii.member(jsii_name="homeRegion")
    def home_region(self) -> typing.Optional[builtins.str]:
        '''Home Region of the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-homeregion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homeRegion"))

    @home_region.setter
    def home_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bec4e32bebad96d2ef2463640c6f6d6c9c3bb1379a497f894958e14241e90e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeRegion", value)

    @builtins.property
    @jsii.member(jsii_name="licenseArn")
    def license_arn(self) -> typing.Optional[builtins.str]:
        '''License ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-licensearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseArn"))

    @license_arn.setter
    def license_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d83a85f53c039c1c928847a68f495615a89f6d5c1c822456896d0f7222a9a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseArn", value)

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):.

        - An AWS account, which includes only the account specified.
        - An organizational unit (OU), which includes all accounts in the OU.
        - An organization, which will include all accounts across your organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-principals
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569a23d2525cef8226d581b3db0346e2fbb0813cde187cb4ca2a0b5d043626ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''Granted license status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c6a9c98a59d425b901a56da731f79bc37e50909631583fd71be399d7f7eb33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-licensemanager.CfnGrantProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_operations": "allowedOperations",
        "grant_name": "grantName",
        "home_region": "homeRegion",
        "license_arn": "licenseArn",
        "principals": "principals",
        "status": "status",
    },
)
class CfnGrantProps:
    def __init__(
        self,
        *,
        allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        grant_name: typing.Optional[builtins.str] = None,
        home_region: typing.Optional[builtins.str] = None,
        license_arn: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGrant``.

        :param allowed_operations: Allowed operations for the grant.
        :param grant_name: Grant name.
        :param home_region: Home Region of the grant.
        :param license_arn: License ARN.
        :param principals: The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):. - An AWS account, which includes only the account specified. - An organizational unit (OU), which includes all accounts in the OU. - An organization, which will include all accounts across your organization.
        :param status: Granted license status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_licensemanager as licensemanager
            
            cfn_grant_props = licensemanager.CfnGrantProps(
                allowed_operations=["allowedOperations"],
                grant_name="grantName",
                home_region="homeRegion",
                license_arn="licenseArn",
                principals=["principals"],
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02b4d210550141f89c9976c05eb7dd0f48f2865927adc5d82c2d594e60d2124)
            check_type(argname="argument allowed_operations", value=allowed_operations, expected_type=type_hints["allowed_operations"])
            check_type(argname="argument grant_name", value=grant_name, expected_type=type_hints["grant_name"])
            check_type(argname="argument home_region", value=home_region, expected_type=type_hints["home_region"])
            check_type(argname="argument license_arn", value=license_arn, expected_type=type_hints["license_arn"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_operations is not None:
            self._values["allowed_operations"] = allowed_operations
        if grant_name is not None:
            self._values["grant_name"] = grant_name
        if home_region is not None:
            self._values["home_region"] = home_region
        if license_arn is not None:
            self._values["license_arn"] = license_arn
        if principals is not None:
            self._values["principals"] = principals
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def allowed_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allowed operations for the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-allowedoperations
        '''
        result = self._values.get("allowed_operations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def grant_name(self) -> typing.Optional[builtins.str]:
        '''Grant name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantname
        '''
        result = self._values.get("grant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_region(self) -> typing.Optional[builtins.str]:
        '''Home Region of the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-homeregion
        '''
        result = self._values.get("home_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_arn(self) -> typing.Optional[builtins.str]:
        '''License ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-licensearn
        '''
        result = self._values.get("license_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):.

        - An AWS account, which includes only the account specified.
        - An organizational unit (OU), which includes all accounts in the OU.
        - An organization, which will include all accounts across your organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Granted license status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGrantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLicense(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-licensemanager.CfnLicense",
):
    '''A CloudFormation ``AWS::LicenseManager::License``.

    Specifies a granted license.

    Granted licenses are licenses for products that your organization purchased from AWS Marketplace or directly from a seller who integrated their software with managed entitlements. For more information, see `Granted licenses <https://docs.aws.amazon.com/license-manager/latest/userguide/granted-licenses.html>`_ in the *AWS License Manager User Guide* .

    :cloudformationResource: AWS::LicenseManager::License
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_licensemanager as licensemanager
        
        cfn_license = licensemanager.CfnLicense(self, "MyCfnLicense",
            consumption_configuration=licensemanager.CfnLicense.ConsumptionConfigurationProperty(
                borrow_configuration=licensemanager.CfnLicense.BorrowConfigurationProperty(
                    allow_early_check_in=False,
                    max_time_to_live_in_minutes=123
                ),
                provisional_configuration=licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                    max_time_to_live_in_minutes=123
                ),
                renew_type="renewType"
            ),
            entitlements=[licensemanager.CfnLicense.EntitlementProperty(
                name="name",
                unit="unit",
        
                # the properties below are optional
                allow_check_in=False,
                max_count=123,
                overage=False,
                value="value"
            )],
            home_region="homeRegion",
            issuer=licensemanager.CfnLicense.IssuerDataProperty(
                name="name",
        
                # the properties below are optional
                sign_key="signKey"
            ),
            license_name="licenseName",
            product_name="productName",
            validity=licensemanager.CfnLicense.ValidityDateFormatProperty(
                begin="begin",
                end="end"
            ),
        
            # the properties below are optional
            beneficiary="beneficiary",
            license_metadata=[licensemanager.CfnLicense.MetadataProperty(
                name="name",
                value="value"
            )],
            product_sku="productSku",
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        consumption_configuration: typing.Union[typing.Union["CfnLicense.ConsumptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        entitlements: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLicense.EntitlementProperty", typing.Dict[builtins.str, typing.Any]]]]],
        home_region: builtins.str,
        issuer: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLicense.IssuerDataProperty", typing.Dict[builtins.str, typing.Any]]],
        license_name: builtins.str,
        product_name: builtins.str,
        validity: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLicense.ValidityDateFormatProperty", typing.Dict[builtins.str, typing.Any]]],
        beneficiary: typing.Optional[builtins.str] = None,
        license_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLicense.MetadataProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        product_sku: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::LicenseManager::License``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param consumption_configuration: Configuration for consumption of the license.
        :param entitlements: License entitlements.
        :param home_region: Home Region of the license.
        :param issuer: License issuer.
        :param license_name: License name.
        :param product_name: Product name.
        :param validity: Date and time range during which the license is valid, in ISO8601-UTC format.
        :param beneficiary: License beneficiary.
        :param license_metadata: License metadata.
        :param product_sku: Product SKU.
        :param status: License status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b88bdc74f59e32e59c8440a67f3e0d74329501e42da1ffa5fb2b01f91056c77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLicenseProps(
            consumption_configuration=consumption_configuration,
            entitlements=entitlements,
            home_region=home_region,
            issuer=issuer,
            license_name=license_name,
            product_name=product_name,
            validity=validity,
            beneficiary=beneficiary,
            license_metadata=license_metadata,
            product_sku=product_sku,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395c038f5000766e4cb476c8e995968d9f60bebea1f4cdce7caa0fa02ad2c4a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd1910f815b7b7bead73b686e5e574898c01a762bede1740754a017bc41a72e8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLicenseArn")
    def attr_license_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the license.

        :cloudformationAttribute: LicenseArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLicenseArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The license version.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="consumptionConfiguration")
    def consumption_configuration(
        self,
    ) -> typing.Union["CfnLicense.ConsumptionConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Configuration for consumption of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-consumptionconfiguration
        '''
        return typing.cast(typing.Union["CfnLicense.ConsumptionConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "consumptionConfiguration"))

    @consumption_configuration.setter
    def consumption_configuration(
        self,
        value: typing.Union["CfnLicense.ConsumptionConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dc043447c93af0363ee62475d9b47587199d2a327f83e927dfbc0b397ee56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="entitlements")
    def entitlements(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.EntitlementProperty"]]]:
        '''License entitlements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-entitlements
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.EntitlementProperty"]]], jsii.get(self, "entitlements"))

    @entitlements.setter
    def entitlements(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.EntitlementProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489ce0c71931359ecfeb59ee81538e16e7f71a1bc4c4c76fe568a96a753f0de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlements", value)

    @builtins.property
    @jsii.member(jsii_name="homeRegion")
    def home_region(self) -> builtins.str:
        '''Home Region of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-homeregion
        '''
        return typing.cast(builtins.str, jsii.get(self, "homeRegion"))

    @home_region.setter
    def home_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3b8689d584889300693ac85f3bc0f7f484904d56dc68cc2dd650c1942afab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeRegion", value)

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.IssuerDataProperty"]:
        '''License issuer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-issuer
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.IssuerDataProperty"], jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.IssuerDataProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090e996273fd3b52f8388c4f421ead0dad89a11ed46f29e24d46eb212d39ade1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value)

    @builtins.property
    @jsii.member(jsii_name="licenseName")
    def license_name(self) -> builtins.str:
        '''License name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensename
        '''
        return typing.cast(builtins.str, jsii.get(self, "licenseName"))

    @license_name.setter
    def license_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0986bd63d619fefade90297603b78ce07847a93758fa8ec57d0fa577cdb7c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseName", value)

    @builtins.property
    @jsii.member(jsii_name="productName")
    def product_name(self) -> builtins.str:
        '''Product name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productname
        '''
        return typing.cast(builtins.str, jsii.get(self, "productName"))

    @product_name.setter
    def product_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a1c506b0e8d399a2e962a72441af6608af150244a22fd15cf5a0f34916cb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productName", value)

    @builtins.property
    @jsii.member(jsii_name="validity")
    def validity(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.ValidityDateFormatProperty"]:
        '''Date and time range during which the license is valid, in ISO8601-UTC format.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-validity
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.ValidityDateFormatProperty"], jsii.get(self, "validity"))

    @validity.setter
    def validity(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.ValidityDateFormatProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2a6e1c03afdcee98620c6698769bac0f189c3fbd060fcdfd06c99bb238fb64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validity", value)

    @builtins.property
    @jsii.member(jsii_name="beneficiary")
    def beneficiary(self) -> typing.Optional[builtins.str]:
        '''License beneficiary.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-beneficiary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beneficiary"))

    @beneficiary.setter
    def beneficiary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585635f09cc69a014d502195ecea582dfdbf2bff05df3859fd864e3105377b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beneficiary", value)

    @builtins.property
    @jsii.member(jsii_name="licenseMetadata")
    def license_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.MetadataProperty"]]]]:
        '''License metadata.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensemetadata
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.MetadataProperty"]]]], jsii.get(self, "licenseMetadata"))

    @license_metadata.setter
    def license_metadata(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.MetadataProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff44b9a5cbc5ab85f0660b1adb503a64cd8e3dca7c7a0b849feefd1f758e9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="productSku")
    def product_sku(self) -> typing.Optional[builtins.str]:
        '''Product SKU.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productsku
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productSku"))

    @product_sku.setter
    def product_sku(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52be865f49b15436bb526050ab9f8b46a3114e5ea887858e678079e1297c341e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productSku", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''License status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd3476b5198f6ec91515547b1b99e171622de9962268631345cf1742eb02a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.BorrowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_early_check_in": "allowEarlyCheckIn",
            "max_time_to_live_in_minutes": "maxTimeToLiveInMinutes",
        },
    )
    class BorrowConfigurationProperty:
        def __init__(
            self,
            *,
            allow_early_check_in: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            max_time_to_live_in_minutes: jsii.Number,
        ) -> None:
            '''Details about a borrow configuration.

            :param allow_early_check_in: Indicates whether early check-ins are allowed.
            :param max_time_to_live_in_minutes: Maximum time for the borrow configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                borrow_configuration_property = licensemanager.CfnLicense.BorrowConfigurationProperty(
                    allow_early_check_in=False,
                    max_time_to_live_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db5cae5aaba71101407c74936fcf84c6d2290754dc7dbcc16051cc13e50d87e1)
                check_type(argname="argument allow_early_check_in", value=allow_early_check_in, expected_type=type_hints["allow_early_check_in"])
                check_type(argname="argument max_time_to_live_in_minutes", value=max_time_to_live_in_minutes, expected_type=type_hints["max_time_to_live_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allow_early_check_in": allow_early_check_in,
                "max_time_to_live_in_minutes": max_time_to_live_in_minutes,
            }

        @builtins.property
        def allow_early_check_in(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Indicates whether early check-ins are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html#cfn-licensemanager-license-borrowconfiguration-allowearlycheckin
            '''
            result = self._values.get("allow_early_check_in")
            assert result is not None, "Required property 'allow_early_check_in' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def max_time_to_live_in_minutes(self) -> jsii.Number:
            '''Maximum time for the borrow configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html#cfn-licensemanager-license-borrowconfiguration-maxtimetoliveinminutes
            '''
            result = self._values.get("max_time_to_live_in_minutes")
            assert result is not None, "Required property 'max_time_to_live_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BorrowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.ConsumptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "borrow_configuration": "borrowConfiguration",
            "provisional_configuration": "provisionalConfiguration",
            "renew_type": "renewType",
        },
    )
    class ConsumptionConfigurationProperty:
        def __init__(
            self,
            *,
            borrow_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLicense.BorrowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provisional_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLicense.ProvisionalConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            renew_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about a consumption configuration.

            :param borrow_configuration: Details about a borrow configuration.
            :param provisional_configuration: Details about a provisional configuration.
            :param renew_type: Renewal frequency.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                consumption_configuration_property = licensemanager.CfnLicense.ConsumptionConfigurationProperty(
                    borrow_configuration=licensemanager.CfnLicense.BorrowConfigurationProperty(
                        allow_early_check_in=False,
                        max_time_to_live_in_minutes=123
                    ),
                    provisional_configuration=licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                        max_time_to_live_in_minutes=123
                    ),
                    renew_type="renewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a1b4d585af775482850ac1ad8c620f441ef193d12e96ccb05a90e7591ee4e68)
                check_type(argname="argument borrow_configuration", value=borrow_configuration, expected_type=type_hints["borrow_configuration"])
                check_type(argname="argument provisional_configuration", value=provisional_configuration, expected_type=type_hints["provisional_configuration"])
                check_type(argname="argument renew_type", value=renew_type, expected_type=type_hints["renew_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if borrow_configuration is not None:
                self._values["borrow_configuration"] = borrow_configuration
            if provisional_configuration is not None:
                self._values["provisional_configuration"] = provisional_configuration
            if renew_type is not None:
                self._values["renew_type"] = renew_type

        @builtins.property
        def borrow_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.BorrowConfigurationProperty"]]:
            '''Details about a borrow configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-borrowconfiguration
            '''
            result = self._values.get("borrow_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.BorrowConfigurationProperty"]], result)

        @builtins.property
        def provisional_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.ProvisionalConfigurationProperty"]]:
            '''Details about a provisional configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-provisionalconfiguration
            '''
            result = self._values.get("provisional_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLicense.ProvisionalConfigurationProperty"]], result)

        @builtins.property
        def renew_type(self) -> typing.Optional[builtins.str]:
            '''Renewal frequency.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-renewtype
            '''
            result = self._values.get("renew_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsumptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.EntitlementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "unit": "unit",
            "allow_check_in": "allowCheckIn",
            "max_count": "maxCount",
            "overage": "overage",
            "value": "value",
        },
    )
    class EntitlementProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            unit: builtins.str,
            allow_check_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            max_count: typing.Optional[jsii.Number] = None,
            overage: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a resource entitled for use with a license.

            :param name: Entitlement name.
            :param unit: Entitlement unit.
            :param allow_check_in: Indicates whether check-ins are allowed.
            :param max_count: Maximum entitlement count. Use if the unit is not None.
            :param overage: Indicates whether overages are allowed.
            :param value: Entitlement resource. Use only if the unit is None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                entitlement_property = licensemanager.CfnLicense.EntitlementProperty(
                    name="name",
                    unit="unit",
                
                    # the properties below are optional
                    allow_check_in=False,
                    max_count=123,
                    overage=False,
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b06e0adb829d29ec71b5bb5af36c1b0d39bffcafa7f0b6db6b555045306cde3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument allow_check_in", value=allow_check_in, expected_type=type_hints["allow_check_in"])
                check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
                check_type(argname="argument overage", value=overage, expected_type=type_hints["overage"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "unit": unit,
            }
            if allow_check_in is not None:
                self._values["allow_check_in"] = allow_check_in
            if max_count is not None:
                self._values["max_count"] = max_count
            if overage is not None:
                self._values["overage"] = overage
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> builtins.str:
            '''Entitlement name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unit(self) -> builtins.str:
            '''Entitlement unit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-unit
            '''
            result = self._values.get("unit")
            assert result is not None, "Required property 'unit' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allow_check_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether check-ins are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-allowcheckin
            '''
            result = self._values.get("allow_check_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def max_count(self) -> typing.Optional[jsii.Number]:
            '''Maximum entitlement count.

            Use if the unit is not None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-maxcount
            '''
            result = self._values.get("max_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def overage(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether overages are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-overage
            '''
            result = self._values.get("overage")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Entitlement resource.

            Use only if the unit is None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntitlementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.IssuerDataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sign_key": "signKey"},
    )
    class IssuerDataProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sign_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details associated with the issuer of a license.

            :param name: Issuer name.
            :param sign_key: Asymmetric KMS key from AWS Key Management Service . The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                issuer_data_property = licensemanager.CfnLicense.IssuerDataProperty(
                    name="name",
                
                    # the properties below are optional
                    sign_key="signKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27db99fed442999ceeaee35f3047b98e17323bd6ee7f2c748d4324c7b4afbf71)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sign_key", value=sign_key, expected_type=type_hints["sign_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if sign_key is not None:
                self._values["sign_key"] = sign_key

        @builtins.property
        def name(self) -> builtins.str:
            '''Issuer name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html#cfn-licensemanager-license-issuerdata-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sign_key(self) -> typing.Optional[builtins.str]:
            '''Asymmetric KMS key from AWS Key Management Service .

            The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html#cfn-licensemanager-license-issuerdata-signkey
            '''
            result = self._values.get("sign_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IssuerDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.MetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class MetadataProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''Describes key/value pairs.

            :param name: The key name.
            :param value: The value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                metadata_property = licensemanager.CfnLicense.MetadataProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50638ff1ff1fa3831b58015fb707bb0ca22ec555a8fc6c20ef6da3135205e5ea)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The key name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html#cfn-licensemanager-license-metadata-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html#cfn-licensemanager-license-metadata-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.ProvisionalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_time_to_live_in_minutes": "maxTimeToLiveInMinutes"},
    )
    class ProvisionalConfigurationProperty:
        def __init__(self, *, max_time_to_live_in_minutes: jsii.Number) -> None:
            '''Details about a provisional configuration.

            :param max_time_to_live_in_minutes: Maximum time for the provisional configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-provisionalconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                provisional_configuration_property = licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                    max_time_to_live_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c676fa2be3d69ae46fd6020b7a6550e2a7895c6bdba2e8a8dbafeeb82a484b40)
                check_type(argname="argument max_time_to_live_in_minutes", value=max_time_to_live_in_minutes, expected_type=type_hints["max_time_to_live_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "max_time_to_live_in_minutes": max_time_to_live_in_minutes,
            }

        @builtins.property
        def max_time_to_live_in_minutes(self) -> jsii.Number:
            '''Maximum time for the provisional configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-provisionalconfiguration.html#cfn-licensemanager-license-provisionalconfiguration-maxtimetoliveinminutes
            '''
            result = self._values.get("max_time_to_live_in_minutes")
            assert result is not None, "Required property 'max_time_to_live_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-licensemanager.CfnLicense.ValidityDateFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"begin": "begin", "end": "end"},
    )
    class ValidityDateFormatProperty:
        def __init__(self, *, begin: builtins.str, end: builtins.str) -> None:
            '''Date and time range during which the license is valid, in ISO8601-UTC format.

            :param begin: Start of the time range.
            :param end: End of the time range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_licensemanager as licensemanager
                
                validity_date_format_property = licensemanager.CfnLicense.ValidityDateFormatProperty(
                    begin="begin",
                    end="end"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6acf1c6ab58993f900aad21e8a59f24dfb4665955d58fbcaa7d58c8173c946f)
                check_type(argname="argument begin", value=begin, expected_type=type_hints["begin"])
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "begin": begin,
                "end": end,
            }

        @builtins.property
        def begin(self) -> builtins.str:
            '''Start of the time range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html#cfn-licensemanager-license-validitydateformat-begin
            '''
            result = self._values.get("begin")
            assert result is not None, "Required property 'begin' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def end(self) -> builtins.str:
            '''End of the time range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html#cfn-licensemanager-license-validitydateformat-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityDateFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-licensemanager.CfnLicenseProps",
    jsii_struct_bases=[],
    name_mapping={
        "consumption_configuration": "consumptionConfiguration",
        "entitlements": "entitlements",
        "home_region": "homeRegion",
        "issuer": "issuer",
        "license_name": "licenseName",
        "product_name": "productName",
        "validity": "validity",
        "beneficiary": "beneficiary",
        "license_metadata": "licenseMetadata",
        "product_sku": "productSku",
        "status": "status",
    },
)
class CfnLicenseProps:
    def __init__(
        self,
        *,
        consumption_configuration: typing.Union[typing.Union[CfnLicense.ConsumptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        entitlements: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.EntitlementProperty, typing.Dict[builtins.str, typing.Any]]]]],
        home_region: builtins.str,
        issuer: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.IssuerDataProperty, typing.Dict[builtins.str, typing.Any]]],
        license_name: builtins.str,
        product_name: builtins.str,
        validity: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.ValidityDateFormatProperty, typing.Dict[builtins.str, typing.Any]]],
        beneficiary: typing.Optional[builtins.str] = None,
        license_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.MetadataProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        product_sku: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLicense``.

        :param consumption_configuration: Configuration for consumption of the license.
        :param entitlements: License entitlements.
        :param home_region: Home Region of the license.
        :param issuer: License issuer.
        :param license_name: License name.
        :param product_name: Product name.
        :param validity: Date and time range during which the license is valid, in ISO8601-UTC format.
        :param beneficiary: License beneficiary.
        :param license_metadata: License metadata.
        :param product_sku: Product SKU.
        :param status: License status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_licensemanager as licensemanager
            
            cfn_license_props = licensemanager.CfnLicenseProps(
                consumption_configuration=licensemanager.CfnLicense.ConsumptionConfigurationProperty(
                    borrow_configuration=licensemanager.CfnLicense.BorrowConfigurationProperty(
                        allow_early_check_in=False,
                        max_time_to_live_in_minutes=123
                    ),
                    provisional_configuration=licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                        max_time_to_live_in_minutes=123
                    ),
                    renew_type="renewType"
                ),
                entitlements=[licensemanager.CfnLicense.EntitlementProperty(
                    name="name",
                    unit="unit",
            
                    # the properties below are optional
                    allow_check_in=False,
                    max_count=123,
                    overage=False,
                    value="value"
                )],
                home_region="homeRegion",
                issuer=licensemanager.CfnLicense.IssuerDataProperty(
                    name="name",
            
                    # the properties below are optional
                    sign_key="signKey"
                ),
                license_name="licenseName",
                product_name="productName",
                validity=licensemanager.CfnLicense.ValidityDateFormatProperty(
                    begin="begin",
                    end="end"
                ),
            
                # the properties below are optional
                beneficiary="beneficiary",
                license_metadata=[licensemanager.CfnLicense.MetadataProperty(
                    name="name",
                    value="value"
                )],
                product_sku="productSku",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87992c3b41e1de94c3ad6dcda8a6a2368e3ce55fcacea1ac6543511bf4a90139)
            check_type(argname="argument consumption_configuration", value=consumption_configuration, expected_type=type_hints["consumption_configuration"])
            check_type(argname="argument entitlements", value=entitlements, expected_type=type_hints["entitlements"])
            check_type(argname="argument home_region", value=home_region, expected_type=type_hints["home_region"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument license_name", value=license_name, expected_type=type_hints["license_name"])
            check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
            check_type(argname="argument validity", value=validity, expected_type=type_hints["validity"])
            check_type(argname="argument beneficiary", value=beneficiary, expected_type=type_hints["beneficiary"])
            check_type(argname="argument license_metadata", value=license_metadata, expected_type=type_hints["license_metadata"])
            check_type(argname="argument product_sku", value=product_sku, expected_type=type_hints["product_sku"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumption_configuration": consumption_configuration,
            "entitlements": entitlements,
            "home_region": home_region,
            "issuer": issuer,
            "license_name": license_name,
            "product_name": product_name,
            "validity": validity,
        }
        if beneficiary is not None:
            self._values["beneficiary"] = beneficiary
        if license_metadata is not None:
            self._values["license_metadata"] = license_metadata
        if product_sku is not None:
            self._values["product_sku"] = product_sku
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def consumption_configuration(
        self,
    ) -> typing.Union[CfnLicense.ConsumptionConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Configuration for consumption of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-consumptionconfiguration
        '''
        result = self._values.get("consumption_configuration")
        assert result is not None, "Required property 'consumption_configuration' is missing"
        return typing.cast(typing.Union[CfnLicense.ConsumptionConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def entitlements(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.EntitlementProperty]]]:
        '''License entitlements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-entitlements
        '''
        result = self._values.get("entitlements")
        assert result is not None, "Required property 'entitlements' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.EntitlementProperty]]], result)

    @builtins.property
    def home_region(self) -> builtins.str:
        '''Home Region of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-homeregion
        '''
        result = self._values.get("home_region")
        assert result is not None, "Required property 'home_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.IssuerDataProperty]:
        '''License issuer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-issuer
        '''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.IssuerDataProperty], result)

    @builtins.property
    def license_name(self) -> builtins.str:
        '''License name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensename
        '''
        result = self._values.get("license_name")
        assert result is not None, "Required property 'license_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_name(self) -> builtins.str:
        '''Product name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productname
        '''
        result = self._values.get("product_name")
        assert result is not None, "Required property 'product_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validity(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.ValidityDateFormatProperty]:
        '''Date and time range during which the license is valid, in ISO8601-UTC format.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-validity
        '''
        result = self._values.get("validity")
        assert result is not None, "Required property 'validity' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.ValidityDateFormatProperty], result)

    @builtins.property
    def beneficiary(self) -> typing.Optional[builtins.str]:
        '''License beneficiary.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-beneficiary
        '''
        result = self._values.get("beneficiary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.MetadataProperty]]]]:
        '''License metadata.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensemetadata
        '''
        result = self._values.get("license_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.MetadataProperty]]]], result)

    @builtins.property
    def product_sku(self) -> typing.Optional[builtins.str]:
        '''Product SKU.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productsku
        '''
        result = self._values.get("product_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''License status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLicenseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGrant",
    "CfnGrantProps",
    "CfnLicense",
    "CfnLicenseProps",
]

publication.publish()

def _typecheckingstub__1cfb01eaf2e60f6d86118f6a67a9ca1f909c856f4a1df234e7cf60cc3bc4f052(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    grant_name: typing.Optional[builtins.str] = None,
    home_region: typing.Optional[builtins.str] = None,
    license_arn: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d58eca7fd6f15ce9ba5f9055106a7cd57d8b5e73bc36f6eb0b0cd73a66ec494(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abc50cebfd23c96cdca11ee7bad500dcd66654bf98fc8a4b5d8fe4f4f1257b6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42210aafe4071d70a83c3ad694f6cbcff6d70522b6bcf275fc8231999c3e51bf(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44355f69624bc48c1a72c3f00697478fdbe47d01b17e493c3f7715228b0f365c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bec4e32bebad96d2ef2463640c6f6d6c9c3bb1379a497f894958e14241e90e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d83a85f53c039c1c928847a68f495615a89f6d5c1c822456896d0f7222a9a6d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569a23d2525cef8226d581b3db0346e2fbb0813cde187cb4ca2a0b5d043626ff(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c6a9c98a59d425b901a56da731f79bc37e50909631583fd71be399d7f7eb33(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02b4d210550141f89c9976c05eb7dd0f48f2865927adc5d82c2d594e60d2124(
    *,
    allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    grant_name: typing.Optional[builtins.str] = None,
    home_region: typing.Optional[builtins.str] = None,
    license_arn: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b88bdc74f59e32e59c8440a67f3e0d74329501e42da1ffa5fb2b01f91056c77(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    consumption_configuration: typing.Union[typing.Union[CfnLicense.ConsumptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    entitlements: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.EntitlementProperty, typing.Dict[builtins.str, typing.Any]]]]],
    home_region: builtins.str,
    issuer: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.IssuerDataProperty, typing.Dict[builtins.str, typing.Any]]],
    license_name: builtins.str,
    product_name: builtins.str,
    validity: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.ValidityDateFormatProperty, typing.Dict[builtins.str, typing.Any]]],
    beneficiary: typing.Optional[builtins.str] = None,
    license_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.MetadataProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_sku: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395c038f5000766e4cb476c8e995968d9f60bebea1f4cdce7caa0fa02ad2c4a0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1910f815b7b7bead73b686e5e574898c01a762bede1740754a017bc41a72e8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dc043447c93af0363ee62475d9b47587199d2a327f83e927dfbc0b397ee56f(
    value: typing.Union[CfnLicense.ConsumptionConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489ce0c71931359ecfeb59ee81538e16e7f71a1bc4c4c76fe568a96a753f0de0(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.EntitlementProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3b8689d584889300693ac85f3bc0f7f484904d56dc68cc2dd650c1942afab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090e996273fd3b52f8388c4f421ead0dad89a11ed46f29e24d46eb212d39ade1(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.IssuerDataProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0986bd63d619fefade90297603b78ce07847a93758fa8ec57d0fa577cdb7c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a1c506b0e8d399a2e962a72441af6608af150244a22fd15cf5a0f34916cb74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2a6e1c03afdcee98620c6698769bac0f189c3fbd060fcdfd06c99bb238fb64(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.ValidityDateFormatProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585635f09cc69a014d502195ecea582dfdbf2bff05df3859fd864e3105377b1c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff44b9a5cbc5ab85f0660b1adb503a64cd8e3dca7c7a0b849feefd1f758e9f9(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLicense.MetadataProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52be865f49b15436bb526050ab9f8b46a3114e5ea887858e678079e1297c341e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd3476b5198f6ec91515547b1b99e171622de9962268631345cf1742eb02a2a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5cae5aaba71101407c74936fcf84c6d2290754dc7dbcc16051cc13e50d87e1(
    *,
    allow_early_check_in: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    max_time_to_live_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1b4d585af775482850ac1ad8c620f441ef193d12e96ccb05a90e7591ee4e68(
    *,
    borrow_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.BorrowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisional_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.ProvisionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    renew_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b06e0adb829d29ec71b5bb5af36c1b0d39bffcafa7f0b6db6b555045306cde3(
    *,
    name: builtins.str,
    unit: builtins.str,
    allow_check_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    overage: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27db99fed442999ceeaee35f3047b98e17323bd6ee7f2c748d4324c7b4afbf71(
    *,
    name: builtins.str,
    sign_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50638ff1ff1fa3831b58015fb707bb0ca22ec555a8fc6c20ef6da3135205e5ea(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c676fa2be3d69ae46fd6020b7a6550e2a7895c6bdba2e8a8dbafeeb82a484b40(
    *,
    max_time_to_live_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6acf1c6ab58993f900aad21e8a59f24dfb4665955d58fbcaa7d58c8173c946f(
    *,
    begin: builtins.str,
    end: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87992c3b41e1de94c3ad6dcda8a6a2368e3ce55fcacea1ac6543511bf4a90139(
    *,
    consumption_configuration: typing.Union[typing.Union[CfnLicense.ConsumptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    entitlements: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.EntitlementProperty, typing.Dict[builtins.str, typing.Any]]]]],
    home_region: builtins.str,
    issuer: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.IssuerDataProperty, typing.Dict[builtins.str, typing.Any]]],
    license_name: builtins.str,
    product_name: builtins.str,
    validity: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.ValidityDateFormatProperty, typing.Dict[builtins.str, typing.Any]]],
    beneficiary: typing.Optional[builtins.str] = None,
    license_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLicense.MetadataProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_sku: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
