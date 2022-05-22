import re
from structures.List import ListItem, ListGroup, List
from structures.Table import Row, Table

def listgroup_parser(listGroup: ListGroup, j = 0) -> tuple[int, ListGroup]:
        li = List()
        current_indent = listGroup.getMember(j).indent
        i = j
        while i < len(listGroup):
            if listGroup.getMember(i).indent > current_indent:
                k, listChild = listgroup_parser(listGroup, i)
                listGroup.getMember(i - 1).listChild = listChild
                i = k
            elif listGroup.getMember(i).indent < current_indent:
                return i, li
            else:
                li.addChildren(listGroup.getMember(i))
                i += 1
        return i, li

def list_parser(items: list[ListItem]):
    # items: OrderedListItem
    last = -2 # the line of the last member of the last ListGroup in listgroups
    listgroups = []
    for item in items:
        if last + 1 != item.ln:
            listgroups.append(ListGroup())
        listgroups[-1].add(item)
        last = item.ln
    
    lists = []
    for listgroup in listgroups:
        _, listgroup = listgroup_parser(listgroup)
        lists.append(listgroup)
    
    return lists

def table_parser(rows: list[Row]):
    # 1. group the rows into a Table class
    # Tables are guided by the heading

    last = -2 # the line of the last member of the last ListGroup in listgroups
    tables: list[Table] = []
    for row in rows:
        if last + 1 != row.ln:
            tables.append(Table())
        tables[-1].addRow(row)
        last = row.ln

    return tables    

def parser_substitutable(text: str) -> str:
    # Regular Expressions
    heading3 = re.compile(r"^\s*### (.{0,})", re.MULTILINE)
    heading3_sub = r"\\subsubsection{\1}"
    heading2 = re.compile(r"^\s*## (.{0,})", re.MULTILINE)
    heading2_sub = r"\\subsection{\1}"
    heading1 = re.compile(r"^\s*# (.{0,})", re.MULTILINE)
    heading1_sub = r"\\section{\1}"
    bitalics = re.compile(r"\*\*\*([^\*]+?)\*\*\*");
    bitalics_sub = r"\\textbf{\\textit{\1}}"
    italics = re.compile(r"\*([^\*]+?)\*")
    italics_sub = r"\\textit{\1}"
    bold = re.compile(r"\*\*([^\*]+?)\*\*")
    bold_sub = r"\\textbf{\1}"
    links = re.compile(r"\[(.{0,})\]\((.{0,})\)")
    links_sub = r"\\href{\1}{\2}"

    # Substitutions
    text = bold.sub(bold_sub, text)
    text = italics.sub(italics_sub, text)
    text = bitalics.sub(bitalics_sub, text)
    text = links.sub(links_sub, text)
    text = heading3.sub(heading3_sub, text)
    text = heading2.sub(heading2_sub, text)
    text = heading1.sub(heading1_sub, text)
    return text

def parser(listItems: list[ListItem], rows: list[Row], text: str):


    pass
