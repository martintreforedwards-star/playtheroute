The Route - Master Data Workflow
Purpose
The Route uses a layered data architecture to ensure stations, networks, routes and game datasets can be maintained independently.

The key principle is:

A station exists once in the project.
A station may appear in multiple network games.
Networks define gameplay coverage.
Routepedia defines railway routes and branches.
Puzzle datasets are generated from the underlying data.
Core Files
master_station.csv
The authoritative list of all stations used within The Route.

Each station should appear only once.

Fields:

station_id
crs
station_name
latitude
longitude
region
primary_network
Example:

uk_000123,DFD,Dartford,51.447,-0.219,North Kent,Southeastern
Rules:

Never duplicate stations.
CRS should be unique.
station_id should never change once assigned.
New stations are added here first.
network_membership.csv
Maps stations to individual network games.

Fields:

station_id
network
route_station_id
crs
station_name
Example:

uk_000123,Southeastern,SE0040,DFD,Dartford
uk_000123,Southern,SO0088,DFD,Dartford
Rules:

A station may have multiple membership records.
route_station_id is unique within a network.
CRS and station_name are retained for auditing.
