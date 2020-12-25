import utils
import subprocess

DAY = 23
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

myInput = utils.getRawInput(f"day{DAY:02}")
# utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

myInput = myInput.strip()

# Example input
# myInput = "389125467"


cups = [int(c) for c in myInput]
maxCup = max(cups)

# Helper functions/classes


class Node:
    """ linked list node """

    def __init__(self, val):
        self.val = val
        self.next = None


def getLoopAfterOne(node_dict):
    """ Return the cups represented as asked in the spec """
    oneNode = node_dict[1]
    currentNode = oneNode.next
    s = ""
    while currentNode != oneNode:
        s += str(currentNode.val)
        currentNode = currentNode.next
    return s


def getDebugString(node_dict, firstNode, currentNode):
    s = ""
    n = firstNode
    while True:
        if n == currentNode:
            s += "(" + str(n.val) + ") "
        else:
            s += str(n.val) + " "
        n = n.next
        if n == firstNode:
            return s


# Main game function


def playGame(cups, nbOfMoves):
    # Convert into doubly linked list
    # + dict for easy access
    NODE_DICT = {}
    for idx, val in enumerate(cups):
        n = Node(val)
        NODE_DICT[val] = n
        if idx > 0:
            nPrev = NODE_DICT[cups[idx - 1]]
            nPrev.next = n
    # link first and last nodes
    NODE_DICT[cups[-1]].next = NODE_DICT[cups[0]]

    maxCup = max(cups)
    currentNode = NODE_DICT[cups[0]]
    currentTick = 1
    while currentTick <= nbOfMoves:
        # print("--tick ", currentTick)
        # print(getDebugString(NODE_DICT, NODE_DICT[cups[0]], currentNode))
        # Remove next 3 cups by snipping them out
        snipStart = currentNode.next
        snipStop = snipStart.next.next
        # patch the other cups
        currentNode.next = snipStop.next

        snippedValues = [snipStart.val, snipStart.next.val, snipStop.val]

        # print("snipped values: " + "".join([str(v) for v in snippedValues]))

        # Find destination cup
        destinationValue = currentNode.val - 1
        while destinationValue == 0 or destinationValue in snippedValues:
            if destinationValue == 0:
                destinationValue = maxCup
            else:
                destinationValue -= 1

        destinationNode = NODE_DICT[destinationValue]

        # Add picked cups after the destinationNode
        destinationNextNode = destinationNode.next
        destinationNode.next = snipStart
        snipStop.next = destinationNextNode

        # Update current node
        currentNode = currentNode.next

        currentTick += 1

    return NODE_DICT


# Part 2
print("Part 1", getLoopAfterOne(playGame(cups.copy(), 10)))

# Part 2
cups = [int(c) for c in myInput] + list(range(maxCup + 1, int(1e6) + 1))

# Helper for Part 2
def getProdTwoAfterOne(node_dict):
    oneNode = node_dict[1]
    nextNode = oneNode.next
    nextNextNode = nextNode.next
    return nextNode.val * nextNextNode.val


print("Part 2", getProdTwoAfterOne(playGame(cups, int(1e7))))

# I of course had to rewrite the playGame() function for Part 2 because
# I used built-in lists at first.
# I also lost some time by first implementing doubly linked lists (prev/next),
# which was not useful
# Then I had a typo which made the snipped elements incorrect and messed up the
# chain
