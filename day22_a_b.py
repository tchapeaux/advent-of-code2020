import utils
import subprocess
from collections import deque

DAY = 22
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

deck1 = deque()
deck2 = deque()

currentDeck = None
for line in myInput:
    if "Player 1" in line:
        currentDeck = deck1
    elif "Player 2" in line:
        currentDeck = deck2
    elif line:
        currentDeck.append(int(line))


def deckScore(deck):
    score = 0
    for idx, val in enumerate(deck):
        score += val * (len(deck) - idx)
    return score


def playGame(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card2 > card1:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise Exception(f"Same card {card1} {card2}")

    winningDeck = deck1 if len(deck1) > 0 else deck2
    return deckScore(winningDeck)


print("Part 1", playGame(deck1.copy(), deck2.copy()))


def playRecursiveGame(deck1, deck2):
    """ Returns a tuple (winningPlayer, winningScore) """
    # keep a round hash to check if a round is repeated
    SEEN_HASHES = set()
    roundTick = 0
    while len(deck1) > 0 and len(deck2) > 0:
        roundTick += 1
        roundHash = (
            ",".join([str(c) for c in deck1]) + "|" + ",".join([str(c) for c in deck2])
        )
        if roundHash in SEEN_HASHES:
            return (1, deckScore(deck1))
        # print("round", roundTick, roundHash)
        SEEN_HASHES.add(roundHash)

        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if card1 <= len(deck1) and card2 <= len(deck2):
            # Prepare subgame
            deck1Copy = deck1.copy()
            subDeck1 = deque()
            for _ in range(card1):
                subDeck1.append(deck1Copy.popleft())
            deck2Copy = deck2.copy()
            subDeck2 = deque()
            for _ in range(card2):
                subDeck2.append(deck2Copy.popleft())
            (subWinner, _) = playRecursiveGame(subDeck1, subDeck2)
        else:
            subWinner = 1 if card1 > card2 else 2

        if subWinner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            assert subWinner == 2
            deck2.append(card2)
            deck2.append(card1)

    winningDeck = deck1 if len(deck1) > 0 else deck2
    return (1 if len(deck1) > 0 else 2, deckScore(winningDeck))


print("Part 2", playRecursiveGame(deck1.copy(), deck2.copy()))
