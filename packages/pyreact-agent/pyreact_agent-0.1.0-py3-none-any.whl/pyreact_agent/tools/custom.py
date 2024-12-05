from datetime import datetime


def get_now(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Use this tool with arguments like "{{"format": str}}" to get the current time
    """
    return datetime.now().strftime(format)
