'''
# AWS::CodeGuruReviewer Construct Library

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
import aws_cdk.aws_codegurureviewer as codegurureviewer
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for CodeGuruReviewer construct libraries](https://constructs.dev/search?q=codegurureviewer)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::CodeGuruReviewer resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeGuruReviewer.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::CodeGuruReviewer](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeGuruReviewer.html).

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
class CfnRepositoryAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codegurureviewer.CfnRepositoryAssociation",
):
    '''A CloudFormation ``AWS::CodeGuruReviewer::RepositoryAssociation``.

    This resource configures how Amazon CodeGuru Reviewer retrieves the source code to be reviewed. You can use an AWS CloudFormation template to create an association with the following repository types:

    - AWS CodeCommit - For more information, see `Create an AWS CodeCommit repository association <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-codecommit-association.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .
    - Bitbucket - For more information, see `Create a Bitbucket repository association <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-bitbucket-association.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .
    - GitHub Enterprise Server - For more information, see `Create a GitHub Enterprise Server repository association <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-github-enterprise-association.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .
    - S3Bucket - For more information, see `Create code reviews with GitHub Actions <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/working-with-cicd.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .

    .. epigraph::

       You cannot use a CloudFormation template to create an association with a GitHub repository.

    :cloudformationResource: AWS::CodeGuruReviewer::RepositoryAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codegurureviewer as codegurureviewer
        
        cfn_repository_association = codegurureviewer.CfnRepositoryAssociation(self, "MyCfnRepositoryAssociation",
            name="name",
            type="type",
        
            # the properties below are optional
            bucket_name="bucketName",
            connection_arn="connectionArn",
            owner="owner",
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
        type: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeGuruReviewer::RepositoryAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the repository.
        :param type: The type of repository that contains the source code to be reviewed. The valid values are:. - ``CodeCommit`` - ``Bitbucket`` - ``GitHubEnterpriseServer`` - ``S3Bucket``
        :param bucket_name: The name of the bucket. This is required for your S3Bucket repository. The name must start with the prefix ``codeguru-reviewer-*`` .
        :param connection_arn: The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection. Its format is ``arn:aws:codestar-connections:region-id:aws-account_id:connection/connection-id`` . For more information, see `Connection <https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Connection.html>`_ in the *AWS CodeStar Connections API Reference* . ``ConnectionArn`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.
        :param owner: The owner of the repository. For a GitHub Enterprise Server or Bitbucket repository, this is the username for the account that owns the repository. ``Owner`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.
        :param tags: An array of key-value pairs used to tag an associated repository. A tag is a custom attribute label with two parts: - A *tag key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag keys are case sensitive. - An optional field known as a *tag value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag value is the same as using an empty string. Like tag keys, tag values are case sensitive.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0e79c0aee7add79b228d4e85c20069f98d6475fd1380a5435e3c6c776a80ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRepositoryAssociationProps(
            name=name,
            type=type,
            bucket_name=bucket_name,
            connection_arn=connection_arn,
            owner=owner,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d843e806a4ca6b06a0cf9039130d936fa5f2d6e92cca5054b5ae59d12ddbc870)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19e908baa6b7f5d76196e61a997f7c6bba4da0c004438a0a257e6bd8c0cc223a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationArn")
    def attr_association_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ```RepositoryAssociation`` <https://docs.aws.amazon.com/codeguru/latest/reviewer-api/API_RepositoryAssociation.html>`_ object. You can retrieve this ARN by calling ``ListRepositories`` .

        :cloudformationAttribute: AssociationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs used to tag an associated repository.

        A tag is a custom attribute label with two parts:

        - A *tag key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag keys are case sensitive.
        - An optional field known as a *tag value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag value is the same as using an empty string. Like tag keys, tag values are case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72bac44abd29ec361ca5f82358c05d4c3349210c1e4f285889862ab7b957ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of repository that contains the source code to be reviewed. The valid values are:.

        - ``CodeCommit``
        - ``Bitbucket``
        - ``GitHubEnterpriseServer``
        - ``S3Bucket``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334a345cd03e6f13793b0034fd2c1ea07852e4f806b99c5b0baef7ad32dca234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket.

        This is required for your S3Bucket repository. The name must start with the prefix ``codeguru-reviewer-*`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-bucketname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16799a47f44e33f4e537886cf91d264ffddeed890b38866fae115bfe4eca9768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.

        Its format is ``arn:aws:codestar-connections:region-id:aws-account_id:connection/connection-id`` . For more information, see `Connection <https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Connection.html>`_ in the *AWS CodeStar Connections API Reference* .

        ``ConnectionArn`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-connectionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionArn"))

    @connection_arn.setter
    def connection_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f14d609b673dbfea8d851deecd9736112459d1ce862a2a9b1897b91081248d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionArn", value)

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        '''The owner of the repository.

        For a GitHub Enterprise Server or Bitbucket repository, this is the username for the account that owns the repository.

        ``Owner`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-owner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccb9b538b4c2f12a6a03a2dc4699d5393fd221d52a09e3d3c3317623ff765dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codegurureviewer.CfnRepositoryAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "bucket_name": "bucketName",
        "connection_arn": "connectionArn",
        "owner": "owner",
        "tags": "tags",
    },
)
class CfnRepositoryAssociationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRepositoryAssociation``.

        :param name: The name of the repository.
        :param type: The type of repository that contains the source code to be reviewed. The valid values are:. - ``CodeCommit`` - ``Bitbucket`` - ``GitHubEnterpriseServer`` - ``S3Bucket``
        :param bucket_name: The name of the bucket. This is required for your S3Bucket repository. The name must start with the prefix ``codeguru-reviewer-*`` .
        :param connection_arn: The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection. Its format is ``arn:aws:codestar-connections:region-id:aws-account_id:connection/connection-id`` . For more information, see `Connection <https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Connection.html>`_ in the *AWS CodeStar Connections API Reference* . ``ConnectionArn`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.
        :param owner: The owner of the repository. For a GitHub Enterprise Server or Bitbucket repository, this is the username for the account that owns the repository. ``Owner`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.
        :param tags: An array of key-value pairs used to tag an associated repository. A tag is a custom attribute label with two parts: - A *tag key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag keys are case sensitive. - An optional field known as a *tag value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag value is the same as using an empty string. Like tag keys, tag values are case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codegurureviewer as codegurureviewer
            
            cfn_repository_association_props = codegurureviewer.CfnRepositoryAssociationProps(
                name="name",
                type="type",
            
                # the properties below are optional
                bucket_name="bucketName",
                connection_arn="connectionArn",
                owner="owner",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae41387ef19469ddf7aed92fb38b52786ef8abb9ef298b29f025d1773636e2e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn
        if owner is not None:
            self._values["owner"] = owner
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of repository that contains the source code to be reviewed. The valid values are:.

        - ``CodeCommit``
        - ``Bitbucket``
        - ``GitHubEnterpriseServer``
        - ``S3Bucket``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket.

        This is required for your S3Bucket repository. The name must start with the prefix ``codeguru-reviewer-*`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.

        Its format is ``arn:aws:codestar-connections:region-id:aws-account_id:connection/connection-id`` . For more information, see `Connection <https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Connection.html>`_ in the *AWS CodeStar Connections API Reference* .

        ``ConnectionArn`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The owner of the repository.

        For a GitHub Enterprise Server or Bitbucket repository, this is the username for the account that owns the repository.

        ``Owner`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-owner
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs used to tag an associated repository.

        A tag is a custom attribute label with two parts:

        - A *tag key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag keys are case sensitive.
        - An optional field known as a *tag value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag value is the same as using an empty string. Like tag keys, tag values are case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnRepositoryAssociation",
    "CfnRepositoryAssociationProps",
]

publication.publish()

def _typecheckingstub__1a0e79c0aee7add79b228d4e85c20069f98d6475fd1380a5435e3c6c776a80ed(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d843e806a4ca6b06a0cf9039130d936fa5f2d6e92cca5054b5ae59d12ddbc870(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e908baa6b7f5d76196e61a997f7c6bba4da0c004438a0a257e6bd8c0cc223a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72bac44abd29ec361ca5f82358c05d4c3349210c1e4f285889862ab7b957ea7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334a345cd03e6f13793b0034fd2c1ea07852e4f806b99c5b0baef7ad32dca234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16799a47f44e33f4e537886cf91d264ffddeed890b38866fae115bfe4eca9768(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f14d609b673dbfea8d851deecd9736112459d1ce862a2a9b1897b91081248d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccb9b538b4c2f12a6a03a2dc4699d5393fd221d52a09e3d3c3317623ff765dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae41387ef19469ddf7aed92fb38b52786ef8abb9ef298b29f025d1773636e2e(
    *,
    name: builtins.str,
    type: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
