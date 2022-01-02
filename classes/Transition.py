class Transition:
    def __init__(self, name: str, from_user: str, to_user: str):
        self.name = name
        self.from_user = from_user
        self.to_user = to_user

    def __eq__(self, other):
        return self.name == other.name

