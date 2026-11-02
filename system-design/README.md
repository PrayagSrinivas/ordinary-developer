# System Design

Small Python simulations for the System Design playlist. Each one lets you run the idea from the episode and compare the approaches yourself.

| # | Topic | Worst idea | Better idea | Best | Code |
|---|---|---|---|---|---|
| 001 | Load Balancing | One bigger server | Round robin | Health checks and least connections | [simulation.py](001-load-balancing/simulation.py) |
| 002 | Caching | Query the database every time | A cache on each server | One shared cache with an expiry | [simulation.py](002-caching/simulation.py) |
| 003 | CDN | A faster server | A server in each region | Copies at the edge | [simulation.py](003-cdn/simulation.py) |

The numbers in these simulations are small examples for learning, not real benchmarks.
