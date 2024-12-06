r'''
# TokenInjectableDockerBuilder

The `TokenInjectableDockerBuilder` is a flexible AWS CDK construct that enables the usage of AWS CDK tokens in the building, pushing, and deployment of Docker images to Amazon Elastic Container Registry (ECR). It leverages AWS CodeBuild and Lambda custom resources.

---


## Why?

AWS CDK already provides mechanisms for creating deployable assets using Docker, such as [DockerImageAsset](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ecr_assets.DockerImageAsset.html) and [DockerImageCode](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.DockerImageCode.html), but these Constructs are limited because they cannot accept CDK tokens as build-args. The `TokenInjectableDockerBuilder` allows injecting CDK tokens as build-time arguments into Docker-based assets, enabling more dynamic dependency relationships.

For example, a Next.js frontend Docker image may require an API Gateway URL. With this construct, you can deploy the API Gateway first, then pass its URL as a build-time argument to the Next.js Docker image.

---


## Features

* Automatically builds and pushes Docker images to ECR.
* Supports custom build arguments for Docker builds, including CDK tokens resolved at deployment time.
* Retrieves Docker images for use in ECS or Lambda.

---


## Installation

### For NPM

Install the construct using NPM:

```bash
npm install token-injectable-docker-builder
```

### For Python

Install the construct using pip:

```bash
pip install token-injectable-docker-builder
```

---


## Constructor

### `TokenInjectableDockerBuilder`

#### Parameters

* **`scope`**: The construct's parent scope.
* **`id`**: The construct ID.
* **`props`**: Configuration properties.

#### Properties in `TokenInjectableDockerBuilderProps`

| Property               | Type               | Required | Description                                                                                           |
|------------------------|--------------------|----------|-------------------------------------------------------------------------------------------------------|
| `path`                 | `string`          | Yes      | The file path to the Dockerfile or source code directory.                                             |
| `buildArgs`            | `{ [key: string]: string }` | No | Build arguments to pass to the Docker build process.                                                  |
| `dockerLoginSecretArn` | `string`          | No       | ARN of an AWS Secrets Manager secret for Docker credentials. Skips login if not provided.             |

---


## Usage Examples

### TypeScript/NPM Example

Here is how to use `TokenInjectableDockerBuilder` in an AWS CDK project with TypeScript:

```python
import * as cdk from 'aws-cdk-lib';
import { TokenInjectableDockerBuilder } from 'token-injectable-docker-builder';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const dockerBuilder = new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', {
      path: './docker',
      buildArgs: {
        TOKEN: 'my-secret-token',
        ENV: 'production',
      },
      dockerLoginSecretArn: 'arn:aws:secretsmanager:us-east-1:123456789012:secret:DockerLoginSecret',
    });

    // Use in ECS
    new ecs.FargateTaskDefinition(this, 'TaskDefinition', {
      containerImage: dockerBuilder.containerImage,
    });

    // Use in Lambda
    new lambda.Function(this, 'DockerLambdaFunction', {
      runtime: lambda.Runtime.FROM_IMAGE,
      code: dockerBuilder.dockerImageCode,
      handler: lambda.Handler.FROM_IMAGE,
    });
  }
}
```

---


### Python Example

Here is how to use `TokenInjectableDockerBuilder` in an AWS CDK project with Python:

```python
from aws_cdk import core as cdk
from token_injectable_docker_builder import TokenInjectableDockerBuilder
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_lambda as lambda_

class MyStack(cdk.Stack):

    def __init__(self, scope: cdk.App, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        docker_builder = TokenInjectableDockerBuilder(self, "MyDockerBuilder",
            path="./docker",
            build_args={
                "TOKEN": "my-secret-token",
                "ENV": "production"
            },
            docker_login_secret_arn="arn:aws:secretsmanager:us-east-1:123456789012:secret:DockerLoginSecret"
        )

        # Use in ECS
        ecs.FargateTaskDefinition(self, "TaskDefinition",
            container_image=docker_builder.container_image
        )

        # Use in Lambda
        lambda_.Function(self, "DockerLambdaFunction",
            runtime=lambda_.Runtime.FROM_IMAGE,
            code=docker_builder.docker_image_code,
            handler=lambda_.Handler.FROM_IMAGE
        )
```

---


## How It Works

1. **Docker Source**: Packages the source code or Dockerfile specified in the `path` property as an S3 asset.
2. **CodeBuild Project**:

   * Uses the packaged asset and `buildArgs` to build the Docker image.
   * Pushes the image to an ECR repository.
3. **Custom Resource**:

   * Triggers the build process using a Lambda function (`onEvent`).
   * Monitors the build status using another Lambda function (`isComplete`).
4. **Outputs**:

   * `.containerImage`: Returns the Docker image for ECS.
   * `.dockerImageCode`: Returns the Docker image code for Lambda.

---


## IAM Permissions

The construct automatically grants permissions for:

* CodeBuild to pull and push images to ECR.
* Lambda to monitor build status and retrieve logs.
* Encryption via a custom KMS key.

---


## Notes

* **Build Arguments**: Pass custom arguments via `buildArgs` as `--build-arg` flags.
* **ECR Repository**: Automatically creates an ECR repository with lifecycle rules.
* **Custom Resources**: Manages lifecycle events for builds using custom Lambda handlers.

---


## Troubleshooting

1. **Build Errors**: Check CodeBuild logs in CloudWatch.
2. **Lambda Errors**: Check `onEvent` and `isComplete` Lambda logs in CloudWatch.
3. **Permissions**: Ensure IAM roles have the required permissions for CodeBuild, ECR, and Secrets Manager.

---


## Support

Open an issue on [GitHub](https://github.com/AlexTech314/TokenInjectableDockerBuilder).

---


## Reference Links

[![View on Construct Hub](https://constructs.dev/badge?package=token-injectable-docker-builder)](https://constructs.dev/packages/token-injectable-docker-builder)
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class TokenInjectableDockerBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="token-injectable-docker-builder.TokenInjectableDockerBuilder",
):
    '''A CDK construct to build and push Docker images to an ECR repository using CodeBuild and Lambda custom resources.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_login_secret_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param path: The path to the directory containing the Dockerfile or source code.
        :param build_args: Build arguments to pass to the Docker build process. These are transformed into ``--build-arg`` flags.
        :param docker_login_secret_arn: The ARN of the AWS Secrets Manager secret containing Docker login credentials. This secret should store a JSON object with the following structure:: { "username": "my-docker-username", "password": "my-docker-password" } If not provided, the construct will skip Docker login during the build process.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab459e7d115d1d8742a5a5096b6fc8a04c58d19c7ae560c4cfa28a2a885351e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TokenInjectableDockerBuilderProps(
            path=path,
            build_args=build_args,
            docker_login_secret_arn=docker_login_secret_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="dockerImageCode")
    def docker_image_code(self) -> _aws_cdk_aws_lambda_ceddda9d.DockerImageCode:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.DockerImageCode, jsii.get(self, "dockerImageCode"))


