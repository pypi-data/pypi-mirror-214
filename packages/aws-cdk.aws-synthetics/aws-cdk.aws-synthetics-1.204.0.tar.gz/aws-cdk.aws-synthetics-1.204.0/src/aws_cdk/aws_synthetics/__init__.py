'''
# Amazon CloudWatch Synthetics Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

Amazon CloudWatch Synthetics allow you to monitor your application by generating **synthetic** traffic. The traffic is produced by a **canary**: a configurable script that runs on a schedule. You configure the canary script to follow the same routes and perform the same actions as a user, which allows you to continually verify your user experience even when you don't have any traffic on your applications.

## Canary

To illustrate how to use a canary, assume your application defines the following endpoint:

```console
% curl "https://api.example.com/user/books/topbook/"
The Hitchhikers Guide to the Galaxy

```

The below code defines a canary that will hit the `books/topbook` endpoint every 5 minutes:

```python
canary = synthetics.Canary(self, "MyCanary",
    schedule=synthetics.Schedule.rate(Duration.minutes(5)),
    test=synthetics.Test.custom(
        code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
    environment_variables={
        "stage": "prod"
    }
)
```

The following is an example of an `index.js` file which exports the `handler` function:

```js
const synthetics = require('Synthetics');
const log = require('SyntheticsLogger');

const pageLoadBlueprint = async function () {
  // Configure the stage of the API using environment variables
  const url = `https://api.example.com/${process.env.stage}/user/books/topbook/`;

  const page = await synthetics.getPage();
  const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  // Wait for page to render. Increase or decrease wait time based on endpoint being monitored.
  await page.waitFor(15000);
  // This will take a screenshot that will be included in test output artifacts.
  await synthetics.takeScreenshot('loaded', 'loaded');
  const pageTitle = await page.title();
  log.info('Page title: ' + pageTitle);
  if (response.status() !== 200) {
    throw 'Failed to load page!';
  }
};

exports.handler = async () => {
  return await pageLoadBlueprint();
};
```

> **Note:** The function **must** be called `handler`.

The canary will automatically produce a CloudWatch Dashboard:

![UI Screenshot](images/ui-screenshot.png)

The Canary code will be executed in a lambda function created by Synthetics on your behalf. The Lambda function includes a custom [runtime](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html) provided by Synthetics. The provided runtime includes a variety of handy tools such as [Puppeteer](https://www.npmjs.com/package/puppeteer-core) (for nodejs based one) and Chromium.

To learn more about Synthetics capabilities, check out the [docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html).

### Canary Schedule

You can specify the schedule on which a canary runs by providing a
[`Schedule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-synthetics.Schedule.html)
object to the `schedule` property.

Configure a run rate of up to 60 minutes with `Schedule.rate`:

```python
schedule = synthetics.Schedule.rate(Duration.minutes(5))
```

You can also specify a [cron expression](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_cron.html) with `Schedule.cron`:

```python
schedule = synthetics.Schedule.cron(
    hour="0,8,16"
)
```

If you want the canary to run just once upon deployment, you can use `Schedule.once()`.

### Configuring the Canary Script

To configure the script the canary executes, use the `test` property. The `test` property accepts a `Test` instance that can be initialized by the `Test` class static methods. Currently, the only implemented method is `Test.custom()`, which allows you to bring your own code. In the future, other methods will be added. `Test.custom()` accepts `code` and `handler` properties -- both are required by Synthetics to create a lambda function on your behalf.

The `synthetics.Code` class exposes static methods to bundle your code artifacts:

* `code.fromInline(code)` - specify an inline script.
* `code.fromAsset(path)` - specify a .zip file or a directory in the local filesystem which will be zipped and uploaded to S3 on deployment. See the above Note for directory structure.
* `code.fromBucket(bucket, key[, objectVersion])` - specify an S3 object that contains the .zip file of your runtime code. See the above Note for directory structure.

Using the `Code` class static initializers:

```python
# To supply the code from a S3 bucket:
import aws_cdk.aws_s3 as s3
# To supply the code inline:
synthetics.Canary(self, "Inline Canary",
    test=synthetics.Test.custom(
        code=synthetics.Code.from_inline("/* Synthetics handler code */"),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_4
)

# To supply the code from your local filesystem:
synthetics.Canary(self, "Asset Canary",
    test=synthetics.Test.custom(
        code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_4
)
bucket = s3.Bucket(self, "Code Bucket")
synthetics.Canary(self, "Bucket Canary",
    test=synthetics.Test.custom(
        code=synthetics.Code.from_bucket(bucket, "canary.zip"),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_4
)
```

> **Note:** Synthetics have a specified folder structure for canaries. For Node scripts supplied via `code.fromAsset()` or `code.fromBucket()`, the canary resource requires the following folder structure:
>
> ```plaintext
> canary/
> ├── nodejs/
>    ├── node_modules/
>         ├── <filename>.js
> ```
>
> For Python scripts supplied via `code.fromAsset()` or `code.fromBucket()`, the canary resource requires the following folder structure:
>
> ```plaintext
> canary/
> ├── python/
>     ├── <filename>.py
> ```
>
> See Synthetics [docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html).

### Running a canary on a VPC

You can specify what [VPC a canary executes in](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html).
This can allow for monitoring services that may be internal to a specific VPC. To place a canary within a VPC, you can specify the `vpc` property with the desired `VPC` to place then canary in.
This will automatically attach the appropriate IAM permissions to attach to the VPC. This will also create a Security Group and attach to the default subnets for the VPC unless specified via `vpcSubnets` and `securityGroups`.

```python
import aws_cdk.aws_ec2 as ec2

# vpc: ec2.IVpc

synthetics.Canary(self, "Vpc Canary",
    test=synthetics.Test.custom(
        code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_4,
    vpc=vpc
)
```

> **Note:** By default, the Synthetics runtime needs access to the S3 and CloudWatch APIs, which will fail in a private subnet without internet access enabled (e.g. an isolated subnnet).
>
> Ensure that the Canary is placed in a VPC either with internet connectivity or with VPC Endpoints for S3 and CloudWatch enabled and configured.
>
> See [Synthetics VPC docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html).

### Alarms

You can configure a CloudWatch Alarm on a canary metric. Metrics are emitted by CloudWatch automatically and can be accessed by the following APIs:

* `canary.metricSuccessPercent()` - percentage of successful canary runs over a given time
* `canary.metricDuration()` - how much time each canary run takes, in seconds.
* `canary.metricFailed()` - number of failed canary runs over a given time

Create an alarm that tracks the canary metric:

```python
import aws_cdk.aws_cloudwatch as cloudwatch

# canary: synthetics.Canary

cloudwatch.Alarm(self, "CanaryAlarm",
    metric=canary.metric_success_percent(),
    evaluation_periods=2,
    threshold=90,
    comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD
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

import aws_cdk.assets as _aws_cdk_assets_b1c45fb6
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_525817d7
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.ArtifactsBucketLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "prefix": "prefix"},
)
class ArtifactsBucketLocation:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for specifying the s3 location that stores the data of each canary run.

        The artifacts bucket location **cannot**
        be updated once the canary is created.

        :param bucket: (experimental) The s3 location that stores the data of each run.
        :param prefix: (experimental) The S3 bucket prefix. Specify this if you want a more specific path within the artifacts bucket. Default: - no prefix

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3 as s3
            import aws_cdk.aws_synthetics as synthetics
            
            # bucket: s3.Bucket
            
            artifacts_bucket_location = synthetics.ArtifactsBucketLocation(
                bucket=bucket,
            
                # the properties below are optional
                prefix="prefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877fe1a8370a2771d3c0c74a66a087e021a140579a0ad46a2b32a6044fea341d)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_55f001a5.IBucket:
        '''(experimental) The s3 location that stores the data of each run.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_55f001a5.IBucket, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 bucket prefix.

        Specify this if you want a more specific path within the artifacts bucket.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsBucketLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_67de8e8d.IConnectable)
