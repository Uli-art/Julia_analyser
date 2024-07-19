from identifier_table import create_id_table, print_identifier_table, update_code_with_id, update_code, MyException
from tokenizer import JuliaTokenizer
from syntax_analiser import JuliaSyntax, print_parse_tree
from token_struct import print_token, TokenError, TOKEN_ERROR_DESCRIPTION
from tkinter import filedialog as fd


def select_file():
    filetypes = (
        ('text files', '*.txt'),
    )
    return fd.askopenfilename(
        title='Open a file',
        initialdir='C:\\Users\\ulyas\\Documents\\6_sem\\MTran\\Lab_2\\tests',
        filetypes=filetypes)


if __name__ == '__main__':
    filename = select_file()

    with open(filename) as f:
        julia_code = f.read()

    tokenizer = JuliaTokenizer(julia_code)
    tokens = tokenizer.tokenize()
    identifiers = create_id_table(tokens)

    syntax_analyser = JuliaSyntax(tokens, identifiers)
    tree = syntax_analyser.syntax_tree()
    print_parse_tree(tree)

    # print("{:<17} {:<10}".format('Kind', 'Value'))
    # print("{:<17} {:<10}".format('-----', '------'))
    # for token in tokens:
    #     if token.token_error != TokenError.NO_ERR:
    #         exception = TOKEN_ERROR_DESCRIPTION[token.token_error] + " in '" + str(token.value) + "'"
    #         raise MyException(exception)
    #     print("{:<17} {:<10}".format(token.kind, token.value))
    #
    # print('\n')
    # identifiers = create_id_table(tokens)
    # print_identifier_table(identifiers)
    #
    # print('\n')
    # print(update_code(julia_code, tokens, identifiers))
