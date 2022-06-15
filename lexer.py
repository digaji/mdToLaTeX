#!/usr/bin/python3
from copy import copy
from typing_extensions import Self
import re


class BlockQuote:
    
    def __init__(self, content, depth, line, col):
        self.content = content
        self.depth = depth
        self.children = []
        self.line = line
        self.col = col
    
    def append_child(self, child: Self):
        self.children.append(child)
    
    def __repr__(self):
        return f"BlockQuote(content={repr(self.content)}, depth={self.depth}, children={self.children}, line={self.line}, col={self.col})"

class UnorderedLi:

    def __init__(self, content, depth, line, col):
        self.content = content
        self.depth = depth
        self.children = []
        self.line = line
        self.col = col
    
    def append_child(self, child: Self):
        self.children.append(child)
    
    def plain_text(self):
        space = " " * self.depth
        return f"{space * self.depth} * {self.content}"
    
    def print_tree(self):
        print(self.plain_text())
        for child in self.children:
            child.print_tree()
    
    def __repr__(self):
        return f"UnorderedLi(content={repr(self.content)}, depth={self.depth}, children={self.children}, line={self.line}, col={self.col})"

class OrderedLi:

    def __init__(self, content, depth, line, col):
        self.content = content
        self.depth = depth
        self.children = []
        self.line = line
        self.col = col
    
    def append_child(self, child: Self):
        self.children.append(child)
    
    def plain_text(self):
        space = " " * self.depth
        return f"{space * self.depth} * {self.content}"
    
    def print_tree(self):
        print(self.plain_text())
        for child in self.children:
            child.print_tree()
    
    def __repr__(self):
        return f"OrderedLi(content={repr(self.content)}, depth={self.depth}, children={self.children}, line={self.line}, col={self.col})"

class HRule:

    def __init__(self, line, col):
        self.line = line
        self.col = col

    def __repr__(self):
        return f"HRule(line={self.line}, col={self.line})"

class Line:

    def __init__(self, content, line, col):
        self.content = content
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Line(content={repr(self.content)}, line={self.line}, col={self.col})"
    
    def is_empty(self):
        return len(self.content) == 0

class CodeBlock:

    def __init__(self, content, line, col):
        self.content: str = content
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"CodeBlock(content={repr(self.content)}, line={self.line}, col={self.col})"

class SomeString:

    def __init__(self, content, line, col):
        self.content: str = content
        self.line = line
        self.col = col
    
    def lstrip(self):
        return SomeString(self.content.lstrip(), self.line, self.col)
    
    def rstrip(self):
        return SomeString(self.content.rstrip(), self.line, self.col)
    
    def strip(self):
        return SomeString(self.content.strip(), self.line, self.col)
    
    def __repr__(self):
        return f"SomeString(content={repr(self.content)}, line={self.line}, col={self.col})"
    
class SomeStringBuilder:

    def __init__(self):
        self.string = []
        self.line = 1
        self.col = 1
    
    def add_string(self, string):
        self.string.append(string)

    def set_line(self, line: int):
        self.line = line
    
    def set_col(self, col: int):
        self.col = col
    
    def clear(self):
        self.string = []
        self.line = 1
        self.col = 1
    
    def is_empty(self):
        return len(self.string) == 0

    def get_some_string(self):
        return SomeString(''.join(self.string), self.line, self.col)

class Heading:

    def __init__(self, content, lvl, line, col):
        self.content = content
        self.lvl = lvl
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Heading(content={repr(self.content)}, lvl={self.lvl}, line={self.line}, col={self.col})"

