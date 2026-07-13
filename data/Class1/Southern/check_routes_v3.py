from routes_v3 import southern_route_templates

stations = set()

for route in southern_route_templates:
    for station in route:
        stations.add(station)

print("Routes:", len(southern_route_templates))
print("Stations:", len(stations))

print("\nNewest stations:")

for s in sorted(stations):
    if s in [
        "Uckfield",
        "Buxted",
        "Crowborough",
        "Eridge",
        "East Grinstead",
        "Dormans",
        "Lingfield",
        "Wallington",
        "West Sutton",
        "Dorking",
        "Warnham",
        "Ockley",
        "Holmwood"
    ]:
        print(s)