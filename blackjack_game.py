# -*- coding: utf-8 -*-
"""
The goal of this notebook is to create a blackjack game
with the following attributes: 
(1) The game needs to have one player versus an automated dealer. 
(2) The player can stand or hit. 
(3) The player must be able to pick their betting amount. 
(4) The program needs to keep track fo the players total money. 
(5) The program needs to alert the player of wins,losses, or busts, etc..
"""

import random

def ask_num_decks():
    """ Asks for the number of decks player wants to play with."""
    while True:
        numdecks = raw_input('How many decks would you like to play with? (enter an int): ')
        try:
            numdecks = int(numdecks)
            break
        except ValueError:
            print 'Not an integer number of decks.'
    return numdecks

def get_bet_amount(player):
    """ Ask for bet amount for a hand"""
    while True:
        bet_amount = raw_input('How much would you like to bet? (enter an int): ')
        try:
            bet_amount = int(bet_amount)
            if bet_amount > player.total_money:
                print "You don't have that much money!"
                continue
            else:
                print "Ok, let's start!"
                break
        except ValueError:
            print 'Not an integer bet amount.'
    return bet_amount    

def sum_card_values(hand):
    """ Calculates the sum of the cards in the dealer & players hands."""
    handsum = 0
    numaces = 0
    for rank, suit in hand:
        if rank == 'Jack' or rank == 'Queen' or rank == 'King':
            rank = 10
        elif rank == 'Ace':
            rank = 1
            numaces +=1
        handsum += rank
    
    num = 0
    while num <= numaces:
        if handsum + 10*num <= 21:
            handsum = handsum + 10*num
        num +=1
    
    return handsum

class Deck(object):
    """ Creates deck for blackjack game.
    The default number of decks to use is 1,
    change by using the numdecks attribute."""
    
    suits = ['Heart', 'Spade', 'Club', 'Diamond']
    ranks = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
    
    def __init__(self, numdecks = 1):
        self.numdecks = numdecks
        suitlist = []
        for suit in Deck.suits:
            for j in range(13):
                suitlist.append(suit)
        deck = zip(Deck.ranks*4, suitlist)
        
        self.deck = deck * numdecks
    
    def shuffle(self):
        return random.shuffle(self.deck)
    
    def deal(self, num_cards):
        return self.deck[:num_cards], self.deck[num_cards:]

class Player(object):
    """Initializes a player with a hand and an amount of money to spend.
    hand default = [], money default = 100"""
    
    def __init__(self, name, hand = [], total_money = 100):
        self.name = name
        self.hand = hand
        self.total_money = total_money
    
    def changeMoney(self, bet_amount):
        self.total_money += bet_amount
        no_money = False
        if self.total_money <= 0:
            no_money = True
        return self.total_money, no_money
    
    def ask_for_hit(self):
        while True:
            hit = raw_input('%s, your cards sum to %d, would you like to hit? (Y/N): ' %(self.name, sum_card_values(self.hand)))
            if hit.lower() == 'y':
                return True
                break
            elif hit.lower() == 'n':
                return False
                break
            else:
                print 'Invalid entry.'

class Dealer(object):
    """Dealer initialized with empty hand"""
    def __init__(self, hand = []):
        self.hand = hand
    
    def do_I_hit(self, hand):
        if sum_card_values(self.hand) < 17:
            return True
        else:
            return False

def initialize_game():
    # Get player name
    playername = raw_input('Please enter your player name: ')
    player = Player(playername)
    print "%s, you have %d dollars to spend." %(player.name, player.total_money)
    
    # Ask number of decks to play with
    numdecks = ask_num_decks()
    
    # Initialize dealer
    dealer = Dealer()
    
    return player, dealer, numdecks

def first_deal(player, dealer, deck):
    player.hand, deck.deck = deck.deal(2) # deal cards to player
    print '{0}, your hand is: {1}'.format(player.name, player.hand)
    
    dealer.hand, deck.deck = deck.deal(2) # deal cards to dealer, only the top one is revealed
    print "The dealer's top card is: ", dealer.hand[0]
    
    return player, dealer, deck

def hit(hit_bool, deck):
    '''Returns the new card to be appended to the player hand
    and the new deck with that card removed if hit_bool == True,
    else returns an empty tuple and the same deck.'''
    if hit_bool == True:
        newcard, deck.deck = deck.deal(1)
        return newcard[0], deck.deck #returns new card to be appended to player's hand
                                    # and new deck with card removed.
    else:
        return (0,0), deck.deck

