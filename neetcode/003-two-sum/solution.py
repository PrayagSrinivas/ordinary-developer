"""Two Sum: from the worst idea to the best one.

Three ways to find the two indices, in the order the episode covers them.
Run this file to check all three: python3 solution.py
"""


def every_pair(nums, target):
    """Try every pair. O(n²) time, O(1) space."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def two_pointers(nums, target):
    """Sort, but carry the original indices along. O(n log n) time, O(n) space."""
    ordered = sorted(enumerate(nums), key=lambda pair: pair[1])
    left, right = 0, len(ordered) - 1
    while left < right:
        total = ordered[left][1] + ordered[right][1]
        if total == target:
            return sorted([ordered[left][0], ordered[right][0]])
        if total < target:
            left += 1
        else:
            right -= 1
    return []


def hash_map(nums, target):
    """Ask "what number do I need?" at each step. O(n) time, O(n) space."""
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []


if __name__ == "__main__":
    cases = [
        ([5, 11, 2, 9, 7], 9, [2, 4]),   # the example from the video
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 3], 6, [0, 1]),
        ([-3, 4, 3, 90], 0, [0, 2]),
    ]
    for solve in (every_pair, two_pointers, hash_map):
        for nums, target, expected in cases:
            assert solve(nums, target) == expected, (solve.__name__, nums, target)
    print(f"All {len(cases)} cases pass for all 3 approaches.")
