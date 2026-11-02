"""Group Anagrams: from the worst idea to the best one.

Three ways to group words that are anagrams of each other, in the order the episode covers them.
Run this file to check all three: python3 solution.py
"""
from collections import defaultdict


def is_anagram(s, t):
    """The check from Valid Anagram: count up for s, down for t."""
    if len(s) != len(t):
        return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[ord(a) - 97] += 1
        count[ord(b) - 97] -= 1
    return not any(count)


def every_pair(words):
    """Compare each word with every word after it. Up to n(n-1)/2 checks, so O(n² · k) time."""
    groups, placed = [], [False] * len(words)
    for i, word in enumerate(words):
        if placed[i]:
            continue
        group = [word]
        for j in range(i + 1, len(words)):
            if not placed[j] and is_anagram(word, words[j]):
                group.append(words[j])
                placed[j] = True
        groups.append(group)
    return groups


def sorted_key(words):
    """Anagrams sort to the same letters, so use the sorted word as the key. O(n · k log k) time."""
    groups = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


def count_key(words):
    """Anagrams have the same letter counts, so use the 26 counts as the key. O(n · k) time."""
    groups = defaultdict(list)
    for word in words:
        count = [0] * 26
        for letter in word:
            count[ord(letter) - 97] += 1
        groups[tuple(count)].append(word)    # a list can't be a dict key, a tuple can
    return list(groups.values())


def same_groups(a, b):
    return sorted(sorted(g) for g in a) == sorted(sorted(g) for g in b)


if __name__ == "__main__":
    cases = [
        (["eat", "tea", "tan", "ate", "nat", "bat"], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),   # the example from the video
        ([""], [[""]]),
        (["a"], [["a"]]),
        (["ab", "ba", "abc", "cab", "bca", "x"], [["ab", "ba"], ["abc", "bca", "cab"], ["x"]]),
        (["aab", "abb"], [["aab"], ["abb"]]),
    ]
    approaches = (every_pair, sorted_key, count_key)
    for solve in approaches:
        for words, expected in cases:
            assert same_groups(solve(words), expected), (solve.__name__, words)

    n = 10_000
    assert n * (n - 1) // 2 == 49_995_000     # every pair of 10,000 words: about fifty million
    print(f"All {len(cases)} cases pass for all {len(approaches)} approaches.")
