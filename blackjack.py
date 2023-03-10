import random
import string
import os
import time

suits = ('Diamonds', 'Spades', 'Hearts', 'Clubs')
ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'J', 'K')

card_value = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
              '7': 7, '8': 8, '9': 9, '10': 10, 'Q': 10, 'J': 10, 'K': 10}

min_bet = 5
max_bet = 500
chip_amount = 500


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + self.rank

    def draw(self):
        print(self.rank + ' ' + self.suit)


class Hand():
    def __init__(self):
        self.cards = []
        self.hasAce = False
        self.hasInsurance = False
        self.value = 0

    def card_add(self, card):
        self.cards.append(card)
        if card.rank == 'A':
            self.hasAce = True

        self.value += card_value[card.rank]

    def calc_value(self, hidden=False):
        if hidden == False:
            if (self.hasAce == True and self.value <= 11):
                self.value += 10

            return self.value

        else:
            return self.value - card_value[self.cards[0].rank]

    def take_insurance(self):
        insurance = input(
            "\nThe dealer has an Ace. Woud you like to take insurance, 'Y' or 'N'?\n").lower()
        while insurance != 'y' and insurance != 'n':
            insurance = input(
                "\nPlease enter a valid input, 'Y' or 'N': \n").lower()

        if insurance == 'y':
            self.hasInsurance = True

    def draw(self, hidden=False):
        if hidden == True:
            starting_card = 1

        else:
            starting_card = 0

        for card in range(starting_card, len(self.cards)):
            self.cards[card].draw()

    def clear(self):
        self.cards = []
        self.hasAce = False
        self.value = 0


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def get_card(self):
        return self.deck.pop()


def make_bet():
    global playing, bet, min_bet, max_bet, chip_amount
    bet = 0

    os.system('clear')
    print("How much do you want to bet? \nThe minimum bet is {} chips and the maximum bet is {} chips. \nYou currently have {} chips".format(
        min_bet, max_bet, chip_amount))

    while bet == 0:
        input_bet = input("\nEnter bet: ")
        while True:
            flag = True
            try:
                int(input_bet)

            except ValueError:
                flag = False

            if flag == True:
                input_bet = int(input_bet)
                break

            else:
                input_bet = input("\nPlease enter a valid bet: ")

        if input_bet <= chip_amount:
            if input_bet >= min_bet and input_bet <= max_bet:
                bet = input_bet

            elif input_bet < min_bet:
                print(
                    "The minimum bet is {} chips. Please enter anoter bet".format(min_bet))

            else:
                print(
                    "The maximum bet is {} chips. Please enter anoter bet".format(max_bet))

        else:
            print("Your total amount of chips is {}".format(chip_amount))


def game_start():
    global playing, result, deck, player_hand, dealer_hand, chip_amount, bet
    playing = True

    while playing:

        print("\nShuffle or leave? Press p to Shuffle or l to Leave")
        continue_playing()
        if chip_amount <= 0:
            print("\nNo chips left! Come back later\n")
            game_exit()

        else:
            print("\nYou got {} chips left\n".format(chip_amount))


def deal_cards():
    global playing, deck, player_hand, dealer_hand, deck, chip_amount, bet

    make_bet()
    deck = Deck()
    deck.shuffle()
    player_hand.clear()
    dealer_hand.clear()

    player_hand.card_add(deck.get_card())
    player_hand.card_add(deck.get_card())

    dealer_hand.card_add(deck.get_card())
    dealer_hand.card_add(deck.get_card())

    chip_amount -= bet
    hidden = True
    game_step()


def print_hands(hidden):
    os.system('clear')

    print("\nYour current hand is ")
    player_hand.draw(False)
    print("Your hand's value is {}".format(player_hand.calc_value(False)))

    print("\nThe dealer current hand is ")
    dealer_hand.draw(hidden)
    print("The dealer's hand's value is {}".format(
        dealer_hand.calc_value(hidden)))

    if dealer_hand.cards[1].rank == 'A':
        player_hand.take_insurance()


def game_step():
    global player_hand, dealer_hand
    print_hands(True)

    if check_blackjack():
        stand()

    else:
        print("\n(H)it or (S)tand?")
        player_input()


def hit():
    global deck, dealer_hand, player_hand, chip_amount, bet
    card = deck.get_card()
    player_hand.card_add(card)

    os.system('clear')
    print("\nYou drew ", end=' ')
    card.draw()

    if player_hand.calc_value() > 21:
        print("\nYou got {} and busted!".format(player_hand.calc_value()))
        chip_amount -= bet

    else:
        game_step()


def stand():
    global player_hand, dealer_hand, deck, chip_amount, bet

    os.system('clear')
    print_hands(False)
    time.sleep(2)

    while (dealer_hand.calc_value() <= 16):
        card = deck.get_card()
        dealer_hand.card_add(card)
        print("\nThe dealer got ", end='')
        card.draw()
        time.sleep(2)

    check_result()


def check_blackjack():
    global player_hand, dealer_hand, deck, bet, chip_amount
    if (player_hand.calc_value() == 21):
        print("\nCongratulations! You got a blackjack!")
        time.sleep(5)
        stand()
        return True

    else:
        return False


def check_result():
    global dealer_hand, player_hand, deck, bet, chip_amount
    if player_hand.calc_value() <= 21:
        if player_hand.calc_value() > dealer_hand.calc_value():
            print("\nYou got {} and dealer got {}. You won {} chips".format(
                player_hand.calc_value(), dealer_hand.calc_value(), bet))
            chip_amount += 2 * bet

        elif player_hand.calc_value() == dealer_hand.calc_value():
            print("\nDraw! You gained {} chips back".format(bet))
            chip_amount += bet

        else:
            if dealer_hand.calc_value() > 21:
                print(
                    "\nDealer got busted and you didn't. You won {} chips!".format(bet))
                chip_amount += 2 * bet

            else:
                print("\nDealer got {} and you got {}. You lost {} chips".format(
                    dealer_hand.calc_value(), player_hand.calc_value(), bet))
                if player_hand.hasInsurance and dealer_hand.calc_value() == 21:
                    print("\nYou had insurance and got {} chips back.\n".format(bet))
                    chip_amount += bet

    else:
        print("Busted! You got {} and lost {} chips".format(
            player_hand.calc_value(), bet))


def player_input():
    choice = input().lower()
    while choice != 'h' and choice != 's':
        print("Invalid input. Please enter h, s")
        choice = input().lower()

    if choice == 'h':
        hit()
    else:
        stand()


def continue_playing():
    choice = input().lower()
    while choice != 'p' and choice != 'l':
        print("Invalid input. Please enter p or l")
        choice = input().lower()

    if choice == 'p':
        deal_cards()

    else:
        game_exit()


def game_exit():
    global playing

    playing = False
    print("Thanks for playing")
    exit()


os.system('clear')
intro = "Welcome to Blackjack!\n \nEach round you and the dealer will get 2 initial cards. The goal of the game is to score as close as possible of 21. If you \
      get a hand value higher than 21, you will get busted and lose your chips. You win if you get a score highter than the dealer or if the dealer get busted. Each round, you can hit (get another card) or stand (wait for the dealer to his lasting cards)."

print(intro)
player_hand = Hand()
dealer_hand = Hand()
game_start()
