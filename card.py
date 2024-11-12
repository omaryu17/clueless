class Card():

    def __init__(self, card_type, name):
        assert card_type in ["room","weapon","suspect"], f"Card type must be room, weapon, or suspect not: {card_type}"
        self.card_type = card_type
        self.name = name

    def get_info(self):
        return self.card_type, self.name
    
    def __repr__(self):
        return f"Card(type={self.card_type}, name='{self.name}')"
    
    def to_str(self):
        return f"{self.card_type}:{self.name}"
    
    @classmethod
    def from_str(cls, card_str):
        card_type, name = card_str.split(":")
        return cls(card_type, name)