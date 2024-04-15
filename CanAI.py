import random

global playerScore
global compScore

playerScore = 0
compScore = 0

def createLists():
    global ranks 
    global suits
    global library
    global deck 
    global playerHand
    global compHand
    global discard
    global playerField
    global compField
    global refScores
    global isPlayerTurnOne
    global isCompTurnOne
    global isFrozen
    global knownPlayerCards

    ranks = {
        "A": "Ace",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        "0": "Ten",
        "J": "Jack",
        "Q": "Queen",
        "K": "King"
    }
    suits = {
        "C": "Clubs",
        "D": "Diamonds",
        "H": "Hearts",
        "S": "Spades"
    }
    refScores = {
        '3': 5,
        '4': 5,
        '5': 5,
        '6': 5,
        '7': 5,
        '8': 10,
        '9': 10,
        '0': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
        'A': 20,
        '2': 20,
        'O': 50
    }
    library = {}
    deck = []
    playerHand = []
    compHand = []
    discard = []
    playerField = {}
    compField = {}
    isPlayerTurnOne = True
    isCompTurnOne = True
    isFrozen = False
    knownPlayerCards = {}
    for rank in refScores.keys():
        knownPlayerCards[rank] = 0

def buildLibrary():
    for suit in suits.keys():
        for rank in ranks.keys():
            library[rank + suit] = ranks[rank] + " of " + suits[suit]

def buildDeck():
    for card in library.keys():
        deck.append(card)
        deck.append(card)
    for i in range(4):
        deck.append("OO")
    random.shuffle(deck)

def sort(hand):
    tempHand = []
    secondTempHand = []
    tens = []
    jackQueens = []
    kings = []
    aces = []
    for card in hand:
        if card[0] == '2' or card[0] == 'O':
            tempHand.append(card)
        elif (card[0] >= '3' and card[0] <= '9'):
            secondTempHand.append(card)
        elif card[0] == '0':
            tens.append(card)
        else:
            if card[0] == 'J' or card[0] == 'Q':
                jackQueens.append(card)
            elif card[0] == "K":
                kings.append(card)
            else:
                aces.append(card)
    tempHand.sort()
    secondTempHand.sort()
    tens.sort()
    jackQueens.sort()
    kings.sort()
    aces.sort()
    wilds = []
    for i in range(len(tempHand)):
        ind = (i+1)*(-1)
        wilds.append(tempHand[ind])
    finalHand = wilds + secondTempHand + tens + jackQueens + kings + aces
    return finalHand

def sortField(field):
    ranks = []
    sortedField = {}
    for rank in list(field.keys()):
        ranks.append(rank)
    ranks = sort(ranks)
    for rank in ranks:
        sortedField[rank] = field[rank]
    return sortedField

def draw(hand, field, numDraws):
    for i in range(numDraws):
        if len(deck) == 0:
            return "end"
        card = deck.pop(random.randint(0, len(deck)-1))
        if card == "3D" or card == "3H":
            if '3R' not in field.keys():
                field['3R'] = [card]
            else:
                field['3R'].append(card)
            test = draw(hand, field, 1)
            if test == "end":
                return
        else:
            hand.append(card)
        # hand = sort(hand)

def dealHands():
    for i in range(15):
        global playerHand
        global compHand
        draw(playerHand, playerField, 1)
        draw(compHand, compField, 1)
        playerHand = sort(playerHand)
        compHand = sort(compHand)
    discard.append(deck.pop(random.randint(0, len(deck)-1)))

def countNumRank(rank, hand):
    ct = 0
    for card in hand:
        if card[0] == rank:
            ct += 1
    return ct

def countNumWC(list):
    wildCount = 0
    for card in list:
            if card[0] == '2' or card[0] == 'O':
                wildCount += 1
    return wildCount

def hasCanasta(field):
    for rank in field.keys():
        if len(field[rank]) >= 7:
            return True
    return False

def canGoOut(hand, field):
    if hasCanasta(field):
        return True
    else:
        wildCt = countNumWC(hand)
        onFieldWC = 0
        for card in hand:
            if card[0] == '2' or card[0] == 'O':
                continue
            ct = countNumRank(card[0], hand)
            onField = 0
            if card[0] not in field.keys():
                onField = 0
            else:
                onField = len(field[card[0]])
                onFieldWC = countNumWC(field[card[0]])
            if ct + onField + wildCt >= 7 and ct + onField - onFieldWC >= 4:
                return True
        for rank in field:
            if len(field[rank]) + wildCt >= 7 and len(field[rank]) - countNumWC(field[rank]) >= 4:
                return True
    return False

def calcValueField(field):
    score = 0
    for rank in field.keys():
        if rank == "3R":
            if len(field[rank]) == 4:
                score += 800
            else:
                score += 100*len(field[rank])
        else:
            isRed = True
            for card in field[rank]:
                score += refScores[card[0]]
                if not card[0] == rank:
                    isRed = False
            if len(field[rank]) >= 7:
                if isRed:
                    score += 500
                else:
                    score += 300
    return score

def calcValueFieldNoThrees(field):
    score = 0
    for rank in field.keys():
        if not rank == "3R":
            for card in field[rank]:
                score += refScores[card[0]]
    return score

def calcValueHand(hand):
    score = 0
    for card in hand:
        score += refScores[card[0]]
    return score

def printScore():
    print("Score")
    print("Player 1: " + str(playerScore) + " + " + str(calcValueField(playerField)) + " - " + str(calcValueHand(playerHand)))
    print("Computer: " + str(compScore) + " + " + str(calcValueField(compField)) + " - " + str(calcValueHand(compHand)))

def retToHand(toPlay, hand):
    for rank in list(toPlay.keys()):
        for card in list(toPlay[rank]):
            hand.append(card)
            toPlay[rank].remove(card)
    sort(hand)
            
def hasLetter(string):
    for char in string:
        if char < '0' or char > '9':
            return True
    return False

def setPlayerTurn():
    isPlayerTurnOne = False

def onlyRedThrees(field):
    for rank in field.keys():
        if not rank == "3R" and len(field[rank]) > 0:
            return False
    return True    

def printField():
    # print("Deck:\n", deck)
    global playerField
    global compField
    playerField = sortField(playerField)
    compField = sortField(compField)
    printScore()
    print("Discard:\n", discard)
    print("Player Hand:\n", playerHand)
    print("Player Field:\n", playerField)
    # print("Computer Hand:\n", compHand)
    print("Computer Hand Length:", len(compHand))
    print("Computer Field:\n", compField)
    print("\n")

def checkFrozen():
    for card in discard:
        if card[0] == "2" or card[0] == 'O' or card == "3D" or card == "3H":
            return True
    return False

def checkOnlyBlackThrees(hand):
    ct = 0
    for card in hand:
        if not card[0] == '3':
            ct += 1
    if ct > 1:
        return False
    return True

def playCards(pickedUp, scoreToBeat):
    global isPlayerTurnOne
    global playerField
    global playerHand
    global discard

    action = input().upper()
    do=True
    if action == "Play" or action == "P" or action == "p":
        printField()
        print("How many cards from your hand would you like to play? Type 'E' to exit.")
        while do:
            action = input().upper()
            if (action == 'E' or action == "e") and not isPlayerTurnOne:
                ct = 0
                for card in playerField[list(toPlay.keys())[0]]:
                    if card == pickedUp and ct < 1:
                        discard.append(card)
                        ct += 1
                    else:
                        playerHand.append(card)
                del playerField[list(toPlay.keys())[0]]
                printField()
                print("Type 'D' to draw or 'U' to pick up the discard pile.")
                return playCards(pickedUp, scoreToBeat)
            elif action  == "E":
                printField()
                return action
            elif hasLetter(action):
                print("I'm sorry, your input was not a number.  Please enter a number.")
            elif (not int(action) > 0 or not int(action) <= len(playerHand)):
                print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
            elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
                print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
            else:
                numToPlay = int(action)
                toPlay = {}
                i = 0
                needBreak = False
                while i < numToPlay:
                    if not do:
                        break
                    if not i==0:
                        printField()
                        print("Please enter the next card.")
                    else:
                        printField()
                        print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
                        while do:
                            action = input().upper()
                            printField()
                            if action == "E" or action == "e":
                                do = False
                                needBreak = True
                                print("How many cards from your hand would you like to play? Type 'E' to exit.")
                            elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
                                print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
                            else:
                                if action not in playerField.keys() and numToPlay < 3:                                            
                                    print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
                                    numToPlay = 3
                                toPlay[action] = []
                                do = False
                                print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
                    i += 1
                    if needBreak:
                        do = True
                        break
                    do = True
                    while do:
                        action = input().upper()
                        if action == "E" or action == "e":
                            do = False
                            print("How many cards from your hand would you like to play? Type 'E' to exit.")
                        elif action not in playerHand:
                            print("I'm sorry, that card is not in the player's hand, choose a different card.")
                        else:
                            if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
                                print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
                            else:
                                toPlay[list(toPlay.keys())[0]].append(action)
                                playerHand.remove(action)
                                do=False
                    do=True
                    if action == "E" or action == "e":
                        retToHand(toPlay, playerHand)
                        playerHand = sort(playerHand)
                        discard.append(pickedUp)
                        break
                if not action == "E" and not action == "e":
                    if list(toPlay.keys())[0] not in playerField.keys():
                        if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            discard.append(pickedUp)
                            printField()
                            print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
                            print("How many cards from your hand would you like to play? Type 'E' to exit.")
                            continue
                        else:
                            playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
                            if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                            else:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                    elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
                        retToHand(toPlay, playerHand)
                        playerHand = sort(playerHand)
                        discard.append(pickedUp)
                        printField()
                        print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
                        print("How many cards from your hand would you like to play? Type 'E' to exit.")
                        continue
                    else:
                        for card in toPlay[list(toPlay.keys())[0]]:
                            playerField[list(toPlay.keys())[0]].append(card)
                        if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                            knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                        else:
                            knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                    score = calcValueFieldNoThrees(playerField)
                    if score >= scoreToBeat:
                        for card in discard:
                            # if card == pickedUp:
                            #     continue  
                            if card == "3D" or card == "3H":
                                if '3R' not in playerField.keys():
                                    playerField['3R'] = [card]
                                else:
                                    playerField['3R'].append(card)
                                continue
                            playerHand.append(card)
                            knownPlayerCards[card[0]] += 1
                        discard.clear()
                        playerHand = sort(playerHand)
                        # setPlayerTurn()
                        isPlayerTurnOne = False
                        do = False
                    printField()
                    if len(playerHand) == 0:
                        do = False
                        return "end"
                    print("How many cards from your hand would you like to play? Type 'E' to exit.")
    elif action == "D":
        test = draw(playerHand, playerField, 2)
        if test == "end":
            return test
        playerHand = sort(playerHand)
        ct = 0
        print(toPlay)
        for card in playerField[list(toPlay.keys())[0]]:
            if card == pickedUp and ct < 1:
                discard.append(card)
                ct += 1
            else:
                playerHand.append(card)
        del playerField[list(toPlay.keys())[0]]
        # printField()
        do = False
        action = "E"
        playerHand = sort(playerHand)
        printField()
        return "br"
    else:
        print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
        return "cont"

