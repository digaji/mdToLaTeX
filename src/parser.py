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
    heading3_sub = r"\\subsubsection*{\1}"
    heading2 = re.compile(r"^\s*## (.{0,})", re.MULTILINE)
    heading2_sub = r"\\subsection*{\1}"
    heading1 = re.compile(r"^\s*# (.{0,})", re.MULTILINE)
    heading1_sub = r"\\section*{\1}"
    bitalics = re.compile(r"\*\*\*([^\*]+?)\*\*\*")
    bitalics_sub = r"\\textbf{\\textit{\1}}"
    italics = re.compile(r"\*([^ ][^\*]+?)\*")
    italics_sub = r"\\textit{\1}"
    bold = re.compile(r"\*\*([^ ][^\*]+?)\*\*")
    bold_sub = r"\\textbf{\1}"
    links = re.compile(r"\[(.{0,})\]\((.{0,})\)")
    links_sub = r"\\href{\2}{\1}"
    hrule = re.compile(r"^---$", re.MULTILINE)
    hrule_sub = r"\\hrulefill\\\\"
    # code uses xparse in latex
    code = re.compile(r"`(.*)`")
    code_sub = r"\\verb\|\1\|"

    # Substitutions
    text = bold.sub(bold_sub, text)
    text = italics.sub(italics_sub, text)
    text = bitalics.sub(bitalics_sub, text)
    text = links.sub(links_sub, text)
    text = code.sub(code_sub, text)
    text = hrule.sub(hrule_sub, text)
    text = heading3.sub(heading3_sub, text)
    text = heading2.sub(heading2_sub, text)
    text = heading1.sub(heading1_sub, text)
    return text

def block_injection(injections, text: str):
    # write document outlines

    text_lines = text.splitlines()
    current_line = 0
    offset = 0
    for intrvl, tot_lines, obj in injections:
        start, end = intrvl
        for line in text_lines[current_line:start]:
            print(line)
        obj.print()
        current_line = end + 1
    # print(text_lines[current_line:-1])
    for line in text_lines[current_line: len(text_lines)]:
        print(line)

def file_injection(injections, text: str, f):
    config =\
"""\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{hyperref}
\\usepackage[a4paper, margin=2cm]{geometry}
\\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=blue,
    pdftitle={Overleaf Example},
    pdfpagemode=FullScreen,
    }
\\title{testing}
\\author{bryn.ghiffar }
\\date{April 2022}

\\begin{document}
"""
    f.write(config)

    text_lines = text.splitlines()
    current_line = 0
    offset = 0
    for intrvl, tot_lines, obj in injections:
        start, end = intrvl
        for line in text_lines[current_line:start]:
            f.write(line + "\n")
        obj.print(f)
        current_line = end + 1
    # print(text_lines[current_line:-1])
    for line in text_lines[current_line: len(text_lines)]:
        f.write(line + "\n")
    f.write("\\end{document}\n")

def parser(listItems: list[ListItem], rows: list[Row], text: str):


    pass
