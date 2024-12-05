from abc import ABC, abstractmethod
from typing import List

from pyreact_agent.message import Message


class BaseLLMClient(ABC):
    @abstractmethod
    def query(self, prompt: List[Message]) -> Message:
        raise NotImplementedError
