from lexer import OrderedLi, TableRow, UnorderedLi, BlockQuote, Lexer

class TableBlock:

    def __init__(self):
        self.rows: list[TableRow] = []
    
    def add_row(self, row: TableRow):
        self.rows.append(row)
    
    def __repr__(self):
        s = f"Table(\n"
        for row in self.rows:
            s += "  " + str(row) + "\n"
        s += ")"
        return s

class UnorderedBlock:

    def __init__(self):
        self.items: list[UnorderedLi] = []
    
    def add_item(self, item: UnorderedLi):
        self.items.append(item)
    
    def __repr__(self):
        s = "UnorderedBlock(\n"
        for item in self.items:
            s += "  " + str(item) + "\n"
        s += ")"
        return s

class OrderedBlock:

    def __init__(self):
        self.items: list[OrderedLi] = []
    
    def add_item(self, item: OrderedLi):
        self.items.append(item)
    
    def __repr__(self):
        s = "OrderedBlock(\n"
        for item in self.items:
            s += "  " + str(item) + "\n"
        s += ")"
        return s

class BlockQuoteBlock:

    def __init__(self):
        self.items: list[BlockQuote] = []
    
    def add_item(self, item: BlockQuote):
        self.items.append(item)
    
    def __repr__(self):
        s = "BlockQuoteBlock(\n"
        for item in self.items:
            s += "  " + str(item) + "\n"
        s += ")"
        return s

class TokenPointer:

    def __init__(self, tokens, current = 0):
        self.tokens = tokens
        self.current = current
    
    def at_end(self):
        return self.current == len(self.tokens)
    
    def peek(self, n = 1) -> str: # looks at the current 
        if self.current + n > len(self.tokens):
            return None
        if n == 1:
            return self.tokens[self.current]
        return self.tokens[self.current:self.current + n]
    
    def peek_back(self, n = 1):
        if self.current - n < 0:
            return None
        return self.tokens[self.current - n:self.current]
    
    def move(self, n = 1):
        if n < 0:
            raise Exception("n must be a positive integer")
        if n == 0:
            return self.peek()

        
        if self.current + n > len(self.tokens):
            before = self.current
            self.current = len(self.tokens)
            return self.tokens[before:self.current]

        before = self.current
        self.current += n
        return self.tokens[before:self.current]
    
    def back(self, n = 1):
        if n < 0:
            raise Exception("n must be a positive integer")
        if n == 0:
            return self.peek()

        
        if self.current - n < 0:
            before = self.current
            self.current = 0
            return self.tokens[self.current:before]
        
        before = self.current
        self.current -= n
        return self.text[before:self.current]
    
    def copy(self):
        return TokenPointer(self.tokens, self.current)
    
