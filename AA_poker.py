API_key= "5376534440:AAEmLbsKTC6gK5cMdGraHURrg8a26qqkNps"

import telebot
from telebot import types
import random

bot = telebot.TeleBot(API_key)
d=[""]
Lobby={}
players={}
@bot.message_handler(commands=["start"])
def handle_hi(message):
    bot.send_message(message.chat.id, "Do you want to host a game room or join?:", reply_markup=hostorjoin)

@bot.message_handler(commands=["host"])
def handle_host(message):
    bot.send_message(message.chat.id, "Type a 4 digit room ID:")
    d[0]="Hosting"


@bot.message_handler(commands=["join"])
def handle_join(message):
    bot.send_message(message.chat.id, "Type a 4 digit room ID:")
    d[0]="Joining"

@bot.message_handler()
def code(message):
    try:
        if d[0]=="Hosting":
            player1=player(message.chat.id,0)
            Lobby[message.text]=room(player1,message.text)
            players[message.chat.id]=player1
            player1.roomcode=message.text
            d[0]=""
        elif d[0]=="Joining":
            if message.text in Lobby:
                player2=player(message.chat.id,0)
                player2.roomcode=message.text
                Lobby[message.text].join(player2)
                players[message.chat.id]=player2
#player1_turn
        elif d[0]=="player1_turn":
            if message.chat.id!=Lobby[players[message.chat.id].roomcode].player1.id:
                bot.send_message(message.chat.id, "Not your turn")
            elif int(message.text)>10:
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "Can't bet more than 10 try again")
            elif message.text != "0":
                Lobby[players[message.chat.id].roomcode].game.bet=int(message.text)
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "Player1 bet $"+message.text+" press Y for accept N for no")
                d[0]="player2_YorN"
            elif message.text == "0":
                Lobby[players[message.chat.id].roomcode].player1.streak=0
                d[0]="player1_throw"
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,  "Type the index of the cards you want to throw, eg. 135, type 0 if you dont want to change")
#player2_turn
        elif d[0]=="player2_turn":
            if message.chat.id!=Lobby[players[message.chat.id].roomcode].player2.id:
                bot.send_message(message.chat.id, "Not your turn")
            elif int(message.text)>10:
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "Can't bet more than 10 try again")
            elif message.text != "0":
                Lobby[players[message.chat.id].roomcode].game.bet=int(message.text)
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "Player2 bet $"+message.text+" press Y for accept N for no")
                d[0]="player1_YorN"
            elif message.text == "0":
                Lobby[players[message.chat.id].roomcode].player2.streak=0
                d[0]="player2_throw"
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,  "Type the index of the cards you want to throw, eg. 135, type 0 if you dont want to change")
#player1_YorN
        elif d[0]=="player1_YorN":
            if message.chat.id!=Lobby[players[message.chat.id].roomcode].player1.id:
                bot.send_message(message.chat.id, "Not your turn")
            elif message.text.upper()=="Y":
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "This is your opponents hand "+str(Lobby[players[message.chat.id].roomcode].player2.hand)+"who won? type 1 or 2")
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "This is your opponents hand "+str(Lobby[players[message.chat.id].roomcode].player1.hand))
                d[0]="giving money"
            elif message.text.upper()=="N":
                d[0]="player2_throw"
                if Lobby[players[message.chat.id].roomcode].player2.streak == 4:
                    Lobby[players[message.chat.id].roomcode].game.bet/=2
                    Lobby[players[message.chat.id].roomcode].player2.money+=Lobby[players[message.chat.id].roomcode].game.bet
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "You won $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at $"+str(Lobby[players[message.chat.id].roomcode].player2.money))
                    Lobby[players[message.chat.id].roomcode].player1.money-=Lobby[players[message.chat.id].roomcode].game.bet
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "You lost $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at $"+str(Lobby[players[message.chat.id].roomcode].player1.money))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "new game? Y or N")
                    d[0]="new_game?"
                else:
                    Lobby[players[message.chat.id].roomcode].player2.streak+=1
                    Lobby[players[message.chat.id].roomcode].player1.streak=0
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "Player 1 declined your bet,your streak is at "+str(Lobby[players[message.chat.id].roomcode].player2.streak)+", type the index of the cards you want to throw")    
#player2_YorN
        elif d[0]=="player2_YorN":
            if message.chat.id!=Lobby[players[message.chat.id].roomcode].player2.id:
                bot.send_message(message.chat.id, "Not your turn")
            elif message.text.upper()=="Y":
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "This is your opponents hand "+str(Lobby[players[message.chat.id].roomcode].player2.hand)+"who won? type 1 or 2")
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "This is your opponents hand "+str(Lobby[players[message.chat.id].roomcode].player1.hand))
                d[0]="giving money"
            elif message.text.upper()=="N":
                d[0]="player1_throw"
                if Lobby[players[message.chat.id].roomcode].player1.streak == 4:
                    Lobby[players[message.chat.id].roomcode].game.bet/=2
                    Lobby[players[message.chat.id].roomcode].player1.money+=Lobby[players[message.chat.id].roomcode].game.bet
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "You won $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at"+str(Lobby[players[message.chat.id].roomcode].player1.money))
                    Lobby[players[message.chat.id].roomcode].player2.money-=Lobby[players[message.chat.id].roomcode].game.bet
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "You lost $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at"+str(Lobby[players[message.chat.id].roomcode].player2.money))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "new game? Y or N")
                    d[0]="new_game?"
                else:
                    Lobby[players[message.chat.id].roomcode].player1.streak+=1
                    Lobby[players[message.chat.id].roomcode].player2.streak=0
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "Player 2 declined your bet,your streak is at "+str(Lobby[players[message.chat.id].roomcode].player1.streak)+", type the index of the cards you want to throw")
#player1_throw
        elif d[0]=="player1_throw":
            if message.chat.id!=Lobby[players[message.chat.id].roomcode].player1.id:
                bot.send_message(message.chat.id, "Not your turn")
            elif message.text=="0":
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,"opponent no change")
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,str(Lobby[players[message.chat.id].roomcode].player1.hand))
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "type the amount of $ you want to challenge")
                d[0]="player2_turn"
            else:
                text=players[message.chat.id].replace(Lobby[players[message.chat.id].roomcode].game.deck,message.text)
                if Lobby[players[message.chat.id].roomcode].game.deck.is_empty():
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,"opponent threw away "+str(text))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,"the deck is empty, how much would you like to bet?")
                    d[0]="player_1_end_bet"
                if text==None:
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,"the deck is left with "+len(Lobby[players[message.chat.id].roomcode].game.deck.deck)+" cards left, try again")
                else:
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,"opponent threw away "+str(text))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,str(Lobby[players[message.chat.id].roomcode].player1.hand))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "type the amount of $ you want to challenge")
                    d[0]="player2_turn"
