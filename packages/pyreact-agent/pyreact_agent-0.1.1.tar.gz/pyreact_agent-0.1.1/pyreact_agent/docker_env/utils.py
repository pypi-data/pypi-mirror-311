import docker
import os
import time

container_cache = dict()
image_cache = dict()


def get_docker_client(docker_url: str = None):
    """
    Initialize a Docker client. If running inside a Docker container,
    ensure the Docker socket is available.

    :param docker_url: Docker daemon URL. Defaults to None, which uses the local Docker environment.
    :type docker_url: str, optional
    :return: Docker client object.
    :rtype: docker.DockerClient
    """
    if docker_url:
        return docker.DockerClient(base_url=docker_url)
    return docker.from_env()


def get_docker_container(container_name: str = "my-python-container", docker_url: str = None):
    """
    Get a Docker container object by name or ID.

    :param container_name: Name or ID of the Docker container.
    :type container_name: str
    :param docker_url: Docker daemon URL. Defaults to None for local Docker environment.
    :type docker_url: str, optional
    :return: Docker container object.
    :rtype: docker.models.containers.Container
    """
    client = get_docker_client(docker_url)

    if container_name in container_cache:
        return container_cache[container_name]

    try:
        # Retrieve the container
        container = client.containers.get(container_name)
        container_cache[container_name] = container
        return container
    except docker.errors.NotFound:
        raise ValueError(f"Container '{container_name}' not found.")


def get_docker_image(image_name: str = "my-python-env", docker_url: str = None):
    """
    Get a Docker image object by name or ID.

    :param image_name: Name or ID of the Docker image.
    :type image_name: str
    :param docker_url: Docker daemon URL. Defaults to None for local Docker environment.
    :type docker_url: str, optional
    :return: Docker image object.
    :rtype: docker.models.images.Image
    """
    client = get_docker_client(docker_url)

    if image_name in image_cache:
        return image_cache[image_name]

    try:
        # Retrieve the image
        image = client.images.get(image_name)
        image_cache[image_name] = image
        return image
    except docker.errors.ImageNotFound:
        raise ValueError(f"Docker image '{image_name}' not found.")


def build_docker_image(dockerfile_path: str = None, image_name: str = "my-python-env", docker_url: str = None):
    """
    Build a Docker image from a Dockerfile.

    :param dockerfile_path: Path to the Dockerfile. Defaults to the directory where this script is located.
    :type dockerfile_path: str, optional
    :param image_name: Name to give the Docker image.
    :type image_name: str
    :param docker_url: Docker daemon URL. Defaults to None for local Docker environment.
    :type docker_url: str, optional
    :return: None
    :rtype: None
    """
    if dockerfile_path is None:
        dockerfile_path = os.path.dirname(os.path.abspath(__file__))

    client = get_docker_client(docker_url)

    print(f"Building Docker image '{image_name}' from Dockerfile at '{dockerfile_path}'...")
    try:
        image, logs = client.images.build(path=dockerfile_path, tag=image_name, rm=True)
        for log in logs:
            if "stream" in log:
                print(log["stream"].strip())
        print(f"Successfully built Docker image '{image_name}'.")
    except docker.errors.BuildError as build_err:
        print(f"Error during Docker image build: {build_err}")
    except docker.errors.APIError as api_err:
        print(f"Docker API error: {api_err}")


def run_docker_image(
        image_name: str,
        local_bound_dir: str = None,
        container_name: str = None,
        docker_url: str = None
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
    :param docker_url: Docker daemon URL. Defaults to None for local Docker environment.
    :type docker_url: str, optional
    :return: None
    :rtype: None
    """
    # Initialize Docker client
    client = get_docker_client(docker_url)

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


def start_container_by_name(container_name: str, docker_url: str = None):
    """
    Start a stopped Docker container by its name.

    :param container_name: The name of the container to start.
    :type container_name: str
    :param docker_url: Docker daemon URL. Defaults to None for local Docker environment.
    :type docker_url: str, optional
    :return: None
    :rtype: None
    """
    client = get_docker_client(docker_url)
    try:
        container = client.containers.get(container_name)
        container.start()
        print(f"Container '{container_name}' started successfully.")
    except docker.errors.NotFound:
        raise ValueError(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        raise ValueError(f"Failed to start container '{container_name}': {api_err}")


def stop_container_by_name(container_name: str, docker_url: str = None):
    """
    Stop a running Docker container by its name.

    :param container_name: The name of the container to stop.
    :type container_name: str
    :param docker_url: Docker daemon URL. Defaults to None for local Docker environment.
    :type docker_url: str, optional
    :return: None
    :rtype: None
    """
    client = get_docker_client(docker_url)
    try:
        container = client.containers.get(container_name)
        container.stop()
        print(f"Container '{container_name}' stopped successfully.")
    except docker.errors.NotFound:
        raise ValueError(f"Container '{container_name}' not found.")
    except docker.errors.APIError as api_err:
        raise ValueError(f"Failed to stop container '{container_name}': {api_err}")