class Parser:

    def __init__(self, tokens):
        self.main = TokenPointer(tokens)
    
    def parse_table_block(self):
        if type(self.main.peek()) is TableRow:
            tb = TableBlock()
            head: TableRow = self.main.peek()
            col = len(head.columns)
            tb.add_row(head)
            self.main.move()

            # want to get head separator row
            if (type(self.main.peek()) is TableRow):
                sep: TableRow = self.main.peek()
                if len(sep.columns) != col:
                    raise Exception(f"Number of columns of table row on line {sep.line} col {sep.col} does not match it's head")
                
                for column in sep.columns:
                    if column.content.count('-') == 0:
                        raise Exception(f"Table row separator on line {sep.line} and col {sep.col} must contain atleast one '-' character")
                    if not all(s in '-:' for s in column.content):
                        raise Exception(f"Table row separator on line {sep.line} and col {sep.col} must only contain '-' character")
                self.main.move()

                while type(self.main.peek()) is TableRow:
                    row: TableRow = self.main.peek()
                    if (len(row.columns) != col):
                        raise Exception(f"Number of columns of table row on line {row.line} and col {row.col} does not match it's head")
                    # add it
                    tb.add_row(row)
                    self.main.move()
                return tb
            else:
                raise Exception(f"Cannot have table head only on line {head.line} col {head.col}, must have at least a head separator")
    
    def parse_unordered_block_children(self, depth_child = 0):
        item = self.main.peek()
        if type(item) is UnorderedLi:
            if (item.depth == depth_child):
                ub = UnorderedBlock()
                while (type(item) is UnorderedLi) and (item.depth == depth_child):
                    self.main.move()
                    child = self.parse_unordered_block_children(item.depth + 1)
                    if child:
                        item.children.append(child)
                    ub.add_item(item)
                    item = self.main.peek()
                return ub
            elif item.depth > depth_child:
                raise Exception(f"Depth of UnorderedLi item at line {item.line} col {item.col} does not match parent child depth")
    
    def parse_unordered_block(self):
        item = self.main.peek()
        if type(item) is UnorderedLi:
            if item.depth == 0:
                ub = UnorderedBlock()
                while (type(item) is UnorderedLi) and (item.depth == 0):
                    ub.add_item(item)
                    self.main.move()
                    child = self.parse_unordered_block_children(1)
                    if (child):
                        item.children.append(child)
                    item = self.main.peek()
                return ub
            else:
                raise Exception(f"UnorderedLi item at line {item.line} col {item.col} does not have a parent, its depth must be zero")

    def parse_ordered_block_children(self, depth_child = 0):
        item = self.main.peek()
        if type(item) is OrderedLi:
            if (item.depth == depth_child):
                ub = OrderedBlock()
                while (type(item) is OrderedLi) and (item.depth == depth_child):
                    self.main.move()
                    child = self.parse_ordered_block_children(item.depth + 1)
                    if child:
                        item.children.append(child)
                    ub.add_item(item)
                    item = self.main.peek()
                return ub
            elif item.depth > depth_child:
                raise Exception(f"Depth of OrderedLi item at line {item.line} col {item.col} does not match parent child depth")
    
    def parse_ordered_block(self):
        item = self.main.peek()
        if type(item) is OrderedLi:
            if item.depth == 0:
                ub = OrderedBlock()
                while (type(item) is OrderedLi) and (item.depth == 0):
                    ub.add_item(item)
                    self.main.move()
                    child = self.parse_ordered_block_children(1)
                    if (child):
                        item.children.append(child)
                    item = self.main.peek()
                return ub
            else:
                raise Exception(f"OrderedLi item at line {item.line} col {item.col} does not have a parent, its depth must be zero")

    def parse_block_quote_block_children(self, depth_child = 0):
        item = self.main.peek()
        if type(item) is BlockQuote:
            if (item.depth == depth_child):
                ub = BlockQuoteBlock()
                while (type(item) is BlockQuote) and (item.depth == depth_child):
                    self.main.move()
                    child = self.parse_block_quote_block_children(item.depth + 1)
                    if child:
                        item.children.append(child)
                    ub.add_item(item)
                    item = self.main.peek()
                return ub
            elif item.depth > depth_child:
                raise Exception(f"Depth of BlockQuote item at line {item.line} col {item.col} does not match parent child depth")
    
    def parse_block_quote_block(self):
        item = self.main.peek()
        if type(item) is BlockQuote:
            if item.depth == 1:
                bqb = BlockQuoteBlock()
                while (type(item) is BlockQuote) and (item.depth == 1):
                    bqb.add_item(item)
                    self.main.move()
                    child = self.parse_block_quote_block_children(2)
                    if (child):
                        item.children.append(child)
                    item = self.main.peek()
                return bqb
            else:
                raise Exception(f"BlockQuote item at line {item.line} col {item.col} does not have a parent, its depth must be zero")
    
    def parse(self):
        document = []
        while not (self.main.at_end()):
            block = None

            block = self.parse_table_block()
            if not (block is None):
                document.append(block)
                continue
        
            block = self.parse_unordered_block()
            if not (block is None):
                document.append(block)
                continue

            block = self.parse_ordered_block()
            if not (block is None):
                document.append(block)
                continue

            block = self.parse_block_quote_block()
            if not (block is None):
                document.append(block)
                continue

            block = self.main.peek()
            self.main.move()
            document.append(block)

        return document




def main():
    '''
    Main Program entry point
    '''
    with open("test.txt", "r") as f:
        text = f.read()
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    document = parser.parse()
    for block in document:
        print(block)

if __name__ == '__main__':
    main()