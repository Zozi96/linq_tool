# Linq Tool

![Build Status](https://github.com/Zozi96/linq_tool/actions/workflows/tests.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/linq-tool.svg)
![License](https://img.shields.io/github/license/Zozi96/linq_tool.svg)

Linq is a Python package that provides LINQ-like functionality for performing common operations on iterables. Inspired by LINQ from C#, this package allows you to easily manipulate collections in a functional style.

## Features

- **Select**: Project each element of a sequence into a new form.
- **Where**: Filter elements based on a predicate.
- **GroupBy**: Group elements by a key selector function.
- **OrderBy**: Sort elements based on a key.
- **Distinct**: Remove duplicate elements.
- And many more!

## Installation

You can install Linq via pip:

```bash
pip install linq-tool
```

## Usage Examples

You might create a Linq instance and iterate throughout the object

```python
linq = Linq([1, 2, 3])
for item in linq:
    print(item) # 1
```

The object is an iterable, if you need to use it as list, you need to invoke the `to_list` method

### Select

```python
from linq_tool import Linq

linq = Linq([1, 2, 3])
result = linq.select(lambda x: x * 2).to_list()
print(result)  # Output: [2, 4, 6]
```

### Where

```python
linq = Linq([1, 2, 3, 4])
result = linq.where(lambda x: x % 2 == 0).to_list()
print(result)  # Output: [2, 4]
```

### GroupBy

```python
linq = Linq(['apple', 'banana', 'apricot', 'blueberry'])
result = linq.group_by(lambda x: x[0]).to_list()
print(result)  # Output: [('a', ['apple', 'apricot']), ('b', ['banana', 'blueberry'])]
```

### OrderBy

```python
linq = Linq([{'name': 'apple', 'price': 5}, {'name': 'banana', 'price': 3}])
result = linq.order_by(lambda x: x['price']).to_list()
print(result)  # Output: [{'name': 'banana', 'price': 3}, {'name': 'apple', 'price': 5}]
```

### Distinct

```python
linq = Linq([1, 2, 2, 3, 4, 4])
result = linq.distinct().to_list()
print(result)  # Output: [1, 2, 3, 4]
```

### Take

```python
linq = Linq([1, 2, 2, 3, 4, 4])
result = linq.distinct().to_list()
print(result)  # Output: [1, 2, 3, 4]
```

### Skip

```python
linq = Linq([1, 2, 3, 4, 5])
result = linq.skip(2).to_list()
print(result)  # Output: [3, 4, 5]
```

### FirstOrDefault

```python
linq = Linq([1, 2, 3])
result = linq.first_or_default()
print(result)  # Output: 1

empty_linq = Linq([])
result = empty_linq.first_or_default(42)
print(result)  # Output: 42
```

### LastOrDefault

```python
linq = Linq([1, 2, 3])
result = linq.last_or_default()
print(result)  # Output: 3

empty_linq = Linq([])
result = empty_linq.last_or_default(42)
print(result)  # Output: 42
```

### Any

```python
linq = Linq([1, 2, 3])
result = linq.any(lambda x: x > 2)
print(result)  # Output: True

result = linq.any(lambda x: x > 3)
print(result)  # Output: False
```

### All

```python
linq = Linq([1, 2, 3])
result = linq.all(lambda x: x > 0)
print(result)  # Output: True

result = linq.all(lambda x: x > 1)
print(result)  # Output: False
```

### Count

```python
linq = Linq([1, 2, 3, 4])
result = linq.count()
print(result)  # Output: 4
```

### TakeWhile

```python
linq = Linq([1, 2, 3, 4, 5])
result = linq.take_while(lambda x: x < 4).to_list()
print(result)  # Output: [1, 2, 3]
```

### SkipWhile

```python
linq = Linq([1, 2, 3, 4, 5])
result = linq.skip_while(lambda x: x < 4).to_list()
print(result)  # Output: [4, 5]
```

### SkipWhile

```python
linq = Linq([1, 2, 3, 4, 5])
result = linq.skip_while(lambda x: x < 4).to_list()
print(result)  # Output: [4, 5]
```

### ZipWith

```python
linq = Linq([1, 2, 3])
result = linq.zip_with(['a', 'b', 'c']).to_list()
print(result)  # Output: [(1, 'a'), (2, 'b'), (3, 'c')]
```

### ZipLongest

```python
linq = Linq([1, 2, 3])
result = linq.zip_longest_with(['a', 'b'], fillvalue='x').to_list()
print(result)  # Output: [(1, 'a'), (2, 'b'), (3, 'x')]
```

### Batch

```python
linq = Linq([1, 2, 3, 4, 5, 6])
result = linq.batch(2).to_list()
print(result) # [(1, 2), (3, 4), (5, 6)]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
