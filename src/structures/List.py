class ListItem:

    def __init__(self, ln, indent, content: str):
        self.ln = ln # line number, indexed by zero
        self.indent = indent # the indent level
        self.content = content # the content of the ol
        self.listChild = None # if it has children
    
    def __str__(self):
        return f"OrderedListItem(ln={self.ln}, indent={self.indent}, content={repr(self.content)})"
    
    def __repr__(self):
        return self.__str__()

class List:

    def __init__(self):
        self.items: list[ListItem] = []
        pass

    def addChildren(self, item: ListItem):
        self.items.append(item)
    
    def print_ol(self):
        current_indent = self.items[0].indent
        ind_str = "  "
        print(ind_str * current_indent + "\\begin{enumerate}")
        for i, item in enumerate(self.items):
            print(ind_str * item.indent, f"\item {item.content}", sep="")
            if item.listChild:
                item.listChild.print_ol()
        print(ind_str * current_indent + "\\end{enumerate}")


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
