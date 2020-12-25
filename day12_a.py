import utils
import math
import subprocess

DAY = 12
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")


def degToRad(x):
    return x * math.pi / 180


currentX = 0
currentY = 0
direction = 0  # EAST

# example input
# myInput = ["F10", "N3", "F7", "R90", "F11"]

for idx, line in enumerate(myInput):
    instr = line[0]
    value = int(line[1:])
    if instr == "N":
        currentY += value
    if instr == "S":
        currentY -= value
    if instr == "E":
        currentX += value
    if instr == "W":
        currentX -= value
    if instr == "L":
        direction += degToRad(value)
    if instr == "R":
        direction -= degToRad(value)
    if instr == "F":
        currentX += value * math.cos(direction)
        currentY += value * math.sin(direction)
    print("Step", idx, line, instr, value)
    print(currentX, currentY, direction % (2 * math.pi))


print("Part 1", abs(currentX) + abs(currentY))

# First try error: two consecutive errors
# One: forgot to multiply by value in the F case
# Two: F considered North as positive, and N/S considered the opposite