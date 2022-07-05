from enum import Enum
from code_generator import CodeGenerator
import copy

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __str__(self):
        return f'<{self.type}: {self.value}>'

    __repr__ = __str__

class TokenTypes(Enum):
    START = 'START'
    YOUR = 'YOUR'
    STRING = 'STRING'
    DOT = 'DOT'
    COMMA = 'COMMA'
    EOF = 'EOF'
    WILLBE = 'WILLBE'
    AND = 'AND'

#                         #
#        L E X E R        #
#                         #
class Lexer:

    def __init__(self, source_code):
        self.START_PHRASE = 'starsaresaying'
        self.program_started = False
        self.source_code = source_code
        self.pos = 0
        self.current_char = self.source_code[self.pos]

    def advance(self, lenght=1):
        self.pos += lenght
        if self.pos < len(self.source_code):
            self.current_char = self.source_code[self.pos]
        else:
            self.current_char = None

    def skip_comma(self):
        if self.current_char == ',':
            self.advance()
            self.skip_whitespaces()

    def skip_whitespaces(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            else:
                break

    def check_ellipsis(self):
        if self.pos + 2 < len(self.source_code):
            if self.source_code[self.pos:self.pos + 3] == '...':
                self.advance(3)
                return True
        return False

    def get_next_word(self):
        current_word = ''

        while self.current_char is not None:
            if self.current_char.isalpha():
                current_word = ''.join((current_word, self.current_char))
                self.advance()
            else:
                break

        return current_word

    def get_phrase(self, first_word):
        phrase = first_word
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespaces()
                next_word = self.get_next_word()
                phrase = ''.join((phrase, next_word))
            else:
                break
        return phrase

    def get_next_token(self):
        self.skip_whitespaces()

        if self.current_char is None:
            return Token(TokenTypes.EOF, 'EOF')

        elif self.current_char == '.':
            return Token(TokenTypes.DOT, '.')

        elif self.current_char == ',':
            self.skip_comma()
            return Token(TokenTypes.COMMA, ',')

        elif self.current_char.isalpha():
            current_word = self.get_next_word()

            if current_word.lower() == 'your':
                return Token(TokenTypes.YOUR, 'YOUR')

            elif current_word.lower() == 'will':
                self.skip_whitespaces()
                current_word = ''.join(('will', self.get_next_word()))
                return Token(TokenTypes.WILLBE, 'WILLBE')

            elif current_word.lower() == 'and':
                return Token(TokenTypes.AND, 'AND')

            elif not self.program_started and current_word.lower() == 'stars':
                current_phrase = self.get_phrase(current_word)
                if current_phrase.lower() == self.START_PHRASE and self.check_ellipsis():
                    self.program_started = True
                    return Token(TokenTypes.START, 'START')
            else:
                return Token(TokenTypes.STRING, current_word)

        return None

#                         #
#      P A R S E R        #
#                         #
class AST():
    pass

class Prediction(AST):
    def __init__(self, assignment_list):
        self.assignment_list = assignment_list

    def __str__(self):
        return f'<Prediction AST: {str(self.assignment_list)}>'

    __repr__ = __str__

class Assignment(AST):
    def __init__(self, var, sentence_list):
        self.var = var
        self.sentence_list = sentence_list

    def __str__(self):
        return f'<Assignmnet AST: {str(self.var)}; {str(self.sentence_list)}>'

    __repr__ = __str__

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'<Var AST: {self.value}>'

    __repr__ = __str__

class Sentence(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'<Sentence AST: {self.value}>'

    __repr__ = __str__


class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise AssertionError('write it better next time, I see a mistake here!')

    def prediction(self):
        self.eat(TokenTypes.START)
        assignment_node_list = [self.assignment()]
        while self.current_token.type == TokenTypes.COMMA:
            self.eat(TokenTypes.COMMA)
            next_assignment_node = self.assignment()
            assignment_node_list.append(next_assignment_node)

        prediction_node = Prediction(assignment_node_list)
        self.eat(TokenTypes.DOT)
        return prediction_node

    def assignment(self):
        self.eat(TokenTypes.YOUR)
        var_node = self.var()
        self.eat(TokenTypes.WILLBE)
        sentence_node_list = [self.sentence()]
        while self.current_token.type == TokenTypes.AND:
            self.eat(TokenTypes.AND)
            next_sentence_node = self.sentence()
            sentence_node_list.append(next_sentence_node)

        node_assignment = Assignment(var_node, sentence_node_list)
        return node_assignment

    def var(self):
        token = self.current_token
        self.eat(TokenTypes.STRING)
        var_node = Var(token)
        return var_node

    def sentence(self):
        token = self.current_token
        self.eat(TokenTypes.STRING)
        sentence_node = Sentence(token)
        return sentence_node

    def parse(self):
        node = self.prediction()
        return node

#                         #
#  I N T E R P R E T E R  #
#                         #
class NodeVisitor():
    def visit(self, node):
        method_name = '_'.join(('visit', type(node).__name__))
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'where is a frikin visit_{type(node.__name__)}() method?!')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = dict()

    def next_var(self, vars):
        symbol_to_return = None
        max_index = 0

        for symbol, indexes in vars.items():
            current_max_index = max(indexes)

            if current_max_index > max_index:
                max_index = current_max_index
                symbol_to_return = symbol

        return symbol_to_return

    def form_output(self):
        global_scope_copy = copy.deepcopy(self.GLOBAL_SCOPE)
        output = ''

        while len(global_scope_copy) > 0:
            next_var = self.next_var(global_scope_copy)
            global_scope_copy[next_var].pop()
            if len(global_scope_copy[next_var]) == 0:
                global_scope_copy.pop(next_var)

            output = ''.join((next_var[0], output))

        return output

    def visit_Prediction(self, node):
        for assignment_node in node.assignment_list:
            self.visit(assignment_node)

    def visit_Assignment(self, node):
        var_name = self.visit(node.var)
        var_vals = []
        for sentence in node.sentence_list:
            var_vals.append(self.visit(sentence))
        
        var_vals.sort()
        self.GLOBAL_SCOPE[var_name] = var_vals

    def visit_Var(self, node):
        var_name = node.value
        return var_name

    def visit_Sentence(self, node):
        var_val = len(node.value)
        return var_val

    def interp(self):
        try:
            base_node = self.parser.parse()
            self.visit(base_node)
        except AssertionError:
            return None
        else:
            output = self.form_output()
            return output


def main():
    code_generator = CodeGenerator()
    code = code_generator.gen_code()
    lexer = Lexer(code)
    parser = Parser(lexer)
    interp = Interpreter(parser)
    print(interp.interp())

    with open('src.txt', 'w') as src_code:
        src_code.write(code)

    input()

if __name__ == '__main__':
    main()