#player2_throw
        elif d[0]=="player2_throw":
            if message.chat.id!=Lobby[players[message.chat.id].roomcode].player2.id:
                bot.send_message(message.chat.id, "Not your turn")
            elif message.text=="0":
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,"opponent no change")
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,str(Lobby[players[message.chat.id].roomcode].player2.hand))
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "type the amount of $ you want to challenge")
                d[0]="player1_turn"
            else:
                text=players[message.chat.id].replace(Lobby[players[message.chat.id].roomcode].game.deck,message.text)
                if Lobby[players[message.chat.id].roomcode].game.deck.is_empty():
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,"opponent threw away "+str(text))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,"the deck is empty, how much would you like to bet?")
                    d[0]="player_1_end_bet"
                if text==None:
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,"the deck is left with "+len(Lobby[players[message.chat.id].roomcode].game.deck.deck)+" cards left, try again")
                else:
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id,"opponent threw away "+str(text))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id,str(Lobby[players[message.chat.id].roomcode].player2.hand))
                    bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "type the amount of $ you want to challenge")
                    d[0]="player1_turn"
#giving_money
        elif d[0]=="giving money":
            if message.text=="1":
                Lobby[players[message.chat.id].roomcode].player1.money+=Lobby[players[message.chat.id].roomcode].game.bet
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "You won $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at $"+str(Lobby[players[message.chat.id].roomcode].player1.money))
                Lobby[players[message.chat.id].roomcode].player2.money-=Lobby[players[message.chat.id].roomcode].game.bet
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "You lost $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at $"+str(Lobby[players[message.chat.id].roomcode].player2.money))
            if message.text=="2":
                Lobby[players[message.chat.id].roomcode].player2.money+=Lobby[players[message.chat.id].roomcode].game.bet
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "You won $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at $"+str(Lobby[players[message.chat.id].roomcode].player2.money))
                Lobby[players[message.chat.id].roomcode].player1.money-=Lobby[players[message.chat.id].roomcode].game.bet
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "You lost $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at $"+str(Lobby[players[message.chat.id].roomcode].player1.money))
            bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "new game? Y or N")
            d[0]="new_game?"
