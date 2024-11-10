class Suggestion():

    def __init__(self, suggester, suspect, room, weapon):
        self.suggester = suggester  # name
        self.suspect = suspect      # name
        self.weapon = weapon        # name
        self.room = room            # name
        self.disproved = None
        self.disprover = None
    
    def set_result(self, disprover, disproved):
        self.disprover = disprover
        self.disproved = disproved

    def __repr__(self):
        return f"Suggestion(suggester={self.suggester}, suspect={self.suspect}, weapon={self.weapon}, room={self.room}, disprover={self.disprover}, result={self.result})"
    
    def to_dict(self):
        return {
            'suggester': self.suggester,
            'suspect': self.suspect,
            'weapon': self.weapon,
            'room': self.room,
            'disproved': self.status,
            'disprover': self.disprover,
        }
    
    @classmethod
    def from_dict(cls, data):
        suggestion = cls(data['suggester'], data['suspect'], data['room'], data['weapon'])
        suggestion.disproved = data['disproved']
        suggestion.disprover = data['disprover']
        return suggestion