def playerTurn():
    global isPlayerTurnOne
    global playerHand
    global compHand
    global isFrozen
    isFrozen = checkFrozen()
    printField()
    print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
    do = True
    while do:
        action = input().upper()
        if action == "Draw" or action == "D" or action == "d":
            test = draw(playerHand, playerField, 2)
            if test == "end":
                return
            playerHand = sort(playerHand)
            do = False
            printField()
        elif action == "U" or action =="u":
            pickedUp = discard.pop(-1)
            if pickedUp[0] == '2' or pickedUp[0] == 'O' or pickedUp[0] == '3':
                print("I'm sorry, but you cannot pick up that card.  Please type 'D' to draw instead.")
                discard.append(pickedUp)
                continue
            elif pickedUp[0] in playerField.keys() and not isFrozen:
                playerHand.append(pickedUp)
                if len(playerHand) == 1 and len(discard) == 0 and not canGoOut(playerHand, playerField):
                    print("I'm sorry, you cannot go out because you do not have a canasta.  Please draw instead.")
                    playerHand.pop(-1)
                    discard.append(pickedUp)
                else:
                    playerField[pickedUp[0]].append(pickedUp)
                    playerHand.pop(-1)
                    for card in discard:
                        if card == "3D" or card == "3H":
                            if '3R' not in playerField.keys():
                                playerField['3R'] = [card]
                            else:
                                playerField['3R'].append(card)
                            continue
                        playerHand.append(card)
                        knownPlayerCards[card[0]] += 1
                    playerHand = sort(playerHand)
                    discard.clear()
                    do = False
            elif not isFrozen and countNumRank(pickedUp[0], playerHand) + countNumWC(playerHand) >= 2 and countNumRank(pickedUp[0], playerHand) >= 1:
                if len(playerHand) - 2 + len(discard) <= 1 and not canGoOut(playerHand, playerField):
                    print("I'm sorry, you cannot go out because you do not have a canasta.  Please draw instead.")
                    discard.append(pickedUp)
                else:
                    numToPlay = 2
                    action = ""
                    toPlay = {}
                    toPlay[pickedUp[0]] = []
                    i = 0
                    while i < numToPlay:
                        if not do:
                            break
                        if not i==0:
                            printField()
                            print("Please enter the next card.")
                        else:
                            printField()
                            print("Enter the symbol (e.g., 'AC') of the first card you would like to play alongside the card you picked up.  Type 'E' to exit.")
                        i += 1
                        do = True
                        while do:
                            action = input().upper()
                            print(action)
                            if action == "E" or action == "e":
                                do = False
                                for card in toPlay[list(toPlay.keys())[0]]:
                                    playerHand.append(card)
                                playerHand = sort(playerHand)
                                toPlay.clear()
                                printField()
                                print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
                            elif action not in playerHand:
                                print("I'm sorry, that card is not in the player's hand, choose a different card.")
                            else:
                                if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
                                    print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
                                else:
                                    toPlay[list(toPlay.keys())[0]].append(action)
                                    playerHand.remove(action)
                                    do=False
                        do=True
                        if action == "E" or action == "e":
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            discard.append(pickedUp)
                            break
                    if not action == "E" and not action == "e":
                        if list(toPlay.keys())[0] not in playerField.keys():
                            if countNumWC(toPlay[list(toPlay.keys())[0]]) > len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
                                retToHand(toPlay, playerHand)
                                playerHand = sort(playerHand)
                                discard.append(pickedUp)
                                printField()
                                print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand or the discard pile.")
                                print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
                                continue
                            else:
                                playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
                                playerField[list(toPlay.keys())[0]].append(pickedUp)
                                if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                    knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                                else:
                                    knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                        else:
                            for card in toPlay[list(toPlay.keys())[0]]:
                                playerField[list(toPlay.keys())[0]].append(card)
                            playerField[list(toPlay.keys())[0]].append(pickedUp)
                            if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                            else:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                            
                        printField()
                        do = False
                    elif action == "E":
                        continue
                    count = 0
                    while isPlayerTurnOne:
                        score = calcValueFieldNoThrees(playerField)
                        if count == 0:
                            count += 1
                            if playerScore < 1500 and score < 50:
                                print("You need to play a total of 50 points to pick up the rest of the discard pile.")
                                print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
                            elif playerScore >= 1500 and playerScore <3000 and score < 90:
                                print("You need to play a total of 90 points to pick up the rest of the discard pile.")
                                print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
                            elif playerScore >= 3000 and score < 120:
                                print("You need to play a total of 120 points to pick up the rest of the discard pile.")
                                print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
                        if (playerScore < 1500 and score < 50):
                            action = playCards(pickedUp, scoreToBeat = 50)
                            if action == "end":
                                return
                            elif action == "br":
                                break
                            elif action == "cont":
                                continue
                        elif playerScore >= 1500 and playerScore < 3000 and score < 90:
                            action = playCards(pickedUp, scoreToBeat = 90)
                            if action == "end":
                                return
                            elif action == "br":
                                break
                            elif action == "cont":
                                continue
                        elif playerScore >= 3000 and score < 120:
                            action = playCards(pickedUp, scoreToBeat = 120)
                            if action == "end":
                                return
                            elif action == "br":
                                break
                            elif action == "cont":
                                continue
                        ct = 0
                        if action == 'E' and isPlayerTurnOne:
                            for card in playerField[list(toPlay.keys())[0]]:
                                if card == pickedUp and ct < 1:
                                    discard.append(card)
                                    ct += 1
                                else:
                                    playerHand.append(card)
                            del playerField[list(toPlay.keys())[0]]
                            print("Type 'D' to draw two cards or 'U' to pick up the discard pile.")
                            break
                        elif action == 'E':
                            do=False
                            break
                        setPlayerTurn()
                        do=False
                        break
                    if not action == 'E':
                        for card in discard:
                            if card == "3D" or card == "3H":
                                if '3R' not in playerField.keys():
                                    playerField['3R'] = [card]
                                else:
                                    playerField['3R'].append(card)
                                continue
                            playerHand.append(card)
                            knownPlayerCards[card[0]] += 1
                        discard.clear()
                        playerHand = sort(playerHand)
                        printField()
            elif isFrozen and countNumRank(pickedUp[0], playerHand) >= 2:
                if len(playerHand) - 2 + len(discard) <= 1 and not canGoOut(playerHand, playerField):
                    print("I'm sorry, you cannot go out because you do not have a canasta.  Please draw instead.")
                    discard.append(pickedUp)
                else:
                    numToPlay = 2
                    action = ""
                    toPlay = {}
                    toPlay[pickedUp[0]] = []
                    i = 0
                    while i < numToPlay:
                        if not do:
                            break
                        if not i==0:
                            printField()
                            print("Please enter the next card.")
                        else:
                            printField()
                            print("Enter the symbol (e.g., 'AC') of the first card you would like to play alongside the card you picked up.  Type 'E' to exit.")
                        i += 1
                        do = True
                        while do:
                            action = input().upper()
                            print(action)
                            if action == "E" or action == "e":
                                do = False
                                for card in toPlay[list(toPlay.keys())[0]]:
                                    playerHand.append(card)
                                playerHand = sort(playerHand)
                                toPlay.clear()
                                printField()
                                print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
                            elif action not in playerHand:
                                print("I'm sorry, that card is not in the player's hand, choose a different card.")
                            else:
                                if not action[0] == list(toPlay.keys())[0]:
                                    print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
                                else:
                                    toPlay[list(toPlay.keys())[0]].append(action)
                                    playerHand.remove(action)
                                    do=False
                        do=True
                        if action == "E" or action == "e":
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            discard.append(pickedUp)
                            break
                    if not action == "E" and not action == "e":
                        if list(toPlay.keys())[0] not in playerField.keys():
                            if countNumWC(toPlay[list(toPlay.keys())[0]]) > len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
                                retToHand(toPlay, playerHand)
                                playerHand = sort(playerHand)
                                discard.append(pickedUp)
                                printField()
                                print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand or the discard pile.")
                                print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
                                continue
                            else:
                                playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
                                playerField[list(toPlay.keys())[0]].append(pickedUp)
                                if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                    knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                                else:
                                    knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                        else:
                            for card in toPlay[list(toPlay.keys())[0]]:
                                playerField[list(toPlay.keys())[0]].append(card)
                            playerField[list(toPlay.keys())[0]].append(pickedUp)
                            if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                            else:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                            
                        printField()
                        do = False
                    elif action == "E":
                        continue
                    count = 0
                    while isPlayerTurnOne:
                        score = calcValueFieldNoThrees(playerField)
                        if count == 0:
                            count += 1
                            if playerScore < 1500 and score < 50:
                                print("You need to play a total of 50 points to pick up the rest of the discard pile.")
                                print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
                            elif playerScore >= 1500 and playerScore <3000 and score < 90:
                                print("You need to play a total of 90 points to pick up the rest of the discard pile.")
                                print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
                            elif playerScore >= 3000 and score < 120:
                                print("You need to play a total of 120 points to pick up the rest of the discard pile.")
                                print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
                        if (playerScore < 1500 and score < 50):
                            action = playCards(pickedUp, scoreToBeat = 50)
                            if action == "end":
                                return
                            elif action == "br":
                                break
                            elif action == "cont":
                                continue
                        elif playerScore >= 1500 and playerScore < 3000 and score < 90:
                            action = playCards(pickedUp, scoreToBeat = 90)
                            if action == "end":
                                return
                            elif action == "br":
                                break
                            elif action == "cont":
                                continue
                        elif playerScore >= 3000 and score < 120:
                            action = playCards(pickedUp, scoreToBeat = 120)
                            if action == "end":
                                return
                            elif action == "br":
                                break
                            elif action == "cont":
                                continue
                        ct = 0
                        if action == 'E' and isPlayerTurnOne:
                            for card in playerField[list(toPlay.keys())[0]]:
                                if card == pickedUp and ct < 1:
                                    discard.append(card)
                                    ct += 1
                                else:
                                    playerHand.append(card)
                            del playerField[list(toPlay.keys())[0]]
                            print("Type 'D' to draw two cards or 'U' to pick up the discard pile.")
                            break
                        elif action == 'E':
                            do=False
                            break
                        setPlayerTurn()
                        do=False
                        break
                    if not action == 'E':
                        for card in discard:
                            if card == "3D" or card == "3H":
                                if '3R' not in playerField.keys():
                                    playerField['3R'] = [card]
                                else:
                                    playerField['3R'].append(card)
                                continue
                            playerHand.append(card)
                            knownPlayerCards[card[0]] += 1
                        discard.clear()
                        playerHand = sort(playerHand)
                        printField()
            else:
                print("I'm sorry, you cannot play that card.  Please draw instead.")
                discard.append(pickedUp)
        else:
            print("I'm sorry, that is not a valid action, type 'D' to draw two cards or 'U' to pick up the discard pile.")
    print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
    do = True
    while do:
        action = input().upper()
        if action == "Discard" or action == "C" or action == "c":
            if isPlayerTurnOne and len(playerField.keys()) > 0 and not onlyRedThrees(playerField):
                score = calcValueField(playerField)
                for rank in playerField.keys():
                    if rank == '3R':
                        if len(playerField[rank]) == 4:
                            score -= 800
                        else:
                            score -= 100*len(playerField[rank])
                if playerScore < 1500 and score < 50:
                    toTrim = []
                    for rank in playerField:
                        if not rank == "3R":
                            toPlay[rank] = playerField[rank]
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            toTrim.append(rank)
                    for rank in toTrim:
                        del playerField[rank]
                    print("I'm sorry, you need to make 50 points on your first play.  All cards played have been returned to your hand.")
                    print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
                    continue
                elif playerScore >= 1500 and playerScore < 3000 and score < 90:
                    toTrim = []
                    for rank in playerField:
                        if not rank == "3R":
                            toPlay[rank] = playerField[rank]
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            toTrim.append(rank)
                    for rank in toTrim:
                        del playerField[rank]
                    print("I'm sorry, you need to make 50 points on your first play.  All cards played have been returned to your hand.")
                    print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
                    continue
                elif playerScore >= 3000 and score < 120:
                    toTrim = []
                    for rank in playerField:
                        if not rank == "3R":
                            toPlay[rank] = playerField[rank]
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            toTrim.append(rank)
                    for rank in toTrim:
                        del playerField[rank]
                    print("I'm sorry, you need to make 50 points on your first play.  All cards played have been returned to your hand.")
                    print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
                    continue
                setPlayerTurn()
            printField()
            print("Type the symbol (e.g., 'AC') of the card you would like to discard.  Type 'E' to exit.")
            while do:
                action = input().upper()
                if action == 'E' or action == "e":
                    print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
                    break
                elif action not in playerHand:
                    print("I'm sorry, that card is not in the player's hand, type the symbol (e.g., 'AC') of the card you would like to discard.")
                else:
                    discard.append(playerHand.pop(playerHand.index(action)))
                    playerHand = sort(playerHand)
                    do = False
        elif action == "Play" or action == "P" or action == "p":
            printField()
            print("How many cards from your hand would you like to play? Type 'E' to exit.")
            while do:
                action = input().upper()
                if action == 'E' or action == "e":
                    print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
                    break
                elif hasLetter(action):
                    print("I'm sorry, your input was not a number.  Please enter a number.")
                elif (not int(action) > 0 or not int(action) <= len(playerHand)):
                    print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
                elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
                    print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
                else:
                    numToPlay = int(action)
                    toPlay = {}
                    i = 0
                    needBreak = False
                    while i < numToPlay:
                        if not do:
                            break
                        if not i==0:
                            printField()
                            print("Please enter the next card.")
                        else:
                            printField()
                            print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
                            while do:
                                action = input().upper()
                                printField()
                                if action == "E" or action == "e":
                                    do = False
                                    needBreak = True
                                    print("How many cards from your hand would you like to play? Type 'E' to exit.")
                                elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
                                    print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
                                elif action[0] == '3' and not checkOnlyBlackThrees(playerHand):
                                    print("I'm sorry, but you need to play the rest of the cards in your hand before you play your black threes.")
                                else:
                                    if action not in playerField.keys() and numToPlay < 3:                                            
                                        print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
                                        numToPlay = 3
                                    toPlay[action] = []
                                    do = False
                                    print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
                        i += 1
                        if needBreak:
                            do = True
                            break
                        do = True
                        while do:
                            action = input().upper()
                            if action == "E" or action == "e":
                                do = False
                                print("How many cards from your hand would you like to play? Type 'E' to exit.")
                            elif action not in playerHand:
                                print("I'm sorry, that card is not in the player's hand, choose a different card.")
                            else:
                                if (not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2') or (list(toPlay.keys())[0] == '3' and not action[0] == '3'):
                                    print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
                                else:
                                    toPlay[list(toPlay.keys())[0]].append(action)
                                    playerHand.remove(action)
                                    do=False
                        do=True
                        if action == "E" or action == "e":
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            break
                    if not action == "E" and not action == "e":
                        if list(toPlay.keys())[0] not in playerField.keys():
                            if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
                                retToHand(toPlay, playerHand)
                                playerHand = sort(playerHand)
                                printField()
                                print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
                                print("How many cards from your hand would you like to play? Type 'E' to exit.")
                                continue
                            else:
                                playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
                                if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                    knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                                else:
                                    knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                        elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
                            retToHand(toPlay, playerHand)
                            playerHand = sort(playerHand)
                            printField()
                            print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
                            print("How many cards from your hand would you like to play? Type 'E' to exit.")
                            continue
                        else:
                            for card in toPlay[list(toPlay.keys())[0]]:
                                playerField[list(toPlay.keys())[0]].append(card)
                            if len(toPlay) > knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]]:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] = 0
                            else:
                                knownPlayerCards[(toPlay[list(toPlay.keys())[0]])[0][0]] -= len(toPlay[list(toPlay.keys())[0]])
                        printField()
                        if len(playerHand) == 0:
                            do = False
                            break
                        print("How many cards from your hand would you like to play? Type 'E' to exit.")
        else:
            print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'C' to discard and end your turn.")

