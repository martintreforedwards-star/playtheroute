# The Route - Master Data Workflow

## Purpose

The Route uses a layered data architecture to ensure stations, networks, routes and game datasets can be maintained independently.

The key principle is:

* A station exists once in the project.
* A station may appear in multiple network games.
* Networks define gameplay coverage.
* Routepedia defines railway routes and branches.
* Puzzle datasets are generated from the underlying data.

---

## Core Files

### master_station.csv

The authoritative list of all stations used within The Route.

Each station should appear only once.

Fields:

```text
station_id
crs
station_name
latitude
longitude
region
primary_network
```

Example:

```text
uk_000123,DFD,Dartford,51.447,-0.219,North Kent,Southeastern
```

Rules:

* Never duplicate stations.
* CRS should be unique.
* station_id should never change once assigned.
* New stations are added here first.

---

### network_membership.csv

Maps stations to individual network games.

Fields:

```text
station_id
network
route_station_id
crs
station_name
```

Example:

```text
uk_000123,Southeastern,SE0040,DFD,Dartford
uk_000123,Southern,SO0088,DFD,Dartford
```

Rules:

* A station may have multiple membership records.
* route_station_id is unique within a network.
* CRS and station_name are retained for auditing.

---

### network_scope.md

Defines what is included within a network game.

Each network folder should contain a scope file.

The scope should define:

* Included main lines
* Included branch lines
* Included operators
* Excluded areas
* Dataset reference

Purpose:

* Explains why stations belong in a game.
* Provides the foundation for Routepedia.

---

### routepedia.csv (future)

Defines routes and branches used across the project.

Example:

```text
route_id,network,route_name,route_type
SE_R01,Southeastern,South Eastern Main Line,mainline
SE_R02,Southeastern,Chatham Main Line,mainline
SE_R03,Southeastern,Medway Valley Line,branch
```

Purpose:

* Route-based clues
* Route statistics
* Future Routepedia reference material

---

## New Network Workflow

When creating a new network:

### Step 1

Create or validate the network station dataset.

Example:

```text
se_master_v1.csv
```

### Step 2

Review stations against master_station.csv using CRS.

### Step 3

For existing stations:

* Reuse existing station_id.

### Step 4

For new stations:

* Create a new station_id.
* Add to master_station.csv.

### Step 5

Create network_membership records.

Example:

```text
uk_000123,Southeastern,SE0040,DFD,Dartford
```

### Step 6

Create network_scope.md.

### Step 7

Run audit checks.

---

## Audit Checks

Before committing changes:

### Check 1

Every membership record has:

* station_id
* network
* route_station_id
* CRS
* station_name

### Check 2

Every CRS maps to a single station_id.

### Check 3

No duplicate station_ids exist in master_station.csv.

### Check 4

All network station counts match expected totals.

---

## Route Station ID Standards

Format:

```text
SO0001 Southern
SE0001 Southeastern
GW0001 GWR
GA0001 Greater Anglia
CT0001 c2c
CH0001 Chiltern
WM0001 West Midlands
```

Rules:

* Unique within each network.
* Never renumber existing IDs.
* Retired IDs remain retired.

---

## Long-Term Architecture

```text
master_station.csv
        ↓
network_membership.csv
        ↓
network_scope.md
        ↓
routepedia.csv
        ↓
puzzle generation
```

This structure allows networks to be expanded, audited and maintained without affecting existing games.
