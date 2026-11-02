"""Geohashing: from the worst idea to the best one.

A small simulation of the cancelled order from the episode. A rider holds a hot order, and we want
every customer within 500 metres. It compares checking everyone, an index on latitude, and geohash boxes.
Run this file to see the comparison: python3 simulation.py
"""
import math
import random

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
EARTH_M = 6_371_000


def geohash(lat, lon, precision=6):
    """Cut the map in half again and again, alternating longitude and latitude. Every 5 cuts make one character."""
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    code, bits, value, use_lon = "", 0, 0, True
    while len(code) < precision:
        rng, x = (lon_range, lon) if use_lon else (lat_range, lat)
        mid = (rng[0] + rng[1]) / 2
        value = value * 2 + (x >= mid)
        rng[0 if x >= mid else 1] = mid
        use_lon, bits = not use_lon, bits + 1
        if bits == 5:
            code, bits, value = code + BASE32[value], 0, 0
    return code


def box_size(precision=6):
    """Height and width of one box, in degrees."""
    lon_bits = (precision * 5 + 1) // 2
    return 180 / 2 ** (precision * 5 - lon_bits), 360 / 2 ** lon_bits


def nine_boxes(lat, lon, precision=6):
    """The rider's box and the eight around it."""
    h, w = box_size(precision)
    return {geohash(lat + dy * h, lon + dx * w, precision) for dy in (-1, 0, 1) for dx in (-1, 0, 1)}


def metres(a, b):
    (lat1, lon1), (lat2, lon2) = [(math.radians(x), math.radians(y)) for x, y in (a, b)]
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * EARTH_M * math.asin(math.sqrt(h))


if __name__ == "__main__":
    random.seed(4)
    # A million customers spread over a city about 28 km across, and a rider in the middle.
    customers = [(random.uniform(12.85, 13.10), random.uniform(77.45, 77.70)) for _ in range(1_000_000)]
    rider, radius = (12.9716, 77.5946), 500

    near = [c for c in customers if metres(rider, c) <= radius]              # worst: measure everyone
    lat_m = radius / 111_320
    strip = [c for c in customers if abs(c[0] - rider[0]) <= lat_m]          # better: one index on latitude
    boxes = nine_boxes(*rider)
    by_box = {}
    for c in customers:                                                     # built once, like an index
        by_box.setdefault(geohash(*c), []).append(c)
    candidates = [c for b in boxes for c in by_box.get(b, [])]               # best: nine prefix lookups
    found = [c for c in candidates if metres(rider, c) <= radius]
    own_box = [c for c in by_box[geohash(*rider)] if metres(rider, c) <= radius]

    h, w = box_size()
    print(f"Box size at precision 6: {h * 111_320:.0f} m by {w * 111_320 * math.cos(math.radians(rider[0])):.0f} m")
    print(f"Measure everyone:     {len(customers):,} checks, {len(near):,} nearby")
    print(f"Index on latitude:    {len(strip):,} people in a strip across the city")
    print(f"Nine geohash boxes:   {len(candidates):,} people, then {len(found):,} nearby")
    print(f"Rider's box only:     misses {len(near) - len(own_box):,} nearby customers")

    assert sorted(found) == sorted(near)              # nine boxes find everyone within 500 m
    assert len(own_box) < len(near)                   # one box alone misses people across the edge
    assert len(candidates) < len(strip) < len(customers)
    assert geohash(*rider)[:5] == geohash(rider[0] + 0.001, rider[1] + 0.001)[:5]   # nearby places share a prefix
    print("All checks pass.")
