from myParser import BlockQuoteBlock, OrderedBlock, Parser, TableBlock, UnorderedBlock
from lexer import Bitalics, Bold, CodeBlock, HRule, Heading, InlineCode, Italics, Lexer, Line, Link, SomeString

class BlockPointer:

    def __init__(self, document, current = 0):
        self.document = document
        self.current = current

    def at_end(self):
        return self.current == len(self.document)

    def peek(self, n = 1):
        if self.current + n > len(self.document):
            return None
        if n == 1:
            return self.document[self.current]
        return self.document[self.current:self.current + n]

    def move(self, n = 1):
        if n < 0:
            raise Exception("n must be a positive integer")
        if n == 0:
            return self.peek()

        
        if self.current + n > len(self.document):
            before = self.current
            self.current = len(self.document)
            return self.document[before:self.current]

        before = self.current
        self.current += n
        return self.document[before:self.current]



class Generator:

    def __init__(self, document, write = lambda x : print(x, end="")):
        self.main = BlockPointer(document)
        self.write = write

    
    def generate_heading(self):
        '''Generates a heading to latex'''
        item = self.main.peek()
        template = lambda family, content: f"{{\\noindent \\{family} \\textbf{{{content}}}}}" + "\\" * 4 + "\n"
        if type(item) is Heading:
            if item.lvl == 1:
                # self.write(f"{{\\noindent \\Huge \\textbf{{{item.content}}}}}" + "\\" * 2 + "\n")
                self.write(template("Huge", item.content))
            elif item.lvl == 2:
                # self.write(f"{{\\LARGE {item.content}}}" + "\\" * 2 + "\n")
                self.write(template("LARGE", item.content))
            elif item.lvl == 3:
                # self.write(f"{{\\Large {item.content}}}\n" + "\\" * 2 + "\n")
                self.write(template("Large", item.content))
            self.main.move()
            return True
    
    def generate_line(self, itemp = None, linebreak = False):
        '''Generates a line'''
        if itemp is None:
            item = self.main.peek()
        else:
            item = itemp
        if type(item) is Line:
            for content in item.content:
                if type(content) is SomeString:
                    self.write(content.content)
                    continue
                if type(content) is Bitalics:
                    self.write(f"\\textbf{{\\textit{{{content.content}}}}}")
                    continue
                if type(content) is Bold:
                    self.write(f"\\textbf{{{content.content}}}")
                    continue
                if type(content) is Italics:
                    self.write(f"\\textit{{{content.content}}}")
                    continue
                if type(content) is Link:
                    self.write(f"\\href{{{content.url}}}{{{content.text}}}")
                    continue
                if type(content) is InlineCode:
                    self.write(f"\\verb|{content.content}|")
            if linebreak or (len(item.content) == 0):
                self.write("\\" * 2)
            self.write("\n")
            if itemp is None:
                self.main.move()
            return True

    def generate_blockquote(self, itemp = None, depth = 1):
        '''Generates blockquotes'''
        if itemp is None:
            item = self.main.peek()
        else:
            item = itemp
        if type(item) is BlockQuoteBlock:
            self.write("\t" * (depth - 1))
            self.write("\\begin{displayquote}\n")
            for it in item.items:
                self.write("\t" * depth)
                self.generate_line(it.content, linebreak=False)
                if len(it.children) > 0:
                    self.generate_blockquote(it.children[0], depth + 1)
            self.write("\t" * (depth - 1))
            self.write("\\end{displayquote}\n")
            if itemp is None:
                self.main.move()
            return True

                
    
    def generate_table(self):
        '''Generates table'''
        item = self.main.peek()
        if type(item) is TableBlock:
            col = len(item.rows[0].columns)
            ltx_col_str = "|" + "c|" * col
            self.write(f"\\begin{{tabular}}{{{ltx_col_str}}}\n")
            self.write("\t\\hline\n")
            for row in item.rows:
                for i, column in enumerate(row.columns):
                    if i == 0:
                        self.write("\t" + column.content)
                    else:
                        self.write(" & " + column.content)
                self.write(" " + "\\" * 2 + "\n")
                self.write("\t\\hline\n")

            self.write("\\end{tabular}" + "\\" * 6 + "\n")
            self.main.move()
            return True
    
    def generate_unordered(self, itemp = None, depth = 0):
        '''Generats unordered list'''
        if itemp is None:
            item = self.main.peek()
        else:
            item = itemp
        if type(item) is UnorderedBlock:
            self.write("\t" * depth)
            self.write("\\begin{itemize}\n")
            for it in item.items:
                self.write("\t" * (depth + 1))
                self.write("\\item ")
                self.generate_line(it.content, linebreak=False)
                if len(it.children) > 0:
                    self.generate_unordered(it.children[0], depth + 1)
            self.write("\t" * depth)
            self.write("\\end{itemize}\n")
            if itemp is None:
                self.main.move()
            return True


    def generate_ordered(self, itemp = None, depth = 0):
        '''Generats unordered list'''
        if itemp is None:
            item = self.main.peek()
        else:
            item = itemp
        if type(item) is OrderedBlock:
            self.write("\t" * depth)
            self.write("\\begin{enumerate}[label=\\arabic*.]\n")
            for it in item.items:
                self.write("\t" * (depth + 1))
                self.write("\\item ")
                self.generate_line(it.content, linebreak=False)
                if len(it.children) > 0:
                    self.generate_ordered(it.children[0], depth + 1)
                self.write(f"")
            self.write("\t" * depth)
            self.write("\\end{enumerate}\n")
            if itemp is None:
                self.main.move()
            return True
    
    def generate_codeblock(self):
        '''Generates code block'''
        item = self.main.peek()
        if type(item) is CodeBlock:
            self.write("\\begin{lstlisting}")
            self.write(item.content)
            self.write("\\end{lstlisting}\n")
            self.main.move()
            return True

    
    def generate_hrule(self):
        '''Generate hrule'''
        item = self.main.peek()
        if type(item) is HRule:
            self.write("\\rule{170mm}{1pt}" + "\\" * 4 + "\n")
            self.main.move()
            return True
    
    def config_doc(self):
        doc_type = "\\documentclass{article}"
        self.write(doc_type)
        self.write("\n")
    
    def config_packages(self):
        packages = [
            "\\usepackage{csquotes}",
            "\\usepackage{hyperref}",
            "\\usepackage[a4paper, margin=2cm]{geometry}",
            "\\usepackage{listings}",
            "\\usepackage[utf8]{inputenc}"
            "\\usepackage{xcolor}",
            "\\usepackage{enumitem}",
        ]
        self.write("% --- PACKAGES ---\n")
        for package in packages:
            self.write(package)
            self.write("\n")
    
    def config_hyperref(self):
        hyperref_setup =\
