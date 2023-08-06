'''
# AWS Amplify Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

The AWS Amplify Console provides a Git-based workflow for deploying and hosting fullstack serverless web applications. A fullstack serverless app consists of a backend built with cloud resources such as GraphQL or REST APIs, file and data storage, and a frontend built with single page application frameworks such as React, Angular, Vue, or Gatsby.

## Setting up an app with branches, custom rules and a domain

To set up an Amplify Console app, define an `App`:

```python
import aws_cdk.aws_codebuild as codebuild


amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    build_spec=codebuild.BuildSpec.from_object_to_yaml({
        # Alternatively add a `amplify.yml` to the repo
        "version": "1.0",
        "frontend": {
            "phases": {
                "pre_build": {
                    "commands": ["yarn"
                    ]
                },
                "build": {
                    "commands": ["yarn build"
                    ]
                }
            },
            "artifacts": {
                "base_directory": "public",
                "files": -"**/*"
            }
        }
    })
)
```

To connect your `App` to GitLab, use the `GitLabSourceCodeProvider`:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitLabSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-gitlab-token")
    )
)
```

To connect your `App` to CodeCommit, use the `CodeCommitSourceCodeProvider`:

```python
import aws_cdk.aws_codecommit as codecommit


repository = codecommit.Repository(self, "Repo",
    repository_name="my-repo"
)

amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
)
```

The IAM role associated with the `App` will automatically be granted the permission
to pull the CodeCommit repository.

Add branches:

```python
# amplify_app: amplify.App


master = amplify_app.add_branch("master") # `id` will be used as repo branch name
dev = amplify_app.add_branch("dev",
    performance_mode=True
)
dev.add_environment("STAGE", "dev")
```

Auto build and pull request preview are enabled by default.

Add custom rules for redirection:

```python
# amplify_app: amplify.App

amplify_app.add_custom_rule({
    "source": "/docs/specific-filename.html",
    "target": "/documents/different-filename.html",
    "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
})
```

When working with a single page application (SPA), use the
`CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT` to set up a 200
rewrite for all files to `index.html` except for the following
file extensions: css, gif, ico, jpg, js, png, txt, svg, woff,
ttf, map, json, webmanifest.

```python
# my_single_page_app: amplify.App


my_single_page_app.add_custom_rule(amplify.CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT)
```

Add a domain and map sub domains to branches:

```python
# amplify_app: amplify.App
# master: amplify.Branch
# dev: amplify.Branch


domain = amplify_app.add_domain("example.com",
    enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
    auto_subdomain_creation_patterns=["*", "pr*"]
)
domain.map_root(master) # map master branch to domain root
domain.map_sub_domain(master, "www")
domain.map_sub_domain(dev)
```

## Restricting access

Password protect the app with basic auth by specifying the `basicAuth` prop.

Use `BasicAuth.fromCredentials` when referencing an existing secret:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_credentials("username", SecretValue.secrets_manager("my-github-token"))
)
```

Use `BasicAuth.fromGeneratedPassword` to generate a password in Secrets Manager:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

Basic auth can be added to specific branches:

```python
# amplify_app: amplify.App

amplify_app.add_branch("feature/next",
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

## Automatically creating and deleting branches

Use the `autoBranchCreation` and `autoBranchDeletion` props to control creation/deletion
of branches:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
        patterns=["feature/*", "test/*"]),
    auto_branch_deletion=True
)
```

## Adding custom response headers

Use the `customResponseHeaders` prop to configure custom response headers for an Amplify app:

```python
amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    custom_response_headers=[amplify.CustomResponseHeader(
        pattern="*.json",
        headers={
            "custom-header-name-1": "custom-header-value-1",
            "custom-header-name-2": "custom-header-value-2"
        }
    ), amplify.CustomResponseHeader(
        pattern="/path/*",
        headers={
            "custom-header-name-1": "custom-header-value-2"
        }
    )
    ]
)
```

## Deploying Assets

`sourceCodeProvider` is optional; when this is not specified the Amplify app can be deployed to using `.zip` packages. The `asset` property can be used to deploy S3 assets to Amplify as part of the CDK:

```python
import aws_cdk.aws_s3_assets as assets

# asset: assets.Asset
# amplify_app: amplify.App

branch = amplify_app.add_branch("dev", asset=asset)
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

import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_0f2c5c86
import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_692dd32c
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_kms as _aws_cdk_aws_kms_e491a92b
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_525817d7
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.AppProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_name": "appName",
        "auto_branch_creation": "autoBranchCreation",
        "auto_branch_deletion": "autoBranchDeletion",
        "basic_auth": "basicAuth",
        "build_spec": "buildSpec",
        "custom_response_headers": "customResponseHeaders",
        "custom_rules": "customRules",
        "description": "description",
        "environment_variables": "environmentVariables",
        "role": "role",
        "source_code_provider": "sourceCodeProvider",
    },
)
class AppProps:
    def __init__(
        self,
        *,
        app_name: typing.Optional[builtins.str] = None,
        auto_branch_creation: typing.Optional[typing.Union["AutoBranchCreation", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_branch_deletion: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional["BasicAuth"] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        custom_response_headers: typing.Optional[typing.Sequence[typing.Union["CustomResponseHeader", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_rules: typing.Optional[typing.Sequence["CustomRule"]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        source_code_provider: typing.Optional["ISourceCodeProvider"] = None,
    ) -> None:
        '''(experimental) Properties for an App.

        :param app_name: (experimental) The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: (experimental) The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param auto_branch_deletion: (experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository. Default: false
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: (experimental) BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param custom_response_headers: (experimental) The custom HTTP response headers for an Amplify app. Default: - no custom response headers
        :param custom_rules: (experimental) Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: (experimental) A description for the application. Default: - no description
        :param environment_variables: (experimental) Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param role: (experimental) The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: (experimental) The source code provider for this application. Default: - not connected to a source code provider

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if isinstance(auto_branch_creation, dict):
            auto_branch_creation = AutoBranchCreation(**auto_branch_creation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a42617415a38f5dc244a1f6aa313edb2a8d55d6c1adf78c65786ca5aa9c283)
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument auto_branch_creation", value=auto_branch_creation, expected_type=type_hints["auto_branch_creation"])
            check_type(argname="argument auto_branch_deletion", value=auto_branch_deletion, expected_type=type_hints["auto_branch_deletion"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument custom_response_headers", value=custom_response_headers, expected_type=type_hints["custom_response_headers"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument source_code_provider", value=source_code_provider, expected_type=type_hints["source_code_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_name is not None:
            self._values["app_name"] = app_name
        if auto_branch_creation is not None:
            self._values["auto_branch_creation"] = auto_branch_creation
        if auto_branch_deletion is not None:
            self._values["auto_branch_deletion"] = auto_branch_deletion
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if custom_response_headers is not None:
            self._values["custom_response_headers"] = custom_response_headers
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if role is not None:
            self._values["role"] = role
        if source_code_provider is not None:
            self._values["source_code_provider"] = source_code_provider

    @builtins.property
    def app_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the application.

        :default: - a CDK generated name

        :stability: experimental
        '''
        result = self._values.get("app_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_branch_creation(self) -> typing.Optional["AutoBranchCreation"]:
        '''(experimental) The auto branch creation configuration.

        Use this to automatically create
        branches that match a certain pattern.

        :default: - no auto branch creation

        :stability: experimental
        '''
        result = self._values.get("auto_branch_creation")
        return typing.cast(typing.Optional["AutoBranchCreation"], result)

    @builtins.property
    def auto_branch_deletion(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_branch_deletion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection at an
        app level to all your branches.

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["BasicAuth"], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec]:
        '''(experimental) BuildSpec for the application.

        Alternatively, add a ``amplify.yml``
        file to the repository.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec], result)

    @builtins.property
    def custom_response_headers(
        self,
    ) -> typing.Optional[typing.List["CustomResponseHeader"]]:
        '''(experimental) The custom HTTP response headers for an Amplify app.

        :default: - no custom response headers

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/custom-headers.html
        :stability: experimental
        '''
        result = self._values.get("custom_response_headers")
        return typing.cast(typing.Optional[typing.List["CustomResponseHeader"]], result)

    @builtins.property
    def custom_rules(self) -> typing.Optional[typing.List["CustomRule"]]:
        '''(experimental) Custom rewrite/redirect rules for the application.

        :default: - no custom rewrite/redirect rules

        :stability: experimental
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.List["CustomRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the application.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM service role to associate with the application.

        The App
        implements IGrantable.

        :default: - a new role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def source_code_provider(self) -> typing.Optional["ISourceCodeProvider"]:
        '''(experimental) The source code provider for this application.

        :default: - not connected to a source code provider

        :stability: experimental
        '''
        result = self._values.get("source_code_provider")
        return typing.cast(typing.Optional["ISourceCodeProvider"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.AutoBranchCreation",
    jsii_struct_bases=[],
    name_mapping={
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "build_spec": "buildSpec",
        "environment_variables": "environmentVariables",
        "patterns": "patterns",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
    },
)
class AutoBranchCreation:
    def __init__(
        self,
        *,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional["BasicAuth"] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Auto branch creation configuration.

        :param auto_build: (experimental) Whether to enable auto building for the auto created branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the auto created branch. Default: - no password protection
        :param build_spec: (experimental) Build spec for the auto created branch. Default: - application build spec
        :param environment_variables: (experimental) Environment variables for the auto created branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param patterns: (experimental) Automated branch creation glob patterns. Default: - all repository branches
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews of the auto created branch. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the auto created branch. Default: true
        :param stage: (experimental) Stage for the auto created branch. Default: - no stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ac19789aacae3d0e48d81cfb04a5a816dd7e43734474e962cb006478d5d075)
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if patterns is not None:
            self._values["patterns"] = patterns
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the auto created branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the auto created branch.

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["BasicAuth"], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec]:
        '''(experimental) Build spec for the auto created branch.

        :default: - application build spec

        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Automated branch creation glob patterns.

        :default: - all repository branches

        :stability: experimental
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews of the auto created branch.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the auto created branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the auto created branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoBranchCreation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BasicAuth(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amplify.BasicAuth"):
    '''(experimental) Basic Auth configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            basic_auth=amplify.BasicAuth.from_generated_password("username")
        )
    '''

    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    ) -> None:
        '''
        :param username: (experimental) The username.
        :param encryption_key: (experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: (experimental) The password. Default: - A Secrets Manager generated password

        :stability: experimental
        '''
        props = BasicAuthProps(
            username=username, encryption_key=encryption_key, password=password
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromCredentials")
    @builtins.classmethod
    def from_credentials(
        cls,
        username: builtins.str,
        password: _aws_cdk_core_f4b25747.SecretValue,
    ) -> "BasicAuth":
        '''(experimental) Creates a Basic Auth configuration from a username and a password.

        :param username: The username.
        :param password: The password.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c714597b18b7dc32f97dd6ef337450b0173afb0347a32120cbb4aeb534b8618)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        return typing.cast("BasicAuth", jsii.sinvoke(cls, "fromCredentials", [username, password]))

    @jsii.member(jsii_name="fromGeneratedPassword")
    @builtins.classmethod
    def from_generated_password(
        cls,
        username: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    ) -> "BasicAuth":
        '''(experimental) Creates a Basic Auth configuration with a password generated in Secrets Manager.

        :param username: The username.
        :param encryption_key: The encryption key to use to encrypt the password in Secrets Manager.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8066b70bbf8acdea4529e1fc01e4e13b1d9a6d007667709746d61eb92debc509)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        return typing.cast("BasicAuth", jsii.sinvoke(cls, "fromGeneratedPassword", [username, encryption_key]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
    ) -> "BasicAuthConfig":
        '''(experimental) Binds this Basic Auth configuration to an App.

        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb784752e3e9e80e5500ace32f5397aba12950541e26f52b553c111ac0062ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("BasicAuthConfig", jsii.invoke(self, "bind", [scope, id]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.BasicAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_basic_auth": "enableBasicAuth",
        "password": "password",
        "username": "username",
    },
)
class BasicAuthConfig:
    def __init__(
        self,
        *,
        enable_basic_auth: builtins.bool,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''(experimental) A Basic Auth configuration.

        :param enable_basic_auth: (experimental) Whether to enable Basic Auth.
        :param password: (experimental) The password.
        :param username: (experimental) The username.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            basic_auth_config = amplify.BasicAuthConfig(
                enable_basic_auth=False,
                password="password",
                username="username"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725255ee8ddeece1d0727bed73b046182864b6472f9ca50218cbf3969c8318a0)
            check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_basic_auth": enable_basic_auth,
            "password": password,
            "username": username,
        }

    @builtins.property
    def enable_basic_auth(self) -> builtins.bool:
        '''(experimental) Whether to enable Basic Auth.

        :stability: experimental
        '''
        result = self._values.get("enable_basic_auth")
        assert result is not None, "Required property 'enable_basic_auth' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.BasicAuthProps",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "encryption_key": "encryptionKey",
        "password": "password",
    },
)
class BasicAuthProps:
    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    ) -> None:
        '''(experimental) Properties for a BasicAuth.

        :param username: (experimental) The username.
        :param encryption_key: (experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: (experimental) The password. Default: - A Secrets Manager generated password

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            import aws_cdk.aws_kms as kms
            import aws_cdk.core as cdk
            
            # key: kms.Key
            # secret_value: cdk.SecretValue
            
            basic_auth_props = amplify.BasicAuthProps(
                username="username",
            
                # the properties below are optional
                encryption_key=key,
                password=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4860d9fa9f2450fb760b9897e0f1f89547eb82fc9a8dd5d4dc9d07e0a0876787)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''(experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager.

        :default: - default master key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def password(self) -> typing.Optional[_aws_cdk_core_f4b25747.SecretValue]:
        '''(experimental) The password.

        :default: - A Secrets Manager generated password

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.BranchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "asset": "asset",
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "description": "description",
        "environment_variables": "environmentVariables",
        "performance_mode": "performanceMode",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
    },
)
class BranchOptions:
    def __init__(
        self,
        *,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to add a branch to an application.

        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # amplify_app: amplify.App
            
            
            master = amplify_app.add_branch("master") # `id` will be used as repo branch name
            dev = amplify_app.add_branch("dev",
                performance_mode=True
            )
            dev.add_environment("STAGE", "dev")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb6497d56beb44cabc8b6f4fb539b9189400191567b0bd23257aa07df6e2429)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset is not None:
            self._values["asset"] = asset
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def asset(self) -> typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset]:
        '''(experimental) Asset for deployment.

        The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's
        startDeployment API to initiate and deploy a S3 asset onto the App.

        :default: - no asset

        :stability: experimental
        '''
        result = self._values.get("asset")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset], result)

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuth]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the branch

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuth], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec]:
        '''(experimental) BuildSpec for the branch.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the branch.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge
        for a longer interval. When performance mode is enabled, hosting configuration or code changes
        can take up to 10 minutes to roll out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.BranchProps",
    jsii_struct_bases=[BranchOptions],
    name_mapping={
        "asset": "asset",
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "description": "description",
        "environment_variables": "environmentVariables",
        "performance_mode": "performanceMode",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
        "app": "app",
    },
)
class BranchProps(BranchOptions):
    def __init__(
        self,
        *,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
        app: "IApp",
    ) -> None:
        '''(experimental) Properties for a Branch.

        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage
        :param app: (experimental) The application within which the branch must be created.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            import aws_cdk.aws_codebuild as codebuild
            import aws_cdk.aws_s3_assets as s3_assets
            
            # app: amplify.App
            # asset: s3_assets.Asset
            # basic_auth: amplify.BasicAuth
            # build_spec: codebuild.BuildSpec
            
            branch_props = amplify.BranchProps(
                app=app,
            
                # the properties below are optional
                asset=asset,
                auto_build=False,
                basic_auth=basic_auth,
                branch_name="branchName",
                build_spec=build_spec,
                description="description",
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                performance_mode=False,
                pull_request_environment_name="pullRequestEnvironmentName",
                pull_request_preview=False,
                stage="stage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e412147e99ae5baa3039fe6719857bfe75faa8b883b0f4a1fbe6504d4ce9f1)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
        }
        if asset is not None:
            self._values["asset"] = asset
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def asset(self) -> typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset]:
        '''(experimental) Asset for deployment.

        The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's
        startDeployment API to initiate and deploy a S3 asset onto the App.

        :default: - no asset

        :stability: experimental
        '''
        result = self._values.get("asset")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset], result)

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuth]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the branch

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuth], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec]:
        '''(experimental) BuildSpec for the branch.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the branch.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge
        for a longer interval. When performance mode is enabled, hosting configuration or code changes
        can take up to 10 minutes to roll out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app(self) -> "IApp":
        '''(experimental) The application within which the branch must be created.

        :stability: experimental
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast("IApp", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApp(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.CfnApp",
):
    '''A CloudFormation ``AWS::Amplify::App``.

    The AWS::Amplify::App resource specifies Apps in Amplify Hosting. An App is a collection of branches.

    :cloudformationResource: AWS::Amplify::App
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amplify as amplify
        
        cfn_app = amplify.CfnApp(self, "MyCfnApp",
            name="name",
        
            # the properties below are optional
            access_token="accessToken",
            auto_branch_creation_config=amplify.CfnApp.AutoBranchCreationConfigProperty(
                auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                build_spec="buildSpec",
                enable_auto_branch_creation=False,
                enable_auto_build=False,
                enable_performance_mode=False,
                enable_pull_request_preview=False,
                environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                framework="framework",
                pull_request_environment_name="pullRequestEnvironmentName",
                stage="stage"
            ),
            basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                enable_basic_auth=False,
                password="password",
                username="username"
            ),
            build_spec="buildSpec",
            custom_headers="customHeaders",
            custom_rules=[amplify.CfnApp.CustomRuleProperty(
                source="source",
                target="target",
        
                # the properties below are optional
                condition="condition",
                status="status"
            )],
            description="description",
            enable_branch_auto_deletion=False,
            environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                name="name",
                value="value"
            )],
            iam_service_role="iamServiceRole",
            oauth_token="oauthToken",
            platform="platform",
            repository="repository",
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
        access_token: typing.Optional[builtins.str] = None,
        auto_branch_creation_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApp.AutoBranchCreationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApp.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        custom_headers: typing.Optional[builtins.str] = None,
        custom_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApp.CustomRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApp.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        iam_service_role: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Amplify::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param access_token: The personal access token for a GitHub repository for an Amplify app. The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored. Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` . You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Minimum length of 1. Maximum length of 255.
        :param auto_branch_creation_config: Sets the configuration for your automatic branch creation.
        :param basic_auth_config: The credentials for basic authorization for an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param custom_headers: The custom HTTP headers for an Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 25000. *Pattern:* (?s).*
        :param custom_rules: The custom rewrite and redirect rules for an Amplify app.
        :param description: The description for an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_branch_auto_deletion: Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.
        :param environment_variables: The environment variables map for an Amplify app.
        :param iam_service_role: The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 1000. *Pattern:* (?s).*
        :param oauth_token: The OAuth token for a third-party source control system for an Amplify app. The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored. Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` . You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param platform: The platform for the Amplify app. For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .
        :param repository: The repository for an Amplify app. *Pattern:* (?s).*
        :param tags: The tag for an Amplify app.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9dd6b3c3ac2a4d99e31efbe2893e3064a44e76cb7a7c7e1b2bf967114b14be5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppProps(
            name=name,
            access_token=access_token,
            auto_branch_creation_config=auto_branch_creation_config,
            basic_auth_config=basic_auth_config,
            build_spec=build_spec,
            custom_headers=custom_headers,
            custom_rules=custom_rules,
            description=description,
            enable_branch_auto_deletion=enable_branch_auto_deletion,
            environment_variables=environment_variables,
            iam_service_role=iam_service_role,
            oauth_token=oauth_token,
            platform=platform,
            repository=repository,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d2fb63c2bcce5f4ac4dcc55b2f1e4e99c91001d22117418ab62ff32879bd22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e600803ddfffd15923ed881b3362028d47f5ba7f426cdd202b9a2bda19b311)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> builtins.str:
        '''Unique Id for the Amplify App.

        :cloudformationAttribute: AppId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppId"))

    @builtins.property
    @jsii.member(jsii_name="attrAppName")
    def attr_app_name(self) -> builtins.str:
        '''Name for the Amplify App.

        :cloudformationAttribute: AppName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppName"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''ARN for the Amplify App.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDefaultDomain")
    def attr_default_domain(self) -> builtins.str:
        '''Default domain for the Amplify App.

        :cloudformationAttribute: DefaultDomain
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDefaultDomain"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tag for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4b35920f963c3c2366324d0140da8bbe37413ec990db63258aee1716ae927f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Optional[builtins.str]:
        '''The personal access token for a GitHub repository for an Amplify app.

        The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored.

        Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` .

        You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c11fa16c4cc2bc2049a1a51395c410e62af1e8103592e5620af514196c184f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value)

    @builtins.property
    @jsii.member(jsii_name="autoBranchCreationConfig")
    def auto_branch_creation_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.AutoBranchCreationConfigProperty"]]:
        '''Sets the configuration for your automatic branch creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.AutoBranchCreationConfigProperty"]], jsii.get(self, "autoBranchCreationConfig"))

    @auto_branch_creation_config.setter
    def auto_branch_creation_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.AutoBranchCreationConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b39f8927bb4ca9e428f1b67ec3cc0945c06866dcc4584ebe24b6c8604759d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoBranchCreationConfig", value)

    @builtins.property
    @jsii.member(jsii_name="basicAuthConfig")
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.BasicAuthConfigProperty"]]:
        '''The credentials for basic authorization for an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.BasicAuthConfigProperty"]], jsii.get(self, "basicAuthConfig"))

    @basic_auth_config.setter
    def basic_auth_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.BasicAuthConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279222b8f8cec11c6c42ee2278755b26bb926bbc0c3f86cf50791f8123f76c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="buildSpec")
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildSpec"))

    @build_spec.setter
    def build_spec(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b2f643d3d3b2c4c3bb1e9d21afe3e60538c0f295c6342103102ad7bc128465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildSpec", value)

    @builtins.property
    @jsii.member(jsii_name="customHeaders")
    def custom_headers(self) -> typing.Optional[builtins.str]:
        '''The custom HTTP headers for an Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 25000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customheaders
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customHeaders"))

    @custom_headers.setter
    def custom_headers(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3780397e4bf7723a37a69802bd8a5537571b31a59dbb55faa34ea6021e1da26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="customRules")
    def custom_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.CustomRuleProperty"]]]]:
        '''The custom rewrite and redirect rules for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.CustomRuleProperty"]]]], jsii.get(self, "customRules"))

    @custom_rules.setter
    def custom_rules(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.CustomRuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfbfc672f48c7f9df26172026d7d10caa3be72f2a5e8c312e6fee32b457119d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRules", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f48ff70fa9321cc85c80cf9a3d83f1e37c37d2a0922517ef2fa4b821cd30404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enableBranchAutoDeletion")
    def enable_branch_auto_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-enablebranchautodeletion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableBranchAutoDeletion"))

    @enable_branch_auto_deletion.setter
    def enable_branch_auto_deletion(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198d39c14c29636514232b80b68229f74f53bdf8d9fd96e32bab18cfa89b561a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBranchAutoDeletion", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]]:
        '''The environment variables map for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c85f2da14bcc5480f42ddbfbb27ed936a3494a6713541ac00f736bc3d520d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="iamServiceRole")
    def iam_service_role(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamServiceRole"))

    @iam_service_role.setter
    def iam_service_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2106a698f378c3da9034a184b2032b1cf89133e449f06aa5fc5f297fd466e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamServiceRole", value)

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> typing.Optional[builtins.str]:
        '''The OAuth token for a third-party source control system for an Amplify app.

        The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored.

        Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` .

        You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthToken"))

    @oauth_token.setter
    def oauth_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0ed74d81cc49cb057bb3fc9238cc0c326cd0e551bc8ceb0988bfb6c3f14477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthToken", value)

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform for the Amplify app.

        For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-platform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fda7d6bf558e33fe4915f5899a7d2eb3e58e5b50373edd54e9213034be6388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[builtins.str]:
        '''The repository for an Amplify app.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e81a827a479788365ce697c88d5cf005de3d7522fada40feed1cf7164e27e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnApp.AutoBranchCreationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_branch_creation_patterns": "autoBranchCreationPatterns",
            "basic_auth_config": "basicAuthConfig",
            "build_spec": "buildSpec",
            "enable_auto_branch_creation": "enableAutoBranchCreation",
            "enable_auto_build": "enableAutoBuild",
            "enable_performance_mode": "enablePerformanceMode",
            "enable_pull_request_preview": "enablePullRequestPreview",
            "environment_variables": "environmentVariables",
            "framework": "framework",
            "pull_request_environment_name": "pullRequestEnvironmentName",
            "stage": "stage",
        },
    )
    class AutoBranchCreationConfigProperty:
        def __init__(
            self,
            *,
            auto_branch_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApp.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            build_spec: typing.Optional[builtins.str] = None,
            enable_auto_branch_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApp.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            framework: typing.Optional[builtins.str] = None,
            pull_request_environment_name: typing.Optional[builtins.str] = None,
            stage: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the AutoBranchCreationConfig property type to automatically create branches that match a certain pattern.

            :param auto_branch_creation_patterns: Automated branch creation glob patterns for the Amplify app.
            :param basic_auth_config: Sets password protection for your auto created branch.
            :param build_spec: The build specification (build spec) for the autocreated branch. *Length Constraints:* Minimum length of 1. Maximum length of 25000.
            :param enable_auto_branch_creation: Enables automated branch creation for the Amplify app.
            :param enable_auto_build: Enables auto building for the auto created branch.
            :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
            :param enable_pull_request_preview: Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app. Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
            :param environment_variables: Environment variables for the auto created branch.
            :param framework: The framework for the autocreated branch.
            :param pull_request_environment_name: If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* . *Length Constraints:* Maximum length of 20. *Pattern:* (?s).*
            :param stage: Stage for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                auto_branch_creation_config_property = amplify.CfnApp.AutoBranchCreationConfigProperty(
                    auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                    basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                        enable_basic_auth=False,
                        password="password",
                        username="username"
                    ),
                    build_spec="buildSpec",
                    enable_auto_branch_creation=False,
                    enable_auto_build=False,
                    enable_performance_mode=False,
                    enable_pull_request_preview=False,
                    environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    framework="framework",
                    pull_request_environment_name="pullRequestEnvironmentName",
                    stage="stage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0af36cdd2d98df90e240d5db6b05a42d7e0ae596fe63a890d4553ede9f6bb05)
                check_type(argname="argument auto_branch_creation_patterns", value=auto_branch_creation_patterns, expected_type=type_hints["auto_branch_creation_patterns"])
                check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
                check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
                check_type(argname="argument enable_auto_branch_creation", value=enable_auto_branch_creation, expected_type=type_hints["enable_auto_branch_creation"])
                check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
                check_type(argname="argument enable_performance_mode", value=enable_performance_mode, expected_type=type_hints["enable_performance_mode"])
                check_type(argname="argument enable_pull_request_preview", value=enable_pull_request_preview, expected_type=type_hints["enable_pull_request_preview"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
                check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
                check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_branch_creation_patterns is not None:
                self._values["auto_branch_creation_patterns"] = auto_branch_creation_patterns
            if basic_auth_config is not None:
                self._values["basic_auth_config"] = basic_auth_config
            if build_spec is not None:
                self._values["build_spec"] = build_spec
            if enable_auto_branch_creation is not None:
                self._values["enable_auto_branch_creation"] = enable_auto_branch_creation
            if enable_auto_build is not None:
                self._values["enable_auto_build"] = enable_auto_build
            if enable_performance_mode is not None:
                self._values["enable_performance_mode"] = enable_performance_mode
            if enable_pull_request_preview is not None:
                self._values["enable_pull_request_preview"] = enable_pull_request_preview
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if framework is not None:
                self._values["framework"] = framework
            if pull_request_environment_name is not None:
                self._values["pull_request_environment_name"] = pull_request_environment_name
            if stage is not None:
                self._values["stage"] = stage

        @builtins.property
        def auto_branch_creation_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Automated branch creation glob patterns for the Amplify app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-autobranchcreationpatterns
            '''
            result = self._values.get("auto_branch_creation_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def basic_auth_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.BasicAuthConfigProperty"]]:
            '''Sets password protection for your auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-basicauthconfig
            '''
            result = self._values.get("basic_auth_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.BasicAuthConfigProperty"]], result)

        @builtins.property
        def build_spec(self) -> typing.Optional[builtins.str]:
            '''The build specification (build spec) for the autocreated branch.

            *Length Constraints:* Minimum length of 1. Maximum length of 25000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-buildspec
            '''
            result = self._values.get("build_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_auto_branch_creation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables automated branch creation for the Amplify app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobranchcreation
            '''
            result = self._values.get("enable_auto_branch_creation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def enable_auto_build(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables auto building for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobuild
            '''
            result = self._values.get("enable_auto_build")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def enable_performance_mode(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables performance mode for the branch.

            Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableperformancemode
            '''
            result = self._values.get("enable_performance_mode")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def enable_pull_request_preview(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app.

            Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

            To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

            For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enablepullrequestpreview
            '''
            result = self._values.get("enable_pull_request_preview")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]]:
            '''Environment variables for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]], result)

        @builtins.property
        def framework(self) -> typing.Optional[builtins.str]:
            '''The framework for the autocreated branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-framework
            '''
            result = self._values.get("framework")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
            '''If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews.

            For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI.

            To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

            If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed.

            For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

            *Length Constraints:* Maximum length of 20.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-pullrequestenvironmentname
            '''
            result = self._values.get("pull_request_environment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage(self) -> typing.Optional[builtins.str]:
            '''Stage for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-stage
            '''
            result = self._values.get("stage")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoBranchCreationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnApp.BasicAuthConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_basic_auth": "enableBasicAuth",
            "password": "password",
            "username": "username",
        },
    )
    class BasicAuthConfigProperty:
        def __init__(
            self,
            *,
            enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the BasicAuthConfig property type to set password protection at an app level to all your branches.

            :param enable_basic_auth: Enables basic authorization for the Amplify app's branches.
            :param password: The password for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.
            :param username: The user name for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                basic_auth_config_property = amplify.CfnApp.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53ca9d287c59aa571660643589355b1c8948432b620e5e69ce27d9e88da4443d)
                check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_basic_auth is not None:
                self._values["enable_basic_auth"] = enable_basic_auth
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def enable_basic_auth(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables basic authorization for the Amplify app's branches.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-enablebasicauth
            '''
            result = self._values.get("enable_basic_auth")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The user name for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnApp.CustomRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source": "source",
            "target": "target",
            "condition": "condition",
            "status": "status",
        },
    )
    class CustomRuleProperty:
        def __init__(
            self,
            *,
            source: builtins.str,
            target: builtins.str,
            condition: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The CustomRule property type allows you to specify redirects, rewrites, and reverse proxies.

            Redirects enable a web app to reroute navigation from one URL to another.

            :param source: The source pattern for a URL rewrite or redirect rule. *Length Constraints:* Minimum length of 1. Maximum length of 2048. *Pattern:* (?s).+
            :param target: The target pattern for a URL rewrite or redirect rule. *Length Constraints:* Minimum length of 1. Maximum length of 2048. *Pattern:* (?s).+
            :param condition: The condition for a URL rewrite or redirect rule, such as a country code. *Length Constraints:* Minimum length of 0. Maximum length of 2048. *Pattern:* (?s).*
            :param status: The status code for a URL rewrite or redirect rule. - **200** - Represents a 200 rewrite rule. - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL. - **302** - Represents a 302 temporary redirect rule. - **404** - Represents a 404 redirect rule. - **404-200** - Represents a 404 rewrite rule. *Length Constraints:* Minimum length of 3. Maximum length of 7. *Pattern:* .{3,7}

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                custom_rule_property = amplify.CfnApp.CustomRuleProperty(
                    source="source",
                    target="target",
                
                    # the properties below are optional
                    condition="condition",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0857683e4163f353c24f2174f94e3175fac8c4f2e9063683234700290f3d379c)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source": source,
                "target": target,
            }
            if condition is not None:
                self._values["condition"] = condition
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def source(self) -> builtins.str:
            '''The source pattern for a URL rewrite or redirect rule.

            *Length Constraints:* Minimum length of 1. Maximum length of 2048.

            *Pattern:* (?s).+

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target(self) -> builtins.str:
            '''The target pattern for a URL rewrite or redirect rule.

            *Length Constraints:* Minimum length of 1. Maximum length of 2048.

            *Pattern:* (?s).+

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The condition for a URL rewrite or redirect rule, such as a country code.

            *Length Constraints:* Minimum length of 0. Maximum length of 2048.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status code for a URL rewrite or redirect rule.

            - **200** - Represents a 200 rewrite rule.
            - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL.
            - **302** - Represents a 302 temporary redirect rule.
            - **404** - Represents a 404 redirect rule.
            - **404-200** - Represents a 404 rewrite rule.

            *Length Constraints:* Minimum length of 3. Maximum length of 7.

            *Pattern:* .{3,7}

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnApp.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''Environment variables are key-value pairs that are available at build time.

            Set environment variables for all branches in your app.

            :param name: The environment variable name. *Length Constraints:* Maximum length of 255. *Pattern:* (?s).*
            :param value: The environment variable value. *Length Constraints:* Maximum length of 5500. *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                environment_variable_property = amplify.CfnApp.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a464ed55ca87d5ae228d5260eb1dce153db71c6d814611892808178d1915acdf)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The environment variable name.

            *Length Constraints:* Maximum length of 255.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The environment variable value.

            *Length Constraints:* Maximum length of 5500.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "access_token": "accessToken",
        "auto_branch_creation_config": "autoBranchCreationConfig",
        "basic_auth_config": "basicAuthConfig",
        "build_spec": "buildSpec",
        "custom_headers": "customHeaders",
        "custom_rules": "customRules",
        "description": "description",
        "enable_branch_auto_deletion": "enableBranchAutoDeletion",
        "environment_variables": "environmentVariables",
        "iam_service_role": "iamServiceRole",
        "oauth_token": "oauthToken",
        "platform": "platform",
        "repository": "repository",
        "tags": "tags",
    },
)
class CfnAppProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        auto_branch_creation_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        custom_headers: typing.Optional[builtins.str] = None,
        custom_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        iam_service_role: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApp``.

        :param name: The name for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param access_token: The personal access token for a GitHub repository for an Amplify app. The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored. Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` . You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Minimum length of 1. Maximum length of 255.
        :param auto_branch_creation_config: Sets the configuration for your automatic branch creation.
        :param basic_auth_config: The credentials for basic authorization for an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param custom_headers: The custom HTTP headers for an Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 25000. *Pattern:* (?s).*
        :param custom_rules: The custom rewrite and redirect rules for an Amplify app.
        :param description: The description for an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_branch_auto_deletion: Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.
        :param environment_variables: The environment variables map for an Amplify app.
        :param iam_service_role: The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 1000. *Pattern:* (?s).*
        :param oauth_token: The OAuth token for a third-party source control system for an Amplify app. The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored. Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` . You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param platform: The platform for the Amplify app. For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .
        :param repository: The repository for an Amplify app. *Pattern:* (?s).*
        :param tags: The tag for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            cfn_app_props = amplify.CfnAppProps(
                name="name",
            
                # the properties below are optional
                access_token="accessToken",
                auto_branch_creation_config=amplify.CfnApp.AutoBranchCreationConfigProperty(
                    auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                    basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                        enable_basic_auth=False,
                        password="password",
                        username="username"
                    ),
                    build_spec="buildSpec",
                    enable_auto_branch_creation=False,
                    enable_auto_build=False,
                    enable_performance_mode=False,
                    enable_pull_request_preview=False,
                    environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    framework="framework",
                    pull_request_environment_name="pullRequestEnvironmentName",
                    stage="stage"
                ),
                basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                build_spec="buildSpec",
                custom_headers="customHeaders",
                custom_rules=[amplify.CfnApp.CustomRuleProperty(
                    source="source",
                    target="target",
            
                    # the properties below are optional
                    condition="condition",
                    status="status"
                )],
                description="description",
                enable_branch_auto_deletion=False,
                environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                iam_service_role="iamServiceRole",
                oauth_token="oauthToken",
                platform="platform",
                repository="repository",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c547002d958c31b5e4e0088f44d0cbe129912efaaa857da6f51258547be9f9ca)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument auto_branch_creation_config", value=auto_branch_creation_config, expected_type=type_hints["auto_branch_creation_config"])
            check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument custom_headers", value=custom_headers, expected_type=type_hints["custom_headers"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_branch_auto_deletion", value=enable_branch_auto_deletion, expected_type=type_hints["enable_branch_auto_deletion"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument iam_service_role", value=iam_service_role, expected_type=type_hints["iam_service_role"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if auto_branch_creation_config is not None:
            self._values["auto_branch_creation_config"] = auto_branch_creation_config
        if basic_auth_config is not None:
            self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if description is not None:
            self._values["description"] = description
        if enable_branch_auto_deletion is not None:
            self._values["enable_branch_auto_deletion"] = enable_branch_auto_deletion
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if iam_service_role is not None:
            self._values["iam_service_role"] = iam_service_role
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token
        if platform is not None:
            self._values["platform"] = platform
        if repository is not None:
            self._values["repository"] = repository
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''The personal access token for a GitHub repository for an Amplify app.

        The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored.

        Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` .

        You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_branch_creation_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.AutoBranchCreationConfigProperty]]:
        '''Sets the configuration for your automatic branch creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        '''
        result = self._values.get("auto_branch_creation_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.AutoBranchCreationConfigProperty]], result)

    @builtins.property
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.BasicAuthConfigProperty]]:
        '''The credentials for basic authorization for an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        '''
        result = self._values.get("basic_auth_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.BasicAuthConfigProperty]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_headers(self) -> typing.Optional[builtins.str]:
        '''The custom HTTP headers for an Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 25000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customheaders
        '''
        result = self._values.get("custom_headers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.CustomRuleProperty]]]]:
        '''The custom rewrite and redirect rules for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.CustomRuleProperty]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_branch_auto_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-enablebranchautodeletion
        '''
        result = self._values.get("enable_branch_auto_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.EnvironmentVariableProperty]]]]:
        '''The environment variables map for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.EnvironmentVariableProperty]]]], result)

    @builtins.property
    def iam_service_role(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        '''
        result = self._values.get("iam_service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[builtins.str]:
        '''The OAuth token for a third-party source control system for an Amplify app.

        The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored.

        Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` .

        You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform for the Amplify app.

        For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The repository for an Amplify app.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tag for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBranch(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.CfnBranch",
):
    '''A CloudFormation ``AWS::Amplify::Branch``.

    The AWS::Amplify::Branch resource specifies a new branch within an app.

    :cloudformationResource: AWS::Amplify::Branch
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amplify as amplify
        
        cfn_branch = amplify.CfnBranch(self, "MyCfnBranch",
            app_id="appId",
            branch_name="branchName",
        
            # the properties below are optional
            basic_auth_config=amplify.CfnBranch.BasicAuthConfigProperty(
                password="password",
                username="username",
        
                # the properties below are optional
                enable_basic_auth=False
            ),
            build_spec="buildSpec",
            description="description",
            enable_auto_build=False,
            enable_performance_mode=False,
            enable_pull_request_preview=False,
            environment_variables=[amplify.CfnBranch.EnvironmentVariableProperty(
                name="name",
                value="value"
            )],
            framework="framework",
            pull_request_environment_name="pullRequestEnvironmentName",
            stage="stage",
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
        app_id: builtins.str,
        branch_name: builtins.str,
        basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBranch.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBranch.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        framework: typing.Optional[builtins.str] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Amplify::Branch``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param branch_name: The name for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param description: The description for the branch that is part of an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_auto_build: Enables auto building for the branch.
        :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
        :param environment_variables: The environment variables for the branch.
        :param framework: The framework for the branch.
        :param pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* . *Length Constraints:* Maximum length of 20. *Pattern:* (?s).*
        :param stage: Describes the current stage for the branch. *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST
        :param tags: The tag for the branch.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae54455d3d5af65245a98458f974e24a4452e78e7b783b0954949bfeac4bce1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBranchProps(
            app_id=app_id,
            branch_name=branch_name,
            basic_auth_config=basic_auth_config,
            build_spec=build_spec,
            description=description,
            enable_auto_build=enable_auto_build,
            enable_performance_mode=enable_performance_mode,
            enable_pull_request_preview=enable_pull_request_preview,
            environment_variables=environment_variables,
            framework=framework,
            pull_request_environment_name=pull_request_environment_name,
            stage=stage,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0570b0f9ea113f5e51234698cb616024eeeda61b5f94ced0132c086bf1ed72aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24f7627463f6a6cad1a615fa7f2aead3962939f68a1156fc0f9219102b3b9f08)
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
        '''ARN for a branch, part of an Amplify App.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrBranchName")
    def attr_branch_name(self) -> builtins.str:
        '''Name for a branch, part of an Amplify App.

        :cloudformationAttribute: BranchName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBranchName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tag for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e325fedb60c9a7c317f7be1cc30a0ab63a5587c180bb9d4fbecc61ae7bd43e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''The name for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2150d4306517c8b8af7a047fa9a72722040ddc8ec92fb0632b43887b440216e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value)

    @builtins.property
    @jsii.member(jsii_name="basicAuthConfig")
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBranch.BasicAuthConfigProperty"]]:
        '''The basic authorization credentials for a branch of an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBranch.BasicAuthConfigProperty"]], jsii.get(self, "basicAuthConfig"))

    @basic_auth_config.setter
    def basic_auth_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBranch.BasicAuthConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea97a250bb087e54bdb9839c21179235bebf3481b32bf7d7b02891358c1a4da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="buildSpec")
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildSpec"))

    @build_spec.setter
    def build_spec(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afd31bcf2f8caa89e7babd1de1c2d12308f7b00427086ada56bc41a28465a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildSpec", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the branch that is part of an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d372e31f76f850dafb7c7d4eb1f331d33fe97f120ca6c915c53d7a516d1c52f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enableAutoBuild")
    def enable_auto_build(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables auto building for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableAutoBuild"))

    @enable_auto_build.setter
    def enable_auto_build(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b620fdfa28ccb436b9323410492e0c866850d73decfe6436a07ff144b830d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoBuild", value)

    @builtins.property
    @jsii.member(jsii_name="enablePerformanceMode")
    def enable_performance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableperformancemode
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enablePerformanceMode"))

    @enable_performance_mode.setter
    def enable_performance_mode(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922c1d1174c05de33f9c5d97a475641a4c4aab8b0abb04055ea23972939fe61e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePerformanceMode", value)

    @builtins.property
    @jsii.member(jsii_name="enablePullRequestPreview")
    def enable_pull_request_preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch.

        If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

        For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enablePullRequestPreview"))

    @enable_pull_request_preview.setter
    def enable_pull_request_preview(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac33618c47b126ed1f0bd5f51e5892e8961309386be955c6f39329524da86b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePullRequestPreview", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBranch.EnvironmentVariableProperty"]]]]:
        '''The environment variables for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBranch.EnvironmentVariableProperty"]]]], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBranch.EnvironmentVariableProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c38dce7f10f082bc47720d8facce56a0afe0b73b1e44024d78975fd3c76944b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="framework")
    def framework(self) -> typing.Optional[builtins.str]:
        '''The framework for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-framework
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "framework"))

    @framework.setter
    def framework(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16567042afb581540e47e92b110d1083ed38f63ac7054d82933939d125cf1a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "framework", value)

    @builtins.property
    @jsii.member(jsii_name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews.

        For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

        *Length Constraints:* Maximum length of 20.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pullRequestEnvironmentName"))

    @pull_request_environment_name.setter
    def pull_request_environment_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c3e6f9e0de0bc96367289d5c6f20ed36be294724a94b69984a3bbbe8b86a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullRequestEnvironmentName", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[builtins.str]:
        '''Describes the current stage for the branch.

        *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec971cd709f279c324312ccb382b176cc5643d0c9f5a60dd78c45ac656f24bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnBranch.BasicAuthConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "username": "username",
            "enable_basic_auth": "enableBasicAuth",
        },
    )
    class BasicAuthConfigProperty:
        def __init__(
            self,
            *,
            password: builtins.str,
            username: builtins.str,
            enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Use the BasicAuthConfig property type to set password protection for a specific branch.

            :param password: The password for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.
            :param username: The user name for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.
            :param enable_basic_auth: Enables basic authorization for the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                basic_auth_config_property = amplify.CfnBranch.BasicAuthConfigProperty(
                    password="password",
                    username="username",
                
                    # the properties below are optional
                    enable_basic_auth=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a1c81aca3a46996a7cf3912747f70f94f0dae7aedb1daa6c1c7eb646a1b4eb2)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
                check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }
            if enable_basic_auth is not None:
                self._values["enable_basic_auth"] = enable_basic_auth

        @builtins.property
        def password(self) -> builtins.str:
            '''The password for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The user name for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def enable_basic_auth(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables basic authorization for the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-enablebasicauth
            '''
            result = self._values.get("enable_basic_auth")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnBranch.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''The EnvironmentVariable property type sets environment variables for a specific branch.

            Environment variables are key-value pairs that are available at build time.

            :param name: The environment variable name. *Length Constraints:* Maximum length of 255. *Pattern:* (?s).*
            :param value: The environment variable value. *Length Constraints:* Maximum length of 5500. *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                environment_variable_property = amplify.CfnBranch.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb803dc15df951d430798b81d922acf35888c8dcb6caa82ab6009bc4fa163858)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The environment variable name.

            *Length Constraints:* Maximum length of 255.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The environment variable value.

            *Length Constraints:* Maximum length of 5500.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.CfnBranchProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "branch_name": "branchName",
        "basic_auth_config": "basicAuthConfig",
        "build_spec": "buildSpec",
        "description": "description",
        "enable_auto_build": "enableAutoBuild",
        "enable_performance_mode": "enablePerformanceMode",
        "enable_pull_request_preview": "enablePullRequestPreview",
        "environment_variables": "environmentVariables",
        "framework": "framework",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "stage": "stage",
        "tags": "tags",
    },
)
class CfnBranchProps:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        branch_name: builtins.str,
        basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBranch.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBranch.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        framework: typing.Optional[builtins.str] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBranch``.

        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param branch_name: The name for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param description: The description for the branch that is part of an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_auto_build: Enables auto building for the branch.
        :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
        :param environment_variables: The environment variables for the branch.
        :param framework: The framework for the branch.
        :param pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* . *Length Constraints:* Maximum length of 20. *Pattern:* (?s).*
        :param stage: Describes the current stage for the branch. *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST
        :param tags: The tag for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            cfn_branch_props = amplify.CfnBranchProps(
                app_id="appId",
                branch_name="branchName",
            
                # the properties below are optional
                basic_auth_config=amplify.CfnBranch.BasicAuthConfigProperty(
                    password="password",
                    username="username",
            
                    # the properties below are optional
                    enable_basic_auth=False
                ),
                build_spec="buildSpec",
                description="description",
                enable_auto_build=False,
                enable_performance_mode=False,
                enable_pull_request_preview=False,
                environment_variables=[amplify.CfnBranch.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                framework="framework",
                pull_request_environment_name="pullRequestEnvironmentName",
                stage="stage",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58765b995e3a3c35dcd3203d8be9e85a8af1094b0ed6889553c10c59f17e9662)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
            check_type(argname="argument enable_performance_mode", value=enable_performance_mode, expected_type=type_hints["enable_performance_mode"])
            check_type(argname="argument enable_pull_request_preview", value=enable_pull_request_preview, expected_type=type_hints["enable_pull_request_preview"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "branch_name": branch_name,
        }
        if basic_auth_config is not None:
            self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if description is not None:
            self._values["description"] = description
        if enable_auto_build is not None:
            self._values["enable_auto_build"] = enable_auto_build
        if enable_performance_mode is not None:
            self._values["enable_performance_mode"] = enable_performance_mode
        if enable_pull_request_preview is not None:
            self._values["enable_pull_request_preview"] = enable_pull_request_preview
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if framework is not None:
            self._values["framework"] = framework
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if stage is not None:
            self._values["stage"] = stage
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''The name for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        '''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBranch.BasicAuthConfigProperty]]:
        '''The basic authorization credentials for a branch of an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        '''
        result = self._values.get("basic_auth_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBranch.BasicAuthConfigProperty]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the branch that is part of an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_build(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables auto building for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        '''
        result = self._values.get("enable_auto_build")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def enable_performance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableperformancemode
        '''
        result = self._values.get("enable_performance_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def enable_pull_request_preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch.

        If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

        For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        '''
        result = self._values.get("enable_pull_request_preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBranch.EnvironmentVariableProperty]]]]:
        '''The environment variables for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBranch.EnvironmentVariableProperty]]]], result)

    @builtins.property
    def framework(self) -> typing.Optional[builtins.str]:
        '''The framework for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-framework
        '''
        result = self._values.get("framework")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews.

        For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

        *Length Constraints:* Maximum length of 20.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''Describes the current stage for the branch.

        *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tag for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDomain(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.CfnDomain",
):
    '''A CloudFormation ``AWS::Amplify::Domain``.

    The AWS::Amplify::Domain resource allows you to connect a custom domain to your app.

    :cloudformationResource: AWS::Amplify::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amplify as amplify
        
        cfn_domain = amplify.CfnDomain(self, "MyCfnDomain",
            app_id="appId",
            domain_name="domainName",
            sub_domain_settings=[amplify.CfnDomain.SubDomainSettingProperty(
                branch_name="branchName",
                prefix="prefix"
            )],
        
            # the properties below are optional
            auto_sub_domain_creation_patterns=["autoSubDomainCreationPatterns"],
            auto_sub_domain_iam_role="autoSubDomainIamRole",
            enable_auto_sub_domain=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        app_id: builtins.str,
        domain_name: builtins.str,
        sub_domain_settings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.SubDomainSettingProperty", typing.Dict[builtins.str, typing.Any]]]]],
        auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
        enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Amplify::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param domain_name: The domain name for the domain association. *Length Constraints:* Maximum length of 255. *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$
        :param sub_domain_settings: The setting for the subdomain.
        :param auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains. *Length Constraints:* Maximum length of 1000. *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+
        :param enable_auto_sub_domain: Enables the automated creation of subdomains for branches.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcad90986ae427b69544c7f362f745108911b66125dff5eccc810b17f2ba99b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            app_id=app_id,
            domain_name=domain_name,
            sub_domain_settings=sub_domain_settings,
            auto_sub_domain_creation_patterns=auto_sub_domain_creation_patterns,
            auto_sub_domain_iam_role=auto_sub_domain_iam_role,
            enable_auto_sub_domain=enable_auto_sub_domain,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381b713e8667226770767758b43f8105dfda8bde777f73501ce85809fe27bee5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf314e52e1ea91ffb655d297ef76100e5e540eb3b1ff8882dafab743cd8b1383)
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
        '''ARN for the Domain Association.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoSubDomainCreationPatterns")
    def attr_auto_sub_domain_creation_patterns(self) -> typing.List[builtins.str]:
        '''Branch patterns for the automatically created subdomain.

        :cloudformationAttribute: AutoSubDomainCreationPatterns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrAutoSubDomainCreationPatterns"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoSubDomainIamRole")
    def attr_auto_sub_domain_iam_role(self) -> builtins.str:
        '''The IAM service role for the subdomain.

        :cloudformationAttribute: AutoSubDomainIAMRole
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAutoSubDomainIamRole"))

    @builtins.property
    @jsii.member(jsii_name="attrCertificateRecord")
    def attr_certificate_record(self) -> builtins.str:
        '''DNS Record for certificate verification.

        :cloudformationAttribute: CertificateRecord
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCertificateRecord"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''Name of the domain.

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainStatus")
    def attr_domain_status(self) -> builtins.str:
        '''Status for the Domain Association.

        :cloudformationAttribute: DomainStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrEnableAutoSubDomain")
    def attr_enable_auto_sub_domain(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''Specifies whether the automated creation of subdomains for branches is enabled.

        :cloudformationAttribute: EnableAutoSubDomain
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrEnableAutoSubDomain"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusReason")
    def attr_status_reason(self) -> builtins.str:
        '''Reason for the current status of the domain.

        :cloudformationAttribute: StatusReason
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusReason"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ea3f2fe871af1076106e23c65ec477c68a24f9201e979b06720796280a5bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name for the domain association.

        *Length Constraints:* Maximum length of 255.

        *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d05a2d9eb69278804b0c5a2658fec92f0ac6d287dec4aa6fe5ed9674fd4325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="subDomainSettings")
    def sub_domain_settings(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.SubDomainSettingProperty"]]]:
        '''The setting for the subdomain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.SubDomainSettingProperty"]]], jsii.get(self, "subDomainSettings"))

    @sub_domain_settings.setter
    def sub_domain_settings(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.SubDomainSettingProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10d5558f90b26f77dc405fe86464a18a91184c5b6bf4bd7a7d07e1c8fab3eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subDomainSettings", value)

    @builtins.property
    @jsii.member(jsii_name="autoSubDomainCreationPatterns")
    def auto_sub_domain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the branch patterns for automatic subdomain creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomaincreationpatterns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoSubDomainCreationPatterns"))

    @auto_sub_domain_creation_patterns.setter
    def auto_sub_domain_creation_patterns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00afb3cf5ecae89c8d6ba6fabdeb995e5c0ab9fa6a8b0fd60d80474b33f1df61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubDomainCreationPatterns", value)

    @builtins.property
    @jsii.member(jsii_name="autoSubDomainIamRole")
    def auto_sub_domain_iam_role(self) -> typing.Optional[builtins.str]:
        '''The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomainiamrole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoSubDomainIamRole"))

    @auto_sub_domain_iam_role.setter
    def auto_sub_domain_iam_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782e66e12f275620aa8f41fd05ad58239696590373588a8d959ba88f3122c939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubDomainIamRole", value)

    @builtins.property
    @jsii.member(jsii_name="enableAutoSubDomain")
    def enable_auto_sub_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables the automated creation of subdomains for branches.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-enableautosubdomain
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableAutoSubDomain"))

    @enable_auto_sub_domain.setter
    def enable_auto_sub_domain(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763945f88c06feda2681fea779bebe32558139e36367d90e56b89dc82850a032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoSubDomain", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplify.CfnDomain.SubDomainSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"branch_name": "branchName", "prefix": "prefix"},
    )
    class SubDomainSettingProperty:
        def __init__(self, *, branch_name: builtins.str, prefix: builtins.str) -> None:
            '''The SubDomainSetting property type enables you to connect a subdomain (for example, example.exampledomain.com) to a specific branch.

            :param branch_name: The branch name setting for the subdomain. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
            :param prefix: The prefix setting for the subdomain. *Length Constraints:* Maximum length of 255. *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplify as amplify
                
                sub_domain_setting_property = amplify.CfnDomain.SubDomainSettingProperty(
                    branch_name="branchName",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6cf478b2b1ad15b0cad30f4ef3c8ef85983a10f093aea27266dae8310fe0fee1)
                check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "branch_name": branch_name,
                "prefix": prefix,
            }

        @builtins.property
        def branch_name(self) -> builtins.str:
            '''The branch name setting for the subdomain.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            *Pattern:* (?s).+

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-branchname
            '''
            result = self._values.get("branch_name")
            assert result is not None, "Required property 'branch_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> builtins.str:
            '''The prefix setting for the subdomain.

            *Length Constraints:* Maximum length of 255.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-prefix
            '''
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubDomainSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "domain_name": "domainName",
        "sub_domain_settings": "subDomainSettings",
        "auto_sub_domain_creation_patterns": "autoSubDomainCreationPatterns",
        "auto_sub_domain_iam_role": "autoSubDomainIamRole",
        "enable_auto_sub_domain": "enableAutoSubDomain",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        domain_name: builtins.str,
        sub_domain_settings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]]]]],
        auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
        enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomain``.

        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param domain_name: The domain name for the domain association. *Length Constraints:* Maximum length of 255. *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$
        :param sub_domain_settings: The setting for the subdomain.
        :param auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains. *Length Constraints:* Maximum length of 1000. *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+
        :param enable_auto_sub_domain: Enables the automated creation of subdomains for branches.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            cfn_domain_props = amplify.CfnDomainProps(
                app_id="appId",
                domain_name="domainName",
                sub_domain_settings=[amplify.CfnDomain.SubDomainSettingProperty(
                    branch_name="branchName",
                    prefix="prefix"
                )],
            
                # the properties below are optional
                auto_sub_domain_creation_patterns=["autoSubDomainCreationPatterns"],
                auto_sub_domain_iam_role="autoSubDomainIamRole",
                enable_auto_sub_domain=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028b81cae4e9723af6c8b32ab71ba4c313c8a84d4fc64edd7dc009aeeee8da5f)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument sub_domain_settings", value=sub_domain_settings, expected_type=type_hints["sub_domain_settings"])
            check_type(argname="argument auto_sub_domain_creation_patterns", value=auto_sub_domain_creation_patterns, expected_type=type_hints["auto_sub_domain_creation_patterns"])
            check_type(argname="argument auto_sub_domain_iam_role", value=auto_sub_domain_iam_role, expected_type=type_hints["auto_sub_domain_iam_role"])
            check_type(argname="argument enable_auto_sub_domain", value=enable_auto_sub_domain, expected_type=type_hints["enable_auto_sub_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "domain_name": domain_name,
            "sub_domain_settings": sub_domain_settings,
        }
        if auto_sub_domain_creation_patterns is not None:
            self._values["auto_sub_domain_creation_patterns"] = auto_sub_domain_creation_patterns
        if auto_sub_domain_iam_role is not None:
            self._values["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role
        if enable_auto_sub_domain is not None:
            self._values["enable_auto_sub_domain"] = enable_auto_sub_domain

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name for the domain association.

        *Length Constraints:* Maximum length of 255.

        *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_domain_settings(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.SubDomainSettingProperty]]]:
        '''The setting for the subdomain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        '''
        result = self._values.get("sub_domain_settings")
        assert result is not None, "Required property 'sub_domain_settings' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.SubDomainSettingProperty]]], result)

    @builtins.property
    def auto_sub_domain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the branch patterns for automatic subdomain creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomaincreationpatterns
        '''
        result = self._values.get("auto_sub_domain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_sub_domain_iam_role(self) -> typing.Optional[builtins.str]:
        '''The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomainiamrole
        '''
        result = self._values.get("auto_sub_domain_iam_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_sub_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables the automated creation of subdomains for branches.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-enableautosubdomain
        '''
        result = self._values.get("enable_auto_sub_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.CodeCommitSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository"},
)
class CodeCommitSourceCodeProviderProps:
    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_codecommit_692dd32c.IRepository,
    ) -> None:
        '''(experimental) Properties for a CodeCommit source code provider.

        :param repository: (experimental) The CodeCommit repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_codecommit as codecommit
            
            
            repository = codecommit.Repository(self, "Repo",
                repository_name="my-repo"
            )
            
            amplify_app = amplify.App(self, "App",
                source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345157c20d08b130c79585b5ce878c85941077868619ff57bc7e2e22286d5f38)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }

    @builtins.property
    def repository(self) -> _aws_cdk_aws_codecommit_692dd32c.IRepository:
        '''(experimental) The CodeCommit repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_aws_cdk_aws_codecommit_692dd32c.IRepository, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.CustomResponseHeader",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "pattern": "pattern"},
)
class CustomResponseHeader:
    def __init__(
        self,
        *,
        headers: typing.Mapping[builtins.str, builtins.str],
        pattern: builtins.str,
    ) -> None:
        '''(experimental) Custom response header of an Amplify App.

        :param headers: (experimental) The map of custom headers to be applied.
        :param pattern: (experimental) These custom headers will be applied to all URL file paths that match this pattern.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            custom_response_header = amplify.CustomResponseHeader(
                headers={
                    "headers_key": "headers"
                },
                pattern="pattern"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb280fccd6a370bbbf11d9edff44e37ba68d6928807dddc249dc311095b2be9)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "headers": headers,
            "pattern": pattern,
        }

    @builtins.property
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The map of custom headers to be applied.

        :stability: experimental
        '''
        result = self._values.get("headers")
        assert result is not None, "Required property 'headers' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''(experimental) These custom headers will be applied to all URL file paths that match this pattern.

        :stability: experimental
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResponseHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomRule(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amplify.CustomRule"):
    '''(experimental) Custom rewrite/redirect rule for an Amplify App.

    :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        
        amplify_app.add_custom_rule({
            "source": "/docs/specific-filename.html",
            "target": "/documents/different-filename.html",
            "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
        })
    '''

    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional["RedirectStatus"] = None,
    ) -> None:
        '''
        :param source: (experimental) The source pattern for a URL rewrite or redirect rule.
        :param target: (experimental) The target pattern for a URL rewrite or redirect rule.
        :param condition: (experimental) The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: (experimental) The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        :stability: experimental
        '''
        options = CustomRuleOptions(
            source=source, target=target, condition=condition, status=status
        )

        jsii.create(self.__class__, self, [options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SINGLE_PAGE_APPLICATION_REDIRECT")
    def SINGLE_PAGE_APPLICATION_REDIRECT(cls) -> "CustomRule":
        '''(experimental) Sets up a 200 rewrite for all paths to ``index.html`` except for path containing a file extension.

        :stability: experimental
        '''
        return typing.cast("CustomRule", jsii.sget(cls, "SINGLE_PAGE_APPLICATION_REDIRECT"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''(experimental) The source pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        '''(experimental) The target pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The condition for a URL rewrite or redirect rule, e.g. country code.

        :default: - no condition

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional["RedirectStatus"]:
        '''(experimental) The status code for a URL rewrite or redirect rule.

        :default: PERMANENT_REDIRECT

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional["RedirectStatus"], jsii.get(self, "status"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.CustomRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "condition": "condition",
        "status": "status",
    },
)
class CustomRuleOptions:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional["RedirectStatus"] = None,
    ) -> None:
        '''(experimental) Options for a custom rewrite/redirect rule for an Amplify App.

        :param source: (experimental) The source pattern for a URL rewrite or redirect rule.
        :param target: (experimental) The target pattern for a URL rewrite or redirect rule.
        :param condition: (experimental) The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: (experimental) The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            custom_rule_options = amplify.CustomRuleOptions(
                source="source",
                target="target",
            
                # the properties below are optional
                condition="condition",
                status=amplify.RedirectStatus.REWRITE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2e261119c6973bfbce688947f42d461b52338425e97fde0e5ac7fb04ed5247)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }
        if condition is not None:
            self._values["condition"] = condition
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) The source pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) The target pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The condition for a URL rewrite or redirect rule, e.g. country code.

        :default: - no condition

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["RedirectStatus"]:
        '''(experimental) The status code for a URL rewrite or redirect rule.

        :default: PERMANENT_REDIRECT

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["RedirectStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Domain(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.Domain",
):
    '''(experimental) An Amplify Console domain.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        # master: amplify.Branch
        # dev: amplify.Branch
        
        
        domain = amplify_app.add_domain("example.com",
            enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
            auto_subdomain_creation_patterns=["*", "pr*"]
        )
        domain.map_root(master) # map master branch to domain root
        domain.map_sub_domain(master, "www")
        domain.map_sub_domain(dev)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app: "IApp",
        auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app: (experimental) The application to which the domain must be connected.
        :param auto_sub_domain_iam_role: (experimental) The IAM role with access to Route53 when using enableAutoSubdomain. Default: the IAM role from App.grantPrincipal
        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3812136db5a4ad43710dd15f4868abb8cd6250c7cfb24bd4b374902b26129260)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            app=app,
            auto_sub_domain_iam_role=auto_sub_domain_iam_role,
            auto_subdomain_creation_patterns=auto_subdomain_creation_patterns,
            domain_name=domain_name,
            enable_auto_subdomain=enable_auto_subdomain,
            sub_domains=sub_domains,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="mapRoot")
    def map_root(self, branch: "IBranch") -> "Domain":
        '''(experimental) Maps a branch to the domain root.

        :param branch: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c84706b963ab53916cca4a03a6f63fd063a67875077e6db032fc97833fe6b58)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("Domain", jsii.invoke(self, "mapRoot", [branch]))

    @jsii.member(jsii_name="mapSubDomain")
    def map_sub_domain(
        self,
        branch: "IBranch",
        prefix: typing.Optional[builtins.str] = None,
    ) -> "Domain":
        '''(experimental) Maps a branch to a sub domain.

        :param branch: The branch.
        :param prefix: The prefix. Use '' to map to the root of the domain. Defaults to branch name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ca6cc71927e93a54c4134210227a4c448fb8f794a013fcb8748689dd0d4b1e)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast("Domain", jsii.invoke(self, "mapSubDomain", [branch, prefix]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="certificateRecord")
    def certificate_record(self) -> builtins.str:
        '''(experimental) The DNS Record for certificate verification.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateRecord"))

    @builtins.property
    @jsii.member(jsii_name="domainAutoSubDomainCreationPatterns")
    def domain_auto_sub_domain_creation_patterns(self) -> typing.List[builtins.str]:
        '''(experimental) Branch patterns for the automatically created subdomain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainAutoSubDomainCreationPatterns"))

    @builtins.property
    @jsii.member(jsii_name="domainAutoSubDomainIamRole")
    def domain_auto_sub_domain_iam_role(self) -> builtins.str:
        '''(experimental) The IAM service role for the subdomain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainAutoSubDomainIamRole"))

    @builtins.property
    @jsii.member(jsii_name="domainEnableAutoSubDomain")
    def domain_enable_auto_sub_domain(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''(experimental) Specifies whether the automated creation of subdomains for branches is enabled.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "domainEnableAutoSubDomain"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) The name of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainStatus")
    def domain_status(self) -> builtins.str:
        '''(experimental) The status of the domain association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainStatus"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        '''(experimental) The reason for the current status of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.DomainOptions",
    jsii_struct_bases=[],
    name_mapping={
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "domain_name": "domainName",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
    },
)
class DomainOptions:
    def __init__(
        self,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Options to add a domain to an application.

        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # amplify_app: amplify.App
            # master: amplify.Branch
            # dev: amplify.Branch
            
            
            domain = amplify_app.add_domain("example.com",
                enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
                auto_subdomain_creation_patterns=["*", "pr*"]
            )
            domain.map_root(master) # map master branch to domain root
            domain.map_sub_domain(master, "www")
            domain.map_sub_domain(dev)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5f4e81d015354f82eb3159bfe0c270faadf0fd7c175645067982a00888e501)
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which should automatically create subdomains.

        :default: - all repository branches ['*', 'pr*']

        :stability: experimental
        '''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically create subdomains for connected branches.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        '''(experimental) Subdomains.

        :default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomain"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.DomainProps",
    jsii_struct_bases=[DomainOptions],
    name_mapping={
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "domain_name": "domainName",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
        "app": "app",
        "auto_sub_domain_iam_role": "autoSubDomainIamRole",
    },
)
class DomainProps(DomainOptions):
    def __init__(
        self,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
        app: "IApp",
        auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''(experimental) Properties for a Domain.

        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains
        :param app: (experimental) The application to which the domain must be connected.
        :param auto_sub_domain_iam_role: (experimental) The IAM role with access to Route53 when using enableAutoSubdomain. Default: the IAM role from App.grantPrincipal

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            import aws_cdk.aws_iam as iam
            
            # app: amplify.App
            # branch: amplify.Branch
            # role: iam.Role
            
            domain_props = amplify.DomainProps(
                app=app,
            
                # the properties below are optional
                auto_subdomain_creation_patterns=["autoSubdomainCreationPatterns"],
                auto_sub_domain_iam_role=role,
                domain_name="domainName",
                enable_auto_subdomain=False,
                sub_domains=[amplify.SubDomain(
                    branch=branch,
            
                    # the properties below are optional
                    prefix="prefix"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6bb0f1ca7e1558c6afa7580fba1358c7519bcf6518be82974b3a12a9208062)
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument auto_sub_domain_iam_role", value=auto_sub_domain_iam_role, expected_type=type_hints["auto_sub_domain_iam_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
        }
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains
        if auto_sub_domain_iam_role is not None:
            self._values["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which should automatically create subdomains.

        :default: - all repository branches ['*', 'pr*']

        :stability: experimental
        '''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically create subdomains for connected branches.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        '''(experimental) Subdomains.

        :default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomain"]], result)

    @builtins.property
    def app(self) -> "IApp":
        '''(experimental) The application to which the domain must be connected.

        :stability: experimental
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast("IApp", result)

    @builtins.property
    def auto_sub_domain_iam_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role with access to Route53 when using enableAutoSubdomain.

        :default: the IAM role from App.grantPrincipal

        :stability: experimental
        '''
        result = self._values.get("auto_sub_domain_iam_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.GitHubSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "oauth_token": "oauthToken",
        "owner": "owner",
        "repository": "repository",
    },
)
class GitHubSourceCodeProviderProps:
    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_core_f4b25747.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''(experimental) Properties for a GitHub source code provider.

        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f7fba5e451129c731de09264876451a7d4fb040d59b9c95aca89c539c22421)
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token": oauth_token,
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def oauth_token(self) -> _aws_cdk_core_f4b25747.SecretValue:
        '''(experimental) A personal access token with the ``repo`` scope.

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_aws_cdk_core_f4b25747.SecretValue, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The user or organization owning the repository.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.GitLabSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "oauth_token": "oauthToken",
        "owner": "owner",
        "repository": "repository",
    },
)
class GitLabSourceCodeProviderProps:
    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_core_f4b25747.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''(experimental) Properties for a GitLab source code provider.

        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitLabSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-gitlab-token")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394c4cd146711c120d8bf9c35d2415dfd1867a3d839cd9e7979c791c9419d21f)
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token": oauth_token,
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def oauth_token(self) -> _aws_cdk_core_f4b25747.SecretValue:
        '''(experimental) A personal access token with the ``repo`` scope.

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_aws_cdk_core_f4b25747.SecretValue, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The user or organization owning the repository.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitLabSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-amplify.IApp")
class IApp(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAppProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-amplify.IApp"

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApp).__jsii_proxy_class__ = lambda : _IAppProxy


@jsii.interface(jsii_type="@aws-cdk/aws-amplify.IBranch")
class IBranch(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) A branch.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IBranchProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) A branch.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-amplify.IBranch"

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBranch).__jsii_proxy_class__ = lambda : _IBranchProxy


