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
from ply import lex
import unicodedata
import re


def get_unicode_name(character):
    # replace non-alphanumeric characters with underscores
    sc = re.sub(r"[^a-zA-Z0-9]", "_", unicodedata.name(character))
    # convert to uppercase
    sc = sc.upper()
    # remove leading and trailing underscores
    sc = sc.strip("_")
    # replace consecutive underscores with a single underscore
    sc = re.sub(r"_+", "_", sc)
    # return upper snake cased character name
    return sc


# --


class Token(lex.LexToken):
    """
    This class describes a simple token wrapper.
    @see REBNFLexer.tokenize
    """

    def __init__(self, token: lex.LexToken):
        assert isinstance(token, lex.LexToken)
        super().__init__()
        self.__dict__.update(token.__dict__)

    @property
    def lcpos(self):
        return (
            self.lineno,
            self.column,
        )

    def __str__(self):
        return f"{self.__class__.__name__}({self.type}, {repr(self.value)}, {self.lcpos}, {self.lexpos})"


# --

# def group(*choices): return '(' + '|'.join(choices) + ')'
# def maybe(*choices): return group(*choices) + '?'

# --

literal_type_map = {
    '>': 'GREATER',
    '{': 'LBRACE',
    '<': 'LESS',
    '(': 'LPAR',
    '[': 'LSQB',
    '-': 'MINUS',
    '+': 'PLUS',
    '}': 'RBRACE',
    ')': 'RPAR',
    ']': 'RSQB',
    ';': 'SEMICOLON',
    '*': 'ASTERISK',
    '|': 'VBAR',
    '?': 'OPTIONAL',
    '.': 'DOT',
    # "...": "ELLIPSIS",
}


class REBNFLexer(object):
    """
    This class describes a rebnf lexer.
    """

    literals = literal_type_map.keys()

    tokens = (
        "ASSIGN",
        "COMMENT",
        "NAME",
        "NEWLINE",
        "REGEX",
        "STRING",
        *literal_type_map.values(),
    )

    t_ASSIGN = r"::=|:|="
    t_ignore = " \t\r\f\b"

    def t_NEWLINE(self, t):
        r"\n"
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_STRING(self, t):
        r"r?(\'[^\n\'\\]*(\\.[^\n\'\\]*)*\'|\"[^\n\"\\]*(\\.[^\n\"\\]*)*\")"
        if t.value.startswith("r"):
            t.type = "REGEX"
        return t

    def t_COMMENT(self, t):
        r"(\#.*\n?|\(\*(?:.|\n)*?\*\))"
        t.lexer.lineno += t.value.count("\n")
        return t

    @lex.TOKEN("|".join(re.escape(k) for k in literal_type_map.keys()))
    def t_LITERAL(self, t):
        t.type = literal_type_map.get(t.value)
        return t

    # @lex.TOKEN('|'.join([
    #     r"import\ +(\w+(?:\ +as\ +\w+)?)",
    #     r"from\ +(\.*\w+(?:\.\w+)*)\ +import\ +(\w+(?:\ +as\ +\w+)?(?:,\ *\w+(?:\ +as\ +\w+)?)*)\ *",
    #     r"from\ +(\.*\w+(?:\.\w+)*)\ +import\ +\(\s+(\w+(?:\ +as\ +\w+)?(?:,\s+\w+(?:\ +as\ +\w+)?)*)\ *",
    # ]))
    # def t_IMPORT(self, t):
    #     return t

    def t_NAME(self, t):
        r"<[a-zA-Z][a-zA-Z0-9_]*>|[a-zA-Z][a-zA-Z0-9_]*"
        # support for optional identifier enclosures
        if t.value.startswith("<") and t.value.endswith(">"):
            t.value = t.value[1:-1]
        return t

    # def t_SYMBOL(self, t):
    #     r"<|>|-|\n|\t|\r|\f|\b"
    #     return t

    def find_column(self, data, token):
        line_start = data.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def t_error(self, t):
        print(
            f"\033[91mlexer error: at line {t.lineno}, column {self.find_column(t.lexer.lexdata, t)}, unexpected token {repr(t.value[0])}\033[0m"
        )
        exit(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def token(self):
        return self.lexer.token()

    def tokenize(self, code):
        self.lexer.input(code)
        output = list()
        while tok := self.lexer.token():
            tok.column = self.find_column(self.lexer.lexdata, tok)
            output.append(Token(tok))
        return output
