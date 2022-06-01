import re
class Row:

    def __init__(self, ln: int, *cols: list[str]):
        self.ln = ln
        self.ncols = len(cols)
        self.cols: list[str] = [s.strip() for s in cols]
    
    def __str__(self):
        return f"Row({self.ln = }, {self.cols = }, {self.ncols = })"
    
    def __repr__(self):
        return self.__str__()

class Table:

    def __init__(self):
        self.rows: list[Row] = []
    
    def addRow(self, item: Row) -> None:
        self.rows.append(item)
    
    def print(self, f = None):
        if len(self.rows) == 0:
            return
        line_pat = re.compile(r"[ -:]+")
        match_all = lambda cols: all(map(lambda s : not (line_pat.match(s) is None), cols))
        # set the number of columns to be the number of columns of the first row
        ncols = self.rows[0].ncols 
        ind_str = "  "
        ind_lev = 1
        if not f:
            print("\\begin{tabular}{" + "|" + "c|" * ncols + "}")
        else:
            f.write("\\begin{tabular}{" + "|" + "c|" * ncols + "}\n")
        if not f:
            print(ind_str * ind_lev + "\\hline")
        else:
            f.write(ind_str * ind_lev + "\\hline\n")
        for i, row in enumerate(self.rows):
            if (i == 1) and (match_all(row.cols)):
                continue
            c = 0
            while c < ncols:
                if c < row.ncols:
                    if c == 0:
                        if not f:
                            print(ind_str * ind_lev + row.cols[c], sep="", end="")
                        else:
                            f.write(ind_str * ind_lev + row.cols[c])
                    else:
                        if not f:
                            print(f" & {row.cols[c]}", sep="", end="")
                        else:
                            f.write(f" & {row.cols[c]}")
                else:
                    if not f:
                        print(f" & ", sep="", end="")
                    else:
                        f.write(f" & ")
                c += 1
            if not f:
                print("\\\\\n" + ind_str * ind_lev + "\\hline")
            else:
                f.write("\\\\\n" + ind_str * ind_lev + "\\hline\n")
        if not f:
            print("\\end{tabular}")
        else:
            f.write("\\end{tabular}\n")


    def total_lines(self):
        return 2 * len(self.rows) + 3

    def markdown_lines_range(self):
        return (self.rows[0].ln, self.rows[-1].ln)
    
    def latex_lines_range(self):
        return (self.rows[0].ln, self.rows[0].ln + self.total_lines() - 1)
    
    def inject(self):
        return (self.markdown_lines_range(), self.total_lines(), self)
    
    