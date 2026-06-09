import json

with open("data/stations/southeastern.json") as f:
    stations = json.load(f)

candidates = []

for s in stations:
    if (
        s.get("route_diversity_band") == "many"
        or s.get("route_count", 0) >= 3
    ):
        candidates.append(s)

candidates = sorted(
    candidates,
    key=lambda s: (
        -s.get("route_count", 0),
        s["station_name"]
    )
)

for s in candidates:
    print(
        f'{s["station_name"]}'
        f' | routes={s.get("route_count")}'
        f' | diversity={s.get("route_diversity_band")}'
        f' | terminals={s.get("london_terminal_count")}'
    )

print("\nTotal candidates:", len(candidates))
