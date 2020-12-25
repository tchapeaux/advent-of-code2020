import utils
import subprocess

DAY = 17
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

ACTIVE = "#"
INACTIVE = "."

# PART 2
# This one has FOUR DIMENSIONS
# But the code will remain mostly the same


class Grid3DBool:
    def __init__(self):
        self.cells = {}
        self.tick = 0

    def get(self, x, y, z, w):
        if x not in self.cells:
            return False
        if y not in self.cells[x]:
            return False
        if z not in self.cells[x][y]:
            return False
        if w not in self.cells[x][y][z]:
            return False
        assert self.cells[x][y][z][w] is True
        return self.cells[x][y][z][w]

    def set(self, x, y, z, w, value):
        if x not in self.cells:
            self.cells[x] = {}
        if y not in self.cells[x]:
            self.cells[x][y] = {}
        if z not in self.cells[x][y]:
            self.cells[x][y][z] = {}
        if value is True:
            self.cells[x][y][z][w] = True
        elif value is False:
            if w in self.cells[x][y][z]:
                del self.cells[x][y][z][w]
        else:
            raise Exception(f"Tried to set value {value}")

    def neighborsCoord(self, x, y, z, w):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    for dw in [-1, 0, 1]:
                        if dx == dy == dz == dw == 0:
                            continue
                        yield (x + dx, y + dy, z + dz, w + dw)

    def doTick(self):
        nextTick = Grid3DBool()
        # Go through all active cells
        # Update them in the new tick grid
        # And mark inactive cells that are neighbors
        inactiveCloseCells = set()
        for x in self.cells:
            for y in self.cells[x]:
                for z in self.cells[x][y]:
                    for w in self.cells[x][y][z]:
                        neighCoord = self.neighborsCoord(x, y, z, w)
                        activeNeighCount = 0
                        for (x2, y2, z2, w2) in neighCoord:
                            if self.get(x2, y2, z2, w2):
                                activeNeighCount += 1
                            else:
                                inactiveCloseCells.add((x2, y2, z2, w2))
                        if 2 <= activeNeighCount <= 3:
                            nextTick.set(x, y, z, w, True)
        # Go through inactive cells that are close to active cells
        # And update them in the new tick grid
        for (x, y, z, w) in inactiveCloseCells:
            neighCoord = self.neighborsCoord(x, y, z, w)
            activeNeighCount = 0
            for (x2, y2, z2, w2) in neighCoord:
                if self.get(x2, y2, z2, w2):
                    activeNeighCount += 1
            if activeNeighCount == 3:
                nextTick.set(x, y, z, w, True)

        self.tick += 1
        print("Tick", self.tick)
        self.cells = nextTick.cells

    def nbOfActive(self):
        return sum(
            [
                sum(
                    [
                        sum(
                            [
                                sum([1 if value else 0 for value in line.values()])
                                for line in plane.values()
                            ]
                        )
                        for plane in hyperplane.values()
                    ]
                )
                for hyperplane in self.cells.values()
            ]
        )


# Parse input
# Assume top-left is x,y,z = 0,0,0

grid = Grid3DBool()
for y, line in enumerate(myInput):
    for x, cell in enumerate(line):
        val = cell == ACTIVE
        grid.set(x, y, 0, 0, val)

grid.doTick()
grid.doTick()
grid.doTick()
grid.doTick()
grid.doTick()
grid.doTick()

print("Part 2", grid.nbOfActive())