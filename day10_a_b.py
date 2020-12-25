import utils
import subprocess

DAY = 10
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

myInput = [int(x) for x in myInput]

# I assume that there are no duplicates so let's check it
assert len(set(myInput)) == len(myInput)


# Add outlet (0)
myInput.append(0)
# Add device (always 3 higher than the max)
myInput.append(max(myInput) + 3)

# Sort
myInput = sorted(myInput)

diffCount = {1: 0, 2: 0, 3: 0}

for i in range(1, len(myInput)):
    prev = myInput[i - 1]
    cur = myInput[i]
    diff = cur - prev
    if diff not in diffCount:
        raise Exception(f"Found unexpected diff {diff}")
    diffCount[diff] += 1

print("Part 1 - ", diffCount[1] * diffCount[3])

# Part 2
# I like how in the instructions they are like "please don't bruteforce"

# I think there must be some sort of recursion
# - if the list is x = [A, B, C, D, E, F]
# - And the first choice is between A and B
# we have something like
#     nbChoices(x) = nbChoices(x[1:] + nbChoices(x[2:]))
# and
#     if len(x) == 1:
#         nbChoices == 1
# let's try it

# (after some time)
# WAIT
# doing it like ^ this I will do the same operation lots of time!!
# but I can store partial results!!

PARTIAL_RESULT_STORE = {}


def nbChoices(x, lastValue):
    assert len(x) == 0 or min(x) > lastValue
    # assume x is sorted
    possibleChoices = [c for c in x if 1 <= c - lastValue <= 3]
    assert 0 <= len(possibleChoices) <= 3

    if len(possibleChoices) == 0:
        return 1

    returnSum = 0
    for c in possibleChoices:
        if c not in PARTIAL_RESULT_STORE:
            idx = x.index(c)
            sublist = x[idx + 1 :]
            nbChoiceForC = nbChoices(sublist, c)
            PARTIAL_RESULT_STORE[c] = nbChoiceForC

        returnSum += PARTIAL_RESULT_STORE[c]
    return returnSum


print("Part 2 - ", nbChoices(myInput[1:], 0))