import json


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


# transitions = Transition("name1", "user1", "to user1")
# print(transitions.get_map()) # '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'
# a = json.loads(str(transitions.get_map()))
# i = {'name':'name1', 'from_user':'user1', 'to_user':'to user1'}
# print(a)
# print(i['name'])
