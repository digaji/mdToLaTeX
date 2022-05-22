import sys, os
sys.path.append(os.getcwd() + f"\\src")

from lexer import table_lexer
from parser import table_parser

def main():
    with open("tests/table_parser/table.md", "r") as f:
        text = "".join(f.readlines())
        items = table_lexer(text)
        tables = table_parser(items)
        # for item in items:
        #     print(item) 
        for table in tables:
            table.print()
        
    pass

if __name__ == '__main__':
    main()