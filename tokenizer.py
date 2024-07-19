from token_struct import Token, TokenError
from kind_of_token import Type, KEYWORDS, OPEN_BRACKETS, CLOSE_BRACKETS, COMPARISON_WORDS, OPS_REVERSE


class JuliaTokenizer:
    def __init__(self, code):
        self.code = code
        self.position = -1
        self.tokens = []
        self.brackets = ""
        self.row = 1
        self.col = 0

    def tokenize(self):
        while self.position < len(self.code):
            char = self.next_char()

            if char == Type.ENDMARKER:
                if len(self.brackets) != 0:
                    self.tokens.append(
                        Token(OPEN_BRACKETS[self.brackets[0]], self.brackets[0], TokenError.EOF_BRACKETS,
                              self.row, self.col))
                break
            elif char == '\n':
                self.row += 1
                self.col = 0
                continue
            elif char.isspace():
                self.col += 1
                continue
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                if self.is_keyword(identifier):
                    self.tokens.append(Token(Type.KEYWORD, identifier, TokenError.NO_ERR,
                              self.row, self.col))
                    self.col += len(identifier)
                    continue
                if self.is_comparison(identifier):
                    if identifier == "in":
                        self.tokens.append(Token(Type.IN, identifier, TokenError.NO_ERR,
                              self.row, self.col))
                    else:
                        self.tokens.append(Token(Type.ISA, identifier, TokenError.NO_ERR,
                              self.row, self.col))
                    self.col += len(identifier)
                    continue
                # kword = self.is_keyword_typo(identifier)
                # if kword:
                #     self.tokens.append(Token(kword, identifier, TokenError.TYPO,
                #               self.row, self.col))
                #     self.col += len(identifier)
                #     continue

                self.tokens.append(Token(Type.IDENTIFIER, identifier, TokenError.NO_ERR,
                              self.row, self.col))
                self.col += len(identifier)
                continue
            elif char.isdigit():
                number = self.read_number()
                if self.is_decimal_literal(number):
                    self.tokens.append(Token(Type.INTEGER, number, TokenError.NO_ERR,
                              self.row, self.col))
                    self.col += len(number)
                    continue
                elif len(number) >= 2:
                    if number[0] == '0':
                        if number[1] == 'b':
                            if self.is_binary_literal(number):
                                self.tokens.append(Token(Type.BIN_INT, number, TokenError.NO_ERR, self.row, self.col))
                            else:
                                self.tokens.append(Token(Type.BIN_INT, number, TokenError.INVALID_NUMERIC_CONSTANT,
                                                         self.row, self.col))
                            self.col += len(number)
                            continue
                        elif number[1] == 'o':
                            if self.is_octal_literal(number):
                                self.tokens.append(Token(Type.OCT_INT, number, TokenError.NO_ERR, self.row, self.col))
                            else:
                                self.tokens.append(Token(Type.OCT_INT, number, TokenError.INVALID_NUMERIC_CONSTANT,
                                                         self.row, self.col))
                            self.col += len(number)
                            continue
                        elif number[1] == 'x':
                            if self.is_hex_literal(number):
                                self.tokens.append(Token(Type.HEX_INT, number, TokenError.NO_ERR, self.row, self.col))
                            else:
                                self.tokens.append(Token(Type.HEX_INT, number, TokenError.INVALID_NUMERIC_CONSTANT,
                                                         self.row, self.col))
                            self.col += len(number)
                            continue
                    if self.is_float_literal(number):
                        self.tokens.append(Token(Type.FLOAT, number, TokenError.NO_ERR, self.row, self.col))
                        self.col += len(number)
                        continue
                self.tokens.append(Token(Type.INTEGER, number, TokenError.INVALID_NUMERIC_CONSTANT, self.row, self.col))
                self.col += len(number)
                continue
            elif char == '#':
                comment = self.read_comment()
                if not comment:
                    self.tokens.append(Token(Type.COMMENT, comment, TokenError.EOF_MULTICOMMENT, self.row, self.col))
                    # self.col += len(comment)
                    continue
            elif char in "()[]{}":
                if char in OPEN_BRACKETS.keys():
                    self.tokens.append(Token(OPEN_BRACKETS[char], char, TokenError.NO_ERR, self.row, self.col))
                    self.brackets += char
                elif char in CLOSE_BRACKETS.keys():
                    if self.check_brackets(char):
                        self.tokens.append(Token(CLOSE_BRACKETS[char], char, TokenError.NO_ERR, self.row, self.col))
                        self.brackets = self.brackets[:-1]
                    else:
                        self.tokens.append(Token(CLOSE_BRACKETS[char], char, TokenError.EOF_BRACKETS, self.row, self.col))
                self.col += 1
            elif char in OPS_REVERSE.keys():
                operator = self.read_comparison_operator()
                if operator in OPS_REVERSE.keys():
                    self.tokens.append(Token(OPS_REVERSE[operator], operator, TokenError.NO_ERR, self.row, self.col))
                else:
                    self.tokens.append(Token(Type.OP, operator, TokenError.INVALID_OPERATOR, self.row, self.col))
                self.col += len(operator)
            elif char == ',':
                self.tokens.append(Token(Type.COMMA, char, TokenError.NO_ERR, self.row, self.col))
                self.col += 1
            elif char == ';':
                self.tokens.append(Token(Type.SEMICOLON, char, TokenError.NO_ERR, self.row, self.col))
                self.col += 1
            elif char == '@':
                self.tokens.append(Token(Type.AT_SIGN, char, TokenError.NO_ERR, self.row, self.col))
                self.col += 1
            elif char == '\'':
                char_literal, error = self.read_char()
                if not error:
                    self.tokens.append(Token(Type.CHAR, char_literal, TokenError.NO_ERR, self.row, self.col))
                    self.col += 1
                    continue
                self.tokens.append(Token(Type.CHAR, char_literal, TokenError.EOF_CHAR, self.row, self.col))
            elif char == '"':
                string, is_triple = self.read_string()
                if string:
                    if is_triple:
                        self.tokens.append(Token(Type.TRIPLE_STRING, string, TokenError.NO_ERR, self.row, self.col))
                    else:
                        self.tokens.append(Token(Type.STRING, string, TokenError.NO_ERR, self.row, self.col))
                    self.col += len(string)
                else:
                    if is_triple:
                        self.tokens.append(Token(Type.TRIPLE_STRING, is_triple, TokenError.EOF_STRING, self.row, self.col))
                    else:
                        self.tokens.append(Token(Type.STRING, is_triple, TokenError.EOF_STRING, self.row, self.col))

        return self.tokens

    def next_char(self):
        if self.position + 1 < len(self.code):
            self.position += 1
            return self.code[self.position]
        return Type.ENDMARKER

    def peek_char(self):
        if self.position + 1 < len(self.code):
            return self.code[self.position + 1]
        return Type.ENDMARKER

    def read_identifier(self):
        start = self.position
        while (self.position < len(self.code) and self.peek_char() != Type.ENDMARKER) and (
                self.peek_char().isalnum() or self.peek_char() == '_'):
            self.next_char()
        return self.code[start:self.position + 1]

    def is_keyword(self, identifier):
        return identifier.lower() in KEYWORDS.keys()

    def is_keyword_typo(self, identifier):
        for kword in KEYWORDS.keys():
            if compare_strings(identifier.lower(), kword) == 1:
                return kword
        return False

    def is_comparison(self, identifier):
        return identifier.lower() in COMPARISON_WORDS

    def read_number(self):
        start = self.position
        while (self.position < len(self.code) and self.peek_char() != Type.ENDMARKER) and (
                self.peek_char().isalnum() or self.peek_char() == '.'):
            self.next_char()
        return self.code[start:self.position + 1]

    def is_binary_literal(self, number):
        for i in range(2, len(number)):
            if number[i] != '0' and number[i] != '1':
                return False
        return True

    def is_octal_literal(self, number):
        for i in range(2, len(number)):
            if not ('0' <= number[i] <= '7'):
                return False
        return True

    def is_decimal_literal(self, number):
        return number.isdigit()

    def is_hex_literal(self, number):
        for i in range(2, len(number)):
            if not (number[i].isdigit() or 'a' <= number[i].lower() <= 'f'):
                return False
        return True

    def is_float_literal(self, number):
        return number.replace(".", "", 1).replace("e-", "", 1).replace("e+", "", 1).isnumeric()

    def read_comment(self):
        start = self.position
        next_char = self.next_char()
        if next_char != '=':
            while (self.position < len(self.code) and self.peek_char() != Type.ENDMARKER) and self.code[self.position] != '\n':
                self.next_char()
            return self.code[start:self.position]

        while (self.position < len(self.code) and self.peek_char() != Type.ENDMARKER) and self.next_char() != '=' and self.peek_char() != '#':
            if self.peek_char() == Type.ENDMARKER:
                return False
        self.next_char()
        return self.code[start:self.position + 1]

    def check_brackets(self, char):
        if len(self.brackets) == 0 or OPEN_BRACKETS[self.brackets[-1]].value[0] + 1 != CLOSE_BRACKETS[char].value[0]:
            return False
        return True

    def read_string(self):
        start = self.position
        quots = '"'
        if self.code.find('"""', self.position) == self.position:
            quots = '"""'
        find_result = self.code.find(quots, self.position + len(quots))
        if find_result == -1:
            self.position = len(self.code) - 1
            return False,  self.code[start:self.position + 1]
        else:
            self.position = find_result + len(quots) - 1
            return self.code[start:self.position + 1], len(quots) == 3

    def read_char(self):
        start = self.position
        find_result = self.code.find("'", self.position + 1)
        if find_result == -1:
            self.position = len(self.code) - 1
            return self.code[start:self.position + 1], True
        else:
            self.position = find_result
            if self.position - start > 2:
                return self.code[start:self.position + 1], True
            return self.code[start:self.position + 1], False

    def read_comparison_operator(self):
        start = self.position
        while self.position < len(self.code) and self.peek_char() in OPS_REVERSE.keys():
            self.next_char()
        return self.code[start:self.position + 1]


def compare_strings(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

