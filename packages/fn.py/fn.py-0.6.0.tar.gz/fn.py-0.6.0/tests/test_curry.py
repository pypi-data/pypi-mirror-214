import unittest

from fn.func import curried, _has_type_hint_support


class Curriedtest(unittest.TestCase):

    def _assert_instance(self, expected, acutal):
        self.assertEqual(expected.__module__, acutal.__module__)
        self.assertEqual(expected.__name__, acutal.__name__)

        if _has_type_hint_support:
            self.assertEqual(expected.__annotations__, acutal.__annotations__)

    def test_curried_wrapper(self):

        @curried
        def _child(a, b, c, d):
            return a + b + c + d

        @curried
        def _moma(a, b):
            return _child(a, b)

        res1 = _moma(1)
        self._assert_instance(_moma, res1)
        res2 = res1(2)
        self._assert_instance(_child, res2)
        res3 = res2(3)
        self._assert_instance(_child, res3)
        res4 = res3(4)

        self.assertEqual(res4, 10)

    @unittest.skipIf(not _has_type_hint_support, "Type hint aren't supported")
    def test_curried_with_annotations_when_they_are_supported(self):

        def _custom_sum(a, b, c, d):
            return a + b + c + d

        _custom_sum.__annotations__ = {
                                        'a': int,
                                        'b': int,
                                        'c': int,
                                        'd': int,
                                        'return': int
                                      }

        custom_sum = curried(_custom_sum)

        res1 = custom_sum(1)
        self._assert_instance(custom_sum, res1)
        res2 = res1(2)
        self._assert_instance(custom_sum, res2)
        res3 = res2(3)
        self._assert_instance(custom_sum, res3)
        res4 = res3(4)

        self.assertEqual(res4, 10)
