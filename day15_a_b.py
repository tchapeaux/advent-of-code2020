import utils
import subprocess

DAY = 15
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

myInput = utils.getRawInput(f"day{DAY:02}")
# utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

# Example input
# myInput = "0,3,6"

print("Input: ", myInput)
starters = [int(x) for x in myInput.split(",")]


def findNthNumber(starters, n):
    # Will record the value said in order
    stepValues = []
    # Will record, for each value, at which steps it was said
    whenSpokenDict = {}

    def sayValue(step, val):
        stepValues.append(val)
        if val not in whenSpokenDict:
            whenSpokenDict[val] = [step]
        else:
            whenSpokenDict[val].append(step)

    step = 1
    while step <= n:

        if step <= len(starters):
            val = starters[step - 1]
            sayValue(step, val)
            # print(step, val)
            step += 1
            continue

        lastValueSaid = stepValues[-1]
        firstTimeSaid = len(whenSpokenDict[lastValueSaid]) == 1
        if firstTimeSaid:
            val = 0
            sayValue(step, val)
            # print(step, val)
        else:
            lastOccurence = whenSpokenDict[lastValueSaid][-2]
            val = (step - 1) - lastOccurence
            sayValue(step, val)
            # print(step, val)

        step += 1
    return stepValues[-1]


print("Part 1 ", findNthNumber(starters, 2020))
print("Part 2", findNthNumber(starters, 30000000))