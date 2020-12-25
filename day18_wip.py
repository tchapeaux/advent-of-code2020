import utils
import subprocess

DAY = 18
# subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")


class Operator:
    def __init__(self, symbol, left, right):
        self.symbol = symbol
        self.left = left
        self.right = right

    def compute(self):
        val1, val2 = None, None
        if type(self.left) == int:
            val1 = self.left
        elif type(self.left) == Operator:
            val1 = self.left.compute()

        if type(self.right) == int:
            val2 = self.right
        elif type(self.right) == Operator:
            val2 = self.right.compute()

        if symbol == "+":
            return val1 + val2
        if symbol == "*":
            return val1 * val2


def findClosingBracket(s, openingIdx):
    assert s[openingIdx] == "("
    curIdx = openingIdx + 1
    parenthesisStack = 1
    while curIdx < len(s):
        if s[curIdx] == "(":
            parenthesisStack += 1
        if s[curIdx] == ")":
            parenthesisStack -= 1
            if parenthesisStack == 0:
                return curIdx
        curIdx += 1
    raise Exception(f"Did not find the closing parenthesis in - {s}")


assert findClosingBracket("()", 0) == 1
assert findClosingBracket("(aaa(bb(c)bb)aaaaaa)", 0) == 19


def calculateString(s):
    words = s.split(" ")

    if len(words) == 1:
        return int(words[0])

    if words[0][0] == "(":
        # Find closing bracket
        closingIdx = findClosingBracket(s, 0)
        if closingIdx == len(s) - 1:
            return calculateString(s[1:-1])
        leftVal = calculateString(s[1:closingIdx])
        operator = s[closingIdx + 2]
        rightVal = calculateString(s[closingIdx + 4 :])
    else:
        leftVal = int(words[0])
        operator = words[1]
        rightVal = calculateString(" ".join(words[2:]))

    assert operator in "+*"
    if operator == "+":
        return leftVal + rightVal
    elif operator == "*":
        return leftVal * rightVal
    else:
        raise Exception(f"Unknown operator f{operator}")


assert calculateString("0") == 0
assert calculateString("(1 + 2 + 3)") == 6
assert calculateString("5 * (2 + 3)") == 25
print(calculateString("5 * 2 + 3"))
assert calculateString("5 * 2 + 3") == 13
