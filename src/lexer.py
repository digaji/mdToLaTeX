# The lexer tokenizes the input stream consisting of markdown text
import re
import os
# - Markdown is just fancy plain text

#TODO: Change this to List
class OrderedList:

    def __init__(self):
        self.items = []
        pass

    def addChildren(self, item):
        self.items.append(item)
    
    #TODO: add in the the option to print ordered and unordered
    def print_ol(self):
        for i, item in enumerate(self.items):
            print("  " * item.indent, f"{i + 1}. {item.content}", sep="")
            if item.ordered_list:
                item.ordered_list.print_ol()
        


#TODO: Change this ListItem
class OrderedListItem:

    def __init__(self, ln, indent, content: str):
        self.ln = ln # line number, indexed by zero
        self.indent = indent # the indent level
        self.content = content # the content of the ol
        self.ordered_list = None # if it has children
    
    def __str__(self):
        return f"OrderedListItem(ln={self.ln}, indent={self.indent}, content={repr(self.content)})"
    
    def __repr__(self):
        return self.__str__()

class ListGroup:

    def __init__(self):
        self.members = []
    
    def add(self, member):
        self.members.append(member)
    
    def convert(self, j = 0):
        # 0 1 1 0 1 0 1
        #       ^
        orderedList = OrderedList()
        current_indent = self.members[j].indent
        i = j
        while i < len(self.members):
            if self.members[i].indent > current_indent:
                k, childOrderedList = self.convert(i)
                # childOrderedList.print_ol()
                self.members[i - 1].ordered_list = childOrderedList
                i = k
            elif self.members[i].indent < current_indent:
                return i, orderedList
            else:
                orderedList.addChildren(self.members[i])
                i += 1
        return i, orderedList

        # want to construct listgroup with higher current indent levels
    
    def __str__(self):
        return f"ListGroup(members={repr(self.members)})"
    
    def __repr__(self):
        return self.__str__()


# TODO: Implement folding on inline elements.
# parts of text that should be on the same block, should be on the same line, except for code
def folding(text: str):
    # Solves the block problem
    # putting in line elements on the same line and leaving block level elements alone
    pass

# Should also work for ul's
def tokenize_ol(text: str):
    # return objects
    text_by_line = text.splitlines()
    item_reg = re.compile(r"^((\t| )*)\d+\. (.*)$")
    items = [] # These are where the lists goes
    count_indent = lambda s : s.count("    ") + s.count("\t")
    for i, line in enumerate(text_by_line):
        if item_reg.match(line):
            match = item_reg.match(line)
            items.append(OrderedListItem(i, count_indent(match.group(1)) if match.group(1) else 0, match.group(3)))
            # For DEBUGGING
            # if match.group(3) == "john":
            #     print(repr(line))
            #     print(repr(match.group(1)))
            #     print(print(items[-1]))
    
    return items

def parse_ol(items):
    # items: OrderedListItem
    last = -2 # the line of the last member of the last ListGroup in listgroups
    listgroups = []
    for item in items:
        if last + 1 != item.ln:
            listgroups.append(ListGroup())
        listgroups[-1].add(item)
        last = item.ln
    
    group = listgroups[2]
    print(group)
    # for group in listgroups:
    #     print(group)
    _, orderedList = group.convert()
    orderedList.print_ol()
        

def tokenize_table(text: str):
    text_by_line = text.splitlines()
    row_reg = re.compile(r"^\|(([^\|]*)\|)+$")
    items = [] # These are where the lists goes
    for i, line in enumerate(text_by_line):
        if row_reg.match(line):
            cols = line.strip("|").split("|")
            print(repr(line), cols)



def lexer(text):
    # print(repr(text))
    heading3 = re.compile(r"^\s*### (.{0,})", re.MULTILINE)
    heading3_sub = r"\\subsubsection{\1}"
    heading2 = re.compile(r"^\s*## (.{0,})", re.MULTILINE)
    heading2_sub = r"\\subsection{\1}"
    heading1 = re.compile(r"^\s*# (.{0,})", re.MULTILINE)
    heading1_sub = r"\\section{\1}"

    # Italics and bold are a bit weird when combined in weird ways
    # parse_ol(tokenize_ol(text))
    tokenize_table(text)

    bitalics = re.compile(r"\*\*\*([^\*]+?)\*\*\*");
    bitalics_sub = r"\\textbf{\\textit{\1}}"
    italics = re.compile(r"\*([^\*]+?)\*")
    italics_sub = r"\\textit{\1}"
    bold = re.compile(r"\*\*([^\*]+?)\*\*")
    bold_sub = r"\\textbf{\1}"
    links = re.compile(r"\[(.{0,})\]\((.{0,})\)")
    links_sub = r"\\href{\1}{\2}"

    text = bold.sub(bold_sub, text)
    text = italics.sub(italics_sub, text)
    text = bitalics.sub(bitalics_sub, text)
    text = links.sub(links_sub, text)
    text = heading3.sub(heading3_sub, text)
    text = heading2.sub(heading2_sub, text)
    text = heading1.sub(heading1_sub, text)

    # print(text)
    pass

def main():
    
    filename = "table.md"
    filepath = os.getcwd() + f"\\tests\\{filename}"
    with open(filepath, "r") as f:
        lexer(''.join(f.readlines()))
    pass

if __name__ == '__main__':
    main()
