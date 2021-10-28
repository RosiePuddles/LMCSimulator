from sys import argv, exit
from execution import Program
from translator import LMC2ASM

if len(argv) == 2:
    exit(0)

if argv[1] == "-b":
    prog_path = argv[2]
    test_path = argv[3]
    try:
        return_raw = argv[4].lower() in ["true", "yes"]
    except IndexError:
        return_raw = False
    prog = Program(open(prog_path).read())
    prog.test(test_path, return_raw)
elif argv[1] == "-r":
    prog_path = argv[2]
    Program(open(prog_path).read()).run([], True)
elif argv[1] == "-t":
    LMC2ASM(open(argv[2]).read())
