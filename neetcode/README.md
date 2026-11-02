# NeetCode 150

Python solutions for the NeetCode 150 playlist, numbered by position in the list. Each `solution.py` holds every approach from the episode, from the worst idea to the best one.

## Arrays & Hashing

| # | Problem | Worst idea | Better idea | Best | Code |
|---|---|---|---|---|---|
| 001 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Every pair, O(n²) | Sort, O(n log n) | Hash set, O(n) | [solution.py](001-contains-duplicate/solution.py) |
| 002 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Every order, O(n!) | Sort both, O(n log n) | Count letters, O(n) | [solution.py](002-valid-anagram/solution.py) |
| 003 | [Two Sum](https://leetcode.com/problems/two-sum/) | Every pair, O(n²) | Two pointers, O(n log n) | Hash map, O(n) | [solution.py](003-two-sum/solution.py) |
| 004 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Every pair, O(n²·k) | Sorted key, O(n·k log k) | Count key, O(n·k) | [solution.py](004-group-anagrams/solution.py) |
