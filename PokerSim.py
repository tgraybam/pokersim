# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 21:16:48 2017

@author: tgraybam
"""
import cmd 
import random
import collections
import itertools
from tqdm import tqdm

def new_deck():
    """
    create a deck of cards
    suit: club=C, diamond=D, heart=H spade=S
    rank: ace=A, 10=T, jack=J, queen=Q, king=K, numbers=2..9
    ace of spade would be AS, 8 of heart would be 8H and so on
    return a list of a full deck of cards
    """
    rs = [rank + suit for rank in "A23456789TJQK" for suit in "CDHS"]
    return rs
    
    
def draw_cards(n, cards_list):
    """
    randomly draw n cards from the deck (cards_list)
    remove those cards from the deck
    since object cards_list is by reference, it will change too
    return a list of n cards
    """
    random.shuffle(cards_list)
    return [cards_list.pop() for k in range(n)]

            
def hand_to_numbers(cards):
    card_rank = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
                 "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
                         "t": 10, "j": 11, "q": 12, "k": 13, "a": 14}
    result = []

    for i in cards:
        if len(i) == 1:
            a=card_rank[i]
        else:
            a=card_rank[i[0]]
        result.append(a)
    result.sort()
    return result
    
            
def check_straight(cards):
    hand = hand_to_numbers(cards)
    hand.sort()
    if  (hand[-1] - hand[-2]) ==1 and (hand[-2] - hand[-3]) == 1 and (hand[-3] - hand[-4]) ==1 and (hand[-4] - hand[-5]) ==1:
        handval = str(hand[-1])
        return ['Straight', handval]
    else:
        return False

 
def check_flush(cards):
    suit = cards[0][1]
    for i in cards[1:]:
        if i[1] == suit:
            continue
        else:
            return False
    hand = hand_to_numbers(cards)
    hand.sort()
    handval = hand[-1]    
    return ['Flush', handval]


def check_pairs(cards):
    if len(cards) != 5:
        return 'Not a proper hand'

    cards = hand_to_numbers(cards)
        
    seen = []
    uniq = []
    for x in cards:
        if len(uniq) == 0:
            uniq.append(x)
        else:
            if x in uniq:
                seen.append(x)
            else:
                uniq.append(x)
     
    if len(uniq) == 4:
        handval = seen[0]
        return ['One pair', handval]
    elif len(uniq) == 3:
        if len(set(seen)) == 1:
            handval = seen[0]
            return ['Three of a kind', handval]
        elif len(set(seen)) == 2:
            seen.sort()
            handval = str([seen[1], seen[0]])
            return ['Two pair', handval]
        else:
            return 'Weirdness'
    elif len(uniq) == 2:
        if len(set(seen)) == 1:
            handval = seen[0]
            return ['Four of a kind', handval]
        elif len(set(seen)) == 2:
            counts = collections.Counter(seen)
            #print counts
            sorted_three_and_pair = sorted(seen, key=lambda x: -counts[x])
            #print sorted_three_and_pair
            handval = str([sorted_three_and_pair[0],sorted_three_and_pair[2]])
            return ['Full house', handval]
        else:
            return 'More weirdness'
    elif len(uniq) == 5:
        return [False,False]  ## hack hack
      
      
def ValueHand(hand):
    if check_flush(hand) != False and check_straight(hand) != False:
        return ['Straight flush', check_flush(hand)[1]]
    elif check_pairs(hand)[0] == 'Four of a kind':
        return ['Four of a kind', check_pairs(hand)[1]]
    elif check_pairs(hand)[0] == 'Full house':
        return ['Full house', check_pairs(hand)[1]]
    elif check_flush(hand) != False:
        return check_flush(hand)
    elif check_straight(hand) != False:
        return check_straight(hand)
    elif check_pairs(hand)[0] == 'Three of a kind':
        return ['Three of a kind', check_pairs(hand)[1]]
    elif check_pairs(hand)[0] == 'Two pair':
        return ['Two pair', check_pairs(hand)[1]]
    elif check_pairs(hand)[0] == 'One pair':
        return ['One pair', check_pairs(hand)[1]]
    else:
        highcard = hand_to_numbers(hand)
        return ['High card',highcard[-1]]


def BestHand(Hand):

    hierarchy ={'Straight flush':1, "Four of a kind":2, 
    "Full house":3, "Flush":4, "Straight":5, "Three of a kind":6,"Two pair":7, 
    "One pair":8, "High card":9, 'Temporary default':20}
    #print Hand
    possible_hands = itertools.combinations(Hand,5)
 
    best = ['Temporary default',20] ## hack hack -- to start with a default comparison
    for i in possible_hands:
        #print i, ValueHand(i)
        newHand = ValueHand(i)
        #print newHand, hierarchy[newHand[0]]
        if hierarchy[newHand[0]] < hierarchy[best[0]]:
            best = newHand
        elif hierarchy[newHand[0]] == hierarchy[best[0]]:
            if type(newHand[1]) is list:
                if (newHand[1][0]) > best[1][0]:
                    best = newHand
                elif (newHand[1][0]) == best[1][0]:
                    if (newHand[1][1]) > best[1][1]:
                        best = newHand
                    else:
                        continue
            else:
                if (newHand[1]) > best[1]:
                    best=newHand
                else:
                    continue
#       print best
    return best
            
def BetterBestHand(Hands):

    hierarchy ={'Straight flush':1, "Four of a kind":2, 
    "Full house":3, "Flush":4, "Straight":5, "Three of a kind":6,"Two pair":7, 
    "One pair":8, "High card":9, 'Temporary default':20}
    #print Hand
 
    best = ['Temporary default',20] ## hack hack -- to start with a default comparison
    for i in Hands:
        #print i, ValueHand(i)
        newHand = i
        #print newHand, hierarchy[newHand[0]]
        if hierarchy[newHand[0]] < hierarchy[best[0]]:
            best = newHand
        elif hierarchy[newHand[0]] == hierarchy[best[0]]:
            if type(newHand[1]) is list:
                if (newHand[1][0]) > best[1][0]:
                    best = newHand
                elif (newHand[1][0]) == best[1][0]:
                    if (newHand[1][1]) > best[1][1]:
                        best = newHand
                    else:
                        continue
            else:
                if (newHand[1]) > best[1]:
                    best=newHand
                else:
                    continue
#       print best
    return best


        
class TexasHoldEmSim(cmd.Cmd):
    """Simulate frequency of poker hands based on two hole-cards"""
    
    prompt = '-->: '
    intro = "Simulate frequency of poker hands based on two hole-cards"
    
    def do_EOF(self, line):
        return True
    
    def do_RandomHoleCards(self, line):
        """Generate two random cards (mostly just for testing)"""
        foo=draw_cards(2,MainDeck)
        print foo
    
    def do_Test(self, cards):
        """test hand frequencies given two cards as input"""
        
        card1 = cards.split()[0]
        card2 = cards.split()[1]
        players = cards.split()[2]
        players = int(players)-1
        flops = cards.split()[3]
        Hand = [card1,card2]

        win=0
        lossortie=0

        for flop in tqdm(range(int(flops))):
            Hand = [card1,card2]
            handsintheflop=[]
            remainingdeck = list(set(MainDeck) - set([card1,card2]))
            random.shuffle(remainingdeck)

            flop_plus_river_plus_turn = [remainingdeck.pop() for k in range(5)]
            #print flop_plus_river_plus_turn
            Hand.extend(flop_plus_river_plus_turn)
            #print Hand
            myHand = BestHand(Hand)

            for h in range(players):
                tempHand = draw_cards(2, remainingdeck)
                remainingdeck = list(set(remainingdeck) - set(tempHand))
                tempHand.extend(flop_plus_river_plus_turn)
                besttempHand = BestHand(tempHand)
                handsintheflop.append(besttempHand)
                #print "temphand --->", tempHand, besttempHand                
        
            #print "Hand myHand ++++>", Hand, myHand
            handsintheflop.append(myHand)
            #print handsintheflop
            
            winner = BetterBestHand(handsintheflop)
            #print "winner >>>", winner
            #print "myHand >>>", myHand
            #print '----------------'
            if winner == myHand:
                win+=1
            else: 
                lossortie+=1
            myHand=[]  ## avoid the ever expanding myHand! 
            flop_plus_river_plus_turn = []
            handsintheflop = []
 
        print flops, win, lossortie
        expect = (win*1.0)/(int(flops)*1.0) * 100.0
        print 'Hole cards: %s ---> wins %s percent of the time in a %s handed game' % ([card1,card2], expect, (players+1))
        
if __name__ == '__main__':
    MainDeck = new_deck()
    TexasHoldEmSim().cmdloop()

    
#st = ['8H','9H','TD','JS','QH']
#fl = ['8H','9H','6H','2H','QH']
#sf = ['7H', '8H', '9H', 'TH', 'JH']
#hc = ['8H', '9H', 'TD', 'JS', '2D']
#fh = ['8H', '9H', '9D', '9S', '8D']
#tp = ['8H', '9H', '9D', 'TS', '8D']
#threek = ['8H', '9H', '9D', '9S', '2D']
#twok = ['8H', '9H', '9D', '3S', '2D']
#test = ['8H', '9H', '9D', '9S', '2D', 'AH','5D']
#test2 = ['8H', '9H', '9D', '8S', '2D', '9S','8C']
#tests = ['8H','9H','TD','JS','QH', 'KH','4S']
#g=[['One pair', 14], ['Two pair', '[14, 10]'], ['One pair', 14], ['Straight', '10'],['Straight','12'], ['Full house']]
