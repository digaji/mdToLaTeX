class ListItem:

    def __init__(self, ln, indent, content: str, ordered: bool = True):
        self.ln = ln # line number, indexed by zero
        self.indent = indent # the indent level
        self.content = content # the content of the ol
        self.listChild = None # if it has children
        self.ordered = ordered
    
    def __str__(self):
        return f"OrderedListItem(ln={self.ln}, indent={self.indent}, content={repr(self.content)})"
    
    def __repr__(self):
        return self.__str__()

class List:

    def __init__(self, ordered: bool = True):
        self.items: list[ListItem] = []
        self.ordered = ordered
        pass

    def addChildren(self, item: ListItem):
        self.items.append(item)
    
    def print(self, f = None):
        current_indent = self.items[0].indent
        order = "enumerate" if self.items[0].ordered else "itemize"
        ind_str = "  "
        if not f:
            print(ind_str * current_indent + f"\\begin{{{order}}}")
        else:
            f.write(ind_str * current_indent + f"\\begin{{{order}}}\n")
        for i, item in enumerate(self.items):
            if not f:
                print(ind_str * item.indent, f"\item {item.content}", sep="")
            else:
                f.write(ind_str * item.indent + f"\item {item.content}\n")
            if item.listChild:
                item.listChild.print(f)
        if not f:
            print(ind_str * current_indent + f"\\end{{{order}}}")
        else:
            f.write(ind_str * current_indent + f"\\end{{{order}}}\n")

    def total_lines(self):
        # Returns the total number of lines to be added
        tot = 1
        for item in self.items:
            if item.listChild:
                tot += item.listChild.total_lines()
            tot += 1
        tot += 1
        return tot

    def markdown_lines_range(self):
        return (self.items[0].ln, self.items[-1].ln)
    
    def latex_lines_range(self):
        return (self.items[0].ln, self.items[0].ln + self.total_lines() - 1)
    
    def inject(self):
        return (self.markdown_lines_range(), self.total_lines(), self)


class ListGroup:

    def __init__(self):
        self.members: list[ListItem] = []
    
    def add(self, member):
        self.members.append(member)
    
    def getMember(self, i: int) -> ListItem:
        return self.members[i]
    
    def __len__(self) -> int:
        return len(self.members)
    
    def __str__(self):
        return f"ListGroup(members={repr(self.members)})"
    
    def __repr__(self):
        return self.__str__()
