from token_struct import TokenError, TOKEN_ERROR_DESCRIPTION
from kind_of_token import Type, LITERALS, OPEN_BRACKETS, CLOSE_BRACKETS, OPS_REVERSE, KEYWORDS
from identifier_table import MyException
from syntax_analiser import TreeNode, ExpressionNode

from identifier_table import create_id_table
from tokenizer import JuliaTokenizer
from syntax_analiser import JuliaSyntax, print_parse_tree
from tkinter import filedialog as fd


class JuliaSemantic:

    def __init__(self, root, identifiers):
        self.root = root
        self.identifiers = identifiers
        self.cur_scope = 0
        self.identifier_scope = [[]]
        self.functions = {}
        self.variables = {}

    def get_functions(self, node):
        if node:
            if isinstance(node, TreeNode):
                if node.text == "function":
                    params = [x.value for x in node.children if isinstance(x, ExpressionNode)]
                    params.pop(0)
                    params = [x for x in params if x != ',']
                    self.functions[node.children[0].value] = params
            if isinstance(node, TreeNode):
                for child in node.children:
                    self.get_functions(child)
        return self.functions

    def check_functions(self, node):
        if node:
            if isinstance(node, TreeNode):
                if node.children and isinstance(node.children[0], ExpressionNode) and node.children[0].value in self.functions.keys():
                    params = [x.value for x in node.children if isinstance(x, ExpressionNode) and x.value != ',']
                    params.pop(0)
                    if len(params) != len(self.functions[node.children[0].value]):
                        self.raise_exception("Incorrect number of function parameters " + node.children[0].value)
            if isinstance(node, TreeNode):
                for child in node.children:
                    self.check_functions(child)
        return self.functions

    def get_variables(self, node):
        if node:
            if isinstance(node, TreeNode):
                children_iter = iter(node.children)
                for child in children_iter:
                    if isinstance(child, ExpressionNode):
                        var = [v.value for k, v in self.identifiers.items() if v.value == child.value]
                        if not var:
                            continue
                        var = var[0]
                        try:
                            next_node = next(children_iter)
                        except:
                            continue
                        if var and next_node and isinstance(next_node, ExpressionNode) and next_node.value == '=':
                            if var in self.variables.keys():
                                if self.variables[var][1]:
                                    self.raise_exception("Changing a constant variable")
                            is_const = False
                            if child.parent.text == "const":
                                is_const = True
                            el_type = self.get_type(children_iter)
                            self.variables[var] = (el_type, is_const)
                            continue
            if isinstance(node, TreeNode):
                for child in node.children:
                    self.get_variables(child)
        return self.variables

    def check_variables(self, node):
        for var in identifiers.values():
            if var.kind == Type.IDENTIFIER:
                if var.value in self.variables.keys():
                    continue
                if var.value in self.functions.keys():
                    continue
                find = False
                for param in self.functions.values():
                    if var.value in param:
                        find = True
                        continue
                if find:
                    continue
                cur_node = node.find(node, var.value)
                if cur_node:
                    parent = cur_node.parent
                    if parent.text in KEYWORDS.keys():
                        self.variables[var.value] = (Type.INTEGER, 0)
                        continue
                    check_node = self.find_node(parent.children, var.value)
                    if check_node.value in OPS_REVERSE.keys():
                        continue
                    find = False
                    for id in identifiers.values():
                        if id.value == check_node.value and (id.kind == Type.IDENTIFIER or id.kind in LITERALS):
                            self.functions[var.value] = []
                            find = True
                            continue
                    if find:
                        for id in identifiers.values():
                            if id.value == var.value and id.kind == Type.IDENTIFIER:
                                id.kind = Type.FUNCTION
                                continue
                        continue
                self.raise_exception("Undefined variable " + var.value)

    def get_type(self, cur_iter):
        next_next_node = next(cur_iter)
        if not next_next_node:
            return "any"
        if isinstance(next_next_node, ExpressionNode) and next_next_node.value not in OPS_REVERSE:
            cur_identifier = [v for k, v in self.identifiers.items() if v.value == next_next_node.value][0]
            if cur_identifier.kind == Type.IDENTIFIER:
                if cur_identifier.value in self.variables.keys():
                    return self.variables[cur_identifier.value][0]
                else:
                    self.raise_exception("Undefined variable " + cur_identifier.value)
            return cur_identifier.kind
        elif isinstance(next_next_node, ExpressionNode) and next_next_node.value in OPS_REVERSE:
            return self.get_type(cur_iter)
        elif isinstance(next_next_node, TreeNode):
            return self.get_type(iter(next_next_node.children))

    def is_boolean_expression(self, condition):
        self.variables['a'] = (Type.INTEGER, 0)
        if isinstance(condition, bool):
            return True
        elif isinstance(condition, str):
            val_dict = {}
            for key, value in self.variables.items():
                if value[0] in [Type.INTEGER, Type.BIN_INT, Type.HEX_INT, Type.OCT_INT, Type.FLOAT]:
                    val_dict[key] = 0
                elif value[0] in [Type.STRING, Type.TRIPLE_STRING]:
                    val_dict[key] = ""
                elif value[0] in [Type.CHAR]:
                    val_dict[key] = ''
            condition = condition.replace('||', 'or').replace('&&', 'and')
            try:
                eval_result = eval(condition, val_dict)
                print(eval_result)
                return isinstance(eval_result, bool)
            except SyntaxError:
                print(SyntaxError.text)
                return False
        else:
            return False

    def check_conditionals(self, node):
        conditional_nodes = node.find_nodes(node, "if")
        conditional_nodes += node.find_nodes(node, "while")
        for cond_node in conditional_nodes:
            cond_str = ""

            def get_str(cond_node_func, cond_str_func):
                if isinstance(cond_node_func, TreeNode):
                    if isinstance(cond_node_func.children[0], TreeNode):
                        if cond_node_func.children[0].text == "True":
                            self.raise_exception("if always true")
                        if cond_node_func.children[0].text == "False":
                            self.raise_exception("if always false")
                    children = cond_node_func.children
                    for i in range(children.__len__()):
                    # for child in cond_node.children:
                        if isinstance(children[i], ExpressionNode):
                            cond_str_func += children[i].value + " "
                        elif isinstance(children[i], TreeNode) and "n_" in children[i].text and i != 2:
                            return cond_str_func
                        else:
                            cond_str_func = get_str(children[i], cond_str_func)
                return cond_str_func

            cond_str = get_str(cond_node, cond_str)
            bool_cond = self.is_boolean_expression(cond_str)
            if not bool_cond:
                self.raise_exception("incorrect if conditional")

        print(conditional_nodes)

    @staticmethod
    def find_node(children, var):
        for i in range(children.__len__()):
            if isinstance(children[i], ExpressionNode) and children[i].value == var:
                if i == 0:
                    return children[1]
                else:
                    return children[i - 1]
        return None

    @staticmethod
    def raise_exception(text):
        exception = "Error: " + str(text)
        raise MyException(exception)


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
    print(identifiers)
    syntax_analyser = JuliaSyntax(tokens, identifiers)
    tree = syntax_analyser.syntax_tree()
    print_parse_tree(tree)

    semantic_analyser = JuliaSemantic(tree, identifiers)
    func = semantic_analyser.get_functions(tree)
    variables = semantic_analyser.get_variables(tree)

    semantic_analyser.check_functions(tree)
    semantic_analyser.check_variables(tree)
    semantic_analyser.check_conditionals(tree)




