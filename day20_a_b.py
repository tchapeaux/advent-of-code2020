import copy
import utils
import math
import re
import subprocess

DAY = 20
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# myInput = utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

# quick check
allIndices = [int(l[5:-1]) for l in myInput if "Tile" in l]
# print(max(allIndices), math.sqrt(max(allIndices)))
# print(len(allIndices), math.sqrt(len(allIndices)))
# oh so it seems the indices are random, and there are actually many less tiles

TILE_SIZE = 10
NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
GRID_SIZE = int(math.sqrt(len(allIndices)))

# fun fact
# I completely mess up x/y in this whole program
# but I mess it up consistently so the solution is still correct


class Tile:
    def __init__(self, idx, data=None):
        self.idx = int(idx)
        self.data = data or []
        self.connectors = {}

    def isComplete(self):
        return len(self.data) == TILE_SIZE and all(
            [len(row) == TILE_SIZE for row in self.data]
        )

    def addRow(self, row):
        assert len(row) == TILE_SIZE
        assert len(self.data) < TILE_SIZE
        self.data.append(row)

    def getConnectors(self):
        assert self.isComplete()
        if NORTH not in self.connectors:
            # Compute connectors only once
            self.connectors[NORTH] = "".join(self.data[0])
            self.connectors[SOUTH] = "".join(self.data[-1])
            self.connectors[EAST] = "".join([row[-1] for row in self.data])
            self.connectors[WEST] = "".join([row[0] for row in self.data])
        return self.connectors

    def flip(self):
        """ Return new Tile with flipped content """
        newTile = Tile(self.idx)
        newTile.data = [row[::-1] for row in self.data]
        newTile.connectors = {}  # will be recomputed when accessed
        return newTile

    def rotate(self):
        """ Return new Tile with content flipped 90° clockwise """
        newTile = Tile(self.idx)

        newTile.data = []
        for idx in range(TILE_SIZE):
            newRow = [row[idx] for row in self.data][::-1]
            newTile.data.append(newRow)

        newTile.connectors = {}  # will be recomputed when accessed
        return newTile

    def __repr__(self):
        reprStr = [f"Tile {self.idx}:"]
        for idx in range(TILE_SIZE):
            reprStr.append("".join(self.data[idx]))
        return "\n".join(reprStr)


# Parse input

allTiles = {}
currentTile = None

for idx, line in enumerate(myInput):
    if line.startswith("Tile"):
        assert currentTile is None
        tileIdx = int(line[5:-1])
        currentTile = Tile(idx=tileIdx)
    if line.startswith(".") or line.startswith("#"):
        currentTile.addRow([c for c in line])
    if len(line) == 0 or idx == len(myInput) - 1:
        assert currentTile.isComplete()
        allTiles[currentTile.idx] = currentTile
        currentTile = None


assert len(allTiles.keys()) == len(allIndices)
assert all([t.isComplete() for t in allTiles.values()])
assert all([t.idx > 0 for t in allTiles.values()])

print("Initial parsing OK")


# Generate flipped and rotated versions of all Tiles

# 0° and 90°
PLAIN = [allTiles, {idx: allTiles[idx].rotate() for idx in allTiles.keys()}]
# 180°
PLAIN.append({idx: PLAIN[-1][idx].rotate() for idx in allTiles.keys()})
# 270°
PLAIN.append({idx: PLAIN[-1][idx].rotate() for idx in allTiles.keys()})

# Same for FLIPPED
FLIPPED = [{idx: allTiles[idx].flip() for idx in allTiles.keys()}]
FLIPPED.append({idx: FLIPPED[-1][idx].rotate() for idx in allTiles.keys()})
FLIPPED.append({idx: FLIPPED[-1][idx].rotate() for idx in allTiles.keys()})
FLIPPED.append({idx: FLIPPED[-1][idx].rotate() for idx in allTiles.keys()})

ALL_TILES_BIN = [
    PLAIN[0],
    PLAIN[1],
    PLAIN[2],
    PLAIN[3],
    FLIPPED[0],
    FLIPPED[1],
    FLIPPED[2],
    FLIPPED[3],
]

print("Pre-compute alternate tiles OK")

# General idea for the rest:
# Try to find an arrangement greedily by placing the tiles from all buckets and backtracking (also use the pre-computation to speed up)


class TileGrid:
    def __init__(self, gridSize):
        self.data = [[None] * gridSize for _ in range(gridSize)]
        self.gridSize = gridSize

    def getNeighbors(self, x, y):
        neigh = {}
        if x > 0:
            neigh[NORTH] = self.data[x - 1][y]
        if x < self.gridSize - 1:
            neigh[SOUTH] = self.data[x + 1][y]
        if y > 0:
            neigh[WEST] = self.data[x][y - 1]
        if y < self.gridSize - 1:
            neigh[EAST] = self.data[x][y + 1]
        return neigh

    def placeTile(self, x, y, tile):
        """ Return True if placed successfully, False otherwise """
        assert self.data[x][y] is None
        neighs = self.getNeighbors(x, y)
        tileConnectors = tile.getConnectors()
        for direction, neigh in neighs.items():
            if not neigh:
                continue
            neighConnectors = neigh.getConnectors()
            if direction == NORTH and tileConnectors[NORTH] != neighConnectors[SOUTH]:
                return False
            if direction == SOUTH and tileConnectors[SOUTH] != neighConnectors[NORTH]:
                return False
            if direction == EAST and tileConnectors[EAST] != neighConnectors[WEST]:
                return False
            if direction == WEST and tileConnectors[WEST] != neighConnectors[EAST]:
                return False
        self.data[x][y] = tile
        return True

    def isIdxPlaced(self, idx):
        for row in self.data:
            if any([tile.idx == idx for tile in row if tile]):
                return True
        return False


