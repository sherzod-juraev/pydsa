import random

import pytest

from pydsa.exc import InvalidValueError
from pydsa.sorting import bucket_sort, counting_sort, radix_sort

INTEGER_SORTS = [counting_sort, radix_sort]


@pytest.mark.parametrize("sort_fn", INTEGER_SORTS)
class TestIntegerSorts:
    def test_empty(self, sort_fn) -> None:
        assert sort_fn([]) == []

    def test_single_element(self, sort_fn) -> None:
        assert sort_fn([7]) == [7]

    def test_single_zero(self, sort_fn) -> None:
        assert sort_fn([0]) == [0]

    def test_basic(self, sort_fn) -> None:
        assert sort_fn([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]

    def test_all_zeros_and_all_equal(self, sort_fn) -> None:
        assert sort_fn([0, 0, 0]) == [0, 0, 0]
        assert sort_fn([9] * 6) == [9] * 6

    def test_already_sorted_and_reversed(self, sort_fn) -> None:
        assert sort_fn([1, 2, 3, 4]) == [1, 2, 3, 4]
        assert sort_fn([4, 3, 2, 1]) == [1, 2, 3, 4]

    def test_values_with_different_digit_counts(self, sort_fn) -> None:
        data = [100, 5, 99, 1000, 0, 10, 7]
        assert sort_fn(data) == sorted(data)

    def test_input_is_not_modified_and_result_is_a_new_list(self, sort_fn) -> None:
        data = [3, 1, 2]
        result = sort_fn(data)
        assert data == [3, 1, 2]
        assert result is not data

    def test_single_element_result_is_a_copy(self, sort_fn) -> None:
        data = [3]
        assert sort_fn(data) is not data

    def test_negative_number_is_rejected(self, sort_fn) -> None:
        with pytest.raises(InvalidValueError):
            sort_fn([3, -1, 2])

    def test_single_negative_number_is_rejected(self, sort_fn) -> None:
        with pytest.raises(InvalidValueError):
            sort_fn([-5])

    def test_negative_at_either_end_is_rejected(self, sort_fn) -> None:
        with pytest.raises(InvalidValueError):
            sort_fn([-1, 2, 3])
        with pytest.raises(InvalidValueError):
            sort_fn([1, 2, -3])

    def test_invalid_value_error_is_also_a_value_error(self, sort_fn) -> None:
        with pytest.raises(ValueError):
            sort_fn([-1])

    @pytest.mark.parametrize("seed", range(15))
    def test_random_against_builtin_sorted(self, sort_fn, seed: int) -> None:
        rng = random.Random(seed)
        data = [rng.randrange(0, 500) for _ in range(rng.randrange(0, 150))]
        assert sort_fn(data) == sorted(data)


class TestCountingSort:
    def test_large_gap_between_values(self) -> None:
        assert counting_sort([0, 100_000]) == [0, 100_000]


class TestRadixSort:
    def test_large_numbers(self) -> None:
        data = [10**12 + 3, 5, 10**9, 10**12, 0]
        assert radix_sort(data) == sorted(data)

    def test_equal_digits_keep_a_stable_inner_pass(self) -> None:
        data = [170, 45, 75, 90, 802, 24, 2, 66]
        assert radix_sort(data) == sorted(data)

    @pytest.mark.parametrize("base_value", [9, 10, 11, 99, 100, 101, 999, 1000, 1001])
    def test_digit_count_boundaries(self, base_value: int) -> None:
        data = [base_value, 1, base_value - 1, 0]
        assert radix_sort(data) == sorted(data)


class TestBucketSort:
    def test_empty_and_single(self) -> None:
        assert bucket_sort([]) == []
        assert bucket_sort([0.5]) == [0.5]

    def test_floats_in_unit_interval(self) -> None:
        data = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
        assert bucket_sort(data) == sorted(data)

    def test_negative_and_large_floats(self) -> None:
        data = [-3.5, 100.25, 0.0, -0.5, 42.0, -100.0]
        assert bucket_sort(data) == sorted(data)

    def test_integers_stay_integers(self) -> None:
        result = bucket_sort([3, 1, 2])
        assert result == [1, 2, 3]
        assert all(type(v) is int for v in result)

    def test_all_equal_values(self) -> None:
        assert bucket_sort([2.5] * 8) == [2.5] * 8

    def test_two_distinct_values(self) -> None:
        assert bucket_sort([1.0, 0.0, 1.0, 0.0]) == [0.0, 0.0, 1.0, 1.0]

    def test_input_is_not_modified(self) -> None:
        data = [0.3, 0.1, 0.2]
        bucket_sort(data)
        assert data == [0.3, 0.1, 0.2]

    def test_heavily_clustered_values(self) -> None:
        data = [1000.0 + i * 1e-6 for i in range(50)][::-1] + [0.0]
        assert bucket_sort(data) == sorted(data)

    @pytest.mark.parametrize("seed", range(15))
    def test_random_floats(self, seed: int) -> None:
        rng = random.Random(seed)
        data = [rng.uniform(-50, 50) for _ in range(rng.randrange(0, 120))]
        assert bucket_sort(data) == sorted(data)
