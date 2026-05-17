import numpy as np
import pytest
from pydsa import (
    activity_selection,
    job_sequencing,
    fractional_knapsack,
    huffman_coding,
)


class TestActivitySelection:
    """activity_selection"""

    def test_empty_arrays(self):
        start = np.array([], dtype=int)
        finish = np.array([], dtype=int)
        result = activity_selection(start, finish)
        assert len(result) == 0

    def test_single_activity(self):
        start = np.array([1], dtype=int)
        finish = np.array([4], dtype=int)
        result = activity_selection(start, finish)
        assert list(result) == [0]

    def test_all_compatible(self):
        start = np.array([1, 3, 5], dtype=int)
        finish = np.array([2, 4, 6], dtype=int)
        result = activity_selection(start, finish)
        assert list(result) == [0, 1, 2]

    def test_classic_case(self):
        start = np.array([1, 3, 0, 5, 8, 5], dtype=int)
        finish = np.array([2, 4, 6, 7, 9, 9], dtype=int)
        result = activity_selection(start, finish)
        assert list(result) == [0, 1, 3, 4]

    def test_overlapping(self):
        start = np.array([1, 2, 3], dtype=int)
        finish = np.array([4, 3, 4], dtype=int)
        result = activity_selection(start, finish)
        assert len(result) in [1, 2]  # depends on sort stability

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError):
            activity_selection(np.array([1, 2]), np.array([1, 2, 3]))


class TestJobSequencing:
    """job_sequencing"""

    def test_empty_arrays(self):
        deadlines = np.array([], dtype=int)
        profits = np.array([], dtype=int)
        result = job_sequencing(deadlines, profits)
        assert len(result) == 0

    def test_single_job(self):
        deadlines = np.array([2], dtype=int)
        profits = np.array([100], dtype=int)
        result = job_sequencing(deadlines, profits)
        assert list(result) == [0]

    def test_all_jobs_fit(self):
        deadlines = np.array([1, 1, 1], dtype=int)
        profits = np.array([10, 5, 8], dtype=int)
        result = job_sequencing(deadlines, profits)
        assert list(result) == [0]

    def test_classic_case(self):
        deadlines = np.array([4, 1, 1, 1], dtype=int)
        profits = np.array([20, 10, 40, 30], dtype=int)
        result = job_sequencing(deadlines, profits)
        assert np.sum(profits[result]) == 60  # 20+40

    def test_multiple_slots(self):
        deadlines = np.array([2, 1, 2], dtype=int)
        profits = np.array([100, 50, 80], dtype=int)
        result = job_sequencing(deadlines, profits)
        assert np.sum(profits[result]) == 180

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError):
            job_sequencing(np.array([1, 2]), np.array([1, 2, 3]))


class TestFractionalKnapsack:
    """fractional_knapsack"""

    def test_empty_arrays(self):
        total_weight, total_price = fractional_knapsack(
            np.array([], dtype=float),
            np.array([], dtype=float),
            10
        )
        assert total_weight == 0
        assert total_price == 0

    def test_single_item_fits(self):
        w, p = fractional_knapsack(
            np.array([5.0]), np.array([10.0]), 10
        )
        assert w == 5.0
        assert p == 10.0

    def test_single_item_partial(self):
        w, p = fractional_knapsack(
            np.array([10.0]), np.array([50.0]), 3
        )
        assert w == 3.0
        assert p == 15.0  # 50 * (3/10)

    def test_classic_case(self):
        w, p = fractional_knapsack(
            np.array([10.0, 20.0, 30.0]),
            np.array([60.0, 100.0, 120.0]),
            50
        )
        assert w == 50.0
        assert p == 240.0  # 10+20+20

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError):
            fractional_knapsack(np.array([1.0, 2.0]), np.array([1.0, 2.0, 3.0]), 5)


class TestHuffmanCoding:
    """huffman_coding"""

    def test_empty_text(self):
        encoded, codes = huffman_coding("")
        assert encoded == ""
        assert codes == {}

    def test_single_character(self):
        encoded, codes = huffman_coding("aaaa")
        assert encoded == "0000"
        assert codes == {"a": "0"}

    def test_two_characters(self):
        encoded, codes = huffman_coding("aab")
        assert len(codes) == 2
        assert set(codes.keys()) == {"a", "b"}
        assert codes["a"] != codes["b"]

    def test_prefix_free(self):
        text = "hello world"
        _, codes = huffman_coding(text)
        code_list = list(codes.values())
        for i, c1 in enumerate(code_list):
            for j, c2 in enumerate(code_list):
                if i != j:
                    assert not c1.startswith(c2), f"{c1} is prefix of {c2}"

    def test_encoding_decoding(self):
        text = "mississippi river"
        encoded, codes = huffman_coding(text)
        reverse_codes = {v: k for k, v in codes.items()}
        decoded = ""
        temp = ""
        for bit in encoded:
            temp += bit
            if temp in reverse_codes:
                decoded += reverse_codes[temp]
                temp = ""
        assert decoded == text

    def test_all_unique(self):
        text = "abcdef"
        encoded, codes = huffman_coding(text)
        assert len(codes) == 6
        assert len(encoded) == sum(len(codes[c]) for c in text)

    def test_common_text(self):
        text = "this is an example of a huffman tree"
        encoded, codes = huffman_coding(text)
        assert len(codes) > 0
        assert len(encoded) > 0
        reverse_codes = {v: k for k, v in codes.items()}
        decoded = ""
        temp = ""
        for bit in encoded:
            temp += bit
            if temp in reverse_codes:
                decoded += reverse_codes[temp]
                temp = ""
        assert decoded == text