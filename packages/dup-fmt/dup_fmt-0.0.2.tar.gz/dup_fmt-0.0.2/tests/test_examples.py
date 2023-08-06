# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object examples.
"""
import unittest
from datetime import datetime

from packaging.version import Version

import dup_fmt.formatter as fmt


class DatetimeExampleTestCase(unittest.TestCase):
    def test_parse_examples(self):
        self.assertEqual(
            datetime(2021, 1, 1, microsecond=135000),
            fmt.Datetime.parse("2021-01-1 135043", "%Y-%m-%-d %f").value,
        )
        # FIXME: this datetime does not match with monday in this week
        self.assertEqual(
            datetime(2021, 1, 3),
            fmt.Datetime.parse("2021-Jan Monday 3", "%Y-%b %A %-d").value,
        )


class VersionExampleTestCase(unittest.TestCase):
    def test_parse_examples(self):
        self.assertEqual(
            Version("1.0.5"),
            fmt.Version.parse("version: 1-0-5", "version: %m-%n-%c").value,
        )
