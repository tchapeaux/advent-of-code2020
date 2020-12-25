import utils
import subprocess
import re

DAY = 14
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

memory = {}
mask = "X" * 36
MEM_REGEX = r"^mem\[(\d+)\] = (\d+)$"

# Part 1

currentAndMask = 0xFFFFFFFF
currentOrMask = 0x0


def updateAndOrMasks(mask):
    currentAndMask = int("0b" + "".join(["0" if c == "0" else "1" for c in mask]), 2)
    currentOrMask = int("0b" + "".join(["1" if c == "1" else "0" for c in mask]), 2)
    return (currentAndMask, currentOrMask)


for line in myInput:
    if line.startswith("mask = "):
        mask = line[len("mask = ") :]
        (currentAndMask, currentOrMask) = updateAndOrMasks(mask)
    elif line.startswith("mem["):
        m = re.search(MEM_REGEX, line)
        assert m
        addr, value = m.groups()
        addr = int(addr)
        value = int(value)
        value &= currentAndMask
        value |= currentOrMask
        memory[addr] = value

print("Part 1 -", sum([val for val in memory.values()]))

# Now Part 2
# I first tried to do it with bitwise operators but it took forever to run for some reason
# So I recoded with string operator and got a result in less than a second
# Not sure if the perf boost is because of string operator or just the rewrite fixing a bug

# Uncomment for example input
"""
myInput = [
    "mask = 000000000000000000000000000000X1001X",
    "mem[42] = 100",
    "mask = 00000000000000000000000000000000X0XX",
    "mem[26] = 1",
]
#"""

# Reset variables
memory = {}


def getAllReplacements(addrWithFloating):
    # Take a string with X's in it
    # Return all possible replacements of the X by 1 and 0
    if not "X" in addrWithFloating:
        yield addrWithFloating
    else:
        firstXIdx = addrWithFloating.index("X")
        beforeFirstX = addrWithFloating[:firstXIdx]
        afterFirstX = addrWithFloating[firstXIdx + 1 :]
        for possibleAfters in getAllReplacements(afterFirstX):
            yield beforeFirstX + "0" + possibleAfters
            yield beforeFirstX + "1" + possibleAfters


def getAllAddresses(address, mask):
    # print(bin(address).zfill(38))

    # We construct the new address with string operations
    # I'm sure there is a clever binary operation way of doing it as well
    newAddress = []
    for idx in range(36):
        if mask[idx] == "X":
            newAddress.append("X")
        elif mask[idx] == "1":
            newAddress.append("1")
        else:
            assert mask[idx] == "0"
            addressDigit = (address >> (35 - idx)) & 1
            newAddress.append(str(addressDigit))

    # print("2 " + "".join(newAddress))
    # print("m " + mask)

    replacements = list(getAllReplacements("".join(newAddress)))
    return replacements


for idx, line in enumerate(myInput):
    print(idx, "/", len(myInput))
    if line.startswith("mask = "):
        mask = line[len("mask = ") :]
        # print("Mask is now", mask)
    elif line.startswith("mem["):
        m = re.search(MEM_REGEX, line)
        assert m
        addr, value = m.groups()
        # print("Memory line", addr, value)
        addr = int(addr)
        value = int(value)

        addressesToWrite = set(getAllAddresses(addr, mask))
        # print("Must write in", addressesToWrite)
        for addrToWrite in addressesToWrite:
            # print("Write", value, "to", int(addrToWrite, 2))
            memory[int(addrToWrite, 2)] = value

print("Part 2 -", sum([val for val in memory.values()]))

# Some stupid errors I made:
# Confusing addr and address variable (naming is important people!!)
# range(len(35)) instead of range(len(36))