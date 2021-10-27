from math import floor

class Program:
    def __init__(self, text):
        self.full, self.data, self.pointers = format_prog(text)

    def __getitem__(self, item):
        return self.data[item]

    def test(self, test_file: str, raw_data: bool = False):
        out = """
\033[4mPass/Fail:\033[0m
Passed          : {passed}
Failed          : {failed}

\033[4mPassed tests:\033[0m
Min cycles      : {min_c}
Average cycles  : {ave_c}
Max cycles      : {max_c}
"""
        out += "\n\033[4mRaw data:\033[0m\n{raw}" if raw_data else ""
        res = []
        with open(test_file, "r") as f:
            whole_file = f.read().splitlines()
            num_tests = len(whole_file)
            for num, d in enumerate(whole_file):
                print("\r[{:<50}] {:0>5}/{}".format("*" * floor(50 * (num + 1) / num_tests), num + 1, num_tests), end="")
                name, inputs, outputs, max_cycles = d.split(";")
                inputs = [int(i) for i in inputs.split(",")]
                outputs = [int(i) for i in outputs.split(",")]
                res.append(self.single_test(inputs, outputs, name, int(max_cycles)))
        print(out.format(passed=(passed := sum([i for _, _, i in res])), failed=len(res) - passed,
                         min_c=min([i for _, i, _ in res]), max_c=max([i for _, i, _ in res]),
                         ave_c=sum([i for _, i, _ in res]) / len(res),
                         raw="\n".join(
                             [f"{test_name:<20} c={cycles:<4} p={pass_}" for test_name, cycles, pass_ in res])))

    def single_test(self, given: list, expected: list, test_name: str, max_cycles=50000) -> [int, bool]:
        def error(message):
            print(f"\nTest {test_name}\n{message}")
            return [test_name, cycles, False]

        break_conditions = {"BR": lambda: True, "BRP": lambda: acc > 0, "BRZ": lambda: acc == 0}
        given.reverse()
        line = 0
        cycles = 0
        acc = 0
        out = []
        while cycles < max_cycles:
            cmd, ptr = self.full[line]
            if cmd == "IN":
                try:
                    acc = given.pop()
                except IndexError:
                    return error("Tried input with none given")
            elif cmd == "LDA":
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                acc = self.data[ptr]
            elif cmd == "STO":
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                self.data[ptr] = acc
            elif cmd in ["BR", "BRZ", "BRP"]:
                if ptr not in self.pointers.keys():
                    return error(f"{ptr} does not exist as a pointer")
                if break_conditions[cmd]():
                    line = self.pointers[ptr]
                    cycles += 1
                    continue
            elif cmd == "ADD":
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                acc += self.data[ptr]
            elif cmd == "SUB":
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                acc -= self.data[ptr]
            elif cmd == "OUT":
                out.append(acc)
            elif cmd == "HLT":
                return [test_name, cycles, out == expected]
            elif cmd == "DAT":
                return error("Why are you trying to run data? Stop it. Get some help")
            else:
                return error(f"The fuck is this {cmd}?")
            line += 1
            cycles += 1


def format_prog(raw_text: str):
    pointers = {}
    data = {}
    full = []
    ln = 0
    for i in raw_text.splitlines():
        if i[0] == "#":
            continue
        else:
            temp = i.split("\t")
            if temp[-1].strip()[0] == "#":
                del temp[-1]
            if temp[1] == "DAT":
                data[temp[0]] = int(temp[2] if temp[2] else 0)
            elif temp[0] != "":
                pointers[temp[0]] = ln
            if len(temp) == 2:
                temp = [temp[0], temp[1], ""]
            elif len(temp) == 1:
                temp = [temp[0], "", ""]
            full.append(temp[1:])
            ln += 1
    return [full, data, pointers]
