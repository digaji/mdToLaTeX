from lexer import list_lexer, table_lexer
from parser import parser_substitutable, list_parser, table_parser, block_injection, file_injection

def generate_latex(mdsrc: str, textarg: str):

    with open(mdsrc, "r") as f:
        text = "".join(f.readlines())
        # print(text)
        text = parser_substitutable(text)
        injections = []
        inject = lambda x: x.inject()
        # lexically analyzing the text
        rows = table_lexer(text)
        tables = table_parser(rows)
        injections.extend(map(inject, tables))

        items = list_lexer(text)
        lists = list_parser(items)
        injections.extend(map(inject, lists))
        injections = sorted(injections, key = lambda x: x[0])
        with open(textarg, "w") as out:
            file_injection(injections, text, out)
        


def main():
    generate_latex("build/in.md", "build/out.tex")
    pass

if __name__ == '__main__':
    main()