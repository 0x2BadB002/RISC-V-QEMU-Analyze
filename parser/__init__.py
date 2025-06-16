import pyparsing as pp

from domain.command import Command


def extract_mnemonic(tokens: str):
    instruction_str = tokens[0]
    return instruction_str.strip().split()[0] if instruction_str.strip() else ""


integer = pp.Word(pp.nums).setParseAction(lambda t: int(t[0]))
hex_number = pp.Regex(r'0x[0-9a-fA-F]+')
mnemonic = pp.QuotedString('"', unquoteResults=True).setParseAction(extract_mnemonic)

load_store = pp.Keyword("load") | pp.Keyword("store")

comma = pp.Suppress(pp.Optional(pp.White()) + "," + pp.Optional(pp.White()))

parser = (
    integer("index") + comma
    + hex_number("addr1") + comma
    + hex_number("addr2") + comma
    + mnemonic("instruction")
    + pp.ZeroOrMore(
        comma
        + load_store("op_type")
        + comma + hex_number("addr3")
    )
    + pp.StringEnd()
)


def parse(line: str) -> Command:
    data = parser.parseString(line).asList()

    cmd = Command(
        cpu_index=data[0],
        command=data[3],
    )

    if len(data) > 4:
        cmd.address = int(data[5], base=16)

    return cmd