class TextPointer:

    def __init__(self, text, current = 0, line = 1, col = 1):
        self.text = text
        self.current = current
        self.whitespace = " \t\n"
        self.line = line
        self.col = col
    
    def at_line(self):
        return self.line
    
    def at_col(self):
        return self.col

    def at_start(self):
        return self.current == 0

    def at_end(self):
        return self.current == len(self.text)
    
    def at_begin_line(self):
        return self.at_start() or self.peek_back() == "\n"
    
    def at_end_line(self):
        return self.at_end() or self.peek() == "\n"
    
    def peek(self, n = 1) -> str: # looks at the current 
        if self.current + n > len(self.text):
            return None
        return self.text[self.current:self.current + n]
    
    def peek_back(self, n = 1):
        if self.current - n < 0:
            return None
        return self.text[self.current - n:self.current]
    
    def move(self, n = 1):
        if n < 0:
            raise Exception("n must be a positive integer")
        if n == 0:
            return self.peek()

        if self.current + n > len(self.text):
            before = self.current
            self.current = len(self.text)
            return self.text[before:self.current]

        s = []
        for _ in range(n):
            s.append(self.peek())
            if self.peek() == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.current += 1
        # before = self.current
        # self.current += n
        # dl += self.text[before:self.current].count("\n")
        return "".join(s)
    
    def move_non_whitespace(self): # moves until a non whitespace character is found
        '''
        Moves the cursor until a whitespace character is found.
        Returns the string before the whitespace, not including the whitespace.
        '''
        s = []
        while (not self.at_end()) and (self.peek() in self.whitespace):
            s.append(self.peek())
            self.move()
        return "".join(s)
    
    def move_next_line(self):
        '''
        Moves the cursor until the start of the next line.
        Returns the string before the newline character, not including the newline character
        '''
        s = []
        while not self.at_end_line():
            s.append(self.peek())
            self.move()
        self.move()
        return "".join(s)
    
    def move_next_line_until(self, *strings):
        s = []
        while (not self.at_end_line()):
            for v in strings:
                if self.peek(len(v)) == v:
                    self.move(len(v))
                    return "".join(s)
            s.append(self.peek())
            self.move()
        self.move()
        return "".join(s)

    def move_next_line_until_throw(self, *strings):
        s = []
        while (not self.at_end_line()):
            for v in strings:
                if self.peek(len(v)) == v:
                    self.move(len(v))
                    return "".join(s)
            s.append(self.peek())
            self.move()
        raise Exception("Matching string not found. End of line reached")

    def move_until(self, *strings):
        s = []
        while (not self.at_end()):
            for v in strings:
                if self.peek(len(v)) == v:
                    self.move(len(v))
                    return "".join(s)
            s.append(self.peek())
            self.move()
        self.move()
        return "".join(s)

    def move_until_throw(self, *strings):
        s = []
        while (not self.at_end()):
            for v in strings:
                if self.peek(len(v)) == v:
                    self.move(len(v))
                    return "".join(s)
            s.append(self.peek())
            self.move()
        raise Exception("Ending string not found")
        
    
    def back(self, n = 1):
        if n < 0:
            raise Exception("n must be a positive integer")
        if n == 0:
            return self.peek()

        if self.current - n < 0:
            before = self.current
            self.current = 0
            return self.text[self.current:before]

        before = self.current
        self.current -= n
        return self.text[before:self.current]
    
    def copy(self):
        return TextPointer(self.text, self.current, self.at_line(), self.at_col())
    
class TableRow:

    def __init__(self, line, col):
        self.columns = []
        self.line = line
        self.col = col
    
    def append_column(self, column):
        self.columns.append(column)
    
    def __repr__(self):
        rep = "TableRow("
        for i, v in enumerate(self.columns):
            rep += f"col-{i + 1}={repr(v)}, "
        rep += f"line={self.line}, col={self.col})"
        return rep

class InlineCode:

    def __init__(self, content, line, col):
        self.content = content
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"InlineCode(content={repr(self.content)}, line={self.line}, col={self.col})"

class Bitalics:

    def __init__(self, content, line, col):
        self.content = content
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Bitalics(content={repr(self.content)}, line={self.line}, col={self.col})"

class Bold:

    def __init__(self, content, line, col):
        self.content = content
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Bold(content={repr(self.content)}, line={self.line}, col={self.col})"

class Italics:

    def __init__(self, content, line, col):
        self.content = content
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Italics(content={repr(self.content)}, line={self.line}, col={self.col})"

class Link:

    def __init__(self, text, url, line, col):
        self.text = text
        self.url = url
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Link(text={repr(self.text)}, url={repr(self.url)}, line={self.line}, col={self.col})"

