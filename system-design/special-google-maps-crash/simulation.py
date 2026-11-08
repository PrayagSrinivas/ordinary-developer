"""How a map spots a crash nobody has reported: from the worst idea to the best one.

A small, made-up highway at 6 pm. Twelve stretches, each a kilometre long. Stretches 3 to 6 are a bottleneck that is
slow every evening. Just after 18:05 a car crashes on stretch 9. Every phone in a car sends its speed once a minute.
This is a teaching model, not Google's real system: it compares three ways to notice the crash, then shows the
99-phones-in-a-handcart trick and one way to resist it.
Run this file to see the comparison: python3 simulation.py
"""
import random
import statistics

random.seed(6)
STRETCHES = range(1, 13)
CRASH_STRETCH, CRASH_MINUTE = 9, 5             # the crash happens just after 18:05, so 18:05's readings miss it
SLOW_KMH = 40                                  # the "better" idea: any road under 40 km/h counts as trouble
DROP = .5                                      # the best idea: under half of what this stretch usually does now
MIN_VEHICLES = 10                              # never trust a handful of phones
CONFIRM = 2                                    # the drop has to hold for two minutes in a row


def normal_speed(stretch):
    """What this stretch usually does on a weekday at 6 pm, learned from months of history."""
    return 30 if 3 <= stretch <= 6 else 85


def true_speed(stretch, minute):
    """What traffic really does today. The bottleneck is slow as usual; the crash stops stretch 9 and backs up 8."""
    v = normal_speed(stretch)
    if minute > CRASH_MINUTE:
        if stretch == CRASH_STRETCH:
            v = 6
        elif stretch == CRASH_STRETCH - 1 and minute > CRASH_MINUTE + 3:
            v = 25                             # the queue reaches the stretch behind it a few minutes later
        elif stretch == CRASH_STRETCH + 1:
            v = 95                             # past the crash the road empties out
    return v


def pings(stretch, minute):
    """One speed reading per phone: about 30 cars, plus two people walking on the pavement."""
    cars = [max(0, random.gauss(true_speed(stretch, minute), 6)) for _ in range(30)]
    return cars + [random.gauss(5, 1) for _ in range(2)]


def live(minute):
    return {s: statistics.median(pings(s, minute)) for s in STRETCHES}


def worst():
    """Wait for someone to report it. No reports, no warning."""
    return "nothing until someone stops to report it"


def better(speeds):
    """Flag every slow road."""
    return [s for s, v in speeds.items() if v < SLOW_KMH]


def best(history):
    """Flag a stretch only when it falls under half of its own normal, for two minutes in a row."""
    flagged = []
    for s in STRETCHES:
        recent = [h[s] for h in history[-CONFIRM:]]
        if len(recent) == CONFIRM and all(v < DROP * normal_speed(s) for v in recent):
            flagged.append(s)
    return flagged


def vehicles(phones):
    """Count vehicles, not phones: phones that sit within 5 m of each other and move together are one vehicle."""
    groups = []
    for p in phones:
        for g in groups:
            if abs(g[0] - p) < 5:
                break
        else:
            groups.append([p])
    return len(groups)


if __name__ == "__main__":
    history, spotted = [], None
    for minute in range(0, 12):
        speeds = live(minute)
        history.append(speeds)
        if spotted is None and CRASH_STRETCH in best(history):
            spotted = minute
        if minute == CRASH_MINUTE + 1:
            slow = better(speeds)
    print("worst  :", worst())
    print(f"better : {len(slow)} slow stretches at 18:0{CRASH_MINUTE + 1} {slow}, but only one is a crash")
    print(f"best   : flags {best(history[:spotted + 1])} at 18:{spotted:02d}, {spotted - CRASH_MINUTE} minutes after the crash")
    later = best(history)
    print(f"         by 18:{len(history) - 1}: {later} (the queue has reached the stretch behind)")
    assert slow == [3, 4, 5, 6, 9] and best(history[:spotted + 1]) == [9] and spotted - CRASH_MINUTE == 2

    # The handcart: 99 phones walked down an empty side street at 4 km/h, beside two real cars doing 30.
    cart = [random.gauss(0, 1.5) for _ in range(99)]        # positions along the street, in metres, all in one cart
    cars = [140, 410]
    phone_speeds = [4] * 99 + [30, 30]
    print(f"\nhandcart: {len(phone_speeds)} phones, median speed {statistics.median(phone_speeds)} km/h, so a phone count says jam")
    n = vehicles(cart + cars)
    print(f"          counted as vehicles: {n}, under {MIN_VEHICLES}, so no jam")
    assert n == 3
