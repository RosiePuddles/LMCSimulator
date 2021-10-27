def LMC2ASM(raw_data: str):
    raw_data = raw_data.splitlines()
    data = raw_data[0] if raw_data[0][0] != "#" else raw_data[1]
    data = data[7:]
    data = data[:data.find("%") - 1].split(",")
    assert len(data) == 100
    body = []
    values = {}
    pointers = []
    for i in filter(lambda x: x[0] in ["1", "2", "3", "5"], data):
        values[i[1:]] = 0
    for i in values.keys():
        values[i] = int(data[int(i)])

    for i in filter(lambda x: x[0] in ["6", "7", "8"], data):
        pointers.append(i[1:])
    for n, i in enumerate(data):
        n = str(n).rjust(2, "0")
        if n in values.keys():
            continue
        out = f'P{n}\t' if n in pointers else "\t"
        code = i[0]
        if code == "9":
            out += ("IN" if i == "901" else "OUT")
        elif code in ["1", "2", "3", "5"]:
            cmd = {"1": "ADD", "2": "SUB", "3": "STO", "5": "LDA"}.get(code)
            out += f"{cmd}\tC{i[1:]}"
        elif code in ["6", "7", "8"]:
            cmd = {"6": "BR", "7": "BRZ", "8": "BRP"}.get(code)
            out += f"{cmd}\tP{i[1:]}"
        body.append(out)

    body.extend([f'C{k}\tDAT' + ("" if v == 0 else f"\t{v}") for k, v in values.items()])
    print("\n".join(filter(lambda x: x != "\t", body)))