def knownNumCopies(rank):
    global playerField
    global knownPlayerCards

    numOnField = 0
    if rank in list(playerField.keys()):
        numOnField += len(playerField[rank])
    numOnField += knownPlayerCards[rank]
    return numOnField

def numSeen(rank):
    count = 0
    if rank in compField.keys():
        for card in compField[rank]:
            if card[0] == rank:
                count += 1
    if rank in playerField.keys():
        for card in playerField[rank]:
            if card[0] == rank:
                count += 1
    if rank in knownPlayerCards.keys():
        count += knownPlayerCards[rank]
    for card in compHand:
        if card[0] == rank:
            count += 1
    for card in discard:
        if card[0] == rank:
             count += 1
    return count
            
def compDiscard():
    global compHand
    global playerField
    global discard
    global knownPlayerCards
    
    if len(compHand) == 0:
        return
    for card in compHand:
        if card[0] == '3':
            discard.append(compHand.pop(compHand.index(card)))
            return
    if isFrozen:
        noDiscard = []
        onField = []
        for card in compHand:
            if knownPlayerCards[card[0]] >= 2:
                noDiscard.append(card)
            if card[0] in list(playerField.keys()):
                onField.append(card)
        length = 0
        ind = -100
        for card in onField:
            if card in noDiscard:
                continue
            elif len(playerField[card[0]]) > length:
                length = len(playerField[card[0]])
                ind = compHand.index(card)
        if not ind == -100:
            discard.append(compHand.pop(ind))
            return
        numCopiesSeen = 0
        ind = -100
        for card in compHand:
            if knownPlayerCards[card[0]] >= 1:
                continue
            if numSeen(card[0]) > numCopiesSeen:
                numCopiesSeen = numSeen(card[0])
                ind = compHand.index(card)
        if not ind == -100:
            discard.append(compHand.pop(ind))
            return
    singles = []
    doubles = []
    wild = []
    for card in compHand:
        if card[0] == 'O' or card[0] == '2':
            wild.append(card)
            continue
        if card[0] == '3':
            discard.append(compHand.pop(compHand.index(card)))
            return
        foundMatch = False
        for i in range(len(compHand)):
            if card[0] == compHand[i][0] and not compHand.index(card) == i:
                foundMatch = True
                doubles.append(card)
                break
        if not foundMatch:
            singles.append(card)
    for card in singles:
        if knownNumCopies(card[0]) == 0 and card[0] not in playerField.keys():
            discard.append(compHand.pop(compHand.index(card)))
            return
    for card in doubles:
        if knownNumCopies(card[0]) == 0 and card[0] not in playerField.keys():
            discard.append(compHand.pop(compHand.index(card)))
            return
    for card in singles:
        if knownNumCopies(card[0]) == 1 and card[0] not in playerField.keys():
            discard.append(compHand.pop(compHand.index(card)))
            return
    for card in doubles:
        if knownNumCopies(card[0]) == 1 and card[0] not in playerField.keys():
            discard.append(compHand.pop(compHand.index(card)))
            return
    if not len(wild) == 0:
        discard.append(compHand.pop(-1))
        return
    length = 100
    ind = 0
    for card in compHand:
        key = card[0]
        toAdd = 0
        if key in playerField.keys():
            toAdd = len(playerField[key])
        if knownNumCopies(key) + toAdd < length:
            length = knownNumCopies(key) + toAdd
            ind = compHand.index(card)
    discard.append(compHand.pop(ind))

def discardNoCopy():
    global compHand
    global playerField
    global discard
    if len(compHand) == 0:
        return
    if isFrozen:
        onField = []
        for card in compHand:
            if card[0] in list(playerField.keys()):
                onField.append(card)
        length = 0
        ind = -100
        for card in onField:
            if len(playerField[card[0]]) > length:
                length = len(playerField[card[0]])
                ind = compHand.index(card)
        if not ind == -100:
            discard.append(compHand.pop(ind))
            return
    doubles = []
    wild = []
    for card in compHand:
        if card[0] == 'O' or card[0] == '2':
            wild.append(card)
            continue
        foundMatch = False
        for i in range(len(compHand)):
            if card[0] == compHand[i][0] and not compHand.index(card) == i:
                foundMatch = True
                doubles.append(card)
                break
        if not foundMatch:
            if card[0] not in list(playerField.keys()):
                discard.append(compHand.pop(compHand.index(card)))
                return
    for card in doubles:
        if card[0] not in list(playerField.keys()):
            discard.append(compHand.pop(compHand.index(card)))
            return
    if not len(wild) == 0:
        discard.append(compHand.pop(-1))
        return
    length = 100
    ind = 0
    for card in compHand:
        key = card[0]
        if len(playerField[key]) < length:
            length = len(playerField[key])
            ind = compHand.index(card)
    discard.append(compHand.pop(ind))

def playThree():
    canPlay = []
    canPlayWithWild = []
    wild = []
    for card in compHand:
        if card[0] == 'O' or card[0] == '2':
            wild.append(card)
            continue
        elif card[0] == '3':
            continue
        ct = 0
        for i in range(len(compHand)):
            if card[0] == compHand[i][0]:
                ct += 1
        if ct >= 3 and card[0] not in canPlay:
            canPlay.append(card[0])
        elif ct + len(wild) - len(canPlayWithWild) >= 3 and ct == 2 and card[0] not in canPlayWithWild:
            canPlayWithWild.append(card[0])
    for rank in canPlay:
        if len(compHand) - 3 <= 1 and not canGoOut(compHand, compField):
            canPlay.clear()
            break
        toPlay = []
        for card in compHand:
            if rank == card[0]:
                toPlay.append(card)
        for card in toPlay:
            compHand.remove(card)
        compField[rank] = toPlay
    i = 0
    while i < len(canPlayWithWild):
        if (len(compHand) - 3 <= 1 and not canGoOut(compHand, compField)) or countNumWC(compHand) == 0:
            canPlayWithWild.clear()
            break
        toPlay = []
        numWild = 0
        for card in compHand:
            if canPlayWithWild[(-1)*(i+1)] == card[0]:
                toPlay.append(card)
            elif card[0] == "O" and numWild == 0:
                toPlay.append(card)
                numWild += 1
            elif card[0] == "2" and numWild == 0:
                toPlay.append(card)
                numWild += 1
        for card in toPlay:
            compHand.remove(card)
        compField[canPlayWithWild[(-1)*(i+1)]] = toPlay
        i+=1
        
