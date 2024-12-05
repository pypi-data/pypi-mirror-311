r'''
<div align="center">
  <h1>
	<img width="512" src="assets/alma-cdk-project.svg" alt="Alma CDK Project" />
  <br/>
  <br/>
  </h1>

![Stability: Stable](https://img.shields.io/badge/stability-stable-%234BCA2A)
![Versioning: SemVer 2.0.0](https://img.shields.io/badge/versioning-semver_2.0.0-blue)
[![release](https://github.com/alma-cdk/project/actions/workflows/release.yml/badge.svg)](https://github.com/alma-cdk/project/actions/workflows/release.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=alma-cdk_project&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=alma-cdk_project)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=alma-cdk_project&metric=coverage)](https://sonarcloud.io/summary/new_code?id=alma-cdk_project)

  <hr/>
</div>

> [!Tip]
> Migrating from `v0` to `v1`? See [Migration Guide](/docs/MIGRATION-GUIDE-0-to-1.md).

<br/>

Opinionated CDK “framework” with constructs & utilities for:

* deploying multiple environments to multiple accounts (with many-to-many relationship)
* managing account configuration through standardized props (no more random config files)
* querying account and/or environment specific information within your CDK code
* enabling dynamic & short-lived “feature-environments”
* enabling well-defined tagging
* providing structure & common conventions to CDK projects
* choosing the target account & environment by passing in runtime context:

  ```sh
  npx cdk deploy -c account=dev -c environment=feature/abc-123
  ```

  ... which means you don't need to define all the possible environments ahead of time!

## Account Strategies

Depending on the use case, you may choose a configuration between 1-3 AWS accounts with the following environments:

1. **Shared account (`shared`)**:

   ![default-multi](assets/accounts-1x.svg)
   <br/>
2. **Multi-account (`dev`+`prod`)***– RECOMMENDED*:

   ![default-multi](assets/accounts-2x.svg)
   <br/>

<br/>
</details>

1. **Multi-account (`dev`+`preprod`+`prod`)**:

   ![default-multi](assets/accounts-3x.svg)
   <br/>

<br/>

## Getting Started

Steps required to define a *environmental* project resources; At first, it might seem complex but once you get into the habbit of defining your projects this way it starts to make sense:

1. Choose your [Account Strategy](#account-strategies)
2. Initialize a new `Project` instead of `cdk.App`:

   ```python
   // bin/app.ts
   import { Project, AccountStrategy } from '@alma-cdk/project';

   const project = new Project({
     // Basic info, you could also read these from package.json if you want
     name: 'my-cool-project',
     author: {
       organization: 'Acme Corp',
       name: 'Mad Scientists',
       email: 'mad.scientists@acme.example.com',
     },

     // If not set, defaults to one of: $CDK_DEFAULT_REGION, $AWS_REGION or us-east-1
     defaultRegion: 'eu-west-1',

     // Configures the project to use 2 AWS accounts (recommended)
     accounts: AccountStrategy.two({
       dev: {
         id: '111111111111',
         config: {
           // whatever you want here as [string]: any
           baseDomain: 'example.net',
         },
       },
       prod: {
         id: '222222222222',
         config: {
           // whatever you want here as [string]: any
           baseDomain: 'example.com',
         },
       },
     }),
   })
   ```
3. Define a stack which `extends SmartStack` with resources:

   ```python
   // lib/my-stack.ts
   import { Construct } from 'constructs';
   import { StackProps, RemovalPolicy } from 'aws-cdk-lib';
   import { SmartStack, Name, UrlName, PathName, EC } from '@alma-cdk/project';

   export class MyStack extends SmartStack {
     constructor(scope: Construct, id: string, props: StackProps) {
       super(scope, id, props);

       new dynamodb.Table(this, 'Table', {
         removalPolicy: EC.isStable(this) ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,

         tableName: Name.it(this, 'MyTable'),
         partitionKey: {
           type: dynamodb.AttributeType.STRING,
           name: 'pk',
         },
         // StagingMyTable
       });

       new events.EventBus(this, 'EventBus', {
         eventBusName: Name.withProject(this, 'MyEventBus'),
         // MyCoolProjectStagingMyEventBus
       });

       new s3.Bucket(this, 'Bucket', {

         removalPolicy: EC.isStable(this) ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,
         autoDeleteObjects: EC.isStable(this) ? false : true,

         bucketName: UrlName.globally(this, 'MyBucket'),
         // acme-corp-my-cool-project-feature-foo-bar-my-bucket
       });

       new ssm.StringParameter(this, 'Parameter', {
         stringValue: 'Foo',
         tier: ssm.ParameterTier.ADVANCED,
         parameterName: PathName.withProject(this, 'MyNamespace/MyParameter'),
         // /MyCoolProject/Staging/MyNamespace/MyParameter
       });
     }
   }
   ```
4. Define a new *environmental* which `extends EnvironmentWrapper` and initialize all your environmental `SmartStack` stacks within:

   ```python
   // lib/environment.ts
   import { Construct } from 'constructs';
   import { EnvironmentWrapper } from '@alma-cdk/project';
   import { MyStack } from './my-stack';

   export class Environment extends EnvironmentWrapper {
     constructor(scope: Construct) {
       super(scope);
       new MyStack(this, 'MyStack', { description: 'This is required' });
     }
   }
   ```

   Resulting Stack properties (given `environment=staging`):

   |        Property         |                    Example value                     |
   | :---------------------- | :--------------------------------------------------- |
   | `stackName`             | `"MyCoolProject-Environment-Staging-MyExampleStack"` |
   | `terminationProtection` | `true`                                               |
   | `env.account`           | `"111111111111"`                                     |
   | `env.region`            | `"eu-west-1"`                                        |

   Resulting Tags for the Stack and its resources (given `environment=staging`):

   |        Property         |           Example value           |
   | :---------------------- | :-------------------------------- |
   | `Account`               | `dev`                             |
   | `Environment`           | `staging`                         |
   | `Project`               | `my-cool-project`                 |
   | `Author`                | `Mad Scientists`                  |
   | `Organization`          | `Acme Corp`                       |
   | `Contact`               | `mad.scientists@acme.example.com` |
5. Finally initialize the environment with the `Project` scope:

   ```python
   // bin/app.ts
   import { Project, Accounts } from '@alma-cdk/project';
   import { Environment } from '../lib/environment';

   const project = new Project({/* removed for brevity, see step 1 */})

   new Environment(project);
   ```

<br/>

## Documentation

See detailed documentation for specific classes & methods at [constructs.dev](http://constructs.dev/packages/@alma-cdk/project).

Generally speaking you would be most interested in the following:

* Project
* AccountStrategy
* SmartStack
* AccountWrapper & EnvironmentWrapper
* AccountContext (AC)
* EnvironmentContext (EC)
* Name / UrlName / PathName

### Migration Guide

Migrating from `v0` to `v1`? See [Migration Guide](/docs/MIGRATION-GUIDE-0-to-1.md).

### Roadmap

For now, see [Issue #36](https://github.com/alma-cdk/project/issues/36).

<br/>
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

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@alma-cdk/project.Account",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "config": "config", "environments": "environments"},
)
class Account:
    def __init__(
        self,
        *,
        id: builtins.str,
        config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''AWS account configuration.

        :param id: AWS Account ID.
        :param config: AWS account specific configuration. For example VPC IDs (for existing VPCs), Direct Connect Gateway IDs, apex domain names (for Route53 Zone lookups), etc. Basically configuration for resources that are defined outside of this CDK application.
        :param environments: List of accepted environments for the given account. List of strings or strings representing regexp initialization (passed onto ``new Regexp("^"+environment+"$", "i")``).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf24cf0aafd9d5f29615609737dd382ada1eb1717b9c13714bee0f5e9e53958)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if config is not None:
            self._values["config"] = config
        if environments is not None:
            self._values["environments"] = environments

    @builtins.property
    def id(self) -> builtins.str:
        '''AWS Account ID.

        Example::

            '123456789012'
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''AWS account specific configuration.

        For example VPC IDs (for existing VPCs), Direct Connect Gateway IDs, apex domain names (for Route53 Zone lookups), etc. Basically configuration for resources that are defined outside of this CDK application.

        Example::

            {
              dev: {
                id: '111111111111',
                config: {
                  baseDomain: 'example.net',
                },
              },
              prod: {
                id: '222222222222',
                config: {
                  baseDomain: 'example.com',
                },
              },
            },
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def environments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of accepted environments for the given account.

        List of strings or strings representing regexp initialization (passed onto ``new Regexp("^"+environment+"$", "i")``).

        Example::

            ["development", "feature/.*"]
        '''
        result = self._values.get("environments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Account(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alma-cdk/project.AccountConfiguration",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "config": "config"},
)
class AccountConfiguration:
    def __init__(
        self,
        *,
        id: builtins.str,
        config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''Interface for a single account type configuration.

        :param id: 
        :param config: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e010d089320f66392656e82caca5525dfb8027e565e72d346c91e39ab2ed007)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if config is not None:
            self._values["config"] = config

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccountContext(
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.AccountContext",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getAccountConfig")
    @builtins.classmethod
    def get_account_config(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        key: builtins.str,
    ) -> typing.Any:
        '''
        :param scope: -
        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f59810c64573cd114a6222761c75b4def09a997c899fb352fe2fc59dfc2dc87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "getAccountConfig", [scope, key]))

    @jsii.member(jsii_name="getAccountId")
    @builtins.classmethod
    def get_account_id(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492006c9c20d82f92a933bb0e00fac380dccd1fcd06bf3afaa5e0b2616c388ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getAccountId", [scope]))

    @jsii.member(jsii_name="getAccountType")
    @builtins.classmethod
    def get_account_type(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10df1db8c4562e59f7908fd621867b7bde2c236658cf99b71700fcf13e696ad6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getAccountType", [scope]))

    @jsii.member(jsii_name="isDev")
    @builtins.classmethod
    def is_dev(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ea853f481ae2a186916a7fb498d943a9f41e7899e0d39059570f2d23535674)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDev", [scope]))

    @jsii.member(jsii_name="isMock")
    @builtins.classmethod
    def is_mock(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb089136259ec8e202d69f58e72b2aa46bc5d2674078a5f40a707b3229d2093f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMock", [scope]))

    @jsii.member(jsii_name="isPreProd")
    @builtins.classmethod
    def is_pre_prod(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc66fae43324ffed116ac12ec4fc9d31fdfecea9bafd33cb76d117c5e9fee31e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isPreProd", [scope]))

    @jsii.member(jsii_name="isProd")
    @builtins.classmethod
    def is_prod(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3abb1e2410671cdca133b42d0476684502e2672325165603a53959be128b3d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isProd", [scope]))

    @jsii.member(jsii_name="isShared")
    @builtins.classmethod
    def is_shared(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a5bdfc6f2d8f216710c431c567ebb622b8675c9229150f40d971cd199a6aec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isShared", [scope]))


class AccountStrategy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@alma-cdk/project.AccountStrategy",
):
    '''Use static methods of ``AccountStrategy`` abstract class to define your account strategy.

    Available strategies are:

    - One Account: ``shared``
    - Two Accounts: ``dev``+``prod`` – *recommended*
    - Three Accounts: ``dev``+``preprod``+``prod``
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="one")
    @builtins.classmethod
    def one(
        cls,
        *,
        shared: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> typing.Mapping[builtins.str, Account]:
        '''Enables single account strategy.

        1. ``shared`` account with environments:

           - development
           - feature/*
           - test
           - qaN
           - staging
           - preproduction
           - production

        :param shared: 
        :param mock: 

        Example::

            AccountStrategy.one({
              shared: {
                id: '111111111111',
              },
            }),
        '''
        props = AccountStrategyOneProps(shared=shared, mock=mock)

        return typing.cast(typing.Mapping[builtins.str, Account], jsii.sinvoke(cls, "one", [props]))

    @jsii.member(jsii_name="three")
    @builtins.classmethod
    def three(
        cls,
        *,
        dev: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        preprod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        prod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> typing.Mapping[builtins.str, Account]:
        '''Enables triple account strategy.

        1. ``dev`` account with environments:

           - development
           - feature/*
           - test
           - staging

        2. ``preprod`` account with environments:

           - qaN
           - preproduction

        3. ``prod`` account with environments:

           - production

        :param dev: 
        :param preprod: 
        :param prod: 
        :param mock: 

        Example::

            AccountStrategy.three({
              dev: {
                id: '111111111111',
              },
              preprod: {
                id: '222222222222',
              },
              prod: {
                id: '333333333333',
              },
            }),
        '''
        props = AccountStrategyThreeProps(
            dev=dev, preprod=preprod, prod=prod, mock=mock
        )

        return typing.cast(typing.Mapping[builtins.str, Account], jsii.sinvoke(cls, "three", [props]))

    @jsii.member(jsii_name="two")
    @builtins.classmethod
    def two(
        cls,
        *,
        dev: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        prod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> typing.Mapping[builtins.str, Account]:
        '''Enables dual account strategy.

        1. ``dev`` account with environments:

           - development
           - feature/*
           - test
           - qaN
           - staging

        2. ``prod`` account with environments:

           - preproduction
           - production

        :param dev: 
        :param prod: 
        :param mock: 

        Example::

            AccountStrategy.two({
              dev: {
                id: '111111111111',
              },
              prod: {
                id: '222222222222',
              },
            }),
        '''
        props = AccountStrategyTwoProps(dev=dev, prod=prod, mock=mock)

        return typing.cast(typing.Mapping[builtins.str, Account], jsii.sinvoke(cls, "two", [props]))


class _AccountStrategyProxy(AccountStrategy):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AccountStrategy).__jsii_proxy_class__ = lambda : _AccountStrategyProxy


@jsii.data_type(
    jsii_type="@alma-cdk/project.AccountStrategyOneProps",
    jsii_struct_bases=[],
    name_mapping={"shared": "shared", "mock": "mock"},
)
class AccountStrategyOneProps:
    def __init__(
        self,
        *,
        shared: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props ``AccountStrategy.one``.

        :param shared: 
        :param mock: 
        '''
        if isinstance(shared, dict):
            shared = AccountConfiguration(**shared)
        if isinstance(mock, dict):
            mock = AccountConfiguration(**mock)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c277e9dae2fcb922d6bfb505ec1f104ef4811b7652e64a98bb9c979f4fb067)
            check_type(argname="argument shared", value=shared, expected_type=type_hints["shared"])
            check_type(argname="argument mock", value=mock, expected_type=type_hints["mock"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shared": shared,
        }
        if mock is not None:
            self._values["mock"] = mock

    @builtins.property
    def shared(self) -> AccountConfiguration:
        result = self._values.get("shared")
        assert result is not None, "Required property 'shared' is missing"
        return typing.cast(AccountConfiguration, result)

    @builtins.property
    def mock(self) -> typing.Optional[AccountConfiguration]:
        result = self._values.get("mock")
        return typing.cast(typing.Optional[AccountConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountStrategyOneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alma-cdk/project.AccountStrategyThreeProps",
    jsii_struct_bases=[],
    name_mapping={"dev": "dev", "preprod": "preprod", "prod": "prod", "mock": "mock"},
)
class AccountStrategyThreeProps:
    def __init__(
        self,
        *,
        dev: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        preprod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        prod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props ``AccountStrategy.three``.

        :param dev: 
        :param preprod: 
        :param prod: 
        :param mock: 
        '''
        if isinstance(dev, dict):
            dev = AccountConfiguration(**dev)
        if isinstance(preprod, dict):
            preprod = AccountConfiguration(**preprod)
        if isinstance(prod, dict):
            prod = AccountConfiguration(**prod)
        if isinstance(mock, dict):
            mock = AccountConfiguration(**mock)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac623d3c8e04a1a862985ffe7e8e77ac241fdf0140fcc21897ea95e1ae24172b)
            check_type(argname="argument dev", value=dev, expected_type=type_hints["dev"])
            check_type(argname="argument preprod", value=preprod, expected_type=type_hints["preprod"])
            check_type(argname="argument prod", value=prod, expected_type=type_hints["prod"])
            check_type(argname="argument mock", value=mock, expected_type=type_hints["mock"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dev": dev,
            "preprod": preprod,
            "prod": prod,
        }
        if mock is not None:
            self._values["mock"] = mock

    @builtins.property
    def dev(self) -> AccountConfiguration:
        result = self._values.get("dev")
        assert result is not None, "Required property 'dev' is missing"
        return typing.cast(AccountConfiguration, result)

    @builtins.property
    def preprod(self) -> AccountConfiguration:
        result = self._values.get("preprod")
        assert result is not None, "Required property 'preprod' is missing"
        return typing.cast(AccountConfiguration, result)

    @builtins.property
    def prod(self) -> AccountConfiguration:
        result = self._values.get("prod")
        assert result is not None, "Required property 'prod' is missing"
        return typing.cast(AccountConfiguration, result)

    @builtins.property
    def mock(self) -> typing.Optional[AccountConfiguration]:
        result = self._values.get("mock")
        return typing.cast(typing.Optional[AccountConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountStrategyThreeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alma-cdk/project.AccountStrategyTwoProps",
    jsii_struct_bases=[],
    name_mapping={"dev": "dev", "prod": "prod", "mock": "mock"},
)
class AccountStrategyTwoProps:
    def __init__(
        self,
        *,
        dev: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        prod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
        mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props ``AccountStrategy.two``.

        :param dev: 
        :param prod: 
        :param mock: 
        '''
        if isinstance(dev, dict):
            dev = AccountConfiguration(**dev)
        if isinstance(prod, dict):
            prod = AccountConfiguration(**prod)
        if isinstance(mock, dict):
            mock = AccountConfiguration(**mock)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2f1978fe657429245f4d6bdb833cc25a69cb0e10a6324cd3e1abb0d7f2aa35)
            check_type(argname="argument dev", value=dev, expected_type=type_hints["dev"])
            check_type(argname="argument prod", value=prod, expected_type=type_hints["prod"])
            check_type(argname="argument mock", value=mock, expected_type=type_hints["mock"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dev": dev,
            "prod": prod,
        }
        if mock is not None:
            self._values["mock"] = mock

    @builtins.property
    def dev(self) -> AccountConfiguration:
        result = self._values.get("dev")
        assert result is not None, "Required property 'dev' is missing"
        return typing.cast(AccountConfiguration, result)

    @builtins.property
    def prod(self) -> AccountConfiguration:
        result = self._values.get("prod")
        assert result is not None, "Required property 'prod' is missing"
        return typing.cast(AccountConfiguration, result)

    @builtins.property
    def mock(self) -> typing.Optional[AccountConfiguration]:
        result = self._values.get("mock")
        return typing.cast(typing.Optional[AccountConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountStrategyTwoProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccountType(metaclass=jsii.JSIIMeta, jsii_type="@alma-cdk/project.AccountType"):
    '''Internal class to handle set/get operations for Account Type.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="get")
    @builtins.classmethod
    def get(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0506937a6a45a7d27b89aa68c38e328c32d74d447e06dfbc13cb3c2ac0b883d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "get", [scope]))

    @jsii.member(jsii_name="matchFromEnvironment")
    @builtins.classmethod
    def match_from_environment(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
        environment_type: builtins.str,
    ) -> builtins.str:
        '''
        :param scope: -
        :param accounts: -
        :param environment_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e48162b5fd07e1969e6cf918bdc33c11adf9d999ced8e5842d102b57c201f3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument environment_type", value=environment_type, expected_type=type_hints["environment_type"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "matchFromEnvironment", [scope, accounts, environment_type]))

    @jsii.member(jsii_name="set")
    @builtins.classmethod
    def set(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        account_type: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param account_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd172dac2276583edb28058ad720fbbe6a7633ca4a3aef0e97246451bb42af62)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
        return typing.cast(None, jsii.sinvoke(cls, "set", [scope, account_type]))


class AccountWrapper(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.AccountWrapper",
):
    '''Wrapper for account-level stacks.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct) -> None:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d44f9e937418990f927db991f525c3e16c234b625674d5a17baf630e655171)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        jsii.create(self.__class__, self, [scope])


@jsii.data_type(
    jsii_type="@alma-cdk/project.Acknowledgeable",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "message": "message"},
)
class Acknowledgeable:
    def __init__(
        self,
        *,
        id: builtins.str,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Interface for acknowledging warnings.

        :param id: 
        :param message: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920f2e77e9cf320099305ccf96450b4f9f83bcc6237d4274861cb7459aba33e4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Acknowledgeable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alma-cdk/project.Author",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "email": "email", "organization": "organization"},
)
class Author:
    def __init__(
        self,
        *,
        name: builtins.str,
        email: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Author information.

        I.e. who owns/develops this project/service.

        :param name: Human-readable name for the team/contact responsible for this project/service.
        :param email: Email address for the team/contact responsible for this project/service.
        :param organization: Human-readable name for the organization responsible for this project/service.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9806608d940e2c529f315a9d963444cbf25cb45199300ad989179a073228168a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if email is not None:
            self._values["email"] = email
        if organization is not None:
            self._values["organization"] = organization

    @builtins.property
    def name(self) -> builtins.str:
        '''Human-readable name for the team/contact responsible for this project/service.

        Example::

            'Mad Scientists'
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address for the team/contact responsible for this project/service.

        Example::

            'mad.scientists@acme.example.com'
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''Human-readable name for the organization responsible for this project/service.

        Example::

            'Acme Corp'
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Author(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvRegExp(metaclass=jsii.JSIIMeta, jsii_type="@alma-cdk/project.EnvRegExp"):
    def __init__(self, base: builtins.str) -> None:
        '''
        :param base: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554c8d7299225ada4161c40beb571ff0dbe1da3055897a08b14f3e1dab0f288c)
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
        jsii.create(self.__class__, self, [base])

    @jsii.member(jsii_name="test")
    def test(self, value: builtins.str) -> builtins.bool:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f0927e23b72a3a0c834d35b892cfec0e752ac193c944b816750dcaada816de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "test", [value]))


@jsii.enum(jsii_type="@alma-cdk/project.EnvironmentCategory")
class EnvironmentCategory(enum.Enum):
    '''Availalbe Enviroment Categories.

    Categories are useful grouping to make distinction between ``stable``
    environments (``staging`` & ``production``) from ``feature`` or ``verification``
    environments (such as ``test`` or ``preproduction``).
    '''

    MOCK = "MOCK"
    DEVELOPMENT = "DEVELOPMENT"
    FEATURE = "FEATURE"
    VERIFICATION = "VERIFICATION"
    STABLE = "STABLE"


class EnvironmentContext(
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.EnvironmentContext",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getCategory")
    @builtins.classmethod
    def get_category(cls, scope: _constructs_77d1e7e8.Construct) -> EnvironmentCategory:
        '''Get Environment Category.

        Categories are useful grouping to make distinction between ``stable``
        environments (``staging`` & ``production``) from ``feature`` or ``verification``
        environments (such as ``test`` or ``preproduction``).

        :param scope: Construct.

        :return: Environment Category

        Example::

            'mock'
            'development'
            'feature'
            'verification'
            'stable'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0adb5d1d64195ce3ab2ccf7dff81307d61bf5bc6b2f82d11a21abdcb268617)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(EnvironmentCategory, jsii.sinvoke(cls, "getCategory", [scope]))

    @jsii.member(jsii_name="getFeatureInfo")
    @builtins.classmethod
    def get_feature_info(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''Get Feature Info.

        If environment belongs to ``feature`` category,
        this will return a string describing the feature (sting after ``feature/``-prefix).

        If environment is not a feature environment, will return an empty string.

        :param scope: Construct.

        :return: string indicating the feature this environment relates to, if not feature environment returns an empty string
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa16e73db27f034966584d96d088cc088872f8301a96c50ee3e65c36cba05725)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getFeatureInfo", [scope]))

    @jsii.member(jsii_name="getLabel")
    @builtins.classmethod
    def get_label(cls, scope: _constructs_77d1e7e8.Construct) -> "EnvironmentLabel":
        '''Get Environment Label.

        Labels are useful since Environment Name can be complex,
        such as ``feature/foo-bar`` or ``qa3``,
        but we need to be able to “label” all ``feature/*`` and ``qaN`` environments
        as either ``feature`` or ``qa``.

        :param scope: Construct.

        :return: Environment Label

        Example::

            'mock'
            'development'
            'feature'
            'test'
            'staging'
            'qa'
            'preproduction'
            'production'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dcaaa164f5352416aa23e098dd42c2987338c445ce91d789bb9986ad6357b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("EnvironmentLabel", jsii.sinvoke(cls, "getLabel", [scope]))

    @jsii.member(jsii_name="getName")
    @builtins.classmethod
    def get_name(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''Get Environment Name.

        :param scope: Construct.

        :return: Environment Name (as given via ``--context environment``)

        Example::

            'mock1'
            'mock2'
            'mock3'
            'development'
            'feature/foo-bar'
            'feature/ABC-123/new-stuff'
            'test'
            'staging'
            'qa1'
            'qa2'
            'qa3'
            'preproduction'
            'production'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24daf4bb6262768bfdd826884f13bb50284a2e6894f128d50c6c3e1a17984c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getName", [scope]))

    @jsii.member(jsii_name="getUrlName")
    @builtins.classmethod
    def get_url_name(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''Get Environment URL/DNS Compatible Name.

        :param scope: Construct.

        :return: Environment URL/DNS Compatible Name (as given via ``--context environment`` but ``param-cased``)

        Example::

            'mock1'
            'mock2'
            'mock3'
            'development'
            'feature-foo-bar'
            'feature-abc-123-new-stuff'
            'test'
            'staging'
            'qa1'
            'qa2'
            'qa3'
            'preproduction'
            'production'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fb0c49651ad26cd57ff22a13b50bed5739d33f796752a0469a68dcd9de925a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getUrlName", [scope]))

    @jsii.member(jsii_name="isDevelopment")
    @builtins.classmethod
    def is_development(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''Check if Environment is part of ``development`` category.

        Returns true for ``development``, otherwise ``false``.

        :param scope: Construct.

        :return: boolean indicating does Environment belong to ``development`` category
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d8033f28ad77515adb67e3a26ce69ad6dff35b6beb3785ba5cd377b1ea80af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDevelopment", [scope]))

    @jsii.member(jsii_name="isFeature")
    @builtins.classmethod
    def is_feature(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''Check if Environment is part of ``feature`` category.

        Returns ``true`` for environments with name beginning with ``feature/``-prefix, otherwise ``false``.

        :param scope: Construct.

        :return: boolean indicating does Environment belong to ``feature`` category
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685ce69311ab899adac1f80c26eeacae03fbe0f59a50cae46c3b7238d36fb517)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isFeature", [scope]))

    @jsii.member(jsii_name="isMock")
    @builtins.classmethod
    def is_mock(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''Check if Environment is part of ``mock`` category.

        :param scope: Construct.

        :return: boolean indicating does Environment belong to ``mock`` category
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2d298d1b5542096a31f67ccbb6a4c9f5a9de4c7e6d18c4c91b73eea25b9108)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMock", [scope]))

    @jsii.member(jsii_name="isStable")
    @builtins.classmethod
    def is_stable(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''Check if Environment is part of ``stable`` category.

        Returns ``true`` for ``staging`` & ``production``, otherwise ``false``.

        :param scope: Construct.

        :return: boolean indicating does Environment belong to ``stable`` category
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0939c8f4e2d5f2bbca05beaef050488c678c4ee4b0d1e68c0dead4d596ae81bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStable", [scope]))

    @jsii.member(jsii_name="isVerification")
    @builtins.classmethod
    def is_verification(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.bool:
        '''Check if Environment is part of ``verification`` category.

        Returns ``true`` for ``test`` & ``preproduction``, otherwise ``false``.

        :param scope: Construct.

        :return: boolean indicating does Environment belong to ``verification`` category
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025874f923c9552a4f2bf3d528af99578b2a910ba17594c74faaa4f284485055)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isVerification", [scope]))


@jsii.enum(jsii_type="@alma-cdk/project.EnvironmentLabel")
class EnvironmentLabel(enum.Enum):
    '''Available Environment Labels.

    Labels are useful since Environment Name can be complex,
    such as ``feature/foo-bar`` or ``qa3``,
    but we need to be able to “label” all ``feature/*`` and ``qaN`` environments
    as either ``feature`` or ``qa``.
    '''

    MOCK = "MOCK"
    DEVELOPMENT = "DEVELOPMENT"
    FEATURE = "FEATURE"
    TEST = "TEST"
    STAGING = "STAGING"
    QA = "QA"
    PREPRODUCTION = "PREPRODUCTION"
    PRODUCTION = "PRODUCTION"


class EnvironmentType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.EnvironmentType",
):
    '''Internal class to handle set/get operations for Environment Type.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="get")
    @builtins.classmethod
    def get(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        allowed_environments: typing.Sequence[builtins.str],
    ) -> builtins.str:
        '''
        :param scope: -
        :param allowed_environments: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24dc0dd669cccdfb10c0e96c5df5a1479362803233dec40094ff2ab44057450)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument allowed_environments", value=allowed_environments, expected_type=type_hints["allowed_environments"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "get", [scope, allowed_environments]))

    @jsii.member(jsii_name="set")
    @builtins.classmethod
    def set(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        environment_type: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param environment_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cabc590b37686ad5bbd983be59e85470cd275e564400fdb2b1bcc8580aa158c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument environment_type", value=environment_type, expected_type=type_hints["environment_type"])
        return typing.cast(None, jsii.sinvoke(cls, "set", [scope, environment_type]))

    @jsii.member(jsii_name="tryGet")
    @builtins.classmethod
    def try_get(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.Optional[builtins.str]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1343628b9463a487cb26376b11ee60503e5d4bfc5726b4680ba4e3072516e698)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "tryGet", [scope]))


class EnvironmentWrapper(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.EnvironmentWrapper",
):
    '''Wrapper for environmental stacks.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct) -> None:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446310dcdb1e90562a94604888e87f660f0351492c84025f6a1e243127d1daba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        jsii.create(self.__class__, self, [scope])


class Name(metaclass=jsii.JSIIAbstractClass, jsii_type="@alma-cdk/project.Name"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="globally")
    @builtins.classmethod
    def globally(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''PascalCase naming with global prefixes (org, project…).

        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00df1444ca51f3a34c88ac770bba7e4eaf60357104be1fa1a38a730effefe2f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "globally", [scope, base_name, props]))

    @jsii.member(jsii_name="it")
    @builtins.classmethod
    def it(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''
        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c97e8ad7a8ef7589db3a0aec166f71f2901cab117ea701bd9ece2a1297c23c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "it", [scope, base_name, props]))

    @jsii.member(jsii_name="withProject")
    @builtins.classmethod
    def with_project(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''
        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec3a482b0b5cf5b10f0446a6e50e391c93540c8c293936cbefcd6d00ef1de56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "withProject", [scope, base_name, props]))


class _NameProxy(Name):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Name).__jsii_proxy_class__ = lambda : _NameProxy


@jsii.data_type(
    jsii_type="@alma-cdk/project.NameProps",
    jsii_struct_bases=[],
    name_mapping={"max_length": "maxLength", "trim": "trim"},
)
class NameProps:
    def __init__(
        self,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06094e70c63c6997695a0b02cd2da34e13fe2418801e2f68366dec4bc25f8393)
            check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            check_type(argname="argument trim", value=trim, expected_type=type_hints["trim"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_length is not None:
            self._values["max_length"] = max_length
        if trim is not None:
            self._values["trim"] = trim

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trim(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("trim")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Project(
    _aws_cdk_ceddda9d.App,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.Project",
):
    '''High-level wrapper for ``cdk.App`` with specific requirements for props.

    Use it like you would ``cdk.App`` and assign stacks into it.

    Example::

        // new Project instead of new App
        const project = new Project({
          name: 'my-cool-project',
          author: {
            organization: 'Acme Corp',
            name: 'Mad Scientists',
            email: 'mad.scientists@acme.example.com',
          },
          defaultRegion: 'eu-west-1', // defaults to one of: $CDK_DEFAULT_REGION, $AWS_REGION or us-east-1
          accounts: {
            dev: {
              id: '111111111111',
              environments: ['development', 'feature/.*', 'staging'],
              config: {
                baseDomain: 'example.net',
              },
            },
            prod: {
              id: '222222222222',
              environments: ['production'],
              config: {
                baseDomain: 'example.com',
              },
            },
          },
        })
    '''

    def __init__(
        self,
        *,
        accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
        author: typing.Union[Author, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        default_region: typing.Optional[builtins.str] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
        outdir: typing.Optional[builtins.str] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Initializes a new Project (which can be used in place of cdk.App).

        :param accounts: Dictionary of AWS account specific configuration. The key value can be anything (such as AWS Account alias), but it's recommended to keep it short such as ``dev`` or ``prod``.
        :param author: Author information. I.e. who owns/develops this project/service.
        :param name: Name of your project/service. Prefer ``hyphen-case``.
        :param default_region: Specify default region you wish to use. If left empty will default to one of the following in order: 1. ``$CDK_DEFAULT_REGION`` 2. ``$AWS_REGION`` 3. 'us-east-1'
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param default_stack_synthesizer: The stack synthesizer to use by default for all Stacks in the App. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. Default: - A ``DefaultStackSynthesizer`` with default settings
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param policy_validation_beta1: Validation plugins to run after synthesis. Default: - no validation plugins
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The ``AppProps.context`` property This property is recommended over the ``AppProps.context`` property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        '''
        props = ProjectProps(
            accounts=accounts,
            author=author,
            name=name,
            default_region=default_region,
            analytics_reporting=analytics_reporting,
            auto_synth=auto_synth,
            context=context,
            default_stack_synthesizer=default_stack_synthesizer,
            outdir=outdir,
            policy_validation_beta1=policy_validation_beta1,
            post_cli_context=post_cli_context,
            stack_traces=stack_traces,
            tree_metadata=tree_metadata,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="getAccount")
    @builtins.classmethod
    def get_account(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        account_type: builtins.str,
    ) -> Account:
        '''Return account configuration.

        :param scope: -
        :param account_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8271ee93f2d2fbb5d7d744fe7b0962c64292313d921b5b9e00f00623a78a044f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
        return typing.cast(Account, jsii.sinvoke(cls, "getAccount", [scope, account_type]))

    @jsii.member(jsii_name="getConfiguration")
    @builtins.classmethod
    def get_configuration(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> "ProjectConfiguration":
        '''Return the project configuration as given in ProjectProps.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e253de5d98d08c1f2180cba3141f8b01eeb2a4160f8929fb334a713ba5da8d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("ProjectConfiguration", jsii.sinvoke(cls, "getConfiguration", [scope]))

    @jsii.member(jsii_name="acknowledgeWarnings")
    def acknowledge_warnings(
        self,
        acknowledgements: typing.Sequence[typing.Union[Acknowledgeable, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Acknowledge warnings for all stacks in the project.

        :param acknowledgements: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65df5ed73b20e7c87567ea92ca693d50b6cce4933556f42a03c21c957854b73a)
            check_type(argname="argument acknowledgements", value=acknowledgements, expected_type=type_hints["acknowledgements"])
        return typing.cast(None, jsii.invoke(self, "acknowledgeWarnings", [acknowledgements]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CONTEXT_SCOPE")
    def CONTEXT_SCOPE(cls) -> builtins.str:
        '''Namespace/key how this tool internally keeps track of the project configuration.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CONTEXT_SCOPE"))


@jsii.data_type(
    jsii_type="@alma-cdk/project.ProjectConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "accounts": "accounts",
        "author": "author",
        "name": "name",
        "default_region": "defaultRegion",
    },
)
class ProjectConfiguration:
    def __init__(
        self,
        *,
        accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
        author: typing.Union[Author, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        default_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accounts: Dictionary of AWS account specific configuration. The key value can be anything (such as AWS Account alias), but it's recommended to keep it short such as ``dev`` or ``prod``.
        :param author: Author information. I.e. who owns/develops this project/service.
        :param name: Name of your project/service. Prefer ``hyphen-case``.
        :param default_region: Specify default region you wish to use. If left empty will default to one of the following in order: 1. ``$CDK_DEFAULT_REGION`` 2. ``$AWS_REGION`` 3. 'us-east-1'
        '''
        if isinstance(author, dict):
            author = Author(**author)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652ec219fc4f578e6db75fd1ba3efd41dde95e34581dca7bfc7b42304cbd8e1c)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument author", value=author, expected_type=type_hints["author"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default_region", value=default_region, expected_type=type_hints["default_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "author": author,
            "name": name,
        }
        if default_region is not None:
            self._values["default_region"] = default_region

    @builtins.property
    def accounts(self) -> typing.Mapping[builtins.str, Account]:
        '''Dictionary of AWS account specific configuration.

        The key value can be anything (such as AWS Account alias), but it's recommended to keep it short such as ``dev`` or ``prod``.

        Example::

            accounts: {
              dev: {
                id: '111111111111',
                config: {
                  baseDomain: 'example.net',
                },
              },
              prod: {
                id: '222222222222',
                config: {
                  baseDomain: 'example.com',
                },
              },
            },
        '''
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.Mapping[builtins.str, Account], result)

    @builtins.property
    def author(self) -> Author:
        '''Author information.

        I.e. who owns/develops this project/service.
        '''
        result = self._values.get("author")
        assert result is not None, "Required property 'author' is missing"
        return typing.cast(Author, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of your project/service.

        Prefer ``hyphen-case``.

        Example::

            'my-cool-project'
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_region(self) -> typing.Optional[builtins.str]:
        '''Specify default region you wish to use.

        If left empty will default to one of the following in order:

        1. ``$CDK_DEFAULT_REGION``
        2. ``$AWS_REGION``
        3. 'us-east-1'
        '''
        result = self._values.get("default_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectContext(
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.ProjectContext",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getAccountConfig")
    @builtins.classmethod
    def get_account_config(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        key: builtins.str,
        default_value: typing.Any = None,
    ) -> typing.Any:
        '''
        :param scope: -
        :param key: -
        :param default_value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141248910025e66566ce546d21bad5daa16953cfe58c5b1e10d65cc0289a5d00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "getAccountConfig", [scope, key, default_value]))

    @jsii.member(jsii_name="getAccountId")
    @builtins.classmethod
    def get_account_id(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675d9482cd85bb94471970c5d729b7e7cd1f05828e165de72737673ecac7749e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getAccountId", [scope]))

    @jsii.member(jsii_name="getAccountType")
    @builtins.classmethod
    def get_account_type(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''Returns the account type given in runtime/CLI context.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0140dfb7ced8a20c2af76d82923f41e0942c778cc1907c7ff2524cb1a6f53de2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getAccountType", [scope]))

    @jsii.member(jsii_name="getAllowedEnvironments")
    @builtins.classmethod
    def get_allowed_environments(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.List[builtins.str]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4470bbbdefbe863284650990854056480b73e39f4326e6d3ea6bf10975c52fa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "getAllowedEnvironments", [scope]))

    @jsii.member(jsii_name="getAuthorEmail")
    @builtins.classmethod
    def get_author_email(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.Optional[builtins.str]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400bf232f6ce1610bf72ba52f18c8c15a6f2d544225a5438646d7b79317ed2ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "getAuthorEmail", [scope]))

    @jsii.member(jsii_name="getAuthorName")
    @builtins.classmethod
    def get_author_name(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b2d5accd7d7ece036b28a83d4d594e659c2959144b1d7dac62c18fa3cdaf17)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getAuthorName", [scope]))

    @jsii.member(jsii_name="getAuthorOrganization")
    @builtins.classmethod
    def get_author_organization(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.Optional[builtins.str]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eacf88f8a09eb196d4afb7ac2b75f692a9fb64b42943aa528d829fa3b7b4e05)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "getAuthorOrganization", [scope]))

    @jsii.member(jsii_name="getDefaultRegion")
    @builtins.classmethod
    def get_default_region(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8352acb42b318d65938154ac3edc577f94f4f400c3859c14cc33b02c652804ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getDefaultRegion", [scope]))

    @jsii.member(jsii_name="getEnvironment")
    @builtins.classmethod
    def get_environment(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dea8b4f71a942251aea42562d016e02ba5b1c20a1c186feaa7931e226f4cac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getEnvironment", [scope]))

    @jsii.member(jsii_name="getName")
    @builtins.classmethod
    def get_name(cls, scope: _constructs_77d1e7e8.Construct) -> builtins.str:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f0824ac5f3ccf841fa8c49fcf2ff6f1b6b99747ed0e7e15e5ae0072620ebda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getName", [scope]))

    @jsii.member(jsii_name="tryGetEnvironment")
    @builtins.classmethod
    def try_get_environment(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> typing.Optional[builtins.str]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e941a37d39600a4ba152ba73e76ab2b8016d1707bbc1adff93824791e6148c92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "tryGetEnvironment", [scope]))


@jsii.data_type(
    jsii_type="@alma-cdk/project.ProjectProps",
    jsii_struct_bases=[ProjectConfiguration, _aws_cdk_ceddda9d.AppProps],
    name_mapping={
        "accounts": "accounts",
        "author": "author",
        "name": "name",
        "default_region": "defaultRegion",
        "analytics_reporting": "analyticsReporting",
        "auto_synth": "autoSynth",
        "context": "context",
        "default_stack_synthesizer": "defaultStackSynthesizer",
        "outdir": "outdir",
        "policy_validation_beta1": "policyValidationBeta1",
        "post_cli_context": "postCliContext",
        "stack_traces": "stackTraces",
        "tree_metadata": "treeMetadata",
    },
)
class ProjectProps(ProjectConfiguration, _aws_cdk_ceddda9d.AppProps):
    def __init__(
        self,
        *,
        accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
        author: typing.Union[Author, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        default_region: typing.Optional[builtins.str] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
        outdir: typing.Optional[builtins.str] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Props given to ``Project``.

        I.e. custom props for this construct and the usual props given to ``cdk.App``.

        :param accounts: Dictionary of AWS account specific configuration. The key value can be anything (such as AWS Account alias), but it's recommended to keep it short such as ``dev`` or ``prod``.
        :param author: Author information. I.e. who owns/develops this project/service.
        :param name: Name of your project/service. Prefer ``hyphen-case``.
        :param default_region: Specify default region you wish to use. If left empty will default to one of the following in order: 1. ``$CDK_DEFAULT_REGION`` 2. ``$AWS_REGION`` 3. 'us-east-1'
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param default_stack_synthesizer: The stack synthesizer to use by default for all Stacks in the App. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. Default: - A ``DefaultStackSynthesizer`` with default settings
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param policy_validation_beta1: Validation plugins to run after synthesis. Default: - no validation plugins
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The ``AppProps.context`` property This property is recommended over the ``AppProps.context`` property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        '''
        if isinstance(author, dict):
            author = Author(**author)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cf7fa7740f02787247e32918b9363c6582897bc16d6eb80f287e0e6b6978b9)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument author", value=author, expected_type=type_hints["author"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default_region", value=default_region, expected_type=type_hints["default_region"])
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument auto_synth", value=auto_synth, expected_type=type_hints["auto_synth"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument default_stack_synthesizer", value=default_stack_synthesizer, expected_type=type_hints["default_stack_synthesizer"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument policy_validation_beta1", value=policy_validation_beta1, expected_type=type_hints["policy_validation_beta1"])
            check_type(argname="argument post_cli_context", value=post_cli_context, expected_type=type_hints["post_cli_context"])
            check_type(argname="argument stack_traces", value=stack_traces, expected_type=type_hints["stack_traces"])
            check_type(argname="argument tree_metadata", value=tree_metadata, expected_type=type_hints["tree_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "author": author,
            "name": name,
        }
        if default_region is not None:
            self._values["default_region"] = default_region
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if auto_synth is not None:
            self._values["auto_synth"] = auto_synth
        if context is not None:
            self._values["context"] = context
        if default_stack_synthesizer is not None:
            self._values["default_stack_synthesizer"] = default_stack_synthesizer
        if outdir is not None:
            self._values["outdir"] = outdir
        if policy_validation_beta1 is not None:
            self._values["policy_validation_beta1"] = policy_validation_beta1
        if post_cli_context is not None:
            self._values["post_cli_context"] = post_cli_context
        if stack_traces is not None:
            self._values["stack_traces"] = stack_traces
        if tree_metadata is not None:
            self._values["tree_metadata"] = tree_metadata

    @builtins.property
    def accounts(self) -> typing.Mapping[builtins.str, Account]:
        '''Dictionary of AWS account specific configuration.

        The key value can be anything (such as AWS Account alias), but it's recommended to keep it short such as ``dev`` or ``prod``.

        Example::

            accounts: {
              dev: {
                id: '111111111111',
                config: {
                  baseDomain: 'example.net',
                },
              },
              prod: {
                id: '222222222222',
                config: {
                  baseDomain: 'example.com',
                },
              },
            },
        '''
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.Mapping[builtins.str, Account], result)

    @builtins.property
    def author(self) -> Author:
        '''Author information.

        I.e. who owns/develops this project/service.
        '''
        result = self._values.get("author")
        assert result is not None, "Required property 'author' is missing"
        return typing.cast(Author, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of your project/service.

        Prefer ``hyphen-case``.

        Example::

            'my-cool-project'
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_region(self) -> typing.Optional[builtins.str]:
        '''Specify default region you wish to use.

        If left empty will default to one of the following in order:

        1. ``$CDK_DEFAULT_REGION``
        2. ``$AWS_REGION``
        3. 'us-east-1'
        '''
        result = self._values.get("default_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in the Stacks of this app.

        :default: Value of 'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_synth(self) -> typing.Optional[builtins.bool]:
        '''Automatically call ``synth()`` before the program exits.

        If you set this, you don't have to call ``synth()`` explicitly. Note that
        this feature is only available for certain programming languages, and
        calling ``synth()`` is still recommended.

        :default:

        true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false``
        otherwise
        '''
        result = self._values.get("auto_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context values for the application.

        Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def default_stack_synthesizer(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer]:
        '''The stack synthesizer to use by default for all Stacks in the App.

        The Stack Synthesizer controls aspects of synthesis and deployment,
        like how assets are referenced and what IAM roles to use. For more
        information, see the README of the main CDK package.

        :default: - A ``DefaultStackSynthesizer`` with default settings
        '''
        result = self._values.get("default_stack_synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The output directory into which to emit synthesized artifacts.

        You should never need to set this value. By default, the value you pass to
        the CLI's ``--output`` flag will be used, and if you change it to a different
        directory the CLI will fail to pick up the generated Cloud Assembly.

        This property is intended for internal and testing use.

        :default:

        - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``.
        If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_validation_beta1(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]]:
        '''Validation plugins to run after synthesis.

        :default: - no validation plugins
        '''
        result = self._values.get("policy_validation_beta1")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]], result)

    @builtins.property
    def post_cli_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context values for the application.

        Context provided here has precedence over context set by:

        - The CLI via --context
        - The ``context`` key in ``cdk.json``
        - The ``AppProps.context`` property

        This property is recommended over the ``AppProps.context`` property since you
        can make final decision over which context value to take in your app.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context

        Example::

            // context from the CLI and from `cdk.json` are stored in the
            // CDK_CONTEXT env variable
            const cliContext = JSON.parse(process.env.CDK_CONTEXT!);
            
            // determine whether to take the context passed in the CLI or not
            const determineValue = process.env.PROD ? cliContext.SOMEKEY : 'my-prod-value';
            new App({
              postCliContext: {
                SOMEKEY: determineValue,
              },
            });
        '''
        result = self._values.get("post_cli_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def stack_traces(self) -> typing.Optional[builtins.bool]:
        '''Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs.

        :default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        '''
        result = self._values.get("stack_traces")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tree_metadata(self) -> typing.Optional[builtins.bool]:
        '''Include construct tree metadata as part of the Cloud Assembly.

        :default: true
        '''
        result = self._values.get("tree_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SmartStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/project.SmartStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4acbebd77836c7e0229190b770d5f42c8d3592cf837829c609b09e8f27d3b688)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.StackProps(
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            permissions_boundary=permissions_boundary,
            stack_name=stack_name,
            suppress_template_indentation=suppress_template_indentation,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class UrlName(
    Name,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@alma-cdk/project.UrlName",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="globally")
    @builtins.classmethod
    def globally(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''PascalCase naming with global prefixes (org, project…).

        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132d1bd5492f9fa79b50d4cebba153c29c4a55f48849c0dcb198922173621264)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "globally", [scope, base_name, props]))

    @jsii.member(jsii_name="it")
    @builtins.classmethod
    def it(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''
        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb1336351664dd207da2653e6e2e08f8d77b9fb62d88deb5c54448ad422f206)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "it", [scope, base_name, props]))

    @jsii.member(jsii_name="withProject")
    @builtins.classmethod
    def with_project(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''
        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00bf57716c24ce59dc55f26941600be46117e5da217e719ce029931feb72b9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "withProject", [scope, base_name, props]))


class _UrlNameProxy(
    UrlName,
    jsii.proxy_for(Name), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, UrlName).__jsii_proxy_class__ = lambda : _UrlNameProxy


class PathName(
    UrlName,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@alma-cdk/project.PathName",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="globally")
    @builtins.classmethod
    def globally(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''PascalCase naming with global prefixes (org, project…).

        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d3fb984d54bc80cdd2909ff0ae0d1010fec47c1c9281a7137744b88a678c22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "globally", [scope, base_name, props]))

    @jsii.member(jsii_name="it")
    @builtins.classmethod
    def it(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''
        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88df8a9a0941d3859261e49836983523d1efffebb8222b1957a087f57f9963af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "it", [scope, base_name, props]))

    @jsii.member(jsii_name="withProject")
    @builtins.classmethod
    def with_project(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        base_name: builtins.str,
        *,
        max_length: typing.Optional[jsii.Number] = None,
        trim: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''
        :param scope: -
        :param base_name: -
        :param max_length: 
        :param trim: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9255856470a1c906dd3bc1297d860146ec1b2aa0a2042bc77aaac8a37f925e08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument base_name", value=base_name, expected_type=type_hints["base_name"])
        props = NameProps(max_length=max_length, trim=trim)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "withProject", [scope, base_name, props]))


class _PathNameProxy(
    PathName,
    jsii.proxy_for(UrlName), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PathName).__jsii_proxy_class__ = lambda : _PathNameProxy


__all__ = [
    "Account",
    "AccountConfiguration",
    "AccountContext",
    "AccountStrategy",
    "AccountStrategyOneProps",
    "AccountStrategyThreeProps",
    "AccountStrategyTwoProps",
    "AccountType",
    "AccountWrapper",
    "Acknowledgeable",
    "Author",
    "EnvRegExp",
    "EnvironmentCategory",
    "EnvironmentContext",
    "EnvironmentLabel",
    "EnvironmentType",
    "EnvironmentWrapper",
    "Name",
    "NameProps",
    "PathName",
    "Project",
    "ProjectConfiguration",
    "ProjectContext",
    "ProjectProps",
    "SmartStack",
    "UrlName",
]

publication.publish()

def _typecheckingstub__fdf24cf0aafd9d5f29615609737dd382ada1eb1717b9c13714bee0f5e9e53958(
    *,
    id: builtins.str,
    config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    environments: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e010d089320f66392656e82caca5525dfb8027e565e72d346c91e39ab2ed007(
    *,
    id: builtins.str,
    config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f59810c64573cd114a6222761c75b4def09a997c899fb352fe2fc59dfc2dc87(
    scope: _constructs_77d1e7e8.Construct,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492006c9c20d82f92a933bb0e00fac380dccd1fcd06bf3afaa5e0b2616c388ab(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10df1db8c4562e59f7908fd621867b7bde2c236658cf99b71700fcf13e696ad6(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ea853f481ae2a186916a7fb498d943a9f41e7899e0d39059570f2d23535674(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb089136259ec8e202d69f58e72b2aa46bc5d2674078a5f40a707b3229d2093f(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc66fae43324ffed116ac12ec4fc9d31fdfecea9bafd33cb76d117c5e9fee31e(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3abb1e2410671cdca133b42d0476684502e2672325165603a53959be128b3d2(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a5bdfc6f2d8f216710c431c567ebb622b8675c9229150f40d971cd199a6aec(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c277e9dae2fcb922d6bfb505ec1f104ef4811b7652e64a98bb9c979f4fb067(
    *,
    shared: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
    mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac623d3c8e04a1a862985ffe7e8e77ac241fdf0140fcc21897ea95e1ae24172b(
    *,
    dev: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
    preprod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
    prod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
    mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2f1978fe657429245f4d6bdb833cc25a69cb0e10a6324cd3e1abb0d7f2aa35(
    *,
    dev: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
    prod: typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]],
    mock: typing.Optional[typing.Union[AccountConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0506937a6a45a7d27b89aa68c38e328c32d74d447e06dfbc13cb3c2ac0b883d(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e48162b5fd07e1969e6cf918bdc33c11adf9d999ced8e5842d102b57c201f3f(
    scope: _constructs_77d1e7e8.Construct,
    accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
    environment_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd172dac2276583edb28058ad720fbbe6a7633ca4a3aef0e97246451bb42af62(
    scope: _constructs_77d1e7e8.Construct,
    account_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d44f9e937418990f927db991f525c3e16c234b625674d5a17baf630e655171(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920f2e77e9cf320099305ccf96450b4f9f83bcc6237d4274861cb7459aba33e4(
    *,
    id: builtins.str,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9806608d940e2c529f315a9d963444cbf25cb45199300ad989179a073228168a(
    *,
    name: builtins.str,
    email: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554c8d7299225ada4161c40beb571ff0dbe1da3055897a08b14f3e1dab0f288c(
    base: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f0927e23b72a3a0c834d35b892cfec0e752ac193c944b816750dcaada816de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0adb5d1d64195ce3ab2ccf7dff81307d61bf5bc6b2f82d11a21abdcb268617(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa16e73db27f034966584d96d088cc088872f8301a96c50ee3e65c36cba05725(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dcaaa164f5352416aa23e098dd42c2987338c445ce91d789bb9986ad6357b2(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24daf4bb6262768bfdd826884f13bb50284a2e6894f128d50c6c3e1a17984c5(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fb0c49651ad26cd57ff22a13b50bed5739d33f796752a0469a68dcd9de925a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d8033f28ad77515adb67e3a26ce69ad6dff35b6beb3785ba5cd377b1ea80af(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685ce69311ab899adac1f80c26eeacae03fbe0f59a50cae46c3b7238d36fb517(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2d298d1b5542096a31f67ccbb6a4c9f5a9de4c7e6d18c4c91b73eea25b9108(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0939c8f4e2d5f2bbca05beaef050488c678c4ee4b0d1e68c0dead4d596ae81bb(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025874f923c9552a4f2bf3d528af99578b2a910ba17594c74faaa4f284485055(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24dc0dd669cccdfb10c0e96c5df5a1479362803233dec40094ff2ab44057450(
    scope: _constructs_77d1e7e8.Construct,
    allowed_environments: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cabc590b37686ad5bbd983be59e85470cd275e564400fdb2b1bcc8580aa158c(
    scope: _constructs_77d1e7e8.Construct,
    environment_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1343628b9463a487cb26376b11ee60503e5d4bfc5726b4680ba4e3072516e698(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446310dcdb1e90562a94604888e87f660f0351492c84025f6a1e243127d1daba(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00df1444ca51f3a34c88ac770bba7e4eaf60357104be1fa1a38a730effefe2f7(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c97e8ad7a8ef7589db3a0aec166f71f2901cab117ea701bd9ece2a1297c23c(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec3a482b0b5cf5b10f0446a6e50e391c93540c8c293936cbefcd6d00ef1de56(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06094e70c63c6997695a0b02cd2da34e13fe2418801e2f68366dec4bc25f8393(
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8271ee93f2d2fbb5d7d744fe7b0962c64292313d921b5b9e00f00623a78a044f(
    scope: _constructs_77d1e7e8.Construct,
    account_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e253de5d98d08c1f2180cba3141f8b01eeb2a4160f8929fb334a713ba5da8d1(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65df5ed73b20e7c87567ea92ca693d50b6cce4933556f42a03c21c957854b73a(
    acknowledgements: typing.Sequence[typing.Union[Acknowledgeable, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652ec219fc4f578e6db75fd1ba3efd41dde95e34581dca7bfc7b42304cbd8e1c(
    *,
    accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
    author: typing.Union[Author, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    default_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141248910025e66566ce546d21bad5daa16953cfe58c5b1e10d65cc0289a5d00(
    scope: _constructs_77d1e7e8.Construct,
    key: builtins.str,
    default_value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675d9482cd85bb94471970c5d729b7e7cd1f05828e165de72737673ecac7749e(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0140dfb7ced8a20c2af76d82923f41e0942c778cc1907c7ff2524cb1a6f53de2(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4470bbbdefbe863284650990854056480b73e39f4326e6d3ea6bf10975c52fa1(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400bf232f6ce1610bf72ba52f18c8c15a6f2d544225a5438646d7b79317ed2ae(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b2d5accd7d7ece036b28a83d4d594e659c2959144b1d7dac62c18fa3cdaf17(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eacf88f8a09eb196d4afb7ac2b75f692a9fb64b42943aa528d829fa3b7b4e05(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8352acb42b318d65938154ac3edc577f94f4f400c3859c14cc33b02c652804ae(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dea8b4f71a942251aea42562d016e02ba5b1c20a1c186feaa7931e226f4cac(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f0824ac5f3ccf841fa8c49fcf2ff6f1b6b99747ed0e7e15e5ae0072620ebda(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e941a37d39600a4ba152ba73e76ab2b8016d1707bbc1adff93824791e6148c92(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cf7fa7740f02787247e32918b9363c6582897bc16d6eb80f287e0e6b6978b9(
    *,
    accounts: typing.Mapping[builtins.str, typing.Union[Account, typing.Dict[builtins.str, typing.Any]]],
    author: typing.Union[Author, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    default_region: typing.Optional[builtins.str] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    auto_synth: typing.Optional[builtins.bool] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
    outdir: typing.Optional[builtins.str] = None,
    policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
    post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    stack_traces: typing.Optional[builtins.bool] = None,
    tree_metadata: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acbebd77836c7e0229190b770d5f42c8d3592cf837829c609b09e8f27d3b688(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132d1bd5492f9fa79b50d4cebba153c29c4a55f48849c0dcb198922173621264(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb1336351664dd207da2653e6e2e08f8d77b9fb62d88deb5c54448ad422f206(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00bf57716c24ce59dc55f26941600be46117e5da217e719ce029931feb72b9a(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d3fb984d54bc80cdd2909ff0ae0d1010fec47c1c9281a7137744b88a678c22(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88df8a9a0941d3859261e49836983523d1efffebb8222b1957a087f57f9963af(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9255856470a1c906dd3bc1297d860146ec1b2aa0a2042bc77aaac8a37f925e08(
    scope: _constructs_77d1e7e8.Construct,
    base_name: builtins.str,
    *,
    max_length: typing.Optional[jsii.Number] = None,
    trim: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
