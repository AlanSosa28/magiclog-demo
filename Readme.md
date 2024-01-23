
# Alan's Flask Application Deployment to EKS

This repository contains a Flask application designed to calculate a person's age based on their provided date of birth. It is containerized using Docker and deployed to an Amazon EKS cluster using a GitHub Actions workflow.

## Application Overview

`app.py` is a Flask application with the following functionality:

- **Endpoint `/birthday`**: 
  - Method: POST
  - Accepts JSON payload with two fields: `name` (string) and `date` (string in `dd-mm-YYYY` format).
  - Calculates the age of the person from the provided birth date.
  - Returns the person's name along with their calculated age in years.
  - Handles error for future birth dates by returning a `400` status code.

## How to Use

To use the application:

1. Send a POST request to the `/birthday` endpoint with a JSON body:
   ```json
   {
     "name": "Alice",
     "date": "15-04-1990"
   }
   ```
2. The application will respond with the calculated age:
   ```json
   {
     "data": "Alice is 32 years old"
   }
   ```

## Deployment

The application is deployed to AWS EKS using the provided GitHub Actions workflow in `.github/workflows/deploy.yml`.

- The workflow automates the process of:
  - Building a Docker image.
  - Pushing it to Docker Hub.
  - Updating Kubernetes manifests.
  - Applying the manifests to the EKS cluster.

## AWS Integration

The GitHub Actions workflow includes steps to configure AWS credentials and update `kubeconfig` for Kubernetes command-line tool (`kubectl`) interactions with the Amazon EKS cluster.

Details on how the application connects to AWS are as follows:

- **AWS Credentials**: The workflow uses secrets stored in the GitHub repository to authenticate with AWS. The necessary secrets like `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and others are set in the repository's settings.

- **EKS Cluster Configuration**: Using the `aws eks update-kubeconfig` command, the workflow configures `kubectl` with the appropriate access details to interact with the EKS cluster.

## Project Structure

```
.
├── .github
│   └── workflows
│       └── deploy.yml
├── docker
│   └── Dockerfile
└── manifest
    ├── deployment.yaml
    ├── ingress.yaml
    └── service.yaml
```

## Dockerfile

The Dockerfile in the `docker` directory outlines the steps to create a Docker image of the Flask application. The image is based on Python 3.9-slim and includes all necessary dependencies.

## GitHub Actions Workflow (`deploy.yml`)

- Triggered on push to the `main` branch or manual dispatch.
- Builds the Docker image with the Git commit hash as a tag.
- Pushes the image to Docker Hub.
- Configures AWS credentials and updates `kubeconfig`.
- Applies the updated Kubernetes manifests to the EKS cluster.

For more details on the workflow, refer to the `.github/workflows/deploy.yml` file in this repository.

## Notes

- Ensure you have the correct permissions and roles configured in AWS IAM to allow the GitHub Actions workflow to interact with EKS.
- Review and adjust the Kubernetes manifests in the `manifest` directory to match your deployment requirements.
