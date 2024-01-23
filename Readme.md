
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

# Dockerfile Description and Security Aspects

The Dockerfile provided for the Flask application employs several best practices for security and efficiency:

1. **Base Image**:
   - `FROM python:3.9-slim`: Utilizes an official Python base image, specifically the 'slim' variant, which is a minimized version containing only essential components. This reduces the overall image size and minimizes the attack surface by limiting the number of packages and potential vulnerabilities.

2. **Package Installation**:
   - The `RUN apt-get update` and `install` commands are used to install necessary system dependencies. The `--no-install-recommends` flag is included to avoid installing unnecessary packages, further reducing the image size and potential attack vectors.
   - The command `rm -rf /var/lib/apt/lists/*` is used to clear the package manager cache. This removal reduces the image size and removes unnecessary files that could potentially include sensitive information.

3. **Non-Root User**:
   - `RUN useradd -m alan`: Creates a non-root user named 'alan' to run the application. This is a crucial security practice to mitigate the effects of a container breakout. If an attacker compromises the application, they would have limited permissions, unlike a root user.
   - `USER alan`: Switches the user context to the non-root user 'alan'. All subsequent commands in the Dockerfile and the running container will execute with the permissions of this user.

4. **Working Directory**:
   - `WORKDIR /home/alan/app`: Sets the working directory to `/home/alan/app`. This directory becomes the default location for any RUN, CMD, ENTRYPOINT, COPY, and ADD instructions that follow in the Dockerfile.

5. **Copying Application Files**:
   - The `COPY` instructions transfer the application files `requirements.txt` and `app.py` into the container. They are owned by the non-root user 'alan', which aligns with the principle of least privilege.
   - `RUN pip install`: Installs the Python dependencies listed in `requirements.txt`. The `--user` flag installs packages locally for the non-root user, and `--no-cache-dir` avoids caching the downloaded packages, which is good for security and minimizing image size.

6. **Exposing Ports**:
   - `EXPOSE 5000`: Exposes port 5000, which is the default port for Flask applications. This instruction is used for documentation purposes and does not actually publish the port.

7. **Environment Variables**:
   - `ENV FLASK_APP=app.py` and `ENV FLASK_RUN_HOST=0.0.0.0`: These environment variables are set for Flask. `FLASK_RUN_HOST=0.0.0.0` tells Flask to listen on all network interfaces, which is necessary in a containerized environment.

8. **Running the Application**:
   - `CMD ["python", "-m", "flask", "run"]`: The command to run the Flask application when the container starts. Using the array format for `CMD` ensures that the application is run directly and not within a shell, which is more secure and avoids any shell injection vulnerabilities.

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