def canMakeFirstPlay():
    canPlay = []
    canPlayLengths = []
    canPlayWithWild = []
    wild = []
    for card in compHand:
        if card[0] == 'O' or card[0] == '2':
            wild.append(card)
            continue
        elif card[0] == '3':
            continue
        ct = 0
        for i in range(len(compHand)):
            if card[0] == compHand[i][0]:
                ct += 1
        if ct >= 3:
            canPlay.append(card)
            canPlayLengths.append(ct)
        elif ct + len(wild) >= 3 and ct == 2:
            canPlayWithWild.append(card)
    canPlayScore = 0
    canPlayWithWildScore = 0
    wildScore = 0
    for card in canPlay:
        canPlayScore += refScores[card[0]]
    targetScore = 120
    if compScore < 1500:
        targetScore = 50
    elif compScore < 3000:
        targetScore = 90
    targetScore -= canPlayScore
    if targetScore <= 0:
        return True
    ct = 0
    while ct < len(canPlayWithWild)/2 and ct < len(wild):
        wildScore += refScores[wild[ct][0]]
        canPlayWithWildScore += refScores[canPlayWithWild[2*ct][0]]
        ct += 1
    targetScore -= (canPlayWithWildScore + wildScore)
    if targetScore <= 0:
        return True
    numWildsLeft = len(wild) - ct
    if numWildsLeft <= 0:
        return False
    numPossibleWilds = 0
    for length in canPlayLengths:
        numPossibleWilds += length - 1
    numWildsUsed = 0
    remainingWildScore = 0
    while ct < len(wild) and numPossibleWilds - numWildsUsed > 0:
        remainingWildScore += refScores[wild[ct][0]]
        ct += 1
        numWildsUsed += 1
    targetScore -= remainingWildScore
    if targetScore <= 0:
        return True

    # numWildsCt = len(wild)*2
    # i=0
    # while i < len(canPlayWithWild):
    #     if numWildsCt == 0:
    #         break
    #     numWildsCt -= 1
    #     canPlayWithWildScore += refScores[canPlayWithWild[(-1)*(i+1)][0]]
    #     i+=1
    # sum = 0
    # for length in canPlayLengths:
    #     sum += length
    # sum = sum - len(canPlayLengths)
    # i = 0
    # while i < (len(wild) - ct) and i < sum:
    #     wildScore += refScores[wild[ct+i][0]]
    #     i+=1
    # if compScore < 1500:
    #     if canPlayScore + canPlayWithWildScore + wildScore > 50:
    #         return True
    # elif compScore < 3000:
    #     if canPlayScore + canPlayWithWildScore + wildScore > 90:
    #         return True
    # elif compScore < 5000:
    #     if canPlayScore + canPlayWithWildScore + wildScore > 120:
    #         return True
    return False

def madeFirstPlay():
    score = calcValueFieldNoThrees(compField)
    if (compScore < 1500 and score >= 50) or (compScore < 3000 and compScore >= 1500 and score >= 90) or (compScore < 5000 and compScore >= 3000 and score >= 120):
        return True
    return False
    
def playWilds():
    global compHand
    global compField
    toRemoveCard = {}
    for card in compHand:
        toRemoveCard[card[0]] = []
        if card[0] == "2" or card[0] == "O":
            closest = ""
            closestLength = 0
            for rank in list(compField.keys()):
                if len(compField[rank]) >= 7:
                    continue
                elif countNumRank(rank, compField[rank]) > 1 + countNumWC (compField[rank]) and len(compField[rank]) > closestLength:
                    closest = rank
                    closestLength = len(compField[rank])
            if not closest == "":
                toRemoveCard[card[0]].append(card)
            print(canGoOut(compHand, compField))
            if len(compHand) - len(toRemoveCard[card[0]]) <= 1 and not canGoOut(compHand, compField):
                retToHand(toRemoveCard[card[0]], compHand)
                toRemoveCard.clear()
                break
            if not closest == "":
                compField[closest].append(card)
    for rank in toRemoveCard.keys():
        for card in toRemoveCard[rank]:
            compHand.remove(card)

def playSingles():
    toPlay = []
    for card in compHand:
        if card[0] in list(compField.keys()):
            toPlay.append(card)
        if len(compHand) - len(toPlay) <= 1 and not canGoOut(compHand, compField):
            toPlay.clear()
            break
    for card in toPlay:
        compField[card[0]].append(compHand.pop(compHand.index(card)))

def shouldPlay():
    global isFrozen
    if isFrozen and canGoOut(compHand, compField):
        return True
    elif isFrozen:
        return False
    elif not canGoOut(compHand, compField):
        if canGoOut(playerHand, playerField):
            return True
        elif len(compHand) <= 3:
            return False
        elif len(compHand) <= 5:
            playSingles()
            return False
    return True

def canPickUpDiscard():
    toPickUp = discard[-1]
    if toPickUp[0] == '3' or toPickUp[0] == '2' or toPickUp[0] == 'O':
        return False
    elif isFrozen:
        if countNumRank(toPickUp[0], compHand) >= 2:
            return True
    else:
        if countNumRank(toPickUp[0], compHand) + countNumWC(compHand) >= 2:
            return True
        elif toPickUp[0] in compField.keys():
            return True
    return False

def pickUpDiscard():
    pickedUp = discard.pop(-1)
    toPlay = {}
    toPlay[pickedUp[0]] = []
    for card in compHand:
        if card[0] == pickedUp[0]:
            toPlay[pickedUp[0]].append(card)
    if not isFrozen and len(toPlay[pickedUp[0]]) < 2 and pickedUp[0] not in compField.keys():
        for card in compHand:
            if card[0] == '2' or card[0] == 'O':
                toPlay[pickedUp[0]].append(card)
            if len(toPlay[pickedUp[0]]) >= 2:
                break
    if pickedUp[0] not in compField.keys():
        compField[pickedUp[0]] = []
        for card in toPlay[pickedUp[0]]:
            compField[pickedUp[0]].append(card)
        compField[pickedUp[0]].append(pickedUp)
    else:
        compField[pickedUp[0]].append(pickedUp)
        for card in toPlay[pickedUp[0]]:
            compField[pickedUp[0]].append(card)
    for card in toPlay[pickedUp[0]]:
        print(card)
        compHand.remove(card)
    for card in discard:
        compHand.append(card)
    sort(compHand)
    sortField(compField)
    discard.clear()
   
def compTurn():
    global compHand
    global isFrozen
    global isCompTurnOne
    isFrozen = checkFrozen()
    print(canPickUpDiscard())
    if not isCompTurnOne and canPickUpDiscard():
        pickUpDiscard()
    else:
        test = draw(compHand, compField, 2)
        if test == "end":
            return
    compHand = sort(compHand)
    if isCompTurnOne:
        print(canMakeFirstPlay())
        if canMakeFirstPlay():
            playThree()
        if not madeFirstPlay():
            playWilds()
            isCompTurnOne = False
        else:
            isCompTurnOne = False
    else:
        if shouldPlay():
            if not hasCanasta(compField):
                playSingles()
                playWilds()
                playThree()
            else:
                playSingles()
                playThree()
                playWilds()
    compDiscard()


    # discard.append(compHand.pop(random.randint(0, len(compHand)-1)))
        
def setScore(num, player):
    global playerScore
    global compScore
    if player == "C":
        compScore = num
    else:
        playerScore = num

def main():
    createLists()
    buildLibrary()
    buildDeck()
    dealHands()
    inGame = True
    while True:
        while inGame:
            if len(deck) == 0:
                printField()
                setScore(compScore + calcValueField(compField) -calcValueHand(compHand), "C")
                setScore(playerScore + calcValueField(playerField) - calcValueHand(playerHand), "P")
                break
            elif len(compHand) == 0:
                printField()
                setScore(compScore + calcValueField(compField) + 100, "C")
                setScore(playerScore + calcValueField(playerField) - calcValueHand(playerHand), "P")
                break
            playerTurn()
            if len(deck) == 0:
                printField()
                setScore(compScore + calcValueField(compField) -calcValueHand(compHand), "C")
                setScore(playerScore + calcValueField(playerField) - calcValueHand(playerHand), "P")
                break
            elif len(playerHand) == 0:
                printField()
                setScore(playerScore + calcValueField(playerField) + 100, "P")
                setScore(compScore + calcValueField(compField) - calcValueHand(compHand), "C")
                break
            compTurn()
        if not inGame:
            break
        print("Score")
        print("Player 1: " + str(playerScore))
        print("Computer: " + str(compScore))
        print()
        if compScore < 5000 and playerScore < 5000:
            print("Ready for the next hand?  Type 'S' to start or 'Q' to quit.")
            while True:
                action = input().upper()
                if action == 'S':
                    createLists()
                    buildLibrary()
                    buildDeck()
                    dealHands()
                    break
                elif action == "Q":
                    inGame = False
                    break
                else:
                    print("I'm sorry, that is not a valid action, type 'S' to start a new hand or 'Q' to quit")
        else:
            break
    if compScore > playerScore:
        print("The computer won!")
    else: print("The player won!")

print("test")

main()

# def playerTurn():
#     global isPlayerTurnOne
#     global playerHand
#     global compHand
#     global isFrozen
#     isFrozen = checkFrozen()
#     printField()
#     print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
#     do = True
#     while do:
#         action = input().upper()
#         if action == "Draw" or action == "D" or action == "d":
#             test = draw(playerHand, playerField, 2)
#             if test == "end":
#                 return
#             playerHand = sort(playerHand)
#             do = False
#             printField()
#         elif action == "U" or action =="u":
#             pickedUp = discard.pop(-1)
#             if pickedUp[0] == '2' or pickedUp[0] == 'O' or pickedUp[0] == '3':
#                 print("I'm sorry, but you cannot pick up that card.  Please type 'D' to draw instead.")
#                 discard.append(pickedUp)
#                 continue
#             elif pickedUp[0] in playerField.keys() and not isFrozen:
#                 playerHand.append(pickedUp)
#                 if len(playerHand) == 1 and len(discard) == 0 and not canGoOut(playerHand, playerField):
#                     print("I'm sorry, you cannot go out because you do not have a canasta.  Please draw instead.")
#                     playerHand.pop(-1)
#                     discard.append(pickedUp)
#                 else:
#                     playerField[pickedUp[0]].append(pickedUp)
#                     playerHand.pop(-1)
#                     for card in discard:
#                         # if card == pickedUp:
#                         #     continue
#                         if card == "3D" or card == "3H":
#                             if '3R' not in playerField.keys():
#                                 playerField['3R'] = [card]
#                             else:
#                                 playerField['3R'].append(card)
#                             continue
#                         playerHand.append(card)
#                     playerHand = sort(playerHand)
#                     discard.clear()
#                     do = False
#             elif not isFrozen and countNumRank(pickedUp[0], playerHand) + countNumWC(playerHand) >= 2 and countNumRank(pickedUp[0], playerHand) >= 1:
#                 if len(playerHand) - 2 + len(discard) <= 1 and not canGoOut(playerHand, playerField):
#                     print("I'm sorry, you cannot go out because you do not have a canasta.  Please draw instead.")
#                     discard.append(pickedUp)
#                 else:
#                     numToPlay = 2
#                     action = ""
#                     toPlay = {}
#                     toPlay[pickedUp[0]] = []
#                     i = 0
#                     # needBreak = False
#                     while i < numToPlay:
#                         if not do:
#                             break
#                         if not i==0:
#                             printField()
#                             print("Please enter the next card.")
#                         else:
#                             printField()
#                             print("Enter the symbol (e.g., 'AC') of the first card you would like to play alongside the card you picked up.  Type 'E' to exit.")
#                         i += 1
#                         # if needBreak:
#                         #     do = True
#                         #     break
#                         do = True
#                         while do:
#                             action = input().upper()
#                             print(action)
#                             if action == "E" or action == "e":
#                                 do = False
#                                 # discard.append(pickedUp)
#                                 for card in toPlay[list(toPlay.keys())[0]]:
#                                     playerHand.append(card)
#                                 playerHand = sort(playerHand)
#                                 toPlay.clear()
#                                 printField()
#                                 print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
#                             elif action not in playerHand:
#                                 print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             else:
#                                 if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                                     print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                                 else:
#                                     toPlay[list(toPlay.keys())[0]].append(action)
#                                     playerHand.remove(action)
#                                     do=False
#                         do=True
#                         if action == "E" or action == "e":
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             discard.append(pickedUp)
#                             break
#                     if not action == "E" and not action == "e":
#                         if list(toPlay.keys())[0] not in playerField.keys():
#                             if countNumWC(toPlay[list(toPlay.keys())[0]]) > len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                                 retToHand(toPlay, playerHand)
#                                 playerHand = sort(playerHand)
#                                 discard.append(pickedUp)
#                                 printField()
#                                 print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand or the discard pile.")
#                                 print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
#                                 continue
#                             else:
#                                 playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                                 playerField[list(toPlay.keys())[0]].append(pickedUp)
#                         else:
#                             for card in toPlay[list(toPlay.keys())[0]]:
#                                 playerField[list(toPlay.keys())[0]].append(card)
#                             playerField[list(toPlay.keys())[0]].append(pickedUp)
                            
