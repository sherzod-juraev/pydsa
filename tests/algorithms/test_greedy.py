import pytest

from pydsa import (
    activity_selection,
    fractional_knapsack,
    huffman_coding,
    job_sequencing,
)


class TestActivitySelection:
    def test_classic_example(self) -> None:
        start = [1, 3, 0, 5, 8, 5]
        finish = [2, 4, 6, 7, 9, 9]
        assert activity_selection(start, finish) == [0, 1, 3, 4]

    def test_empty_input(self) -> None:
        assert activity_selection([], []) == []

    def test_mismatched_lengths_raises(self) -> None:
        with pytest.raises(ValueError):
            activity_selection([1, 2], [1])

    def test_single_activity(self) -> None:
        assert activity_selection([1], [2]) == [0]

    def test_all_overlapping_picks_one(self) -> None:
        # every activity overlaps every other — only one can be selected
        result = activity_selection([1, 1, 1], [10, 10, 10])
        assert len(result) == 1


class TestJobSequencing:
    def test_mismatched_lengths_raises(self) -> None:
        with pytest.raises(ValueError):
            job_sequencing([1, 2], [10])

    def test_empty_input(self) -> None:
        assert job_sequencing([], []) == []

    def test_all_same_deadline_picks_highest_profit(self) -> None:
        # deadline=1 for all — only one slot exists, must pick highest profit
        result = job_sequencing([1, 1, 1], [10, 40, 20])
        assert result == [1]

    def test_enough_slots_for_all(self) -> None:
        result = job_sequencing([3, 3, 3], [10, 20, 30])
        assert len(result) == 3


class TestFractionalKnapsack:
    def test_mismatched_lengths_raises(self) -> None:
        with pytest.raises(ValueError):
            fractional_knapsack([1, 2], [1], 5)

    def test_empty_input(self) -> None:
        assert fractional_knapsack([], [], 10) == (0.0, 0.0)

    def test_zero_capacity(self) -> None:
        weight, price = fractional_knapsack([1, 2, 3], [10, 20, 30], 0)
        assert weight == 0
        assert price == 0

    def test_capacity_fits_everything(self) -> None:
        weight, price = fractional_knapsack([1, 2, 3], [10, 20, 30], 100)
        assert weight == 6
        assert price == 60

    def test_fractional_split_occurs(self) -> None:
        # capacity smaller than total weight — best-ratio item taken first,
        # a fractional amount of the next item fills remaining capacity
        weight, price = fractional_knapsack([10, 20], [60, 100], 15)
        assert weight == 15


class TestHuffmanCoding:
    def test_empty_text(self) -> None:
        assert huffman_coding("") == ("", {})

    def test_single_character_text(self) -> None:
        encoded, codes = huffman_coding("aaaa")
        assert encoded == "0000"
        assert codes == {"a": "0"}

    def test_roundtrip_decoding(self) -> None:
        text = "abracadabra"
        encoded, codes = huffman_coding(text)
        # manually decode using the returned codes to verify correctness
        reverse = {v: k for k, v in codes.items()}
        decoded = ""
        buffer = ""
        for bit in encoded:
            buffer += bit
            if buffer in reverse:
                decoded += reverse[buffer]
                buffer = ""
        assert decoded == text

    def test_codes_are_prefix_free(self) -> None:
        # no code should be a prefix of another — required for unambiguous decoding
        _, codes = huffman_coding("this is an example")
        values = list(codes.values())
        for i, code_a in enumerate(values):
            for code_b in values[i + 1 :]:
                assert not code_a.startswith(code_b)
                assert not code_b.startswith(code_a)