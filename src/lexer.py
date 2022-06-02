# The lexer tokenizes the input stream consisting of markdown text
import re
import os
from typing import Optional
from typing_extensions import Self
from structures.List import ListItem
from structures.Table import Row

# TODO: Implement folding on inline elements.
# parts of text that should be on the same block, should be on the same line, except for code
def folding(text: str):
    # Solves the block problem
    # putting in line elements on the same line and leaving block level elements alone
    pass

# Should also work for ul's
def list_lexer(text: str):
    # return objects
    text_by_line = text.splitlines()
    item_reg = re.compile(r"^((\t| )*)\d+\. (.*)$")
    uitem_reg = re.compile(r"^((\t| )*)[\*-] (.*)$")
    items = [] # These are where the lists goes
    count_indent = lambda s : s.count("    ") + s.count("\t")
    for ln, line in enumerate(text_by_line):
        if item_reg.match(line):
            match = item_reg.match(line)
            items.append(ListItem(
                                ln, 
                                count_indent(match.group(1)) if match.group(1) else 0,
                                match.group(3))
                            )
        
        if uitem_reg.match(line):
            match = uitem_reg.match(line)
            items.append(ListItem(
                                ln, 
                                count_indent(match.group(1)) if match.group(1) else 0,
                                match.group(3),
                                ordered=False
                                )
                            )
    return items

def table_lexer(text: str):
    text_by_line = text.splitlines()
    row_reg = re.compile(r"^\|(([^\|]*)\|)+$")
    rows : list[Row] = []
    for i, line in enumerate(text_by_line):
        if row_reg.match(line):
            cols = line.strip("|").split("|")
            rows.append(Row(i, *cols))
    return rows


def lexer(text):
    # Italics and bold are a bit weird when combined in weird ways
    # parse_ol(tokenize_ol(text))
    rows = table_lexer(text)
    items = list_lexer(text)
    return rows, items, text

def main():
    
    filename = "table.md"
    filepath = os.getcwd() + f"\\tests\\{filename}"
    with open(filepath, "r") as f:
        rows, items, text = lexer(''.join(f.readlines()))
        print(rows)

def to_block(ranges, text: str):
    text_lines = text.splitlines()
    line = 0
    blocks = []
    for start, end in ranges:
        blocks.append(text_lines[line:start])
        line = end + 1
    return blocks

if __name__ == '__main__':
    main()
