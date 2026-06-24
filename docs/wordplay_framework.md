# Wordplay Framework

## Purpose

This document defines the standard wordplay clue families used across The Route network datasets.

The aim is to identify recurring patterns within UK station names that:

* Appear frequently enough to create meaningful gameplay.
* Work consistently across multiple rail networks.
* Can be discovered intuitively by players.
* Support future network expansion without requiring bespoke clue systems.

Wordplay clues use **substring matching**.

For example:

* Contains "ham" matches **City Thameslink**, **Streatham**, and **West Ham**.
* Contains "ton" matches **Tonbridge**, **Southampton**, and **Clapham Junction**.
* Contains "west" matches **West Croydon** and **Wandsworth Common**.

Word boundaries are not required.

---

# Approved Clue Families

## Direction

Directional words found within station names.

### Approved Terms

* north
* south
* east
* west

### Notes

These occur consistently across UK networks and provide strong gameplay value.

---

## Settlement

Historic settlement suffixes and place-name elements.

### Approved Terms

* ham
* ton
* bridge
* field
* bury
* wick
* gate
* worth

### Notes

This is the strongest national wordplay category and should be prioritised when available.

---

## Nature

Landscape and environmental features.

### Approved Terms

* park
* hill
* wood
* green
* heath

### Notes

Useful across many networks, although prevalence varies regionally.

---

## Water

Maritime and waterside references.

### Approved Terms

* port
* sea

### Notes

Particularly useful for coastal networks.

---

## Religious

Ecclesiastical and historic church references.

### Approved Terms

* st
* church
* minster

### Notes

"st" is the most common religious clue nationally.

---

## Transport

Railway and transport terminology.

### Approved Terms

* road
* central
* parkway
* junction

### Notes

Strong clue family that players generally understand immediately.

---

## Civic

Administrative and civic terminology.

### Approved Terms

* town

### Notes

Limited but still useful where present.

---

# Deferred Terms

The following terms are recognised but currently occur too infrequently to justify routine gameplay use:

* upper
* lower
* forest
* harbour
* quay
* square
* market

These may be promoted in future if network-specific analysis demonstrates sufficient coverage.

---

# National Analysis Baseline

Analysis of 2,605 UK stations identified the following strongest wordplay terms:

| Term   | Matches |
| ------ | ------: |
| st     |     440 |
| ton    |     374 |
| ham    |     177 |
| park   |      88 |
| bridge |      66 |
| hill   |      69 |
| road   |      58 |
| west   |      58 |
| field  |      55 |
| wood   |      51 |

These terms form the core wordplay vocabulary for The Route.

---

# Network Implementation

Individual networks should only include clues that generate a useful number of valid stations.

Recommended range:

* Minimum: 5 stations
* Ideal: 5–30 stations
* Maximum: 40 stations

Clues outside these ranges should normally be excluded unless they serve a specific gameplay purpose.

Examples:

### Southern

Approved:

* Contains ham
* Contains ton
* Contains west
* Contains hill

Rejected:

* Contains green (2 stations)

---

This framework should be reviewed whenever a new network is added or the national station dataset is significantly updated.
