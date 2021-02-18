from typing import (
    Any,
    cast,
    List,
    Tuple,
)
from unittest import TestCase

from frl.ast import Program
from frl.evaluator import (
    evaluate,
    NULL
)
from frl.lexer import Lexer
from frl.object import (
    Boolean,
    Environment,
    Error,
    Float,
    Function,
    Integer,
    Object,
)
from frl.parser import Parser


class EvaluatorTest(TestCase):

    def test_integer_evaluator(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('10', 10),
            ('15', 15),
            ('-4', -4),
            ('-50', -50),
            ('5 + 5', 10),
            ('5 - 10', -5),
            ('2 * 2 * 2 * 2', 16),
            ('2 * 5 - 3', 7),
            ('50 / 2', 25),
            ('2 * (5 - 3)', 4),
            ('(2 + 7) / 3', 3),
            ('-50 / 2 * 2 + 10', -40),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_float_evaluator(self) -> None:
        tests: List[Tuple[str, float]] = [
            ('5.0', 5.0),
            ('10.0', 10.0),
            ('-5.0', -5.0),
            ('-10.0', -10.0),
            ('5 / 2', 2.5),
            ('2.5 * 2.0 + 7.0', 12.0),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_float_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('true', True),
            ('false', False),
            ('1 < 2', True),
            ('1 <= 2', True),
            ('2 > 2', False),
            ('2 >= 2', True),
            ('1 < 1', False),
            ('1 >= 2', False),
            ('1 > 1', False),
            ('0.3 <= 0.2', False),
            ('1 == 1', True),
            ('2 == 1', False),
            ('1 != 1', False),
            ('1 != 5', True),
            ('true == true', True),
            ('false == false', True),
            ('true == false', False),
            ('true != false', True),
            ('(1 < 2) == true', True),
            ('(1 < 2) == false', False),
            ('(1 > 2) == true', False),
            ('(1 > 2) == false', True),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_bang_operator(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('!true', False),
            ('!false', True),
            ('!!true', True),
            ('!!false', False),
            ('!5', False),
            ('!!5', True),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('if (true) { 10 }', 10),
            ('if (false) { 10 }', None),
            ('if (1) { 10 }', 10),
            ('if (1 < 2) { 10 }', 10),
            ('if (1 > 2) { 10 }', None),
            ('if (1 < 2) { 10 } else { 20 }', 10),
            ('if (1 > 2) { 10 } else { 20 }', 20),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            if type(expected) == int:
                self._test_integer_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def test_return_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('return 10;', 10),
            ('return 10; 9;', 10),
            ('return 2 * 5; 9;', 10),
            ('9; return 2 * 6; 9;', 12),
            ('''
                if (10 > 1) {
                    if (20 > 10) {
                        return 1;
                    }
                    
                    return 0;
                }
             ''', 1),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_return_float_evaluation(self) -> None:
        tests: List[Tuple[str, float]] = [
            ('return 10.0;', 10.0),
            ('return 10.5; 9;', 10.5),
            ('return 2 * 5 / 3; 9;', 3.3333333333333335),
            ('9; return 2 * 6 / 7; 9;', 1.7142857142857142),
            ('''
                if (10 > 1) {
                    if (20 > 10) {
                        return 1.4;
                    }
                    
                    return 0.1;
                }
             ''', 1.4),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_float_object(evaluated, expected)

    def test_error_handling(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('true + 5;',
             '''on the line 1.
Unexpected type: Cannot operate \'BOOLEAN\' and \'INTEGERS\' with \'+\'.'''),
            ('true - 5;',
             '''on the line 1.
Unexpected type: Cannot operate \'BOOLEAN\' and \'INTEGERS\' with \'-\'.'''),
            ('5 * true; 9;',
             '''on the line 1.
Unexpected type: Cannot operate \'INTEGERS\' and \'BOOLEAN\' with \'*\'.'''),
            ('-true;',
             '''on the line 1.
Unexpected operator: - operator to type \'BOOLEAN\'.'''),
            ('false + true;',
             '''on the line 1.
Unexpected operator: \'BOOLEAN\' + \'BOOLEAN\'.'''),
            ('5; false - true; 10;',
             '''on the line 1.
Unexpected operator: \'BOOLEAN\' - \'BOOLEAN\'.'''),
            ('''
                if (10 > 7) {
                    return true + false;
                }
             ''',
             '''on the line 3.
Unexpected operator: \'BOOLEAN\' + \'BOOLEAN\'.'''),
            ('''
                if (10 > 1) {
                    return true * false;
                }
             ''',
             '''on the line 3.
Unexpected operator: \'BOOLEAN\' * \'BOOLEAN\'.'''),
            ('''
                if (5 < 2) {
                    return 1;
                } else {
                    return true / false;
                }
             ''',
             '''on the line 5.
Unexpected operator: \'BOOLEAN\' / \'BOOLEAN\'.'''),
            ('foobar;',
             '''on the line 1.
Undefined variable: foobar.''')
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            self.assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)
            self.assertEquals(evaluated.message, expected)

    def test_assigment_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('var a = 5; a;', 5),
            ('var a = 5 * 5; a;', 25),
            ('var a = 5; var b = a; b;', 5),
            ('var a = 5; var b = a; var c = a + b + 5; c;', 15),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_function_evaluation(self) -> None:
        source: str = ' fun(x) { x + 2; }; fun suma(x) { x + 2; };'

        evaluated = self._evaluate_tests(source)

        self.assertIsInstance(evaluated, Function)

        evaluated = cast(Function, evaluated)
        if len(str(evaluated.ident)) != 0:
            self.assertEquals(str(evaluated.ident), "suma")
        self.assertEquals(len(evaluated.parameters), 1)
        self.assertEquals(str(evaluated.parameters[0]), 'x')
        self.assertEquals(str(evaluated.body), '(x + 2)')

    def test_function_calls(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('var identidad = fun(x) { x }; identidad(5);', 5),
            # ('fun identidad(x) { x }; identidad(5);', 5),
            ('''
                var identidad = fun(x) {
                    return x;
                };
                identidad(5);
             ''', 5),
            # ('''
            #     fun identidad(x) {
            #         return x;
            #     };
            #     identidad(5);
            #  ''', 5),
            ('''
                var doble = fun(x) {
                    return 2 * x;
                };
                doble(5);
             ''', 10),
            # ('''
            #     fun doble(x) {
            #         return 2 * x;
            #     };
            #     doble(5);
            #  ''', 10),
            # ('''
            #     fun suma(x, y) {
            #         return x + y;
            #     };
            #     suma(3, 8);
            #  ''', 11),
            # ('''
            #     fun suma(x, y) {
            #         return x + y;
            #     };
            #     suma(5 + 5, suma(10, 10));
            #  ''', 30),
            ('fun(x) { x }(5)', 5),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def _test_null_object(self, evaluated: Object) -> None:
        self.assertEquals(evaluated, NULL)

    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        env: Environment = Environment()

        evaluated = evaluate(program, env)

        assert evaluated is not None
        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)

        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_float_object(self, evaluated: Object, expected: float) -> None:
        self.assertIsInstance(evaluated, Float)

        evaluated = cast(Float, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)
