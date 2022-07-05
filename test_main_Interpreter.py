import unittest
from main_Interpreter import*

class TestLexer(unittest.TestCase):
    def test_assignment_YOUR(self):
        code = 'Your luck will be excellent'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        right_token = Token(TokenTypes.YOUR, 'YOUR')
        self.assertEqual(token, right_token)

    def test_assignment_ID(self):
        code = 'luck will be excellent'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        right_token = Token(TokenTypes.STRING, 'luck')
        self.assertEqual(token, right_token)

    def test_assignment_STRING(self):
        code = 'excellent'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        right_token = Token(TokenTypes.STRING, 'excellent')
        self.assertEqual(token, right_token)

    def test_assignment_WILLBE(self):
        code = 'will be'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        right_token = Token(TokenTypes.WILLBE, 'WILLBE')
        self.assertEqual(token, right_token)

    def test_assignment_AND(self):
        code = 'and sssa'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        right_token = Token(TokenTypes.AND, 'AND')
        self.assertEqual(token, right_token)

    def test_starting_phrase_right(self):
        code = 'Stars are saying...'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        right_token = Token(TokenTypes.START, 'START')
        self.assertEqual(token, right_token)
        
    def test_starting_phrase_wrong(self):
        code = 'Stars are saying'
        lexer = Lexer(code)
        token = lexer.get_next_token()
        self.assertEqual(token, None)


class TestInterpreter(unittest.TestCase):
    def test_assignment(self):
        code = 'Stars are saying... Your luck will be excellent.'
        lexer = Lexer(code)
        parser = Parser(lexer)
        interp = Interpreter(parser)
        interp.interp()
        self.assertEqual(interp.GLOBAL_SCOPE.get('luck'), [len('excellent')])

    def test_more_assignments(self):
        code = 'Stars are saying... Your luck will be excellent, your health will be perfect.'
        lexer = Lexer(code)
        parser = Parser(lexer)
        interp = Interpreter(parser)
        interp.interp()
        self.assertEqual(interp.GLOBAL_SCOPE.get('luck'), [len('excellent')])
        self.assertEqual(interp.GLOBAL_SCOPE.get('health'), [len('perfect')])

    def test_multiple_sentences(self):
        code = 'Stars are saying... Your luck will be great and cool.'
        lexer = Lexer(code)
        parser = Parser(lexer)
        interp = Interpreter(parser)
        interp.interp()
        self.assertEqual(interp.GLOBAL_SCOPE.get('luck'), [len('cool'), len('great')])

    def test_result(self):
        code = 'Stars are saying... Your hair will be ok, your elbows will be fine, your legs will be strong and healthy, your octopus will be significant.'
        lexer = Lexer(code)
        parser = Parser(lexer)
        interp = Interpreter(parser)
        output = interp.interp()
        self.assertEqual(output, 'hello')

class TestCodeGenerator(unittest.TestCase):
    def test_valid_code_generation(self):
        code_generator = CodeGenerator()
        code = code_generator.gen_code()
        lexer = Lexer(code)
        parser = Parser(lexer)
        interp = Interpreter(parser)
        output = interp.interp()
        self.assertNotEqual(output, None)
