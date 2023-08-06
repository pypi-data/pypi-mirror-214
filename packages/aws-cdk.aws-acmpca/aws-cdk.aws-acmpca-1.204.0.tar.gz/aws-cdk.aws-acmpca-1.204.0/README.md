# AWS::ACMPCA Construct Library

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
import aws_cdk.aws_acmpca as acmpca
```

## Certificate Authority

This package contains a `CertificateAuthority` class.
At the moment, you cannot create new Authorities using it,
but you can import existing ones using the `fromCertificateAuthorityArn` static method:

```python
certificate_authority = acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CA", "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/023077d8-2bfa-4eb0-8f22-05c96deade77")
```

## Low-level `Cfn*` classes

You can always use the low-level classes
(starting with `Cfn*`) to create resources like the Certificate Authority:

```python
cfn_certificate_authority = acmpca.CfnCertificateAuthority(self, "CA",
    type="ROOT",
    key_algorithm="RSA_2048",
    signing_algorithm="SHA256WITHRSA",
    subject=acmpca.CfnCertificateAuthority.SubjectProperty(
        country="US",
        organization="string",
        organizational_unit="string",
        distinguished_name_qualifier="string",
        state="string",
        common_name="123",
        serial_number="string",
        locality="string",
        title="string",
        surname="string",
        given_name="string",
        initials="DG",
        pseudonym="string",
        generation_qualifier="DBG"
    )
)
```

If you need to pass the higher-level `ICertificateAuthority` somewhere,
you can get it from the lower-level `CfnCertificateAuthority` using the same `fromCertificateAuthorityArn` method:

```python
# cfn_certificate_authority: acmpca.CfnCertificateAuthority


certificate_authority = acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", cfn_certificate_authority.attr_arn)
```
