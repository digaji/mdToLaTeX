import sys, os
sys.path.append(os.getcwd() + f"\\src")

from lexer import to_block, table_lexer, list_lexer
from parser import table_parser, block_injection, list_parser

def main():
    with open("tests/to_block/table.md") as f:
        text = "".join(f.readlines())
        rows = table_lexer(text)
        tables = table_parser(rows)

        items = list_lexer(text)
        lists = list_parser(items)
        injections = list(map(lambda x : x.inject(), tables))
        injections.extend(list(map(lambda x : x.inject(), lists)))
        print(injections)
        # blocks = to_block(ranges, text)
        block_injection(injections, text)
        # print(blocks)

if __name__ == "__main__":
    main()