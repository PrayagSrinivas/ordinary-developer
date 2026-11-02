"""CDN: from the worst idea to the best one.

A small simulation of one page load from the episode. A warehouse in New York is the origin
server, and a konbini on the corner is an edge server. It compares where the answer comes from.
Run this file to see the comparison: python3 simulation.py
"""

TRIPS = 7          # connecting, then the page, styles, scripts and images, there and back
SERVER_MS = 5      # the server's work on each trip

# How long the network takes for one trip there and back, in milliseconds.
NETWORK_MS = {"New York": 5, "Tokyo": 155}
EDGE_TOTAL_MS = 5  # network and work together, from a shop on the corner


def page_ms(city, server_ms=SERVER_MS):
    """Load one page from the server in New York."""
    return TRIPS * (NETWORK_MS[city] + server_ms)


def first_visit_ms(files_in_shop, files):
    """Files the shop lacks are fetched from New York once. After that, it keeps a copy."""
    misses = files - files_in_shop
    return files_in_shop * EDGE_TOTAL_MS + misses * (EDGE_TOTAL_MS + page_ms("Tokyo") / TRIPS)


if __name__ == "__main__":
    new_york, tokyo = page_ms("New York"), page_ms("Tokyo")
    faster_new_york = page_ms("New York", SERVER_MS / 2)
    faster_tokyo = page_ms("Tokyo", SERVER_MS / 2)
    edge = TRIPS * EDGE_TOTAL_MS

    print(f"New York: {new_york} ms    Tokyo: {tokyo} ms")
    print(f"Faster server: New York {1 - faster_new_york / new_york:.0%} better, Tokyo {1 - faster_tokyo / tokyo:.1%} better")
    print(f"From the corner shop: {edge} ms")

    assert new_york == 70
    assert tokyo == 1120                                # over a second
    assert 1 - faster_new_york / new_york == 0.25       # a quarter faster
    assert 1 - faster_tokyo / tokyo < 0.02              # less than two percent
    assert edge == 35
    assert first_visit_ms(0, 1) == 165                  # the first person pays for the trip
    assert first_visit_ms(1, 1) == 5                    # the next person doesn't
    print("All checks pass.")
