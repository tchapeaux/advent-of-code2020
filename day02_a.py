import re
import utils

myInput = utils.getLinesInput("day02")


def parseLine(line):
    lineRegex = r"(\d+)-(\d+) (\w): (\w*)"
    m = re.search(lineRegex, line)
    low, high, pattern, password = m.groups()
    return low, high, pattern, password


myInput = [parseLine(line) for line in myInput]


def islineCorrect(line):
    low, high, pattern, password = line
    return int(low) <= password.count(pattern) <= int(high)


for line in myInput:
    print(line, islineCorrect(line))

onlyCorrects = [line for line in myInput if islineCorrect(line)]
print(len(onlyCorrects))
