import pygame
import random
    
LARGEUR = 1000
HAUTEUR = 750

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

    def dessinerPetit(self, screen):
        positionSouris = pygame.mouse.get_pos()

        if self.x < positionSouris[0] < self.x + self.l and self.y < positionSouris[1] < self.y + self.h:
            pygame.draw.rect(screen, self.couleurSubbriance, (self.x, self.y, self.l, self.h))
        else :
            pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.l, self.h))

        font = pygame.font.SysFont(None, 36)
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
        self.cuttingCardDraw = False
        self.cards = []
        for i in range(0, 6):
            for suit in ["S", "H", 'C', 'D']:
                for value in range(1, 14):
                    self.cards.append(Card(suit, value))

    def shuffle(self) -> None:
        random.shuffle(self.cards)
    
    def addCuttingCard(self):
        indexMilieu = round(len(self.cards) // 2)
        self.cards.insert(indexMilieu, Card("R", 0))

    def deal(self) :
        if len(self.cards) != 0:
            card = self.cards.pop()
            if card.suit == 'R':
                self.cuttingCardDraw = True
            return card
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
        self.bet = 50

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
        self.canDouble = False
        self.gameStarted = False
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.addCuttingCard()
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Blackjack")
        self.clock = pygame.time.Clock()
        self.boutonTirer = Bouton(LARGEUR - 200, HAUTEUR / 2, 150, 50, "Tirer", BLACK, BLANC, ROUGE)
        self.message = ""
        self.boutonRecommencer = Bouton(0, HAUTEUR / 2, 300, 50, "Recommencer", BLACK, BLANC, ROUGE)
        self.boutonCecommencer = Bouton(0, HAUTEUR / 2, 300, 50, "Commencer", BLACK, BLANC, ROUGE)
        self.boutonRester = Bouton(LARGEUR - 200, HAUTEUR / 2 - 70, 150, 50, "Rester", BLACK, BLANC, ROUGE)
        self.boutonDoubler = Bouton(LARGEUR - 200, HAUTEUR / 2 + 70, 150, 50, "Doubler", BLACK, BLANC, ROUGE)
        self.boutonAugmenterMise = Bouton(170, HAUTEUR - 95, 30, 30, "+", BLACK, BLANC, ROUGE)
        self.boutonDiminuerMise = Bouton(230, HAUTEUR - 95, 30, 30, "-", BLACK, BLANC, ROUGE)
        self.boutonDoublerMise = Bouton(170, HAUTEUR - 55, 30, 30, "x2", BLACK, BLANC, ROUGE)
        self.boutonDiviserMise = Bouton(230, HAUTEUR - 55, 30, 30, "/2", BLACK, BLANC, ROUGE)

    def reset(self):
        self.gameStarted = True
        if self.deck.cuttingCardDraw:
            self.deck = Deck()
            self.deck.shuffle()
            self.deck.addCuttingCard()
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        self.message = ""

    def afficherMessage(self, screen, message):
        font = pygame.font.SysFont(None, 56)
        textSurface = font.render(message, 1, BLACK)
        textRectangle = textSurface.get_rect(center = (LARGEUR/2, HAUTEUR/2))
        screen.blit(textSurface, textRectangle)

    def dessinerMonaie(self):
        font = pygame.font.SysFont(None, 36)
        textSurface = font.render("Argent : " + str(round(self.player.money)), 1, BLACK)
        textRect = textSurface.get_rect(topleft=(10,HAUTEUR - 50))
        self.screen.blit(textSurface, textRect)

        textSurfaceMise = font.render("Mise : "+ str(round(self.player.bet)), 1, BLACK)
        textMiseRect = textSurfaceMise.get_rect(topleft=(10, HAUTEUR - 90))
        self.screen.blit(textSurfaceMise, textMiseRect)

    def perdre(self):
        self.message = "Perdu !"
        self.player.money -= self.player.bet
        self.gameStarted = False

    def gagner(self):
        self.message = "Gagné !"
        self.player.money += self.player.bet
        self.gameStarted = False

    def egalite(self):
        self.message = "Egalité"
        self.gameStarted = False

    def comparerMains(self):
        self.dealer.retournerCarte(0)
        while self.dealer.hand.calculerTotal() < 17 :
            self.dealer.hit(self.deck)
        if self.player.hand.calculerTotal() > 21 or (self.dealer.hand.calculerTotal() <= 21 and self.player.hand.calculerTotal() < self.dealer.hand.calculerTotal()):
            self.perdre()
        elif self.dealer.hand.calculerTotal() > 21 or (self.dealer.hand.calculerTotal() < self.player.hand.calculerTotal()):
            self.gagner()
        else:
            self.egalite()

    def start(self):
        self.canDouble = True
        self.gameStarted = True
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())

        if self.player.hand.hasBlackjack() and self.dealer.hand.hasBlackjack():
            self.egalite()
        elif self.player.hand.hasBlackjack():
            self.message = "BlackJack"  
            self.player.money += self.player.bet * 1.5
            self.gameStarted = False
        elif self.dealer.hand.hasBlackjack():
            if self.dealer.hand.cards[0] =='1':
                self.perdre() 
            else :
                self.dealer.retournerCarte(0)
        else:
            self.dealer.retournerCarte(0)

        return

    def play(self):
    
        running = True

        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.boutonTirer.estClique(pygame.mouse.get_pos()) and not self.player.hand.calculerTotal() >= 21 and not self.message:
                        self.canDouble = False
                        self.player.hit(self.deck)
                        if self.player.isBusted():
                            self.message = "Bust !"
                            self.player.money -= self.player.bet
                            self.gameStarted = False
                        elif self.player.hand.calculerTotal() == 21:
                            self.comparerMains()

                    if not self.message and self.boutonCecommencer.estClique(pygame.mouse.get_pos()):
                        self.start()

                    if self.boutonRester.estClique(pygame.mouse.get_pos()) and not self.player.isBusted() and not self.message :
                        self.comparerMains()

                    if self.boutonDoubler.estClique(pygame.mouse.get_pos()) and not self.player.hand.calculerTotal() >= 21 and not self.message and self.canDouble:
                        self.player.bet *= 2
                        self.player.hit(self.deck)
                        if self.player.isBusted():
                            self.message = "Bust !"
                            self.player.money -= self.player.bet
                            self.gameStarted = False
                        else: 
                            self.comparerMains()

                        self.player.bet /= 2

    
                    if self.message and self.boutonRecommencer.estClique(pygame.mouse.get_pos()) and self.player.money > 0 and self.player.money >= self.player.bet:
                        self.reset()
                        self.start()
                    
                    if self.boutonAugmenterMise.estClique(pygame.mouse.get_pos()):
                        if self.player.money >= self.player.bet + 10:
                            self.player.bet += 10
                        else :
                            self.player.bet = self.player.money
                    
                    if self.boutonDiminuerMise.estClique(pygame.mouse.get_pos()):
                        if self.player.bet >= 10:
                            self.player.bet -= 10
                        else :
                            self.player.bet = 0

                    if self.boutonDoublerMise.estClique(pygame.mouse.get_pos()):
                        if self.player.money >= self.player.bet * 2:
                            self.player.bet *= 2
                        else :
                            self.player.bet = self.player.money

                    if self.boutonDiviserMise.estClique(pygame.mouse.get_pos()):
                        self.player.bet = round(self.player.bet /2)
                        if self.player.bet < 10:
                            if self.player.money < 10:
                                self.player.bet = self.player.money
                            else:
                                self.player.bet = 10
                    
            self.screen.fill(BACKGROUND_COLOR)
            self.dessinerMonaie()
            if not self.gameStarted :
                self.boutonCecommencer.dessiner(self.screen)

            if self.gameStarted:
                self.boutonTirer.dessiner(self.screen)
                self.boutonRester.dessiner(self.screen)

            if self.gameStarted and self.canDouble:
                self.boutonDoubler.dessiner(self.screen)

            if not self.gameStarted:
                self.boutonAugmenterMise.dessiner(self.screen)
                self.boutonDiminuerMise.dessiner(self.screen)
                self.boutonDoublerMise.dessinerPetit(self.screen)
                self.boutonDiviserMise.dessinerPetit(self.screen)

            self.player.dessiner(self.screen, HAUTEUR - CARTE_HAUTEUR - 15)
            self.dealer.dessiner(self.screen, 15)
            if self.message:
                self.afficherMessage(self.screen, self.message)
                self.boutonRecommencer.dessiner(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

game = Game()
game.play()