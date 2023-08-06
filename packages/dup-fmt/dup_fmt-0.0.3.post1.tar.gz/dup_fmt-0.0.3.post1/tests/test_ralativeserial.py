# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the Serial formatter object.
"""
import unittest

import dup_fmt.formatter as fmt


class SerialTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ...

    def test_relative_serial(self):
        self.assertEqual(
            hash(5), fmt.relativeserial(**{"number": 5}).__hash__()
        )
        self.assertEqual(
            "<relativeserial(number=5)>",
            fmt.relativeserial(**{"number": 5}).__repr__(),
        )
        self.assertEqual(10, (5 + fmt.relativeserial(**{"number": 5})))
        self.assertEqual(10, (fmt.relativeserial(**{"number": 5}) + 5))
        self.assertEqual(0, (fmt.relativeserial(**{"number": 5}) - 5))
        self.assertEqual(0, (5 - fmt.relativeserial(**{"number": 5})))
        self.assertEqual(49, fmt.relativeserial(**{"number": 49}))
        self.assertTrue(
            fmt.relativeserial(**{"number": 10})
            == (
                fmt.relativeserial(**{"number": 5})
                + fmt.relativeserial(**{"number": 5})
            )
        )
        self.assertTrue(
            fmt.relativeserial(**{"number": 0})
            == (
                fmt.relativeserial(**{"number": 5})
                - fmt.relativeserial(**{"number": 5})
            )
        )
        self.assertTrue(
            fmt.relativeserial(**{"number": 15})
            >= (
                fmt.relativeserial(**{"number": 5})
                + fmt.relativeserial(**{"number": 5})
            )
        )
        self.assertEqual(
            fmt.relativeserial(**{"number": 15}),
            -fmt.relativeserial(**{"number": -15}),
        )
