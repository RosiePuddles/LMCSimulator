from math import floor
import time
from math import inf


class Program:
    def __init__(self, text):
        self.full, self.data, self.pointers = format_prog(text)

    def __getitem__(self, item):
        return self.data[item]

    def test(self, test_file: str, raw_data: bool = False):
        out = """
\033[4mGeneral:\033[0m
Passed          : {passed}
Failed          : {failed}
Pass rate       : {pass_rate:.2f}%
Mailboxes       : {mail}
Time per test   : {tpt:.3f}ns

\033[4mPassed tests:\033[0m
Min cycles      : {min_c}
Max cycles      : {max_c}
Average cycles  : {ave_c:.3f}
Cycles spread   : {sd:.5f}
"""
        out += "\n\033[4mRaw data:\033[0m\n{raw}" if raw_data else ""
        res = []
        with open(test_file, "r") as f:
            whole_file = f.read().splitlines()
            num_tests = len(whole_file)
            total_time = -time.time_ns()
            for num, d in enumerate(whole_file):
                print("\r[{:<50}] {:>5}/{:<5} ({:>3}%)".format("*" * floor(50 * (num + 1) / num_tests), num + 1,
                                                               num_tests, floor(100 * (num + 1) / num_tests)), end="")
                name, inputs, outputs, max_cycles = d.split(";")
                inputs = [int(i) for i in inputs.split(",")]
                outputs = [int(i) for i in outputs.split(",")]
                res.append(self.single_test(inputs, outputs, name, int(max_cycles)))
            total_time += time.time_ns()
        print(out.format(passed=(passed := sum([i for _, _, i in res])), failed=len(res) - passed, pass_rate=100 * passed / len(res),
                         mail=len(self.full), tpt=total_time / num_tests,
                         min_c=min([i for _, i, _ in res]), max_c=max([i for _, i, _ in res]),
                         ave_c=(mean := sum([i for _, i, _ in res]) / len(res)),
                         sd=(sum([(mean - i) ** 2 for _, i, _ in res]) / len(res)) ** 0.5,
                         raw="\n".join(
                             [f"{test_name:<20} c={cycles:<4} p={pass_}" for test_name, cycles, pass_ in res])))

    def run(self, given: list[int] = [], print_out_as_run: bool = True, cycle_limit: int = inf) -> [list[int], int]:
        given.reverse()
        break_conditions = {"BR": lambda: True, "BRP": lambda: not neg, "BRZ": lambda: acc == 0}
        line = 0
        cycles = 0
        acc = 0
        actual_acc = 0
        neg = False
        out = []
        while cycles < cycle_limit:
            def error(message):
                print(f"\nError:\n{message}")
                return [out, cycles]

            cycles += 1
            cmd, ptr = self.full[line]
            if cmd == "IN":
                try:
                    acc = given.pop()
                    actual_acc = acc
                except IndexError:
                    return error("Tried input with none given")
            elif cmd == "LDA":
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                actual_acc = self.data[ptr]
                acc = actual_acc
            elif cmd == "STO":
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                self.data[ptr] = acc
            elif cmd in ["BR", "BRZ", "BRP"]:
                if ptr not in self.pointers.keys():
                    return error(f"{ptr} does not exist as a pointer")
                if break_conditions[cmd]():
                    line = self.pointers[ptr]
                    continue
            elif cmd in ["ADD", "SUB"]:
                if ptr not in self.data.keys():
                    return error(f"{ptr} is an unknown register")
                actual_acc += (1 if cmd == "ADD" else -1) * self.data[ptr]
                neg = actual_acc < 0
                actual_acc = ((actual_acc + 1000) % 2000) - 1000
                acc = actual_acc % 1000
                if acc % 1000 != acc:
                    neg = not neg
                acc %= 1000
            elif cmd == "OUT":
                out.append(acc)
                if print_out_as_run:
                    print(acc)
            elif cmd == "HLT":
                return [out, cycles]
            elif cmd == "DAT":
                return error("Why are you trying to run data? Stop it. Get some help")
            else:
                return error(f"The fuck is this {cmd}?")
            line += 1
        return [out, cycles]

    def single_test(self, given: list, expected: list, test_name: str, max_cycles=50000) -> [int, bool]:
        res = self.run(given, False, max_cycles)
        return [test_name, res[1], res[0] == expected]

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
