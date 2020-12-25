import utils
import subprocess

DAY = 7
subprocess.run(["fetch_my_input_once.bat", str(DAY)])


# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

# So we need to do a graph I think

# This will contain reference to the nodes from the labels
BAGS = dict()  # { label : Node }


class Node(object):
    def __init__(self, label, children):
        self.label = label  # str (= color)
        self.children = children or dict()  # dict of {label: count} items

    def __repr__(self):
        return f"Node({self.label}, {self.children})"


def cleanLabel(label):
    label = label.replace(" bags", "")
    label = label.replace(" bag", "")
    label = label.strip()
    return label


def parseLine(line):
    if line.endswith("."):
        line = line[:-1]
    label, containsFull = line.split(" contain ")
    label = cleanLabel(label)
    children = dict()
    if "no other bags" not in containsFull:
        containsElem = containsFull.split(", ")
        for elem in containsElem:
            childCount = int(elem[0])
            childLabel = elem[1:]
            childLabel = cleanLabel(childLabel)
            children[childLabel] = childCount

    node = Node(label, children)
    BAGS[label] = node
    return node


for line in myInput:
    parseLine(line)


myColor = "shiny gold"

# Part 1

REACHABLE_FROM_SG = set()
reachedColors = [myColor]
while len(reachedColors) > 0:
    currentColor = reachedColors.pop()
    for color, node in BAGS.items():
        if currentColor in node.children.keys():
            if color not in REACHABLE_FROM_SG:
                REACHABLE_FROM_SG.add(color)
                reachedColors.append(color)

# print("reachable", REACHABLE_FROM_SG)
print("Part 1 - size", len(REACHABLE_FROM_SG))


# Part 2

CONTAINS_COUNT = dict()  # {label: count of contained bags}
# Dynamic programming pattern
# (Assumes the input is coherent and will not loop to infinity)
while myColor not in CONTAINS_COUNT:
    for label, node in BAGS.items():
        if label in CONTAINS_COUNT:
            continue
        if len(node.children.keys()) == 0:
            CONTAINS_COUNT[label] = 0
        elif all([key in CONTAINS_COUNT for key in node.children.keys()]):
            sub_counts = [
                count * (1 + CONTAINS_COUNT[key])
                for (key, count) in node.children.items()
            ]
            CONTAINS_COUNT[label] = sum(sub_counts)

print("Part 2 - contains", CONTAINS_COUNT[myColor])
