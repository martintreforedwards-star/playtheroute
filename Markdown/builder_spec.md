# The Route Builder Specification v1.0

## Objective

Produce every data file required by play.html from a single command.

```
python builder/build_network.py <network>
```

---

## Inputs

### Global

- crs_source_of_truth.csv

### Network

- config.json
- master.csv
- route_group_membership.csv
- missing_times.csv (optional)
- landmarks.csv (optional)
- station_facts.csv (optional)

---

## Outputs

Required by play.html

- operator.json
- operator-clues.json
- landmark-challenges.json
- station-facts.json

---

## Builder Stages

1. Load configuration
2. Build enriched dataset
3. Build wordplay
4. Build clue library
5. Export JSON
6. Validate outputs

---

## Phase 1

Use the existing master.csv.

Do NOT introduce automatic CRS extraction yet.

---

## Phase 2

Replace master.csv generation with:

CRS Source of Truth
+
network membership

without changing later stages.

---

## Rule

No operator-specific Python.

Only configuration and data change between operators.