#new_game?
        elif d[0]=="new_game?":
            if message.text.upper()=="Y":
                Lobby[players[message.chat.id].roomcode].player1.reset()
                Lobby[players[message.chat.id].roomcode].player2.reset()
                Lobby[players[message.chat.id].roomcode].game=game(Lobby[players[message.chat.id].roomcode].player1,Lobby[players[message.chat.id].roomcode].player2)
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, str(Lobby[players[message.chat.id].roomcode].player2.hand))
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, str(Lobby[players[message.chat.id].roomcode].player1.hand))
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "You start first, type the amount of $ you want to challenge")
                d[0]="player1_turn"
            elif message.text.upper()=="N":
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "The game have ended, you are at $"+str(Lobby[players[message.chat.id].roomcode].player1.money))
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "The game have ended, you are at $"+str(Lobby[players[message.chat.id].roomcode].player2.money))
                Lobby[players[message.chat.id].roomcode].player1.reset()
                Lobby[players[message.chat.id].roomcode].player2.reset()
#player_1_end_bet
        elif d[0]=="player_1_end_bet":
            Lobby[players[message.chat.id].roomcode].game.bet=int(message.text)
            bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "The deck is empty, your opponent bet $"+message.text,"would you like to take the bet press Y, pay half of the bet press N or bet even more?, type your bet")
            d[0]=="player2_YNorbet"
#player2_YNorbet
        elif d[0]=="player2_YNorbet":
            if message.text.upper()=="Y":
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "This is your opponents hand "+str(Lobby[players[message.chat.id].roomcode].player2.hand)+"who won? type 1 or 2")
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "This is your opponents hand "+str(Lobby[players[message.chat.id].roomcode].player1.hand))
                d[0]="giving money"
            elif message.text.upper()=="N":
                Lobby[players[message.chat.id].roomcode].game.bet/=2
                Lobby[players[message.chat.id].roomcode].player1.money+=Lobby[players[message.chat.id].roomcode].game.bet
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "You won $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at"+str(Lobby[players[message.chat.id].roomcode].player1.money))
                Lobby[players[message.chat.id].roomcode].player2.money-=Lobby[players[message.chat.id].roomcode].game.bet
                bot.send_message(Lobby[players[message.chat.id].roomcode].player2.id, "You lost $"+str(Lobby[players[message.chat.id].roomcode].game.bet)+", you are now at"+str(Lobby[players[message.chat.id].roomcode].player2.money))
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "new game? Y or N")
                d[0]="new_game?"
            elif int(message.text)>Lobby[players[message.chat.id].roomcode].game.bet:
                bot.send_message(Lobby[players[message.chat.id].roomcode].player1.id, "The deck is empty, your opponent bet more at $"+message.text+"press Y to accept, N to lose half")
                Lobby[players[message.chat.id].roomcode].player2.streak=4
                d[0]="player1YorN"
        else:
            bot.send_message(message.chat.id,"Try again, type properlyy")
    except:
        bot.send_message(message.chat.id,"Try again, type properly")
    
            
            

