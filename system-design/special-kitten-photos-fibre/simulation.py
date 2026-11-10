"""How two kitten photos cross the world through optical fibre: from the worst idea to the best one.

Grandma in Mumbai sends two kitten photos to you in London. This is a teaching model with rounded, typical numbers,
not the spec of any one real cable. It checks every number the video says.
Run it: python3 simulation.py
"""
import math

# The photos
PHOTOS, PHOTO_BYTES = 2, 2_000_000            # two photos, about 2 MB each
PACKET_PAYLOAD = 1_460                         # bytes of photo in one 1,500-byte internet packet
BITS = PHOTOS * PHOTO_BYTES * 8

# The route, rounded: Mumbai -> Arabian Sea -> Red Sea -> Mediterranean -> France under the sea, then overland to London
ROUTE_KM, SEA_KM = 10_000, 8_000

# Worst idea: electricity in copper. The 1858 Atlantic telegraph cable sent Queen Victoria's 98-word message in about 16 hours.
TELEGRAPH_WORDS, TELEGRAPH_HOURS = 98, 16
BITS_PER_WORD = 6 * 8                          # five letters and a space, 8 bits a character, a rough modern equivalent

# Better idea: light through the air needs a straight line, and the Earth curves away.
EARTH_RADIUS_M, TOWER_M = 6_371_000, 100

# Best idea: light trapped in glass.
C_KM_S = 299_792
N_CORE, N_CLADDING = 1.468, 1.463              # the core is very slightly denser glass than the cladding around it
LOSS_DB_PER_KM = 0.2                           # typical single-mode fibre at 1550 nm
LASER_BITS_PER_S = 10e9                        # one colour blinking 10 billion times a second (simple on/off model)


def worst():
    rate = TELEGRAPH_WORDS * BITS_PER_WORD / (TELEGRAPH_HOURS * 3600)        # bits a second
    years = BITS / rate / (365.25 * 24 * 3600)
    return rate, years


def better():
    return math.sqrt(2 * EARTH_RADIUS_M * TOWER_M) / 1000                     # km before the curve hides the receiver


def best():
    critical = math.degrees(math.asin(N_CLADDING / N_CORE))                  # hit the wall flatter than this and it bounces back
    speed = C_KM_S / N_CORE
    trip_ms = ROUTE_KM / speed * 1000
    blink_out_ms = BITS / LASER_BITS_PER_S * 1000
    return critical, speed, trip_ms, blink_out_ms


def catch(spacing_km=100):
    left = 10 ** (-LOSS_DB_PER_KM * spacing_km / 10)                          # share of light left after one span
    no_boost = -LOSS_DB_PER_KM * SEA_KM / 10                                  # power of ten left after the whole sea, unboosted
    boosters = SEA_KM // spacing_km
    return left, no_boost, boosters


if __name__ == "__main__":
    packets = PHOTOS * math.ceil(PHOTO_BYTES / PACKET_PAYLOAD)
    print(f"photos : {BITS:,} bits, sent as {packets:,} packets")

    rate, years = worst()
    print(f"worst  : copper telegraph, about {rate:.2f} bits a second, so the two photos take about {years:.0f} years")

    km = better()
    print(f"better : light through air, from a {TOWER_M} m tower the Earth curves out of sight after about {km:.0f} km")

    critical, speed, trip_ms, blink_ms = best()
    print(f"best   : light glancing off the core wall at under {90 - critical:.1f} degrees bounces back in (critical angle {critical:.1f})")
    print(f"         light in glass: about {speed:,.0f} km/s, so {ROUTE_KM:,} km takes about {trip_ms:.0f} ms (a blink is roughly 100 to 150 ms)")
    print(f"         the laser blinks the photos out in about {blink_ms:.1f} ms")

    left, no_boost, boosters = catch()
    print(f"catch  : after 100 km only {left:.0%} of the light is left; across {SEA_KM:,} km unboosted, 1 part in 10^{-no_boost:.0f}")
    print(f"         so about {boosters} boosters sit on the seabed, one every 100 km")

    assert BITS == 32_000_000 and packets == 2_740
    assert round(years) == 12 and round(km) == 36
    assert 85 < critical < 86 and 200_000 < speed < 206_000 and round(trip_ms) == 49
    assert round(left, 2) == .01 and boosters == 80