class Lexer:

    def __init__(self, text):
        self.main = TextPointer(text)
    
    def tokenize_bitalics(self):
        '''
        A inline level element tokenizer
        '''
        temp = self.main.copy()
        if not temp.at_end():
            if temp.peek(3) == "***":
                line = temp.at_line()
                col = temp.at_col()
                temp.move(3)
                content = temp.move_next_line_until("***")
                if temp.peek_back(3) != "***":
                    raise Exception(f"Bitalics on line {line} and col {col} not closed, please close bitalics")
                self.main = temp
                return Bitalics(content, line, col)
    
    def tokenize_link(self):
        '''
        A inline level element tokenizer
        '''
        temp = self.main.copy()
        if not temp.at_end():
            if temp.peek() == "[":
                line = temp.at_line()
                col = temp.at_col()
                temp.move()
                try:
                    text = temp.move_next_line_until_throw(']')
                except Exception as e:
                    raise Exception(f"Link on line {line} and col {col} is missing a ']'")
                if temp.peek() == '(':
                    temp.move()
                    try:
                        url = temp.move_next_line_until_throw(')')
                        self.main = temp
                        return Link(text.strip(), url.strip(), line, col)
                    except Exception as e:
                        raise Exception(f"Link on line {line} and col {col} is missing a ')'")
                else:
                    raise Exception(f"Link on line {line} col {col} is expecting a '(' on line {temp.at_line()} and col {temp.at_col()}")
    
    def tokenize_bold(self):
        '''
        A inline level element tokenizer
        '''
        temp = self.main.copy()
        if not temp.at_end():
            if temp.peek(2) == "**":
                line = temp.at_line()
                col = temp.at_col()
                temp.move(2)
                content = temp.move_next_line_until("**")
                if temp.peek_back(2) != "**":
                    raise Exception(f"Bold on line {line} and col {col} not closed, please close bold")
                self.main = temp
                return Bold(content, line, col)
    
    def tokenize_italics(self):
        '''
        A inline level element tokenizer
        '''
        temp = self.main.copy()
        if not temp.at_end():
            if temp.peek() == "*":
                line = temp.at_line()
                col = temp.at_col()
                temp.move()
                content = temp.move_next_line_until("*")
                if temp.peek_back() != "*":
                    raise Exception(f"Italics on line {line} and col {col} not closed, please close italics")
                self.main = temp
                return Italics(content, line, col)
    
    def tokenize_inlinecode(self):
        '''
        A inline level element tokenizer
        '''
        temp = self.main.copy()
        if not temp.at_end():
            if temp.peek() == "`":
                line = temp.at_line()
                col = temp.at_col()
                temp.move()
                content = temp.move_next_line_until("`")
                if temp.peek_back() != "`":
                    raise Exception(f"InlineCode on line {line} and col {col} not closed, please close InlineCode")
                self.main = temp
                return InlineCode(content, line, col)
    
    def tokenize_heading(self):
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        if (temp.at_begin_line()) and not (temp.at_end()):
            if temp.peek() == "#":
                line = temp.at_line()
                col = temp.at_col()
                lvl = 0
                while (temp.peek() == "#"):
                    lvl += 1
                    temp.move()
                if (temp.peek() == " "):
                    temp.move()
                    content = temp.move_next_line()
                    self.main = temp
                    return Heading(content, lvl, line, col)
                else:
                    raise Exception(f"At line {line} and col {col}, heading must have a space between '#' symbols and start of title")
    
    def tokenize_code_block(self):
        temp = self.main.copy()
        if (temp.at_begin_line()) and not (temp.at_end_line()):
            if temp.peek(3) == "```":
                line = temp.at_line()
                col = temp.at_col()
                temp.move(3)
                try:
                    content = temp.move_until_throw("```")
                except Exception as e:
                    raise Exception(f"Code block closing pair not found, starting at line {line} and col {col}")
                self.main = temp
                return CodeBlock(content, line, col)
    
    def tokenize_ul_element(self):
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        # each line of the form "   * asasdf\n" is a tree element
        if (temp.at_begin_line()) and not (temp.at_end()):
            ind = temp.move_non_whitespace()
            dep = ind.count(" ") // 4 + ind.count("\t")
            if temp.peek(2) == "* ":
                line = temp.at_line()
                col = temp.at_col()
                temp.move(2)
                # content = self.move_next_line()
                self.main = temp
                content = self.tokenize_line()
                if not (content is None):
                    return UnorderedLi(content, dep, line, col)
                else: # Case when there is no item on the list
                    return UnorderedLi([], dep, line, col)
        return None
    
    def tokenize_ol_element(self):
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        # each line of the form "   * asasdf\n" is a tree element
        if (temp.at_begin_line()) and not (temp.at_end()):
            ind = temp.move_non_whitespace()
            dep = ind.count(" ") // 4 + ind.count("\t")
            if temp.peek().isdigit():
                line = temp.at_line()
                col = temp.at_col()
                while temp.peek().isdigit():
                    temp.move()
                if temp.peek(2) != '. ':
                    return None
                temp.move(2)
                # content = self.move_next_line()
                self.main = temp
                content = self.tokenize_line()
                if not (content is None):
                    return OrderedLi(content, dep, line, col)
                else: # Case when there is no item on the list
                    return OrderedLi([], dep, line, col)
        return None
    
    def tokenize_blockquote(self):
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        if (temp.at_begin_line()) and not (temp.at_end()):
            if temp.peek() == ">":
                line = temp.at_line()
                col = temp.at_col()
                dep = 0
                while temp.peek() == ">":
                    dep += 1
                    temp.move()
                if temp.peek() == " ":
                    temp.move()
                    self.main = temp
                    content = self.tokenize_line()

                    # need to be able to parse inline elements here
                    return BlockQuote(content, dep, line, col)
                else:
                    return None
        return None
    
    def tokenize_table_row(self):
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        if (temp.at_begin_line()) and not (temp.at_end()):
            if (temp.peek() == "|"):
                line = temp.at_line()
                col = temp.at_col()
                temp.move()
                string_builder = SomeStringBuilder()
                string_builder.set_line(temp.at_line())
                string_builder.set_col(temp.at_col())
                tr = TableRow(line, col)
                while not temp.at_end_line():
                    while (not temp.at_end_line()) and (temp.peek() != "|"):
                        string_builder.add_string(temp.peek())
                        temp.move()
                    if (temp.peek() == "|"):
                        temp.move()
                        # Need to be able to parse inline elements, here
                        tr.append_column(string_builder.get_some_string().strip())
                        string_builder.clear()
                        string_builder.set_line(temp.at_line())
                        string_builder.set_col(temp.at_col())
                    else:
                        raise Exception(f"Table row incorrect syntax error, starting at line {line} and col {col}")
                temp.move()
                self.main = temp
                return tr
        return None
    
    def tokenize_hrule(self):
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        if (temp.at_begin_line()) and not (temp.at_end()):
            if temp.peek(3) == '---':
                line = temp.at_line()
                col = temp.at_col()
                temp.move(3)
                if temp.peek() == "\n":
                    temp.move()
                    self.main = temp
                    return HRule(line, col)
                else:
                    raise Exception(f"HRule on line {line} and col {col} must be alone on a single line")

    
    def tokenize_line(self): # converts from the current position to the end of a line to a stream of tokens of inline elements
        '''
        A block level element tokenizer
        '''
        temp = self.main.copy()
        tokens = []
        string_builder = SomeStringBuilder()
        if not (temp.at_end()):
            line = temp.at_line()
            col = temp.at_col()

            string_builder.set_line(line)
            string_builder.set_col(col)
            while not temp.at_end_line():
                self.main = temp
                app = None

                app = self.tokenize_bitalics()
                if not (app is None):
                    temp = self.main.copy()
                    if not string_builder.is_empty():
                        tokens.append(string_builder.get_some_string())
                        string_builder.clear()
                        string_builder.set_col(temp.at_col())
                        string_builder.set_line(temp.at_line())
                    tokens.append(app)
                    continue
                
                app = self.tokenize_bold()
                if not (app is None):
                    temp = self.main.copy()
                    if not string_builder.is_empty():
                        tokens.append(string_builder.get_some_string())
                        string_builder.clear()
                        string_builder.set_col(temp.at_col())
                        string_builder.set_line(temp.at_line())
                    tokens.append(app)
                    continue

                app = self.tokenize_link()
                if not (app is None):
                    temp = self.main.copy()
                    if not string_builder.is_empty():
                        tokens.append(string_builder.get_some_string())
                        string_builder.clear()
                        string_builder.set_col(temp.at_col())
                        string_builder.set_line(temp.at_line())
                    tokens.append(app)
                    continue

                app = self.tokenize_italics()
                if not (app is None):
                    temp = self.main.copy()
                    if not string_builder.is_empty():
                        tokens.append(string_builder.get_some_string())
                        string_builder.clear()
                        string_builder.set_col(temp.at_col())
                        string_builder.set_line(temp.at_line())
                    tokens.append(app)
                    continue

                app = self.tokenize_inlinecode()
                if not (app is None):
                    temp = self.main.copy()
                    if not string_builder.is_empty():
                        tokens.append(string_builder.get_some_string())
                        string_builder.clear()
                        string_builder.set_col(temp.at_col())
                        string_builder.set_line(temp.at_line())
                    tokens.append(app)
                    continue

                # bold, italics and bitalics should be here
                string_builder.add_string(temp.peek())
                temp.move()
            temp.move()

            if not string_builder.is_empty():
                tokens.append(string_builder.get_some_string())
            self.main = temp
            return Line(tokens, line, col)
        
        return None
    
    def tokenize(self):
        tokens = []
        while (not self.main.at_end()):
            app = None

            app = self.tokenize_heading()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_hrule()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_table_row()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_blockquote()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_ul_element()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_ol_element()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_code_block()
            if not (app is None):
                tokens.append(app)
                continue

            app = self.tokenize_line()
            if not (app is None):
                tokens.append(app)
                continue
            
        return tokens

def main():
    with open("test.md", "r") as f:
        text = f.read()
    l = Lexer(text)
    tokens = l.tokenize()
    for token in tokens:
        print(token)


if __name__ == '__main__':
    main()
