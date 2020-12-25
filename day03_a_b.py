from math import prod
import utils

myInput = utils.getCellsInput("day03")
maxHeight = len(myInput)
inputWidth = len(myInput[0])

utils.printCells(myInput)


def exploreSlope(slopeX, slopeY):
    current = {"x": 0, "y": 0}
    treeCount = 0

    while current["y"] < maxHeight:
        if myInput[current["y"]][current["x"] % inputWidth] == "#":
            treeCount += 1
        current["x"] += slopeX
        current["y"] += slopeY
    return treeCount


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
part1Index = 1

treesInSlope = []

for idx, slop in enumerate(slopes):
    treeCount = exploreSlope(slop[0], slop[1])
    treesInSlope.append(treeCount)
    print("Slope", slop, "has", treesInSlope[idx], "trees")

print("Part 1", treesInSlope[part1Index])
print("Part 2", prod(treesInSlope))
