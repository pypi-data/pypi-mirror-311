import shlex
import json

from pyreact_agent.tools.core import ToolSet, tool
from pyreact_agent.docker_env.utils import get_docker_container


# Given a python docker container, get a toolset associated with manipulating files in that container
class PythonDockerToolSet(ToolSet):

    def __init__(self, container_name: str):
        self.container = get_docker_container(container_name=container_name)

    @tool
    def write_content_to_file(self, filename: str, content: str) -> str:
        """
        Use this tool with arguments like "{{"filename": str, "content": str}}" to save the content to a file.
        :param filename: Location of the file
        :param content: Content to be written to the file
        :return: Success message if successful, error message otherwise
        """
        try:
            # Safely escape the filename
            escaped_filename = shlex.quote(filename)

            # Construct a Python script to write the content directly
            python_script = f"""
import os
with open({escaped_filename!r}, 'w') as f:
    f.write({content!r})
"""

            # Execute the Python script inside the container
            command = f"python3 -c {shlex.quote(python_script)}"
            exec_result = self.container.exec_run(command)

            if exec_result.exit_code == 0:
                return f"Successfully wrote content to {filename}"
            else:
                return f"Failed to write content to {filename}: {exec_result.output.decode('utf-8')}"
        except Exception as e:
            return f"Failed to write content to {filename}: {str(e)}"

    @tool
    def read_file(self, filename: str) -> str:
        """
        Use this tool with arguments like "{{"filename": str}}" to read the contents of a file.
        :param filename: Location of the file
        :param content: Content to be written to the file
        :return: Success message if successful, returns error message otherwise
        """
        try:
            # Construct the command to read the file contents
            command = f'cat {filename}'

            # Execute the command inside the container
            exec_result = self.container.exec_run(command)

            if exec_result.exit_code == 0:
                return exec_result.output.decode('utf-8')
            else:
                return f"Failed to read file {filename}: {exec_result.output.decode('utf-8')}"

        except Exception as e:
            return f"Failed to read file {filename}: {e}"

    @tool
    def create_folder(self, directory: str) -> str:
        """
        Use this tool with arguments like "{{"directory": str}}" to create a directory (recursively) if it doesn't exist'
        :param directory: Location of the directory
        :return: Success message if successful, returns error message otherwise
        """
        try:
            # Construct the command to create the directory and any necessary parent directories
            command = f'mkdir -p {directory}'

            # Execute the command inside the container
            exec_result = self.container.exec_run(command)

            if exec_result.exit_code == 0:
                return f"Successfully created directory {directory}"
            else:
                return f"Failed to create directory {directory}: {exec_result.output.decode('utf-8')}"

        except Exception as e:
            return f"Failed to create directory {directory}: {e}"

    @tool
    def run_python_script(self, script_path: str) -> str:
        """
        Use this tool with arguments like "{{"script_path": str}}" to run a Python script inside the container.

        :param script_path: Path of the Python script to be executed
        :return: Dictionary containing stdout and stderr outputs if successful, returns error message otherwise
        """
        try:
            # Construct the command to run the Python script
            command = f'python {script_path}'

            # Execute the command inside the container
            exec_result = self.container.exec_run(command)

            # Decode stdout and stderr from bytes to string
            stdout_output = exec_result.output.decode('utf-8')

            return json.dumps({
                "exit_code": exec_result.exit_code,
                "output": stdout_output
            })

        except Exception as e:
            return json.dumps({
                "error": f"Failed to run script {script_path}: {str(e)}"
            })

    @tool
    def run_bash_code(self, bash_code: str) -> str:
        """
        Use this tool with arguments like "{{"bash_code": str}}" to execute arbitrary Bash code inside a Docker container.
        :param bash_code: Bash code to execute
        :return: Output of the executed Bash code, or an error message if unsuccessful
        """
        try:
            # Safely escape the bash code
            escaped_bash_code = shlex.quote(bash_code)

            # Execute the bash code inside the container
            command = f"sh -c {escaped_bash_code}"
            exec_result = self.container.exec_run(command)

            if exec_result.exit_code == 0:
                # Return the output of the bash code
                return exec_result.output.decode('utf-8').strip()
            else:
                return f"Failed to execute Bash code: {exec_result.output.decode('utf-8')}"
        except Exception as e:
            return f"Failed to execute Bash code: {str(e)}"

    @tool
    def run_python_code(self, python_code: str) -> str:
        """
        Use this tool with arguments like "{{"python_code": str}}" to execute arbitrary Python code inside a Docker container.
        :param python_code: Python code to execute
        :return: Output or result of the executed Python code, or an error message if unsuccessful
        """
        try:
            # Safely escape the Python code for execution
            escaped_python_code = shlex.quote(python_code)

            # Execute the Python code inside the container
            command = f"python3 -c {escaped_python_code}"
            exec_result = self.container.exec_run(command)

            if exec_result.exit_code == 0:
                # Return the output of the Python code
                return exec_result.output.decode('utf-8').strip()
            else:
                return f"Failed to execute Python code: {exec_result.output.decode('utf-8')}"
        except Exception as e:
            return f"Failed to execute Python code: {str(e)}"