@jsii.interface(jsii_type="@aws-cdk/aws-amplify.ISourceCodeProvider")
class ISourceCodeProvider(typing_extensions.Protocol):
    '''(experimental) A source code provider.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        '''(experimental) Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        ...


class _ISourceCodeProviderProxy:
    '''(experimental) A source code provider.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-amplify.ISourceCodeProvider"

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        '''(experimental) Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a23b00d6539bdc77b17baaedf3186707afa5a6f4307aa2fe1454bf6c1875af)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast("SourceCodeProviderConfig", jsii.invoke(self, "bind", [app]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceCodeProvider).__jsii_proxy_class__ = lambda : _ISourceCodeProviderProxy


@jsii.enum(jsii_type="@aws-cdk/aws-amplify.RedirectStatus")
class RedirectStatus(enum.Enum):
    '''(experimental) The status code for a URL rewrite or redirect rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        
        amplify_app.add_custom_rule({
            "source": "/docs/specific-filename.html",
            "target": "/documents/different-filename.html",
            "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
        })
    '''

    REWRITE = "REWRITE"
    '''(experimental) Rewrite (200).

    :stability: experimental
    '''
    PERMANENT_REDIRECT = "PERMANENT_REDIRECT"
    '''(experimental) Permanent redirect (301).

    :stability: experimental
    '''
    TEMPORARY_REDIRECT = "TEMPORARY_REDIRECT"
    '''(experimental) Temporary redirect (302).

    :stability: experimental
    '''
    NOT_FOUND = "NOT_FOUND"
    '''(experimental) Not found (404).

    :stability: experimental
    '''
    NOT_FOUND_REWRITE = "NOT_FOUND_REWRITE"
    '''(experimental) Not found rewrite (404).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.SourceCodeProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "access_token": "accessToken",
        "oauth_token": "oauthToken",
    },
)
class SourceCodeProviderConfig:
    def __init__(
        self,
        *,
        repository: builtins.str,
        access_token: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
        oauth_token: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    ) -> None:
        '''(experimental) Configuration for the source code provider.

        :param repository: (experimental) The repository for the application. Must use the ``HTTPS`` protocol. For example, ``https://github.com/aws/aws-cdk``.
        :param access_token: (experimental) Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. Token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is sepcified. Default: - do not use a token
        :param oauth_token: (experimental) OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. OAuth token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is specified. Default: - do not use a token

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            import aws_cdk.core as cdk
            
            # secret_value: cdk.SecretValue
            
            source_code_provider_config = amplify.SourceCodeProviderConfig(
                repository="repository",
            
                # the properties below are optional
                access_token=secret_value,
                oauth_token=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b830d1f0b4ed8f962a9b445488c1d721aa9e75598983dc07a412ce30731554)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The repository for the application. Must use the ``HTTPS`` protocol.

        For example, ``https://github.com/aws/aws-cdk``.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[_aws_cdk_core_f4b25747.SecretValue]:
        '''(experimental) Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        Token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is sepcified.

        :default: - do not use a token

        :stability: experimental
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SecretValue], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[_aws_cdk_core_f4b25747.SecretValue]:
        '''(experimental) OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        OAuth token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is specified.

        :default: - do not use a token

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCodeProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify.SubDomain",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "prefix": "prefix"},
)
class SubDomain:
    def __init__(
        self,
        *,
        branch: IBranch,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Sub domain settings.

        :param branch: (experimental) The branch.
        :param prefix: (experimental) The prefix. Use '' to map to the root of the domain Default: - the branch name

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify as amplify
            
            # branch: amplify.Branch
            
            sub_domain = amplify.SubDomain(
                branch=branch,
            
                # the properties below are optional
                prefix="prefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a23838c4a1c016f89080850da61f6301d09a9aff0ecab4050369cfb8d66633c)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def branch(self) -> IBranch:
        '''(experimental) The branch.

        :stability: experimental
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(IBranch, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix.

        Use '' to map to the root of the domain

        :default: - the branch name

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApp, _aws_cdk_aws_iam_940a1ce0.IGrantable)
class App(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.App",
):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                patterns=["feature/*", "test/*"]),
            auto_branch_deletion=True
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_name: typing.Optional[builtins.str] = None,
        auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_branch_deletion: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        source_code_provider: typing.Optional[ISourceCodeProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: (experimental) The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: (experimental) The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param auto_branch_deletion: (experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository. Default: false
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: (experimental) BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param custom_response_headers: (experimental) The custom HTTP response headers for an Amplify app. Default: - no custom response headers
        :param custom_rules: (experimental) Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: (experimental) A description for the application. Default: - no description
        :param environment_variables: (experimental) Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param role: (experimental) The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: (experimental) The source code provider for this application. Default: - not connected to a source code provider

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd9e80edafcb9da39e2ba9e0f5fb346d03475818387c23e6eb6ef2c3dfd2259)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppProps(
            app_name=app_name,
            auto_branch_creation=auto_branch_creation,
            auto_branch_deletion=auto_branch_deletion,
            basic_auth=basic_auth,
            build_spec=build_spec,
            custom_response_headers=custom_response_headers,
            custom_rules=custom_rules,
            description=description,
            environment_variables=environment_variables,
            role=role,
            source_code_provider=source_code_provider,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAppId")
    @builtins.classmethod
    def from_app_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        app_id: builtins.str,
    ) -> IApp:
        '''(experimental) Import an existing application.

        :param scope: -
        :param id: -
        :param app_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b13d4324c46fd14239d37b05bf08894cff7f10fba3df35f46ad8ec4251bcc68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
        return typing.cast(IApp, jsii.sinvoke(cls, "fromAppId", [scope, id, app_id]))

    @jsii.member(jsii_name="addAutoBranchEnvironment")
    def add_auto_branch_environment(
        self,
        name: builtins.str,
        value: builtins.str,
    ) -> "App":
        '''(experimental) Adds an environment variable to the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6599ef9359e6edb94225440082ca6bbb912f060bfddce983a0dc0d4a7d52f1e1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("App", jsii.invoke(self, "addAutoBranchEnvironment", [name, value]))

    @jsii.member(jsii_name="addBranch")
    def add_branch(
        self,
        id: builtins.str,
        *,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> "Branch":
        '''(experimental) Adds a branch to this application.

        :param id: -
        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc338ecfbc7c7ce2f6ef47f6d20df85a0d41461f158f56955bfa63ea0221f3a8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = BranchOptions(
            asset=asset,
            auto_build=auto_build,
            basic_auth=basic_auth,
            branch_name=branch_name,
            build_spec=build_spec,
            description=description,
            environment_variables=environment_variables,
            performance_mode=performance_mode,
            pull_request_environment_name=pull_request_environment_name,
            pull_request_preview=pull_request_preview,
            stage=stage,
        )

        return typing.cast("Branch", jsii.invoke(self, "addBranch", [id, options]))

    @jsii.member(jsii_name="addCustomRule")
    def add_custom_rule(self, rule: CustomRule) -> "App":
        '''(experimental) Adds a custom rewrite/redirect rule to this application.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ffd633e379f93fb7a23f1def35a12ed4c1f9be0ffbbb4ebf5f5962b9db21e3)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast("App", jsii.invoke(self, "addCustomRule", [rule]))

    @jsii.member(jsii_name="addDomain")
    def add_domain(
        self,
        id: builtins.str,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> Domain:
        '''(experimental) Adds a domain to this application.

        :param id: -
        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e306721ccfacc3190328ea7a3da978650e6c4e4095a174c6e5ca7c82891d75)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = DomainOptions(
            auto_subdomain_creation_patterns=auto_subdomain_creation_patterns,
            domain_name=domain_name,
            enable_auto_subdomain=enable_auto_subdomain,
            sub_domains=sub_domains,
        )

        return typing.cast(Domain, jsii.invoke(self, "addDomain", [id, options]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> "App":
        '''(experimental) Adds an environment variable to this application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45acf7f091b341df843ee9ffc55cdf9713197695eee71293de0518951bd32288)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("App", jsii.invoke(self, "addEnvironment", [name, value]))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        '''(experimental) The name of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> builtins.str:
        '''(experimental) The default domain of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "defaultDomain"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_940a1ce0.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IPrincipal, jsii.get(self, "grantPrincipal"))


@jsii.implements(IBranch)
class Branch(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.Branch",
):
    '''(experimental) An Amplify Console branch.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        
        
        master = amplify_app.add_branch("master") # `id` will be used as repo branch name
        dev = amplify_app.add_branch("dev",
            performance_mode=True
        )
        dev.add_environment("STAGE", "dev")
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app: IApp,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app: (experimental) The application within which the branch must be created.
        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f172b7f073b73bf3938e7d7bbb6c4d9db57a040103dffa9d80d74848f02b0739)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BranchProps(
            app=app,
            asset=asset,
            auto_build=auto_build,
            basic_auth=basic_auth,
            branch_name=branch_name,
            build_spec=build_spec,
            description=description,
            environment_variables=environment_variables,
            performance_mode=performance_mode,
            pull_request_environment_name=pull_request_environment_name,
            pull_request_preview=pull_request_preview,
            stage=stage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromBranchName")
    @builtins.classmethod
    def from_branch_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        branch_name: builtins.str,
    ) -> IBranch:
        '''(experimental) Import an existing branch.

        :param scope: -
        :param id: -
        :param branch_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e33f944b5c80d2180485391c5db3593166254cbdc67b3f0955d7d9f9ad4b1a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(IBranch, jsii.sinvoke(cls, "fromBranchName", [scope, id, branch_name]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> "Branch":
        '''(experimental) Adds an environment variable to this branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167bd2c85d090b96a026a483f8d88dd3a5228fd8367ae0d9cf05df75ef063403)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Branch", jsii.invoke(self, "addEnvironment", [name, value]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the branch.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))


@jsii.implements(ISourceCodeProvider)
class CodeCommitSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.CodeCommitSourceCodeProvider",
):
    '''(experimental) CodeCommit source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codecommit as codecommit
        
        
        repository = codecommit.Repository(self, "Repo",
            repository_name="my-repo"
        )
        
        amplify_app = amplify.App(self, "App",
            source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
        )
    '''

    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_codecommit_692dd32c.IRepository,
    ) -> None:
        '''
        :param repository: (experimental) The CodeCommit repository.

        :stability: experimental
        '''
        props = CodeCommitSourceCodeProviderProps(repository=repository)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec3cbf5376f8045c3c0fef31b6f9d39e44d6b5afa90a68cf57d42f45e3a90e3)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [app]))


