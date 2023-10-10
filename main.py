import pygame
import random
    
LARGEUR = 1000
HAUTEUR = 800

CARTE_LARGEUR = 96
CARTE_HAUTEUR = 144

BACKGROUND_COLOR = (11, 127, 57)

pygame.init()

class Card :
    suit = None
    value = None

    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value
        self.image = pygame.image.load(f"images/{self.suit}_{self.value}.png")
        self.backImage = pygame.image.load("images/back.png")
        self.faceUp = False
        
    def flip(self):
        self.faceUp = not self.faceUp

class Deck :
    cards = None

    def __init__(self) -> None:
        self.cards = []
        for suit in ["S", "H", 'C', 'D']:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) :
        return self.cards.pop()
    
    def lenght(self) :
        return len(self.cards)
    
class Hand :
    def __init__(self) -> None:
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)

    def calculerTotal(self):
        total = 0
        for card in self.cards:
            if card.value == 1 and total <= 10:
                total += 11
            else :
                total += min(card.value, 10)
        return total
    
    def hasBlackjack(self):
        if len(self.cards) != 2:
            return False
        
        asPresent = self.cards[0].value == 1 or self.cards[1].value == 1
        dixPresent = self.cards[0].value in [10, 11, 12, 13] or self.cards[1].value in [10, 11, 12, 13]

        if asPresent and dixPresent :
            return True
        else : 
            return False
    

    
class Player :

    def __init__(self) -> None:
        self.hand = Hand()
        self.money = 500

    def dessiner(self, screen, y):
        xOffset = round((LARGEUR - CARTE_LARGEUR - 15)/2)
        for card in self.hand.cards:
            imageToDraw = card.image if card.faceUp else card.backImage
            screen.blit(imageToDraw, (xOffset, y))
            xOffset += 20
    def retournerCarte(self, index):
        if index < len(self.hand.cards):
            self.hand.cards[index].flip()

class Dealer(Player):
    pass

class Game :
    def __init__(self) -> None:
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.shuffle()
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Blackjack")
        self.clock = pygame.time.Clock()

    def play(self):
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())

        if self.player.hand.hasBlackjack() and self.dealer.hand.hasBlackjack():
            #les deux joueurs ont gagnés
            self.player.retournerCarte(0)
            self.player.retournerCarte(1)
            self.dealer.retournerCarte(0)
            self.dealer.retournerCarte(1)
        elif self.player.hand.hasBlackjack():
            #le joueur a gagné
            self.player.retournerCarte(0)
            self.player.retournerCarte(1)
            self.dealer.retournerCarte(0)
            self.dealer.retournerCarte(1)   
        elif self.dealer.hand.hasBlackjack():
            #le dealer a gagné
            self.player.retournerCarte(0)
            self.player.retournerCarte(1)
            self.dealer.retournerCarte(0)
            self.dealer.retournerCarte(1)    
        else :
            self.player.retournerCarte(0)
            self.player.retournerCarte(1)

            self.dealer.retournerCarte(1)

        running = True

        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BACKGROUND_COLOR)

            self.player.dessiner(self.screen, HAUTEUR - CARTE_HAUTEUR - 15)
            self.dealer.dessiner(self.screen, 15)

            pygame.display.flip()
            self.clock.tick(60)

game = Game()
game.play()










