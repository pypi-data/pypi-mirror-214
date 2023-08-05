# Azure Machine Learning Feature Store Python SDK

The `azureml-featurestore` package is the core SDK interface for Azure ML Feature Store. This SDK works along the 
`azure-ai-ml` SDK to provide the managed feature store experience.

## Main features in the `azureml-featurestore` package
- Develop feature set specification in Spark with the ability for feature transformation.
- List and get feature sets defined in Azure  ML Feature Store.
- Generate and resolve feature retrieval specification.
- Run offline feature retrieval with point-in-time join.

## Getting started

You can install the package via ` pip install azureml-featurestore `

To learn more about Azure ML managed feature store visit https://aka.ms/featurestore-get-started


# Change Log

## 0.1.0b2 (2023.06.13)

**New Features:**

- [Private preview] Added online store support. Online store supports materialization and online feature values retrieval from Redis cache for batch scoring.

- Various bug fixes

## 0.1.0b1 (2023.05.15)

**New Features:**

Initial release.