#                         printField()
#                         # print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                         do = False
#                     elif action == "E":
#                         # printField()
#                         continue
#                     count = 0
#                     while isPlayerTurnOne:
#                         score = calcValueFieldNoThrees(playerField)
#                         if count == 0:
#                             count += 1
#                             if playerScore < 1500 and score < 50:
#                                 print("You need to play a total of 50 points to pick up the rest of the discard pile.")
#                                 print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                             elif playerScore >= 1500 and playerScore <3000 and score < 90:
#                                 print("You need to play a total of 90 points to pick up the rest of the discard pile.")
#                                 print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                             elif playerScore >= 3000 and score < 120:
#                                 print("You need to play a total of 120 points to pick up the rest of the discard pile.")
#                                 print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                         if (playerScore < 1500 and score < 50):
#                             action = playCards(pickedUp, scoreToBeat = 50)
#                             if action == "end":
#                                 return
#                             elif action == "br":
#                                 break
#                             elif action == "cont":
#                                 continue
#                             # action = input().upper()
#                             # do=True
#                             # if action == "Play" or action == "P" or action == "p":
#                             #     printField()
#                             #     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #     while do:
#                             #         action = input().upper()
#                             #         if (action == 'E' or action == "e") and not isPlayerTurnOne:
#                             #             ct = 0
#                             #             for card in playerField[list(toPlay.keys())[0]]:
#                             #                 if card == pickedUp and ct < 1:
#                             #                     discard.append(card)
#                             #                     ct += 1
#                             #                 else:
#                             #                     playerHand.append(card)
#                             #             del playerField[list(toPlay.keys())[0]]
#                             #             printField()
#                             #             print("Type 'D' to draw or 'U' to pick up the discard pile.")
#                             #             break
#                             #         elif action  == "E":
#                             #             printField()
#                             #             break
#                             #         elif hasLetter(action):
#                             #             print("I'm sorry, your input was not a number.  Please enter a number.")
#                             #         elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                             #             print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                             #         elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                             #             print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                             #         else:
#                             #             numToPlay = int(action)
#                             #             toPlay = {}
#                             #             i = 0
#                             #             needBreak = False
#                             #             while i < numToPlay:
#                             #                 if not do:
#                             #                     break
#                             #                 if not i==0:
#                             #                     printField()
#                             #                     print("Please enter the next card.")
#                             #                 else:
#                             #                     printField()
#                             #                     print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             #                     while do:
#                             #                         action = input().upper()
#                             #                         printField()
#                             #                         if action == "E" or action == "e":
#                             #                             do = False
#                             #                             needBreak = True
#                             #                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                             #                             print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                             #                         else:
#                             #                             if action not in playerField.keys() and numToPlay < 3:                                            
#                             #                                 print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                             #                                 numToPlay = 3
#                             #                             toPlay[action] = []
#                             #                             do = False
#                             #                             print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                             #                 i += 1
#                             #                 if needBreak:
#                             #                     do = True
#                             #                     break
#                             #                 do = True
#                             #                 while do:
#                             #                     action = input().upper()
#                             #                     if action == "E" or action == "e":
#                             #                         do = False
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     elif action not in playerHand:
#                             #                         print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             #                     else:
#                             #                         if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                             #                             print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                             #                         else:
#                             #                             toPlay[list(toPlay.keys())[0]].append(action)
#                             #                             playerHand.remove(action)
#                             #                             do=False
#                             #                 do=True
#                             #                 if action == "E" or action == "e":
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     break
#                             #             if not action == "E" and not action == "e":
#                             #                 if list(toPlay.keys())[0] not in playerField.keys():
#                             #                     if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                             #                         retToHand(toPlay, playerHand)
#                             #                         playerHand = sort(playerHand)
#                             #                         discard.append(pickedUp)
#                             #                         printField()
#                             #                         print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         continue
#                             #                     else:
#                             #                         playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                             #                 elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     printField()
#                             #                     print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     continue
#                             #                 else:
#                             #                     for card in toPlay[list(toPlay.keys())[0]]:
#                             #                         playerField[list(toPlay.keys())[0]].append(card)
#                                             # score = calcValueFieldNoThrees(playerField)
#                                             # if score >= 50:
#                                             #     for card in discard:
#                                             #         # if card == pickedUp:
#                                             #         #     continue  
#                                             #         if card == "3D" or card == "3H":
#                                             #             if '3R' not in playerField.keys():
#                                             #                 playerField['3R'] = [card]
#                                             #             else:
#                                             #                 playerField['3R'].append(card)
#                                             #             continue
#                                             #         playerHand.append(card)
#                                             #     discard.clear()
#                                             #     playerHand = sort(playerHand)
#                                             #     # setPlayerTurn()
#                                             #     isPlayerTurnOne = False
#                                             #     do = False
#                                             # printField()
#                                             # if len(playerHand) == 0:
#                                             #     do = False
#                                             #     break
#                                             # print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             # elif action == "D":
#                             #     test = draw(playerHand, playerField, 2)
#                             #     if test == "end":
#                             #         return
#                             #     playerHand = sort(playerHand)
#                             #     ct = 0
#                             #     print(toPlay)
#                             #     for card in playerField[list(toPlay.keys())[0]]:
#                             #         if card == pickedUp and ct < 1:
#                             #             discard.append(card)
#                             #             ct += 1
#                             #         else:
#                             #             playerHand.append(card)
#                             #     del playerField[list(toPlay.keys())[0]]
#                             #     # printField()
#                             #     do = False
#                             #     action = "E"
#                             #     playerHand = sort(playerHand)
#                             #     printField()
#                             #     break
#                             # else:
#                             #     print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
#                             #     continue
#                         elif playerScore >= 1500 and playerScore < 3000 and score < 90:
#                             # print("You need to play a total of 90 points to pick up the rest of the discard pile.")
#                             # print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                             action = playCards(pickedUp, scoreToBeat = 90)
#                             if action == "end":
#                                 return
#                             elif action == "br":
#                                 break
#                             elif action == "cont":
#                                 continue
                            
#                             # action = input().upper()
#                             # do=True
#                             # if action == "Play" or action == "P" or action == "p":
#                             #     printField()
#                             #     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #     while do:
#                             #         action = input().upper()
#                             #         if (action == 'E' or action == "e") and not isPlayerTurnOne:
#                             #             ct = 0
#                             #             for card in playerField[list(toPlay.keys())[0]]:
#                             #                 if card == pickedUp and ct < 1:
#                             #                     discard.append(card)
#                             #                     ct += 1
#                             #                 else:
#                             #                     playerHand.append(card)
#                             #             del playerField[list(toPlay.keys())[0]]
#                             #             printField()
#                             #             print("Type 'D' to draw or 'U' to pick up the discard pile.")
#                             #             break
#                             #         elif action  == "E":
#                             #             printField()
#                             #             break
#                             #         elif hasLetter(action):
#                             #             print("I'm sorry, your input was not a number.  Please enter a number.")
#                             #         elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                             #             print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                             #         elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                             #             print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                             #         else:
#                             #             numToPlay = int(action)
#                             #             toPlay = {}
#                             #             i = 0
#                             #             needBreak = False
#                             #             while i < numToPlay:
#                             #                 if not do:
#                             #                     break
#                             #                 if not i==0:
#                             #                     printField()
#                             #                     print("Please enter the next card.")
#                             #                 else:
#                             #                     printField()
#                             #                     print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             #                     while do:
#                             #                         action = input().upper()
#                             #                         printField()
#                             #                         if action == "E" or action == "e":
#                             #                             do = False
#                             #                             needBreak = True
#                             #                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                             #                             print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                             #                         else:
#                             #                             if action not in playerField.keys() and numToPlay < 3:                                            
#                             #                                 print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                             #                                 numToPlay = 3
#                             #                             toPlay[action] = []
#                             #                             do = False
#                             #                             print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                             #                 i += 1
#                             #                 if needBreak:
#                             #                     do = True
#                             #                     break
#                             #                 do = True
#                             #                 while do:
#                             #                     action = input().upper()
#                             #                     if action == "E" or action == "e":
#                             #                         do = False
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     elif action not in playerHand:
#                             #                         print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             #                     else:
#                             #                         if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                             #                             print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                             #                         else:
#                             #                             toPlay[list(toPlay.keys())[0]].append(action)
#                             #                             playerHand.remove(action)
#                             #                             do=False
#                             #                 do=True
#                             #                 if action == "E" or action == "e":
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     break
#                             #             if not action == "E" and not action == "e":
#                             #                 if list(toPlay.keys())[0] not in playerField.keys():
#                             #                     if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                             #                         retToHand(toPlay, playerHand)
#                             #                         playerHand = sort(playerHand)
#                             #                         discard.append(pickedUp)
#                             #                         printField()
#                             #                         print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         continue
#                             #                     else:
#                             #                         playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                             #                 elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     printField()
#                             #                     print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     continue
#                             #                 else:
#                             #                     for card in toPlay[list(toPlay.keys())[0]]:
#                             #                         playerField[list(toPlay.keys())[0]].append(card)
#                             #                 score = calcValueFieldNoThrees(playerField)
#                             #                 if score >= 90:
#                             #                     for card in discard:
#                             #                         # if card == pickedUp:
#                             #                         #     continue  
#                             #                         if card == "3D" or card == "3H":
#                             #                             if '3R' not in playerField.keys():
#                             #                                 playerField['3R'] = [card]
#                             #                             else:
#                             #                                 playerField['3R'].append(card)
#                             #                             continue
#                             #                         playerHand.append(card)
#                             #                     discard.clear()
#                             #                     playerHand = sort(playerHand)
#                             #                     # setPlayerTurn()
#                             #                     isPlayerTurnOne = False
#                             #                     do = False
#                             #                 printField()
#                             #                 if len(playerHand) == 0:
#                             #                     do = False
#                             #                     break
#                             #                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             # elif action == "D":
#                             #     test = draw(playerHand, playerField, 2)
#                             #     if test == "end":
#                             #         return
#                             #     playerHand = sort(playerHand)
#                             #     ct = 0
#                             #     print(toPlay)
#                             #     for card in playerField[list(toPlay.keys())[0]]:
#                             #         if card == pickedUp and ct < 1:
#                             #             discard.append(card)
#                             #             ct += 1
#                             #         else:
#                             #             playerHand.append(card)
#                             #     del playerField[list(toPlay.keys())[0]]
#                             #     # printField()
#                             #     do = False
#                             #     action = "E"
#                             #     playerHand = sort(playerHand)
#                             #     printField()
#                             #     break
#                             # else:
#                             #     print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
#                             #     continue
#                         elif playerScore >= 3000 and score < 120:
#                             action = playCards(pickedUp, scoreToBeat = 120)
#                             if action == "end":
#                                 return
#                             elif action == "br":
#                                 break
#                             elif action == "cont":
#                                 continue
                            
