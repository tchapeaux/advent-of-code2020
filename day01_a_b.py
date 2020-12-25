import utils

myInput = utils.getLinesInput("day01")
myInput = [int(x) for x in myInput]

print("Part 1")
# Find which pair of numbers add up to 2020
for idxA, numbA in enumerate(myInput):
    for idxB, numbB in enumerate(myInput):
        if idxA == idxB:
            continue
        if numbA + numbB == 2020:
            print("Found!", numbA, numbB, numbA * numbB)

print("Part 2")
# Same question but for a set of three
for idxA, numbA in enumerate(myInput):
    for idxB, numbB in enumerate(myInput):
        for idxC, numbC in enumerate(myInput):
            if idxA == idxB or idxB == idxC or idxA == idxC:
                continue
            if numbA + numbB + numbC == 2020:
                print("Found!", numbA, numbB, numbC, numbA * numbB * numbC)
