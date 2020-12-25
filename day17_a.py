import utils
import subprocess

DAY = 17
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

ACTIVE = "#"
INACTIVE = "."


class Grid3DBool:
    def __init__(self):
        self.cells = {}
        self.tick = 0

    def get(self, x, y, z):
        if x not in self.cells:
            return False
        if y not in self.cells[x]:
            return False
        if z not in self.cells[x][y]:
            return False
        assert self.cells[x][y][z] is True
        return self.cells[x][y][z]

    def set(self, x, y, z, value):
        if x not in self.cells:
            self.cells[x] = {}
        if y not in self.cells[x]:
            self.cells[x][y] = {}
        if value is True:
            self.cells[x][y][z] = True
        elif value is False:
            if z in self.cells[x][y]:
                del self.cells[x][y][z]
        else:
            raise Exception(f"Tried to set value {value}")

    def neighborsCoord(self, x, y, z):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                    yield (x + dx, y + dy, z + dz)

    def doTick(self):
        nextTick = Grid3DBool()
        # Go through all active cells
        # Update them in the new tick grid
        # And mark inactive cells that are neighbors
        inactiveCloseCells = set()
        for x in self.cells:
            for y in self.cells[x]:
                for z in self.cells[x][y]:
                    neighCoord = self.neighborsCoord(x, y, z)
                    activeNeighCount = 0
                    for (x2, y2, z2) in neighCoord:
                        if self.get(x2, y2, z2):
                            activeNeighCount += 1
                        else:
                            inactiveCloseCells.add((x2, y2, z2))
                    if 2 <= activeNeighCount <= 3:
                        nextTick.set(x, y, z, True)
        # Go through inactive cells that are close to active cells
        # And update them in the new tick grid
        for (x, y, z) in inactiveCloseCells:
            neighCoord = self.neighborsCoord(x, y, z)
            activeNeighCount = 0
            for (x2, y2, z2) in neighCoord:
                if self.get(x2, y2, z2):
                    activeNeighCount += 1
            if activeNeighCount == 3:
                nextTick.set(x, y, z, True)

        self.tick += 1
        self.cells = nextTick.cells

    def nbOfActive(self):
        return sum(
            [
                sum(
                    [
                        sum([1 if value else 0 for value in line.values()])
                        for line in plane.values()
                    ]
                )
                for plane in self.cells.values()
            ]
        )


# Parse input
# Assume top-left is x,y,z = 0,0,0

grid = Grid3DBool()
for y, line in enumerate(myInput):
    for x, cell in enumerate(line):
        val = cell == ACTIVE
        grid.set(x, y, 0, val)

grid.doTick()
grid.doTick()
grid.doTick()
grid.doTick()
grid.doTick()
grid.doTick()

print("Part 1", grid.nbOfActive())