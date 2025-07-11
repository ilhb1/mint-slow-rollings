import ply.lex as lex
import ply.yacc as yacc
import re

from thompson import V

# TODO CONSIDER TWO PARSERS
# TODO IMPLEMENT == 

# COMMANDS TO IMPLEMENT:
# - make revealing
# - draw
# - help

class M_Lexer:
    # List of token names.   This is always required
    tokens = (
       'BSTRING',
       'GENCOMMAND',
       'DEFINEEQUALS',
       'CHECKEQUALS',
       'VAR',
       'COMPOSE',
       'NEG',
       'CONJ',
       'LPAREN',
       'RPAREN',
       'LSQBRACKET',
       'RSQBRACKET',
       'COMMA',
       'APPLY',
       'DEFCOMMAND',
       'NUMBER'
       # 'BOOLEAN'
    )

    # Regular expression rules for simple tokens
    t_GENCOMMAND = r'\/[A-Za-z0-9]+'
    t_DEFINEEQUALS = r':='
    t_CHECKEQUALS = r'='
    t_COMPOSE = r'\*'
    t_NEG = r'\!'
    t_CONJ = r'\^'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LSQBRACKET  = r'\['
    t_RSQBRACKET  = r'\]'
    t_COMMA = r','
    t_VAR = r'[a-zA-Z][a-zA-Z0-9]+'
    t_BSTRING = r"""('[01]+')|("[01]+")"""
    t_APPLY = r'\|'
    t_DEFCOMMAND = r'(def_from_dfs)|(def_from_achains)'
    t_NUMBER = r'[0-9]+'
    # t_BOOLEAN = r'(true)|(false)'

    
    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)
    def get_tokens(self): 
        return self.tokens

class M_Parser():
    def __init__(self, my_lex, dictionary = None):
        self.variables = {}
        if dictionary is not None:
            self.variables = self.variables | dictionary
        self.command_queue = []
        tokens = my_lex.get_tokens()
        def p_statement(p):
            '''statement  : command
                   | equation
                   | expression'''
            p[0] = p[1]

        def p_command(p):
            'command : GENCOMMAND params'
            # print("appending to command queue", p[1], p[2])
            self.command_queue.append((p[1], p[2]))

        def p_equation(p):
            'equation : VAR DEFINEEQUALS expression'
            p[0] = p[1] # I believe this works, but has the side effect of allowing inline definitions with (varname := deffunc())
            self.variables[p[1]] = p[3]

        def p_expression(p):
            '''expression : expression COMPOSE expression
               | LPAREN expression RPAREN
               | NEG expression
               | expression CONJ expression
               | VAR
               | DEFCOMMAND args'''
            if len(p) == 4 and p[2] == '*':
                p[0] = V.product(p[1], p[3])
            elif len(p) == 4 and p[2] == '^':
                p[0] = V.conjugate(p[1], p[3])
            elif len(p) == 3:
                if p[1] == '!':
                    p[0] = V.invert(p[2])
                elif p[1] == "def_from_achains":
                    print(p[2])
                    p[0] = V.init_with_antichains(p[2][0],p[2][1], p[2][2])
                    #debug
                    # print(p[0].D, p[0].R)
                elif p[1] == "def_from_dfs":
                    #debug
                    p[0] = V.init_with_DFS(p[2][0],p[2][1],p[2][2])
                    # print(p[0].D, p[0].R)
            elif len(p) == 4 and type(p[2]) == V:
                p[0] = p[2]
            elif len(p) == 2:
                p[0] = self.variables[p[1]]
                

        # assume right actions for now TODO implement switch
        def p_apply(p):
            '''word : word APPLY expression
                       | BSTRING '''
            if (len(p) == 4):
                # checks if the expression is an object of type V or a named variable
                if type(p[3]) is str:
                    p[0] = p[3].apply(self.variables[p[1]])  
                elif type(p[3]) is V:
                    p[0] = p[3].apply(p[1])  
            elif (len(p) == 2):
                p[0] = p[1]

        def p_args(p):
            '''args : LPAREN params RPAREN'''
            p[0] = p[2]

        def p_list(p):
            '''list : LSQBRACKET params RSQBRACKET'''
            p[0] = p[2]

        def p_params(p):
            '''params : params COMMA param
                      | param'''
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]

        def p_param(p):
            # this param may not be just VAR
            '''param : list 
                     | VAR 
                     | NUMBER 
                     | BSTRING'''
            if type(p[1]) is list:
                p[0] = p[1]
            elif re.compile("""('[01]+')|("[01]+")""").match(p[1]) is not None:
                p[0] = p[1][1:-1]
            elif p[1].isdigit():
                p[0] = int(p[1])
            else:
                p[0] = p[1]

        # Error rule for syntax errors
        def p_error(p):
            print("Syntax error in input!", p)
            # print("Whoa. You are seriously hosed.")
            # if not p:
                # print("End of File!")
                # return

            # # Read ahead looking for a closing '}'
            # while True:
                # tok = self.parser.token()             # Get the next token
                # if not tok or tok.type == 'RBRACE':
                    # break
            # self.parser.restart()

        self.parser = yacc.yacc()

# l = M_Lexer()
# l.build()
# # # l.test("/command")
# # l.test("/definite test := A ^ B + = !word")

# p = M_Parser(l)
# # p.parser.parse("/show(a,b)")
# # p.parser.parse("pa1, par2, pa13")
# # s = "0101|asfg"
# # s = "asdba + asfb"
# # s = "/show(asdb)"
# # s = "/definite test := A ^ B + = !word"
# # l.test(s)
# # res = p.parser.parse(s)

# res = p.parser.parse("""var := def_from_achains(["0","1"], ["0", "1"], [1,0]")""", debug=True)
# print(res)
# print(p.variables[res])

# while True:
    # string = input()
    # res = p.parser.parse(string)
    # print(res)
    # print(p.variables[res])

class Engine:
    # contains lexer and parser for arithmetic with elements of V
    # should be asynchronously accessible by other threads
    # text input in terms of commands 
    """
    statement  : command
               : equation
               : expression

    command    : GENCOMMAND params

    params     : LPAREN params COMMA VAR RPAREN
               | LPAREN VAR RPAREN

    equation   : VAR DEFINEEQUALS expression

    // right actions
    word : word APPLY expression
            | BSTRING
    // or left actions
    word : expression LPAREN BSTRING RPAREN
            | BSTRING

    expression : expression COMPOSE expression
               | LPAREN expression RPAREN
               | NEG expression
               | expression CONJ expression
               | VAR
               | DEFCOMMAND LPAREN list COMMA list RPAREN
               | DEFCOMMAND LPAREN BSTRING COMMA list RPAREN

    # list       : LSQBRACKET rest RSQBRACKET
    list       : LSQBRACKET params RSQBRACKET

    # rest       : ELEM COMPOSE rest
               # | ELEM

    # DEFCOMMAND : def_from_achains
               # | def_from_dfs
    """ 
    def __init__(self, startup_var={}):
        self.lexer = M_Lexer()
        self.lexer.build()
        self.parser = M_Parser(self.lexer, startup_var)

    def parse_string(self, string, debug=False):
        return self.parser.parser.parse(string, debug=debug)

    def get_variables(self):
        return self.parser.variables

    def get_command(self):
        if len(self.parser.command_queue) != 0:
            return self.parser.command_queue.pop()
        return None

    def exec_command(self):
        command = self.get_command()
        if command != None:

            variables = self.get_variables()
            if command[0] == "/show":
                for i in command[1]:
                    print(variables[i])
                    


