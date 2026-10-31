"""Load Balancing: from the worst idea to the best one.

A small simulation of the ramen shop from the episode. Servers are chefs and requests are
customers. It compares round robin with least connections and health checks.
Run this file to see the comparison: python3 simulation.py
"""
from itertools import cycle


def simulate(pick_server, requests, servers=5, down=frozenset()):
    """Send each request to a server and count what happens.

    requests is a list of how many ticks each request takes, arriving one per tick.
    A request sent to a server that is down fails. Returns the failed requests and
    the most open orders any one server ever held.
    """
    busy = [[] for _ in range(servers)]    # finish tick of each open request, per server
    failed = peak = 0
    for tick, duration in enumerate(requests):
        busy = [[end for end in orders if end > tick] for orders in busy]
        chosen = pick_server(busy, down)
        if chosen in down:
            failed += 1
            continue
        busy[chosen].append(tick + duration)
        peak = max(peak, len(busy[chosen]))
    return failed, peak


def round_robin(servers=5):
    """Take turns, whether or not the server can take the request."""
    order = cycle(range(servers))
    return lambda busy, down: next(order)


def least_connections(busy, down):
    """Health check first, then pick the server with the fewest open orders."""
    healthy = [i for i in range(len(busy)) if i not in down]
    return min(healthy, key=lambda i: len(busy[i]))


if __name__ == "__main__":
    # Every fifth request is slow, and server 2 (chef 3) is gone.
    requests = [1, 12, 1, 1, 1] * 40
    down = frozenset({2})

    rr_failed, rr_peak = simulate(round_robin(), requests, down=down)
    lc_failed, lc_peak = simulate(least_connections, requests, down=down)

    print(f"{len(requests)} requests, 5 servers, 1 down")
    print(f"Round robin:       {rr_failed} failed, busiest server held {rr_peak} orders")
    print(f"Least connections: {lc_failed} failed, busiest server held {lc_peak} orders")

    assert rr_failed == len(requests) // 5    # every fifth request hits the dead server
    assert lc_failed == 0                     # the health check skips it
    assert lc_peak < rr_peak                  # slow requests get spread out
    print("All checks pass.")
