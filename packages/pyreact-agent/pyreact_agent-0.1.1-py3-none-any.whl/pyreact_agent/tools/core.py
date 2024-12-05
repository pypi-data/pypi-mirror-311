from typing import List, Callable, Dict
from functools import wraps


def tool(func):
    """
    Decorator to mark a method as a tool.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_tool = True
    return wrapper


# Base class for ToolSets, which are logical groupings of tools that depend on user/application variables
class ToolSet:
    def get_tool_list(self) -> List[Callable]:
        """
        Returns a list of tool functions defined in the ToolSet.
        """
        return [
            getattr(self, method) for method in dir(self)
            if callable(getattr(self, method)) and getattr(getattr(self, method), "_is_tool", False)
        ]

    def get_tool_dict(self) -> Dict[str, Callable]:
        """
        Returns a dictionary of tool functions with method names as keys.
        """
        return {
            method: getattr(self, method) for method in dir(self)
            if callable(getattr(self, method)) and getattr(getattr(self, method), "_is_tool", False)
        }


# Helper class to build tools
class Tools:
    def __init__(self, tool_list: List[Callable] = None, tool_sets: List[ToolSet] = None):
        self.tools = {}
        if tool_list:
            self._register_tool_list(tool_list)
        if tool_sets:
            self._register_tool_sets(tool_sets)
        self.tools_string = "\n".join(f"- {name}: {func.__doc__}" for name, func in self.tools.items())

    def _register_tool_list(self, tool_list: List[Callable]):
        """
        Registers a list of tool functions.
        """
        for tool in tool_list:
            self.tools[tool.__name__] = tool

    def _register_tool_sets(self, tool_sets: List[ToolSet]):
        """
        Registers tools from multiple ToolSet instances.
        """
        for tool_set in tool_sets:
            self.tools.update(tool_set.get_tool_dict())

    def __contains__(self, item):
        return item in self.tools

    def invoke_tool(self, tool_name: str, *args, **kwargs):
        """
        Invokes a tool by name.
        """
        if tool_name in self.tools:
            return self.tools[tool_name](*args, **kwargs)
        else:
            raise ValueError(f"Tool '{tool_name}' not found.")