@jsii.implements(ISourceCodeProvider)
class GitHubSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.GitHubSourceCodeProvider",
):
    '''(experimental) GitHub source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                patterns=["feature/*", "test/*"]),
            auto_branch_deletion=True
        )
    '''

    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_core_f4b25747.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''
        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        '''
        props = GitHubSourceCodeProviderProps(
            oauth_token=oauth_token, owner=owner, repository=repository
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param _app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6bf045dde008ae955cd8ec943365d73847a880c429d5d7d384afbbe4dd45a3)
            check_type(argname="argument _app", value=_app, expected_type=type_hints["_app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [_app]))


@jsii.implements(ISourceCodeProvider)
class GitLabSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify.GitLabSourceCodeProvider",
):
    '''(experimental) GitLab source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitLabSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-gitlab-token")
            )
        )
    '''

    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_core_f4b25747.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''
        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        '''
        props = GitLabSourceCodeProviderProps(
            oauth_token=oauth_token, owner=owner, repository=repository
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param _app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b76bbb0fb7e5cd8388ba823734a905e0b6dc69c96d7a11983c1dc940c495bb)
            check_type(argname="argument _app", value=_app, expected_type=type_hints["_app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [_app]))


__all__ = [
    "App",
    "AppProps",
    "AutoBranchCreation",
    "BasicAuth",
    "BasicAuthConfig",
    "BasicAuthProps",
    "Branch",
    "BranchOptions",
    "BranchProps",
    "CfnApp",
    "CfnAppProps",
    "CfnBranch",
    "CfnBranchProps",
    "CfnDomain",
    "CfnDomainProps",
    "CodeCommitSourceCodeProvider",
    "CodeCommitSourceCodeProviderProps",
    "CustomResponseHeader",
    "CustomRule",
    "CustomRuleOptions",
    "Domain",
    "DomainOptions",
    "DomainProps",
    "GitHubSourceCodeProvider",
    "GitHubSourceCodeProviderProps",
    "GitLabSourceCodeProvider",
    "GitLabSourceCodeProviderProps",
    "IApp",
    "IBranch",
    "ISourceCodeProvider",
    "RedirectStatus",
    "SourceCodeProviderConfig",
    "SubDomain",
]

publication.publish()

def _typecheckingstub__96a42617415a38f5dc244a1f6aa313edb2a8d55d6c1adf78c65786ca5aa9c283(
    *,
    app_name: typing.Optional[builtins.str] = None,
    auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_branch_deletion: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    source_code_provider: typing.Optional[ISourceCodeProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ac19789aacae3d0e48d81cfb04a5a816dd7e43734474e962cb006478d5d075(
    *,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c714597b18b7dc32f97dd6ef337450b0173afb0347a32120cbb4aeb534b8618(
    username: builtins.str,
    password: _aws_cdk_core_f4b25747.SecretValue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8066b70bbf8acdea4529e1fc01e4e13b1d9a6d007667709746d61eb92debc509(
    username: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb784752e3e9e80e5500ace32f5397aba12950541e26f52b553c111ac0062ca(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725255ee8ddeece1d0727bed73b046182864b6472f9ca50218cbf3969c8318a0(
    *,
    enable_basic_auth: builtins.bool,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4860d9fa9f2450fb760b9897e0f1f89547eb82fc9a8dd5d4dc9d07e0a0876787(
    *,
    username: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb6497d56beb44cabc8b6f4fb539b9189400191567b0bd23257aa07df6e2429(
    *,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e412147e99ae5baa3039fe6719857bfe75faa8b883b0f4a1fbe6504d4ce9f1(
    *,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
    app: IApp,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9dd6b3c3ac2a4d99e31efbe2893e3064a44e76cb7a7c7e1b2bf967114b14be5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    auto_branch_creation_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    custom_headers: typing.Optional[builtins.str] = None,
    custom_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    iam_service_role: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d2fb63c2bcce5f4ac4dcc55b2f1e4e99c91001d22117418ab62ff32879bd22(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e600803ddfffd15923ed881b3362028d47f5ba7f426cdd202b9a2bda19b311(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4b35920f963c3c2366324d0140da8bbe37413ec990db63258aee1716ae927f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c11fa16c4cc2bc2049a1a51395c410e62af1e8103592e5620af514196c184f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b39f8927bb4ca9e428f1b67ec3cc0945c06866dcc4584ebe24b6c8604759d82(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.AutoBranchCreationConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279222b8f8cec11c6c42ee2278755b26bb926bbc0c3f86cf50791f8123f76c41(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.BasicAuthConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b2f643d3d3b2c4c3bb1e9d21afe3e60538c0f295c6342103102ad7bc128465(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3780397e4bf7723a37a69802bd8a5537571b31a59dbb55faa34ea6021e1da26a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfbfc672f48c7f9df26172026d7d10caa3be72f2a5e8c312e6fee32b457119d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.CustomRuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f48ff70fa9321cc85c80cf9a3d83f1e37c37d2a0922517ef2fa4b821cd30404(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198d39c14c29636514232b80b68229f74f53bdf8d9fd96e32bab18cfa89b561a(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c85f2da14bcc5480f42ddbfbb27ed936a3494a6713541ac00f736bc3d520d7a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApp.EnvironmentVariableProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2106a698f378c3da9034a184b2032b1cf89133e449f06aa5fc5f297fd466e77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0ed74d81cc49cb057bb3fc9238cc0c326cd0e551bc8ceb0988bfb6c3f14477(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fda7d6bf558e33fe4915f5899a7d2eb3e58e5b50373edd54e9213034be6388(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e81a827a479788365ce697c88d5cf005de3d7522fada40feed1cf7164e27e12(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0af36cdd2d98df90e240d5db6b05a42d7e0ae596fe63a890d4553ede9f6bb05(
    *,
    auto_branch_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    enable_auto_branch_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ca9d287c59aa571660643589355b1c8948432b620e5e69ce27d9e88da4443d(
    *,
    enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0857683e4163f353c24f2174f94e3175fac8c4f2e9063683234700290f3d379c(
    *,
    source: builtins.str,
    target: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a464ed55ca87d5ae228d5260eb1dce153db71c6d814611892808178d1915acdf(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c547002d958c31b5e4e0088f44d0cbe129912efaaa857da6f51258547be9f9ca(
    *,
    name: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    auto_branch_creation_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    custom_headers: typing.Optional[builtins.str] = None,
    custom_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    iam_service_role: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae54455d3d5af65245a98458f974e24a4452e78e7b783b0954949bfeac4bce1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    app_id: builtins.str,
    branch_name: builtins.str,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBranch.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBranch.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0570b0f9ea113f5e51234698cb616024eeeda61b5f94ced0132c086bf1ed72aa(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f7627463f6a6cad1a615fa7f2aead3962939f68a1156fc0f9219102b3b9f08(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e325fedb60c9a7c317f7be1cc30a0ab63a5587c180bb9d4fbecc61ae7bd43e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2150d4306517c8b8af7a047fa9a72722040ddc8ec92fb0632b43887b440216e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea97a250bb087e54bdb9839c21179235bebf3481b32bf7d7b02891358c1a4da5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBranch.BasicAuthConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afd31bcf2f8caa89e7babd1de1c2d12308f7b00427086ada56bc41a28465a9d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d372e31f76f850dafb7c7d4eb1f331d33fe97f120ca6c915c53d7a516d1c52f0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b620fdfa28ccb436b9323410492e0c866850d73decfe6436a07ff144b830d6b(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922c1d1174c05de33f9c5d97a475641a4c4aab8b0abb04055ea23972939fe61e(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac33618c47b126ed1f0bd5f51e5892e8961309386be955c6f39329524da86b0a(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c38dce7f10f082bc47720d8facce56a0afe0b73b1e44024d78975fd3c76944b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBranch.EnvironmentVariableProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16567042afb581540e47e92b110d1083ed38f63ac7054d82933939d125cf1a7c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c3e6f9e0de0bc96367289d5c6f20ed36be294724a94b69984a3bbbe8b86a4e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec971cd709f279c324312ccb382b176cc5643d0c9f5a60dd78c45ac656f24bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c81aca3a46996a7cf3912747f70f94f0dae7aedb1daa6c1c7eb646a1b4eb2(
    *,
    password: builtins.str,
    username: builtins.str,
    enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb803dc15df951d430798b81d922acf35888c8dcb6caa82ab6009bc4fa163858(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58765b995e3a3c35dcd3203d8be9e85a8af1094b0ed6889553c10c59f17e9662(
    *,
    app_id: builtins.str,
    branch_name: builtins.str,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBranch.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBranch.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcad90986ae427b69544c7f362f745108911b66125dff5eccc810b17f2ba99b5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    app_id: builtins.str,
    domain_name: builtins.str,
    sub_domain_settings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]]]]],
    auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
    enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381b713e8667226770767758b43f8105dfda8bde777f73501ce85809fe27bee5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf314e52e1ea91ffb655d297ef76100e5e540eb3b1ff8882dafab743cd8b1383(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ea3f2fe871af1076106e23c65ec477c68a24f9201e979b06720796280a5bbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d05a2d9eb69278804b0c5a2658fec92f0ac6d287dec4aa6fe5ed9674fd4325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10d5558f90b26f77dc405fe86464a18a91184c5b6bf4bd7a7d07e1c8fab3eae(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.SubDomainSettingProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00afb3cf5ecae89c8d6ba6fabdeb995e5c0ab9fa6a8b0fd60d80474b33f1df61(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782e66e12f275620aa8f41fd05ad58239696590373588a8d959ba88f3122c939(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763945f88c06feda2681fea779bebe32558139e36367d90e56b89dc82850a032(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf478b2b1ad15b0cad30f4ef3c8ef85983a10f093aea27266dae8310fe0fee1(
    *,
    branch_name: builtins.str,
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028b81cae4e9723af6c8b32ab71ba4c313c8a84d4fc64edd7dc009aeeee8da5f(
    *,
    app_id: builtins.str,
    domain_name: builtins.str,
    sub_domain_settings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]]]]],
    auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
    enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345157c20d08b130c79585b5ce878c85941077868619ff57bc7e2e22286d5f38(
    *,
    repository: _aws_cdk_aws_codecommit_692dd32c.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb280fccd6a370bbbf11d9edff44e37ba68d6928807dddc249dc311095b2be9(
    *,
    headers: typing.Mapping[builtins.str, builtins.str],
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2e261119c6973bfbce688947f42d461b52338425e97fde0e5ac7fb04ed5247(
    *,
    source: builtins.str,
    target: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    status: typing.Optional[RedirectStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3812136db5a4ad43710dd15f4868abb8cd6250c7cfb24bd4b374902b26129260(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: IApp,
    auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c84706b963ab53916cca4a03a6f63fd063a67875077e6db032fc97833fe6b58(
    branch: IBranch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ca6cc71927e93a54c4134210227a4c448fb8f794a013fcb8748689dd0d4b1e(
    branch: IBranch,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5f4e81d015354f82eb3159bfe0c270faadf0fd7c175645067982a00888e501(
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6bb0f1ca7e1558c6afa7580fba1358c7519bcf6518be82974b3a12a9208062(
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
    app: IApp,
    auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f7fba5e451129c731de09264876451a7d4fb040d59b9c95aca89c539c22421(
    *,
    oauth_token: _aws_cdk_core_f4b25747.SecretValue,
    owner: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394c4cd146711c120d8bf9c35d2415dfd1867a3d839cd9e7979c791c9419d21f(
    *,
    oauth_token: _aws_cdk_core_f4b25747.SecretValue,
    owner: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a23b00d6539bdc77b17baaedf3186707afa5a6f4307aa2fe1454bf6c1875af(
    app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b830d1f0b4ed8f962a9b445488c1d721aa9e75598983dc07a412ce30731554(
    *,
    repository: builtins.str,
    access_token: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    oauth_token: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a23838c4a1c016f89080850da61f6301d09a9aff0ecab4050369cfb8d66633c(
    *,
    branch: IBranch,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd9e80edafcb9da39e2ba9e0f5fb346d03475818387c23e6eb6ef2c3dfd2259(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_name: typing.Optional[builtins.str] = None,
    auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_branch_deletion: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    source_code_provider: typing.Optional[ISourceCodeProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b13d4324c46fd14239d37b05bf08894cff7f10fba3df35f46ad8ec4251bcc68(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    app_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6599ef9359e6edb94225440082ca6bbb912f060bfddce983a0dc0d4a7d52f1e1(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc338ecfbc7c7ce2f6ef47f6d20df85a0d41461f158f56955bfa63ea0221f3a8(
    id: builtins.str,
    *,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ffd633e379f93fb7a23f1def35a12ed4c1f9be0ffbbb4ebf5f5962b9db21e3(
    rule: CustomRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e306721ccfacc3190328ea7a3da978650e6c4e4095a174c6e5ca7c82891d75(
    id: builtins.str,
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45acf7f091b341df843ee9ffc55cdf9713197695eee71293de0518951bd32288(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f172b7f073b73bf3938e7d7bbb6c4d9db57a040103dffa9d80d74848f02b0739(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: IApp,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_525817d7.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_0f2c5c86.BuildSpec] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e33f944b5c80d2180485391c5db3593166254cbdc67b3f0955d7d9f9ad4b1a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167bd2c85d090b96a026a483f8d88dd3a5228fd8367ae0d9cf05df75ef063403(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec3cbf5376f8045c3c0fef31b6f9d39e44d6b5afa90a68cf57d42f45e3a90e3(
    app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6bf045dde008ae955cd8ec943365d73847a880c429d5d7d384afbbe4dd45a3(
    _app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b76bbb0fb7e5cd8388ba823734a905e0b6dc69c96d7a11983c1dc940c495bb(
    _app: App,
) -> None:
    """Type checking stubs"""
    pass
