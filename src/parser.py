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
    # for case in case
    # good_cases, bad_cases = case
    #   for bad_case in bad_cases:
    #       pattern, message = bad_case
    #   for good_case in good_cases:
    #       pattern, sub = good_case 
    cases = [
        # bitalics
        [
            [
                [
                    re.compile(r"(^|[ ])\*\*\*([^ \*][^\*]*?)\*\*\*"),
                    r"\\textbf{\\textit{\2}}"
                ]
            ],
            [
                [
                    re.compile(r"\*\*\*([^\*]+?)\*{0,2}"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially bold and italics at line {line}, col {col}"
                ],
            ]
        ],

        # bold
        [
            [
                [
                    re.compile(r"(^|[ ])\*\*([^ \*][^\*]*?)\*\*"),
                    r"\\textbf{\2}"
                ]
            ],
            [
                [
                    re.compile(r"\*\*([^ \*][^\*]*?)\*?"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially bold at line {line}, col {col}"
                ]
            ]
        ],

        # italics
        [
            [
                [
                    re.compile(r"(^|[ ])\*([^ \*][^\*]*?)\*"),
                    r"\\textit{\2}"
                ]
            ],
            [
                [
                    re.compile(r"\*([^ \*][^\*]*?)[^\*]"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially italics at line {line}, col {col}"
                ]
            ]
        ],

        # images
        [
            [
                [
                    re.compile(r"\!\[(.{0,})\]\s?\((.{0,})\)"),
                    r"\\includegraphics{\2}"
                ]
            ],
            [
                [
                    re.compile(r"\!\[(.{0,})\s?\((.{0,})\)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially an image at line {line}, col {col}"
                ],
                [
                    re.compile(r"\!(.{0,})\]\s?\((.{0,})\)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially an image at line {line}, col {col}"
                ],
                [
                    re.compile(r"\!\[(.{0,})\]\s?(.{0,})\)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially an image at line {line}, col {col}"
                ],
                [
                    re.compile(r"\!\[(.{0,})\]\s?\((.{0,})"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially an image at line {line}, col {col}"
                ]
            ]
        ],

        # links
        [
            [
                [
                    re.compile(r"\[(.{0,})\]\s?\((.{0,})\)"),
                    r"\\href{\2}{\1}"
                ]
            ],
            [
                [
                    re.compile(r"[^\!]\[(.{0,})\s?\((.{0,})\)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially a link at line {line}, col {col}"
                ],
                [
                    re.compile(r"[^\!](.{0,})\]\s?\((.{0,})\)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially a link at line {line}, col {col}"
                ],
                [
                    re.compile(r"[^\!]\[(.{0,})\]\s?(.{0,})\)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially a link at line {line}, col {col}"
                ],
                [
                    re.compile(r"[^\!]\[(.{0,})\]\s?\((.{0,})"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially a link at line {line}, col {col}"
                ]
            ]
        ],

        # code
        [
            [
                [
                    re.compile(r"`([^`]+)`"),
                    r"\\verb\|\1\|"
                ]
            ],
            [
                [
                    re.compile(r"`([^`]+)"),
                    lambda line, col, string: f"Warning: \"{string}\" is potentially an inline code at line {line}, col {col}"
                ]
            ]
        ],

        # hrule
        [
            [
                [
                    re.compile(r"^---$", re.MULTILINE),
                    r"\\hrulefill\\\\"
                ]
            ],
            [

            ]
        ],

        # heading 3
        [
            [ # good match - there can be a couple of good matches
                [
                    re.compile(r"^\s*### (.{0,})$"), # template
                    r"\\subsubsection*{\1}" # substitute with
                ],
            ], # bad matches, you can have empty bad matches
            [
                [
                    # no space case
                    re.compile(r"^\s*###([^ ].{1,})", re.MULTILINE),
                    lambda line, col, string: f"Warning: \"{string}\" is a potential heading 3 at line {line}, col {col}"
                ],
            ]
        ],

        # heading 2
        [
            [
                [
                    re.compile(r"^\s*## (.{0,})", re.MULTILINE),
                    r"\\subsection*{\1}"
                ]
            ],
            [
                [
                    re.compile(r"^\s*##([^ #].{1,})", re.MULTILINE),
                    lambda line, col, string: f"Warning: \"{string}\" is a potential heading 2 at line {line}, col {col}"
                ]
            ]
        ],

        # heading 1
        [
            [
                [
                    re.compile(r"^\s*# (.{0,})", re.MULTILINE),
                    r"\\section*{\1}"
                ]
            ],
            [
                [
                    re.compile(r"^\s*#([^ #].{1,})", re.MULTILINE),
                    lambda line, col, string: f"Warning: \"{string}\" is a potential heading 1 at line {line}, col {col}"
                ]
            ]
        ],

    ]

    # Substitutions
    lines = text.splitlines()

    for i in range(len(lines)):
        for case in cases:
            good_cases, bad_cases = case
            # print(good_cases)
            for good_case in good_cases:
                pattern, sub = good_case
                lines[i], n = pattern.subn(sub, lines[i])
                # print(lines[i])
                if n == 0:
                    for bad_case in bad_cases:
                        pattern, message = bad_case
                        matches = pattern.finditer(lines[i])
                        for match in matches:
                            print(message(i + 1, match.span()[0] + 1, lines[i]))
    return "\n".join(lines)

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
% packages
\\usepackage{hyperref}
\\usepackage[a4paper, margin=2cm]{geometry}
\\usepackage{graphicx}
\\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=blue,
    pdfpagemode=FullScreen,
    }
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
