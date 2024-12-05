import requests
from typing import List, Generator

from pyreact_agent.clients.core import BaseLLMClient
from pyreact_agent.message import Message


class OllamaClient(BaseLLMClient):
    """
    A client to interact with Ollama hosted locally.
    """

    def __init__(self, base_url="http://localhost:11434", model="llama3"):
        self.base_url = base_url
        self.model = model

    def query(self, messages: List[Message]) -> Message:
        """
        Sends a prompt to the Ollama LLM and returns the response.
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [self._format_message(message) for message in messages],
                "stream": False
            }
        )

        response.raise_for_status()

        # Handle standard JSON response
        response_json = response.json()
        # Read the returned message
        response_message = response_json.get("message")
        # Get the role and content
        response_role = response_message.get('role').strip()
        response_content = response_message.get('content').strip()
        # Return the message
        return Message(role=response_role, content=response_content)

    def stream(self, messages: List[Message]) -> Generator[Message, None, None]:
        """
        Sends a prompt to the Ollama LLM and returns the response as a stream.
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [self._format_message(message) for message in messages],
                "stream": True
            }
        )

        response.raise_for_status()

        # Handle streaming responses (NDJSON)
        return self._stream_response(response)

    def _stream_response(self, response: requests.Response) -> Generator[Message, None, None]:
        """
        Processes a streaming response, yielding tokens as they arrive.
        """
        for line in response.iter_lines(decode_unicode=True):
            if line.strip():  # Ignore empty lines
                try:
                    token_data = requests.json.loads(line)
                    yield token_data.get("content", "")  # Yield the current token
                except ValueError as e:
                    print(f"Failed to parse line: {line}. Error: {e}")

    def _format_message(self, message: Message):
        return {
            'role': message.role,
            'content': message.content,
            'images': []
        }
