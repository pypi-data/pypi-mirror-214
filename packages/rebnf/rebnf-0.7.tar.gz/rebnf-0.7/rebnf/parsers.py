"""
ReBNF: Regexes for Extended Backus-Naur Form (EBNF)

Copyright (C) 2023 opsocket <opsocket@pm.me>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses>.
"""
from . import lexers
from ply import yacc
import itertools


class REBNFParser:
    """
    This class describes a rebnf parser.
    """

    tokens = lexers.REBNFLexer.tokens

    def __init__(self):
        self.lexer = lexers.REBNFLexer()
        self.parser = yacc.yacc(module=self)
        # self.parser = yacc.yacc(module=self, debuglog=yacc.NullLogger())
        self.ast = []

    def p_start(self, p):
        """
        start : grammar start
              | grammar
        """
        p[0] = self.ast

    def p_grammar(self, p):
        '''
        grammar : comment
                | import
                | rule
                | newline
        '''
        if p[1]:
            self.ast += p[1],

    def p_newline(self, p):
        '''
        newline : NEWLINE newline
                | NEWLINE
        '''
        pass

    def p_comment(self, p):
        '''
        comment : COMMENT
        '''
        p[0] = ('COMMENT', p[1])

    # -- IMPORTS --

    def p_import(self, p):
        '''
        import : import_statement newline
               | import_statement
               | from_statement newline
               | from_statement
        '''
        p[0] = ('IMPORT', p[1])

    def p_import_statement(self, p):
        '''
        import_statement : NAME import_items
        '''
        if p[1] == 'import':
            p[0] = tuple(p[1:])

    def p_from_statement(self, p):
        '''
        from_statement : NAME dotted_name NAME ASTERISK
                       | NAME dotted_name NAME import_items
        '''
        if p[1] == "from" and p[3] == "import":
            p[0] = tuple(p[1:])

    def p_dotted_name(self, p):
        """
        dotted_name : dots name_parts
                    | name_parts
        """
        p[0] = "".join(p[1:])

    def p_dotted_name_dots(self, p):
        """
        dots : DOT dots
             | DOT
        """
        p[0] = "".join(p[1:])

    def p_dotted_name_name_parts(self, p):
        """
        name_parts : NAME DOT name_parts
                   | NAME
        """
        p[0] = "".join(p[1:])

    def p_import_items(self, p):
        '''
        import_items : import_name "," import_items
                     | import_name
        '''
        if len(p) == 3:
            p[0] = itertools.chain.from_iterable([p[1], p[2]])
        if len(p) == 2:
            p[0] = p[1]

    def p_import_name(self, p):
        '''
        import_name : NAME NAME NAME
                    | NAME
        '''
        if len(p) == 4 and p[2] == "as":
            # ensure import names / aliases are lower case
            if p[1].islower() and p[3].islower():
                p[0] = [p[1], p[3]]
        elif len(p) == 2 and p[1].islower():
            p[0] = p[1]

    def p_import_items_multiline(self, p):
        '''
        import_items_multiline : LPAR NEWLINE import_name NEWLINE RPAR
        '''

    # -- RULES --

    def p_rule(self, p):
        '''
        rule : NAME ASSIGN rhs terminator
             | NAME ASSIGN rhs
        '''
        p[0] = ('RULE', (p[1], p[3]))

    def p_rhs(self, p):
        '''
        rhs : factor NEWLINE VBAR rhs
            
            | factor VBAR rhs

            | factor NEWLINE
            | factor rhs
            | factor
        '''
        if len(p) == 5:
            p[0] = (p[3], (p[1], p[4]))
        elif len(p) == 4:
            p[0] = (p[2], (p[1], p[3]))
        elif len(p) == 3:
            p[0] = p[1]
            if isinstance(p[2], (list, tuple)):
                p[0] = (p[1], p[2])
            else:
                if p[2] != "\n":
                    p[0] = (p[1], p[2])
                else:
                    p[0] = p[1]
        elif len(p) == 2:
            p[0] = p[1]

    def p_factor(self, p):
        """
        factor : term OPTIONAL
               | term ASTERISK
               | term PLUS
               | term MINUS term
               | term
        """
        if len(p) == 4:
            p[0] = [p[2], [p[1], p[3]]]
        elif len(p) == 3:
            p[0] =  [p[2], p[1]]
        else:
            p[0] = p[1]

    def p_term_group(self, p):
        '''
        term_group : factor NEWLINE VBAR term_group
                   | factor VBAR term_group
                   | factor term_group
                   | factor
        '''
        if len(p) == 5:
            p[0] = (p[3], [p[1], p[4]])
        elif len(p) == 4:
            p[0] = (p[2], [p[1], p[3]])
        elif len(p) == 3:
            p[0] = ('CONCAT', (p[1], p[2]))
        elif len(p) == 2:
            p[0] = p[1]

    def p_term(self, p):
        """
        term : LPAR term_group RPAR
             | LSQB term_group RSQB
             | LBRACE term_group RBRACE
             | regex
             | string
             | name
        """
        if len(p) == 4:
            p[0] = (lexers.literal_type_map.get(p[1]), p[2])
        elif len(p) == 2:
            p[0] = p[1]

    def p_regex(self, p):
        '''
        regex : REGEX
        '''
        p[0] = ('REGEX', p[1])

    def p_string(self, p):
        '''
        string : STRING
        '''
        p[0] = ('STRING', p[1])

    def p_name(self, p):
        '''
        name : NAME
        '''
        p[0] = ('NAME', p[1])

    def p_terminator(self, p):
        '''
        terminator : SEMICOLON
                   | DOT
        '''
        p[0] = ('TERMINATOR', p[1])

    def find_column(self, lexdata, lexpos):
        line_start = lexdata.rfind("\n", 0, lexpos) + 1
        return (lexpos - line_start) + 1

    def p_error(self, t):
        if t is not None:
            print('error', self.parser.state)
            print(
                f"\033[91msyntax error: at line {t.lineno}, column {self.find_column(t.lexer.lexdata, t.lexpos)}, unexpected token {repr(t.value[0])}\033[0m"
            )
            exit(1)

    def parse(self, code, tracking=True):
        self.parser.parse(code, tracking=tracking)
        return self.ast
