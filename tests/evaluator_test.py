from typing import (
    cast,
    List,
    Tuple,
)
from unittest import TestCase

from frl.ast import Program
from frl.evaluator import evaluate
from frl.lexer import Lexer
from frl.object import (
    Boolean,
    Float,
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
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_float_evaluator(self) -> None:
        tests: List[Tuple[str, float]] = [
            ('5.9', 5.9),
            ('0.2', 0.2),
            ('1.3', 1.3),
            ('34.1', 34.1),
            ('-12.34', -12.34),
            ('-0.192', -0.192),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_float_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('true', True),
            ('false', False),
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

    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        evaluated = evaluate(program)

        assert evaluated is not None
        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)

        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_float_object(self, evaluated: Object, expected: float) -> None:
        self.assertIsInstance(evaluated, Float)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)
