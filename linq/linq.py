import sys

from itertools import islice, groupby, takewhile, dropwhile, zip_longest
from typing import Generator, Iterable, Callable, Iterator, TypeVar, Generic, List, Optional, Tuple, Any, cast, Final

from more_itertools import first, interleave_longest, last, chunked, unique_everseen

PYTHON_VERSION: Final[Tuple[int, int]] = sys.version_info[:2]

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')


class Linq(Generic[T]):
    def __init__(self, iterable: Iterable[T]) -> None:
        """
        Initialize a new instance of the Linq class.

        Args:
            iterable (Iterable[T]): The source iterable.
        """
        self.iterable: Iterable[T] = iterable

    def select(self, func: Callable[[T], U]) -> 'Linq[U]':
        """
        Applies the given function to each element in the iterable and returns a new Linq object.

        Args:
            func (Callable[[T], U]): The function to apply to each element.

        Returns:
            Linq[U]: A new Linq object with the transformed elements.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.select(lambda x: x * 2).to_list()
            >>> print(result)
            [2, 4, 6]
        """
        return Linq(map(func, self.iterable))

    def where(self, predicate: Callable[[T], bool]) -> 'Linq[T]':
        """
        Filters the elements of the iterable based on the given predicate.

        Args:
            predicate: A callable that takes an element of the iterable as input and returns a boolean value.

        Returns:
            A new instance of Linq containing the filtered elements.

        Example:
            >>> linq = Linq([1, 2, 3, 4])
            >>> result = linq.where(lambda x: x % 2 == 0).to_list()
            >>> print(result)
            [2, 4]
        """
        return Linq(filter(predicate, self.iterable))

    def take(self, count: int) -> 'Linq[T]':
        """
        Returns a new Linq object that contains the first `count` elements from the current Linq object.

        Parameters:
            count (int): The number of elements to take from the current Linq object.

        Returns:
            Linq[T]: A new Linq object that contains the first `count` elements from the current Linq object.

        Example:
            >>> linq = Linq([1, 2, 3, 4, 5])
            >>> result = linq.take(3).to_list()
            >>> print(result)
            [1, 2, 3]
        """
        return Linq(islice(self.iterable, count))

    def skip(self, count: int) -> 'Linq[T]':
        """
        Skips the specified number of elements from the beginning of the iterable.

        Args:
            count (int): The number of elements to skip.

        Returns:
            Linq[T]: A new Linq object that skips the specified number of elements.

        Example:
            >>> linq = Linq([1, 2, 3, 4, 5])
            >>> result = linq.skip(2).to_list()
            >>> print(result)
            [3, 4, 5]
        """
        return Linq(islice(self.iterable, count, None))

    def group_by(self, key_func: Callable[[T], K]) -> 'Linq[Tuple[K, List[T]]]':
        """
        Groups the elements of the iterable based on the provided key function.

        Args:
            key_func (Callable[[T], K]): A function that maps each element of the iterable to a key.

        Returns:
            Linq[Tuple[K, List[T]]]: A new Linq object containing tuples of keys and lists of grouped elements.

        Example:
            >>> linq = Linq(['apple', 'banana', 'apricot', 'blueberry'])
            >>> result = linq.group_by(lambda x: x[0]).to_list()
            >>> print(result)
            [('a', ['apple', 'apricot']), ('b', ['banana', 'blueberry'])]
        """
        sorted_iterable = sorted(self.iterable, key=cast(Callable, key_func))
        return Linq(((key, list(group)) for key, group in groupby(sorted_iterable, key_func)))

    def to_list(self) -> List[T]:
        """
        Converts the iterable into a list.

        Returns:
            List[T]: A list containing the elements of the iterable.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.to_list()
            >>> print(result)
            [1, 2, 3]
        """
        return list(self.iterable)

    def first(self, default: Optional[T] = None) -> Optional[T]:
        """
        Returns the first element of the iterable or the default value if the iterable is empty.

        Parameters:
            default (Optional[T]): The default value to return if the iterable is empty. Defaults to None.

        Returns:
            Optional[T]: The first element of the iterable or the default value if the iterable is empty.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.first_or_default()
            >>> print(result)
            1

            >>> empty_linq = Linq([])
            >>> result = empty_linq.first_or_default(42)
            >>> print(result)
            42
        """
        return first(iter(self.iterable), default=default)

    def last(self, default: Optional[T] = None) -> Optional[T]:
        """
        Returns the last element of the iterable or the default value if the iterable is empty.

        Parameters:
            default (Optional[T]): The default value to return if the iterable is empty.

        Returns:
            Optional[T]: The last element of the iterable or the default value if the iterable is empty.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.last_or_default()
            >>> print(result)
            3

            >>> empty_linq = Linq([])
            >>> result = empty_linq.last_or_default(42)
            >>> print(result)
            42
        """
        return last(iter(self.iterable), default=default)

    def any(self, predicate: Callable[[T], bool] = lambda x: True) -> bool:
        """
        Check if any element in the iterable satisfies the given predicate.

        Parameters:
        - predicate: A callable that takes an element from the iterable and returns a boolean value.
                     If not provided, it defaults to a function that always returns True.

        Returns:
        - bool: True if any element in the iterable satisfies the predicate, False otherwise.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.any(lambda x: x > 2)
            >>> print(result)
            True

            >>> result = linq.any(lambda x: x > 3)
            >>> print(result)
            False
        """
        return any(map(predicate, self.iterable))

    def all(self, predicate: Callable[[T], bool] = lambda x: True) -> bool:
        """
        Returns True if all elements in the iterable satisfy the given predicate,
        or if the iterable is empty. Otherwise, returns False.

        Parameters:
            predicate (Callable[[T], bool], optional): A function that takes an element
                from the iterable and returns a boolean value indicating whether the
                element satisfies the condition. Defaults to lambda x: True.

        Returns:
            bool: True if all elements satisfy the predicate or if the iterable is empty,
            False otherwise.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.all(lambda x: x > 0)
            >>> print(result)
            True

            >>> result = linq.all(lambda x: x > 1)
            >>> print(result)
            False
        """
        return all(map(predicate, self.iterable))

    def count(self) -> int:
        """
        Returns the number of elements in the iterable.

        Returns:
            int: The number of elements in the iterable.

        Example:
            >>> linq = Linq([1, 2, 3, 4])
            >>> result = linq.count()
            >>> print(result)
            4
        """
        return sum(1 for _ in self.iterable)

    def order_by(self, key: Callable[[T], Any], reverse: bool = False) -> 'Linq[T]':
        """
        Orders the elements of the Linq object based on the specified key.

        Parameters:
            key (Callable[[T], Any]): A function that takes an element of the Linq object and returns a value to use for sorting.
            reverse (bool): If True, sorts the elements in descending order. Defaults to False.

        Returns:
            Linq[T]: A new Linq object with the elements sorted based on the specified key.

        Example:
            >>> linq = Linq([{'name': 'apple', 'price': 5}, {'name': 'banana', 'price': 3}])
            >>> result = linq.order_by(lambda x: x['price']).to_list()
            >>> print(result)
            [{'name': 'banana', 'price': 3}, {'name': 'apple', 'price': [{'name': 'banana', 'price': 3}, {'name': 'apple', 'price': 5}]

            >>> result = linq.order_by(lambda x: x['price'], reverse=True).to_list()
            >>> print(result)
            [{'name': 'apple', 'price': 5}, {'name': 'banana', 'price': 3}]
        """
        return Linq(sorted(self.iterable, key=key, reverse=reverse))

    def distinct(self) -> 'Linq[T]':
        """
        Returns a new Linq object with distinct elements from the original iterable.

        Returns:
            Linq[T]: A new Linq object with distinct elements.

        Example:
            >>> linq = Linq([1, 2, 2, 3, 4, 4])
            >>> result = linq.distinct().to_list()
            >>> print(result)
            [1, 2, 3, 4]
        """

        def remove_duplicates(iterable: Iterable[T]) -> Generator[T, None, None]:
            seen = set()
            for item in iterable:
                if item not in seen:
                    seen.add(item)
                    yield item

        return Linq(remove_duplicates(self.iterable))

    def take_while(self, predicate: Callable[[T], bool]) -> 'Linq[T]':
        """
        Returns elements from the iterable as long as the predicate is True.

        Args:
            predicate (Callable[[T], bool]): A function that takes an element and returns a boolean value.

        Returns:
            Linq[T]: A new Linq object with elements that satisfy the predicate.

        Example:
            >>> linq = Linq([1, 2, 3, 4, 5])
            >>> result = linq.take_while(lambda x: x < 4).to_list()
            >>> print(result)
            [1, 2, 3]
        """
        return Linq(takewhile(predicate, self.iterable))

    def skip_while(self, predicate: Callable[[T], bool]) -> 'Linq[T]':
        """
        Skips elements from the iterable as long as the predicate is True.

        Args:
            predicate (Callable[[T], bool]): A function that takes an element and returns a boolean value.

        Returns:
            Linq[T]: A new Linq object with elements that do not satisfy the predicate.

        Example:
            >>> linq = Linq([1, 2, 3, 4, 5])
            >>> result = linq.skip_while(lambda x: x < 4).to_list()
            >>> print(result)
            [4, 5]
        """
        return Linq(dropwhile(predicate, self.iterable))

    def zip_with(self, *others: Iterable[Any]) -> 'Linq[Tuple[T, ...]]':
        """
        Zips the iterable with one or more other iterables.

        Args:
            *others (Iterable[Any]): Other iterables to zip with.

        Returns:
            Linq[Tuple[T, ...]]: A new Linq object with tuples containing elements from each iterable.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.zip_with(['a', 'b', 'c']).to_list()
            >>> print(result)
            [(1, 'a'), (2, 'b'), (3, 'c')]
        """

        return Linq(zip_longest(self.iterable, *others))

    def zip_longest_with(self, *others: Iterable[Any], fillvalue: Optional[Any] = None) -> 'Linq[Tuple[T, ...]]':
        """
        Zips the iterable with one or more other iterables using a fill value for missing elements.

        Args:
            *others (Iterable[Any]): Other iterables to zip with.
            fillvalue (Optional[Any]): The value to use for missing elements. Defaults to None.

        Returns:
            Linq[Tuple[T, ...]]: A new Linq object with tuples containing elements from each iterable.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.zip_longest_with(['a', 'b'], fillvalue='x').to_list()
            >>> print(result)
            [(1, 'a'), (2, 'b'), (3, 'x')]
        """
        return Linq(zip_longest(self.iterable, *others, fillvalue=fillvalue))

    def batch(self, size: int) -> 'Linq[Tuple[T, ...]]':
        """
        Batches elements of the iterable into tuples of the specified size.

        Args:
            size (int): The size of each batch.

        Returns:
            Linq[Tuple[T, ...]]: A new Linq object with tuples of elements.

        Example:
            >>> linq = Linq([1, 2, 3, 4, 5, 6])
            >>> result = linq.batch(2).to_list()
            >>> print(result)
            [(1, 2), (3, 4), (5, 6)]
        """

        if PYTHON_VERSION < (3, 12):
            from more_itertools import batched
        else:
            from itertools import batched

        return Linq(batched(self.iterable, size))

    def chunk_into(self, size: int, strict: bool = False) -> 'Linq[List[T]]':
        """
        Chunks the iterable into lists of the specified size.

        Args:
            size (int): The size of each chunk.
            strict (bool, optional): If True, raises an error if the iterable cannot be evenly divided into chunks of the specified size. Defaults to False.

        Returns:
            Linq[List[T]]: A new Linq object containing the chunked lists.

        """
        return Linq(chunked(self.iterable, size, strict))

    def consecutive_pairs(self) -> 'Linq[Tuple[T, T]]':
        """
        Returns an iterable of consecutive pairs of elements.

        Returns:
            Linq[Tuple[T, T]]: A new Linq object with consecutive pairs of elements.

        Example:
            >>> linq = Linq([1, 2, 3, 4])
            >>> result = linq.consecutive_pairs().to_list()
            >>> print(result)
            [(1, 2), (2, 3), (3, 4)]
        """
        if PYTHON_VERSION < (3, 10):
            from more_itertools import pairwise
        else:
            from itertools import pairwise
        return Linq(pairwise(self.iterable))

    def unique_seen(self, key: Optional[Callable[[T], Any]] = None) -> 'Linq[T]':
        """
        Returns unique elements in the order they are first seen, based on a specified key function.

        Args:
            key (Optional[Callable[[T], Any]]): A function that takes an element as input and returns a value
                to be compared for uniqueness. Defaults to None, meaning the elements themselves are compared.

        Returns:
            Linq[T]: A new Linq object with unique elements in the order they were first seen.

        Examples:

            # Example 1: Unique elements based on their length
            >>> linq = Linq(['apple', 'banana', 'pear', 'apricot', 'peach'])
            >>> result = linq.unique_seen(key=len).to_list()
            >>> print(result)
            ['apple', 'banana', 'apricot']

            # Example 2: Unique elements based on the first character
            >>> linq = Linq(['apple', 'banana', 'avocado', 'blueberry', 'cherry'])
            >>> result = linq.unique_seen(key=lambda x: x[0]).to_list()
            >>> print(result)
            ['apple', 'banana', 'cherry']

            # Example 3: Unique elements based on a dictionary attribute
            >>> linq = Linq([
            ...     {'name': 'apple', 'color': 'red'},
            ...     {'name': 'banana', 'color': 'yellow'},
            ...     {'name': 'cherry', 'color': 'red'},
            ...     {'name': 'pear', 'color': 'green'}
            ... ])
            >>> result = linq.unique_seen(key=lambda x: x['color']).to_list()
            >>> print(result)
            [{'name': 'apple', 'color': 'red'}, {'name': 'banana', 'color': 'yellow'}, {'name': 'pear', 'color': 'green'}]

            # Example 4: Unique elements ignoring case sensitivity
            >>> linq = Linq(['Apple', 'banana', 'apple', 'Banana', 'CHERRY'])
            >>> result = linq.unique_seen(key=lambda x: x.lower()).to_list()
            >>> print(result)
            ['Apple', 'banana', 'CHERRY']
        """
        return Linq(unique_everseen(self.iterable, key=key))

    def interleave_with(self, *others: Iterable) -> 'Linq[T]':
        """
        Interleaves the elements of the iterable with the elements of other iterables, filling with None
        if one iterable is shorter.

        Args:
            *others (Iterable[T]): Other iterables to interleave with.

        Returns:
            Linq[T]: A new Linq object with interleaved elements.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> result = linq.interleave_with(['a', 'b'], ['x', 'y', 'z']).to_list()
            >>> print(result)
            [1, 'a', 'x', 2, 'b', 'y', 3, None, 'z']
        """
        return Linq(interleave_longest(self.iterable, *others))

    def __iter__(self) -> Iterator[T]:
        """
        Returns an iterator for the iterable.

        Returns:
            Iterator[T]: An iterator for the iterable.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> for item in linq:
            ...     print(item)
            1
            2
            3
        """
        return iter(self.iterable)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Linq object.

        Returns:
            str: A string representation of the Linq object.

        Example:
            >>> linq = Linq([1, 2, 3])
            >>> repr(linq)
            'Linq([1, 2, 3])'
        """
        limit: int = 10
        iterator: Iterator[T] = iter(self.iterable)
        preview: List[T] = list(islice(iterator, limit))
        repr_s: str = ', '.join(map(repr, preview)) if len(preview) < limit else f'{", ".join(map(repr, preview))}, ...'
        return f'Linq([{repr_s}])'
