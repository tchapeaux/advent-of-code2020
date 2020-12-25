def getRawInput(filename):
    with open("inputs/" + filename + ".txt") as f:
        return f.read()


def getLinesInput(filename):
    rawInput = getRawInput(filename)
    return [l.strip() for l in rawInput.strip().split("\n")]


def getCellsInput(filename):
    linesInput = getLinesInput(filename)
    return [[c for c in l] for l in linesInput if len(l.strip()) > 0]


def printCells(table):
    for line in table:
        print("".join([str(l) for l in line]))


class Grid(object):
    def __init__(self):
        self._g = {}

    def get(self, x, y):
        if x not in self._g:
            return None
        if y not in self._g[x]:
            return None
        return self._g[x][y]

    def set(self, x, y, newVal):
        if x not in self._g:
            self._g[x] = {}
        self._g[x][y] = newVal


def manhattanDistance(x1, y1, x2, y2):
    # manhattan distance between (x1, y1) and (x2, y2)
    return abs(y2 - y1) + abs(x2 - x1)