'''% --- HYPERREF CONFIG ---
\\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=blue
    urlcolor=blue,
}'''
        self.write(hyperref_setup)
        self.write("\n")
    
    def config_codeblock(self):
        color_definition = "\\definecolor{bgcolor}{rgb}{0.95, 0.95, 0.95}"
        style_definition =\
            '''\\lstdefinestyle{cbstyle}{
                backgroundcolor=\\color{bgcolor},
                basicstyle=\\ttfamily
            }'''
        set_style = "\\lstset{style=cbstyle}"
        self.write("% --- CODEBLOCK CONFIG ---\n")
        self.write(color_definition)
        self.write("\n")
        self.write(style_definition)
        self.write("\n")
        self.write(set_style)
        self.write("\n")
    
    def generate(self):
        self.config_doc()
        self.config_packages()
        self.config_hyperref()
        self.config_codeblock()
        
        self.write("\\begin{document}\n")
        while not self.main.at_end():
            if not (self.generate_heading() is None):
                continue
            if not (self.generate_unordered() is None):
                continue
            if not (self.generate_ordered() is None):
                continue
            if not (self.generate_blockquote() is None):
                continue
            if not (self.generate_line() is None):
                continue
            if not (self.generate_table() is None):
                continue
            if not (self.generate_hrule() is None):
                continue
            if not (self.generate_codeblock() is None):
                continue

            self.write(str(self.main.peek()) + "\n")
            self.main.move()
        self.write("\\end{document}\n")
    
def main():
    with open("test-error-it-b-bi.md", "r") as f:
        text = f.read()

    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    document = parser.parse()
    with open("test-error-it-b-bi.tex", "w") as f:
        generator = Generator(document, f.write)
        generator.generate()


if __name__ == '__main__':
    main()