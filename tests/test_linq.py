import unittest
from linq import Linq


class TestLinq(unittest.TestCase):

    def test_select(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.select(lambda x: x * 2).to_list()
        self.assertEqual(result, [2, 4, 6])

    def test_where(self) -> None:
        linq = Linq([1, 2, 3, 4])
        result = linq.where(lambda x: x % 2 == 0).to_list()
        self.assertEqual(result, [2, 4])

    def test_group_by(self) -> None:
        linq = Linq(['apple', 'banana', 'apricot', 'blueberry'])
        result = linq.group_by(lambda x: x[0]).to_list()
        print(result)
        expected = [('a', ['apple', 'apricot']), ('b', ['banana', 'blueberry'])]
        self.assertEqual(result, expected)

    def test_take(self) -> None:
        linq = Linq([1, 2, 3, 4, 5])
        result = linq.take(3).to_list()
        self.assertEqual(result, [1, 2, 3])

    def test_skip(self) -> None:
        linq = Linq([1, 2, 3, 4, 5])
        result = linq.skip(2).to_list()
        self.assertEqual(result, [3, 4, 5])

    def test_first_or_default(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.first_or_default()
        self.assertEqual(result, 1)

        empty_linq = Linq([])
        result = empty_linq.first_or_default(42)
        self.assertEqual(result, 42)

    def test_last_or_default(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.last_or_default()
        self.assertEqual(result, 3)

        empty_linq = Linq([])
        result = empty_linq.last_or_default(42)
        self.assertEqual(result, 42)

    def test_any(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.any(lambda x: x > 2)
        self.assertTrue(result)

        result = linq.any(lambda x: x > 3)
        self.assertFalse(result)

    def test_all(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.all(lambda x: x > 0)
        self.assertTrue(result)

        result = linq.all(lambda x: x > 1)
        self.assertFalse(result)

    def test_count(self) -> None:
        linq = Linq([1, 2, 3, 4])
        result = linq.count()
        self.assertEqual(result, 4)

    def test_distinct(self) -> None:
        linq = Linq([1, 2, 2, 3, 4, 4])
        result = linq.distinct().to_list()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_order_by(self) -> None:
        linq = Linq([{'name': 'apple', 'price': 5}, {'name': 'banana', 'price': 3}])
        result = linq.order_by(lambda x: x['price']).to_list()
        self.assertEqual(result, [{'name': 'banana', 'price': 3}, {'name': 'apple', 'price': 5}])

        result = linq.order_by(lambda x: x['price'], reverse=True).to_list()
        self.assertEqual(result, [{'name': 'apple', 'price': 5}, {'name': 'banana', 'price': 3}])

    def test_take_while(self) -> None:
        linq = Linq([1, 2, 3, 4, 5])
        result = linq.take_while(lambda x: x < 4).to_list()
        self.assertEqual(result, [1, 2, 3])

    def test_skip_while(self) -> None:
        linq = Linq([1, 2, 3, 4, 5])
        result = linq.skip_while(lambda x: x < 4).to_list()
        self.assertEqual(result, [4, 5])

    def test_zip_with(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.zip_with(['a', 'b', 'c']).to_list()
        self.assertEqual(result, [(1, 'a'), (2, 'b'), (3, 'c')])

    def test_zip_longest_with(self) -> None:
        linq = Linq([1, 2, 3])
        result = linq.zip_longest_with(['a', 'b'], fillvalue='x').to_list()
        self.assertEqual(result, [(1, 'a'), (2, 'b'), (3, 'x')])

    def test_batch(self) -> None:
        linq = Linq([1, 2, 3, 4, 5])
        result = linq.batch(2).to_list()
        self.assertEqual(result, [(1, 2), (3, 4), (5,)])


if __name__ == '__main__':
    unittest.main()
