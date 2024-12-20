from card import Card
import json
import random


class Deck():

    def __init__(self):
        self.card_list = []
        self.solution = []
        self._load_deck()

    def _load_deck(self):
        # reading from json, but can update to db or something later
        with open('cards.json', 'r') as f:
            cards = json.load(f)
        
        for card in cards: 
            self.card_list.append(Card(card_type=card['type'], name=card['name']))

    def _shuffle(self):
        random.shuffle(self.card_list)

    def get_type_cards(self, card_type):
        """Get all weapons, rooms, or suspects"""
        type_cards = []
        for card in self.card_list:
            if card.get_info()[0] == card_type:
                type_cards.append(card)
        return type_cards

    def _create_solution(self):
        """Select one weapon, room, and suspect to be game solution"""
        card_types = ['weapon', 'suspect', 'room']

        self.solution = []
        # get 1 weapon, suspect, and room
        for card_type in card_types:
            cards = self.get_type_cards(card_type)
            chosen_card = random.choice(cards)
            self.solution.append(chosen_card)
            self.card_list.remove(chosen_card)
    
    def get_solution(self):
        return self.solution

    def deal(self, player_list):
        """Create solution and deal remaining cards to Players"""
        self._shuffle()
        self._create_solution()

        cards_to_deal = [card for card in self.card_list if card not in self.solution]

        num_players = len(player_list)
        for i, card in enumerate(cards_to_deal):
            player_list[i%num_players].add_card(card)
        
        return player_list

        


