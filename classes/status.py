class Status:
    def __init__(self, name: str):
        self.name = name
        self.status = "[ORPHAN]"

    def __eq__(self, other):
        return self.name == other.name
