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


def rotatePoint(dX, dY, dAngle):
    # Rotate the point at (dX, dY) around (0, 0) by dAngle radians
    hypothenus = math.sqrt(dX * dX + dY * dY)
    curAngle = math.atan2(dY, dX)  # mind the order of args
    newAngle = curAngle + dAngle
    return (hypothenus * math.cos(newAngle), hypothenus * math.sin(newAngle))


currentX = 0
currentY = 0
waypointDX = 10  # relative to ship
waypointDY = 1  # relative to ship
direction = 0  # EAST

# example input
# myInput = ["F10", "N3", "F7", "R90", "F11"]


for idx, line in enumerate(myInput):
    instr = line[0]
    value = int(line[1:])
    if instr == "N":
        waypointDY += value
    if instr == "S":
        waypointDY -= value
    if instr == "E":
        waypointDX += value
    if instr == "W":
        waypointDX -= value
    if instr == "L":
        [waypointDX, waypointDY] = rotatePoint(waypointDX, waypointDY, degToRad(value))
    if instr == "R":
        [waypointDX, waypointDY] = rotatePoint(waypointDX, waypointDY, -degToRad(value))
    if instr == "F":
        currentX += value * waypointDX
        currentY += value * waypointDY
    print("Step", idx, line, instr, value)
    print(currentX, currentY, direction % (2 * math.pi))


print("Part 2", abs(currentX) + abs(currentY))
