# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object.
"""
import unittest
from abc import ABC
from typing import Dict, Optional, Type

import dup_fmt.formatter as fmt
from dup_fmt.exceptions import FormatterValueError


class SlotLevelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sl = fmt.SlotLevel(level=5)
        self.sl.update(numbers=(2, 3, 4))

    def test_slot_level_properties(self):
        self.assertEqual("<SlotLevel(level=5)>", self.sl.__repr__())
        self.assertEqual("5", self.sl.__str__())
        self.assertEqual(hash(tuple(self.sl.slot)), self.sl.__hash__())
        self.assertEqual(3, self.sl.count)
        self.assertEqual(9, self.sl.value)

    def test_slot_level_update_failed(self):
        with self.assertRaises(FormatterValueError) as context:
            fmt.SlotLevel(level=5).update(numbers=(6,), strict=True)
        self.assertTrue(
            (
                "number for update the slot level object "
                "does not in range of 0 and 5."
            )
            in str(context.exception)
        )
        self.assertEqual(
            "<SlotLevel(level=5)>",
            fmt.SlotLevel(level=5)
            .update(numbers=(6,), strict=False)
            .__repr__(),
        )


class PriorityDataTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ...

    @staticmethod
    def caller(x):
        _ = x
        return 1

    def test_caller(self):
        self.assertEqual(1, self.caller("anythings"))

    def test_init_data(self):
        self.assertEqual(
            "PriorityData(level=5)",
            fmt.PriorityData(**{"value": self.caller, "level": 5}).__repr__(),
        )


class FormatterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        class WrongFormatter(fmt.Formatter):
            base_fmt: str = "%n"

            base_attr_prefix: str = "sr"

            __slots__ = (
                "_sr_number",
                "_sr_serial",
            )

            @property
            def value(self) -> int:  # pragma: no cover
                raise NotImplementedError

            @property
            def string(self) -> str:  # pragma: no cover
                raise NotImplementedError

            @property
            def priorities(self) -> Dict[str, dict]:  # pragma: no cover
                raise NotImplementedError

            @staticmethod
            def formatter(
                serial: Optional[int] = None,
            ) -> Dict[str, Dict[str, str]]:
                _value: str = str(serial or 0)
                return {
                    "%n": {
                        "value": _value,
                        "wrong_regex": r"(?P<number>[0-9]*)",
                    },
                }

        class NotImpPriority(fmt.Formatter, ABC):
            base_fmt: str = "%n"

            base_attr_prefix: str = "sr"

            __slots__ = (
                "_sr_number",
                "_sr_serial",
            )

            @property
            def value(self) -> int:  # pragma: no cover
                return 1

            @property
            def string(self) -> str:  # pragma: no cover
                return "Demo"

            @staticmethod
            def formatter(
                serial: Optional[int] = None,
            ) -> Dict[str, Dict[str, str]]:
                _value: str = str(serial or 0)
                return {
                    "%n": {
                        "value": _value,
                        "wrong_regex": r"(?P<number>[0-9]*)",
                    },
                }

        class ValidateFormatter(fmt.Naming):
            @property
            def validate(self) -> bool:
                return False

        self.wrong_fmt_cls = WrongFormatter
        self.not_imp_priority_cls = NotImpPriority
        self.validate_fmt_cls = ValidateFormatter

    def test_base_formatter_properties(self):
        with self.assertRaises(TypeError) as context:
            fmt.Formatter()
        self.assertTrue(
            (
                "Can't instantiate abstract class Formatter with abstract "
                "methods formatter, priorities, string, value"
            )
            in str(context.exception)
        )

    def test_base_formatter_init_with_fmt(self):
        with self.assertRaises(TypeError) as context:
            fmt.Formatter({"month": 1})
        self.assertTrue(
            (
                "Can't instantiate abstract class Formatter with abstract "
                "methods formatter, priorities, string, value"
            )
            in str(context.exception)
        )

    def test_base_formatter_parse_without_fmt(self):
        with self.assertRaises(NotImplementedError) as context:
            fmt.Formatter.parse("dummy")
        self.assertTrue(
            "This class does not set default format" in str(context.exception)
        )

    def test_base_formatter_parse_with_fmt(self):
        with self.assertRaises(NotImplementedError) as context:
            fmt.Formatter.parse("dummy", "%Z")
        self.assertTrue(
            (
                "Please implement formatter static method "
                "for this sub-formatter class"
            )
            in str(context.exception)
        )

    def test_new_format_with_wrong_formatter(self):
        with self.assertRaises(FormatterValueError) as context:
            self.wrong_fmt_cls.regex()
        self.assertTrue(
            "formatter does not contain `regex` or `cregex` "
            "in dict value" in str(context.exception)
        )

    def test_new_format_without_priorities(self):
        with self.assertRaises(TypeError) as context:
            self.not_imp_priority_cls()
        self.assertTrue(
            "Can't instantiate abstract class NotImpPriority "
            "with abstract method" in str(context.exception)
        )
        self.assertTrue("priorities" in str(context.exception))

    def test_new_validate_error(self):
        with self.assertRaises(FormatterValueError) as context:
            self.validate_fmt_cls()
        self.assertTrue(
            "Parsing value does not valid from validator"
            in str(context.exception)
        )


class ConstantTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.const: Type["fmt.Constant"] = fmt.Constant(
            {
                "%n": "normal",
                "%s": "special",
            }
        )
        self.ct = self.const.parse("normal_life", "%n_life")

    def test_const_parser_raise(self):
        with self.assertRaises(FormatterValueError) as context:
            self.const.parse("special_job", "%s_life")
        self.assertTrue(
            (
                "value 'special_job' does not match "
                "with format '(?P<constant>special)_life'"
            )
            in str(context.exception)
        )

    def test_const_properties(self):
        self.assertEqual(1, self.ct.level.value)
        self.assertEqual("special", self.ct.format("%s"))