@jsii.data_type(
    jsii_type="token-injectable-docker-builder.TokenInjectableDockerBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "build_args": "buildArgs",
        "docker_login_secret_arn": "dockerLoginSecretArn",
    },
)
class TokenInjectableDockerBuilderProps:
    def __init__(
        self,
        *,
        path: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_login_secret_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the ``TokenInjectableDockerBuilder`` construct.

        :param path: The path to the directory containing the Dockerfile or source code.
        :param build_args: Build arguments to pass to the Docker build process. These are transformed into ``--build-arg`` flags.
        :param docker_login_secret_arn: The ARN of the AWS Secrets Manager secret containing Docker login credentials. This secret should store a JSON object with the following structure:: { "username": "my-docker-username", "password": "my-docker-password" } If not provided, the construct will skip Docker login during the build process.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768a8fd54fa9d30e8a3c9ce21d38fb8896ac969a161df6469697e06a05864286)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument docker_login_secret_arn", value=docker_login_secret_arn, expected_type=type_hints["docker_login_secret_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if docker_login_secret_arn is not None:
            self._values["docker_login_secret_arn"] = docker_login_secret_arn

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to the directory containing the Dockerfile or source code.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Build arguments to pass to the Docker build process.

        These are transformed into ``--build-arg`` flags.

        Example::

            {
              TOKEN: 'my-secret-token',
              ENV: 'production'
            }
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def docker_login_secret_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Secrets Manager secret containing Docker login credentials.

        This secret should store a JSON object with the following structure::

           {
             "username": "my-docker-username",
             "password": "my-docker-password"
           }

        If not provided, the construct will skip Docker login during the build process.

        Example::

            'arn:aws:secretsmanager:us-east-1:123456789012:secret:DockerLoginSecret'
        '''
        result = self._values.get("docker_login_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenInjectableDockerBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TokenInjectableDockerBuilder",
    "TokenInjectableDockerBuilderProps",
]

publication.publish()

def _typecheckingstub__aab459e7d115d1d8742a5a5096b6fc8a04c58d19c7ae560c4cfa28a2a885351e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    path: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_login_secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768a8fd54fa9d30e8a3c9ce21d38fb8896ac969a161df6469697e06a05864286(
    *,
    path: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_login_secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
