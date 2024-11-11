class Accusation():

    def __init__(self, accuser, suspect, room, weapon):
        self.accuser = accuser  # accuser character name
        self.suspect = suspect  # suspect character name
        self.weapon = weapon    # weapon name or id idk yet
        self.room = room        # room name
        self.result = None

    def set_result(self, result):
        self.result = result

    def __repr__(self):
        return f"Accusation(accuser={self.accuser}, suspect={self.suspect}, weapon={self.weapon}, room={self.room}, result={self.result})"
    
    def to_dict(self):
        return {
            'accuser': self.accuser,
            'suspect': self.suspect,
            'weapon': self.weapon,
            'room': self.room,
            'result': self.result
        }
    
    @classmethod
    def from_dict(cls, data):
        accusation = cls(data['accuser'], data['suspect'], data['room'], data['weapon'])
        accusation.result = data['result']
        return accusation        