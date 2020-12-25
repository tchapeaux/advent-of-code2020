import utils
import subprocess

DAY = 16
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

# Example inputs
"""
myInput = [
    "class: 0-1 or 4-19",
    "row: 0-5 or 8-19",
    "seat: 0-13 or 16-19",
    "",
    "your ticket:",
    "11,12,13",
    "",
    "nearby tickets:",
    "3,9,18",
    "15,1,5",
    "5,14,9",
]
# """

# Parse

yourTicketLineIdx = myInput.index("your ticket:")


def parseTicket(ticketStr):
    return [int(x) for x in ticketStr.split(",")]


class Field:
    def __init__(self, name, validRanges):
        self.name = name
        self.validRanges = validRanges
        self.idx = None

    def testNumber(self, n):
        for _r in self.validRanges:
            if _r[0] <= n <= _r[1]:
                return True
        return False


def parseConstraint(constraint):
    name, _r = constraint.split(":")
    range1, range2 = [x.strip() for x in _r.split(" or ")]
    validRanges = []
    min1, max1 = range1.split("-")
    validRanges.append((int(min1), int(max1)))
    min2, max2 = range2.split("-")
    validRanges.append((int(min2), int(max2)))
    return Field(name, validRanges)


myTicket = parseTicket(myInput[yourTicketLineIdx + 1])
nearbyTickets = [parseTicket(t) for t in myInput[yourTicketLineIdx + 4 :]]
fieldRules = [parseConstraint(c) for c in myInput[: yourTicketLineIdx - 1]]

errorRate = 0
for values in nearbyTickets:
    assert len(values) == len(fieldRules)
    for val in values:
        if not any([f.testNumber(val) for f in fieldRules]):
            errorRate += val

print("Part 1", errorRate)

# Part 2


def testTicket(values):
    for val in values:
        if not any([f.testNumber(val) for f in fieldRules]):
            return False
    return True


validTickets = [t for t in nearbyTickets if testTicket(t)]

print("There are", len(nearbyTickets), "nearby tickets")
print("There are", len(validTickets), "valid tickets")
print("There are", len(fieldRules), "rules")

# This seems small enough that we can brute force it

# possibilityMatrix[x][y] is true if position X can be rule Y
possibilityMatrix = [
    [True for _ in range(len(fieldRules))] for _2 in range(len(fieldRules))
]

# First pass
# Parse all values of all tickets to see which rules are possible at each location

for values in validTickets:
    for (x, val) in enumerate(values):
        for (y, rule) in enumerate(fieldRules):
            if rule.testNumber(val) is not True:
                possibilityMatrix[x][y] = False


def knowAllRulesIdx(fieldRules):
    return all([r.idx is not None for r in fieldRules])


# Second pass:
# a rule can be locked when the nb of possibility is 1
# when a rule is locked, this possibility is removed for all other rules
# rince and repeat

decidedIndices = set()  # take note of which indices we have already locked

while not knowAllRulesIdx(fieldRules):
    for x in range(len(possibilityMatrix)):
        if x in decidedIndices:
            continue
        if possibilityMatrix[x].count(True) == 1:
            # Lock this rule
            y = possibilityMatrix[x].index(True)
            assert fieldRules[y].idx is None
            fieldRules[y].idx = x
            decidedIndices.add(x)

            # Remove possibility for other rules
            for x2 in range(len(possibilityMatrix)):
                if x2 != x:
                    possibilityMatrix[x2][y] = False

print("Rule order", [r.name for r in sorted(fieldRules, key=lambda r: r.idx)])

print("my ticket", myTicket)

# Use the generated idx to compute the part2 solution

part2Prod = 1
for rule in fieldRules:
    if rule.name.startswith("departure"):
        pos = rule.idx
        part2Prod *= myTicket[pos]

print("Part 2 -", part2Prod)

# first try - too low => !! I used + instead of *