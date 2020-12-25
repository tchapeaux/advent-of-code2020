import utils
import subprocess
import external_lcm
import math

DAY = 13
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

myInput = utils.getLinesInput(f"day{DAY:02}")

# example input
# myInput = ["939", "7,13,x,x,59,x,31,19"]

t0 = int(myInput[0])  # earliest possible time of departure
busses = [int(x) for x in myInput[1].split(",") if x != "x"]

print("t0", t0)
print("busses", busses)


def testBus(bus, t0):
    cur = bus
    while cur < t0:
        cur += bus
    return (cur, bus)


earliestAvailableDepartures = [testBus(b, t0) for b in busses]
(departureTime, busNb) = min(earliestAvailableDepartures)

print("Part 1", departureTime, busNb, (departureTime - t0) * busNb)
# First try was too high because I forgot to substract t0

# Part 2


print("== Part2 ==")

# Helper test functions


def isTickTheSolution(t):
    for (period, offset) in constraints:
        if (t + offset) % period > 0:
            return False
    return True


def testValues(period, offset):
    assert type(period) == int
    assert type(offset) == int
    # Test the value at each period with initial offset
    current = period
    tick = 0
    while True:
        # print("cur", current)
        if isTickTheSolution(current - offset):
            return current - offset

        if tick % 1000000 == 0:
            print("tick", tick, current)

        current += period
        tick += 1


constraints = [
    (int(x), int(idx)) for (idx, x) in enumerate(myInput[1].split(",")) if x != "x"
]

# This is probably an inefficient idea:
# I assume that the biggest a period is, the harder it is to meet the constraint
# So we try to meet the biggest constraints first
constraints = sorted(constraints, reverse=True)

# We iterate over the multiple and check the constraints one by one


maxPeriod = constraints[0][0]
maxPeriodOffset = constraints[0][1]
print("MaxPeriod", maxPeriod)
print("MaxPeriodOffset", maxPeriodOffset)


ARE_YOU_CRAZY_THIS_TAKES_TOO_LONG = True  # Bail out because this is the wrong approach
if not ARE_YOU_CRAZY_THIS_TAKES_TOO_LONG:
    print("Part 2 - ", testValues(maxPeriod, maxPeriodOffset))

# 1000 years later: Indeed this is not good.
# Guesstimation: this takes a few hours to reach the minimal value given by AoC (100000000000000)
# Let's try another approach
# (Some research on DuckDuckGo: "lcm with offsets")
# Oooooh... https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset
# I've added the code from StackOverflow to an external helper file (surely this is legal)
# So from this, we can derive the following function


def lcm_offset(a, aOffset, b, bOffset):
    # Returns when period a and period b with offsets are in sync and at which period it occurs
    period, phase = external_lcm.combine_phased_rotations(
        a, -aOffset % a, b, -bOffset % b
    )
    return period, -phase % period


# The problem here is a bit different BUT we can look at it from the other side
# I.e. if we go back through time, the problem is exactly as stated here, starting with
# an offset and finishing in sync

# If we have 2 different bus, we can combine them into a "meta-bus" with a different offset+period
# corresponding to the time the bus are in sync
# etc etc until all busses are combined


def doPart2(bussesList):
    constraints = [(int(x), int(idx)) for (idx, x) in enumerate(bussesList) if x != "x"]
    constraints = sorted(constraints, reverse=True)
    maxOffset = max([offset for (period, offset) in constraints])
    # Look at it in reverse in time
    # so t0 is the latest arrival and time goes backward
    reversedContraints = [
        (period, maxOffset - offset) for (period, offset) in constraints
    ]

    currentOffset, currentPeriod = 0, 1
    for (p, o) in reversedContraints:
        currentPeriod, currentOffset = lcm_offset(currentPeriod, currentOffset, p, o)

    # The found solution is at the end of the pattern
    # substract the max offset so it's the start
    # print(currentPeriod, currentOffset - maxOffset)
    return currentOffset - maxOffset


# Check with some of the given examples
assert doPart2("7,13,x,x,59,x,31,19".split(",")) == 1068781
assert doPart2("17,x,13,19".split(",")) == 3417
assert doPart2("67,7,59,61".split(",")) == 754018

print("Part 2 - ", doPart2(myInput[1].split(",")))

# This took many attempts to get right, mostly because my math was overly complex

# AFTERHOURS
# After looking at other people solution, I see now that alternatives are possible:
#  Use the Chinese Remainder Theorem
#  Search by max period first, and when you find a correct match, use the LCM as steps
