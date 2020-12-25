import utils
import subprocess

DAY = 6
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")


currentSet = set()
currentSum = 0
for lineIdx, line in enumerate(myInput):
    line = line.strip()
    for letter in line:
        currentSet.add(letter)
    if len(line) == 0 or lineIdx == len(myInput) - 1:
        currentSum += len(currentSet)
        currentSet = set()


print("Part 1 - Sum is", currentSum)

# First try was too high because I forgot to reset the set at each blank line

# Part 2
currentSet = set()
currentSum = 0
for lineIdx, line in enumerate(myInput):
    line = line.strip()
    if lineIdx == 0 or len(myInput[lineIdx - 1].strip()) == 0:
        currentSet = set([l for l in line])
    if len(line) == 0 or lineIdx == len(myInput) - 1:
        currentSum += len(currentSet)
        currentSet = set()
    else:
        currentSet = set([l for l in line if l in currentSet])

print("Part 2 - sum is", currentSum)

# First try was wrong because I was counting the empty lines separating the groups as answers
# (except the last one, so my answer was 1 and I thought it was a trick)
