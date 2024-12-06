# Mat Werber's AWS CDK Construct Library

This project is (or at least, is meant to become) a central repository of the various custom AWS CDK constructs I create in the course of my work.

For now, project goals are:

1. Learn how to publish to the CDK Construct Hub
2. Learn to write better constructs.
3. Improve my existing constructs over time rather than re-creating or copy-pasting them when needed across projects.

## FAQ

### How was this project started?

Rather than piece together the various components and decisions needed to publish to the CDK Construct Hub, I opted to use AWS CDK Construct Library template project provided by [projen](https://projen.io/docs/project-types/aws-cdk-construct-library/)

### How does the project get published to Construct Hub?

Commits trigger a GitHub Action to build and publish this library to **npm**.
