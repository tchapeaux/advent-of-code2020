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


def inBounds(table, x, y):
    return y >= 0 and y < len(table) and x >= 0 and x < len(table[y])


def getFirstSeenIn8Directions(table, x, y):
    assert 0 <= y < len(table)
    assert 0 <= x < len(table[y])
    # print("Check", x, y)
    DIRECTIONS = [
        # x, y
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]
    for (dx, dy) in DIRECTIONS:
        # print("\tDIR", dx, dy)
        # Travel in the direction path
        cx, cy = x + dx, y + dy
        while inBounds(table, cx, cy) and table[cy][cx] == FLOOR:
            cx += dx
            cy += dy
            # print("\t\tcx cy", cx, cy)
            if not inBounds(table, cx, cy):
                break
        if not inBounds(table, cx, cy):
            continue
        yield (cx, cy)


# Part 2 - simulate at infinity until no change
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
            for (xN, yN) in getFirstSeenIn8Directions(currentGrid, x, y):
                if currentGrid[yN][xN] == OCCUPIED:
                    occupiedNeighborCount += 1
            if cell == OCCUPIED and occupiedNeighborCount >= 5:
                newGrid[y][x] = EMPTY
                hasChanged = True
                # print("Change!", y, x, currentGrid[y][x], newGrid[y][x])
            if cell == EMPTY and occupiedNeighborCount == 0:
                newGrid[y][x] = OCCUPIED
                hasChanged = True
                # print("Change!", y, x, currentGrid[y][x], newGrid[y][x])

    print("Tick", tick)
    utils.printCells(newGrid)
    currentGrid = newGrid

print(
    "Part 2 - ",
    sum([sum(1 for cell in row if cell == OCCUPIED) for row in currentGrid]),
)
print("after", tick - 1, "ticks")
