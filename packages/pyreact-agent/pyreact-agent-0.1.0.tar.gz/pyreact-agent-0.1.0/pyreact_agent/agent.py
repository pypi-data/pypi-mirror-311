from typing import List
import json

from pyreact_agent.tools.core import Tools
from pyreact_agent.clients.core import BaseLLMClient
from pyreact_agent.message import Message


class ActionResponseParsingError(Exception):
    """Error used when a response is not properly parsed."""


# ReAct agent
class ReActAgent:
    def __init__(self, llm_client: BaseLLMClient, tools: Tools, verbose: bool=False):
        self.llm_client = llm_client
        self.tools = tools
        self.verbose = verbose
        self.memory: List[Message] = []  # To keep track of the reasoning and actions taken.

    def _get_system_message(self):
        return Message(
            role='system',
            content=(
                f"You're a helpful agent that can reason and act to answer questions. "
                f"You have the following tools:\n{self.tools.tools_string}\n\n" 
                f"Your goal is to answer/execute the User's query/instructions, "
                f"which is found after 'User: <user question>'. In order to do so, "
                f"read previous thoughts, actions, observations, and summaries to evaluate your progress. "
                f"After reading, summarize your progress so far with '\\n\\nSummary: <progress summary>'. "
                f"Then think about what your next action should be "
                f"and express your thoughts with '\\n\\nThought: <internal thoughts>'. "
                f"After expressing your thoughts, if you want to take another action using a tool, "
                f"respond with '\\n\\nAction: <tool_name> Action Input: <tool_input>'. "
                f"If instead you have a final answer to the original question, "
                f"provide the final answer directly with '\\n\\nFinal Answer: <final answer>.'"
            )
        )

    def reason_and_act(self, question):
        """
        Main loop of the ReAct agent.
        """
        # Setup system prompt
        self.memory.append(self._get_system_message())

        if self.verbose:
            print(f"=============\n--- User ---\n=============\n {question}")
        self.memory.append(Message(role='user', content=question + "\n\nSummary:"))

        while True:

            # Query LLM
            response_message = self.llm_client.query(self.memory)
            response = response_message.content
            if self.verbose:
                print(f"==============\n--- Agent ---\n==============\n {response}")
            self.memory.append(response_message)
            yield response_message

            if "Action:" in response:
                # I
                # Extract tool name and input
                try:
                    tool_name, tool_input = self._parse_action(response)
                except ActionResponseParsingError as e:
                    message = f"{e}"
                    if self.verbose:
                        print(f"=============\n--- Tool ---\n=============\n {message}")
                    tool_message = Message(role='tool', content=message)
                    self.memory.append(tool_message)
                    yield tool_message
                    continue  # Try loop again

                if tool_name in self.tools.tools:
                    # Use the tool
                    try:
                        tool_result = self.tools.tools[tool_name](**tool_input)
                    except Exception as e:
                        message = (f"Tool Result: Tool '{tool_name}' failed to execute with inputs {tool_input} "
                                   f"and error: {e}")
                        if self.verbose:
                            print(f"=============\n--- Tool ---\n=============\n {message}")
                        tool_message = Message(role='tool', content=message)
                        self.memory.append(tool_message)
                        yield tool_message
                        continue
                    message = f"Tool Result: Tool '{tool_name}' executed with result: {tool_result}"
                    if self.verbose:
                        print(f"=============\n--- Tool ---\n=============\n {message}")
                    tool_message = Message(role='tool', content=message)
                    self.memory.append(tool_message)
                    yield tool_message
                    continue  # Try loop again
                else:
                    message = f"Tool Result: Tool '{tool_name}' does not exist, " \
                              f"please choose from:\n{self.tools.tools_string}"
                    if self.verbose:
                        print(f"=============\n--- Tool ---\n=============\n {message}")
                    tool_message = Message(role='tool', content=message)
                    self.memory.append(tool_message)
                    yield tool_message
                    continue  # Try loop again
            else:
                # Stop reasoning loop if the LLM provides a final answer
                break

    def _construct_prompt(self):
        """
        Constructs the prompt for the LLM based on memory and tools.
        """
        # TODO: clean up memory to only include summaries past a certain point/token limit
        memory_lines = [f"Memory ID: {memory_id}, {memory}" for memory_id, memory in enumerate(self.memory)]
        memory_str = "\n".join(memory_lines)
        return (
            f"You're a helpful agent that can reason and act to answer questions. "
            f"You have the following tools:\n{self.tools.tools_string}\n\n"
            f"Your goal is to answer/execute the User's query/instructions, "
            f"which is found after 'User: <user question>'. In order to do so, "
            f"read previous thoughts, actions, observations, and summaries to evaluate your progress. "
            f"\n\nPrevious thoughts, actions, observations, and summaries can be found below: \n\n"
            f"{memory_str}\n\n"
            f"After reading, summarize your progress so far with '\\n\\nSummary: <progress summary>'. "
            f"Then think about what your next action should be "
            f"and express your thoughts with '\\n\\nThought: <internal thoughts>'. "
            f"After expressing your thoughts, if you want to take another action using a tool, "
            f"respond with '\\n\\nAction: <tool_name> Action Input: <tool_input>'. "
            f"If instead you have a final answer to the original question, "
            f"provide the final answer directly with '\\n\\nFinal Answer: <final answer>.'"
        )

    def _parse_action(self, response: str):
        """
        Parses the action string to extract the tool name and input.
        Example format: 'calculate(3 + 4)'
        """
        try:
            tool_info = response.split("Action:")[-1]
        except ValueError:
            raise ActionResponseParsingError(
                "Failed to split 'Action:' from response. "
                "Make sure both 'Action:' and 'Action Input:' are present "
                "when invoking a tool."
            )

        try:
            tool_name, tool_input = tool_info.split("Action Input:", 1)
        except ValueError:
            raise ActionResponseParsingError(
                "Failed to split 'Action Input:' from response. "
                "Make sure both 'Action:' and 'Action Input:' are present "
                "when invoking a tool."
            )
        tool_input = tool_input.strip()
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError as e:
            raise ActionResponseParsingError(
                f"Failed to JSON decode action input: \n{tool_input}\n\n "
                f"With the following JSONDecodeError: {e}"
                f"Make sure that the argument for 'Action Input:' is a valid JSON string."
            )
        return tool_name.strip(), tool_input
