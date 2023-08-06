'''
# AWS OpsWorks CM Construct Library

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
import aws_cdk.aws_opsworkscm as opsworkscm
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for OpsWorksCM construct libraries](https://constructs.dev/search?q=opsworkscm)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::OpsWorksCM resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpsWorksCM.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::OpsWorksCM](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpsWorksCM.html).

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
class CfnServer(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworkscm.CfnServer",
):
    '''A CloudFormation ``AWS::OpsWorksCM::Server``.

    The ``AWS::OpsWorksCM::Server`` resource creates an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise configuration management server. For more information, see `Create a Chef Automate Server in AWS CloudFormation <https://docs.aws.amazon.com/opsworks/latest/userguide/opscm-create-server-cfn.html>`_ or `Create a Puppet Enterprise Master in AWS CloudFormation <https://docs.aws.amazon.com/opsworks/latest/userguide/opspup-create-server-cfn.html>`_ in the *AWS OpsWorks User Guide* , and `CreateServer <https://docs.aws.amazon.com/opsworks-cm/latest/APIReference/API_CreateServer.html>`_ in the *AWS OpsWorks CM API Reference* .

    :cloudformationResource: AWS::OpsWorksCM::Server
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_opsworkscm as opsworkscm
        
        cfn_server = opsworkscm.CfnServer(self, "MyCfnServer",
            instance_profile_arn="instanceProfileArn",
            instance_type="instanceType",
            service_role_arn="serviceRoleArn",
        
            # the properties below are optional
            associate_public_ip_address=False,
            backup_id="backupId",
            backup_retention_count=123,
            custom_certificate="customCertificate",
            custom_domain="customDomain",
            custom_private_key="customPrivateKey",
            disable_automated_backup=False,
            engine="engine",
            engine_attributes=[opsworkscm.CfnServer.EngineAttributeProperty(
                name="name",
                value="value"
            )],
            engine_model="engineModel",
            engine_version="engineVersion",
            key_pair="keyPair",
            preferred_backup_window="preferredBackupWindow",
            preferred_maintenance_window="preferredMaintenanceWindow",
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
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
        instance_profile_arn: builtins.str,
        instance_type: builtins.str,
        service_role_arn: builtins.str,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        backup_id: typing.Optional[builtins.str] = None,
        backup_retention_count: typing.Optional[jsii.Number] = None,
        custom_certificate: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[builtins.str] = None,
        custom_private_key: typing.Optional[builtins.str] = None,
        disable_automated_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnServer.EngineAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        engine_model: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::OpsWorksCM::Server``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_profile_arn: The ARN of the instance profile that your Amazon EC2 instances use.
        :param instance_type: The Amazon EC2 instance type to use. For example, ``m5.large`` .
        :param service_role_arn: The service role that the AWS OpsWorks CM service backend uses to work with your account. Although the AWS OpsWorks management console typically creates the service role for you, if you are using the AWS CLI or API commands, run the service-role-creation.yaml AWS CloudFormation template, located at https://s3.amazonaws.com/opsworks-cm-us-east-1-prod-default-assets/misc/opsworks-cm-roles.yaml. This template creates a CloudFormation stack that includes the service role and instance profile that you need.
        :param associate_public_ip_address: Associate a public IP address with a server that you are launching. Valid values are ``true`` or ``false`` . The default value is ``true`` .
        :param backup_id: If you specify this field, AWS OpsWorks CM creates the server by using the backup represented by BackupId.
        :param backup_retention_count: The number of automated backups that you want to keep. Whenever a new backup is created, AWS OpsWorks CM deletes the oldest backups if this number is exceeded. The default value is ``1`` .
        :param custom_certificate: Supported on servers running Chef Automate 2.0 only. A PEM-formatted HTTPS certificate. The value can be be a single, self-signed certificate, or a certificate chain. If you specify a custom certificate, you must also specify values for ``CustomDomain`` and ``CustomPrivateKey`` . The following are requirements for the ``CustomCertificate`` value:. - You can provide either a self-signed, custom certificate, or the full certificate chain. - The certificate must be a valid X509 certificate, or a certificate chain in PEM format. - The certificate must be valid at the time of upload. A certificate can't be used before its validity period begins (the certificate's ``NotBefore`` date), or after it expires (the certificate's ``NotAfter`` date). - The certificate’s common name or subject alternative names (SANs), if present, must match the value of ``CustomDomain`` . - The certificate must match the value of ``CustomPrivateKey`` .
        :param custom_domain: Supported on servers running Chef Automate 2.0 only. An optional public endpoint of a server, such as ``https://aws.my-company.com`` . To access the server, create a CNAME DNS record in your preferred DNS service that points the custom domain to the endpoint that is generated when the server is created (the value of the CreateServer Endpoint attribute). You cannot access the server by using the generated ``Endpoint`` value if the server is using a custom domain. If you specify a custom domain, you must also specify values for ``CustomCertificate`` and ``CustomPrivateKey`` .
        :param custom_private_key: Supported on servers running Chef Automate 2.0 only. A private key in PEM format for connecting to the server by using HTTPS. The private key must not be encrypted; it cannot be protected by a password or passphrase. If you specify a custom private key, you must also specify values for ``CustomDomain`` and ``CustomCertificate`` .
        :param disable_automated_backup: Enable or disable scheduled backups. Valid values are ``true`` or ``false`` . The default value is ``true`` .
        :param engine: The configuration management engine to use. Valid values include ``ChefAutomate`` and ``Puppet`` .
        :param engine_attributes: Optional engine attributes on a specified server. **Attributes accepted in a Chef createServer request:** - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. When no CHEF_AUTOMATE_PIVOTAL_KEY is set, a private key is generated and returned in the response. When you are specifying the value of CHEF_AUTOMATE_PIVOTAL_KEY as a parameter in the AWS CloudFormation console, you must add newline ( ``\\n`` ) characters at the end of each line of the pivotal key value. - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` : The password for the administrative user in the Chef Automate web-based dashboard. The password length is a minimum of eight characters, and a maximum of 32. The password can contain letters, numbers, and special characters (!/@#$%^&+=_). The password must contain at least one lower case letter, one upper case letter, one number, and one special character. When no CHEF_AUTOMATE_ADMIN_PASSWORD is set, one is generated and returned in the response. **Attributes accepted in a Puppet createServer request:** - ``PUPPET_ADMIN_PASSWORD`` : To work with the Puppet Enterprise console, a password must use ASCII characters. - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170. - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add PUPPET_R10K_PRIVATE_KEY to specify a PEM-encoded private SSH key.
        :param engine_model: The engine model of the server. Valid values in this release include ``Monolithic`` for Puppet and ``Single`` for Chef.
        :param engine_version: The major release version of the engine that you want to use. For a Chef server, the valid value for EngineVersion is currently ``2`` . For a Puppet server, valid values are ``2019`` or ``2017`` .
        :param key_pair: The Amazon EC2 key pair to set for the instance. This parameter is optional; if desired, you may specify this parameter to connect to your instances by using SSH.
        :param preferred_backup_window: The start time for a one-hour period during which AWS OpsWorks CM backs up application-level data on your server if automated backups are enabled. Valid values must be specified in one of the following formats: - ``HH:MM`` for daily backups - ``DDD:HH:MM`` for weekly backups ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random, daily start time. *Example:* ``08:00`` , which represents a daily start time of 08:00 UTC. *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)
        :param preferred_maintenance_window: The start time for a one-hour period each week during which AWS OpsWorks CM performs maintenance on the instance. Valid values must be specified in the following format: ``DDD:HH:MM`` . ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random one-hour period on Tuesday, Wednesday, or Friday. See ``TimeWindowDefinition`` for more information. *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)
        :param security_group_ids: A list of security group IDs to attach to the Amazon EC2 instance. If you add this parameter, the specified security groups must be within the VPC that is specified by ``SubnetIds`` . If you do not specify this parameter, AWS OpsWorks CM creates one new security group that uses TCP ports 22 and 443, open to 0.0.0.0/0 (everyone).
        :param subnet_ids: The IDs of subnets in which to launch the server EC2 instance. Amazon EC2-Classic customers: This field is required. All servers must run within a VPC. The VPC must have "Auto Assign Public IP" enabled. EC2-VPC customers: This field is optional. If you do not specify subnet IDs, your EC2 instances are created in a default subnet that is selected by Amazon EC2. If you specify subnet IDs, the VPC must have "Auto Assign Public IP" enabled. For more information about supported Amazon EC2 platforms, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .
        :param tags: A map that contains tag keys and tag values to attach to an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server. - The key cannot be empty. - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @`` - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @`` - Leading and trailing spaces are trimmed from both the key and value. - A maximum of 50 user-applied tags is allowed for any AWS OpsWorks CM server.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc14c369ed9cd38de644f67c679281487a31d00f8abbbe468833411e11545a92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServerProps(
            instance_profile_arn=instance_profile_arn,
            instance_type=instance_type,
            service_role_arn=service_role_arn,
            associate_public_ip_address=associate_public_ip_address,
            backup_id=backup_id,
            backup_retention_count=backup_retention_count,
            custom_certificate=custom_certificate,
            custom_domain=custom_domain,
            custom_private_key=custom_private_key,
            disable_automated_backup=disable_automated_backup,
            engine=engine,
            engine_attributes=engine_attributes,
            engine_model=engine_model,
            engine_version=engine_version,
            key_pair=key_pair,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            security_group_ids=security_group_ids,
            subnet_ids=subnet_ids,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6be11a0cfa97e34d3cbec4f5cdd47a18b46466e2a8d8c07f6bc9555f77a0ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dd329f66d5e8596962042c0f112359bc7d5296fe69230396a707233770701e7)
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
        '''The Amazon Resource Name (ARN) of the server, such as ``arn:aws:OpsWorksCM:us-east-1:123456789012:server/server-a1bzhi`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''A DNS name that can be used to access the engine.

        Example: ``myserver-asdfghjkl.us-east-1.opsworks.io`` .

        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrServerName")
    def attr_server_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServerName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServerName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A map that contains tag keys and tag values to attach to an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server.

        - The key cannot be empty.
        - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @``
        - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @``
        - Leading and trailing spaces are trimmed from both the key and value.
        - A maximum of 50 user-applied tags is allowed for any AWS OpsWorks CM server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceProfileArn")
    def instance_profile_arn(self) -> builtins.str:
        '''The ARN of the instance profile that your Amazon EC2 instances use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-instanceprofilearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceProfileArn"))

    @instance_profile_arn.setter
    def instance_profile_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370591ca79e06e913e4ab1f58f352578fce32964011e562827788111dcbfbe14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceProfileArn", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        '''The Amazon EC2 instance type to use.

        For example, ``m5.large`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-instancetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79c3b3cabb31dfa8fc967c82c058ba04427dd2809dfa7f083d5fcbe798400ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        '''The service role that the AWS OpsWorks CM service backend uses to work with your account.

        Although the AWS OpsWorks management console typically creates the service role for you, if you are using the AWS CLI or API commands, run the service-role-creation.yaml AWS CloudFormation template, located at https://s3.amazonaws.com/opsworks-cm-us-east-1-prod-default-assets/misc/opsworks-cm-roles.yaml. This template creates a CloudFormation stack that includes the service role and instance profile that you need.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-servicerolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b645fbfa6c1a589ddc9676d50434d14d86a2f7e97360e420703754861298091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="associatePublicIpAddress")
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Associate a public IP address with a server that you are launching.

        Valid values are ``true`` or ``false`` . The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-associatepublicipaddress
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "associatePublicIpAddress"))

    @associate_public_ip_address.setter
    def associate_public_ip_address(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e678d05606f27260d8f19ea91b2408abf4171321559f44fa7ca34e24a1cbc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatePublicIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="backupId")
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''If you specify this field, AWS OpsWorks CM creates the server by using the backup represented by BackupId.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-backupid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupId"))

    @backup_id.setter
    def backup_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da7daa5a077f0aca3c52f135f705e0059c94ad44ae2c9e1f088f1aabb5a1532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupId", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionCount")
    def backup_retention_count(self) -> typing.Optional[jsii.Number]:
        '''The number of automated backups that you want to keep.

        Whenever a new backup is created, AWS OpsWorks CM deletes the oldest backups if this number is exceeded. The default value is ``1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-backupretentioncount
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionCount"))

    @backup_retention_count.setter
    def backup_retention_count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3f66359e50f2f55b359895c56fedd7ec8d9c1e8ca724452b7ff8a673e8a3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionCount", value)

    @builtins.property
    @jsii.member(jsii_name="customCertificate")
    def custom_certificate(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. A PEM-formatted HTTPS certificate. The value can be be a single, self-signed certificate, or a certificate chain. If you specify a custom certificate, you must also specify values for ``CustomDomain`` and ``CustomPrivateKey`` . The following are requirements for the ``CustomCertificate`` value:.

        - You can provide either a self-signed, custom certificate, or the full certificate chain.
        - The certificate must be a valid X509 certificate, or a certificate chain in PEM format.
        - The certificate must be valid at the time of upload. A certificate can't be used before its validity period begins (the certificate's ``NotBefore`` date), or after it expires (the certificate's ``NotAfter`` date).
        - The certificate’s common name or subject alternative names (SANs), if present, must match the value of ``CustomDomain`` .
        - The certificate must match the value of ``CustomPrivateKey`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customcertificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customCertificate"))

    @custom_certificate.setter
    def custom_certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619f498d54ec4ea421e809f992d821af7fe2d4d74cafe663ca34297508e1e130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. An optional public endpoint of a server, such as ``https://aws.my-company.com`` . To access the server, create a CNAME DNS record in your preferred DNS service that points the custom domain to the endpoint that is generated when the server is created (the value of the CreateServer Endpoint attribute). You cannot access the server by using the generated ``Endpoint`` value if the server is using a custom domain. If you specify a custom domain, you must also specify values for ``CustomCertificate`` and ``CustomPrivateKey`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customdomain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomain"))

    @custom_domain.setter
    def custom_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37033bdc316af76bd7fdd42c799aeed0ef2d1877bf418043c961e92f3700cd61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDomain", value)

    @builtins.property
    @jsii.member(jsii_name="customPrivateKey")
    def custom_private_key(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. A private key in PEM format for connecting to the server by using HTTPS. The private key must not be encrypted; it cannot be protected by a password or passphrase. If you specify a custom private key, you must also specify values for ``CustomDomain`` and ``CustomCertificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customprivatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPrivateKey"))

    @custom_private_key.setter
    def custom_private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4c40b827089d833cf047e44368b408c003e9b279e7b8d359e42bee76ad029f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPrivateKey", value)

    @builtins.property
    @jsii.member(jsii_name="disableAutomatedBackup")
    def disable_automated_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enable or disable scheduled backups.

        Valid values are ``true`` or ``false`` . The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-disableautomatedbackup
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "disableAutomatedBackup"))

    @disable_automated_backup.setter
    def disable_automated_backup(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04b00aef6312dbe77587e91022ab8200435267c5b3fe0619305060152f6f098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutomatedBackup", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> typing.Optional[builtins.str]:
        '''The configuration management engine to use.

        Valid values include ``ChefAutomate`` and ``Puppet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engine
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99370a5f04fb5d91b170637165b9f0e65c4e3bef83bf536dcebfafd058c12758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="engineAttributes")
    def engine_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnServer.EngineAttributeProperty"]]]]:
        '''Optional engine attributes on a specified server.

        **Attributes accepted in a Chef createServer request:** - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. When no CHEF_AUTOMATE_PIVOTAL_KEY is set, a private key is generated and returned in the response. When you are specifying the value of CHEF_AUTOMATE_PIVOTAL_KEY as a parameter in the AWS CloudFormation console, you must add newline ( ``\\n`` ) characters at the end of each line of the pivotal key value.

        - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` : The password for the administrative user in the Chef Automate web-based dashboard. The password length is a minimum of eight characters, and a maximum of 32. The password can contain letters, numbers, and special characters (!/@#$%^&+=_). The password must contain at least one lower case letter, one upper case letter, one number, and one special character. When no CHEF_AUTOMATE_ADMIN_PASSWORD is set, one is generated and returned in the response.

        **Attributes accepted in a Puppet createServer request:** - ``PUPPET_ADMIN_PASSWORD`` : To work with the Puppet Enterprise console, a password must use ASCII characters.

        - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170.
        - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add PUPPET_R10K_PRIVATE_KEY to specify a PEM-encoded private SSH key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engineattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnServer.EngineAttributeProperty"]]]], jsii.get(self, "engineAttributes"))

    @engine_attributes.setter
    def engine_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnServer.EngineAttributeProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c838713ad291f4f21e265c073ef82f30885ce2f93713072a4e4e70589011dc9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="engineModel")
    def engine_model(self) -> typing.Optional[builtins.str]:
        '''The engine model of the server.

        Valid values in this release include ``Monolithic`` for Puppet and ``Single`` for Chef.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-enginemodel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineModel"))

    @engine_model.setter
    def engine_model(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de0c8baa0f74d2338ca221842487afd4b6d648755a2d06f493a927489c36298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineModel", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The major release version of the engine that you want to use.

        For a Chef server, the valid value for EngineVersion is currently ``2`` . For a Puppet server, valid values are ``2019`` or ``2017`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609e328ab18879274684a69ea27d4a0085ae1007b030e4464fa9cacbb3ae6fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 key pair to set for the instance.

        This parameter is optional; if desired, you may specify this parameter to connect to your instances by using SSH.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-keypair
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99687872df1484868223a1bab79f44b35f0fc9bc6249b6a8ca9fb00834a798b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value)

    @builtins.property
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The start time for a one-hour period during which AWS OpsWorks CM backs up application-level data on your server if automated backups are enabled.

        Valid values must be specified in one of the following formats:

        - ``HH:MM`` for daily backups
        - ``DDD:HH:MM`` for weekly backups

        ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random, daily start time.

        *Example:* ``08:00`` , which represents a daily start time of 08:00 UTC.

        *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-preferredbackupwindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredBackupWindow"))

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4957f042e70801dd3f355ce69a9218845dbf5d0fe70dba57e7826618df54c602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The start time for a one-hour period each week during which AWS OpsWorks CM performs maintenance on the instance.

        Valid values must be specified in the following format: ``DDD:HH:MM`` . ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random one-hour period on Tuesday, Wednesday, or Friday. See ``TimeWindowDefinition`` for more information.

        *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729ab6cef3ae90b21dc1253d647e9a64d4aad1c17a2b1305c22fab8ad279b57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to attach to the Amazon EC2 instance.

        If you add this parameter, the specified security groups must be within the VPC that is specified by ``SubnetIds`` .

        If you do not specify this parameter, AWS OpsWorks CM creates one new security group that uses TCP ports 22 and 443, open to 0.0.0.0/0 (everyone).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348d6d73c584c06518c0228585fad54c1b9bb8158b3acc896703c0995f33b51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of subnets in which to launch the server EC2 instance.

        Amazon EC2-Classic customers: This field is required. All servers must run within a VPC. The VPC must have "Auto Assign Public IP" enabled.

        EC2-VPC customers: This field is optional. If you do not specify subnet IDs, your EC2 instances are created in a default subnet that is selected by Amazon EC2. If you specify subnet IDs, the VPC must have "Auto Assign Public IP" enabled.

        For more information about supported Amazon EC2 platforms, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-subnetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3243184179581fb734cdd92b6f5aee9dae882713c2a22430f0686ecb53e98d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworkscm.CfnServer.EngineAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EngineAttributeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``EngineAttribute`` property type specifies administrator credentials for an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server.

            ``EngineAttribute`` is a property of the ``AWS::OpsWorksCM::Server`` resource type.

            :param name: The name of the engine attribute. *Attribute name for Chef Automate servers:* - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` *Attribute names for Puppet Enterprise servers:* - ``PUPPET_ADMIN_PASSWORD`` - ``PUPPET_R10K_REMOTE`` - ``PUPPET_R10K_PRIVATE_KEY``
            :param value: The value of the engine attribute. *Attribute value for Chef Automate servers:* - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. You can generate this key by running the following `OpenSSL <https://docs.aws.amazon.com/https://www.openssl.org/>`_ command on Linux-based computers. ``openssl genrsa -out *pivotal_key_file_name* .pem 2048`` On Windows-based computers, you can use the PuTTYgen utility to generate a base64-encoded RSA private key. For more information, see `PuTTYgen - Key Generator for PuTTY on Windows <https://docs.aws.amazon.com/https://www.ssh.com/ssh/putty/windows/puttygen>`_ on SSH.com. *Attribute values for Puppet Enterprise servers:* - ``PUPPET_ADMIN_PASSWORD`` : An administrator password that you can use to sign in to the Puppet Enterprise console webpage after the server is online. The password must use between 8 and 32 ASCII characters. - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170. - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add ``PUPPET_R10K_PRIVATE_KEY`` to specify a PEM-encoded private SSH key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworkscm-server-engineattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opsworkscm as opsworkscm
                
                engine_attribute_property = opsworkscm.CfnServer.EngineAttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1578cb3dee05dfbf5f58f84a686b497e834b2341aaa37148ff2559cce1070ce7)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the engine attribute.

            *Attribute name for Chef Automate servers:*

            - ``CHEF_AUTOMATE_ADMIN_PASSWORD``

            *Attribute names for Puppet Enterprise servers:*

            - ``PUPPET_ADMIN_PASSWORD``
            - ``PUPPET_R10K_REMOTE``
            - ``PUPPET_R10K_PRIVATE_KEY``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworkscm-server-engineattribute.html#cfn-opsworkscm-server-engineattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the engine attribute.

            *Attribute value for Chef Automate servers:*

            - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. You can generate this key by running the following `OpenSSL <https://docs.aws.amazon.com/https://www.openssl.org/>`_ command on Linux-based computers.

            ``openssl genrsa -out *pivotal_key_file_name* .pem 2048``

            On Windows-based computers, you can use the PuTTYgen utility to generate a base64-encoded RSA private key. For more information, see `PuTTYgen - Key Generator for PuTTY on Windows <https://docs.aws.amazon.com/https://www.ssh.com/ssh/putty/windows/puttygen>`_ on SSH.com.

            *Attribute values for Puppet Enterprise servers:*

            - ``PUPPET_ADMIN_PASSWORD`` : An administrator password that you can use to sign in to the Puppet Enterprise console webpage after the server is online. The password must use between 8 and 32 ASCII characters.
            - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170.
            - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add ``PUPPET_R10K_PRIVATE_KEY`` to specify a PEM-encoded private SSH key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworkscm-server-engineattribute.html#cfn-opsworkscm-server-engineattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EngineAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworkscm.CfnServerProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_profile_arn": "instanceProfileArn",
        "instance_type": "instanceType",
        "service_role_arn": "serviceRoleArn",
        "associate_public_ip_address": "associatePublicIpAddress",
        "backup_id": "backupId",
        "backup_retention_count": "backupRetentionCount",
        "custom_certificate": "customCertificate",
        "custom_domain": "customDomain",
        "custom_private_key": "customPrivateKey",
        "disable_automated_backup": "disableAutomatedBackup",
        "engine": "engine",
        "engine_attributes": "engineAttributes",
        "engine_model": "engineModel",
        "engine_version": "engineVersion",
        "key_pair": "keyPair",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnServerProps:
    def __init__(
        self,
        *,
        instance_profile_arn: builtins.str,
        instance_type: builtins.str,
        service_role_arn: builtins.str,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        backup_id: typing.Optional[builtins.str] = None,
        backup_retention_count: typing.Optional[jsii.Number] = None,
        custom_certificate: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[builtins.str] = None,
        custom_private_key: typing.Optional[builtins.str] = None,
        disable_automated_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnServer.EngineAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        engine_model: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServer``.

        :param instance_profile_arn: The ARN of the instance profile that your Amazon EC2 instances use.
        :param instance_type: The Amazon EC2 instance type to use. For example, ``m5.large`` .
        :param service_role_arn: The service role that the AWS OpsWorks CM service backend uses to work with your account. Although the AWS OpsWorks management console typically creates the service role for you, if you are using the AWS CLI or API commands, run the service-role-creation.yaml AWS CloudFormation template, located at https://s3.amazonaws.com/opsworks-cm-us-east-1-prod-default-assets/misc/opsworks-cm-roles.yaml. This template creates a CloudFormation stack that includes the service role and instance profile that you need.
        :param associate_public_ip_address: Associate a public IP address with a server that you are launching. Valid values are ``true`` or ``false`` . The default value is ``true`` .
        :param backup_id: If you specify this field, AWS OpsWorks CM creates the server by using the backup represented by BackupId.
        :param backup_retention_count: The number of automated backups that you want to keep. Whenever a new backup is created, AWS OpsWorks CM deletes the oldest backups if this number is exceeded. The default value is ``1`` .
        :param custom_certificate: Supported on servers running Chef Automate 2.0 only. A PEM-formatted HTTPS certificate. The value can be be a single, self-signed certificate, or a certificate chain. If you specify a custom certificate, you must also specify values for ``CustomDomain`` and ``CustomPrivateKey`` . The following are requirements for the ``CustomCertificate`` value:. - You can provide either a self-signed, custom certificate, or the full certificate chain. - The certificate must be a valid X509 certificate, or a certificate chain in PEM format. - The certificate must be valid at the time of upload. A certificate can't be used before its validity period begins (the certificate's ``NotBefore`` date), or after it expires (the certificate's ``NotAfter`` date). - The certificate’s common name or subject alternative names (SANs), if present, must match the value of ``CustomDomain`` . - The certificate must match the value of ``CustomPrivateKey`` .
        :param custom_domain: Supported on servers running Chef Automate 2.0 only. An optional public endpoint of a server, such as ``https://aws.my-company.com`` . To access the server, create a CNAME DNS record in your preferred DNS service that points the custom domain to the endpoint that is generated when the server is created (the value of the CreateServer Endpoint attribute). You cannot access the server by using the generated ``Endpoint`` value if the server is using a custom domain. If you specify a custom domain, you must also specify values for ``CustomCertificate`` and ``CustomPrivateKey`` .
        :param custom_private_key: Supported on servers running Chef Automate 2.0 only. A private key in PEM format for connecting to the server by using HTTPS. The private key must not be encrypted; it cannot be protected by a password or passphrase. If you specify a custom private key, you must also specify values for ``CustomDomain`` and ``CustomCertificate`` .
        :param disable_automated_backup: Enable or disable scheduled backups. Valid values are ``true`` or ``false`` . The default value is ``true`` .
        :param engine: The configuration management engine to use. Valid values include ``ChefAutomate`` and ``Puppet`` .
        :param engine_attributes: Optional engine attributes on a specified server. **Attributes accepted in a Chef createServer request:** - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. When no CHEF_AUTOMATE_PIVOTAL_KEY is set, a private key is generated and returned in the response. When you are specifying the value of CHEF_AUTOMATE_PIVOTAL_KEY as a parameter in the AWS CloudFormation console, you must add newline ( ``\\n`` ) characters at the end of each line of the pivotal key value. - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` : The password for the administrative user in the Chef Automate web-based dashboard. The password length is a minimum of eight characters, and a maximum of 32. The password can contain letters, numbers, and special characters (!/@#$%^&+=_). The password must contain at least one lower case letter, one upper case letter, one number, and one special character. When no CHEF_AUTOMATE_ADMIN_PASSWORD is set, one is generated and returned in the response. **Attributes accepted in a Puppet createServer request:** - ``PUPPET_ADMIN_PASSWORD`` : To work with the Puppet Enterprise console, a password must use ASCII characters. - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170. - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add PUPPET_R10K_PRIVATE_KEY to specify a PEM-encoded private SSH key.
        :param engine_model: The engine model of the server. Valid values in this release include ``Monolithic`` for Puppet and ``Single`` for Chef.
        :param engine_version: The major release version of the engine that you want to use. For a Chef server, the valid value for EngineVersion is currently ``2`` . For a Puppet server, valid values are ``2019`` or ``2017`` .
        :param key_pair: The Amazon EC2 key pair to set for the instance. This parameter is optional; if desired, you may specify this parameter to connect to your instances by using SSH.
        :param preferred_backup_window: The start time for a one-hour period during which AWS OpsWorks CM backs up application-level data on your server if automated backups are enabled. Valid values must be specified in one of the following formats: - ``HH:MM`` for daily backups - ``DDD:HH:MM`` for weekly backups ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random, daily start time. *Example:* ``08:00`` , which represents a daily start time of 08:00 UTC. *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)
        :param preferred_maintenance_window: The start time for a one-hour period each week during which AWS OpsWorks CM performs maintenance on the instance. Valid values must be specified in the following format: ``DDD:HH:MM`` . ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random one-hour period on Tuesday, Wednesday, or Friday. See ``TimeWindowDefinition`` for more information. *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)
        :param security_group_ids: A list of security group IDs to attach to the Amazon EC2 instance. If you add this parameter, the specified security groups must be within the VPC that is specified by ``SubnetIds`` . If you do not specify this parameter, AWS OpsWorks CM creates one new security group that uses TCP ports 22 and 443, open to 0.0.0.0/0 (everyone).
        :param subnet_ids: The IDs of subnets in which to launch the server EC2 instance. Amazon EC2-Classic customers: This field is required. All servers must run within a VPC. The VPC must have "Auto Assign Public IP" enabled. EC2-VPC customers: This field is optional. If you do not specify subnet IDs, your EC2 instances are created in a default subnet that is selected by Amazon EC2. If you specify subnet IDs, the VPC must have "Auto Assign Public IP" enabled. For more information about supported Amazon EC2 platforms, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .
        :param tags: A map that contains tag keys and tag values to attach to an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server. - The key cannot be empty. - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @`` - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @`` - Leading and trailing spaces are trimmed from both the key and value. - A maximum of 50 user-applied tags is allowed for any AWS OpsWorks CM server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_opsworkscm as opsworkscm
            
            cfn_server_props = opsworkscm.CfnServerProps(
                instance_profile_arn="instanceProfileArn",
                instance_type="instanceType",
                service_role_arn="serviceRoleArn",
            
                # the properties below are optional
                associate_public_ip_address=False,
                backup_id="backupId",
                backup_retention_count=123,
                custom_certificate="customCertificate",
                custom_domain="customDomain",
                custom_private_key="customPrivateKey",
                disable_automated_backup=False,
                engine="engine",
                engine_attributes=[opsworkscm.CfnServer.EngineAttributeProperty(
                    name="name",
                    value="value"
                )],
                engine_model="engineModel",
                engine_version="engineVersion",
                key_pair="keyPair",
                preferred_backup_window="preferredBackupWindow",
                preferred_maintenance_window="preferredMaintenanceWindow",
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f6f15119be85919a59238206d6ee160e75dc35b275713b4c02e4c139c0b55d)
            check_type(argname="argument instance_profile_arn", value=instance_profile_arn, expected_type=type_hints["instance_profile_arn"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument associate_public_ip_address", value=associate_public_ip_address, expected_type=type_hints["associate_public_ip_address"])
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument backup_retention_count", value=backup_retention_count, expected_type=type_hints["backup_retention_count"])
            check_type(argname="argument custom_certificate", value=custom_certificate, expected_type=type_hints["custom_certificate"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument custom_private_key", value=custom_private_key, expected_type=type_hints["custom_private_key"])
            check_type(argname="argument disable_automated_backup", value=disable_automated_backup, expected_type=type_hints["disable_automated_backup"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_attributes", value=engine_attributes, expected_type=type_hints["engine_attributes"])
            check_type(argname="argument engine_model", value=engine_model, expected_type=type_hints["engine_model"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_profile_arn": instance_profile_arn,
            "instance_type": instance_type,
            "service_role_arn": service_role_arn,
        }
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if backup_retention_count is not None:
            self._values["backup_retention_count"] = backup_retention_count
        if custom_certificate is not None:
            self._values["custom_certificate"] = custom_certificate
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if custom_private_key is not None:
            self._values["custom_private_key"] = custom_private_key
        if disable_automated_backup is not None:
            self._values["disable_automated_backup"] = disable_automated_backup
        if engine is not None:
            self._values["engine"] = engine
        if engine_attributes is not None:
            self._values["engine_attributes"] = engine_attributes
        if engine_model is not None:
            self._values["engine_model"] = engine_model
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_profile_arn(self) -> builtins.str:
        '''The ARN of the instance profile that your Amazon EC2 instances use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-instanceprofilearn
        '''
        result = self._values.get("instance_profile_arn")
        assert result is not None, "Required property 'instance_profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The Amazon EC2 instance type to use.

        For example, ``m5.large`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-instancetype
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_role_arn(self) -> builtins.str:
        '''The service role that the AWS OpsWorks CM service backend uses to work with your account.

        Although the AWS OpsWorks management console typically creates the service role for you, if you are using the AWS CLI or API commands, run the service-role-creation.yaml AWS CloudFormation template, located at https://s3.amazonaws.com/opsworks-cm-us-east-1-prod-default-assets/misc/opsworks-cm-roles.yaml. This template creates a CloudFormation stack that includes the service role and instance profile that you need.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        assert result is not None, "Required property 'service_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Associate a public IP address with a server that you are launching.

        Valid values are ``true`` or ``false`` . The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-associatepublicipaddress
        '''
        result = self._values.get("associate_public_ip_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''If you specify this field, AWS OpsWorks CM creates the server by using the backup represented by BackupId.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-backupid
        '''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention_count(self) -> typing.Optional[jsii.Number]:
        '''The number of automated backups that you want to keep.

        Whenever a new backup is created, AWS OpsWorks CM deletes the oldest backups if this number is exceeded. The default value is ``1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-backupretentioncount
        '''
        result = self._values.get("backup_retention_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_certificate(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. A PEM-formatted HTTPS certificate. The value can be be a single, self-signed certificate, or a certificate chain. If you specify a custom certificate, you must also specify values for ``CustomDomain`` and ``CustomPrivateKey`` . The following are requirements for the ``CustomCertificate`` value:.

        - You can provide either a self-signed, custom certificate, or the full certificate chain.
        - The certificate must be a valid X509 certificate, or a certificate chain in PEM format.
        - The certificate must be valid at the time of upload. A certificate can't be used before its validity period begins (the certificate's ``NotBefore`` date), or after it expires (the certificate's ``NotAfter`` date).
        - The certificate’s common name or subject alternative names (SANs), if present, must match the value of ``CustomDomain`` .
        - The certificate must match the value of ``CustomPrivateKey`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customcertificate
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. An optional public endpoint of a server, such as ``https://aws.my-company.com`` . To access the server, create a CNAME DNS record in your preferred DNS service that points the custom domain to the endpoint that is generated when the server is created (the value of the CreateServer Endpoint attribute). You cannot access the server by using the generated ``Endpoint`` value if the server is using a custom domain. If you specify a custom domain, you must also specify values for ``CustomCertificate`` and ``CustomPrivateKey`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customdomain
        '''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_private_key(self) -> typing.Optional[builtins.str]:
        '''Supported on servers running Chef Automate 2.0 only. A private key in PEM format for connecting to the server by using HTTPS. The private key must not be encrypted; it cannot be protected by a password or passphrase. If you specify a custom private key, you must also specify values for ``CustomDomain`` and ``CustomCertificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-customprivatekey
        '''
        result = self._values.get("custom_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_automated_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enable or disable scheduled backups.

        Valid values are ``true`` or ``false`` . The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-disableautomatedbackup
        '''
        result = self._values.get("disable_automated_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The configuration management engine to use.

        Valid values include ``ChefAutomate`` and ``Puppet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnServer.EngineAttributeProperty]]]]:
        '''Optional engine attributes on a specified server.

        **Attributes accepted in a Chef createServer request:** - ``CHEF_AUTOMATE_PIVOTAL_KEY`` : A base64-encoded RSA public key. The corresponding private key is required to access the Chef API. When no CHEF_AUTOMATE_PIVOTAL_KEY is set, a private key is generated and returned in the response. When you are specifying the value of CHEF_AUTOMATE_PIVOTAL_KEY as a parameter in the AWS CloudFormation console, you must add newline ( ``\\n`` ) characters at the end of each line of the pivotal key value.

        - ``CHEF_AUTOMATE_ADMIN_PASSWORD`` : The password for the administrative user in the Chef Automate web-based dashboard. The password length is a minimum of eight characters, and a maximum of 32. The password can contain letters, numbers, and special characters (!/@#$%^&+=_). The password must contain at least one lower case letter, one upper case letter, one number, and one special character. When no CHEF_AUTOMATE_ADMIN_PASSWORD is set, one is generated and returned in the response.

        **Attributes accepted in a Puppet createServer request:** - ``PUPPET_ADMIN_PASSWORD`` : To work with the Puppet Enterprise console, a password must use ASCII characters.

        - ``PUPPET_R10K_REMOTE`` : The r10k remote is the URL of your control repository (for example, ssh://git@your.git-repo.com:user/control-repo.git). Specifying an r10k remote opens TCP port 8170.
        - ``PUPPET_R10K_PRIVATE_KEY`` : If you are using a private Git repository, add PUPPET_R10K_PRIVATE_KEY to specify a PEM-encoded private SSH key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engineattributes
        '''
        result = self._values.get("engine_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnServer.EngineAttributeProperty]]]], result)

    @builtins.property
    def engine_model(self) -> typing.Optional[builtins.str]:
        '''The engine model of the server.

        Valid values in this release include ``Monolithic`` for Puppet and ``Single`` for Chef.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-enginemodel
        '''
        result = self._values.get("engine_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The major release version of the engine that you want to use.

        For a Chef server, the valid value for EngineVersion is currently ``2`` . For a Puppet server, valid values are ``2019`` or ``2017`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 key pair to set for the instance.

        This parameter is optional; if desired, you may specify this parameter to connect to your instances by using SSH.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-keypair
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The start time for a one-hour period during which AWS OpsWorks CM backs up application-level data on your server if automated backups are enabled.

        Valid values must be specified in one of the following formats:

        - ``HH:MM`` for daily backups
        - ``DDD:HH:MM`` for weekly backups

        ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random, daily start time.

        *Example:* ``08:00`` , which represents a daily start time of 08:00 UTC.

        *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The start time for a one-hour period each week during which AWS OpsWorks CM performs maintenance on the instance.

        Valid values must be specified in the following format: ``DDD:HH:MM`` . ``MM`` must be specified as ``00`` . The specified time is in coordinated universal time (UTC). The default value is a random one-hour period on Tuesday, Wednesday, or Friday. See ``TimeWindowDefinition`` for more information.

        *Example:* ``Mon:08:00`` , which represents a start time of every Monday at 08:00 UTC. (8:00 a.m.)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to attach to the Amazon EC2 instance.

        If you add this parameter, the specified security groups must be within the VPC that is specified by ``SubnetIds`` .

        If you do not specify this parameter, AWS OpsWorks CM creates one new security group that uses TCP ports 22 and 443, open to 0.0.0.0/0 (everyone).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of subnets in which to launch the server EC2 instance.

        Amazon EC2-Classic customers: This field is required. All servers must run within a VPC. The VPC must have "Auto Assign Public IP" enabled.

        EC2-VPC customers: This field is optional. If you do not specify subnet IDs, your EC2 instances are created in a default subnet that is selected by Amazon EC2. If you specify subnet IDs, the VPC must have "Auto Assign Public IP" enabled.

        For more information about supported Amazon EC2 platforms, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A map that contains tag keys and tag values to attach to an AWS OpsWorks for Chef Automate or OpsWorks for Puppet Enterprise server.

        - The key cannot be empty.
        - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @``
        - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : / @``
        - Leading and trailing spaces are trimmed from both the key and value.
        - A maximum of 50 user-applied tags is allowed for any AWS OpsWorks CM server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html#cfn-opsworkscm-server-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnServer",
    "CfnServerProps",
]

publication.publish()

def _typecheckingstub__bc14c369ed9cd38de644f67c679281487a31d00f8abbbe468833411e11545a92(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_profile_arn: builtins.str,
    instance_type: builtins.str,
    service_role_arn: builtins.str,
    associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    backup_id: typing.Optional[builtins.str] = None,
    backup_retention_count: typing.Optional[jsii.Number] = None,
    custom_certificate: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[builtins.str] = None,
    custom_private_key: typing.Optional[builtins.str] = None,
    disable_automated_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnServer.EngineAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    engine_model: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6be11a0cfa97e34d3cbec4f5cdd47a18b46466e2a8d8c07f6bc9555f77a0ec(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd329f66d5e8596962042c0f112359bc7d5296fe69230396a707233770701e7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370591ca79e06e913e4ab1f58f352578fce32964011e562827788111dcbfbe14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79c3b3cabb31dfa8fc967c82c058ba04427dd2809dfa7f083d5fcbe798400ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b645fbfa6c1a589ddc9676d50434d14d86a2f7e97360e420703754861298091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e678d05606f27260d8f19ea91b2408abf4171321559f44fa7ca34e24a1cbc82(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da7daa5a077f0aca3c52f135f705e0059c94ad44ae2c9e1f088f1aabb5a1532(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3f66359e50f2f55b359895c56fedd7ec8d9c1e8ca724452b7ff8a673e8a3ac(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619f498d54ec4ea421e809f992d821af7fe2d4d74cafe663ca34297508e1e130(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37033bdc316af76bd7fdd42c799aeed0ef2d1877bf418043c961e92f3700cd61(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4c40b827089d833cf047e44368b408c003e9b279e7b8d359e42bee76ad029f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04b00aef6312dbe77587e91022ab8200435267c5b3fe0619305060152f6f098(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99370a5f04fb5d91b170637165b9f0e65c4e3bef83bf536dcebfafd058c12758(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c838713ad291f4f21e265c073ef82f30885ce2f93713072a4e4e70589011dc9d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnServer.EngineAttributeProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de0c8baa0f74d2338ca221842487afd4b6d648755a2d06f493a927489c36298(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609e328ab18879274684a69ea27d4a0085ae1007b030e4464fa9cacbb3ae6fc3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99687872df1484868223a1bab79f44b35f0fc9bc6249b6a8ca9fb00834a798b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4957f042e70801dd3f355ce69a9218845dbf5d0fe70dba57e7826618df54c602(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729ab6cef3ae90b21dc1253d647e9a64d4aad1c17a2b1305c22fab8ad279b57c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348d6d73c584c06518c0228585fad54c1b9bb8158b3acc896703c0995f33b51e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3243184179581fb734cdd92b6f5aee9dae882713c2a22430f0686ecb53e98d1(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1578cb3dee05dfbf5f58f84a686b497e834b2341aaa37148ff2559cce1070ce7(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f6f15119be85919a59238206d6ee160e75dc35b275713b4c02e4c139c0b55d(
    *,
    instance_profile_arn: builtins.str,
    instance_type: builtins.str,
    service_role_arn: builtins.str,
    associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    backup_id: typing.Optional[builtins.str] = None,
    backup_retention_count: typing.Optional[jsii.Number] = None,
    custom_certificate: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[builtins.str] = None,
    custom_private_key: typing.Optional[builtins.str] = None,
    disable_automated_backup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnServer.EngineAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    engine_model: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
