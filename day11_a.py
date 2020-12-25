import copy
import utils
import subprocess

DAY = 11
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
# utils.getLinesInput(f"day{DAY:02}")
myInput = utils.getCellsInput(f"day{DAY:02}")

# myInput = utils.getCellsInput("example11")

print("Tick 0")
utils.printCells(myInput)


FLOOR = "."
OCCUPIED = "#"
EMPTY = "L"


def getNeighborsCoord(table, x, y):
    assert 0 <= y < len(table)
    assert 0 <= x < len(table[y])
    if y > 0:
        if x > 0:
            yield (x - 1, y - 1)  # TOPLEFT
        yield (x, y - 1)  # TOP
        if x < len(table[y]) - 1:
            yield (x + 1, y - 1)  # TOPRIGHT

    if x > 0:
        yield (x - 1, y)  # MIDDLELEFT
    if x < len(table[y]) - 1:
        yield (x + 1, y)  # MIDDLERIGHT

    if y < len(table) - 1:
        if x > 0:
            yield (x - 1, y + 1)  # BOTTOMLEFT
        yield (x, y + 1)  # BOTTOM
        if x < len(table[y]) - 1:
            yield (x + 1, y + 1)  # BOTTOMRIGHT


# Part 1 - simulate at infinity until no change
currentGrid = copy.deepcopy(myInput)
tick = 0
hasChanged = True
while hasChanged:
    tick += 1
    hasChanged = False
    newGrid = copy.deepcopy(currentGrid)
    for y in range(len(currentGrid)):
        for x in range(len(currentGrid[y])):
            cell = currentGrid[y][x]
            if cell == "FLOOR":
                continue
            occupiedNeighborCount = 0
            for (xN, yN) in getNeighborsCoord(currentGrid, x, y):
                if currentGrid[yN][xN] == OCCUPIED:
                    occupiedNeighborCount += 1
            if cell == OCCUPIED and occupiedNeighborCount >= 4:
                newGrid[y][x] = EMPTY
                hasChanged = True
                # print("Change!", y, x, currentGrid[y][x], newGrid[y][x])
            if cell == EMPTY and occupiedNeighborCount == 0:
                newGrid[y][x] = OCCUPIED
                hasChanged = True
                # print("Change!", y, x, currentGrid[y][x], newGrid[y][x])

    print("Tick", tick)
    # utils.printCells(newGrid)
    currentGrid = newGrid

print(
    "Part 1 - ",
    sum([sum(1 for cell in row if cell == OCCUPIED) for row in currentGrid]),
)
print("after", tick - 1, "ticks")
