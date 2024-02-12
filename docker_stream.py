import docker
from docker.errors import APIError, DockerException, ImageNotFound
import sys 

class DockerClient:

    """
    A client for managing Docker containers using the Docker SDK for Python.

    This class provides methods to run Docker containers and stream their logs,
    utilizing the Docker SDK to communicate with the Docker daemon.

    Attributes:
        client (docker.DockerClient): A client connection to the Docker server.
        image (str): The Docker image to use for creating containers.
        command (str or list): The command to be executed inside the container.
    """

    def __init__(self, image, command):

        """
        Initializes the DockerClient instance.

        Establishes a Docker client connection from the environment and sets
        the image and command for running containers.

        Parameters:
            image (str): The Docker image name to use for running containers.
            command (str or list): The command to execute inside the container.
        
        """

        try:
            self.client = docker.from_env()  
        except DockerException:
            print("Failed to initialize Docker client. Please ensure Docker is running and accessible.")
            sys.exit(1)  
        self.image = image
        self.command = command


    def run_container(self):

        """
        Runs a Docker container using the specified image and command.

        The container is run in detached mode, allowing this method to return
        a container instance immediately without waiting for the command to complete.

        Returns:
            docker.models.containers.Container: The Docker container instance that was started.

        """

        try:
            container = self.client.containers.run(self.image, self.command, detach=True)
            for line in container.logs(stream=True):
                print(line.strip())
            return container
        except ImageNotFound:
            print(f"Image '{self.image}' not found. Please check the image name and try again.")
            sys.exit(1)
        except APIError:
            print("Server error occurred while trying to run the container. Please try again later.")
            sys.exit(1)
        except DockerException:
            print("General Docker error occurred. Please check your Docker setup and try again.")
            sys.exit(1)

