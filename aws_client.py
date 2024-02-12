import boto3
import time
import sys  
sys.tracebacklimit = 0
from botocore.exceptions import ClientError, EndpointConnectionError, ParamValidationError



class AWSClient:
    def __init__(self, access_key_id, secret_access_key, region, group, stream):

        """
        Initializes the AWSClient with credentials and target AWS CloudWatch Logs information.

        Parameters:
            access_key_id (str): AWS access key ID.
            secret_access_key (str): AWS secret access key.
            region (str): AWS region where the log group and stream are to be created.
            group (str): Name of the log group to create or use.
            stream (str): Name of the log stream to create or use within the log group.
        """

        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.group = group
        self.stream = stream
        self.cloudwatch = boto3.client(
                "logs",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            )


    def ensure_log_group_and_stream(self):

        """
        Ensures that the specified log group and log stream exist in AWS CloudWatch Logs.

        Creates the log group and log stream if they do not already exist.
        If creation is not possible due to AWS permissions or other issues,
        the function prints an error message and exits.
        """

        try:
            self.cloudwatch.create_log_group(logGroupName=self.group)
        except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
            pass
        except EndpointConnectionError:
            print(f"Error: Could not connect to the endpoint URL. One of the AWS credentials '{self.region}', '{self.access_key_id}', '{self.secret_access_key}',  is incorrect or unavailable. Please check and try again.")
            sys.exit(1)
        except ClientError as e:
            print("Failed to create log group. Please check your AWS permissions and parameters.")
            sys.exit(1)

        try:
            self.cloudwatch.create_log_stream(logGroupName=self.group, logStreamName=self.stream)
        except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
            pass
        except EndpointConnectionError:
            print(f"Error: Could not connect to the endpoint URL. One of the AWS credentials '{self.region}', '{self.access_key_id}', '{self.secret_access_key}',  is incorrect or unavailable. Please check and try again.")
            sys.exit(1)
        except ClientError as e:
            print("Failed to create log stream. Please check your AWS permissions and parameters.")
            sys.exit(1)

    def send_log(self, message):

        """
        Sends a log message to the specified log stream within the log group.

        Parameters:
            message (str): The log message to be sent.

        If sending the log message is not possible due to AWS permissions or other issues,
        the function prints an error message and exits.
        """

        try:
            self.cloudwatch.put_log_events(
                logGroupName=self.group,
                logStreamName=self.stream,
                logEvents=[{"timestamp": int(time.time() * 1000), "message": message}],
            )
        except ParamValidationError as e:
            print("The 'message' field in your log event sent to AWS CloudWatch is an empty string.")
            sys.exit(1)
        except ClientError as e:
            print("Error sending log data. Please check your AWS permissions, log group, and log stream.")
            sys.exit(1)


