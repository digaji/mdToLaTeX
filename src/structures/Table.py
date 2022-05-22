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
    
    def print(self):
        if len(self.rows) == 0:
            return
        line_pat = re.compile(r"[ -:]+")
        match_all = lambda cols: all(map(lambda s : not (line_pat.match(s) is None), cols))
        # set the number of columns to be the number of columns of the first row
        ncols = self.rows[0].ncols 
        ind_str = "  "
        ind_lev = 1
        print("\\begin{tabular}{" + "|" + "c|" * ncols + "}")
        print(ind_str * ind_lev + "\\hline")
        for i, row in enumerate(self.rows):
            if (i == 1) and (match_all(row.cols)):
                continue
            c = 0
            while c < ncols:
                if c < row.ncols:
                    if c == 0:
                        print(ind_str * ind_lev + row.cols[c], sep="", end="")
                    else:
                        print(f" & {row.cols[c]}", sep="", end="")
                else:
                    print(f" & ", sep="", end="")
                c += 1
            print("\\\\\n" + ind_str * ind_lev + "\\hline")
        print("\\end{tabular}")
    