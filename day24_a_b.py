import utils
import subprocess

DAY = 24
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

# Example input
# myInput = utils.getLinesInput(f"example24")


EAST = "e"
WEST = "w"
SOUTHEAST = "se"
SOUTHWEST = "sw"
NORTHEAST = "ne"
NORTHWEST = "nw"

ALL_DIRECTIONS = [
    EAST,
    WEST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHEAST,
    NORTHWEST,
]


def parseLine(line):
    directions = []
    idx = 0
    while idx < len(line):
        if line[idx] == EAST:
            directions.append(EAST)
            idx += 1
        elif line[idx] == WEST:
            directions.append(WEST)
            idx += 1
        elif line[idx] == "n":
            if line[idx + 1] == EAST:
                directions.append(NORTHEAST)
            elif line[idx + 1] == WEST:
                directions.append(NORTHWEST)
            idx += 2
        elif line[idx] == "s":
            if line[idx + 1] == EAST:
                directions.append(SOUTHEAST)
            elif line[idx + 1] == WEST:
                directions.append(SOUTHWEST)
            idx += 2
    return directions


tileInstructions = [parseLine(line) for line in myInput]

# Helper functions
# Assume a hexagonal grid with odd-r horizontal layout
# terminology is from https://www.redblobgames.com/grids/hexagons/#coordinates-offset


def getNeighbor(x, y, direction):
    if direction == EAST:
        return (x + 1, y)
    if direction == WEST:
        return (x - 1, y)
    isRowEven = y % 2 == 0
    if direction == NORTHEAST:
        return (x if isRowEven else x + 1, y - 1)
    if direction == NORTHWEST:
        return (x - 1 if isRowEven else x, y - 1)
    if direction == SOUTHEAST:
        return (x if isRowEven else x + 1, y + 1)
    if direction == SOUTHWEST:
        return (x - 1 if isRowEven else x, y + 1)


def getTileFromInstructions(instructions):
    """ Follow the directions from 0,0 to arrive at a tile """
    currentTile = (0, 0)
    for direction in instructions:
        currentTile = getNeighbor(currentTile[0], currentTile[1], direction)
    return currentTile


# Keep track of marked (flipped) tiles
# Warning: tiles can be flipped twice (we remove them from the set in that case)
markedTiles = set()

for tileToFlipInstr in tileInstructions:
    tileToFlip = getTileFromInstructions(tileToFlipInstr)
    if tileToFlip in markedTiles:
        markedTiles.remove(tileToFlip)
    else:
        markedTiles.add(tileToFlip)

print("Part 1", len(markedTiles))

# For Part 2, we need to do a game-of-life in our hex grid. Fun!

blackTiles = markedTiles  # rename


def yieldAllNeighbors(x, y):
    for direction in ALL_DIRECTIONS:
        yield getNeighbor(x, y, direction)


def doTick(currentBlackTiles):
    # We will do this in 2 parts:
    # for all black tiles, check if they are still black and keep track of their neighbors
    # for all white neighbors, check if they need to be flipped

    newBlackTiles = set()
    allNeighborsOfBlacks = set()

    # Step 1 - check all current black tiles
    for tile in currentBlackTiles:
        countBlackNeighbors = 0
        for neigh in yieldAllNeighbors(tile[0], tile[1]):
            allNeighborsOfBlacks.add(neigh)
            if neigh in currentBlackTiles:
                countBlackNeighbors += 1

        if countBlackNeighbors > 0 and countBlackNeighbors <= 2:
            newBlackTiles.add(tile)

    # Step 2 - check all neighbors of current black tiles
    for tile in allNeighborsOfBlacks:
        # Only consider white neighbors
        if tile in currentBlackTiles:
            continue
        # count neighbors
        countBlackNeighbors = 0
        for neigh in yieldAllNeighbors(tile[0], tile[1]):
            if neigh in currentBlackTiles:
                countBlackNeighbors += 1

        if countBlackNeighbors == 2:
            newBlackTiles.add(tile)

    return newBlackTiles


# Do the simulation
for tick in range(100):
    blackTiles = doTick(blackTiles)
    print("Day", tick + 1, ":", len(blackTiles))

print("Part 2", len(blackTiles))

# First try was wrong because I initially inverted the condition for existing black tiles
# i.e. I was keeping them black when they needed to be flipped to white, and the opposite as well