###Deck class###
class deck:
    def __init__(self):
        self.fulldeck=[{"value": "2", "suit": "♣"}, {"value": "2", "suit": "♦"}, {"value": "2", "suit": "♥"}, {"value": "2", "suit": "♠"}, {"value": "3", "suit": "♣"}, {"value": "3", "suit": "♦"}, {"value": "3", "suit": "♥"}, {"value": "3", "suit": "♠"}, {"value": "4", "suit": "♣"}, {"value": "4", "suit": "♦"}, {"value": "4", "suit": "♥"}, {"value": "4", "suit": "♠"}, {"value": "5", "suit": "♣"}, {"value": "5", "suit": "♦"}, {"value": "5", "suit": "♥"}, {"value": "5", "suit": "♠"}, {"value": "6", "suit": "♣"}, {"value": "6", "suit": "♦"}, {"value": "6", "suit": "♥"}, {"value": "6", "suit": "♠"}, {"value": "7", "suit": "♣"}, {"value": "7", "suit": "♦"}, {"value": "7", "suit": "♥"}, {"value": "7", "suit": "♠"}, {"value": "8", "suit": "♣"}, {"value": "8", "suit": "♦"}, {
    "value": "8", "suit": "♥"}, {"value": "8", "suit": "♠"}, {"value": "9", "suit": "♣"}, {"value": "9", "suit": "♦"}, {"value": "9", "suit": "♥"}, {"value": "9", "suit": "♠"}, {"value": "T", "suit": "♣"}, {"value": "T", "suit": "♦"}, {"value": "T", "suit": "♥"}, {"value": "T", "suit": "♠"}, {"value": "J", "suit": "♣"}, {"value": "J", "suit": "♦"}, {"value": "J", "suit": "♥"}, {"value": "J", "suit": "♠"}, {"value": "Q", "suit": "♣"}, {"value": "Q", "suit": "♦"}, {"value": "Q", "suit": "♥"}, {"value": "Q", "suit": "♠"}, {"value": "K", "suit": "♣"}, {"value": "K", "suit": "♦"}, {"value": "K", "suit": "♥"}, {"value": "K", "suit": "♠"}, {"value": "A", "suit": "♣"}, {"value": "A", "suit": "♦"}, {"value": "A", "suit": "♥"}, {"value": "A", "suit": "♠"}]
        self.deck=(list(range(52)))
        random.shuffle(self.deck)

    def shuffle(self):
        self.deck=(list(range(52)))
        random.shuffle(self.deck)

    def deal(self,num,player):
        cards=[]
        for i in range(num):
            if self.deck:
                num=self.deck.pop()
                string+=[self.fulldeck[num]["value"]+self.fulldeck[num]["suit"]]
        return cards
    def show_deck(self):
        deck=[]
        for i in range(len(self.deck)):
            if self.deck:
                num=self.deck[i]
                deck+=[self.fulldeck[num]["value"]+self.fulldeck[num]["suit"]]
        return deck
    def is_empty(self):
        return len(self.deck)==0
            

###Player class###
class player():
    def __init__(self,idd,money):
        self.id=idd
        self.money=money
        self.streak=0
        self.hand=[]
        self.roomcode=""
    def draw(self,deck,num):
        for i in range(num):
            if deck.deck:
                num=deck.deck.pop()
                self.hand+=[deck.fulldeck[num]["value"]+deck.fulldeck[num]["suit"],]
    def discard(self,string):
        for nums in string:
            index=int(nums)-1
            self.hand[index]=0
        for i in range(len(self.hand)):
            if 0 in self.hand:
                self.hand.remove(0)
    def replace(self,deck,string):
        ret=[]
        if len(string)>len(deck.deck):
            return None
        else:
            for nums in string:
                index=int(nums)-1
                num=deck.deck.pop()
                string=[deck.fulldeck[num]["value"]+deck.fulldeck[num]["suit"]]
                ret+=[self.hand[index],]
                self.hand[index]=string[0]
            return ret
    def reset(self):
        self.streak=0
        self.hand=[]

###Game class###
class game():
    def __init__(self,player1,player2):
        self.deck=deck()
        self.player1=player1
        self.player2=player2
        self.bet=0
        self.player2.draw(self.deck,5)
        self.player1.draw(self.deck,5)

    

###Room class###
class room():
    def __init__(self,player1,code):
        self.game=""
        self.code=code
        self.player1=player1
        self.player2=""

    def join(self,player2):
        self.player2=player2
        self.game=game(self.player1,self.player2)
        bot.send_message(self.player1.id, "Player2 have joined the game")
        bot.send_message(self.player2.id, str(self.player2.hand))
        bot.send_message(self.player1.id, str(self.player1.hand))
        bot.send_message(self.player1.id, "You start first, type the amount of $ you want to challenge")
        d[0]="player1_turn"
        

