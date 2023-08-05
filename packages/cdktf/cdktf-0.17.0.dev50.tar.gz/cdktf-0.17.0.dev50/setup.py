import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf",
    "version": "0.17.0.dev50",
    "description": "Cloud Development Kit for Terraform",
    "license": "MPL-2.0",
    "url": "https://github.com/hashicorp/terraform-cdk",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/hashicorp/terraform-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf",
        "cdktf._jsii",
        "cdktf.testing_matchers"
    ],
    "package_data": {
        "cdktf._jsii": [
            "cdktf@0.17.0-pre.50.jsii.tgz"
        ],
        "cdktf": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "constructs>=10.0.25, <11.0.0",
        "jsii>=1.79.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
