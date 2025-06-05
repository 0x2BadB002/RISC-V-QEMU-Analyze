import pyparsing as pp

from domain.command import Command

hex_num = pp.Suppress("0x") + pp.Word(pp.srange("[0-9a-fA-F]"))
parser = pp.Word(pp.srange("[a-zA-Z0-9_.]")) + pp.Opt(hex_num)


def parse(line: str) -> Command:
    data = parser.parseString(line)

    cmd = Command(
        command=data[0],
    )

    if len(data) > 1:
        cmd.address = int(data[1], base=16)

    return cmd