#                             # action = input().upper()
#                             # do=True
#                             # if action == "Play" or action == "P" or action == "p":
#                             #     printField()
#                             #     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #     while do:
#                             #         action = input().upper()
#                             #         if (action == 'E' or action == "e") and not isPlayerTurnOne:
#                             #             ct = 0
#                             #             for card in playerField[list(toPlay.keys())[0]]:
#                             #                 if card == pickedUp and ct < 1:
#                             #                     discard.append(card)
#                             #                     ct += 1
#                             #                 else:
#                             #                     playerHand.append(card)
#                             #             del playerField[list(toPlay.keys())[0]]
#                             #             printField()
#                             #             print("Type 'D' to draw or 'U' to pick up the discard pile.")
#                             #             break
#                             #         elif action  == "E":
#                             #             printField()
#                             #             break
#                             #         elif hasLetter(action):
#                             #             print("I'm sorry, your input was not a number.  Please enter a number.")
#                             #         elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                             #             print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                             #         elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                             #             print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                             #         else:
#                             #             numToPlay = int(action)
#                             #             toPlay = {}
#                             #             i = 0
#                             #             needBreak = False
#                             #             while i < numToPlay:
#                             #                 if not do:
#                             #                     break
#                             #                 if not i==0:
#                             #                     printField()
#                             #                     print("Please enter the next card.")
#                             #                 else:
#                             #                     printField()
#                             #                     print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             #                     while do:
#                             #                         action = input().upper()
#                             #                         printField()
#                             #                         if action == "E" or action == "e":
#                             #                             do = False
#                             #                             needBreak = True
#                             #                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                             #                             print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                             #                         else:
#                             #                             if action not in playerField.keys() and numToPlay < 3:                                            
#                             #                                 print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                             #                                 numToPlay = 3
#                             #                             toPlay[action] = []
#                             #                             do = False
#                             #                             print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                             #                 i += 1
#                             #                 if needBreak:
#                             #                     do = True
#                             #                     break
#                             #                 do = True
#                             #                 while do:
#                             #                     action = input().upper()
#                             #                     if action == "E" or action == "e":
#                             #                         do = False
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     elif action not in playerHand:
#                             #                         print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             #                     else:
#                             #                         if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                             #                             print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                             #                         else:
#                             #                             toPlay[list(toPlay.keys())[0]].append(action)
#                             #                             playerHand.remove(action)
#                             #                             do=False
#                             #                 do=True
#                             #                 if action == "E" or action == "e":
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     break
#                             #             if not action == "E" and not action == "e":
#                             #                 if list(toPlay.keys())[0] not in playerField.keys():
#                             #                     if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                             #                         retToHand(toPlay, playerHand)
#                             #                         playerHand = sort(playerHand)
#                             #                         discard.append(pickedUp)
#                             #                         printField()
#                             #                         print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         continue
#                             #                     else:
#                             #                         playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                             #                 elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     printField()
#                             #                     print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     continue
#                             #                 else:
#                             #                     for card in toPlay[list(toPlay.keys())[0]]:
#                             #                         playerField[list(toPlay.keys())[0]].append(card)
#                             #                 score = calcValueFieldNoThrees(playerField)
#                             #                 if score >= 120:
#                             #                     for card in discard:
#                             #                         # if card == pickedUp:
#                             #                         #     continue 
#                             #                         if card == "3D" or card == "3H":
#                             #                             if '3R' not in playerField.keys():
#                             #                                 playerField['3R'] = [card]
#                             #                             else:
#                             #                                 playerField['3R'].append(card)
#                             #                             continue 
#                             #                         playerHand.append(card)
#                             #                     discard.clear()
#                             #                     playerHand = sort(playerHand)
#                             #                     # setPlayerTurn()
#                             #                     isPlayerTurnOne = False
#                             #                     do = False
#                             #                 printField()
#                             #                 if len(playerHand) == 0:
#                             #                     do = False
#                             #                     break
#                             #                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             # elif action == "D":
#                             #     test = draw(playerHand, playerField, 2)
#                             #     if test == "end":
#                             #         return
#                             #     playerHand = sort(playerHand)
#                             #     ct = 0
#                             #     print(toPlay)
#                             #     for card in playerField[list(toPlay.keys())[0]]:
#                             #         if card == pickedUp and ct < 1:
#                             #             discard.append(card)
#                             #             ct += 1
#                             #         else:
#                             #             playerHand.append(card)
#                             #     del playerField[list(toPlay.keys())[0]]
#                             #     # printField()
#                             #     do = False
#                             #     action = "E"
#                             #     playerHand = sort(playerHand)
#                             #     printField()
#                             #     break
#                             # else:
#                             #     print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
#                             #     continue
#                         ct = 0
#                         if action == 'E' and isPlayerTurnOne:
#                             for card in playerField[list(toPlay.keys())[0]]:
#                                 if card == pickedUp and ct < 1:
#                                     discard.append(card)
#                                     ct += 1
#                                 else:
#                                     playerHand.append(card)
#                             del playerField[list(toPlay.keys())[0]]
#                             print("Type 'D' to draw two cards or 'U' to pick up the discard pile.")
#                             break
#                         elif action == 'E':
#                             do=False
#                             break
#                         setPlayerTurn()
#                         do=False
#                         break
#                     if not action == 'E':
#                         for card in discard:
#                             # if card == pickedUp:
#                             #     continue
#                             if card == "3D" or card == "3H":
#                                 if '3R' not in playerField.keys():
#                                     playerField['3R'] = [card]
#                                 else:
#                                     playerField['3R'].append(card)
#                                 continue
#                             playerHand.append(card)
#                         discard.clear()
#                         playerHand = sort(playerHand)
#                         printField()
#             elif isFrozen and countNumRank(pickedUp[0], playerHand) >= 2:
#                 if len(playerHand) - 2 + len(discard) <= 1 and not canGoOut(playerHand, playerField):
#                     print("I'm sorry, you cannot go out because you do not have a canasta.  Please draw instead.")
#                     discard.append(pickedUp)
#                 else:
#                     numToPlay = 2
#                     action = ""
#                     toPlay = {}
#                     toPlay[pickedUp[0]] = []
#                     i = 0
#                     # needBreak = False
#                     while i < numToPlay:
#                         if not do:
#                             break
#                         if not i==0:
#                             printField()
#                             print("Please enter the next card.")
#                         else:
#                             printField()
#                             print("Enter the symbol (e.g., 'AC') of the first card you would like to play alongside the card you picked up.  Type 'E' to exit.")
#                         i += 1
#                         # if needBreak:
#                         #     do = True
#                         #     break
#                         do = True
#                         while do:
#                             action = input().upper()
#                             print(action)
#                             if action == "E" or action == "e":
#                                 do = False
#                                 # discard.append(pickedUp)
#                                 for card in toPlay[list(toPlay.keys())[0]]:
#                                     playerHand.append(card)
#                                 playerHand = sort(playerHand)
#                                 toPlay.clear()
#                                 printField()
#                                 print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
#                             elif action not in playerHand:
#                                 print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             else:
#                                 if not action[0] == list(toPlay.keys())[0]:
#                                     print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                                 else:
#                                     toPlay[list(toPlay.keys())[0]].append(action)
#                                     playerHand.remove(action)
#                                     do=False
#                         do=True
#                         if action == "E" or action == "e":
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             discard.append(pickedUp)
#                             break
#                     if not action == "E" and not action == "e":
#                         if list(toPlay.keys())[0] not in playerField.keys():
#                             if countNumWC(toPlay[list(toPlay.keys())[0]]) > len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                                 retToHand(toPlay, playerHand)
#                                 playerHand = sort(playerHand)
#                                 discard.append(pickedUp)
#                                 printField()
#                                 print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand or the discard pile.")
#                                 print("It is the player's turn, type 'D' to draw two cards or 'U' to pick up the discard pile.")
#                                 continue
#                             else:
#                                 playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                                 playerField[list(toPlay.keys())[0]].append(pickedUp)
#                         else:
#                             for card in toPlay[list(toPlay.keys())[0]]:
#                                 playerField[list(toPlay.keys())[0]].append(card)
#                             playerField[list(toPlay.keys())[0]].append(pickedUp)
                            
#                         printField()
#                         # print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                         do = False
#                     elif action == "E":
#                         # printField()
#                         continue
#                     count = 0
#                     while isPlayerTurnOne:
#                         score = calcValueFieldNoThrees(playerField)
#                         if count == 0:
#                             count += 1
#                             if playerScore < 1500 and score < 50:
#                                 print("You need to play a total of 50 points to pick up the rest of the discard pile.")
#                                 print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                             elif playerScore >= 1500 and playerScore <3000 and score < 90:
#                                 print("You need to play a total of 90 points to pick up the rest of the discard pile.")
#                                 print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                             elif playerScore >= 3000 and score < 120:
#                                 print("You need to play a total of 120 points to pick up the rest of the discard pile.")
#                                 print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                         if (playerScore < 1500 and score < 50):
#                             action = playCards(pickedUp, scoreToBeat = 50)
#                             if action == "end":
#                                 return
#                             elif action == "br":
#                                 break
#                             elif action == "cont":
#                                 continue
                            
