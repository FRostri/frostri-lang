from typing import (
    Any,
    cast,
    List,
    Tuple,
    Union,
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
    Integer,
    Object,
    String,
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
Undefined variable: foobar.'''),
            ('"Foo" - "Bar";',
             '''on the line 1.
Unexpected operator: \'STRING\' - \'STRING\'.'''),
            ("'Foo' * 'Bar';",
             '''on the line 1.
Unexpected operator: \'STRING\' * \'STRING\'.''')
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

    def test_string_evaluation(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('"Hello world!"', 'Hello world!'),
            ("'Platzi'", 'Platzi'),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_string_object(evaluated, expected)

    def test_string_concatenation(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('"Foo" + "bar";', 'Foobar'),
            ("'Hello,' + ' ' + 'world!'", "Hello, world!"),
            # ('''
            #     var saludo = fun(nombre) {
            #         return "Hole " + nombre + "!";
            #     };
            #     saludo("Isaac");
            #  ''',
            #  'Hola Isaac!'),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_string_object(evaluated, expected)

    def test_string_comparison(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('"a" == "a"', True),
            ('"a" != "a"', False),
            ('"a" == "b"', False),
            ('"a" != "b"', True),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_builtin_functions(self) -> None:
        tests: List[Tuple[str, Union[str, int]]] = [
            ('get_len("");', 0),
            ('get_len("cuatro");', 6),
            ('get_len("");', 10),
            ('get_len("uno", "dos");',
             '''on the line 1.
Too arguments for the \'get_len\' function. given 2, expected 1'''),
            ('get_len(1);',
             '''on the line 1.
Unexpected type argument: expected \'STRING\' recived \'INTEGERS\''''),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            if type(expected) == int:
                expected = cast(int, expected)
                self._test_integer_object(evaluated, expected)
            else:
                expected = cast(str, expected)
                self._test_error_object(evaluated, expected)

    def _test_error_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, Error)

        evaluated = cast(Error, evaluated)
        self.assertEquals(evaluated.message, expected)

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

    def _test_string_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, String)

        evaluated = cast(String, evaluated)
        self.assertEquals(evaluated.value, expected)
