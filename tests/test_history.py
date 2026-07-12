import unittest
from history import History


class TestHistory(unittest.TestCase):
    def test_date_parsing(self):
        h = History(None, "1:23.4", "21.07.15", "良", "外", "1", "36.5", "Taro")
        self.assertEqual(h.getDateStr(), "2021.07.15")

    def test_get_time_int(self):
        h = History(None, "1:23.4", "21.07.15")
        self.assertEqual(h.getTimeInt(), 834)

    def test_get_time_invalid(self):
        h = History(None, "bad", "21.07.15")
        self.assertEqual(h.getTimeInt(), 0)

    def test_get_time_format(self):
        h = History(None, "1:23.4", "21.07.15", "良", "外", "1", "36.5", "Taro")
        self.assertIn("1:23.4 [36.5]  (2021.07.15 良 1/外)", h.getTime())

    def test_has_history(self):
        rc1 = object()
        rc2 = object()
        h = History(rc1, "")
        self.assertTrue(h.hasHistory(rc1))
        self.assertFalse(h.hasHistory(rc2))


if __name__ == '__main__':
    unittest.main()
