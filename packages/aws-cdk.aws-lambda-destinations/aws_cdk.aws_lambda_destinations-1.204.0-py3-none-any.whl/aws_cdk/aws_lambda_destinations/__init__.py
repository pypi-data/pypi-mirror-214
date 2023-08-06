'''
# Amazon Lambda Destinations Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This library provides constructs for adding destinations to a Lambda function.
Destinations can be added by specifying the `onFailure` or `onSuccess` props when creating a function or alias.

## Destinations

The following destinations are supported

* Lambda function
* SQS queue - Only standard SQS queues are supported for failure destinations, FIFO queues are not supported.
* SNS topic
* EventBridge event bus

Example with a SNS topic for successful invocations:

```python
# An sns topic for successful invocations of a lambda function
import aws_cdk.aws_sns as sns


my_topic = sns.Topic(self, "Topic")

my_fn = lambda_.Function(self, "Fn",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
    # sns topic for successful invocations
    on_success=destinations.SnsDestination(my_topic)
)
```

Example with a SQS queue for unsuccessful invocations:

```python
# An sqs queue for unsuccessful invocations of a lambda function
import aws_cdk.aws_sqs as sqs


dead_letter_queue = sqs.Queue(self, "DeadLetterQueue")

my_fn = lambda_.Function(self, "Fn",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("// your code"),
    # sqs queue for unsuccessful invocations
    on_failure=destinations.SqsDestination(dead_letter_queue)
)
```

See also [Configuring Destinations for Asynchronous Invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-async-destinations).

### Invocation record

When a lambda function is configured with a destination, an invocation record is created by the Lambda service
when the lambda function completes. The invocation record contains the details of the function, its context, and
the request and response payloads.

The following example shows the format of the invocation record for a successful invocation:

```json
{
	"version": "1.0",
	"timestamp": "2019-11-24T23:08:25.651Z",
	"requestContext": {
		"requestId": "c2a6f2ae-7dbb-4d22-8782-d0485c9877e2",
		"functionArn": "arn:aws:lambda:sa-east-1:123456789123:function:event-destinations:$LATEST",
		"condition": "Success",
		"approximateInvokeCount": 1
	},
	"requestPayload": {
		"Success": true
	},
	"responseContext": {
		"statusCode": 200,
		"executedVersion": "$LATEST"
	},
	"responsePayload": "<data returned by the function here>"
}
```

In case of failure, the record contains the reason and error object:

```json
{
  "version": "1.0",
  "timestamp": "2019-11-24T21:52:47.333Z",
  "requestContext": {
    "requestId": "8ea123e4-1db7-4aca-ad10-d9ca1234c1fd",
    "functionArn": "arn:aws:lambda:sa-east-1:123456678912:function:event-destinations:$LATEST",
    "condition": "RetriesExhausted",
    "approximateInvokeCount": 3
  },
  "requestPayload": {
    "Success": false
  },
  "responseContext": {
    "statusCode": 200,
    "executedVersion": "$LATEST",
    "functionError": "Handled"
  },
  "responsePayload": {
    "errorMessage": "Failure from event, Success = false, I am failing!",
    "errorType": "Error",
    "stackTrace": [ "exports.handler (/var/task/index.js:18:18)" ]
  }
}
```

#### Destination-specific JSON format

* For SNS/SQS (`SnsDestionation`/`SqsDestination`), the invocation record JSON is passed as the `Message` to the destination.
* For Lambda (`LambdaDestination`), the invocation record JSON is passed as the payload to the function.
* For EventBridge (`EventBridgeDestination`), the invocation record JSON is passed as the `detail` in the PutEvents call.
  The value for the event field `source` is `lambda`, and the value for the event field `detail-type`
  is either 'Lambda Function Invocation Result - Success' or 'Lambda Function Invocation Result – Failure',
  depending on whether the lambda function invocation succeeded or failed. The event field `resource`
  contains the function and destination ARNs. See [AWS Events](https://docs.aws.amazon.com/eventbridge/latest/userguide/aws-events.html)
  for the different event fields.

### Auto-extract response payload with lambda destination

The `responseOnly` option of `LambdaDestination` allows to auto-extract the response payload from the
invocation record:

```python
# Auto-extract response payload with a lambda destination
# destination_fn: lambda.Function


source_fn = lambda_.Function(self, "Source",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
    # auto-extract on success
    on_success=destinations.LambdaDestination(destination_fn,
        response_only=True
    )
)
```

In the above example, `destinationFn` will be invoked with the payload returned by `sourceFn`
(`responsePayload` in the invocation record, not the full record).

When used with `onFailure`, the destination function is invoked with the error object returned
by the source function.

Using the `responseOnly` option allows to easily chain asynchronous Lambda functions without
having to deal with data extraction in the runtime code.
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

import aws_cdk.aws_events as _aws_cdk_aws_events_efcdfa54
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.aws_sns as _aws_cdk_aws_sns_889c7272
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_48bffef9
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IDestination)
class EventBridgeDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-destinations.EventBridgeDestination",
):
    '''Use an Event Bridge event bus as a Lambda destination.

    If no event bus is specified, the default event bus is used.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_events as events
        import aws_cdk.aws_lambda_destinations as lambda_destinations
        
        # event_bus: events.EventBus
        
        event_bridge_destination = lambda_destinations.EventBridgeDestination(event_bus)
    '''

    def __init__(
        self,
        event_bus: typing.Optional[_aws_cdk_aws_events_efcdfa54.IEventBus] = None,
    ) -> None:
        '''
        :param event_bus: -

        :default: - use the default event bus
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d77b070a2d9267867221ab50ebfcdfd2b21136bd87cc55766a6dbad80bfd8f1)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
        jsii.create(self.__class__, self, [event_bus])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
    ) -> _aws_cdk_aws_lambda_5443dbc3.DestinationConfig:
        '''Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: The destination type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea87252c682d172a9ca2c534b6db808040d39d85f88925e60955c7570adf427d)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        _options = _aws_cdk_aws_lambda_5443dbc3.DestinationOptions(type=type)

        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.DestinationConfig, jsii.invoke(self, "bind", [_scope, fn, _options]))


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IDestination)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-destinations.LambdaDestination",
):
    '''Use a Lambda function as a Lambda destination.

    :exampleMetadata: infused

    Example::

        # Auto-extract response payload with a lambda destination
        # destination_fn: lambda.Function
        
        
        source_fn = lambda_.Function(self, "Source",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            # auto-extract on success
            on_success=destinations.LambdaDestination(destination_fn,
                response_only=True
            )
        )
    '''

    def __init__(
        self,
        fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        response_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param fn: -
        :param response_only: Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d75ef8c020ab307fe7892562f36bc2ec57c2598d7710ad53ba92243005a420)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        options = LambdaDestinationOptions(response_only=response_only)

        jsii.create(self.__class__, self, [fn, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
    ) -> _aws_cdk_aws_lambda_5443dbc3.DestinationConfig:
        '''Returns a destination configuration.

        :param scope: -
        :param fn: -
        :param type: The destination type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1cd88de5194ac2badcbd923b7a82975ed72ddf4fbac65037963c3ab3f4932a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        options = _aws_cdk_aws_lambda_5443dbc3.DestinationOptions(type=type)

        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.DestinationConfig, jsii.invoke(self, "bind", [scope, fn, options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lambda-destinations.LambdaDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={"response_only": "responseOnly"},
)
class LambdaDestinationOptions:
    def __init__(self, *, response_only: typing.Optional[builtins.bool] = None) -> None:
        '''Options for a Lambda destination.

        :param response_only: Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        :exampleMetadata: infused

        Example::

            # Auto-extract response payload with a lambda destination
            # destination_fn: lambda.Function
            
            
            source_fn = lambda_.Function(self, "Source",
                runtime=lambda_.Runtime.NODEJS_14_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                # auto-extract on success
                on_success=destinations.LambdaDestination(destination_fn,
                    response_only=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fa5ad84fb9a007d11e447d85048ed485ae5153cc3b89c93416713145625788)
            check_type(argname="argument response_only", value=response_only, expected_type=type_hints["response_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if response_only is not None:
            self._values["response_only"] = response_only

    @builtins.property
    def response_only(self) -> typing.Optional[builtins.bool]:
        '''Whether the destination function receives only the ``responsePayload`` of the source function.

        When set to ``true`` and used as ``onSuccess`` destination, the destination
        function will be invoked with the payload returned by the source function.

        When set to ``true`` and used as ``onFailure`` destination, the destination
        function will be invoked with the error object returned by source function.

        See the README of this module to see a full explanation of this option.

        :default: false The destination function receives the full invocation record.
        '''
        result = self._values.get("response_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IDestination)
class SnsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-destinations.SnsDestination",
):
    '''Use a SNS topic as a Lambda destination.

    :exampleMetadata: infused

    Example::

        # An sns topic for successful invocations of a lambda function
        import aws_cdk.aws_sns as sns
        
        
        my_topic = sns.Topic(self, "Topic")
        
        my_fn = lambda_.Function(self, "Fn",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            # sns topic for successful invocations
            on_success=destinations.SnsDestination(my_topic)
        )
    '''

    def __init__(self, topic: _aws_cdk_aws_sns_889c7272.ITopic) -> None:
        '''
        :param topic: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c3959b4f9bd3dd154c04d6b7fae32d01160e5c877080b1f3ea76391c523394)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
    ) -> _aws_cdk_aws_lambda_5443dbc3.DestinationConfig:
        '''Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: The destination type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a19fae8a77ce7bfe0f7ba8783f669cfc226b5715e83edc0a2cbc537f6c4aec)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        _options = _aws_cdk_aws_lambda_5443dbc3.DestinationOptions(type=type)

        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.DestinationConfig, jsii.invoke(self, "bind", [_scope, fn, _options]))


@jsii.implements(_aws_cdk_aws_lambda_5443dbc3.IDestination)
class SqsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lambda-destinations.SqsDestination",
):
    '''Use a SQS queue as a Lambda destination.

    :exampleMetadata: infused

    Example::

        # An sqs queue for unsuccessful invocations of a lambda function
        import aws_cdk.aws_sqs as sqs
        
        
        dead_letter_queue = sqs.Queue(self, "DeadLetterQueue")
        
        my_fn = lambda_.Function(self, "Fn",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("// your code"),
            # sqs queue for unsuccessful invocations
            on_failure=destinations.SqsDestination(dead_letter_queue)
        )
    '''

    def __init__(self, queue: _aws_cdk_aws_sqs_48bffef9.IQueue) -> None:
        '''
        :param queue: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4ac9efb142c0e85c91fce31090fb080a76ff7e3ed78e15953efb07a41bf004)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        jsii.create(self.__class__, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
    ) -> _aws_cdk_aws_lambda_5443dbc3.DestinationConfig:
        '''Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: The destination type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741e28ea5ee8d87fae0e40d8ffb319912cc80cef8f6613eb5cd7695662d0ec1f)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        _options = _aws_cdk_aws_lambda_5443dbc3.DestinationOptions(type=type)

        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.DestinationConfig, jsii.invoke(self, "bind", [_scope, fn, _options]))


__all__ = [
    "EventBridgeDestination",
    "LambdaDestination",
    "LambdaDestinationOptions",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()

def _typecheckingstub__7d77b070a2d9267867221ab50ebfcdfd2b21136bd87cc55766a6dbad80bfd8f1(
    event_bus: typing.Optional[_aws_cdk_aws_events_efcdfa54.IEventBus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea87252c682d172a9ca2c534b6db808040d39d85f88925e60955c7570adf427d(
    _scope: _aws_cdk_core_f4b25747.Construct,
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d75ef8c020ab307fe7892562f36bc2ec57c2598d7710ad53ba92243005a420(
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    response_only: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1cd88de5194ac2badcbd923b7a82975ed72ddf4fbac65037963c3ab3f4932a(
    scope: _aws_cdk_core_f4b25747.Construct,
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fa5ad84fb9a007d11e447d85048ed485ae5153cc3b89c93416713145625788(
    *,
    response_only: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c3959b4f9bd3dd154c04d6b7fae32d01160e5c877080b1f3ea76391c523394(
    topic: _aws_cdk_aws_sns_889c7272.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a19fae8a77ce7bfe0f7ba8783f669cfc226b5715e83edc0a2cbc537f6c4aec(
    _scope: _aws_cdk_core_f4b25747.Construct,
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4ac9efb142c0e85c91fce31090fb080a76ff7e3ed78e15953efb07a41bf004(
    queue: _aws_cdk_aws_sqs_48bffef9.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741e28ea5ee8d87fae0e40d8ffb319912cc80cef8f6613eb5cd7695662d0ec1f(
    _scope: _aws_cdk_core_f4b25747.Construct,
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    type: _aws_cdk_aws_lambda_5443dbc3.DestinationType,
) -> None:
    """Type checking stubs"""
    pass
