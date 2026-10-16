import random

import pytest

from pydsa.sorting import heap_sort


def test_empty_and_single() -> None:
    assert heap_sort([]) == []
    assert heap_sort([1]) == [1]


def test_input_is_not_modified() -> None:
    data = [3, 1, 2]
    heap_sort(data)
    assert data == [3, 1, 2]


def test_large_random_input() -> None:
    rng = random.Random(9)
    data = [rng.randrange(-1000, 1000) for _ in range(5_000)]
    assert heap_sort(data) == sorted(data)


def test_import_exposes_the_function_not_the_module() -> None:
    import pydsa.sorting as sorting

    assert callable(sorting.heap_sort)
    assert callable(sorting.heap_sort)
    assert sorting.heap_sort.__name__ == "heap_sort"


@pytest.mark.parametrize("seed", range(10))
def test_random_with_duplicates(seed: int) -> None:
    rng = random.Random(seed)
    data = [rng.randrange(8) for _ in range(rng.randrange(0, 60))]
    assert heap_sort(data) == sorted(data)
