from typing import (
    cast,
    List,
    Any,
    Tuple,
    Type,
)
from unittest import TestCase

from frl.lexer import Lexer
from frl.parser import Parser
from frl.ast import (
    Block,
    Boolean,
    Call,
    Expression,
    ExpressionStatement,
    Float,
    Function,
    Identifier,
    If,
    Infix,
    Integer,
    LetStatement,
    Prefix,
    Program,
    ReturnStatement,
    StringLiteral,
)


class ParserTest(TestCase):

    def test_pase_program(self) -> None:
        source: str = 'var x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    def test_let_statements(self) -> None:
        source: str = '''
            var x = 5;
            var y = 10;
            var foo = 2.5;
            var bar = true;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 4)

        expected_identifiers_and_values: List[Tuple[str, Any]] = [
            ('x', 5),
            ('y', 10),
            ('foo', 2.5),
            ('bar', True),
        ]

        for statement, (expected_identifier, expected_value) in zip(
                program.statements, expected_identifiers_and_values):
            self.assertEqual(statement.token_literal(), 'var')
            self.assertIsInstance(statement, LetStatement)

            let_statement = cast(LetStatement, statement)

            assert let_statement.name is not None
            self._test_identifier(let_statement.name, expected_identifier)

            assert let_statement.value is not None
            self._test_literal_expression(let_statement.value, expected_value)

    def test_name_in_let_statements(self) -> None:
        source: str = '''
            var x = 5;
            var y = 10;
            var foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        names: List[str] = []
        for statement in program.statements:
            statement = cast(LetStatement, statement)
            assert statement.name is not None
            names.append(statement.name.value)

        expected_names: List[str] = ['x', 'y', 'foo']

        self.assertEquals(names, expected_names)

    def test_parse_errors(self) -> None:
        source: str = '''var x 3;'''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = '''
            return 5;
            return foo;
            return true;
            return false;
            return 3.7;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements), 5)

        expected_return_values: List[Any] = [
            5,
            'foo',
            True,
            False,
            3.7,
        ]

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(
            expression_statement.expression, 'foobar')

    def test_integer_expressions(self) -> None:
        source: str = '5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 5)

    def test_float_expressions(self) -> None:
        source: str = '1.5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 1.5)

    def test_prefix_expression(self) -> None:
        source: str = '!5; -15; !true; !false;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=4)

        for statement, (expected_operator, expected_value) in zip(
                program.statements, [('!', 5), ('-', 15), ('!', True), ('!', False)]):
            statement = cast(ExpressionStatement, statement)
            self.assertIsInstance(statement.expression, Prefix)
            prefix = cast(Prefix, statement.expression)
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)

    def test_infix_expressions(self) -> None:
        source: str = '''
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 > 5;
            5 >= 5;
            5 < 5;
            5 <= 5;
            5 == 5;
            5 != 5;
            true == true;
            true == false;
            true != true;
            true != false;
            false == true;
            false == false;
            false != true;
            false != false;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=18)

        expected_operators_and_values: List[Tuple[Any, str, Any]] = [
            (5, '+', 5),
            (5, '-', 5),
            (5, '*', 5),
            (5, '/', 5),
            (5, '>', 5),
            (5, '>=', 5),
            (5, '<', 5),
            (5, '<=', 5),
            (5, '==', 5),
            (5, '!=', 5),
            (True, '==', True),
            (True, '==', False),
            (True, '!=', True),
            (True, '!=', False),
            (False, '==', True),
            (False, '==', False),
            (False, '!=', True),
            (False, '!=', False),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
                program.statements, expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(statement.expression,
                                        expected_left,
                                        expected_operator,
                                        expected_right)

    def test_boolean_expression(self) -> None:
        source: str = 'true; false;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=2)

        expected_values: List[bool] = [True, False]

        for statement, expected_value in zip(program.statements, expected_values):
            expression_statement = cast(ExpressionStatement, statement)

            assert expression_statement.expression is not None
            self._test_literal_expression(expression_statement.expression,
                                          expected_value)

    def test_operator_precedence(self) -> None:
        test_sources: List[Tuple[str, str, int]] = [
            ('-a * b;', '((-a) * b)', 1),
            ('!-a;', '(!(-a))', 1),
            ('a + b + c;', '((a + b) + c)', 1),
            ('a + b - c;', '((a + b) - c)', 1),
            ('a * b * c;', '((a * b) * c)', 1),
            ('a + b / c;', '(a + (b / c))', 1),
            ('a * b / c;', '((a * b) / c)', 1),
            ('a + b * c + d / e - f;', '(((a + (b * c)) + (d / e)) - f)', 1),
            ('5 > 4.4 == 3 < 4;', '((5 > 4.4) == (3 < 4))', 1),
            ('3 - 4 * 5 == 3.5 * 1.2 + 4 * 5;',
             '((3 - (4 * 5)) == ((3.5 * 1.2) + (4 * 5)))', 1),
            ('3 + 4; -5 * 5;', '(3 + 4)((-5) * 5)', 2),
            ('true;', 'true', 1),
            ('false;', 'false', 1),
            ('3 > 5 == true;', '((3 > 5) == true)', 1),
            ('3 < 5 == false;', '((3 < 5) == false)', 1),
            ('1 + (2 + 3) + 4;', '((1 + (2 + 3)) + 4)', 1),
            ('(5 + 5) * 2;', '((5 + 5) * 2)', 1),
            ('2 / (5 + 5);', '(2 / (5 + 5))', 1),
            ('-(5 + 5);', '(-(5 + 5))', 1),
            ('a + suma(b * c) + d;', '((a + suma((b * c))) + d)', 1),
            ('suma(a, b, 1, 2 * 3, 4 + 5, suma(6, 7 * 8));',
             'suma(a, b, 1, (2 * 3), (4 + 5), suma(6, (7 * 8)))', 1),
            ('suma(a + b + c * d / f + g);',
             'suma((((a + b) + ((c * d) / f)) + g))', 1),
        ]

        for source, expected_result, expected_statement_count in test_sources:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            self._test_program_statements(
                parser, program, expected_statement_count)
            self.assertEquals(str(program), expected_result)

    def test_call_expression(self) -> None:
        source: str = 'suma(1, 2 * 3, 4 + 5);'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        call = cast(Call, cast(ExpressionStatement,
                               program.statements[0]).expression)
        self.assertIsInstance(call, Call)
        self._test_identifier(call.function, 'suma')

        # Test arguments
        assert call.arguments is not None
        self.assertEquals(len(call.arguments), 3)
        self._test_literal_expression(call.arguments[0], 1)
        self._test_infix_expression(call.arguments[1], 2, '*', 3)
        self._test_infix_expression(call.arguments[2], 4, '+', 5)

    def test_if_expression(self) -> None:
        source: str = 'if (x < y) { z }'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        if_expression = cast(If, cast(ExpressionStatement,
                                      program.statements[0]).expression)
        self.assertIsInstance(if_expression, If)

        # Test condition
        assert if_expression.condition is not None
        self._test_infix_expression(if_expression.condition, 'x', '<', 'y')

        # Test consequence
        assert if_expression.consequence is not None
        self._test_block(if_expression.consequence, 1, ['z'])

        self.assertIsNone(if_expression.alternative)

    def test_if_else_expression(self) -> None:
        source: str = '''
            if (x < y) {
                z;
            } else {
                a;
                b;
            };

            if (e != q) {
                q;
            } else {
                e;
            }'''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=2)

        # Test correct node type
        if_expression = cast(If, cast(ExpressionStatement,
                                      program.statements[0]).expression)
        self.assertIsInstance(if_expression, If)

        # Test condition
        assert if_expression.condition is not None
        self._test_infix_expression(if_expression.condition, 'x', '<', 'y')

        # Test consequence
        assert if_expression.consequence is not None
        self._test_block(if_expression.consequence, 1, ['z'])

        # Test alternative
        assert if_expression.alternative is not None
        self._test_block(if_expression.alternative, 2, ["a", "b"])

    def test_function_literal(self) -> None:
        source: str = '''
            fun sum(x, y) { x + y; };
            fun(x, y) { x + y; };
            fun(x, y) {
                x + y;
            };
            '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=3)

        function_literal = cast(Function, cast(ExpressionStatement,
                                               program.statements[0]).expression)
        self.assertIsInstance(function_literal, Function)

        # Test params
        self.assertEquals(len(function_literal.parameters), 2)
        self._test_literal_expression(function_literal.parameters[0], 'x')
        self._test_literal_expression(function_literal.parameters[1], 'y')

        # test body
        assert function_literal.body is not None
        self.assertEquals(len(function_literal.body.statements), 1)

        body = cast(ExpressionStatement, function_literal.body.statements[0])
        assert body.expression is not None
        self._test_infix_expression(body.expression, 'x', '+', 'y')

    def test_function_parameters(self) -> None:
        tests = [
            {'input': 'fun sum() {};',
             'expected_params': []},
            {'input': 'fun(x) {};',
             'expected_params': ['x']},
            {'input': 'fun sum(x, y, z) {};',
             'expected_params': ['x', 'y', 'z']},
        ]

        for test in tests:
            lexer: Lexer = Lexer(test['input'])  # type: ignore
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            function = cast(Function, cast(ExpressionStatement,
                                           program.statements[0]).expression)

            self.assertEquals(len(function.parameters),
                              len(test['expected_params']))

            for idx, param in enumerate(test['expected_params']):
                self._test_literal_expression(function.parameters[idx], param)

    def test_string_literal_expression(self) -> None:
        source: str = '"hello world!";'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        expression_statement = cast(ExpressionStatement, program.statements[0])
        string_literal = cast(StringLiteral, expression_statement.expression)
        
        self.assertIsInstance(string_literal, StringLiteral)
        self.assertEquals(string_literal.value, 'hello world!')

    def _test_block(self,
                    block: Block,
                    statement_numbers: int,
                    expected_identifiers: List[str]) -> None:

        self.assertIsInstance(block, Block)
        self.assertEquals(len(block.statements), statement_numbers)
        self.assertEquals(len(expected_identifiers), len(block.statements))

        for statement, identifier in zip(
            block.statements,
            expected_identifiers
        ):
            statement = cast(ExpressionStatement, statement)

            assert statement.expression is not None
            self._test_identifier(statement.expression, identifier)

    def _test_boolean(self,
                      expression: Expression,
                      expected_value: bool) -> None:
        self.assertIsInstance(expression, Boolean)

        boolean = cast(Boolean, expression)
        self.assertEquals(boolean.value, expected_value)
        self.assertEquals(boolean.token.literal,
                          'true' if expected_value else 'false')

    def _test_infix_expression(self,
                               expression: Expression,
                               expected_left: Any,
                               expected_operator: str,
                               expected_right: Any):
        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEquals(infix.operator, expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)

    def _test_program_statements(self,
                                 parser: Parser,
                                 program: Program,
                                 expected_statement_count: int = 1) -> None:
        if parser.errors:
            print(parser.errors)
        self.assertEquals(len(parser.errors), 0)
        self.assertEquals(len(program.statements), expected_statement_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self,
                                 expression: Expression,
                                 expected_value: Any) -> None:
        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_integer(expression, expected_value)
        elif value_type == float:
            self._test_float(expression, expected_value)
        elif value_type == bool:
            self._test_boolean(expression, expected_value)
        else:
            self.fail(f'Unhandled type of expression. Got={value_type}')

    def _test_identifier(self,
                         expression: Expression,
                         expected_value: str) -> None:
        self.assertIsInstance(expression, Identifier)

        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)

    def _test_integer(self,
                      expression: Expression,
                      expected_value: int) -> None:
        self.assertIsInstance(expression, Integer)

        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))

    def _test_float(self,
                    expression: Expression,
                    expected_value: float) -> None:
        self.assertIsInstance(expression, Float)

        float_ = cast(Float, expression)
        self.assertEquals(float_.value, expected_value)
        self.assertEquals(float_.token.literal, str(expected_value))
