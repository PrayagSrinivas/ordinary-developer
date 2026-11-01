"""Caching: from the worst idea to the best one.

A small simulation of the bento shop from the episode. The kitchen is the database and the
shelf is the cache. It compares no cache, a cache on each server and one shared cache.
Run this file to see the comparison: python3 simulation.py
"""
from collections import OrderedDict

DATABASE_MS = 100
CACHE_MS = 1


class Shelf:
    """A cache where entries expire after ttl seconds, and the oldest used entry goes when full."""

    def __init__(self, ttl=60, size=1000):
        self.ttl, self.size = ttl, size
        self.boxes = OrderedDict()    # key -> (value, the second it expires)

    def get(self, key, now):
        if key not in self.boxes or self.boxes[key][1] <= now:
            self.boxes.pop(key, None)
            return None
        self.boxes.move_to_end(key)
        return self.boxes[key][0]

    def put(self, key, value, now):
        self.boxes[key] = (value, now + self.ttl)
        self.boxes.move_to_end(key)
        if len(self.boxes) > self.size:
            self.boxes.popitem(last=False)    # least recently used


def average_ms(shelf, seconds=600, per_second=1000):
    """Nine in ten requests ask for the home page, and the tenth asks for a page of its own."""
    total_ms = hits = requests = 0
    for second in range(seconds):
        for i in range(per_second):
            key = f"page-{requests}" if i % 10 == 9 else "home"
            requests += 1
            if shelf is None:
                total_ms += DATABASE_MS
            elif shelf.get(key, second) is not None:
                total_ms += CACHE_MS
                hits += 1
            else:
                total_ms += CACHE_MS + DATABASE_MS
                shelf.put(key, "the page", second)
    return total_ms / requests, hits / requests


def answers_after_price_change(shelves):
    """Server 0 changes the price. Then every server is asked for it."""
    for shelf in shelves:
        shelf.put("price", 5, 0)
    shelves[0].put("price", 6, 1)
    return {shelf.get("price", 2) for shelf in shelves}


if __name__ == "__main__":
    no_cache, _ = average_ms(None)
    with_cache, hit_rate = average_ms(Shelf())

    print(f"No cache:     {no_cache:.0f} ms on average")
    print(f"Shared cache: {with_cache:.0f} ms on average, {hit_rate:.0%} served from the cache")

    per_server = answers_after_price_change([Shelf(), Shelf()])
    shared = Shelf()
    one_shelf = answers_after_price_change([shared, shared])
    print(f"A cache on each server gives {len(per_server)} answers, one shared cache gives {len(one_shelf)}")

    small = Shelf(size=2)
    small.put("a", 1, 0)
    small.put("b", 2, 0)
    small.get("a", 0)
    small.put("c", 3, 0)    # the shelf is full, and b has waited longest
    expiring = Shelf(ttl=60)
    expiring.put("box", 1, 0)

    assert no_cache == 100
    assert round(with_cache) == 11                 # 0.9 * 1 + 0.1 * 101
    assert round(hit_rate, 2) == 0.90
    assert per_server == {5, 6} and one_shelf == {6}
    assert small.get("b", 0) is None and small.get("a", 0) == 1
    assert expiring.get("box", 59) == 1 and expiring.get("box", 60) is None
    print("All checks pass.")
