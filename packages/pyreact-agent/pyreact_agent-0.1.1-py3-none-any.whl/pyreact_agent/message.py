

class Message:

    def __init__(self, content: str, role: str = 'user'):
        self.content = content
        self.role = role

    def __str__(self):
        return f"{self.role}: {self.content}"

    def __repr__(self):
        return f"{self.role}: {self.content}"
