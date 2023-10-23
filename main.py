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
    
class Icone :
    def __init__(self, x, y, l, h, text, textCouleur, couleur) -> None:
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.text = text
        self.textCouleur = textCouleur
        self.couleur = couleur

    def dessiner(self, screen):
        pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.l, self.h))
        font = pygame.font.SysFont(None, 36)
        textSurface = font.render(self.text, 1, self.textCouleur)
        textRectangle = textSurface.get_rect(center = (self.x + self.l / 2, self.y + self.h / 2))
        screen.blit(textSurface, textRectangle)
        
class Card :
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
        self.dealSound = pygame.mixer.Sound("sounds/deal.mp3")

    def shuffle(self) -> None:
        random.shuffle(self.cards)
    
    def addCuttingCard(self):
        indexMilieu = round(len(self.cards) // 2)
        self.cards.insert(indexMilieu, Card("R", 0))

    def deal(self) :
        if len(self.cards) != 0:
            card = self.cards.pop()

            self.dealSound.play()
            
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
        self.bet = [50, 0]
        self.hasSplit = False
        self.hasDouble = False
        self.hand2 = Hand()
        self.mainGagne = 0
        self.mainPerdu = 0

    def dessiner(self, screen, xOffset, y, hand):
        for card in hand.cards:
            imageToDraw = card.image if card.faceUp else card.backImage
            screen.blit(imageToDraw, (xOffset, y))
            xOffset += 20

    def retournerCarte(self, index):
        if index < len(self.hand.cards):
            self.hand.cards[index].flip()
        
    def hit(self, hand, deck):
        card = deck.deal()
        hand.addCard(card)

    def isBusted(self, hand):
        return hand.calculerTotal() > 21

class Dealer(Player):
    pass

class Game :
    def __init__(self) -> None:
        self.afficherBoutonAssurance = False
        self.assurence = False

        self.canDouble = False
        self.canDoubleHand2 = False
        
        self.premiereMainTermine = False
        
        self.canSplit = False

        self.gameStarted = False

        self.player = Player()

        self.dealer = Dealer()

        self.deck = Deck()
        self.deck.shuffle()
        self.deck.addCuttingCard()

        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

        pygame.display.set_caption("Blackjack")
        
        self.clock = pygame.time.Clock()

        self.message = ""

        self.boutonTirer = Bouton(LARGEUR - 200, HAUTEUR / 2, 150, 50, "Tirer", BLACK, BLANC, ROUGE)
        self.boutonRecommencer = Bouton(0, HAUTEUR / 2, 300, 50, "Recommencer", BLACK, BLANC, ROUGE)
        self.boutonCommencer = Bouton(0, HAUTEUR / 2, 300, 50, "Commencer", BLACK, BLANC, ROUGE)
        self.boutonRester = Bouton(LARGEUR - 200, HAUTEUR / 2 - 70, 150, 50, "Rester", BLACK, BLANC, ROUGE)
        self.boutonDoubler = Bouton(LARGEUR - 200, HAUTEUR / 2 + 70, 150, 50, "Doubler", BLACK, BLANC, ROUGE)
        self.boutonSplit = Bouton(LARGEUR - 200, HAUTEUR / 2 + 140, 150, 50, "Split", BLACK, BLANC, ROUGE)
        self.boutonAugmenterMise = Bouton(170, HAUTEUR - 95, 30, 30, "+", BLACK, BLANC, ROUGE)
        self.boutonDiminuerMise = Bouton(230, HAUTEUR - 95, 30, 30, "-", BLACK, BLANC, ROUGE)
        self.boutonDoublerMise = Bouton(170, HAUTEUR - 55, 30, 30, "x2", BLACK, BLANC, ROUGE)
        self.boutonDiviserMise = Bouton(230, HAUTEUR - 55, 30, 30, "/2", BLACK, BLANC, ROUGE)
        self.boutonAssurance = Bouton(LARGEUR-200, HAUTEUR/2 - 250, 150, 30, "Assurance", BLACK, BLANC, ROUGE)
        self.boutonPasAssurance = Bouton(LARGEUR-200, HAUTEUR/2 - 200, 200, 30, "Pas d'assurance", BLACK, BLANC, ROUGE)

        self.iconeAssurance = Icone(LARGEUR-200, HAUTEUR/2 - 250, 150, 30, "Assurance", BLACK, ROUGE)

        self.winSound = pygame.mixer.Sound("sounds/win.mp3")
        self.looseSound = pygame.mixer.Sound("sounds/loose.mp3")
        self.rienNeVasPlusSound = pygame.mixer.SoundType("sounds/rienNeVasPlus.mp3")
        
    def reset(self):
        self.gameStarted = True
        if self.deck.cuttingCardDraw:
            self.deck = Deck()
            self.deck.shuffle()
            self.deck.addCuttingCard()
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        self.player.hand2 = Hand()
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

        textSurfaceMise = font.render("Mise : "+ str(round(self.player.bet[0] + self.player.bet[1])), 1, BLACK)
        textMiseRect = textSurfaceMise.get_rect(topleft=(10, HAUTEUR - 90))
        self.screen.blit(textSurfaceMise, textMiseRect)

    def perdre(self):
        self.message = "Perdu !"
        self.gameStarted = False
        self.looseSound.play()

    def gagner(self):
        self.message = "Gagné !"
        self.player.money += 2*self.player.bet[0]
        self.gameStarted = False
        self.winSound.play()

    def egalite(self):
        self.message = "Egalité"
        self.player.money += self.player.bet[0]
        self.gameStarted = False
        self.winSound.play()

    def perdreAvecAssurance(self):
        self.message = "Perdu !"
        self.player.money += 1.5 * self.player.bet[0]
        self.gameStarted = False
        self.winSound.play()

    def comparerMains(self):
        self.dealer.retournerCarte(0)
        while self.dealer.hand.calculerTotal() < 17 :
            self.dealer.hit(self.dealer.hand, self.deck)
        if self.dealer.hand.hasBlackjack() :
            if self.assurence:
                self.perdreAvecAssurance()
            else:
                self.perdre()
        if self.player.hasSplit:
            for bet, hand in zip(self.player.bet, [self.player.hand, self.player.hand2]):
                if self.dealer.hand.calculerTotal() <= 21 and hand.calculerTotal() < self.dealer.hand.calculerTotal():
                    self.player.mainPerdu += 1
                elif self.dealer.hand.calculerTotal() > 21 or (self.dealer.hand.calculerTotal() < hand.calculerTotal()) and not self.player.isBusted(hand):
                    self.player.money += 2*bet
                    self.player.mainGagne += 1
                else:
                    self.player.money += bet
            if self.player.mainGagne > self.player.mainPerdu:
                self.message = "Gagné !"
                self.gameStarted = False
                self.winSound.play()
            elif self.player.mainGagne < self.player.mainPerdu:
                self.message = "Perdu !"
                self.gameStarted = False
                self.looseSound.play()
            else:
                self.message = "Egalité"
                self.gameStarted = False
                self.winSound.play()
        
        else:
            if self.dealer.hand.calculerTotal() <= 21 and self.player.hand.calculerTotal() < self.dealer.hand.calculerTotal():
                self.perdre()
            elif self.dealer.hand.calculerTotal() > 21 or (self.dealer.hand.calculerTotal() < self.player.hand.calculerTotal()):
                self.gagner()
            else:
                self.egalite()

        if self.player.hasDouble:
            self.player.bet[0] /= 2

        self.player.bet[1] = 0

    def start(self):
        
        self.gameStarted = True
        self.assurence = False
        self.canSplit = False
        self.player.bet[1] = 0

        self.player.mainGagne = 0
        self.player.mainPerdu = 0

        self.player.hasDouble = False
        self.player.hasSplit = False
        
        self.premiereMainTermine = False
        
        self.player.hasSplit = False

        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())
        self.player.hand.addCard(self.deck.deal())
        self.dealer.hand.addCard(self.deck.deal())

        self.player.money -= self.player.bet[0]
        
        if self.player.money >= self.player.bet[0]:
            self.canDouble = True

        self.deck.dealSound.set_volume(1)

        if self.player.hand.hasBlackjack() and self.dealer.hand.hasBlackjack():
            self.egalite()
            self.winSound.play()
        elif self.player.hand.hasBlackjack():
            self.message = "BlackJack"  
            self.winSound.play()
            self.player.money += self.player.bet[0] * 2.5
            self.gameStarted = False
        elif self.dealer.hand.hasBlackjack():
            if self.dealer.hand.cards[1].value == 1:
                self.afficherBoutonAssurance = True
                self.dealer.retournerCarte(0)
            else :
                self.perdre()
        else:
            self.dealer.retournerCarte(0)

        if self.dealer.hand.cards[1].value == 1:
            self.afficherBoutonAssurance = True
            
        if self.player.hand.cards[0].value == self.player.hand.cards[1].value or (self.player.hand.cards[0].value >= 10 and self.player.hand.cards[1].value >= 10):
            self.canSplit = True

        return

    def play(self):
    
        running = True

        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    if self.boutonSplit.estClique(pygame.mouse.get_pos()) and self.canSplit and not self.afficherBoutonAssurance:
                        self.player.money -= self.player.bet[0]
                        self.player.bet[1] = self.player.bet[0]
                        self.player.hasSplit = True
                        self.canSplit = False
                        self.player.hand2.addCard(self.player.hand.cards.pop(1))
                        self.player.hand.addCard(self.deck.deal())
                        self.player.hand2.addCard(self.deck.deal())
                        
                    if self.boutonTirer.estClique(pygame.mouse.get_pos()) and not self.message and not self.afficherBoutonAssurance:
                        self.canDouble = False
                        self.canSplit = False
                        if not self.premiereMainTermine:
                            self.player.hit(self.player.hand, self.deck)
                            if self.player.isBusted(self.player.hand):
                                self.looseSound.play()
                                if self.player.hasSplit:
                                    self.premiereMainTermine = True
                                else:
                                    self.message = "Bust"
                            elif self.player.hand.calculerTotal() == 21:
                                if self.player.hasSplit:
                                    self.premiereMainTermine = True
                                else:
                                    self.comparerMains()
                        elif self.premiereMainTermine == True:
                            self.player.hit(self.player.hand2, self.deck)
                            if self.player.isBusted(self.player.hand2):
                                self.looseSound.play()
                                self.comparerMains()

                    if self.boutonAssurance.estClique(pygame.mouse.get_pos()):
                        self.assurence = True
                        self.afficherBoutonAssurance = False
                        self.player.money -= self.player.bet[0] / 2
                    elif self.boutonPasAssurance.estClique(pygame.mouse.get_pos()):
                        self.afficherBoutonAssurance = False

                    if not self.message and self.boutonCommencer.estClique(pygame.mouse.get_pos()) and not self.gameStarted:
                        self.start()

                    if self.boutonRester.estClique(pygame.mouse.get_pos()) and not self.message and not self.afficherBoutonAssurance:
                        self.afficherBoutonAssurance = False
                        if not self.player.hasSplit or self.premiereMainTermine == True:
                            self.comparerMains()
                        else:
                            self.premiereMainTermine = True

                    if self.boutonDoubler.estClique(pygame.mouse.get_pos()) and not self.player.hand.calculerTotal() >= 21 and not self.message and self.canDouble and not self.afficherBoutonAssurance:
                        self.player.money -= self.player.bet[0]
                        self.player.bet[0] *= 2
                        self.player.hit(self.player.hand, self.deck)
                        self.player.hasDouble = True
                        if self.player.isBusted(self.player.hand):
                            self.message = "Bust !"
                            self.looseSound.play()
                            self.gameStarted = False
                        elif not self.player.hasSplit: 
                            self.comparerMains()
                        else:
                            self.premiereMainTermine = True
    
                    if self.message and self.boutonRecommencer.estClique(pygame.mouse.get_pos()) and self.player.money > 0 and self.player.money >= self.player.bet[0]:
                        self.reset()
                        self.start()
                    
                    if not self.gameStarted:
                        if self.boutonAugmenterMise.estClique(pygame.mouse.get_pos()):
                            if self.player.money >= self.player.bet[0] + 10:
                                self.player.bet[0] += 10
                            else :
                                self.player.bet[0] = self.player.money
                        if self.boutonDiminuerMise.estClique(pygame.mouse.get_pos()):
                            if self.player.bet[0] >= 10:
                                self.player.bet[0] -= 10
                            else :
                                self.player.bet[0] = 0
                        if self.boutonDoublerMise.estClique(pygame.mouse.get_pos()):
                            if self.player.money >= self.player.bet[0] * 2:
                                self.player.bet[0] *= 2
                            else :
                                self.player.bet[0] = self.player.money
                        if self.boutonDiviserMise.estClique(pygame.mouse.get_pos()):
                            self.player.bet[0] = round(self.player.bet[0] /2)
                            if self.player.bet[0] < 10:
                                if self.player.money < 10:
                                    self.player.bet[0] = self.player.money
                                else:
                                    self.player.bet[0] = 10
                    
            self.screen.fill(BACKGROUND_COLOR)

            if self.afficherBoutonAssurance:
                self.boutonAssurance.dessinerPetit(self.screen)
                self.boutonPasAssurance.dessinerPetit(self.screen)

            self.dessinerMonaie()

            if not self.gameStarted :
                self.boutonCommencer.dessiner(self.screen)

            if self.gameStarted:
                self.boutonTirer.dessiner(self.screen)
                self.boutonRester.dessiner(self.screen)
                if self.canDouble:
                    self.boutonDoubler.dessiner(self.screen)
                if self.canSplit:
                    self.boutonSplit.dessiner(self.screen)
                
            if not self.gameStarted:
                self.boutonAugmenterMise.dessiner(self.screen)
                self.boutonDiminuerMise.dessiner(self.screen)
                self.boutonDoublerMise.dessinerPetit(self.screen)
                self.boutonDiviserMise.dessinerPetit(self.screen)

            self.dealer.dessiner(self.screen, (LARGEUR - CARTE_LARGEUR - 15) // 2, 15, self.dealer.hand)
        
            if self.message:
                self.afficherMessage(self.screen, self.message)
                self.boutonRecommencer.dessiner(self.screen)
                
            if not self.player.hasSplit:
                self.player.dessiner(self.screen, (LARGEUR - CARTE_LARGEUR - 15) // 2, HAUTEUR - CARTE_HAUTEUR - 15, self.player.hand)
            elif self.player.hasSplit:
                self.player.dessiner(self.screen, (LARGEUR - CARTE_LARGEUR - 15) // 3 * 2, HAUTEUR - CARTE_HAUTEUR - 15, self.player.hand)
                self.player.dessiner(self.screen, (LARGEUR - CARTE_LARGEUR - 15) // 3, HAUTEUR - CARTE_HAUTEUR - 15, self.player.hand2)
                    
                    
            pygame.display.flip()
            self.clock.tick(60)

game = Game()
game.play()