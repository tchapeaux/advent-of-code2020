import utils
import re
import subprocess

DAY = 4
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

myInput = utils.getLinesInput(f"day{DAY:02}")
# myInput = utils.getLinesInput(f"example04_4_invalids")

# H4CK
# If the last line is not an empty line, add one
# This is because we use the empty lines to delimit the passports
if len(myInput[-1].strip()) > 0:
    myInput.append("")

REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def byr(x):
    return re.match(r"^\d{4}$", x) and "1920" <= x <= "2002"


def iyr(x):
    return re.match(r"^\d{4}$", x) and "2010" <= x <= "2020"


def eyr(x):
    return re.match(r"^\d{4}$", x) and "2020" <= x <= "2030"


def hgt(x):
    if x.endswith("cm"):
        return 150 <= int(x[:-2]) <= 193
    if x.endswith("in"):
        return 59 <= int(x[:-2]) <= 76
    return False


def hcl(x):
    return re.match(r"^#[\da-f]{6}$", x)


def ecl(x):
    return x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def pid(x):
    return re.match(r"^\d{9}$", x)


def cid(x):
    return True


VALIDATION_RULES = {
    "byr": byr,
    "iyr": iyr,
    "eyr": eyr,
    "hgt": hgt,
    "hcl": hcl,
    "ecl": ecl,
    "pid": pid,
    "cid": cid,
}

part1 = 0
part2 = 0
currentPassportFields = {}
# Go through input
for i in range(len(myInput)):
    # print("LINE", i, myInput[i])
    line = myInput[i]
    if len(line.strip()) == 0:
        # Empty line => End of passport: check if valid then reset
        print("password was", currentPassportFields)
        part1Checks = [field in currentPassportFields for field in REQUIRED_FIELDS]
        if all(part1Checks):
            part1 += 1
            print("Part 1 Valid!")

            part2Checks = [
                VALIDATION_RULES[key](value)
                for (key, value) in currentPassportFields.items()
            ]

            # DEBUG
            # for (key, value) in currentPassportFields.items():
            #    print(key)
            #    print(VALIDATION_RULES[key](value))

            if all(part2Checks):
                print("Part 2 Valid!")
                part2 += 1
        currentPassportFields = {}
    else:
        # Non-empty line => password line:
        # check which fields are presents and add to current passport
        words = line.strip().split(" ")
        for w in words:
            pre, suf = w.split(":")
            currentPassportFields[pre] = suf

print("PART 1 - Found", part1, "valid passwords")

# First try was off by one
# Because I forgot to count the last line (see H4CK above)

print("PART 2 - Found", part2, "valid passwords")

# First try was not correct because I used < and > for "at least" and "at most"
# instead of <= and >=
