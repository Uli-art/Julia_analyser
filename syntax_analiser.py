from token_struct import TokenError, TOKEN_ERROR_DESCRIPTION
from kind_of_token import Type, LITERALS, OPEN_BRACKETS, CLOSE_BRACKETS, OPS_REVERSE
from identifier_table import MyException


class TreeNode:
    def __init__(self, text, parent):
        self.text = text
        self.children = []
        self.parent = parent

    def find(self, node, x):
        if isinstance(node, ExpressionNode):
            if node.value is x:
                return node
        else:
            for child_node in node.children:
                n = self.find(child_node, x)
                if n:
                    return n
        return None

    def find_nodes(self, root, target_value):
        found_nodes = []

        def search(node):
            if isinstance(node, TreeNode):
                if node.text == target_value:
                    found_nodes.append(node)

                for child in node.children:
                    search(child)

        search(root)
        return found_nodes

    def find_all(self, node, x, arr):
        if isinstance(node, ExpressionNode):
            if node.value is x:
                arr.push(node)
        else:
            for child_node in node.children:
                n = self.find_all(child_node, x, arr)
                if n:
                    return n
        return None


class ExpressionNode:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent


class JuliaSyntax:
    def __init__(self, tokens, identifiers):
        self.identifiers = identifiers
        self.tokens = tokens
        self.root = TreeNode("Program", None)
        self.stack = [self.root]
        self.count = 0
        self.results = 0

    def syntax_analyse(self):
        lines = []
        line = []
        for token in self.tokens:
            if token.token_error != TokenError.NO_ERR:
                self.raise_exception(token, TOKEN_ERROR_DESCRIPTION[token.token_error])

            if token.kind == Type.KEYWORD:
                if token.value == "for":
                    if not self.check_for():
                        self.raise_exception(token, "for loop")
                if token.value == "while":
                    if not self.find_end():
                        self.raise_exception(token, "while loop")
                if token.value == "begin":
                    if not self.find_end():
                        self.raise_exception(token, "begin block")
                if token.value == "function":
                    if not self.check_functions():
                        self.raise_exception(token, "function declaration")
                if token.value == "try":
                    if not self.check_try():
                        self.raise_exception(token, "try")
                if token.value == "return":
                    if not self.check_return():
                        self.raise_exception(token, "return must have a value")

            if token.kind == Type.IDENTIFIER:
                next_token = self.get_next_token()
                if next_token:
                    if (next_token.kind == Type.IDENTIFIER or next_token.kind in LITERALS) and token.row == next_token.row:
                        self.raise_exception(token, "maybe you missed the operator")

            next_token = self.get_next_token()
            if next_token and token.row == next_token.row:
                line.append(token)
            else:
                line.append(token)
                lines.append(line)
                line = []
            self.count += 1
        return lines

    def syntax_tree(self):
        lines = self.syntax_analyse()
        for line in lines:
            parent = self.stack[-1]
            parent.children.append(self.line_node(line))
        return self.root

    def line_node(self, line):
        self.results += 1
        index = 0
        cur_root = TreeNode("n_" + self.results.__str__(), None)
        cur_stack = [cur_root]
        for token in line:
            index += 1
            if token.kind == Type.KEYWORD:
                if token.value == "end":
                    self.stack.pop()
                    cur_stack.pop()
                    continue
                parent = cur_stack[-1]
                new_node = TreeNode(token.value, parent)
                parent.children.append(new_node)
                self.stack.append(new_node)
                cur_stack.append(new_node)
                continue
            if token == '(':
                parent = cur_stack[-1]
                self.results += 1
                new_node = TreeNode("n_" + self.results.__str__(), parent)
                parent.children.append(new_node)
                self.stack.append(new_node)
                cur_stack.append(new_node)
            elif token == ')':
                self.stack.pop()
                cur_stack.pop()
            if token.value in OPEN_BRACKETS or token.value in CLOSE_BRACKETS:
                continue
            else:
                parent = cur_stack[-1]
                if parent.children.__len__() == 2 and \
                        set([el.value for el in line[index::]]).intersection(set(OPS_REVERSE.keys())) and \
                        not ')' in line[index::]:
                    self.results += 1
                    new_node = TreeNode("n_" + self.results.__str__(), parent)
                    parent.children.append(new_node)
                    cur_stack.append(new_node)
                parent = cur_stack[-1]
                # if token.kind == Type.IDENTIFIER or token.kind in LITERALS:
                #     new_node = ExpressionNode( [k for k, v in self.identifiers.items()
                #                                 if v.value == token.value and v.kind == token.kind][0], parent)
                #     parent.children.append(new_node)
                # else:
                new_node = ExpressionNode(token.value, parent)
                parent.children.append(new_node)
                continue
        return cur_root

    #         i = j + k + o * 2
    #         j = 9
    # j + n_1
    #    /    \
    #   k  +   o

    @staticmethod
    def raise_exception(token, text):
        exception = "Syntax error: " + str(text) + " in '" + str(token.value) \
                    + "'" + "line:" + str(token.row) + ":" + str(token.col)
        raise MyException(exception)

    def get_next_token(self):
        return self.tokens[self.count + 1] if self.count + 1 < len(self.tokens) else None

    def get_follow_token(self, i):
        return self.tokens[self.count + i] if self.count + i < len(self.tokens) else None

    def check_for(self):
        if self.get_next_token().kind == Type.IDENTIFIER and self.get_follow_token(
                2).kind == Type.IN and self.find_end():
            return True
        else:
            return False

    def check_return(self):
        next_token = self.get_next_token()
        if next_token.kind in LITERALS or next_token.kind == Type.IDENTIFIER or next_token.value == "true" or next_token.value == "false":
            return True
        else:
            return False

    def find_end(self):
        count_blocks = 0
        for i in range(1, len(self.tokens) - self.count):
            follow_token = self.get_follow_token(i)
            if follow_token.value in ["while", "for", "begin", "function", "try", "if"]:
                count_blocks += 1
            if follow_token.value == "end":
                if count_blocks == 0:
                    return True
                count_blocks -= 1
        return False

    def find_catch(self):
        for i in range(len(self.tokens) - self.count):
            follow_token = self.get_follow_token(i)
            if follow_token.value == "catch":
                return True
        return False

    def check_try(self):
        if self.get_next_token().kind == Type.IDENTIFIER and self.find_catch() and self.find_end():
            return True
        else:
            return False

    def check_functions(self):
        if self.get_next_token().kind == Type.IDENTIFIER and self.get_follow_token(
                2).kind == Type.LPAREN and self.find_end():
            return True
        else:
            return False


def print_parse_tree(node, level=0):
    if node:
        if isinstance(node, TreeNode):
            print('│\t' * level + '├── ' + str(node.text))
        else:
            print('│\t' * level + '├── ' + str(node.value))
        if isinstance(node, TreeNode):
            for child in node.children:
                print_parse_tree(child, level + 1)

# expression = "( + ( * 2 3 ) 4 )"
# parse_tree = build_parse_tree(expression)
# print_parse_tree(parse_tree)

# скобки
# неправильно написанные ключевые слова
# для ключевых слов for, while, return, function, try проверяется сигнатура
