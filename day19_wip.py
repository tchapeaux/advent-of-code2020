import utils
import re
import subprocess
from dataclasses import dataclass

DAY = 19
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")

inputSeparator = myInput.index("")

rules = myInput[:inputSeparator]
messages = myInput[inputSeparator + 1 :]

allRules = {}


@dataclass
class Rule:
    """Represent a rule."""

    idx: int
    possibilities: list


def parseRule(rawRule):
    m = re.match(r"^(\d+):(.*)$", rawRule)
    ruleIndex, rest = m.groups()

    restWords = rest.strip().split(" ")
    # hardcode possibilities based on input inspection
    if len(restWords) == 1:
        if '"' in restWords[0]:
            return Rule(int(ruleIndex), [[restWords[0][1]]])
        return Rule(int(ruleIndex), [[int(restWords[0])]])
    if len(restWords) == 2:
        return Rule(int(ruleIndex), [[int(restWords[0]), int(restWords[1])]])
    if len(restWords) == 3:
        assert restWords[1] == "|"
        return Rule(int(ruleIndex), [[int(restWords[0])], [int(restWords[2])]])
    if len(restWords) == 5:
        assert restWords[2] == "|"
        poss1 = [int(restWords[0]), int(restWords[1])]
        poss2 = [int(restWords[3]), int(restWords[4])]
        return Rule(int(ruleIndex), [poss1, poss2])
    raise Exception(f"Could not parse rule {rawRule}")


for r in rules:
    rule = parseRule(r)
    allRules[rule.idx] = rule
    print("parsed", rule)

print(allRules)


# TBC....