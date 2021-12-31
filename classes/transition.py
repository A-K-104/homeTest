class Transition:
    def __init__(self, name: str, from_user: str, to_user: str):
        self.name = name
        self.from_user = from_user
        self.to_user = to_user

    def get_map(self):
        return '{"name"' + ':"' + self.name + '"' +\
               ', "from_user"' + ':"' + self.from_user +\
               '"' + ', "to_user"' + ':"' + self.to_user + '"}'


def decode_json(json_str):
    return Transition(json_str['name'], json_str['from_user'], json_str['to_user'])

