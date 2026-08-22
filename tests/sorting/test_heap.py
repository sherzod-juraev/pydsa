from pydsa import heap_sort


class TestHeapSort:
    def test_empty_list(self) -> None:
        assert heap_sort([]) == []

    def test_single_element(self) -> None:
        assert heap_sort([42]) == [42]

    def test_already_sorted(self) -> None:
        assert heap_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self) -> None:
        assert heap_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_unsorted(self) -> None:
        assert heap_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]

    def test_all_equal_elements(self) -> None:
        assert heap_sort([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_with_duplicates(self) -> None:
        assert heap_sort([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]

    def test_strings(self) -> None:
        assert heap_sort(["zebra", "apple", "mango", "banana"]) == [
            "apple",
            "banana",
            "mango",
            "zebra",
        ]

    def test_negative_numbers(self) -> None:
        assert heap_sort([-3, 5, -1, 0, 2]) == [-3, -1, 0, 2, 5]

    def test_two_elements(self) -> None:
        assert heap_sort([2, 1]) == [1, 2]

    def test_does_not_mutate_input(self) -> None:
        original = [3, 1, 2]
        heap_sort(original)
        assert original == [3, 1, 2]

    def test_large_input(self) -> None:
        arr = [(i * 37) % 101 for i in range(200)]
        assert heap_sort(arr) == sorted(arr)