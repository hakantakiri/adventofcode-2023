# --- Day 7: Camel Cards ---
# Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

# "Did you bring the parts?"

# You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

# "Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

# "The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

# After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

# You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

# Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

# In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

# Every hand is exactly one type. From strongest to weakest, they are:

# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456
# Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

# If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

# So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

# To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

# 32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483
# This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

# So, the first step is to put the hands in order of strength:

# 32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
# KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
# T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
# Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

# Find the rank of every hand in your set. What are the total winnings?

# Your puzzle answer was 251545216.

# --- Part Two ---
# To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

# To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

# J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

# Now, the above example goes very differently:

# 32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483
# 32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
# KK677 is now the only two pair, making it the second-weakest hand.
# T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
# With the new joker rule, the total winnings in this example are 5905.

# Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

# Your puzzle answer was 250384185.

import copy
f = open('inputs/doc_day_07.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def get_hands_and_points (lines) :
    hands_and_points = []
    for line in lines:
        hands_and_points.append([line.split(' ')[0].strip(), int(line.split(' ')[1].strip())])
    return hands_and_points

def is_5(hand):
    ini = hand[0]
    for c in hand:
        if c != ini:
            return False
    return True
def is_4(hand):
    uh = list(set(hand))
    if( len(uh) != 2):
        return False
    f = 0
    s = 0
    for c in hand:
        if c == uh[0]:
            f = f +1
        elif c == uh[1]  :
            s = s + 1
    if (f==4 or s==4):
        return True
    else:
        return False         
def is_3_2(hand):
    uh = list(set(hand))
    if( len(uh) != 2):
        return False
    f = 0
    s = 0
    for c in hand:
        if c == uh[0]:
            f = f +1
        elif c == uh[1]  :
            s = s + 1
    if (f==3 or s==3):
        return True
    else:
        return False 
def is_3(hand):
    uh = list(set(hand))
    if( len(uh) != 3):
        return False
    f = 0
    s = 0
    t = 0
    for c in hand:
        if c == uh[0]:
            f = f + 1
        elif c == uh[1]  :
            s = s + 1
        elif c == uh[2] :
            t = t + 1
    if (f==3 or s==3 or t ==3):
        return True
    else:
        return False   
def is_2_2(hand):
    uh = list(set(hand))
    if( len(uh) != 3):
        return False
    f = 0
    s = 0
    t = 0
    for c in hand:
        if c == uh[0]:
            f = f + 1
        elif c == uh[1]  :
            s = s + 1
        elif c == uh[2] :
            t = t + 1
    if (f==2 or s==2 or t ==2):
        return True
    else:
        return False
def is_2(hand):
    uh = list(set(hand))
    if( len(uh) == 4):
        return True
    else:
        return False
def is_h(hand):
    uh = list(set(hand))
    if len(uh) == 5:
        return True
    else:
        return False

def get_types(hands_p):
    hands_p_t = []
    for hand_p in hands_p:
        if (is_5(hand_p[0])):
            hands_p_t.append([hand_p[0], hand_p[1], 7])
        elif (is_4(hand_p[0])):
            hands_p_t.append([hand_p[0], hand_p[1], 6])
        elif (is_3_2(hand_p[0])):
            hands_p_t.append([hand_p[0], hand_p[1], 5])
        elif (is_3(hand_p[0])):
            hands_p_t.append([hand_p[0], hand_p[1], 4])
        elif (is_2_2(hand_p[0])):
            hands_p_t.append([hand_p[0], hand_p[1], 3])
        elif (is_2(hand_p[0])):
            hands_p_t.append([hand_p[0], hand_p[1], 2])
        elif (is_h(hand_p[0])):
             hands_p_t.append([hand_p[0], hand_p[1], 1])
        else:
            raise Exception('Error getting type for hand', hand_p)
    return hands_p_t

def is_5_j(hand):
    uh = list(set(hand))
    if len(uh) == 2 or len(uh) == 1:
        return True
    return False
def is_4_j(hand):
    uh = list(set(hand))
    if(len(uh) != 3):
        return False
    f = 0
    s = 0
    uh.remove('J')
    for c in hand:
        if c == uh[0] :
            f = f +1
        elif c == uh[1]  :
            s = s + 1
    if (f==1 or s==1):
        return True
    else:
        return False            
def is_3_2_j(hand):
    uh = list(set(hand))
    if( len(uh) != 3):
        return False
    sj = 0
    f = 0
    s = 0
    uh.remove('J')
    for c in hand:
        if c == 'J':
            sj = sj+1
        if c == uh[0] :
            f = f +1
        elif c == uh[1]  :
            s = s + 1
    if (sj ==1 and f==2 and s==2):
        return True
    else:
        return False
def is_3_j(hand):
    uh = list(set(hand))
    if( len(uh) != 4):
        return False
    return True
def is_2_2_j(hand):
    return False 
def is_2_j(hand):
    uh = list(set(hand))
    if( len(uh) == 5):
        return True
    else:
        return False
def is_h_j(hand):
    return False

def get_types_2(hands_p):

    hands_p_t = []
    for hand_p in hands_p:
        if(hand_p[0].find('J')<0):
            if (is_5(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 7])
            elif (is_4(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 6])
            elif (is_3_2(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 5])
            elif (is_3(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 4])
            elif (is_2_2(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 3])
            elif (is_2(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 2])
            elif (is_h(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 1])
            else:
                raise Exception('Error getting type for hand', hand_p)
        else:
            if (is_5_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 7])
            elif (is_4_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 6])
            elif (is_3_2_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 5])
            elif (is_3_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 4])
            elif (is_2_2_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 3])
            elif (is_2_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 2])
            elif (is_h_j(hand_p[0])):
                hands_p_t.append([hand_p[0], hand_p[1], 1])
            else:
                raise Exception('Error getting type for hand', hand_p)
    return hands_p_t

