"""Contains Duplicate: from the worst idea to the best one.

Three ways to answer "is anything repeated?", in the order the episode covers them.
Run this file to check all three: python3 solution.py
"""


def every_pair(nums):
    """Compare each number with everything after it. O(n²) time, O(1) space."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


def sort_first(nums):
    """Sort so equal numbers sit side by side. O(n log n) time."""
    ordered = sorted(nums)
    for a, b in zip(ordered, ordered[1:]):
        if a == b:
            return True
    return False


def hash_set(nums):
    """Ask "have I seen this before?" for each number. O(n) time, O(n) space."""
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


if __name__ == "__main__":
    cases = [
        ([4, 9, 1, 7, 9, 3], True),   # the example from the video
        ([1, 2, 3, 4], False),
        ([], False),
        ([5], False),
        ([2, 2], True),
        ([-1, 0, 1, -1], True),
    ]
    for solve in (every_pair, sort_first, hash_set):
        for nums, expected in cases:
            assert solve(nums) == expected, (solve.__name__, nums)
    print(f"All {len(cases)} cases pass for all 3 approaches.")
