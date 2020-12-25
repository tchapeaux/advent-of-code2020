import utils
import subprocess

DAY = 9
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

myInput = [int(x) for x in myInput]

PREAMBLE_SIZE = 25


def isSumOfAny2(presumed_sum, candidates):
    # returns True if any 2 different elements in candidates sum to presumed_sum
    for idx1, x1 in enumerate(candidates):
        for idx2, x2 in enumerate(candidates):
            if idx1 == idx2:
                continue
            if x1 + x2 == presumed_sum:
                return True
    return False


# Loop the list to find invalid num
# Which is the first to not be a sum of 2 numbers in its preamble
for idx, currentNum in enumerate(myInput):
    if idx < PREAMBLE_SIZE:
        continue
    candidates = myInput[idx - PREAMBLE_SIZE : idx]
    if not isSumOfAny2(currentNum, candidates):
        invalidNum = currentNum
        print("Part 1", invalidNum)
        break

# Loop the list to find the encryption weakness
# Which is a continuous set of numbers which add up to the invalid num
for idxStart, currentNum in enumerate(myInput):
    if currentNum >= invalidNum:
        continue
    # Investigate all sets starting here
    # make it grow until either you reach invalidNum, you go over it, or you reach the end
    currentSum = currentNum
    for idxEnd in range(idxStart + 1, len(myInput)):
        newNum = myInput[idxEnd]
        currentSum += newNum
        if currentSum == invalidNum:
            print("Part 2", myInput[idxStart] + myInput[idxEnd])
        elif currentSum > invalidNum:
            break
