import sys, os
sys.path.append(os.getcwd() + f"\\src")

from lexer import list_lexer
from parser import list_parser

def main():
    with open("tests/list_parser/lists.md", "r") as f:
        text = "".join(f.readlines())
        items = list_lexer(text)
        lists = list_parser(items)
        for li in lists:
            li.print()
            print(li.total_lines())
            print(li.markdown_lines_range())
            print(li.latex_lines_range())
            print()
        
        
    pass

if __name__ == '__main__':
    main()