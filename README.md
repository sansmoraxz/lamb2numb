# Lamb2Numb

Lambda application template to fast track creating your own AWS lambda in Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<br />

[![ci pipeline](https://github.com/sansmoraxz/lamb2numb/actions/workflows/cipipeline.yaml/badge.svg)](https://github.com/sansmoraxz/lamb2numb/actions/workflows/cipipeline.yaml)
[![Layer Deployment pipeline](https://github.com/sansmoraxz/lamb2numb/actions/workflows/layerpipeline.yaml/badge.svg)](https://github.com/sansmoraxz/lamb2numb/actions/workflows/layerpipeline.yaml)


Includes:-

- Separate [lambda layer](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html) for your lambda dependencies
- [CI/CD pipelines](.github/workflows) for pushing your source code and your layer
- Simple application demonstrating SQS queue consumption
- Linting with [ruff](https://github.com/astral-sh/ruff)
- Unit tests with [moto](https://github.com/getmoto/moto) for the above use case
