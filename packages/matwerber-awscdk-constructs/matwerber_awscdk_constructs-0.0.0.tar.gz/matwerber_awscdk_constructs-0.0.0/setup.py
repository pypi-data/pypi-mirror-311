import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "matwerber-awscdk-constructs",
    "version": "0.0.0",
    "description": "awscdk-constructs",
    "license": "MIT",
    "url": "https://github.com/matwerber1/awscdk-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Mat Werber<matwerber@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/matwerber1/awscdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "matwerber_awscdk_constructs",
        "matwerber_awscdk_constructs._jsii"
    ],
    "package_data": {
        "matwerber_awscdk_constructs._jsii": [
            "awscdk-constructs@0.0.0.jsii.tgz"
        ],
        "matwerber_awscdk_constructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.165.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
