# The lexer tokenizes the input stream consisting of markdown text
import re
import os
# - Markdown is just fancy plain text

def find_ol_regions():
    pass

def find_ul_regions():
    pass

def lexer(text):
    print(repr(text))
    heading3 = re.compile(r"^\s*### (.{0,})", re.MULTILINE)
    heading3_sub = r"\\subsubsection{\1}"
    heading2 = re.compile(r"^\s*## (.{0,})", re.MULTILINE)
    heading2_sub = r"\\subsection{\1}"
    heading1 = re.compile(r"^\s*# (.{0,})", re.MULTILINE)
    heading1_sub = r"\\section{\1}"

    # Italics and bold are a bit weird when combined in weird ways
    bitalics = re.compile(r"\*\*\*([^\*]+?)\*\*\*");
    bitalics_sub = r"\\textbf{\\textit{\1}}"
    italics = re.compile(r"\*([^\*]+?)\*")
    italics_sub = r"\\textit{\1}"
    bold = re.compile(r"\*\*([^\*]+?)\*\*")
    bold_sub = r"\\textbf{\1}"
    links = re.compile(r"\[(.{0,})\]\((.{0,})\)")
    links_sub = r"\\href{\1}{\2}"

    # ordered lists
    # testing ordered lists
    print(re.findall(r"^\s*(\d+\. \w+)\n", text, re.MULTILINE))

    # unordered lists

    text = bold.sub(bold_sub, text)
    text = italics.sub(italics_sub, text)
    text = bitalics.sub(bitalics_sub, text)
    text = links.sub(links_sub, text)
    text = heading3.sub(heading3_sub, text)
    text = heading2.sub(heading2_sub, text)
    text = heading1.sub(heading1_sub, text)

    print(text)
    pass

def main():
    
    filename = "headings.md"
    filepath = os.getcwd() + f"\\tests\\{filename}"
    with open(filepath, "r") as f:
        lexer(''.join(f.readlines()))
    pass

if __name__ == '__main__':
    main()