#                             # action = input().upper()
#                             # do=True
#                             # if action == "Play" or action == "P" or action == "p":
#                             #     printField()
#                             #     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #     while do:
#                             #         action = input().upper()
#                             #         if (action == 'E' or action == "e") and not isPlayerTurnOne:
#                             #             ct = 0
#                             #             for card in playerField[list(toPlay.keys())[0]]:
#                             #                 if card == pickedUp and ct < 1:
#                             #                     discard.append(card)
#                             #                     ct += 1
#                             #                 else:
#                             #                     playerHand.append(card)
#                             #             del playerField[list(toPlay.keys())[0]]
#                             #             printField()
#                             #             print("Type 'D' to draw or 'U' to pick up the discard pile.")
#                             #             break
#                             #         elif action  == "E":
#                             #             printField()
#                             #             break
#                             #         elif hasLetter(action):
#                             #             print("I'm sorry, your input was not a number.  Please enter a number.")
#                             #         elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                             #             print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                             #         elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                             #             print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                             #         else:
#                             #             numToPlay = int(action)
#                             #             toPlay = {}
#                             #             i = 0
#                             #             needBreak = False
#                             #             while i < numToPlay:
#                             #                 if not do:
#                             #                     break
#                             #                 if not i==0:
#                             #                     printField()
#                             #                     print("Please enter the next card.")
#                             #                 else:
#                             #                     printField()
#                             #                     print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             #                     while do:
#                             #                         action = input().upper()
#                             #                         printField()
#                             #                         if action == "E" or action == "e":
#                             #                             do = False
#                             #                             needBreak = True
#                             #                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                             #                             print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                             #                         else:
#                             #                             if action not in playerField.keys() and numToPlay < 3:                                            
#                             #                                 print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                             #                                 numToPlay = 3
#                             #                             toPlay[action] = []
#                             #                             do = False
#                             #                             print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                             #                 i += 1
#                             #                 if needBreak:
#                             #                     do = True
#                             #                     break
#                             #                 do = True
#                             #                 while do:
#                             #                     action = input().upper()
#                             #                     if action == "E" or action == "e":
#                             #                         do = False
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     elif action not in playerHand:
#                             #                         print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             #                     else:
#                             #                         if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                             #                             print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                             #                         else:
#                             #                             toPlay[list(toPlay.keys())[0]].append(action)
#                             #                             playerHand.remove(action)
#                             #                             do=False
#                             #                 do=True
#                             #                 if action == "E" or action == "e":
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     break
#                             #             if not action == "E" and not action == "e":
#                             #                 if list(toPlay.keys())[0] not in playerField.keys():
#                             #                     if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                             #                         retToHand(toPlay, playerHand)
#                             #                         playerHand = sort(playerHand)
#                             #                         discard.append(pickedUp)
#                             #                         printField()
#                             #                         print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         continue
#                             #                     else:
#                             #                         playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                             #                 elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     printField()
#                             #                     print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     continue
#                             #                 else:
#                             #                     for card in toPlay[list(toPlay.keys())[0]]:
#                             #                         playerField[list(toPlay.keys())[0]].append(card)
#                             #                 score = calcValueFieldNoThrees(playerField)
#                             #                 if score >= 50:
#                             #                     for card in discard:
#                             #                         # if card == pickedUp:
#                             #                         #     continue
#                             #                         if card == "3D" or card == "3H":
#                             #                             if '3R' not in playerField.keys():
#                             #                                 playerField['3R'] = [card]
#                             #                             else:
#                             #                                 playerField['3R'].append(card)
#                             #                             continue  
#                             #                         playerHand.append(card)
#                             #                     discard.clear()
#                             #                     playerHand = sort(playerHand)
#                             #                     # setPlayerTurn()
#                             #                     isPlayerTurnOne = False
#                             #                     do = False
#                             #                 printField()
#                             #                 if len(playerHand) == 0:
#                             #                     do = False
#                             #                     break
#                             #                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             # elif action == "D":
#                             #     test = draw(playerHand, playerField, 2)
#                             #     if test == "end":
#                             #         return
#                             #     playerHand = sort(playerHand)
#                             #     ct = 0
#                             #     print(toPlay)
#                             #     for card in playerField[list(toPlay.keys())[0]]:
#                             #         if card == pickedUp and ct < 1:
#                             #             discard.append(card)
#                             #             ct += 1
#                             #         else:
#                             #             playerHand.append(card)
#                             #     del playerField[list(toPlay.keys())[0]]
#                             #     # printField()
#                             #     do = False
#                             #     action = "E"
#                             #     playerHand = sort(playerHand)
#                             #     printField()
#                             #     break
#                             # else:
#                             #     print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
#                             #     continue
#                         elif playerScore >= 1500 and playerScore < 3000 and score < 90:
#                             # print("You need to play a total of 90 points to pick up the rest of the discard pile.")
#                             # print("Type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the discard pile (all cards will be returned to the correct location).")
#                             action = playCards(pickedUp, scoreToBeat = 90)
#                             if action == "end":
#                                 return
#                             elif action == "br":
#                                 break
#                             elif action == "cont":
#                                 continue
                            
#                             # action = input().upper()
#                             # do=True
#                             # if action == "Play" or action == "P" or action == "p":
#                             #     printField()
#                             #     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #     while do:
#                             #         action = input().upper()
#                             #         if (action == 'E' or action == "e") and not isPlayerTurnOne:
#                             #             ct = 0
#                             #             for card in playerField[list(toPlay.keys())[0]]:
#                             #                 if card == pickedUp and ct < 1:
#                             #                     discard.append(card)
#                             #                     ct += 1
#                             #                 else:
#                             #                     playerHand.append(card)
#                             #             del playerField[list(toPlay.keys())[0]]
#                             #             printField()
#                             #             print("Type 'D' to draw or 'U' to pick up the discard pile.")
#                             #             break
#                             #         elif action  == "E":
#                             #             printField()
#                             #             break
#                             #         elif hasLetter(action):
#                             #             print("I'm sorry, your input was not a number.  Please enter a number.")
#                             #         elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                             #             print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                             #         elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                             #             print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                             #         else:
#                             #             numToPlay = int(action)
#                             #             toPlay = {}
#                             #             i = 0
#                             #             needBreak = False
#                             #             while i < numToPlay:
#                             #                 if not do:
#                             #                     break
#                             #                 if not i==0:
#                             #                     printField()
#                             #                     print("Please enter the next card.")
#                             #                 else:
#                             #                     printField()
#                             #                     print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             #                     while do:
#                             #                         action = input().upper()
#                             #                         printField()
#                             #                         if action == "E" or action == "e":
#                             #                             do = False
#                             #                             needBreak = True
#                             #                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                             #                             print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                             #                         else:
#                             #                             if action not in playerField.keys() and numToPlay < 3:                                            
#                             #                                 print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                             #                                 numToPlay = 3
#                             #                             toPlay[action] = []
#                             #                             do = False
#                             #                             print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                             #                 i += 1
#                             #                 if needBreak:
#                             #                     do = True
#                             #                     break
#                             #                 do = True
#                             #                 while do:
#                             #                     action = input().upper()
#                             #                     if action == "E" or action == "e":
#                             #                         do = False
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     elif action not in playerHand:
#                             #                         print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             #                     else:
#                             #                         if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                             #                             print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                             #                         else:
#                             #                             toPlay[list(toPlay.keys())[0]].append(action)
#                             #                             playerHand.remove(action)
#                             #                             do=False
#                             #                 do=True
#                             #                 if action == "E" or action == "e":
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     break
#                             #             if not action == "E" and not action == "e":
#                             #                 if list(toPlay.keys())[0] not in playerField.keys():
#                             #                     if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                             #                         retToHand(toPlay, playerHand)
#                             #                         playerHand = sort(playerHand)
#                             #                         discard.append(pickedUp)
#                             #                         printField()
#                             #                         print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         continue
#                             #                     else:
#                             #                         playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                             #                 elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     printField()
#                             #                     print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     continue
#                             #                 else:
#                             #                     for card in toPlay[list(toPlay.keys())[0]]:
#                             #                         playerField[list(toPlay.keys())[0]].append(card)
#                             #                 score = calcValueFieldNoThrees(playerField)
#                             #                 if score >= 90:
#                             #                     for card in discard:
#                             #                         # if card == pickedUp:
#                             #                         #     continue 
#                             #                         if card == "3D" or card == "3H":
#                             #                             if '3R' not in playerField.keys():
#                             #                                 playerField['3R'] = [card]
#                             #                             else:
#                             #                                 playerField['3R'].append(card)
#                             #                             continue 
#                             #                         playerHand.append(card)
#                             #                     discard.clear()
#                             #                     playerHand = sort(playerHand)
#                             #                     # setPlayerTurn()
#                             #                     isPlayerTurnOne = False
#                             #                     do = False
#                             #                 printField()
#                             #                 if len(playerHand) == 0:
#                             #                     do = False
#                             #                     break
#                             #                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             # elif action == "D":
#                             #     test = draw(playerHand, playerField, 2)
#                             #     if test == "end":
#                             #         return
#                             #     playerHand = sort(playerHand)
#                             #     ct = 0
#                             #     print(toPlay)
#                             #     for card in playerField[list(toPlay.keys())[0]]:
#                             #         if card == pickedUp and ct < 1:
#                             #             discard.append(card)
#                             #             ct += 1
#                             #         else:
#                             #             playerHand.append(card)
#                             #     del playerField[list(toPlay.keys())[0]]
#                             #     # printField()
#                             #     do = False
#                             #     action = "E"
#                             #     playerHand = sort(playerHand)
#                             #     printField()
#                             #     break
#                             # else:
#                             #     print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
#                             #     continue
#                         elif playerScore >= 3000 and score < 120:
#                             action = playCards(pickedUp, scoreToBeat = 120)
#                             if action == "end":
#                                 return
#                             elif action == "br":
#                                 break
#                             elif action == "cont":
#                                 continue
                            
