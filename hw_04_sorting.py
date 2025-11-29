import random
import timeit
import statistics
from typing import List, Callable
from heapq import heappush, heappop


def insertion_sort(arr: List[int]) -> List[int]:
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    if i < len(left):
        result.extend(left[i:])
    if j < len(right):
        result.extend(right[j:])
    return result


def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def timsort(arr: List[int]) -> List[int]:
    return sorted(arr)


def generate_random_list(size: int, seed: int = 0) -> List[int]:
    rnd = random.Random(seed)
    return [rnd.randint(-10_000_000, 10_000_000) for _ in range(size)]


def generate_nearly_sorted_list(
    size: int,
    seed: int = 0,
    perturb_fraction: float = 0.01,
) -> List[int]:
    arr = list(range(size))
    rnd = random.Random(seed)
    swaps = max(1, int(size * perturb_fraction))
    for _ in range(swaps):
        i = rnd.randrange(size)
        j = rnd.randrange(size)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_reverse_sorted_list(size: int) -> List[int]:
    return list(range(size, 0, -1))


def benchmark(
    algorithm: Callable[[List[int]], List[int]],
    data: List[int],
    repeats: int = 3,
) -> float:
    timer = timeit.Timer(lambda: algorithm(data))
    results = timer.repeat(repeat=repeats, number=1)
    return statistics.mean(results)


def merge_k_lists(lists: List[List[int]]) -> List[int]:
    heap = []
    result = []
    for list_index, lst in enumerate(lists):
        if lst:
            heappush(heap, (lst[0], list_index, 0))
    while heap:
        value, list_index, element_index = heappop(heap)
        result.append(value)
        next_index = element_index + 1
        if next_index < len(lists[list_index]):
            heappush(
                heap,
                (lists[list_index][next_index], list_index, next_index),
            )
    return result


def run_benchmark() -> None:
    sizes = [1000, 5000, 10000]
    generators = {
        "random": generate_random_list,
        "nearly_sorted": generate_nearly_sorted_list,
        "reverse_sorted": generate_reverse_sorted_list,
    }
    algorithms = {
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "timsort": timsort,
    }

    print("Порівняння алгоритмів сортування (час у секундах)")
    print("-" * 70)
    print(f"{'size':>7} | {'type':>14} | {'algorithm':>14} | {'time, s':>10}")
    print("-" * 70)

    for size in sizes:
        for gen_name, gen in generators.items():
            base_data = gen(size)
            for algo_name, algo in algorithms.items():
                elapsed = benchmark(algo, base_data, repeats=3)
                print(
                    f"{size:7d} | {gen_name:14} | "
                    f"{algo_name:14} | {elapsed:10.6f}"
                )
    print("-" * 70)


def run_tests() -> None:
    test_data = [
        [],
        [1],
        [3, 2, 1],
        [5, 1, 3, 2, 4],
        [10, -1, 7, 7, 0],
    ]

    for data in test_data:
        expected = sorted(data)
        assert insertion_sort(data) == expected
        assert merge_sort(data) == expected
        assert timsort(data) == expected

    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    expected_merged = [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_lists(lists) == expected_merged

    print("Усі тести пройдені успішно.")


if __name__ == "__main__":
    run_benchmark()
    run_tests()