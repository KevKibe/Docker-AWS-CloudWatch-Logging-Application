## Introduction
This application facilitates running Docker containers and streaming their logs to AWS CloudWatch. It leverages Python's Docker SDK and Boto3 library for AWS interactions. Below is a comprehensive guide to help developers get started and use the application efficiently.<br>
It's particularly useful for those looking to automate log management and monitoring in a cloud environment.

## Prerequisites
- Python: Ensure Python 3.6 or newer is installed. [Python Installation Guide](https://wiki.python.org/moin/BeginnersGuide/Download) 

- Docker: Docker must be installed and running on your system. [Docker Installation Guide](https://docs.docker.com/engine/install/)

- AWS Account: An AWS account is required, with access to CloudWatch Logs.[AWS Account Setup](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)

## Setup

- Clone the Repository: Clone or download the application code to your local machine.
```
git clone https://github.com/KevKibe/Docker-AWS-CloudWatch-Logging-Application.git
```

- Navigate to the project directory 
```
cd Docker-AWS-CloudWatch-Logging-Application
```

- Create a virtual environment for the project and activate it.
```
python3 -m venv env
source env/bin/activate
```

- Install dependencies by running this command
```
pip install -r requirements.txt
```
- AWS Credentials: Ensure your AWS credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) are present and the AWS Cloudwatch permissions are active.

- Docker Daemon: Verify the Docker daemon is running on your system. The application communicates with Docker to manage containers.


## Usage
Command Line Arguments
- --docker-image: Name of the Docker image to run.
- --bash-command: Bash command to execute inside the Docker container.
- --aws-cloudwatch-group: Name of the AWS CloudWatch log group (will be created if it does not exist).
- --aws-cloudwatch-stream: Name of the log stream within the group (will be created if it does not exist).
- --aws-access-key-id: Your AWS access key ID.
- --aws-secret-access-key: Your AWS secret access key.
- --aws-region: The AWS region for CloudWatch Logs.

## Running the Application
Here is an example:
This continuously logs 'Hello World' to AWS CloudWatch.
```
python main.py \
  --docker-image ubuntu:latest \
  --bash-command "bash -c 'while true; do echo hello world; sleep 1; done'" \
  --aws-cloudwatch-group MyLogGroup \
  --aws-cloudwatch-stream MyLogStream \
  --aws-access-key-id <YourAccessKeyId> \
  --aws-secret-access-key <YourSecretAccessKey> \
  --aws-region us-east-1
```
## Using a Python Script File
If you prefer to run a Python script file, ensure the file is accessible within your directory.
```
python main.py \
  --docker-image python:3.8-slim \
  --bash-command 'bash -c "python /path/to/script.py"' \
  --aws-cloudwatch-group MyLogGroup \
  --aws-cloudwatch-stream MyLogStream \
  --aws-access-key-id <YourAccessKeyId> \
  --aws-secret-access-key <YourSecretAccessKey> \
  --aws-region us-east-1
```
