"""Valid Anagram: from the worst idea to the best one.

Three ways to prove two strings are anagrams, in the order the episode covers them.
Run this file to check all three: python3 solution.py
"""
from itertools import permutations


def every_order(s, t):
    """Try every rearrangement of s. O(n!) time, so only safe on tiny inputs."""
    if len(s) != len(t):
        return False
    return any("".join(order) == t for order in permutations(s))


def sort_both(s, t):
    """Sorting makes anagrams identical. O(n log n) time."""
    return sorted(s) == sorted(t)


def count_letters(s, t):
    """Lowercase English only: 26 rods, up for s and down for t. O(n) time, O(1) space."""
    if len(s) != len(t):
        return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[ord(a) - 97] += 1
        count[ord(b) - 97] -= 1
    return not any(count)


def count_any_character(s, t):
    """Unicode follow-up: a hash map instead of a fixed array. O(n) time, O(k) space."""
    if len(s) != len(t):
        return False
    count = {}
    for a, b in zip(s, t):
        count[a] = count.get(a, 0) + 1
        count[b] = count.get(b, 0) - 1
    return not any(count.values())


if __name__ == "__main__":
    cases = [
        ("listen", "silent", True),   # the example from the video
        ("rat", "car", False),        # the counter-example from the video
        ("", "", True),
        ("a", "ab", False),
        ("aab", "abb", False),
        ("anagram", "nagaram", True),
    ]
    approaches = (every_order, sort_both, count_letters, count_any_character)
    for solve in approaches:
        for s, t, expected in cases:
            assert solve(s, t) == expected, (solve.__name__, s, t)
    assert count_any_character("héllo", "lléoh")
    print(f"All {len(cases)} cases pass for all {len(approaches)} approaches.")