grid = TileGrid(GRID_SIZE)

# Recursive function for the backtracking
def tryTile(grid, curX, curY, tile):
    placementSuccess = grid.placeTile(curX, curY, tile)
    if not placementSuccess:
        return False
    if curX == GRID_SIZE - 1 and curY == GRID_SIZE - 1:
        print("Part 1")
        print(
            grid.data[0][0].idx
            * grid.data[0][-1].idx
            * grid.data[-1][0].idx
            * grid.data[-1][-1].idx
        )
        return True
    nextX = curX
    nextY = curY + 1
    if nextY == grid.gridSize:
        nextX += 1
        nextY = 0

    # Refactor:
    # This could be optimized by pre-computing the connections between slides
    # So we only check tiles that are known to connect
    # However we find the solution in less than 2s with pypy3 so good enough
    for _bin in ALL_TILES_BIN:
        for nextTile in [t for t in _bin.values() if not grid.isIdxPlaced(t.idx)]:
            result = tryTile(grid, nextX, nextY, nextTile)
            if result:
                return True
    # If we reach here, no tile was successful
    # remove tile
    grid.data[curX][curY] = None
    return False


print("Greedily searching an arrangement")
FOUND = False
# This could be refactored to avoid the duplicate code for the first iteration
for _bin in ALL_TILES_BIN:
    if FOUND:
        break

    for tile in _bin.values():
        r = tryTile(grid, 0, 0, tile)
        if r:
            FOUND = True
            break

# Recreate the map as one big matrix (list of list)
myMapWithBorders = []
for i in range(GRID_SIZE * TILE_SIZE):
    newRow = []
    for j in range(GRID_SIZE * TILE_SIZE):
        tile_x = int(math.floor(i / TILE_SIZE))
        in_tile_x = i % TILE_SIZE
        tile_y = int(math.floor(j / TILE_SIZE))
        in_tile_y = j % TILE_SIZE
        newRow.append(grid.data[tile_x][tile_y].data[in_tile_x][in_tile_y])
    myMapWithBorders.append(newRow)

# Remove tile borders
def _indicesToRemove():
    current = 0
    while current < TILE_SIZE * GRID_SIZE:
        yield current
        current += TILE_SIZE - 1
        yield current
        current += 1


indicesToRemove = list(_indicesToRemove())


myMap = []
for idx, row in enumerate(myMapWithBorders):
    if idx not in indicesToRemove:
        newRow = []
        for idx2, val in enumerate(row):
            if idx2 not in indicesToRemove:
                newRow.append(val)
        myMap.append(newRow)


PATTERN = [
    [c for c in "                  # "],
    [c for c in "#    ##    ##    ###"],
    [c for c in " #  #  #  #  #  #   "],
]

# Take note of all relative coords to check for the pattern to be present
patternChecks = []
for x, rowPattern in enumerate(PATTERN):
    for y, val in enumerate(rowPattern):
        if val == "#":
            patternChecks.append((x, y))

print("Number of hashes before pattern checking")
nbOfHashes = sum([sum([1 for val in row if val == "#"]) for row in myMap])
print(nbOfHashes)


def checkForPatterns(myMap, patternChecks):
    """ return the number of # not in pattern (as per part 2 spec) """
    for x, row in enumerate(myMap):
        for y, _ in enumerate(row):
            isPattern = True
            for dx, dy in patternChecks:
                if x + dx >= len(myMap) or y + dy >= len(myMap):
                    isPattern = False
                    break
                if myMap[x + dx][y + dy] == ".":
                    isPattern = False
                    break
            if isPattern:
                # Mark all # as O
                for dx, dy in patternChecks:
                    myMap[x + dx][y + dy] = "O"

    return sum([sum([1 for val in row if val == "#"]) for row in myMap])


# Helper functions to generate variants


def rotateMap(myMap):
    newMap = []
    for idx in range(len(myMap)):
        newRow = [row[idx] for row in myMap][::-1]
        newMap.append(newRow)
    return newMap


def flipMap(myMap):
    return [row[::-1] for row in myMap]


# Let's check for patterns in un-flipped maps
for nbOfRotation in range(4):
    print(f"Test with {nbOfRotation} rotations")
    newMap = copy.deepcopy(myMap)
    for _ in range(nbOfRotation):
        newMap = rotateMap(newMap)
    newNbOfHashes = checkForPatterns(newMap, patternChecks)
    if newNbOfHashes != nbOfHashes:
        print("\tPart 2", newNbOfHashes, "<=======")
    else:
        print("\tNo pattern found")

# Let's check with flips
for nbOfRotation in range(4):
    print(f"Test flipped with {nbOfRotation} rotations")
    newMap = flipMap(myMap)
    for _ in range(nbOfRotation):
        newMap = rotateMap(newMap)
    newNbOfHashes = checkForPatterns(newMap, patternChecks)
    if newNbOfHashes != nbOfHashes:
        print("\tPart 2", newNbOfHashes)
    else:
        print("\tNo pattern found")
