import unittest

from sciform import Formatter, ExpMode, GroupingSeparator, FillMode


class TestFormatting(unittest.TestCase):
    def do_test_case_dict(self, cases_dict: dict[float, dict[Formatter, str]]):
        for num, fmt_dict in cases_dict.items():
            for formatter, expected_num_str in fmt_dict.items():
                snum_str = formatter(num)
                with self.subTest(num=num,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    self.assertEqual(snum_str, expected_num_str)

    def test_superscript_exp(self):
        cases_dict = {
            789: {
                Formatter(exp_mode=ExpMode.SCIENTIFIC,
                          superscript_exp=True): '7.89×10²'
            }
        }

        self.do_test_case_dict(cases_dict)

    def test_fill_and_separators(self):
        cases_dict = {
            123456789.654321: {
                Formatter(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.ZERO,
                    top_dig_place=14): '000_000_123_456_789.654_321',
                Formatter(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.SPACE,
                    top_dig_place=14): '      123_456_789.654_321',
            },
            4567899.7654321: {
                Formatter(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.ZERO,
                    top_dig_place=14): '000_000_004_567_899.765_432_1',
                Formatter(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.SPACE,
                    top_dig_place=14): '        4_567_899.765_432_1',
            }
        }

        self.do_test_case_dict(cases_dict)

