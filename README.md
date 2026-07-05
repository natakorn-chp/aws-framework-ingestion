# AWS Framework Pipeline

This project is a data pipeline framework designed to implement an ETL process on AWS, primarily using AWS Glue (see the architecture below). The framework is config-driven and built around a decoupled module design, so pipeline steps can be extended and maintained independently. Configuration files define the set of ETL steps to run and the settings for each one.

In addition to the framework itself, this project includes a CI/CD pipeline (GitHub Actions) that builds the framework into a package (wheel file), uploads the wheel and Glue entry script to Amazon S3, and provisions/updates the AWS Glue job itself via Terraform.

# Architecture
![architecture_pic](/docs/image/cloud_architecture.png)

GitHub Actions builds and deploys the framework into the AWS account (region: Thailand). The **processing layer** runs the framework as an AWS Glue job, reading its configs, and glue entrypoint script from the **Artifacts S3 bucket**. It als read source file from the **Inbound** and land ETL output across **Storage** (raw/persist/curated) S3 buckets. Table metadata is registered in the **Glue Catalog** using **Apache Iceberg** as the table format, which **Athena** then queries directly. A Data Engineer IAM user manages the pipeline/framework side, while a Data Analytic IAM user consumes the curated data through Athena.

> **Note:** the S3 buckets shown above (Artifacts, Inbound, Storage) are provisioned via Terraform in a separate repo: [aws-s3-bucket-terraform](https://github.com/natakorn-chp/aws-s3-bucket-terraform). They are not created by this repo's CI/CD pipeline.

# Getting started

Before running the project, complete the following setup steps:
- Create an AWS account.
- Provision the required AWS infrastructure (S3 buckets, Glue catalog/tables, etc.).
- Upload the two configuration files and sample data to your buckets.
- Create a Glue job, then configure it using the [Glue job settings](#setting-up-the-glue-job) below and the [entry script](docs/glue_script/framework.py).
- Create an IAM role for GitHub Actions to assume via OIDC ([guide](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)).
- Add the required repository secrets and variables.

# Usage
Once set up, trigger the __'workflow-deploy-framework'__ workflow from the Actions tab, selecting the target environment. The workflow will:
1. Build the framework wheel package and upload it to the Artifacts S3 bucket.
2. Upload the Glue entry script to the Artifacts S3 bucket.
3. Run Terraform to provision/update the AWS Glue job with the latest script and configuration.

Once the workflow completes, the Glue job is ready to run against your uploaded configuration files and sample data.
