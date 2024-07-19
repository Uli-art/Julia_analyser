from token_struct import Token
from token_struct import Token, TokenError, TOKEN_ERROR_DESCRIPTION
from kind_of_token import Type, KEYWORDS, OPEN_BRACKETS, CLOSE_BRACKETS, COMPARISON_WORDS, OPS_REVERSE


class MyException(Exception):
    pass


def create_id_table(tokens):
    count = 1
    identifiers = dict()

    for cur_token in tokens:
        if cur_token.token_error == TokenError.NO_ERR:
            if cur_token.kind in (Type.IDENTIFIER, Type.CHAR, Type.STRING, Type.INTEGER, Type.HEX_INT, Type.OCT_INT,
                                  Type.BIN_INT, Type.STRING, Type.TRIPLE_STRING, Type.FLOAT):
                exists = False
                for id in identifiers.keys():
                    if identifiers[id].kind == cur_token.kind and identifiers[id].value == cur_token.value:
                        exists = True
                if not exists:
                    new_id = "id_" + str(count)
                    identifiers[new_id] = cur_token
                    count += 1

    return identifiers


def print_identifier_table(identifiers):
    print("{:<13} {:<17} {:<10}".format('Identifier', 'Kind', 'Value'))
    for k, v in identifiers.items():
        print("{:<13} {:<17} {:<10}".format(k, v.kind, v.value))


def update_code_with_id(tokens, identifiers):
    code_with_id = ""

    for token in tokens:
        if token.token_error != TokenError.NO_ERR:
            raise MyException(TOKEN_ERROR_DESCRIPTION[token.token_error])
        is_identifier = False
        for key, value in identifiers.items():
            if token.kind == value.kind and token.value == value.value:
                code_with_id += "<" + key + ">"
                is_identifier = True
                continue
        if not is_identifier:
            code_with_id += " " + token.value + " "

    return code_with_id


def update_code(code, tokens, identifiers):
    code_with_id = ""
    position = 0
    count = 0
    while position < len(code):
        char = code[position]

        if code[position] in (" ", '\n', '\t'):
            code_with_id += code[position]
        else:
            if count >= len(tokens):
                return code_with_id
            token = tokens[count]
            if token.token_error != TokenError.NO_ERR:
                raise MyException(TOKEN_ERROR_DESCRIPTION[token.token_error])
            is_identifier = False
            for key, value in identifiers.items():
                if token.kind == value.kind and token.value == value.value:
                    code_with_id += "<" + key + ">"
                    position += len(token.value) - 1
                    is_identifier = True
                    continue
            if not is_identifier:
                code_with_id += token.value
                position += len(token.value) - 1
            count += 1
        position += 1

    return code_with_id
