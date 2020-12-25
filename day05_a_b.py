import utils
import subprocess

DAY = 5
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

myInput = utils.getLinesInput(f"day{DAY:02}")


def decodePass(aPass):
    assert len(aPass) == 10
    # print(aPass)
    rowLow = 0
    rowUp = 127
    for i in range(7):
        # print(aPass[i])
        if aPass[i] == "F":
            rowUp = rowLow + (1 + rowUp - rowLow) / 2 - 1
        elif aPass[i] == "B":
            rowLow = rowLow + (1 + rowUp - rowLow) / 2
        # print("=>", rowLow, rowUp)
    assert rowLow == rowUp

    # print("Row", rowLow)

    seatLeft = 0
    seatRight = 7
    for i in range(7, 10):
        # print(aPass[i])
        if aPass[i] == "L":
            seatRight = seatLeft + (1 + seatRight - seatLeft) / 2 - 1
        elif aPass[i] == "R":
            seatLeft = seatLeft + (1 + seatRight - seatLeft) / 2
        # print("=>", seatLeft, seatRight)
    assert seatLeft == seatRight
    # print("Seat", seatLeft)

    return [int(rowLow), int(seatLeft)]


def getSeatId(aPass):
    [row, seat] = decodePass(aPass)
    return row * 8 + seat


assert decodePass("FBFBBFFRLR") == [44, 5]
assert decodePass("BFFFBBFRRR") == [70, 7]
assert decodePass("FFFBBBFRRR") == [14, 7]
assert decodePass("BBFFBBFRLL") == [102, 4]

assert getSeatId("FBFBBFFRLR") == 357
assert getSeatId("BFFFBBFRRR") == 567
assert getSeatId("FFFBBBFRRR") == 119
assert getSeatId("BBFFBBFRLL") == 820

myInputIds = [getSeatId(aPass) for aPass in myInput]
biggestSeatId = max(myInputIds)
print("Part 1 - Max is", biggestSeatId)

for seatId in range(biggestSeatId):
    if (
        seatId not in myInputIds
        and seatId - 1 in myInputIds
        and seatId + 1 in myInputIds
    ):
        print("Part 2 - Missing", seatId)
