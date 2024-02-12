import argparse
from aws_client import AWSClient
from docker_stream import DockerClient
from docker.errors import DockerException

def main():
    parser = argparse.ArgumentParser(description="Run Docker container and stream logs to AWS CloudWatch")
    parser.add_argument("--docker-image", required=True, help="Docker image name")
    parser.add_argument("--bash-command", required=True, help="Bash command to execute in the Docker container")
    parser.add_argument("--aws-cloudwatch-group", required=True, help="AWS CloudWatch log group name, a new one is created if name does not exist")
    parser.add_argument("--aws-cloudwatch-stream", required=True, help="AWS CloudWatch log stream name, a new one is created if name does not exist")
    parser.add_argument("--aws-access-key-id", required=True, help="AWS Access Key ID")
    parser.add_argument("--aws-secret-access-key", required=True, help="AWS Secret Access Key")
    parser.add_argument("--aws-region", required=True, help="AWS Region")

    args = parser.parse_args()

    aws_client = AWSClient(args.aws_access_key_id, args.aws_secret_access_key, args.aws_region, args.aws_cloudwatch_group, args.aws_cloudwatch_stream)
    aws_client.ensure_log_group_and_stream()

    docker_client = DockerClient(args.docker_image, args.bash_command)
    container = docker_client.run_container()

    try:
        for line in container.logs(stream=True, follow=True, stderr=True):
            log_message = line.decode('utf-8').rstrip('\n')
            aws_client.send_log(log_message)
    except DockerException as e:
        print(f"Error streaming logs: {e}")

if __name__ == "__main__":
    main()


