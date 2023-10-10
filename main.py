import pygame
import random
    
LARGEUR = 1000
HAUTEUR = 800

CARTE_LARGEUR = 96
CARTE_HAUTEUR = 144

BACKGROUND_COLOR = (11, 127, 57)
BLACK = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

pygame.init()

class Bouton :
    def __init__(self, x, y, l, h, text, textCouleur, couleur, couleurSubbriance) -> None:
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.text = text
        self.textCouleur = textCouleur
        self.couleur = couleur
        self.couleurSubbriance = couleurSubbriance

    def dessiner(self, screen):
        positionSouris = pygame.mouse.get_pos()

        if self.x < positionSouris[0] < self.x + self.l and self.y < positionSouris[1] < self.y + self.h:
            pygame.draw.rect(screen, self.couleurSubbriance, (self.x, self.y, self.l, self.h))
        else :
            pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.l, self.h))

        font = pygame.font.SysFont(None, 56)
        textSurface = font.render(self.text, 1, self.textCouleur)
        textRectangle = textSurface.get_rect(center = (self.x + self.l / 2, self.y + self.h / 2))
        screen.blit(textSurface, textRectangle)

    def estClique(self, positionSouris):
        return self.x < positionSouris[0] < self.x + self.l and self.y < positionSouris[1] < self.y + self.h

class Card :
    suit = None
    value = None

    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value
        self.image = pygame.image.load(f"images/{self.suit}_{self.value}.png")
        self.backImage = pygame.image.load("images/back.png")
        self.faceUp = True
        
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
        if len(self.cards) != 0:
            return self.cards.pop()
        else :
            print("Erreur, plus de cartes dans le deck")
    
    def lenght(self) :
        return len(self.cards)
    
class Hand :
    def __init__(self) -> None:
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)

    def calculerTotal(self):
        total = 0
        asCount = 0
        for card in self.cards:
            if card.value == 1 and total <= 10:
                total += 11
                asCount += 1
            else :
                total += min(card.value, 10)

        while total > 21 and asCount != 0:
            total -= 10
            asCount -= 1
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
        
    def hit(self, deck):
        card = deck.deal()
        self.hand.addCard(card)

    def isBusted(self):
        return self.hand.calculerTotal() > 21

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
        self.boutonTirer = Bouton(LARGEUR - 200, HAUTEUR / 2, 150, 50, "Tirer", BLACK, BLANC, ROUGE)
        self.message = ""
        self.boutonRecommencer = Bouton(0, HAUTEUR / 2, 300, 50, "Recommencer", BLACK, BLANC, ROUGE)

    def afficherMessage(self, screen, message):
        font = pygame.font.SysFont(None, 56)
        textSurface = font.render(message, 1, BLACK)
        textRectangle = textSurface.get_rect(center = (LARGEUR/2, HAUTEUR/2))
        screen.blit(textSurface, textRectangle)

    def play(self):
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())

        if self.player.hand.hasBlackjack() and self.dealer.hand.hasBlackjack():
            print("les deux joueurs ont gagnés")
            self.message = "egalité"
        elif self.player.hand.hasBlackjack():
            self.message = "BlackJack"  
        elif self.dealer.hand.hasBlackjack():
            self.message("Perdu")   
        else :
            self.dealer.retournerCarte(0)

        running = True

        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.boutonTirer.estClique(pygame.mouse.get_pos()) and not self.player.hand.calculerTotal() >= 21:
                        self.player.hit(self.deck)
                        if self.player.isBusted():
                            self.message = "Bust !"
                        elif self.player.hand.calculerTotal() == 21:
                            self.message = "21"
    
                    if self.message and self.boutonRecommencer.estClique(pygame.mouse.get_pos()):
                        self.__init__()
                        self.play()
                        return
                    
            self.screen.fill(BACKGROUND_COLOR)
            self.boutonTirer.dessiner(self.screen)
            self.player.dessiner(self.screen, HAUTEUR - CARTE_HAUTEUR - 15)
            self.dealer.dessiner(self.screen, 15)
            if self.message:
                self.afficherMessage(self.screen, self.message)
                self.boutonRecommencer.dessiner(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

    

game = Game()
game.play()