def who_won(player, dealer):
    '''Determines if the player or dealer has won after both player and dealer do not hit.
    returns True if player wins, False if dealer wins.'''
    
    player_hand_sum = sum_card_values(player.hand)
    dealer_hand_sum = sum_card_values(dealer.hand)
    
    if player_hand_sum > dealer_hand_sum and player_hand_sum <= 21:
        print 'Congratulations, %s, you won!' %player.name
        return True
    elif player_hand_sum == dealer_hand_sum:
        print 'Tie!'
        return None
    elif player_hand_sum > 21 and dealer_hand_sum > 21:
        print 'Tie!'
        return None
    elif player_hand_sum <= 21 and dealer_hand_sum > 21:
        print 'Congratulations, %s, you won!' %player.name
        return True
    else:
        print 'Sorry, %s, the dealer beat you.' %player.name
        return False

def play_hand(player, dealer, deck, betamount):
    """Function to run through one hand of blackjack.
    Returns boolean True/False in response to 'play another hand?' """
    
    playerbool = True
    dealerbool = True
    
    while playerbool == True:
        
        playerbool = player.ask_for_hit()
        newcard, deck.deck = hit(playerbool, deck)
        player.hand.append(newcard)
        if newcard == (0,0):
            player.hand.remove(newcard)
        print ""
        print "{0}, your hand is: {1}".format(player.name, player.hand)
        if sum_card_values(player.hand) > 21:
            print 'The value of your cards exceeds 21.'
            break
    
    print 'Thank you. Now the dealer will resolve their hand.'
    print '-------------------------------------------------'
    
    if sum_card_values(player.hand) > 21:
        dealerbool = False
    while dealerbool == True:
        dealerbool = dealer.do_I_hit(dealer.hand)
        newdealercard, deck.deck = hit(dealerbool, deck)
        
        # print 'The dealer hand sums to: ', sum_card_values(dealer.hand)
        dealer.hand.append(newdealercard)
        
        if newdealercard == (0,0):
            dealer.hand.remove(newdealercard)
            
        if dealerbool == True:
            print ""
            print "The dealer chose to hit."
            print "The Dealer's new card is: ", newdealercard
            if sum_card_values(dealer.hand) > 21:
                print 'The value of the dealer cards exceeds 21.'
                break
        else:
            print "The dealer chose to stay."

    
    print "The dealer's hand is: ", dealer.hand
    
    did_player_win = who_won(player, dealer)
    
    print '-------------------------------------------------'
    
    if did_player_win == True:
        player.total_money, gameoverbool = player.changeMoney(betamount)
        print "{0}, you now have {1} dollars.".format(player.name, player.total_money)
        while True:
            play_again = raw_input("Would you like to play another hand? (y/n): ")
            if play_again.lower() == 'y':
                return True
                break
            elif play_again.lower() == 'n':
                return False
                break
            else:
                print 'Invalid entry.'
                
    elif did_player_win == False:
        player.total_money, gameoverbool = player.changeMoney(-betamount)
        print "{0}, you now have {1} dollars.".format(player.name, player.total_money)
        if gameoverbool == True:
            print "You have no more money to play with. See you next time!"
            return False
        if gameoverbool == False:
            while True:
                play_again = raw_input("Would you like to play another hand? (y/n): ")
                if play_again.lower() == 'y':
                    return True
                    break
                elif play_again.lower() == 'n':
                    return False
                    break
                else:
                    print 'Invalid entry.'
        
    else:
        print "{0}, you still have {1} dollars.".format(player.name, player.total_money)
        while True:
            play_again = raw_input("Would you like to play another hand? (y/n): ")
            if play_again.lower() == 'y':
                return True
                break
            elif play_again.lower() == 'n':
                return False
                break
            else:
                print 'Invalid entry.'

def play_game():    
    player, dealer, numdecks = initialize_game() # initialize player and game
    
    play_again = True
    
    while play_again == True:
        betamount = get_bet_amount(player)
        deck = Deck(numdecks)
        deck.shuffle()
        
        player, dealer, deck = first_deal(player, dealer, deck) # Give initial cards
        
        play_again = play_hand(player, dealer, deck, betamount)
        
    print 'Thanks for playing!'
    
play_game()