#                             # action = input().upper()
#                             # do=True
#                             # if action == "Play" or action == "P" or action == "p":
#                             #     printField()
#                             #     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #     while do:
#                             #         action = input().upper()
#                             #         if (action == 'E' or action == "e") and not isPlayerTurnOne:
#                             #             ct = 0
#                             #             for card in playerField[list(toPlay.keys())[0]]:
#                             #                 if card == pickedUp and ct < 1:
#                             #                     discard.append(card)
#                             #                     ct += 1
#                             #                 else:
#                             #                     playerHand.append(card)
#                             #             del playerField[list(toPlay.keys())[0]]
#                             #             printField()
#                             #             print("Type 'D' to draw or 'U' to pick up the discard pile.")
#                             #             break
#                             #         elif action  == "E":
#                             #             printField()
#                             #             break
#                             #         elif hasLetter(action):
#                             #             print("I'm sorry, your input was not a number.  Please enter a number.")
#                             #         elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                             #             print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                             #         elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                             #             print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                             #         else:
#                             #             numToPlay = int(action)
#                             #             toPlay = {}
#                             #             i = 0
#                             #             needBreak = False
#                             #             while i < numToPlay:
#                             #                 if not do:
#                             #                     break
#                             #                 if not i==0:
#                             #                     printField()
#                             #                     print("Please enter the next card.")
#                             #                 else:
#                             #                     printField()
#                             #                     print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             #                     while do:
#                             #                         action = input().upper()
#                             #                         printField()
#                             #                         if action == "E" or action == "e":
#                             #                             do = False
#                             #                             needBreak = True
#                             #                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                             #                             print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                             #                         else:
#                             #                             if action not in playerField.keys() and numToPlay < 3:                                            
#                             #                                 print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                             #                                 numToPlay = 3
#                             #                             toPlay[action] = []
#                             #                             do = False
#                             #                             print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                             #                 i += 1
#                             #                 if needBreak:
#                             #                     do = True
#                             #                     break
#                             #                 do = True
#                             #                 while do:
#                             #                     action = input().upper()
#                             #                     if action == "E" or action == "e":
#                             #                         do = False
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     elif action not in playerHand:
#                             #                         print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             #                     else:
#                             #                         if not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2':
#                             #                             print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                             #                         else:
#                             #                             toPlay[list(toPlay.keys())[0]].append(action)
#                             #                             playerHand.remove(action)
#                             #                             do=False
#                             #                 do=True
#                             #                 if action == "E" or action == "e":
#                             #                     retToHand(toPlay, playerHand)
#                             #                     playerHand = sort(playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     break
#                             #             if not action == "E" and not action == "e":
#                             #                 if list(toPlay.keys())[0] not in playerField.keys():
#                             #                     if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                             #                         retToHand(toPlay, playerHand)
#                             #                         playerHand = sort(playerHand)
#                             #                         discard.append(pickedUp)
#                             #                         printField()
#                             #                         print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                         continue
#                             #                     else:
#                             #                         playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                             #                 elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             #                     retToHand(toPlay, playerHand)
#                             #                     discard.append(pickedUp)
#                             #                     printField()
#                             #                     print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             #                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             #                     continue
#                             #                 else:
#                             #                     for card in toPlay[list(toPlay.keys())[0]]:
#                             #                         playerField[list(toPlay.keys())[0]].append(card)
#                             #                 score = calcValueFieldNoThrees(playerField)
#                             #                 if score >= 120:
#                             #                     for card in discard:
#                             #                         # if card == pickedUp:
#                             #                         #     continue  
#                             #                         if card == "3D" or card == "3H":
#                             #                             if '3R' not in playerField.keys():
#                             #                                 playerField['3R'] = [card]
#                             #                             else:
#                             #                                 playerField['3R'].append(card)
#                             #                             continue
#                             #                         playerHand.append(card)
#                             #                     discard.clear()
#                             #                     playerHand = sort(playerHand)
#                             #                     # setPlayerTurn()
#                             #                     isPlayerTurnOne = False
#                             #                     do = False
#                             #                 printField()
#                             #                 if len(playerHand) == 0:
#                             #                     do = False
#                             #                     break
#                             #                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             # elif action == "D":
#                             #     test = draw(playerHand, playerField, 2)
#                             #     if test == "end":
#                             #         return
#                             #     playerHand = sort(playerHand)
#                             #     ct = 0
#                             #     print(toPlay)
#                             #     for card in playerField[list(toPlay.keys())[0]]:
#                             #         if card == pickedUp and ct < 1:
#                             #             discard.append(card)
#                             #             ct += 1
#                             #         else:
#                             #             playerHand.append(card)
#                             #     del playerField[list(toPlay.keys())[0]]
#                             #     # printField()
#                             #     do = False
#                             #     action = "E"
#                             #     playerHand = sort(playerHand)
#                             #     printField()
#                             #     break
#                             # else:
#                             #     print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'D' to draw from the deck instead of picking up the pile.")
#                             #     continue
#                         ct = 0
#                         if action == 'E' and isPlayerTurnOne:
#                             for card in playerField[list(toPlay.keys())[0]]:
#                                 if card == pickedUp and ct < 1:
#                                     discard.append(card)
#                                     ct += 1
#                                 else:
#                                     playerHand.append(card)
#                             del playerField[list(toPlay.keys())[0]]
#                             print("Type 'D' to draw two cards or 'U' to pick up the discard pile.")
#                             break
#                         elif action == 'E':
#                             do=False
#                             break
#                         setPlayerTurn()
#                         do=False
#                         break
#                     if not action == 'E':
#                         for card in discard:
#                             # if card == pickedUp:
#                             #     continue
#                             if card == "3D" or card == "3H":
#                                 if '3R' not in playerField.keys():
#                                     playerField['3R'] = [card]
#                                 else:
#                                     playerField['3R'].append(card)
#                                 continue
#                             playerHand.append(card)
#                         discard.clear()
#                         playerHand = sort(playerHand)
#                         printField()
#             else:
#                 print("I'm sorry, you cannot play that card.  Please draw instead.")
#                 discard.append(pickedUp)
#         else:
#             print("I'm sorry, that is not a valid action, type 'D' to draw two cards or 'U' to pick up the discard pile.")
#     print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#     do = True
#     while do:
#         action = input().upper()
#         if action == "Discard" or action == "C" or action == "c":
#             if isPlayerTurnOne and len(playerField.keys()) > 0 and not onlyRedThrees(playerField):
#                 score = calcValueField(playerField)
#                 for rank in playerField.keys():
#                     if rank == '3R':
#                         if len(playerField[rank]) == 4:
#                             score -= 800
#                         else:
#                             score -= 100*len(playerField[rank])
#                 if playerScore < 1500 and score < 50:
#                     toTrim = []
#                     for rank in playerField:
#                         if not rank == "3R":
#                             toPlay[rank] = playerField[rank]
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             toTrim.append(rank)
#                     for rank in toTrim:
#                         del playerField[rank]
#                     print("I'm sorry, you need to make 50 points on your first play.  All cards played have been returned to your hand.")
#                     print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                     continue
#                 elif playerScore >= 1500 and playerScore < 3000 and score < 90:
#                     toTrim = []
#                     for rank in playerField:
#                         if not rank == "3R":
#                             toPlay[rank] = playerField[rank]
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             toTrim.append(rank)
#                     for rank in toTrim:
#                         del playerField[rank]
#                     print("I'm sorry, you need to make 50 points on your first play.  All cards played have been returned to your hand.")
#                     print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                     continue
#                 elif playerScore >= 3000 and score < 120:
#                     toTrim = []
#                     for rank in playerField:
#                         if not rank == "3R":
#                             toPlay[rank] = playerField[rank]
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             toTrim.append(rank)
#                     for rank in toTrim:
#                         del playerField[rank]
#                     print("I'm sorry, you need to make 50 points on your first play.  All cards played have been returned to your hand.")
#                     print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                     continue
#                 setPlayerTurn()
#             printField()
#             print("Type the symbol (e.g., 'AC') of the card you would like to discard.  Type 'E' to exit.")
#             while do:
#                 action = input().upper()
#                 if action == 'E' or action == "e":
#                     print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                     break
#                 elif action not in playerHand:
#                     print("I'm sorry, that card is not in the player's hand, type the symbol (e.g., 'AC') of the card you would like to discard.")
#                 else:
#                     discard.append(playerHand.pop(playerHand.index(action)))
#                     playerHand = sort(playerHand)
#                     do = False
#         elif action == "Play" or action == "P" or action == "p":
#             printField()
#             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#             while do:
#                 action = input().upper()
#                 if action == 'E' or action == "e":
#                     print("Type 'P' to play cards from your hand or 'C' to discard and end your turn.")
#                     break
#                 elif hasLetter(action):
#                     print("I'm sorry, your input was not a number.  Please enter a number.")
#                 elif (not int(action) > 0 or not int(action) <= len(playerHand)):
#                     print("I'm sorry, you cannot play that many cards.  Please enter a different number.")
#                 elif len(playerHand) - int(action) <= 1 and not canGoOut(playerHand, playerField):
#                     print("I'm sorry, you cannot go out because you do not have a canasta.  Please enter a different number.")
#                 else:
#                     numToPlay = int(action)
#                     toPlay = {}
#                     i = 0
#                     needBreak = False
#                     while i < numToPlay:
#                         if not do:
#                             break
#                         if not i==0:
#                             printField()
#                             print("Please enter the next card.")
#                         else:
#                             printField()
#                             print("Enter the rank of the canasta you would like to play on. Type 'E' to exit.")
#                             while do:
#                                 action = input().upper()
#                                 printField()
#                                 if action == "E" or action == "e":
#                                     do = False
#                                     needBreak = True
#                                     print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                                 elif len(action) > 1 or (not action == "J" and not action == "Q" and not action == "K" and not action == "O" and not action == "A" and not action == '0' and (not action > '2' or not action <= '9')):
#                                     print("I'm sorry, that is not a legal rank.  Please choose a different rank.")
#                                 elif action[0] == '3' and not checkOnlyBlackThrees(playerHand):
#                                     print("I'm sorry, but you need to play the rest of the cards in your hand before you play your black threes.")
#                                 else:
#                                     if action not in playerField.keys() and numToPlay < 3:                                            
#                                         print("Note, you need to play more cards to start this canasta.  Number of cards to play automatically increased to 3.  If you cannot play 3 cards, type 'E' to exit.")
#                                         numToPlay = 3
#                                     toPlay[action] = []
#                                     do = False
#                                     print("Enter the symbol (e.g., 'AC') of one of the cards you would like to play. Type 'E' to exit.")
#                         i += 1
#                         if needBreak:
#                             do = True
#                             break
#                         do = True
#                         while do:
#                             action = input().upper()
#                             if action == "E" or action == "e":
#                                 do = False
#                                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             elif action not in playerHand:
#                                 print("I'm sorry, that card is not in the player's hand, choose a different card.")
#                             else:
#                                 if (not action[0] == list(toPlay.keys())[0] and not action[0] == 'O' and not action[0] == '2') or (list(toPlay.keys())[0] == '3' and not action[0] == '3'):
#                                     print("I'm sorry, that card cannot be played on this rank of canasta.  Choose a different card.")
#                                 else:
#                                     toPlay[list(toPlay.keys())[0]].append(action)
#                                     playerHand.remove(action)
#                                     do=False
#                         do=True
#                         if action == "E" or action == "e":
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             break
#                     if not action == "E" and not action == "e":
#                         if list(toPlay.keys())[0] not in playerField.keys():
#                             if countNumWC(toPlay[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]):
#                                 retToHand(toPlay, playerHand)
#                                 playerHand = sort(playerHand)
#                                 printField()
#                                 print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                                 print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                                 continue
#                             else:
#                                 playerField[list(toPlay.keys())[0]] = toPlay[list(toPlay.keys())[0]]
#                         elif countNumWC(toPlay[list(toPlay.keys())[0]]) + countNumWC(playerField[list(toPlay.keys())[0]]) >= len(toPlay[list(toPlay.keys())[0]]) + len(playerField[list(toPlay.keys())[0]]) - countNumWC(toPlay[list(toPlay.keys())[0]]) - countNumWC(playerField[list(toPlay.keys())[0]]):
#                             retToHand(toPlay, playerHand)
#                             playerHand = sort(playerHand)
#                             printField()
#                             print("I'm sorry, but you are trying to play too many wildcards on this canasta.  All cards were returned to your hand.")
#                             print("How many cards from your hand would you like to play? Type 'E' to exit.")
#                             continue
#                         else:
#                             for card in toPlay[list(toPlay.keys())[0]]:
#                                 playerField[list(toPlay.keys())[0]].append(card)
#                         printField()
#                         if len(playerHand) == 0:
#                             do = False
#                             break
#                         print("How many cards from your hand would you like to play? Type 'E' to exit.")
#         else:
#             print("I'm sorry, that is not a valid action, type 'P' to play cards from your hand or 'C' to discard and end your turn.")
