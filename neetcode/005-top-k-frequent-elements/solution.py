"""Top K Frequent Elements: from the worst idea to the best one.

Four ways to find the k values that appear most often, in the order the episode covers them.
Run this file to check all four: python3 solution.py
"""
import heapq
import math
from collections import Counter


def scan_each(nums, k):
    """Count each value by scanning the whole list. O(n²) time."""
    counts = {x: nums.count(x) for x in nums}
    return sorted(counts, key=counts.get, reverse=True)[:k]


def sort_counts(nums, k):
    """Count once with a hash map, then sort the values by count. O(n log n) time."""
    counts = Counter(nums)
    return sorted(counts, key=counts.get, reverse=True)[:k]


def heap_of_k(nums, k):
    """Keep only the k biggest counts in a heap. O(n log k) time, and only k extra slots."""
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)


def buckets(nums, k):
    """A count can't be bigger than n, so use it as an index: drawer c holds every value seen c times. O(n) time."""
    counts = Counter(nums)
    drawers = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        drawers[count].append(value)
    top = []
    for count in range(len(nums), 0, -1):    # open the drawers from the top down
        for value in drawers[count]:
            top.append(value)
            if len(top) == k:
                return top
    return top


if __name__ == "__main__":
    cases = [
        ([1, 1, 1, 2, 2, 3], 2, [1, 2]),          # the example from the video
        ([1], 1, [1]),
        ([4, 4, 4, 5, 5, 6, 7, 7, 7, 7], 2, [7, 4]),
        ([-1, -1, 2], 1, [-1]),
        ([3, 0, 1, 0], 1, [0]),
    ]
    approaches = (scan_each, sort_counts, heap_of_k, buckets)
    for solve in approaches:
        for nums, k, expected in cases:
            assert sorted(solve(nums, k)) == sorted(expected), (solve.__name__, nums, k)

    n = 100_000
    assert n * n == 10_000_000_000                     # scanning for every number: ten billion steps
    assert round(n * math.log2(n) / 1e6, 1) == 1.7     # sorting: about 1.7 million steps
    print(f"All {len(cases)} cases pass for all {len(approaches)} approaches.")