##host or join###
hostorjoin = types.ReplyKeyboardMarkup(row_width=2)
host = types.KeyboardButton('/host')
join = types.KeyboardButton('/join')
hostorjoin.add(host, join)

##check turn function
def check_turn(message,player):
    if message.chat.id!=player.id:
        return True
    
bot.polling()

    
##function to determine who win
def determine_poker_winner(hand1, hand2):
    """
    Determine which poker hand of 5 wins between hand1 and hand2.
    Each hand is a list of 5 strings, where each string contains a number value from A,2,3,4,5,6,7,8,9,10,J,Q,K and a suit ♦♣♥♠.
    Returns 1 if hand1 wins, 2 if hand2 wins, and 0 if it's a tie.
    """

    # Define the order of poker hands from highest to lowest
    poker_hands = [
        'Royal Flush',
        'Straight Flush',
        'Four of a Kind',
        'Full House',
        'Flush',
        'Straight',
        'Three of a Kind',
        'Two Pair',
        'One Pair',
        'High Card'
    ]

    # Define a function to convert card values from strings to integers
    def card_value(card):
        values = {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            'T': 10,
            '9': 9,
            '8': 8,
            '7': 7,
            '6': 6,
            '5': 5,
            '4': 4,
            '3': 3,
            '2': 2
        }
        return values[card[0]]

    # Define a function to check if a hand is a flush
    def is_flush(hand):
        return all(card[1] == hand[0][1] for card in hand)

    # Define a function to check if a hand is a straight
    def is_straight(hand):
        values = [card_value(card) for card in hand]
        values.sort()
        return all(values[i] == values[i-1] + 1 for i in range(1, 5))

    # Define a function to check if a hand is a straight flush
    def is_straight_flush(hand):
        return is_flush(hand) and is_straight(hand)

    # Define a function to check if a hand is a royal flush
    def is_royal_flush(hand):
        return is_flush(hand) and all(card[0] in ['A', 'K', 'Q', 'J', 'T'] for card in hand)

    # Define a function to check if a hand is a four of a kind
    def is_four_of_a_kind(hand):
        values = [card_value(card) for card in hand]
        return any(values.count(value) == 4 for value in values)

    # Define a function to check if a hand is a full house
    def is_full_house(hand):
        values = [card_value(card) for card in hand]
        return set(values) == set([2, 3]) or set(values) == set([3, 2])

    # Define a function to check if a hand is a three of a kind
    def is_three_of_a_kind(hand):
        values = [card_value(card) for card in hand]
        return any(values.count(value) == 3 for value in values)

    # Define a function to check if a hand is a two pair
    def is_two_pair(hand):
        values = [card_value(card) for card in hand]
        return len(set([value for value in values if values.count(value) == 2])) == 2

    # Define a function to check if a hand is a one pair
    def is_one_pair(hand):
        values = [card_value(card) for card in hand]
        return len(set([value for value in values if values.count(value) == 2])) == 1

    # Define a function to get the rank of a hand
    def get_rank(hand):
        if is_royal_flush(hand):
            return 'Royal Flush'
        elif is_straight_flush(hand):
            return 'Straight Flush'
        elif is_four_of_a_kind(hand):
            return 'Four of a Kind'
        elif is_full_house(hand):
            return 'Full House'
        elif is_flush(hand):
            return 'Flush'
        elif is_straight(hand):
            return 'Straight'
        elif is_three_of_a_kind(hand):
            return 'Three of a Kind'
        elif is_two_pair(hand):
            return 'Two Pair'
        elif is_one_pair(hand):
            return 'One Pair'
        else:
            return 'High Card'

    # Get the rank of each hand
    rank1 = get_rank(hand1)
    rank2 = get_rank(hand2)

    # Determine which hand wins
    if poker_hands.index(rank1) > poker_hands.index(rank2):
        return 1
    elif poker_hands.index(rank1) < poker_hands.index(rank2):
        return 2
    else:
        # If the hands have the same rank, compare the values of the cards to break the tie
        values1 = [card_value(card) for card in hand1]
        values2 = [card_value(card) for card in hand2]
        values1.sort(reverse=True)
        values2.sort(reverse=True)
        for i in range(5):
            if values1[i] > values2[i]:
                return 1
            elif values1[i] < values2[i]:
                return 2
        return 0




bot.polling()
