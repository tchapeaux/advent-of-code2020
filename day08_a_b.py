import utils
import subprocess

DAY = 8
subprocess.run(["fetch_my_input_once.bat", str(DAY)])

# utils.getRawInput(f"day{DAY:02}")
myInput = utils.getLinesInput(f"day{DAY:02}")
# utils.getCellsInput(f"day{DAY:02}")


class CPU:
    def __init__(self, program):
        self.program = program
        self.currentLineIdx = 0
        self.accumulator = 0
        self.hasRun = False

    def executeNextLine(self):
        if self.currentLineIdx == len(self.program):
            # program has finished
            return
        line = self.program[self.currentLineIdx]
        # print(f"EXEC {line}")
        instr, ope1 = line.split(" ")
        if instr == "nop":
            self.currentLineIdx += 1
        elif instr == "jmp":
            self.currentLineIdx += int(ope1)
        elif instr == "acc":
            self.accumulator += int(ope1)
            self.currentLineIdx += 1
        else:
            raise Exception(f"Unknown instruction {instr}")
        #
        # print(f"\tacc {self.accumulator} ip {self.currentLineIdx}")

    def loop(self):
        already_visited = set()
        while self.currentLineIdx not in already_visited:
            already_visited.add(self.currentLineIdx)
            self.executeNextLine()

        self.hasRun = True

    def hasTerminated(self):
        if not self.hasRun:
            raise Exception("Please run first!")
        return self.currentLineIdx == len(self.program)


myCpu = CPU(myInput)
myCpu.loop()
assert not myCpu.hasTerminated()
print("Part 1 - ", myCpu.accumulator)

# Part 2
# This will not be elegant: bruteforcing

for changedLineIdx in range(len(myInput)):
    # print(f"Testing line {changedLineIdx}")
    lines = myInput[:]  # copy
    # Do the transform
    if lines[changedLineIdx].startswith("nop"):
        lines[changedLineIdx] = lines[changedLineIdx].replace("nop", "jmp")
    if lines[changedLineIdx].startswith("jmp"):
        lines[changedLineIdx] = lines[changedLineIdx].replace("jmp", "nop")
    # Run the simulation
    myCpu = CPU(lines)
    myCpu.loop()
    if myCpu.hasTerminated():
        print("Part 2", f"Line {changedLineIdx}", f"Acc {myCpu.accumulator}")
        break
    else:
        pass
        # print("\tnope, ", myCpu.currentLineIdx)

# I had some troubles at first because I forgot that replace() does not change the string in place
# So I was testing the same program over and over and none were terminating
# Other than that, both parts were correct on the first submission to the AoC website