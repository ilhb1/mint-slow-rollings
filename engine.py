class Engine:
    # TODO : the whole thing
    # contains lexer and parser for arithmetic with elements of V
    # should be asynchronously accessible by other threads
    # text input in terms of commands 
    
    def __init__(self):
        self.vars = {}
        self.commands = {}
