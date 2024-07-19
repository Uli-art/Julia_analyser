from enum import Enum

from kind_of_token import Type


class TokenError(Enum):
    NO_ERR = 0
    EOF_MULTICOMMENT = 1
    EOF_STRING = 2
    EOF_CHAR = 3
    EOF_BRACKETS = 4
    INVALID_NUMERIC_CONSTANT = 5
    INVALID_OPERATOR = 6
    UNKNOWN = 7
    TYPO = 8


TOKEN_ERROR_DESCRIPTION = {
    TokenError.NO_ERR: "no error",
    TokenError.EOF_MULTICOMMENT: "unterminated multi-line comment #= ... =#",
    TokenError.EOF_STRING: "unterminated string literal",
    TokenError.EOF_CHAR: "unterminated character literal",
    TokenError.EOF_BRACKETS: "unterminated brackets",
    TokenError.INVALID_NUMERIC_CONSTANT: "invalid numeric constant",
    TokenError.INVALID_OPERATOR: "invalid operator",
    TokenError.TYPO: "typographical error",
    TokenError.UNKNOWN: "unknown",
}


class Token:
    def __init__(self, kind, value, token_error: TokenError, row, col):
        self.kind = kind
        self.value = value
        self.token_error = token_error
        self.row = row
        self.col = col


def kind(token):
    return token.kind


def print_token(token):
    str_val = token.value if token.kind != Type.ENDMARKER else ""
    if token.token_error == TokenError.NO_ERR:
        print(str(kind(token)).ljust(15), end=' ')
        print(f'"{str_val}"')
    else:
        print(f'"{str_val}" ' + TOKEN_ERROR_DESCRIPTION[token.token_error])
