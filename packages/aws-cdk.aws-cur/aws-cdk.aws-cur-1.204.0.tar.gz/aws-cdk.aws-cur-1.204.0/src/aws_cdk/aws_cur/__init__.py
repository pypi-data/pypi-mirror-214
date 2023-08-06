'''
# AWS::CUR Construct Library

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
import aws_cdk.aws_cur as cur
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for CUR construct libraries](https://constructs.dev/search?q=cur)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::CUR resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CUR.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::CUR](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CUR.html).

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
class CfnReportDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cur.CfnReportDefinition",
):
    '''A CloudFormation ``AWS::CUR::ReportDefinition``.

    The definition of AWS Cost and Usage Report. You can specify the report name, time unit, report format, compression format, S3 bucket, additional artifacts, and schema elements in the definition.

    :cloudformationResource: AWS::CUR::ReportDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cur as cur
        
        cfn_report_definition = cur.CfnReportDefinition(self, "MyCfnReportDefinition",
            compression="compression",
            format="format",
            refresh_closed_reports=False,
            report_name="reportName",
            report_versioning="reportVersioning",
            s3_bucket="s3Bucket",
            s3_prefix="s3Prefix",
            s3_region="s3Region",
            time_unit="timeUnit",
        
            # the properties below are optional
            additional_artifacts=["additionalArtifacts"],
            additional_schema_elements=["additionalSchemaElements"],
            billing_view_arn="billingViewArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        compression: builtins.str,
        format: builtins.str,
        refresh_closed_reports: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        report_name: builtins.str,
        report_versioning: builtins.str,
        s3_bucket: builtins.str,
        s3_prefix: builtins.str,
        s3_region: builtins.str,
        time_unit: builtins.str,
        additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        billing_view_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CUR::ReportDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compression: The compression format that Amazon Web Services uses for the report.
        :param format: The format that Amazon Web Services saves the report in.
        :param refresh_closed_reports: Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months. These charges can include refunds, credits, or support fees.
        :param report_name: The name of the report that you want to create. The name must be unique, is case sensitive, and can't include spaces.
        :param report_versioning: Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.
        :param s3_bucket: The S3 bucket where Amazon Web Services delivers the report.
        :param s3_prefix: The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report. Your prefix can't include spaces.
        :param s3_region: The Region of the S3 bucket that Amazon Web Services delivers the report into.
        :param time_unit: The granularity of the line items in the report.
        :param additional_artifacts: A list of manifests that you want AWS to create for this report.
        :param additional_schema_elements: A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.
        :param billing_view_arn: The Amazon Resource Name (ARN) of the billing view. You can get this value by using the billing view service public APIs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d438be52ef2afb5d01e364cc11bf0d3a2e39ff0c18db965719238da27caa5cd1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReportDefinitionProps(
            compression=compression,
            format=format,
            refresh_closed_reports=refresh_closed_reports,
            report_name=report_name,
            report_versioning=report_versioning,
            s3_bucket=s3_bucket,
            s3_prefix=s3_prefix,
            s3_region=s3_region,
            time_unit=time_unit,
            additional_artifacts=additional_artifacts,
            additional_schema_elements=additional_schema_elements,
            billing_view_arn=billing_view_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bba85d53adce769b8337531c0d8bd0b5581778ef67ecb990825ef6022e2ac3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0d1c9dfc18feca9c01d4291c62ca5a9622aab079f4b961be2e4327a6d200170)
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
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        '''The compression format that Amazon Web Services uses for the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-compression
        '''
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495a9560021a0a9848881193942173d692566665a44d92ac681357fcd17285c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        '''The format that Amazon Web Services saves the report in.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-format
        '''
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b543aaa514a8c283aca03ba7d9df1cb49671f32af0ccf14c1873be5981301aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value)

    @builtins.property
    @jsii.member(jsii_name="refreshClosedReports")
    def refresh_closed_reports(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months.

        These charges can include refunds, credits, or support fees.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-refreshclosedreports
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "refreshClosedReports"))

    @refresh_closed_reports.setter
    def refresh_closed_reports(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9294672489cbafe2a370201989f028ec224ee3df9c8e4f487e2fb8e81ddac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshClosedReports", value)

    @builtins.property
    @jsii.member(jsii_name="reportName")
    def report_name(self) -> builtins.str:
        '''The name of the report that you want to create.

        The name must be unique, is case sensitive, and can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportname
        '''
        return typing.cast(builtins.str, jsii.get(self, "reportName"))

    @report_name.setter
    def report_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bae6b928a43eb0128b16c25dd105b086e4054c054c960d60f4c5a34fb2a49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportName", value)

    @builtins.property
    @jsii.member(jsii_name="reportVersioning")
    def report_versioning(self) -> builtins.str:
        '''Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportversioning
        '''
        return typing.cast(builtins.str, jsii.get(self, "reportVersioning"))

    @report_versioning.setter
    def report_versioning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e4f286994402bdf6dae5fcabb493cdea0f37064fadb7e585eba1675aa67d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportVersioning", value)

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        '''The S3 bucket where Amazon Web Services delivers the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eefc83518fbcefaa38f76b6d026f7d754d09d46cd458cc72ce24eef82bbb64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        '''The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report.

        Your prefix can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3prefix
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @s3_prefix.setter
    def s3_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bde87bdb568b28154e738a2595565f2b070f674ce0ba4f874a8297d58cdbf13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Prefix", value)

    @builtins.property
    @jsii.member(jsii_name="s3Region")
    def s3_region(self) -> builtins.str:
        '''The Region of the S3 bucket that Amazon Web Services delivers the report into.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3region
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Region"))

    @s3_region.setter
    def s3_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae5cdad9c7f5decdb616e90eb5eb564dcc3db929e03719f0939bf4f7b8f3348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Region", value)

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        '''The granularity of the line items in the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-timeunit
        '''
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572d31177b5f35aa1678fe16f0759c477e44e1096353339877ac2859bfef8624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value)

    @builtins.property
    @jsii.member(jsii_name="additionalArtifacts")
    def additional_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of manifests that you want AWS to create for this report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalartifacts
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalArtifacts"))

    @additional_artifacts.setter
    def additional_artifacts(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3019cd52da8c2864400d91b0a1e47ba9d3de53a8c80cbe275fc0e5f9cd31261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalArtifacts", value)

    @builtins.property
    @jsii.member(jsii_name="additionalSchemaElements")
    def additional_schema_elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalschemaelements
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalSchemaElements"))

    @additional_schema_elements.setter
    def additional_schema_elements(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cea080f379fcc2568c52a1eba067f4eed5008ade57044ffba689b570f11b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalSchemaElements", value)

    @builtins.property
    @jsii.member(jsii_name="billingViewArn")
    def billing_view_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the billing view.

        You can get this value by using the billing view service public APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-billingviewarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingViewArn"))

    @billing_view_arn.setter
    def billing_view_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bc733ca097db369f3275afeae9ef82bbb9fb8af473ba3f9d902b0a24f15e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingViewArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cur.CfnReportDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "compression": "compression",
        "format": "format",
        "refresh_closed_reports": "refreshClosedReports",
        "report_name": "reportName",
        "report_versioning": "reportVersioning",
        "s3_bucket": "s3Bucket",
        "s3_prefix": "s3Prefix",
        "s3_region": "s3Region",
        "time_unit": "timeUnit",
        "additional_artifacts": "additionalArtifacts",
        "additional_schema_elements": "additionalSchemaElements",
        "billing_view_arn": "billingViewArn",
    },
)
class CfnReportDefinitionProps:
    def __init__(
        self,
        *,
        compression: builtins.str,
        format: builtins.str,
        refresh_closed_reports: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        report_name: builtins.str,
        report_versioning: builtins.str,
        s3_bucket: builtins.str,
        s3_prefix: builtins.str,
        s3_region: builtins.str,
        time_unit: builtins.str,
        additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        billing_view_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnReportDefinition``.

        :param compression: The compression format that Amazon Web Services uses for the report.
        :param format: The format that Amazon Web Services saves the report in.
        :param refresh_closed_reports: Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months. These charges can include refunds, credits, or support fees.
        :param report_name: The name of the report that you want to create. The name must be unique, is case sensitive, and can't include spaces.
        :param report_versioning: Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.
        :param s3_bucket: The S3 bucket where Amazon Web Services delivers the report.
        :param s3_prefix: The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report. Your prefix can't include spaces.
        :param s3_region: The Region of the S3 bucket that Amazon Web Services delivers the report into.
        :param time_unit: The granularity of the line items in the report.
        :param additional_artifacts: A list of manifests that you want AWS to create for this report.
        :param additional_schema_elements: A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.
        :param billing_view_arn: The Amazon Resource Name (ARN) of the billing view. You can get this value by using the billing view service public APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cur as cur
            
            cfn_report_definition_props = cur.CfnReportDefinitionProps(
                compression="compression",
                format="format",
                refresh_closed_reports=False,
                report_name="reportName",
                report_versioning="reportVersioning",
                s3_bucket="s3Bucket",
                s3_prefix="s3Prefix",
                s3_region="s3Region",
                time_unit="timeUnit",
            
                # the properties below are optional
                additional_artifacts=["additionalArtifacts"],
                additional_schema_elements=["additionalSchemaElements"],
                billing_view_arn="billingViewArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ca96be9380cb967299cb09e7b33042f0afde208ea4e7cb0f1fbb28cde0fe52)
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument refresh_closed_reports", value=refresh_closed_reports, expected_type=type_hints["refresh_closed_reports"])
            check_type(argname="argument report_name", value=report_name, expected_type=type_hints["report_name"])
            check_type(argname="argument report_versioning", value=report_versioning, expected_type=type_hints["report_versioning"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            check_type(argname="argument s3_region", value=s3_region, expected_type=type_hints["s3_region"])
            check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument additional_schema_elements", value=additional_schema_elements, expected_type=type_hints["additional_schema_elements"])
            check_type(argname="argument billing_view_arn", value=billing_view_arn, expected_type=type_hints["billing_view_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression": compression,
            "format": format,
            "refresh_closed_reports": refresh_closed_reports,
            "report_name": report_name,
            "report_versioning": report_versioning,
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "s3_region": s3_region,
            "time_unit": time_unit,
        }
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if additional_schema_elements is not None:
            self._values["additional_schema_elements"] = additional_schema_elements
        if billing_view_arn is not None:
            self._values["billing_view_arn"] = billing_view_arn

    @builtins.property
    def compression(self) -> builtins.str:
        '''The compression format that Amazon Web Services uses for the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-compression
        '''
        result = self._values.get("compression")
        assert result is not None, "Required property 'compression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''The format that Amazon Web Services saves the report in.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-format
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def refresh_closed_reports(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months.

        These charges can include refunds, credits, or support fees.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-refreshclosedreports
        '''
        result = self._values.get("refresh_closed_reports")
        assert result is not None, "Required property 'refresh_closed_reports' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def report_name(self) -> builtins.str:
        '''The name of the report that you want to create.

        The name must be unique, is case sensitive, and can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportname
        '''
        result = self._values.get("report_name")
        assert result is not None, "Required property 'report_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def report_versioning(self) -> builtins.str:
        '''Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportversioning
        '''
        result = self._values.get("report_versioning")
        assert result is not None, "Required property 'report_versioning' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''The S3 bucket where Amazon Web Services delivers the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3bucket
        '''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_prefix(self) -> builtins.str:
        '''The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report.

        Your prefix can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3prefix
        '''
        result = self._values.get("s3_prefix")
        assert result is not None, "Required property 's3_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_region(self) -> builtins.str:
        '''The Region of the S3 bucket that Amazon Web Services delivers the report into.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3region
        '''
        result = self._values.get("s3_region")
        assert result is not None, "Required property 's3_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_unit(self) -> builtins.str:
        '''The granularity of the line items in the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-timeunit
        '''
        result = self._values.get("time_unit")
        assert result is not None, "Required property 'time_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of manifests that you want AWS to create for this report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalartifacts
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def additional_schema_elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalschemaelements
        '''
        result = self._values.get("additional_schema_elements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def billing_view_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the billing view.

        You can get this value by using the billing view service public APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-billingviewarn
        '''
        result = self._values.get("billing_view_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnReportDefinition",
    "CfnReportDefinitionProps",
]

publication.publish()

def _typecheckingstub__d438be52ef2afb5d01e364cc11bf0d3a2e39ff0c18db965719238da27caa5cd1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    compression: builtins.str,
    format: builtins.str,
    refresh_closed_reports: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    report_name: builtins.str,
    report_versioning: builtins.str,
    s3_bucket: builtins.str,
    s3_prefix: builtins.str,
    s3_region: builtins.str,
    time_unit: builtins.str,
    additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bba85d53adce769b8337531c0d8bd0b5581778ef67ecb990825ef6022e2ac3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d1c9dfc18feca9c01d4291c62ca5a9622aab079f4b961be2e4327a6d200170(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495a9560021a0a9848881193942173d692566665a44d92ac681357fcd17285c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b543aaa514a8c283aca03ba7d9df1cb49671f32af0ccf14c1873be5981301aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9294672489cbafe2a370201989f028ec224ee3df9c8e4f487e2fb8e81ddac0(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bae6b928a43eb0128b16c25dd105b086e4054c054c960d60f4c5a34fb2a49f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e4f286994402bdf6dae5fcabb493cdea0f37064fadb7e585eba1675aa67d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eefc83518fbcefaa38f76b6d026f7d754d09d46cd458cc72ce24eef82bbb64f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bde87bdb568b28154e738a2595565f2b070f674ce0ba4f874a8297d58cdbf13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae5cdad9c7f5decdb616e90eb5eb564dcc3db929e03719f0939bf4f7b8f3348(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572d31177b5f35aa1678fe16f0759c477e44e1096353339877ac2859bfef8624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3019cd52da8c2864400d91b0a1e47ba9d3de53a8c80cbe275fc0e5f9cd31261(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cea080f379fcc2568c52a1eba067f4eed5008ade57044ffba689b570f11b7c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bc733ca097db369f3275afeae9ef82bbb9fb8af473ba3f9d902b0a24f15e35(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ca96be9380cb967299cb09e7b33042f0afde208ea4e7cb0f1fbb28cde0fe52(
    *,
    compression: builtins.str,
    format: builtins.str,
    refresh_closed_reports: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    report_name: builtins.str,
    report_versioning: builtins.str,
    s3_bucket: builtins.str,
    s3_prefix: builtins.str,
    s3_region: builtins.str,
    time_unit: builtins.str,
    additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