def condition(hands_p_t):
    def convert_c (c):
        if ('23456789'.find(c)>=0):
            return int(c)
        elif c == 'A':
            return 14
        elif c == 'K':
            return 13
        elif c == 'Q':
            return 12
        elif c == 'J':
            return 11
        elif c == 'T':
            return 10
        else:
            raise Exception('- - convert_c: Errror converting char:', c)
            
    hand = hands_p_t[0]
    return (hands_p_t[2], 
            convert_c(hand[0]),
            convert_c(hand[1]),
            convert_c(hand[2]),
            convert_c(hand[3]),
            convert_c(hand[4]),
            )

def condition_j(hands_p_t):
    def convert_c (c):
        if ('23456789'.find(c)>=0):
            return int(c)
        elif c == 'A':
            return 14
        elif c == 'K':
            return 13
        elif c == 'Q':
            return 12
        elif c == 'J':
            return 1
        elif c == 'T':
            return 10
        else:
            raise Exception('- - convert_c: Errror converting char:', c)
            
    hand = hands_p_t[0]
    return (hands_p_t[2], 
            convert_c(hand[0]),
            convert_c(hand[1]),
            convert_c(hand[2]),
            convert_c(hand[3]),
            convert_c(hand[4]),
            )

def order_by_type(hands_p_t):
    new_h = copy.deepcopy(hands_p_t)
    new_h.sort(key=condition)
    return new_h

def order_by_type_j(hands_p_t):
    new_h = copy.deepcopy(hands_p_t)
    new_h.sort(key=condition_j)
    return new_h

def get_wins(hands_p_t):
    wins = 0
    for i, h in enumerate(hands_p_t):
        wins = wins + h[1]*(i+1)
    return wins

#################################### EXECUTION SOLUTION 1

hands_p = get_hands_and_points(lines)
hands_p_t = get_types(hands_p)

# print(f'hands and points: {hands_p}')
# print(f'hands with types: {hands_p_t}')
ord_hands_p_t = order_by_type(hands_p_t)
# print(f'ordered hands with types: {ord_hands_p_t}')

wins = get_wins(ord_hands_p_t)
print(f'Solution 1: {wins}')

#################################### EXECUTION SOLUTION 2

hands_p_t = get_types_2(hands_p)

# print(f'hands and points: {hands_p}')
# print(f'hands with types: {hands_p_t}')
ord_hands_p_t = order_by_type_j(hands_p_t)
# print(f'ordered hands with types: {ord_hands_p_t}')

wins = get_wins(ord_hands_p_t)
print(f'Solution 2: {wins}')

# Solution 1: 251545216
# Solution 2: 250384185