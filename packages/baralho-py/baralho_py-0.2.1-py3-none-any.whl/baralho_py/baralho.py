import random

class Card:
    __suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    __values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    __figures = list(__values.keys())

    def __init__(self, suit: int, value: int):
        self.suit = Card.__suits[suit]
        self.figure = Card.__figures[value] 
        self.value = Card.__values[self.figure]

    def __str__(self) -> str:
        return f'{self.figure} of {self.suit}'

    def __repr__(self) -> str:
        return f'\'{self.figure} of {self.suit}\''

    def __gt__(self, other: 'Card') -> bool:
        return self.value > other.value

    def __lt__(self, other: 'Card') -> bool:
        return self.value < other.value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value
    
class Player:
    
    def __init__(self, name: str, cards: list[Card] | None = None):
        if cards is None:
            cards = []

        self.name = name
        self.cards = cards

    def play(self) -> tuple['Player', Card]:
        return (self, self.cards.pop(0))
    
    def receive(self, cards: list[Card]) -> None:
        self.cards += cards

    def get_total_cards(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return str({'name': self.name, 'cards': self.cards})

    def __repr__(self) -> str:
        return str({'name': self.name, 'cards': self.cards})
    
class Deck:
    
    def __init__(self) -> None:
        self.cards: list[Card] = []
        for suit in range(4):
            for value in range(13):
                self.cards.append(Card(suit, value))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def distribute(self, players: list[Player]) -> None:
        quantity = len(self.cards) // len(players)
        
        self.shuffle()

        decks: list[list[Card]] = []

        for i in range(len(players)):
          decks.append([])
          for _ in range(quantity):     
            decks[i].append(self.cards.pop())

        for player in players:
            deck = decks.pop()

            player.receive(deck)
    
    def __str__(self) -> str:
        string = ''

        for card in self.cards:
            string += card.__str__() + '\n'

        return string
            
class Game:
    
    def __init__(self, players_names: list[str]):
        self.deck = Deck()
        self.players = [Player(name) for name in players_names]
        self.deck.distribute(self.players)
        self.draw_cards: list[Card] = []
        self.rounds = 0

    def round(self) -> None:
        plays: list[tuple[Player, Card]] = []
        self.rounds += 1
        
        print(f'Round {self.rounds}\n')
        self.show_player_total_cards()
        print()

        for player in self.players:
            play = player.play()
            plays.append(play)
            print(f'{player.name} played {play[1]}')

        print()
        
        winner = plays[-1]
        draw = False
        
        for idx in range(len(plays) - 1):
            if plays[idx][1] > winner[1]:
                winner = play
            elif plays[idx][1] == winner[1]:
                draw = True
        
        if draw:
            for _, card in plays:
              self.draw_cards.append(card)

            print('Draw!\n')
        else:
            print(f'{winner[0].name} won the round with {winner[1]}\n')
            winner[0].receive([card for _, card in plays])
            winner[0].receive([card for card in self.draw_cards])
            self.draw_cards = []
        
        self.show_player_total_cards()

        for player in self.players:
            if not len(player.cards):
                self.players.remove(player)
        
        input('\nPress Enter to continue...\n')

    def start(self) -> None:
        print('Game started!\n')
        while len(self.players) > 1:
            self.round()
        
        print(f'{self.players[0].name} won the game!')

    def show_player_total_cards(self) -> None:
        for player in self.players:
            print(f'{player.name} has {player.get_total_cards()} cards')
            