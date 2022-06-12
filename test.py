from lexer import TextPointer

def test_TextPointer():
    p = TextPointer("hello\nhello * *** hi hi")
    s0 = p.move_next_line_until("***")
    s1 = p.move_next_line_until("***")
    s2 = p.move_next_line_until("***")
    print(repr(s0))
    print(repr(s1))
    print(repr(s2))

if __name__ == '__main__':
    test_TextPointer()