class Canary(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-synthetics.Canary",
):
    '''(experimental) Define a new Canary.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        canary = synthetics.Canary(self, "MyCanary",
            schedule=synthetics.Schedule.rate(Duration.minutes(5)),
            test=synthetics.Test.custom(
                code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
                handler="index.handler"
            ),
            runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
            environment_variables={
                "stage": "prod"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        runtime: "Runtime",
        test: "Test",
        artifacts_bucket_location: typing.Optional[typing.Union[ArtifactsBucketLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        canary_name: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        failure_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        schedule: typing.Optional["Schedule"] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        start_after_creation: typing.Optional[builtins.bool] = None,
        success_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        time_to_live: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param runtime: (experimental) Specify the runtime version to use for the canary.
        :param test: (experimental) The type of test that you want your canary to run. Use ``Test.custom()`` to specify the test to run.
        :param artifacts_bucket_location: (experimental) The s3 location that stores the data of the canary runs. Default: - A new s3 bucket will be created without a prefix.
        :param canary_name: (experimental) The name of the canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary name. The canary name makes up part of the canary ARN, which is included in outbound calls over the internet. Default: - A unique name will be generated from the construct ID
        :param environment_variables: (experimental) Key-value pairs that the Synthetics caches and makes available for your canary scripts. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Canary script source code. Default: - No environment variables.
        :param failure_retention_period: (experimental) How many days should failed runs be retained. Default: Duration.days(31)
        :param role: (experimental) Canary execution role. This is the role that will be assumed by the canary upon execution. It controls the permissions that the canary will have. The role must be assumable by the AWS Lambda service principal. If not supplied, a role will be created with all the required permissions. If you provide a Role, you must add the required permissions. Default: - A unique role will be generated for this canary. You can add permissions to roles by calling 'addToRolePolicy'.
        :param schedule: (experimental) Specify the schedule for how often the canary runs. For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes. You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``. Default: 'rate(5 minutes)'
        :param security_groups: (experimental) The list of security groups to associate with the canary's network interfaces. You must provide ``vpc`` when using this prop. Default: - If the canary is placed within a VPC and a security group is not specified a dedicated security group will be created for this canary.
        :param start_after_creation: (experimental) Whether or not the canary should start after creation. Default: true
        :param success_retention_period: (experimental) How many days should successful runs be retained. Default: Duration.days(31)
        :param time_to_live: (experimental) How long the canary will be in a 'RUNNING' state. For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``, your canary will run at 10 minute intervals for an hour, for a total of 6 times. Default: - no limit
        :param vpc: (experimental) The VPC where this canary is run. Specify this if the canary needs to access resources in a VPC. Default: - Not in VPC
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. You must provide ``vpc`` when using this prop. Default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f49d4729949041ace80ae655c099ecea6783cb4e1a45eafccb490375484c289)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CanaryProps(
            runtime=runtime,
            test=test,
            artifacts_bucket_location=artifacts_bucket_location,
            canary_name=canary_name,
            environment_variables=environment_variables,
            failure_retention_period=failure_retention_period,
            role=role,
            schedule=schedule,
            security_groups=security_groups,
            start_after_creation=start_after_creation,
            success_retention_period=success_retention_period,
            time_to_live=time_to_live,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''(experimental) Measure the Duration of a single canary run, in seconds.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes

        :stability: experimental
        '''
        options = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricDuration", [options]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''(experimental) Measure the number of failed canary runs over a given time period.

        Default: sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        options = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricFailed", [options]))

    @jsii.member(jsii_name="metricSuccessPercent")
    def metric_success_percent(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''(experimental) Measure the percentage of successful canary runs.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes

        :stability: experimental
        '''
        options = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricSuccessPercent", [options]))

    @builtins.property
    @jsii.member(jsii_name="artifactsBucket")
    def artifacts_bucket(self) -> _aws_cdk_aws_s3_55f001a5.IBucket:
        '''(experimental) Bucket where data from each canary run is stored.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_55f001a5.IBucket, jsii.get(self, "artifactsBucket"))

    @builtins.property
    @jsii.member(jsii_name="canaryId")
    def canary_id(self) -> builtins.str:
        '''(experimental) The canary ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "canaryId"))

    @builtins.property
    @jsii.member(jsii_name="canaryName")
    def canary_name(self) -> builtins.str:
        '''(experimental) The canary Name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "canaryName"))

    @builtins.property
    @jsii.member(jsii_name="canaryState")
    def canary_state(self) -> builtins.str:
        '''(experimental) The state of the canary.

        For example, 'RUNNING', 'STOPPED', 'NOT STARTED', or 'ERROR'.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "canaryState"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_67de8e8d.Connections:
        '''(experimental) Access the Connections object.

        Will fail if not a VPC-enabled Canary

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_940a1ce0.IRole:
        '''(experimental) Execution role associated with this Canary.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.CanaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "runtime": "runtime",
        "test": "test",
        "artifacts_bucket_location": "artifactsBucketLocation",
        "canary_name": "canaryName",
        "environment_variables": "environmentVariables",
        "failure_retention_period": "failureRetentionPeriod",
        "role": "role",
        "schedule": "schedule",
        "security_groups": "securityGroups",
        "start_after_creation": "startAfterCreation",
        "success_retention_period": "successRetentionPeriod",
        "time_to_live": "timeToLive",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class CanaryProps:
    def __init__(
        self,
        *,
        runtime: "Runtime",
        test: "Test",
        artifacts_bucket_location: typing.Optional[typing.Union[ArtifactsBucketLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        canary_name: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        failure_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        schedule: typing.Optional["Schedule"] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        start_after_creation: typing.Optional[builtins.bool] = None,
        success_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        time_to_live: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for a canary.

        :param runtime: (experimental) Specify the runtime version to use for the canary.
        :param test: (experimental) The type of test that you want your canary to run. Use ``Test.custom()`` to specify the test to run.
        :param artifacts_bucket_location: (experimental) The s3 location that stores the data of the canary runs. Default: - A new s3 bucket will be created without a prefix.
        :param canary_name: (experimental) The name of the canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary name. The canary name makes up part of the canary ARN, which is included in outbound calls over the internet. Default: - A unique name will be generated from the construct ID
        :param environment_variables: (experimental) Key-value pairs that the Synthetics caches and makes available for your canary scripts. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Canary script source code. Default: - No environment variables.
        :param failure_retention_period: (experimental) How many days should failed runs be retained. Default: Duration.days(31)
        :param role: (experimental) Canary execution role. This is the role that will be assumed by the canary upon execution. It controls the permissions that the canary will have. The role must be assumable by the AWS Lambda service principal. If not supplied, a role will be created with all the required permissions. If you provide a Role, you must add the required permissions. Default: - A unique role will be generated for this canary. You can add permissions to roles by calling 'addToRolePolicy'.
        :param schedule: (experimental) Specify the schedule for how often the canary runs. For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes. You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``. Default: 'rate(5 minutes)'
        :param security_groups: (experimental) The list of security groups to associate with the canary's network interfaces. You must provide ``vpc`` when using this prop. Default: - If the canary is placed within a VPC and a security group is not specified a dedicated security group will be created for this canary.
        :param start_after_creation: (experimental) Whether or not the canary should start after creation. Default: true
        :param success_retention_period: (experimental) How many days should successful runs be retained. Default: Duration.days(31)
        :param time_to_live: (experimental) How long the canary will be in a 'RUNNING' state. For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``, your canary will run at 10 minute intervals for an hour, for a total of 6 times. Default: - no limit
        :param vpc: (experimental) The VPC where this canary is run. Specify this if the canary needs to access resources in a VPC. Default: - Not in VPC
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. You must provide ``vpc`` when using this prop. Default: - the Vpc default strategy if not specified

        :stability: experimental
        :exampleMetadata: infused

        Example::

            canary = synthetics.Canary(self, "MyCanary",
                schedule=synthetics.Schedule.rate(Duration.minutes(5)),
                test=synthetics.Test.custom(
                    code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
                    handler="index.handler"
                ),
                runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
                environment_variables={
                    "stage": "prod"
                }
            )
        '''
        if isinstance(artifacts_bucket_location, dict):
            artifacts_bucket_location = ArtifactsBucketLocation(**artifacts_bucket_location)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebafcf9877ad731ac6cdd4e7c1c45bfc4eeb3322e90b5560353937b8375d2a1e)
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument test", value=test, expected_type=type_hints["test"])
            check_type(argname="argument artifacts_bucket_location", value=artifacts_bucket_location, expected_type=type_hints["artifacts_bucket_location"])
            check_type(argname="argument canary_name", value=canary_name, expected_type=type_hints["canary_name"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument failure_retention_period", value=failure_retention_period, expected_type=type_hints["failure_retention_period"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument start_after_creation", value=start_after_creation, expected_type=type_hints["start_after_creation"])
            check_type(argname="argument success_retention_period", value=success_retention_period, expected_type=type_hints["success_retention_period"])
            check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime": runtime,
            "test": test,
        }
        if artifacts_bucket_location is not None:
            self._values["artifacts_bucket_location"] = artifacts_bucket_location
        if canary_name is not None:
            self._values["canary_name"] = canary_name
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if role is not None:
            self._values["role"] = role
        if schedule is not None:
            self._values["schedule"] = schedule
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if start_after_creation is not None:
            self._values["start_after_creation"] = start_after_creation
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def runtime(self) -> "Runtime":
        '''(experimental) Specify the runtime version to use for the canary.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html
        :stability: experimental
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast("Runtime", result)

    @builtins.property
    def test(self) -> "Test":
        '''(experimental) The type of test that you want your canary to run.

        Use ``Test.custom()`` to specify the test to run.

        :stability: experimental
        '''
        result = self._values.get("test")
        assert result is not None, "Required property 'test' is missing"
        return typing.cast("Test", result)

    @builtins.property
    def artifacts_bucket_location(self) -> typing.Optional[ArtifactsBucketLocation]:
        '''(experimental) The s3 location that stores the data of the canary runs.

        :default: - A new s3 bucket will be created without a prefix.

        :stability: experimental
        '''
        result = self._values.get("artifacts_bucket_location")
        return typing.cast(typing.Optional[ArtifactsBucketLocation], result)

    @builtins.property
    def canary_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the canary.

        Be sure to give it a descriptive name that distinguishes it from
        other canaries in your account.

        Do not include secrets or proprietary information in your canary name. The canary name
        makes up part of the canary ARN, which is included in outbound calls over the internet.

        :default: - A unique name will be generated from the construct ID

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html
        :stability: experimental
        '''
        result = self._values.get("canary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-value pairs that the Synthetics caches and makes available for your canary scripts.

        Use environment variables
        to apply configuration changes, such as test and production environment configurations, without changing your
        Canary script source code.

        :default: - No environment variables.

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def failure_retention_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) How many days should failed runs be retained.

        :default: Duration.days(31)

        :stability: experimental
        '''
        result = self._values.get("failure_retention_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) Canary execution role.

        This is the role that will be assumed by the canary upon execution.
        It controls the permissions that the canary will have. The role must
        be assumable by the AWS Lambda service principal.

        If not supplied, a role will be created with all the required permissions.
        If you provide a Role, you must add the required permissions.

        :default:

        - A unique role will be generated for this canary.
        You can add permissions to roles by calling 'addToRolePolicy'.

        :see: required permissions: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        '''(experimental) Specify the schedule for how often the canary runs.

        For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes.
        You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``.

        :default: 'rate(5 minutes)'

        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["Schedule"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''(experimental) The list of security groups to associate with the canary's network interfaces.

        You must provide ``vpc`` when using this prop.

        :default:

        - If the canary is placed within a VPC and a security group is
        not specified a dedicated security group will be created for this canary.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def start_after_creation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the canary should start after creation.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("start_after_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def success_retention_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) How many days should successful runs be retained.

        :default: Duration.days(31)

        :stability: experimental
        '''
        result = self._values.get("success_retention_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def time_to_live(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) How long the canary will be in a 'RUNNING' state.

        For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``,
        your canary will run at 10 minute intervals for an hour, for a total of 6 times.

        :default: - no limit

        :stability: experimental
        '''
        result = self._values.get("time_to_live")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''(experimental) The VPC where this canary is run.

        Specify this if the canary needs to access resources in a VPC.

        :default: - Not in VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        You must provide ``vpc`` when using this prop.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCanary(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-synthetics.CfnCanary",
):
    '''A CloudFormation ``AWS::Synthetics::Canary``.

    Creates or updates a canary. Canaries are scripts that monitor your endpoints and APIs from the outside-in. Canaries help you check the availability and latency of your web services and troubleshoot anomalies by investigating load time data, screenshots of the UI, logs, and metrics. You can set up a canary to run continuously or just once.

    To create canaries, you must have the ``CloudWatchSyntheticsFullAccess`` policy. If you are creating a new IAM role for the canary, you also need the the ``iam:CreateRole`` , ``iam:CreatePolicy`` and ``iam:AttachRolePolicy`` permissions. For more information, see `Necessary Roles and Permissions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Roles>`_ .

    Do not include secrets or proprietary information in your canary names. The canary name makes up part of the Amazon Resource Name (ARN) for the canary, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .

    :cloudformationResource: AWS::Synthetics::Canary
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_synthetics as synthetics
        
        cfn_canary = synthetics.CfnCanary(self, "MyCfnCanary",
            artifact_s3_location="artifactS3Location",
            code=synthetics.CfnCanary.CodeProperty(
                handler="handler",
        
                # the properties below are optional
                s3_bucket="s3Bucket",
                s3_key="s3Key",
                s3_object_version="s3ObjectVersion",
                script="script",
                source_location_arn="sourceLocationArn"
            ),
            execution_role_arn="executionRoleArn",
            name="name",
            runtime_version="runtimeVersion",
            schedule=synthetics.CfnCanary.ScheduleProperty(
                expression="expression",
        
                # the properties below are optional
                duration_in_seconds="durationInSeconds"
            ),
        
            # the properties below are optional
            artifact_config=synthetics.CfnCanary.ArtifactConfigProperty(
                s3_encryption=synthetics.CfnCanary.S3EncryptionProperty(
                    encryption_mode="encryptionMode",
                    kms_key_arn="kmsKeyArn"
                )
            ),
            delete_lambda_resources_on_canary_deletion=False,
            failure_retention_period=123,
            run_config=synthetics.CfnCanary.RunConfigProperty(
                active_tracing=False,
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                memory_in_mb=123,
                timeout_in_seconds=123
            ),
            start_canary_after_creation=False,
            success_retention_period=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            visual_reference=synthetics.CfnCanary.VisualReferenceProperty(
                base_canary_run_id="baseCanaryRunId",
        
                # the properties below are optional
                base_screenshots=[synthetics.CfnCanary.BaseScreenshotProperty(
                    screenshot_name="screenshotName",
        
                    # the properties below are optional
                    ignore_coordinates=["ignoreCoordinates"]
                )]
            ),
            vpc_config=synthetics.CfnCanary.VPCConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
        
                # the properties below are optional
                vpc_id="vpcId"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        artifact_s3_location: builtins.str,
        code: typing.Union[typing.Union["CfnCanary.CodeProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        execution_role_arn: builtins.str,
        name: builtins.str,
        runtime_version: builtins.str,
        schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]],
        artifact_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.ArtifactConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        delete_lambda_resources_on_canary_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        failure_retention_period: typing.Optional[jsii.Number] = None,
        run_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.RunConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        start_canary_after_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        visual_reference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.VisualReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.VPCConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Synthetics::Canary``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param artifact_s3_location: The location in Amazon S3 where Synthetics stores artifacts from the runs of this canary. Artifacts include the log file, screenshots, and HAR files. Specify the full location path, including ``s3://`` at the beginning of the path.
        :param code: Use this structure to input your script code for the canary. This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .
        :param execution_role_arn: The ARN of the IAM role to be used to run the canary. This role must already exist, and must include ``lambda.amazonaws.com`` as a principal in the trust policy. The role must also have the following permissions: - ``s3:PutObject`` - ``s3:GetBucketLocation`` - ``s3:ListAllMyBuckets`` - ``cloudwatch:PutMetricData`` - ``logs:CreateLogGroup`` - ``logs:CreateLogStream`` - ``logs:PutLogEvents``
        :param name: The name for this canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary names. The canary name makes up part of the canary ARN, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .
        :param runtime_version: Specifies the runtime version to use for the canary. For more information about runtime versions, see `Canary Runtime Versions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html>`_ .
        :param schedule: A structure that contains information about how often the canary is to run, and when these runs are to stop.
        :param artifact_config: A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3.
        :param delete_lambda_resources_on_canary_deletion: ``AWS::Synthetics::Canary.DeleteLambdaResourcesOnCanaryDeletion``.
        :param failure_retention_period: The number of days to retain data about failed runs of this canary. If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.
        :param run_config: A structure that contains input information for a canary run. If you omit this structure, the frequency of the canary is used as canary's timeout value, up to a maximum of 900 seconds.
        :param start_canary_after_creation: Specify TRUE to have the canary start making runs immediately after it is created. A canary that you create using CloudFormation can't be used to monitor the CloudFormation stack that creates the canary or to roll back that stack if there is a failure.
        :param success_retention_period: The number of days to retain data about successful runs of this canary. If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.
        :param tags: The list of key-value pairs that are associated with the canary.
        :param visual_reference: If this canary performs visual monitoring by comparing screenshots, this structure contains the ID of the canary run to use as the baseline for screenshots, and the coordinates of any parts of the screen to ignore during the visual monitoring comparison.
        :param vpc_config: If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint. For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8adb76158ebc83b0e1114879c773192d0b987275745c58d9e44e2e547f9cc79b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCanaryProps(
            artifact_s3_location=artifact_s3_location,
            code=code,
            execution_role_arn=execution_role_arn,
            name=name,
            runtime_version=runtime_version,
            schedule=schedule,
            artifact_config=artifact_config,
            delete_lambda_resources_on_canary_deletion=delete_lambda_resources_on_canary_deletion,
            failure_retention_period=failure_retention_period,
            run_config=run_config,
            start_canary_after_creation=start_canary_after_creation,
            success_retention_period=success_retention_period,
            tags=tags,
            visual_reference=visual_reference,
            vpc_config=vpc_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e7672cdc2990df45da2ebf445293f028723a1bc56a4f41407bd45b114772c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8c03f5e2e0aca65aebc755a1c1cb707fdd6b46774d1c954b7951797e1d71705)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCodeSourceLocationArn")
    def attr_code_source_location_arn(self) -> builtins.str:
        '''``Ref`` returns the ARN of the Lambda layer where Synthetics stores the canary script code.

        :cloudformationAttribute: Code.SourceLocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCodeSourceLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the canary.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the canary.

        For example, ``RUNNING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The list of key-value pairs that are associated with the canary.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="artifactS3Location")
    def artifact_s3_location(self) -> builtins.str:
        '''The location in Amazon S3 where Synthetics stores artifacts from the runs of this canary.

        Artifacts include the log file, screenshots, and HAR files. Specify the full location path, including ``s3://`` at the beginning of the path.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactS3Location"))

    @artifact_s3_location.setter
    def artifact_s3_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535213fe8f968723001256a27edd42fa6dd0e8a45b28dc94d3a644af5076c394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(
        self,
    ) -> typing.Union["CfnCanary.CodeProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Use this structure to input your script code for the canary.

        This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        '''
        return typing.cast(typing.Union["CfnCanary.CodeProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "code"))

    @code.setter
    def code(
        self,
        value: typing.Union["CfnCanary.CodeProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d7a99cfe8b521f0c4ac94d0db162ff438ff9648a7449498c6f3dc20d118d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role to be used to run the canary.

        This role must already exist, and must include ``lambda.amazonaws.com`` as a principal in the trust policy. The role must also have the following permissions:

        - ``s3:PutObject``
        - ``s3:GetBucketLocation``
        - ``s3:ListAllMyBuckets``
        - ``cloudwatch:PutMetricData``
        - ``logs:CreateLogGroup``
        - ``logs:CreateLogStream``
        - ``logs:PutLogEvents``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36aac1db5e6a1b7d5d8c7fbfbf993e7d19fed69de2e0b9b337e5bddf4555ecd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for this canary.

        Be sure to give it a descriptive name that distinguishes it from other canaries in your account.

        Do not include secrets or proprietary information in your canary names. The canary name makes up part of the canary ARN, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c2130db4ee16f96fb4ff26768c14064c808f2b82ea94847c42a0a2f50aac14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        '''Specifies the runtime version to use for the canary.

        For more information about runtime versions, see `Canary Runtime Versions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beced46adface6ec3f552c6c926c43fc7aca6273c69be0f74b4ae15ac22090ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.ScheduleProperty"]:
        '''A structure that contains information about how often the canary is to run, and when these runs are to stop.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.ScheduleProperty"], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.ScheduleProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200920497c576a0714b3e81084b3097516d06d18f875245fd9d50a50ffad6089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="artifactConfig")
    def artifact_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.ArtifactConfigProperty"]]:
        '''A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifactconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.ArtifactConfigProperty"]], jsii.get(self, "artifactConfig"))

    @artifact_config.setter
    def artifact_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.ArtifactConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a721db6f2b790e8ff7639352297bfc87af12f89bdc2baff8d7f1184a8d08f8a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactConfig", value)

    @builtins.property
    @jsii.member(jsii_name="deleteLambdaResourcesOnCanaryDeletion")
    def delete_lambda_resources_on_canary_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Synthetics::Canary.DeleteLambdaResourcesOnCanaryDeletion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-deletelambdaresourcesoncanarydeletion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deleteLambdaResourcesOnCanaryDeletion"))

    @delete_lambda_resources_on_canary_deletion.setter
    def delete_lambda_resources_on_canary_deletion(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5649c4dd679377bec144797abccb50b8000bda7684a7ca2400378427836edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteLambdaResourcesOnCanaryDeletion", value)

    @builtins.property
    @jsii.member(jsii_name="failureRetentionPeriod")
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain data about failed runs of this canary.

        If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureRetentionPeriod"))

    @failure_retention_period.setter
    def failure_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4d40163b2c8524be72914366407a0636f998549468b56820f395779614de76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="runConfig")
    def run_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.RunConfigProperty"]]:
        '''A structure that contains input information for a canary run.

        If you omit this structure, the frequency of the canary is used as canary's timeout value, up to a maximum of 900 seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.RunConfigProperty"]], jsii.get(self, "runConfig"))

    @run_config.setter
    def run_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.RunConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7049326db3bb14eae2c879160ce1d9d0ba5c7149398e8088e2d2ae37a1f8b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runConfig", value)

    @builtins.property
    @jsii.member(jsii_name="startCanaryAfterCreation")
    def start_canary_after_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specify TRUE to have the canary start making runs immediately after it is created.

        A canary that you create using CloudFormation can't be used to monitor the CloudFormation stack that creates the canary or to roll back that stack if there is a failure.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "startCanaryAfterCreation"))

    @start_canary_after_creation.setter
    def start_canary_after_creation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c227e49ceab6691d49923513c8dc66343c93fa052b8689e29f9338eca25054d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startCanaryAfterCreation", value)

    @builtins.property
    @jsii.member(jsii_name="successRetentionPeriod")
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain data about successful runs of this canary.

        If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successRetentionPeriod"))

    @success_retention_period.setter
    def success_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8190a74f8342b5846739ef45bcbdf13162302b8f74e8ab2344fc8f19b1427714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="visualReference")
    def visual_reference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.VisualReferenceProperty"]]:
        '''If this canary performs visual monitoring by comparing screenshots, this structure contains the ID of the canary run to use as the baseline for screenshots, and the coordinates of any parts of the screen to ignore during the visual monitoring comparison.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-visualreference
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.VisualReferenceProperty"]], jsii.get(self, "visualReference"))

    @visual_reference.setter
    def visual_reference(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.VisualReferenceProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23813ba279d0d20bcaf3c590c4e427e68413ebe83bd169b8866ed020648c2498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visualReference", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.VPCConfigProperty"]]:
        '''If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint.

        For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.VPCConfigProperty"]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.VPCConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb14178cad2226bf0714354dd4592b585625e7923ef8e74edfee7f85dd489ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.ArtifactConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_encryption": "s3Encryption"},
    )
    class ArtifactConfigProperty:
        def __init__(
            self,
            *,
            s3_encryption: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.S3EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 .

            :param s3_encryption: A structure that contains the configuration of the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 . Artifact encryption functionality is available only for canaries that use Synthetics runtime version syn-nodejs-puppeteer-3.3 or later. For more information, see `Encrypting canary artifacts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-artifactconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                artifact_config_property = synthetics.CfnCanary.ArtifactConfigProperty(
                    s3_encryption=synthetics.CfnCanary.S3EncryptionProperty(
                        encryption_mode="encryptionMode",
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea7de815bbfd8bd4c122f0890398a37b17f5260ecc3b84d1fd58bff1c8eb0e43)
                check_type(argname="argument s3_encryption", value=s3_encryption, expected_type=type_hints["s3_encryption"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_encryption is not None:
                self._values["s3_encryption"] = s3_encryption

        @builtins.property
        def s3_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.S3EncryptionProperty"]]:
            '''A structure that contains the configuration of the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 .

            Artifact encryption functionality is available only for canaries that use Synthetics runtime version syn-nodejs-puppeteer-3.3 or later. For more information, see `Encrypting canary artifacts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-artifactconfig.html#cfn-synthetics-canary-artifactconfig-s3encryption
            '''
            result = self._values.get("s3_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.S3EncryptionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.BaseScreenshotProperty",
        jsii_struct_bases=[],
        name_mapping={
            "screenshot_name": "screenshotName",
            "ignore_coordinates": "ignoreCoordinates",
        },
    )
    class BaseScreenshotProperty:
        def __init__(
            self,
            *,
            screenshot_name: builtins.str,
            ignore_coordinates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A structure representing a screenshot that is used as a baseline during visual monitoring comparisons made by the canary.

            :param screenshot_name: The name of the screenshot. This is generated the first time the canary is run after the ``UpdateCanary`` operation that specified for this canary to perform visual monitoring.
            :param ignore_coordinates: Coordinates that define the part of a screen to ignore during screenshot comparisons. To obtain the coordinates to use here, use the CloudWatch console to draw the boundaries on the screen. For more information, see `Edit or delete a canary <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/synthetics_canaries_deletion.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-basescreenshot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                base_screenshot_property = synthetics.CfnCanary.BaseScreenshotProperty(
                    screenshot_name="screenshotName",
                
                    # the properties below are optional
                    ignore_coordinates=["ignoreCoordinates"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e972da934c239df7dafdca862e9ad38ec1553fcdbbf43ed3a10e86bfebc1a7b)
                check_type(argname="argument screenshot_name", value=screenshot_name, expected_type=type_hints["screenshot_name"])
                check_type(argname="argument ignore_coordinates", value=ignore_coordinates, expected_type=type_hints["ignore_coordinates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "screenshot_name": screenshot_name,
            }
            if ignore_coordinates is not None:
                self._values["ignore_coordinates"] = ignore_coordinates

        @builtins.property
        def screenshot_name(self) -> builtins.str:
            '''The name of the screenshot.

            This is generated the first time the canary is run after the ``UpdateCanary`` operation that specified for this canary to perform visual monitoring.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-basescreenshot.html#cfn-synthetics-canary-basescreenshot-screenshotname
            '''
            result = self._values.get("screenshot_name")
            assert result is not None, "Required property 'screenshot_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ignore_coordinates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Coordinates that define the part of a screen to ignore during screenshot comparisons.

            To obtain the coordinates to use here, use the CloudWatch console to draw the boundaries on the screen. For more information, see `Edit or delete a canary <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/synthetics_canaries_deletion.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-basescreenshot.html#cfn-synthetics-canary-basescreenshot-ignorecoordinates
            '''
            result = self._values.get("ignore_coordinates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BaseScreenshotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "handler": "handler",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
            "script": "script",
            "source_location_arn": "sourceLocationArn",
        },
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            handler: builtins.str,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
            script: typing.Optional[builtins.str] = None,
            source_location_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to input your script code for the canary.

            This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .

            :param handler: The entry point to use for the source code when running the canary. For canaries that use the ``syn-python-selenium-1.0`` runtime or a ``syn-nodejs.puppeteer`` runtime earlier than ``syn-nodejs.puppeteer-3.4`` , the handler must be specified as ``*fileName* .handler`` . For ``syn-python-selenium-1.1`` , ``syn-nodejs.puppeteer-3.4`` , and later runtimes, the handler can be specified as ``*fileName* . *functionName*`` , or you can specify a folder where canary scripts reside as ``*folder* / *fileName* . *functionName*`` .
            :param s3_bucket: If your canary script is located in S3, specify the bucket name here. The bucket must already exist.
            :param s3_key: The S3 key of your script. For more information, see `Working with Amazon S3 Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingObjects.html>`_ .
            :param s3_object_version: The S3 version ID of your script.
            :param script: If you input your canary script directly into the canary instead of referring to an S3 location, the value of this parameter is the script in plain text. It can be up to 5 MB.
            :param source_location_arn: The ARN of the Lambda layer where Synthetics stores the canary script code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                code_property = synthetics.CfnCanary.CodeProperty(
                    handler="handler",
                
                    # the properties below are optional
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion",
                    script="script",
                    source_location_arn="sourceLocationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__475dbe17c4645b87a88a4cdd642e9f5239af9cf2521f616ac1f1448fbc4fff4f)
                check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
                check_type(argname="argument script", value=script, expected_type=type_hints["script"])
                check_type(argname="argument source_location_arn", value=source_location_arn, expected_type=type_hints["source_location_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "handler": handler,
            }
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version
            if script is not None:
                self._values["script"] = script
            if source_location_arn is not None:
                self._values["source_location_arn"] = source_location_arn

        @builtins.property
        def handler(self) -> builtins.str:
            '''The entry point to use for the source code when running the canary.

            For canaries that use the ``syn-python-selenium-1.0`` runtime or a ``syn-nodejs.puppeteer`` runtime earlier than ``syn-nodejs.puppeteer-3.4`` , the handler must be specified as ``*fileName* .handler`` . For ``syn-python-selenium-1.1`` , ``syn-nodejs.puppeteer-3.4`` , and later runtimes, the handler can be specified as ``*fileName* . *functionName*`` , or you can specify a folder where canary scripts reside as ``*folder* / *fileName* . *functionName*`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-handler
            '''
            result = self._values.get("handler")
            assert result is not None, "Required property 'handler' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''If your canary script is located in S3, specify the bucket name here.

            The bucket must already exist.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The S3 key of your script.

            For more information, see `Working with Amazon S3 Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingObjects.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''The S3 version ID of your script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script(self) -> typing.Optional[builtins.str]:
            '''If you input your canary script directly into the canary instead of referring to an S3 location, the value of this parameter is the script in plain text.

            It can be up to 5 MB.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-script
            '''
            result = self._values.get("script")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_location_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda layer where Synthetics stores the canary script code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-sourcelocationarn
            '''
            result = self._values.get("source_location_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.RunConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_tracing": "activeTracing",
            "environment_variables": "environmentVariables",
            "memory_in_mb": "memoryInMb",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class RunConfigProperty:
        def __init__(
            self,
            *,
            active_tracing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            memory_in_mb: typing.Optional[jsii.Number] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A structure that contains input information for a canary run.

            This structure is required.

            :param active_tracing: Specifies whether this canary is to use active AWS X-Ray tracing when it runs. Active tracing enables this canary run to be displayed in the ServiceLens and X-Ray service maps even if the canary does not hit an endpoint that has X-Ray tracing enabled. Using X-Ray tracing incurs charges. For more information, see `Canaries and X-Ray tracing <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_tracing.html>`_ . You can enable active tracing only for canaries that use version ``syn-nodejs-2.0`` or later for their canary runtime.
            :param environment_variables: Specifies the keys and values to use for any environment variables used in the canary script. Use the following format: { "key1" : "value1", "key2" : "value2", ...} Keys must start with a letter and be at least two characters. The total size of your environment variables cannot exceed 4 KB. You can't specify any Lambda reserved environment variables as the keys for your environment variables. For more information about reserved keys, see `Runtime environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-runtime>`_ .
            :param memory_in_mb: The maximum amount of memory that the canary can use while running. This value must be a multiple of 64. The range is 960 to 3008.
            :param timeout_in_seconds: How long the canary is allowed to run before it must stop. You can't set this time to be longer than the frequency of the runs of this canary. If you omit this field, the frequency of the canary is used as this value, up to a maximum of 900 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                run_config_property = synthetics.CfnCanary.RunConfigProperty(
                    active_tracing=False,
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    memory_in_mb=123,
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97afdec6d5442f1925fbce72bd8ff5b2ffc1cbed4c8aa317e745e90de4444d98)
                check_type(argname="argument active_tracing", value=active_tracing, expected_type=type_hints["active_tracing"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument memory_in_mb", value=memory_in_mb, expected_type=type_hints["memory_in_mb"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_tracing is not None:
                self._values["active_tracing"] = active_tracing
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if memory_in_mb is not None:
                self._values["memory_in_mb"] = memory_in_mb
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def active_tracing(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether this canary is to use active AWS X-Ray tracing when it runs.

            Active tracing enables this canary run to be displayed in the ServiceLens and X-Ray service maps even if the canary does not hit an endpoint that has X-Ray tracing enabled. Using X-Ray tracing incurs charges. For more information, see `Canaries and X-Ray tracing <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_tracing.html>`_ .

            You can enable active tracing only for canaries that use version ``syn-nodejs-2.0`` or later for their canary runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-activetracing
            '''
            result = self._values.get("active_tracing")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''Specifies the keys and values to use for any environment variables used in the canary script.

            Use the following format:

            { "key1" : "value1", "key2" : "value2", ...}

            Keys must start with a letter and be at least two characters. The total size of your environment variables cannot exceed 4 KB. You can't specify any Lambda reserved environment variables as the keys for your environment variables. For more information about reserved keys, see `Runtime environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-runtime>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def memory_in_mb(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of memory that the canary can use while running.

            This value must be a multiple of 64. The range is 960 to 3008.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-memoryinmb
            '''
            result = self._values.get("memory_in_mb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''How long the canary is allowed to run before it must stop.

            You can't set this time to be longer than the frequency of the runs of this canary.

            If you omit this field, the frequency of the canary is used as this value, up to a maximum of 900 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.S3EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_mode": "encryptionMode", "kms_key_arn": "kmsKeyArn"},
    )
    class S3EncryptionProperty:
        def __init__(
            self,
            *,
            encryption_mode: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the configuration of the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 .

            Artifact encryption functionality is available only for canaries that use Synthetics runtime version syn-nodejs-puppeteer-3.3 or later. For more information, see `Encrypting canary artifacts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html>`_ .

            :param encryption_mode: The encryption method to use for artifacts created by this canary. Specify ``SSE_S3`` to use server-side encryption (SSE) with an Amazon S3-managed key. Specify ``SSE-KMS`` to use server-side encryption with a customer-managed AWS KMS key. If you omit this parameter, an AWS -managed AWS KMS key is used.
            :param kms_key_arn: The ARN of the customer-managed AWS KMS key to use, if you specify ``SSE-KMS`` for ``EncryptionMode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-s3encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                s3_encryption_property = synthetics.CfnCanary.S3EncryptionProperty(
                    encryption_mode="encryptionMode",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fe623c6e242fced46173ae729e5ea6ad500587f3b65658e118512b527073907)
                check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_mode is not None:
                self._values["encryption_mode"] = encryption_mode
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption method to use for artifacts created by this canary.

            Specify ``SSE_S3`` to use server-side encryption (SSE) with an Amazon S3-managed key. Specify ``SSE-KMS`` to use server-side encryption with a customer-managed AWS KMS key.

            If you omit this parameter, an AWS -managed AWS KMS key is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-s3encryption.html#cfn-synthetics-canary-s3encryption-encryptionmode
            '''
            result = self._values.get("encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the customer-managed AWS KMS key to use, if you specify ``SSE-KMS`` for ``EncryptionMode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-s3encryption.html#cfn-synthetics-canary-s3encryption-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "duration_in_seconds": "durationInSeconds",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            duration_in_seconds: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure specifies how often a canary is to make runs and the date and time when it should stop making runs.

            :param expression: A ``rate`` expression or a ``cron`` expression that defines how often the canary is to run. For a rate expression, The syntax is ``rate( *number unit* )`` . *unit* can be ``minute`` , ``minutes`` , or ``hour`` . For example, ``rate(1 minute)`` runs the canary once a minute, ``rate(10 minutes)`` runs it once every 10 minutes, and ``rate(1 hour)`` runs it once every hour. You can specify a frequency between ``rate(1 minute)`` and ``rate(1 hour)`` . Specifying ``rate(0 minute)`` or ``rate(0 hour)`` is a special value that causes the canary to run only once when it is started. Use ``cron( *expression* )`` to specify a cron expression. You can't schedule a canary to wait for more than a year before running. For information about the syntax for cron expressions, see `Scheduling canary runs using cron <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_cron.html>`_ .
            :param duration_in_seconds: How long, in seconds, for the canary to continue making regular runs according to the schedule in the ``Expression`` value. If you specify 0, the canary continues making runs until you stop it. If you omit this field, the default of 0 is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                schedule_property = synthetics.CfnCanary.ScheduleProperty(
                    expression="expression",
                
                    # the properties below are optional
                    duration_in_seconds="durationInSeconds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b2f10f4b095b130c13b16b9e6f81f513954e9a7bdeb3ac5af152e08a910780c)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "expression": expression,
            }
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def expression(self) -> builtins.str:
            '''A ``rate`` expression or a ``cron`` expression that defines how often the canary is to run.

            For a rate expression, The syntax is ``rate( *number unit* )`` . *unit* can be ``minute`` , ``minutes`` , or ``hour`` .

            For example, ``rate(1 minute)`` runs the canary once a minute, ``rate(10 minutes)`` runs it once every 10 minutes, and ``rate(1 hour)`` runs it once every hour. You can specify a frequency between ``rate(1 minute)`` and ``rate(1 hour)`` .

            Specifying ``rate(0 minute)`` or ``rate(0 hour)`` is a special value that causes the canary to run only once when it is started.

            Use ``cron( *expression* )`` to specify a cron expression. You can't schedule a canary to wait for more than a year before running. For information about the syntax for cron expressions, see `Scheduling canary runs using cron <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_cron.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-expression
            '''
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[builtins.str]:
            '''How long, in seconds, for the canary to continue making regular runs according to the schedule in the ``Expression`` value.

            If you specify 0, the canary continues making runs until you stop it. If you omit this field, the default of 0 is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.VPCConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_id": "vpcId",
        },
    )
    class VPCConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Sequence[builtins.str],
            subnet_ids: typing.Sequence[builtins.str],
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint.

            For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

            :param security_group_ids: The IDs of the security groups for this canary.
            :param subnet_ids: The IDs of the subnets where this canary is to run.
            :param vpc_id: The ID of the VPC where this canary is to run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                v_pCConfig_property = synthetics.CfnCanary.VPCConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                
                    # the properties below are optional
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02dee073365f82e9388517797b106c20f61a60398a204c75fe53c4ecb51ed09a)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''The IDs of the security groups for this canary.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''The IDs of the subnets where this canary is to run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC where this canary is to run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-synthetics.CfnCanary.VisualReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_canary_run_id": "baseCanaryRunId",
            "base_screenshots": "baseScreenshots",
        },
    )
    class VisualReferenceProperty:
        def __init__(
            self,
            *,
            base_canary_run_id: builtins.str,
            base_screenshots: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCanary.BaseScreenshotProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines the screenshots to use as the baseline for comparisons during visual monitoring comparisons during future runs of this canary.

            If you omit this parameter, no changes are made to any baseline screenshots that the canary might be using already.

            Visual monitoring is supported only on canaries running the *syn-puppeteer-node-3.2* runtime or later. For more information, see `Visual monitoring <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_SyntheticsLogger_VisualTesting.html>`_ and `Visual monitoring blueprint <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Blueprints_VisualTesting.html>`_

            :param base_canary_run_id: Specifies which canary run to use the screenshots from as the baseline for future visual monitoring with this canary. Valid values are ``nextrun`` to use the screenshots from the next run after this update is made, ``lastrun`` to use the screenshots from the most recent run before this update was made, or the value of ``Id`` in the `CanaryRun <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_CanaryRun.html>`_ from any past run of this canary.
            :param base_screenshots: An array of screenshots that are used as the baseline for comparisons during visual monitoring.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_synthetics as synthetics
                
                visual_reference_property = synthetics.CfnCanary.VisualReferenceProperty(
                    base_canary_run_id="baseCanaryRunId",
                
                    # the properties below are optional
                    base_screenshots=[synthetics.CfnCanary.BaseScreenshotProperty(
                        screenshot_name="screenshotName",
                
                        # the properties below are optional
                        ignore_coordinates=["ignoreCoordinates"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0fc0614ac0703546d147773c7deb4a60ce2b6a4910fbd8a117601591d44c6d9)
                check_type(argname="argument base_canary_run_id", value=base_canary_run_id, expected_type=type_hints["base_canary_run_id"])
                check_type(argname="argument base_screenshots", value=base_screenshots, expected_type=type_hints["base_screenshots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "base_canary_run_id": base_canary_run_id,
            }
            if base_screenshots is not None:
                self._values["base_screenshots"] = base_screenshots

        @builtins.property
        def base_canary_run_id(self) -> builtins.str:
            '''Specifies which canary run to use the screenshots from as the baseline for future visual monitoring with this canary.

            Valid values are ``nextrun`` to use the screenshots from the next run after this update is made, ``lastrun`` to use the screenshots from the most recent run before this update was made, or the value of ``Id`` in the `CanaryRun <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_CanaryRun.html>`_ from any past run of this canary.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html#cfn-synthetics-canary-visualreference-basecanaryrunid
            '''
            result = self._values.get("base_canary_run_id")
            assert result is not None, "Required property 'base_canary_run_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base_screenshots(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.BaseScreenshotProperty"]]]]:
            '''An array of screenshots that are used as the baseline for comparisons during visual monitoring.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html#cfn-synthetics-canary-visualreference-basescreenshots
            '''
            result = self._values.get("base_screenshots")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCanary.BaseScreenshotProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VisualReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.CfnCanaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_s3_location": "artifactS3Location",
        "code": "code",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "runtime_version": "runtimeVersion",
        "schedule": "schedule",
        "artifact_config": "artifactConfig",
        "delete_lambda_resources_on_canary_deletion": "deleteLambdaResourcesOnCanaryDeletion",
        "failure_retention_period": "failureRetentionPeriod",
        "run_config": "runConfig",
        "start_canary_after_creation": "startCanaryAfterCreation",
        "success_retention_period": "successRetentionPeriod",
        "tags": "tags",
        "visual_reference": "visualReference",
        "vpc_config": "vpcConfig",
    },
)
class CfnCanaryProps:
    def __init__(
        self,
        *,
        artifact_s3_location: builtins.str,
        code: typing.Union[typing.Union[CfnCanary.CodeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        execution_role_arn: builtins.str,
        name: builtins.str,
        runtime_version: builtins.str,
        schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
        artifact_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.ArtifactConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        delete_lambda_resources_on_canary_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        failure_retention_period: typing.Optional[jsii.Number] = None,
        run_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.RunConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        start_canary_after_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        visual_reference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.VisualReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.VPCConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCanary``.

        :param artifact_s3_location: The location in Amazon S3 where Synthetics stores artifacts from the runs of this canary. Artifacts include the log file, screenshots, and HAR files. Specify the full location path, including ``s3://`` at the beginning of the path.
        :param code: Use this structure to input your script code for the canary. This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .
        :param execution_role_arn: The ARN of the IAM role to be used to run the canary. This role must already exist, and must include ``lambda.amazonaws.com`` as a principal in the trust policy. The role must also have the following permissions: - ``s3:PutObject`` - ``s3:GetBucketLocation`` - ``s3:ListAllMyBuckets`` - ``cloudwatch:PutMetricData`` - ``logs:CreateLogGroup`` - ``logs:CreateLogStream`` - ``logs:PutLogEvents``
        :param name: The name for this canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary names. The canary name makes up part of the canary ARN, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .
        :param runtime_version: Specifies the runtime version to use for the canary. For more information about runtime versions, see `Canary Runtime Versions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html>`_ .
        :param schedule: A structure that contains information about how often the canary is to run, and when these runs are to stop.
        :param artifact_config: A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3.
        :param delete_lambda_resources_on_canary_deletion: ``AWS::Synthetics::Canary.DeleteLambdaResourcesOnCanaryDeletion``.
        :param failure_retention_period: The number of days to retain data about failed runs of this canary. If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.
        :param run_config: A structure that contains input information for a canary run. If you omit this structure, the frequency of the canary is used as canary's timeout value, up to a maximum of 900 seconds.
        :param start_canary_after_creation: Specify TRUE to have the canary start making runs immediately after it is created. A canary that you create using CloudFormation can't be used to monitor the CloudFormation stack that creates the canary or to roll back that stack if there is a failure.
        :param success_retention_period: The number of days to retain data about successful runs of this canary. If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.
        :param tags: The list of key-value pairs that are associated with the canary.
        :param visual_reference: If this canary performs visual monitoring by comparing screenshots, this structure contains the ID of the canary run to use as the baseline for screenshots, and the coordinates of any parts of the screen to ignore during the visual monitoring comparison.
        :param vpc_config: If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint. For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_synthetics as synthetics
            
            cfn_canary_props = synthetics.CfnCanaryProps(
                artifact_s3_location="artifactS3Location",
                code=synthetics.CfnCanary.CodeProperty(
                    handler="handler",
            
                    # the properties below are optional
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion",
                    script="script",
                    source_location_arn="sourceLocationArn"
                ),
                execution_role_arn="executionRoleArn",
                name="name",
                runtime_version="runtimeVersion",
                schedule=synthetics.CfnCanary.ScheduleProperty(
                    expression="expression",
            
                    # the properties below are optional
                    duration_in_seconds="durationInSeconds"
                ),
            
                # the properties below are optional
                artifact_config=synthetics.CfnCanary.ArtifactConfigProperty(
                    s3_encryption=synthetics.CfnCanary.S3EncryptionProperty(
                        encryption_mode="encryptionMode",
                        kms_key_arn="kmsKeyArn"
                    )
                ),
                delete_lambda_resources_on_canary_deletion=False,
                failure_retention_period=123,
                run_config=synthetics.CfnCanary.RunConfigProperty(
                    active_tracing=False,
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    memory_in_mb=123,
                    timeout_in_seconds=123
                ),
                start_canary_after_creation=False,
                success_retention_period=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                visual_reference=synthetics.CfnCanary.VisualReferenceProperty(
                    base_canary_run_id="baseCanaryRunId",
            
                    # the properties below are optional
                    base_screenshots=[synthetics.CfnCanary.BaseScreenshotProperty(
                        screenshot_name="screenshotName",
            
                        # the properties below are optional
                        ignore_coordinates=["ignoreCoordinates"]
                    )]
                ),
                vpc_config=synthetics.CfnCanary.VPCConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
            
                    # the properties below are optional
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01e568ae9c4e59793279a4cc2d2e157f34c50ad3155c1644f20c991c5abe45d)
            check_type(argname="argument artifact_s3_location", value=artifact_s3_location, expected_type=type_hints["artifact_s3_location"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument artifact_config", value=artifact_config, expected_type=type_hints["artifact_config"])
            check_type(argname="argument delete_lambda_resources_on_canary_deletion", value=delete_lambda_resources_on_canary_deletion, expected_type=type_hints["delete_lambda_resources_on_canary_deletion"])
            check_type(argname="argument failure_retention_period", value=failure_retention_period, expected_type=type_hints["failure_retention_period"])
            check_type(argname="argument run_config", value=run_config, expected_type=type_hints["run_config"])
            check_type(argname="argument start_canary_after_creation", value=start_canary_after_creation, expected_type=type_hints["start_canary_after_creation"])
            check_type(argname="argument success_retention_period", value=success_retention_period, expected_type=type_hints["success_retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument visual_reference", value=visual_reference, expected_type=type_hints["visual_reference"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_s3_location": artifact_s3_location,
            "code": code,
            "execution_role_arn": execution_role_arn,
            "name": name,
            "runtime_version": runtime_version,
            "schedule": schedule,
        }
        if artifact_config is not None:
            self._values["artifact_config"] = artifact_config
        if delete_lambda_resources_on_canary_deletion is not None:
            self._values["delete_lambda_resources_on_canary_deletion"] = delete_lambda_resources_on_canary_deletion
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if run_config is not None:
            self._values["run_config"] = run_config
        if start_canary_after_creation is not None:
            self._values["start_canary_after_creation"] = start_canary_after_creation
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if tags is not None:
            self._values["tags"] = tags
        if visual_reference is not None:
            self._values["visual_reference"] = visual_reference
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifact_s3_location(self) -> builtins.str:
        '''The location in Amazon S3 where Synthetics stores artifacts from the runs of this canary.

        Artifacts include the log file, screenshots, and HAR files. Specify the full location path, including ``s3://`` at the beginning of the path.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        '''
        result = self._values.get("artifact_s3_location")
        assert result is not None, "Required property 'artifact_s3_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(
        self,
    ) -> typing.Union[CfnCanary.CodeProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Use this structure to input your script code for the canary.

        This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(typing.Union[CfnCanary.CodeProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role to be used to run the canary.

        This role must already exist, and must include ``lambda.amazonaws.com`` as a principal in the trust policy. The role must also have the following permissions:

        - ``s3:PutObject``
        - ``s3:GetBucketLocation``
        - ``s3:ListAllMyBuckets``
        - ``cloudwatch:PutMetricData``
        - ``logs:CreateLogGroup``
        - ``logs:CreateLogStream``
        - ``logs:PutLogEvents``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this canary.

        Be sure to give it a descriptive name that distinguishes it from other canaries in your account.

        Do not include secrets or proprietary information in your canary names. The canary name makes up part of the canary ARN, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''Specifies the runtime version to use for the canary.

        For more information about runtime versions, see `Canary Runtime Versions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.ScheduleProperty]:
        '''A structure that contains information about how often the canary is to run, and when these runs are to stop.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.ScheduleProperty], result)

    @builtins.property
    def artifact_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.ArtifactConfigProperty]]:
        '''A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifactconfig
        '''
        result = self._values.get("artifact_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.ArtifactConfigProperty]], result)

    @builtins.property
    def delete_lambda_resources_on_canary_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Synthetics::Canary.DeleteLambdaResourcesOnCanaryDeletion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-deletelambdaresourcesoncanarydeletion
        '''
        result = self._values.get("delete_lambda_resources_on_canary_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain data about failed runs of this canary.

        If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        '''
        result = self._values.get("failure_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def run_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.RunConfigProperty]]:
        '''A structure that contains input information for a canary run.

        If you omit this structure, the frequency of the canary is used as canary's timeout value, up to a maximum of 900 seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        '''
        result = self._values.get("run_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.RunConfigProperty]], result)

    @builtins.property
    def start_canary_after_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specify TRUE to have the canary start making runs immediately after it is created.

        A canary that you create using CloudFormation can't be used to monitor the CloudFormation stack that creates the canary or to roll back that stack if there is a failure.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        '''
        result = self._values.get("start_canary_after_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain data about successful runs of this canary.

        If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        '''
        result = self._values.get("success_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The list of key-value pairs that are associated with the canary.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def visual_reference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.VisualReferenceProperty]]:
        '''If this canary performs visual monitoring by comparing screenshots, this structure contains the ID of the canary run to use as the baseline for screenshots, and the coordinates of any parts of the screen to ignore during the visual monitoring comparison.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-visualreference
        '''
        result = self._values.get("visual_reference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.VisualReferenceProperty]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.VPCConfigProperty]]:
        '''If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint.

        For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.VPCConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCanaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-synthetics.CfnGroup",
):
    '''A CloudFormation ``AWS::Synthetics::Group``.

    Creates or updates a group which you can use to associate canaries with each other, including cross-Region canaries. Using groups can help you with managing and automating your canaries, and you can also view aggregated run results and statistics for all canaries in a group.

    Groups are global resources. When you create a group, it is replicated across all AWS Regions, and you can add canaries from any Region to it, and view it in any Region. Although the group ARN format reflects the Region name where it was created, a group is not constrained to any Region. This means that you can put canaries from multiple Regions into the same group, and then use that group to view and manage all of those canaries in a single view.

    Each group can contain as many as 10 canaries. You can have as many as 20 groups in your account. Any single canary can be a member of up to 10 groups.

    :cloudformationResource: AWS::Synthetics::Group
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_synthetics as synthetics
        
        cfn_group = synthetics.CfnGroup(self, "MyCfnGroup",
            name="name",
        
            # the properties below are optional
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
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Synthetics::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the group. It can include any Unicode characters. The names for all groups in your account, across all Regions, must be unique.
        :param resource_arns: The ARNs of the canaries that you want to associate with this group.
        :param tags: The list of key-value pairs that are associated with the group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4c494132b86e0643952403d3b0f3c269e2f86d6e14c6c44bb2fa18811c7b23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(name=name, resource_arns=resource_arns, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b6b3a6a8b8bab2d6db7ea7e1dce690166cfa66ea97a76879a828d3bc6981a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__649f4e074de6516cddc1b9e3aecec585f0378b1f018989e0a7d9bbe9761eb8e2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The Id of the group.

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
        '''The list of key-value pairs that are associated with the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the group. It can include any Unicode characters.

        The names for all groups in your account, across all Regions, must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9943582c3acc44f4ac88f67539157fbd2def7c4da37817c300c20aa8d961cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the canaries that you want to associate with this group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-resourcearns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12024193668560e41eae204a5ca429e99cfce03bf4f6abbb3f5b3f39d300f920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "resource_arns": "resourceArns", "tags": "tags"},
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param name: A name for the group. It can include any Unicode characters. The names for all groups in your account, across all Regions, must be unique.
        :param resource_arns: The ARNs of the canaries that you want to associate with this group.
        :param tags: The list of key-value pairs that are associated with the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_synthetics as synthetics
            
            cfn_group_props = synthetics.CfnGroupProps(
                name="name",
            
                # the properties below are optional
                resource_arns=["resourceArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c59b38fc6e51c61173b03e4b4eddc39aa92c9b0997935d24aa385e6293f41b6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the group. It can include any Unicode characters.

        The names for all groups in your account, across all Regions, must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the canaries that you want to associate with this group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-resourcearns
        '''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The list of key-value pairs that are associated with the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-synthetics.Code"):
    '''(experimental) The code the canary should execute.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        canary = synthetics.Canary(self, "MyCanary",
            schedule=synthetics.Schedule.rate(Duration.minutes(5)),
            test=synthetics.Test.custom(
                code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
                handler="index.handler"
            ),
            runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
            environment_variables={
                "stage": "prod"
            }
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
        asset_path: builtins.str,
        *,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "AssetCode":
        '''(experimental) Specify code from a local path.

        Path must include the folder structure ``nodejs/node_modules/myCanaryFilename.js``.

        :param asset_path: Either a directory or a .zip file.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        :return: ``AssetCode`` associated with the specified path.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html#CloudWatch_Synthetics_Canaries_write_from_scratch
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cd0658ef3bce6dfb79939e118e2f8d05ab83708640fc322d62dda01bb45b56)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        options = _aws_cdk_aws_s3_assets_525817d7.AssetOptions(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            follow_symlinks=follow_symlinks,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        return typing.cast("AssetCode", jsii.sinvoke(cls, "fromAsset", [asset_path, options]))

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        key: builtins.str,
        object_version: typing.Optional[builtins.str] = None,
    ) -> "S3Code":
        '''(experimental) Specify code from an s3 bucket.

        The object in the s3 bucket must be a .zip file that contains
        the structure ``nodejs/node_modules/myCanaryFilename.js``.

        :param bucket: The S3 bucket.
        :param key: The object key.
        :param object_version: Optional S3 object version.

        :return: ``S3Code`` associated with the specified S3 object.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html#CloudWatch_Synthetics_Canaries_write_from_scratch
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42046815ab5098b26414f1d10a5f7202589894fd6fe76366e7e5798b45fcb928)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
        return typing.cast("S3Code", jsii.sinvoke(cls, "fromBucket", [bucket, key, object_version]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, code: builtins.str) -> "InlineCode":
        '''(experimental) Specify code inline.

        :param code: The actual handler code (limited to 4KiB).

        :return: ``InlineCode`` with inline code.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ddf2e6430658218e449184e4f4b6c953a4e898bd87514e74fb33dd61284e2a)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        return typing.cast("InlineCode", jsii.sinvoke(cls, "fromInline", [code]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        handler: builtins.str,
        family: "RuntimeFamily",
    ) -> "CodeConfig":
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.
        :param handler: -
        :param family: -

        :return: a bound ``CodeConfig``.

        :stability: experimental
        '''
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        handler: builtins.str,
        family: "RuntimeFamily",
    ) -> "CodeConfig":
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.
        :param handler: -
        :param family: -

        :return: a bound ``CodeConfig``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d41022d8b7a9aea2218074a7cbda64b43c2d1c0401afe2176e44dfa43ebf7a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
        return typing.cast("CodeConfig", jsii.invoke(self, "bind", [scope, handler, family]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Code).__jsii_proxy_class__ = lambda : _CodeProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={"inline_code": "inlineCode", "s3_location": "s3Location"},
)
class CodeConfig:
    def __init__(
        self,
        *,
        inline_code: typing.Optional[builtins.str] = None,
        s3_location: typing.Optional[typing.Union[_aws_cdk_aws_s3_55f001a5.Location, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Configuration of the code class.

        :param inline_code: (experimental) Inline code (mutually exclusive with ``s3Location``). Default: - none
        :param s3_location: (experimental) The location of the code in S3 (mutually exclusive with ``inlineCode``). Default: - none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_synthetics as synthetics
            
            code_config = synthetics.CodeConfig(
                inline_code="inlineCode",
                s3_location=Location(
                    bucket_name="bucketName",
                    object_key="objectKey",
            
                    # the properties below are optional
                    object_version="objectVersion"
                )
            )
        '''
        if isinstance(s3_location, dict):
            s3_location = _aws_cdk_aws_s3_55f001a5.Location(**s3_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681d723e6dd5f8631dc74080fdba0a665b0c97ed6f7400ba0960ca30104b98ff)
            check_type(argname="argument inline_code", value=inline_code, expected_type=type_hints["inline_code"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if s3_location is not None:
            self._values["s3_location"] = s3_location

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) Inline code (mutually exclusive with ``s3Location``).

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_location(self) -> typing.Optional[_aws_cdk_aws_s3_55f001a5.Location]:
        '''(experimental) The location of the code in S3 (mutually exclusive with ``inlineCode``).

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("s3_location")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_55f001a5.Location], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
    },
)
class CronOptions:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: (experimental) The day of the month to run this rule at. Default: - Every day of the month
        :param hour: (experimental) The hour to run this rule at. Default: - Every hour
        :param minute: (experimental) The minute to run this rule at. Default: - Every minute
        :param month: (experimental) The month to run this rule at. Default: - Every month
        :param week_day: (experimental) The day of the week to run this rule at. Default: - Any day of the week

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_cron.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            schedule = synthetics.Schedule.cron(
                hour="0,8,16"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de56190a42d444ca316ba91754f7f8360f07e4e5b71c2787557f5735ef00466)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''(experimental) The day of the month to run this rule at.

        :default: - Every day of the month

        :stability: experimental
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hour to run this rule at.

        :default: - Every hour

        :stability: experimental
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''(experimental) The minute to run this rule at.

        :default: - Every minute

        :stability: experimental
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''(experimental) The month to run this rule at.

        :default: - Every month

        :stability: experimental
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''(experimental) The day of the week to run this rule at.

        :default: - Any day of the week

        :stability: experimental
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-synthetics.CustomTestOptions",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "handler": "handler"},
)
class CustomTestOptions:
    def __init__(self, *, code: Code, handler: builtins.str) -> None:
        '''(experimental) Properties for specifying a test.

        :param code: (experimental) The code of the canary script.
        :param handler: (experimental) The handler for the code. Must end with ``.handler``.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            canary = synthetics.Canary(self, "MyCanary",
                schedule=synthetics.Schedule.rate(Duration.minutes(5)),
                test=synthetics.Test.custom(
                    code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
                    handler="index.handler"
                ),
                runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
                environment_variables={
                    "stage": "prod"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c735339adabc0f51183684af5cecc5e5264be6623fcc7cf026425be48b946e)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code": code,
            "handler": handler,
        }

    @builtins.property
    def code(self) -> Code:
        '''(experimental) The code of the canary script.

        :stability: experimental
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''(experimental) The handler for the code.

        Must end with ``.handler``.

        :stability: experimental
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomTestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InlineCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-synthetics.InlineCode",
):
    '''(experimental) Canary code from an inline string.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_synthetics as synthetics
        
        inline_code = synthetics.InlineCode("code")
    '''

    def __init__(self, code: builtins.str) -> None:
        '''
        :param code: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e2ab9f3c4d97ac64503c8b6cfa4bd0a4f9b0e7e270f60572b7ffb1b8c143ec)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        jsii.create(self.__class__, self, [code])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        handler: builtins.str,
        _family: "RuntimeFamily",
    ) -> CodeConfig:
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -
        :param handler: -
        :param _family: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a334b0268e9378b2d1df831deb28e858711481ff55e36b30bb4bca1d948e00ef)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument _family", value=_family, expected_type=type_hints["_family"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [_scope, handler, _family]))


class Runtime(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-synthetics.Runtime"):
    '''(experimental) Runtime options for a canary.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        canary = synthetics.Canary(self, "MyCanary",
            schedule=synthetics.Schedule.rate(Duration.minutes(5)),
            test=synthetics.Test.custom(
                code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
                handler="index.handler"
            ),
            runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
            environment_variables={
                "stage": "prod"
            }
        )
    '''

    def __init__(self, name: builtins.str, family: "RuntimeFamily") -> None:
        '''
        :param name: The name of the runtime version.
        :param family: The Lambda runtime family.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2019c79b83a886dee3b4830c46526f8f1e0cdfa6ce4857825d8d239ed57c0d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
        jsii.create(self.__class__, self, [name, family])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_1_0")
    def SYNTHETICS_1_0(cls) -> "Runtime":
        '''(experimental) **Deprecated by AWS Synthetics. You can't create canaries with deprecated runtimes.**.

        ``syn-1.0`` includes the following:

        - Synthetics library 1.0
        - Synthetics handler code 1.0
        - Lambda runtime Node.js 10.x
        - Puppeteer-core version 1.14.0
        - The Chromium version that matches Puppeteer-core 1.14.0

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-1.0
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_2_0")
    def SYNTHETICS_NODEJS_2_0(cls) -> "Runtime":
        '''(experimental) **Deprecated by AWS Synthetics. You can't create canaries with deprecated runtimes.**.

        ``syn-nodejs-2.0`` includes the following:

        - Lambda runtime Node.js 10.x
        - Puppeteer-core version 3.3.0
        - Chromium version 83.0.4103.0

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-2.0
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_2_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_2_1")
    def SYNTHETICS_NODEJS_2_1(cls) -> "Runtime":
        '''(experimental) **Deprecated by AWS Synthetics. You can't create canaries with deprecated runtimes.**.

        ``syn-nodejs-2.1`` includes the following:

        - Lambda runtime Node.js 10.x
        - Puppeteer-core version 3.3.0
        - Chromium version 83.0.4103.0

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-2.1
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_2_2")
    def SYNTHETICS_NODEJS_2_2(cls) -> "Runtime":
        '''(experimental) **Deprecated by AWS Synthetics. You can't create canaries with deprecated runtimes.**.

        ``syn-nodejs-2.2`` includes the following:

        - Lambda runtime Node.js 10.x
        - Puppeteer-core version 3.3.0
        - Chromium version 83.0.4103.0

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-2.2
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_2_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_0")
    def SYNTHETICS_NODEJS_PUPPETEER_3_0(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.0`` includes the following: - Lambda runtime Node.js 12.x - Puppeteer-core version 5.5.0 - Chromium version 88.0.4298.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.0
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_1")
    def SYNTHETICS_NODEJS_PUPPETEER_3_1(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.1`` includes the following: - Lambda runtime Node.js 12.x - Puppeteer-core version 5.5.0 - Chromium version 88.0.4298.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.1
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_2")
    def SYNTHETICS_NODEJS_PUPPETEER_3_2(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.2`` includes the following: - Lambda runtime Node.js 12.x - Puppeteer-core version 5.5.0 - Chromium version 88.0.4298.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.2
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_3")
    def SYNTHETICS_NODEJS_PUPPETEER_3_3(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.3`` includes the following: - Lambda runtime Node.js 12.x - Puppeteer-core version 5.5.0 - Chromium version 88.0.4298.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.3
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_4")
    def SYNTHETICS_NODEJS_PUPPETEER_3_4(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.4`` includes the following: - Lambda runtime Node.js 12.x - Puppeteer-core version 5.5.0 - Chromium version 88.0.4298.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.4
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_5")
    def SYNTHETICS_NODEJS_PUPPETEER_3_5(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.5`` includes the following: - Lambda runtime Node.js 14.x - Puppeteer-core version 10.1.0 - Chromium version 92.0.4512.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.5
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_PYTHON_SELENIUM_1_0")
    def SYNTHETICS_PYTHON_SELENIUM_1_0(cls) -> "Runtime":
        '''(experimental) ``syn-python-selenium-1.0`` includes the following: - Lambda runtime Python 3.8 - Selenium version 3.141.0 - Chromium version 83.0.4103.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_python_selenium.html
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_PYTHON_SELENIUM_1_0"))

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> "RuntimeFamily":
        '''(experimental) The Lambda runtime family.

        :stability: experimental
        '''
        return typing.cast("RuntimeFamily", jsii.get(self, "family"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the runtime version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.enum(jsii_type="@aws-cdk/aws-synthetics.RuntimeFamily")
class RuntimeFamily(enum.Enum):
    '''(experimental) All known Lambda runtime families.

    :stability: experimental
    '''

    NODEJS = "NODEJS"
    '''(experimental) All Lambda runtimes that depend on Node.js.

    :stability: experimental
    '''
    PYTHON = "PYTHON"
    '''(experimental) All lambda runtimes that depend on Python.

    :stability: experimental
    '''
    OTHER = "OTHER"
    '''(experimental) Any future runtime family.

    :stability: experimental
    '''


class S3Code(Code, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-synthetics.S3Code"):
    '''(experimental) S3 bucket path to the code zip file.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3 as s3
        import aws_cdk.aws_synthetics as synthetics
        
        # bucket: s3.Bucket
        
        s3_code = synthetics.S3Code(bucket, "key", "objectVersion")
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        key: builtins.str,
        object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: -
        :param key: -
        :param object_version: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7eaef8b0e512fc5b06f27cbb380416666c89ce6fdb0049353cbc6a5e57fd9ae)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
        jsii.create(self.__class__, self, [bucket, key, object_version])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        _handler: builtins.str,
        _family: RuntimeFamily,
    ) -> CodeConfig:
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -
        :param _handler: -
        :param _family: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5752eabbb0486b844aaaafe832ebc037f4e1c3a63b094895098138aef46fe083)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _handler", value=_handler, expected_type=type_hints["_handler"])
            check_type(argname="argument _family", value=_family, expected_type=type_hints["_family"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [_scope, _handler, _family]))


class Schedule(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-synthetics.Schedule"):
    '''(experimental) Schedule for canary runs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        schedule = synthetics.Schedule.rate(Duration.minutes(5))
    '''

    @jsii.member(jsii_name="cron")
    @builtins.classmethod
    def cron(
        cls,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> "Schedule":
        '''(experimental) Create a schedule from a set of cron fields.

        :param day: (experimental) The day of the month to run this rule at. Default: - Every day of the month
        :param hour: (experimental) The hour to run this rule at. Default: - Every hour
        :param minute: (experimental) The minute to run this rule at. Default: - Every minute
        :param month: (experimental) The month to run this rule at. Default: - Every month
        :param week_day: (experimental) The day of the week to run this rule at. Default: - Any day of the week

        :stability: experimental
        '''
        options = CronOptions(
            day=day, hour=hour, minute=minute, month=month, week_day=week_day
        )

        return typing.cast("Schedule", jsii.sinvoke(cls, "cron", [options]))

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(cls, expression: builtins.str) -> "Schedule":
        '''(experimental) Construct a schedule from a literal schedule expression.

        The expression must be in a ``rate(number units)`` format.
        For example, ``Schedule.expression('rate(10 minutes)')``

        :param expression: The expression to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8857a0ca3e5cbf31df6690f9bf857c0d5145f5712443410239144f5a7f62d6)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast("Schedule", jsii.sinvoke(cls, "expression", [expression]))

    @jsii.member(jsii_name="once")
    @builtins.classmethod
    def once(cls) -> "Schedule":
        '''(experimental) The canary will be executed once.

        :stability: experimental
        '''
        return typing.cast("Schedule", jsii.sinvoke(cls, "once", []))

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, interval: _aws_cdk_core_f4b25747.Duration) -> "Schedule":
        '''(experimental) Construct a schedule from an interval.

        Allowed values: 0 (for a single run) or between 1 and 60 minutes.
        To specify a single run, you can use ``Schedule.once()``.

        :param interval: The interval at which to run the canary.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23fcb589eb4697ba34685df0abbd8cbd5efa349f625190d487607c10a5b984e)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
        return typing.cast("Schedule", jsii.sinvoke(cls, "rate", [interval]))

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        '''(experimental) The Schedule expression.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "expressionString"))


class Test(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-synthetics.Test"):
    '''(experimental) Specify a test that the canary should run.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        canary = synthetics.Canary(self, "MyCanary",
            schedule=synthetics.Schedule.rate(Duration.minutes(5)),
            test=synthetics.Test.custom(
                code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
                handler="index.handler"
            ),
            runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_1,
            environment_variables={
                "stage": "prod"
            }
        )
    '''

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, *, code: Code, handler: builtins.str) -> "Test":
        '''(experimental) Specify a custom test with your own code.

        :param code: (experimental) The code of the canary script.
        :param handler: (experimental) The handler for the code. Must end with ``.handler``.

        :return: ``Test`` associated with the specified Code object

        :stability: experimental
        '''
        options = CustomTestOptions(code=code, handler=handler)

        return typing.cast("Test", jsii.sinvoke(cls, "custom", [options]))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> Code:
        '''(experimental) The code that the canary should run.

        :stability: experimental
        '''
        return typing.cast(Code, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        '''(experimental) The handler of the canary.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "handler"))


class AssetCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-synthetics.AssetCode",
):
    '''(experimental) Canary code from an Asset.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.assets as assets
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_synthetics as synthetics
        import aws_cdk.core as cdk
        
        # docker_image: cdk.DockerImage
        # grantable: iam.IGrantable
        # local_bundling: cdk.ILocalBundling
        
        asset_code = synthetics.AssetCode("assetPath",
            asset_hash="assetHash",
            asset_hash_type=cdk.AssetHashType.SOURCE,
            bundling=cdk.BundlingOptions(
                image=docker_image,
        
                # the properties below are optional
                command=["command"],
                entrypoint=["entrypoint"],
                environment={
                    "environment_key": "environment"
                },
                local=local_bundling,
                output_type=cdk.BundlingOutput.ARCHIVED,
                security_opt="securityOpt",
                user="user",
                volumes=[cdk.DockerVolume(
                    container_path="containerPath",
                    host_path="hostPath",
        
                    # the properties below are optional
                    consistency=cdk.DockerVolumeConsistency.CONSISTENT
                )],
                working_directory="workingDirectory"
            ),
            exclude=["exclude"],
            follow=assets.FollowMode.NEVER,
            follow_symlinks=cdk.SymlinkFollowMode.NEVER,
            ignore_mode=cdk.IgnoreMode.GLOB,
            readers=[grantable],
            source_hash="sourceHash"
        )
    '''

    def __init__(
        self,
        asset_path: builtins.str,
        *,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param asset_path: The path to the asset file or directory.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264fc066889d14fbf1e9a7b26fde1708308bfc04cadb600b87d345bc7f757594)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        options = _aws_cdk_aws_s3_assets_525817d7.AssetOptions(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            follow_symlinks=follow_symlinks,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        jsii.create(self.__class__, self, [asset_path, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        handler: builtins.str,
        family: RuntimeFamily,
    ) -> CodeConfig:
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -
        :param handler: -
        :param family: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dca6ed88b55729f321dfcb7807facc4245f1f40789450a80b00c2d390275de2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [scope, handler, family]))


__all__ = [
    "ArtifactsBucketLocation",
    "AssetCode",
    "Canary",
    "CanaryProps",
    "CfnCanary",
    "CfnCanaryProps",
    "CfnGroup",
    "CfnGroupProps",
    "Code",
    "CodeConfig",
    "CronOptions",
    "CustomTestOptions",
    "InlineCode",
    "Runtime",
    "RuntimeFamily",
    "S3Code",
    "Schedule",
    "Test",
]

publication.publish()

def _typecheckingstub__877fe1a8370a2771d3c0c74a66a087e021a140579a0ad46a2b32a6044fea341d(
    *,
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f49d4729949041ace80ae655c099ecea6783cb4e1a45eafccb490375484c289(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    runtime: Runtime,
    test: Test,
    artifacts_bucket_location: typing.Optional[typing.Union[ArtifactsBucketLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    canary_name: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    failure_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    schedule: typing.Optional[Schedule] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    start_after_creation: typing.Optional[builtins.bool] = None,
    success_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    time_to_live: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebafcf9877ad731ac6cdd4e7c1c45bfc4eeb3322e90b5560353937b8375d2a1e(
    *,
    runtime: Runtime,
    test: Test,
    artifacts_bucket_location: typing.Optional[typing.Union[ArtifactsBucketLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    canary_name: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    failure_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    schedule: typing.Optional[Schedule] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    start_after_creation: typing.Optional[builtins.bool] = None,
    success_retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    time_to_live: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8adb76158ebc83b0e1114879c773192d0b987275745c58d9e44e2e547f9cc79b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    artifact_s3_location: builtins.str,
    code: typing.Union[typing.Union[CfnCanary.CodeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    execution_role_arn: builtins.str,
    name: builtins.str,
    runtime_version: builtins.str,
    schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
    artifact_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.ArtifactConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delete_lambda_resources_on_canary_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    failure_retention_period: typing.Optional[jsii.Number] = None,
    run_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.RunConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_canary_after_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    success_retention_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    visual_reference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.VisualReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.VPCConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e7672cdc2990df45da2ebf445293f028723a1bc56a4f41407bd45b114772c5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c03f5e2e0aca65aebc755a1c1cb707fdd6b46774d1c954b7951797e1d71705(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535213fe8f968723001256a27edd42fa6dd0e8a45b28dc94d3a644af5076c394(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d7a99cfe8b521f0c4ac94d0db162ff438ff9648a7449498c6f3dc20d118d36(
    value: typing.Union[CfnCanary.CodeProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36aac1db5e6a1b7d5d8c7fbfbf993e7d19fed69de2e0b9b337e5bddf4555ecd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c2130db4ee16f96fb4ff26768c14064c808f2b82ea94847c42a0a2f50aac14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beced46adface6ec3f552c6c926c43fc7aca6273c69be0f74b4ae15ac22090ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200920497c576a0714b3e81084b3097516d06d18f875245fd9d50a50ffad6089(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.ScheduleProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a721db6f2b790e8ff7639352297bfc87af12f89bdc2baff8d7f1184a8d08f8a3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.ArtifactConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5649c4dd679377bec144797abccb50b8000bda7684a7ca2400378427836edc(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4d40163b2c8524be72914366407a0636f998549468b56820f395779614de76(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7049326db3bb14eae2c879160ce1d9d0ba5c7149398e8088e2d2ae37a1f8b06(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.RunConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c227e49ceab6691d49923513c8dc66343c93fa052b8689e29f9338eca25054d(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8190a74f8342b5846739ef45bcbdf13162302b8f74e8ab2344fc8f19b1427714(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23813ba279d0d20bcaf3c590c4e427e68413ebe83bd169b8866ed020648c2498(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.VisualReferenceProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb14178cad2226bf0714354dd4592b585625e7923ef8e74edfee7f85dd489ac(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCanary.VPCConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7de815bbfd8bd4c122f0890398a37b17f5260ecc3b84d1fd58bff1c8eb0e43(
    *,
    s3_encryption: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.S3EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e972da934c239df7dafdca862e9ad38ec1553fcdbbf43ed3a10e86bfebc1a7b(
    *,
    screenshot_name: builtins.str,
    ignore_coordinates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475dbe17c4645b87a88a4cdd642e9f5239af9cf2521f616ac1f1448fbc4fff4f(
    *,
    handler: builtins.str,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
    source_location_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97afdec6d5442f1925fbce72bd8ff5b2ffc1cbed4c8aa317e745e90de4444d98(
    *,
    active_tracing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    memory_in_mb: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe623c6e242fced46173ae729e5ea6ad500587f3b65658e118512b527073907(
    *,
    encryption_mode: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2f10f4b095b130c13b16b9e6f81f513954e9a7bdeb3ac5af152e08a910780c(
    *,
    expression: builtins.str,
    duration_in_seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dee073365f82e9388517797b106c20f61a60398a204c75fe53c4ecb51ed09a(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fc0614ac0703546d147773c7deb4a60ce2b6a4910fbd8a117601591d44c6d9(
    *,
    base_canary_run_id: builtins.str,
    base_screenshots: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.BaseScreenshotProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01e568ae9c4e59793279a4cc2d2e157f34c50ad3155c1644f20c991c5abe45d(
    *,
    artifact_s3_location: builtins.str,
    code: typing.Union[typing.Union[CfnCanary.CodeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    execution_role_arn: builtins.str,
    name: builtins.str,
    runtime_version: builtins.str,
    schedule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
    artifact_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.ArtifactConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delete_lambda_resources_on_canary_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    failure_retention_period: typing.Optional[jsii.Number] = None,
    run_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.RunConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_canary_after_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    success_retention_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    visual_reference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.VisualReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCanary.VPCConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4c494132b86e0643952403d3b0f3c269e2f86d6e14c6c44bb2fa18811c7b23(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b6b3a6a8b8bab2d6db7ea7e1dce690166cfa66ea97a76879a828d3bc6981a6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649f4e074de6516cddc1b9e3aecec585f0378b1f018989e0a7d9bbe9761eb8e2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9943582c3acc44f4ac88f67539157fbd2def7c4da37817c300c20aa8d961cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12024193668560e41eae204a5ca429e99cfce03bf4f6abbb3f5b3f39d300f920(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c59b38fc6e51c61173b03e4b4eddc39aa92c9b0997935d24aa385e6293f41b6(
    *,
    name: builtins.str,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cd0658ef3bce6dfb79939e118e2f8d05ab83708640fc322d62dda01bb45b56(
    asset_path: builtins.str,
    *,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
    source_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42046815ab5098b26414f1d10a5f7202589894fd6fe76366e7e5798b45fcb928(
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    key: builtins.str,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ddf2e6430658218e449184e4f4b6c953a4e898bd87514e74fb33dd61284e2a(
    code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d41022d8b7a9aea2218074a7cbda64b43c2d1c0401afe2176e44dfa43ebf7a1(
    scope: _constructs_77d1e7e8.Construct,
    handler: builtins.str,
    family: RuntimeFamily,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681d723e6dd5f8631dc74080fdba0a665b0c97ed6f7400ba0960ca30104b98ff(
    *,
    inline_code: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[typing.Union[_aws_cdk_aws_s3_55f001a5.Location, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de56190a42d444ca316ba91754f7f8360f07e4e5b71c2787557f5735ef00466(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c735339adabc0f51183684af5cecc5e5264be6623fcc7cf026425be48b946e(
    *,
    code: Code,
    handler: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e2ab9f3c4d97ac64503c8b6cfa4bd0a4f9b0e7e270f60572b7ffb1b8c143ec(
    code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a334b0268e9378b2d1df831deb28e858711481ff55e36b30bb4bca1d948e00ef(
    _scope: _constructs_77d1e7e8.Construct,
    handler: builtins.str,
    _family: RuntimeFamily,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2019c79b83a886dee3b4830c46526f8f1e0cdfa6ce4857825d8d239ed57c0d(
    name: builtins.str,
    family: RuntimeFamily,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7eaef8b0e512fc5b06f27cbb380416666c89ce6fdb0049353cbc6a5e57fd9ae(
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    key: builtins.str,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5752eabbb0486b844aaaafe832ebc037f4e1c3a63b094895098138aef46fe083(
    _scope: _constructs_77d1e7e8.Construct,
    _handler: builtins.str,
    _family: RuntimeFamily,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8857a0ca3e5cbf31df6690f9bf857c0d5145f5712443410239144f5a7f62d6(
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23fcb589eb4697ba34685df0abbd8cbd5efa349f625190d487607c10a5b984e(
    interval: _aws_cdk_core_f4b25747.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264fc066889d14fbf1e9a7b26fde1708308bfc04cadb600b87d345bc7f757594(
    asset_path: builtins.str,
    *,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
    source_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dca6ed88b55729f321dfcb7807facc4245f1f40789450a80b00c2d390275de2(
    scope: _constructs_77d1e7e8.Construct,
    handler: builtins.str,
    family: RuntimeFamily,
) -> None:
    """Type checking stubs"""
    pass
