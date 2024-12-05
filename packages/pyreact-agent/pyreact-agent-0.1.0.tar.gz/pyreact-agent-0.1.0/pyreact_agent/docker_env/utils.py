import docker
import os
import time

container_cache = dict()


def get_docker_container(container_name: str = "my-python-container"):
    # Initialize Docker client
    client = docker.from_env()

    if container_name in container_cache:
        return container_cache[container_name]
    else:
        # List all running containers and find your container by name or ID
        containers = client.containers.list()

        # Find the container
        container = None
        for c in containers:
            if container_name in c.name:
                container = c
                break

        if not container:
            raise ValueError(f"Container not found {container_name}")
        else:
            container_cache[container_name] = container
            return container


# Cache for Docker images to avoid redundant lookups
image_cache = {}


def get_docker_image(image_name: str = "my-python-env"):
    """
    Get a Docker image object by name or ID.

    :param image_name: Name or ID of the Docker image to retrieve.
    :type image_name: str
    :return: Docker image object.
    :rtype: docker.models.images.Image
    :raises ValueError: If the image is not found.
    """
    # Initialize Docker client
    client = docker.from_env()

    # Check cache first
    if image_name in image_cache:
        return image_cache[image_name]

    try:
        # Retrieve the image
        image = client.images.get(image_name)

        # Cache the image for future calls
        image_cache[image_name] = image
        return image
    except docker.errors.ImageNotFound:
        raise ValueError(f"Docker image not found: {image_name}")


def build_docker_image(dockerfile_path: str = None,
                       image_name: str = "my-python-env",
                       no_duplicate_build: bool = True) -> None:
    """
    Build a Docker image from a Dockerfile.

    :param dockerfile_path: Path to the Dockerfile. If None, defaults to the directory where this script is located.
    :type dockerfile_path: str, optional
    :param image_name: Name to give the Docker image.
    :type image_name: str
    :param no_duplicate_build: Whether to skip building the Docker image if it already exists.
    :type no_duplicate_build: bool
    :return: None
    :rtype: None
    """
    # Use the current directory as default Dockerfile location
    if dockerfile_path is None:
        dockerfile_path = os.path.dirname(os.path.abspath(__file__))

    # Initialize Docker client
    client = docker.from_env()

    if no_duplicate_build:
        try:
            image = get_docker_image(image_name=image_name)
            if image:
                raise NameError(f"Image {image_name} already exists")
        except ValueError:
            pass  # Image doesn't exist, good to go

    print(f"Building Docker image '{image_name}' from Dockerfile at '{dockerfile_path}'...")
    try:
        # Build the image
        image, logs = client.images.build(
            path=dockerfile_path,
            tag=image_name,
            rm=True
        )

        # Output the logs from the build process
        for log in logs:
            if "stream" in log:
                print(log["stream"].strip())

        print(f"Successfully built Docker image '{image_name}'.")
    except docker.errors.BuildError as build_err:
        print(f"Error during Docker image build: {build_err}")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")


def start_python_docker_environment(
        image_name: str,
        local_bound_dir: str = None,
        container_name: str = None
) -> None:
    """
    Start a Docker container with the specified image, bind a local directory,
    and execute a Python script inside it.

    :param image_name: Name of the Docker image to use.
    :type image_name: str
    :param local_bound_dir: Path to the local directory to bind to the container. Defaults to `os.getcwd()/app` if None.
    :type local_bound_dir: str, optional
    :param container_name: Name to assign to the Docker container. If None, Docker will assign a random name.
    :type container_name: str, optional
    :return: None
    :rtype: None
    """
    # Initialize Docker client
    client = docker.from_env()

    if local_bound_dir is None:
        local_bound_dir = f"{os.getcwd()}/app"

    # Create and start a container
    container = client.containers.run(
        image_name,
        detach=True,
        volumes={local_bound_dir: {'bind': '/app', 'mode': 'rw'}},
        name=container_name  # Specify the container name
    )

    # Wait a bit to ensure the container is fully started
    time.sleep(5)

    # Write Python code to a file inside the container
    code = """
    print("Hello, World!")
    """
    container.exec_run(f"echo '{code}' > /app/test_script.py")

    # Execute the script and capture output
    exec_command = "source venv/bin/activate && python /app/test_script.py"
    stdout, stderr = container.exec_run(exec_command)

    # Print captured outputs
    print("STDOUT:", stdout.decode())
    print("STDERR:", stderr.decode())


def start_container_by_name(container_name: str) -> None:
    """
    Start a stopped Docker container by its name.

    :param container_name: The name of the container to start.
    :type container_name: str
    :return: None
    :rtype: None
    :raises ValueError: If the container is not found or cannot be started.
    """
    # Initialize Docker client
    client = docker.from_env()

    try:
        # Retrieve the container
        container = client.containers.get(container_name)

        # Start the container
        container.start()
        print(f"Container '{container_name}' started successfully.")
    except docker.errors.NotFound:
        raise ValueError(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        raise ValueError(f"Failed to start container '{container_name}': {api_err}")


def stop_container_by_name(container_name: str) -> None:
    """
    Stop a running Docker container by its name.

    :param container_name: The name of the container to stop.
    :type container_name: str
    :return: None
    :rtype: None
    :raises ValueError: If the container is not found or cannot be stopped.
    """
    # Initialize Docker client
    client = docker.from_env()

    try:
        # Retrieve the container
        container = client.containers.get(container_name)

        # Stop the container
        container.stop()
        print(f"Container '{container_name}' stopped successfully.")
    except docker.errors.NotFound:
        raise ValueError(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        raise ValueError(f"Failed to stop container '{container_name}': {api_err}")
