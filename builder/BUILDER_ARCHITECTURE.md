# The Route Builder V5 Architecture

## Purpose

The Builder converts raw railway timetable data into a canonical representation of the railway network suitable for:

- The Route gameplay
- Network analysis
- Quality Assurance
- Visualisation
- Future data products

The Builder is designed to be **generic** and should work for any UK railway network without network-specific logic.

---

# Core Design Principles

## 1. One Responsibility Per Stage

Each Builder stage answers exactly one question.

| Stage | Question |
|--------|----------|
| Service Builder | What services exist? |
| Graph Builder | Which service patterns belong together? |
| Route Metrics | What does each route look like? |
| Route Relationships | How do routes relate to one another? |
| Route Families | Which routes belong together? |
| Route Classification | What would passengers call each route? |
| Gameplay Builder | How should the game use this information? |

No stage should duplicate the responsibility of another.

---

## 2. Canonical Outputs

Each stage produces one canonical output.

Later stages may read previous outputs but should never modify them.

```
Darwin Timetable
        │
        ▼
service_patterns.csv
        │
        ▼
pattern_routes.csv
route_tree.csv
        │
        ▼
routes.csv
        │
        ▼
route_relationships.csv
        │
        ▼
route_families.csv
        │
        ▼
routes_classified.csv
        │
        ▼
Gameplay Assets
```

---

# Builder Stages

---

# Stage 1 – Service Builder

## Purpose

Convert raw Darwin timetable data into unique service patterns.

## Input

Darwin timetable

## Output

```
service_patterns.csv
```

Each record represents one unique stopping pattern.

---

# Stage 2 – Graph Builder

## Purpose

Group related service patterns into operational routes.

## Inputs

```
service_patterns.csv
```

## Outputs

```
pattern_routes.csv
route_tree.csv
```

### pattern_routes.csv

Maps every service pattern to a route.

### route_tree.csv

Describes how patterns diverge within a route.

This is **not** a hierarchy of routes.

---

# Stage 3 – Route Metrics

## Purpose

Create one canonical record per route.

## Inputs

```
pattern_routes.csv
route_tree.csv
stations.csv
```

## Output

```
routes.csv
```

Typical fields include:

- route_id
- primary_origin
- operational_origin
- primary_destination
- operational_destination
- service_count
- pattern_count
- branch_count
- unique_station_count
- longest_pattern
- average_pattern_length
- is_public_route

This becomes the canonical route catalogue.

---

# Stage 4 – Route Relationships

## Purpose

Discover structural relationships between routes.

## Input

```
routes.csv
pattern_routes.csv
service_patterns.csv
```

## Output

```
route_relationships.csv
```

Each record represents one relationship.

Example schema

| Field |
|-------|
| relationship_id |
| route_a |
| route_b |
| relationship |
| confidence |
| shared_station_count |
| shared_prefix_length |
| shared_suffix_length |
| divergence_station |
| merge_station |
| evidence |

---

## Relationship Types

### Structural

- Parent
- Child
- Branch
- Merge
- Parallel
- Continuation
- Intersect
- Independent

These relationships are permanent properties of the network.

### Operational

Examples include:

- Express
- Stopping
- Shuttle
- Circular
- Split / Join

These depend upon the timetable.

### Semantic

Examples include:

- Main Line
- Branch Line
- Metro
- Airport
- Coastal

These should be derived from structural relationships rather than directly calculated.

---

# Stage 5 – Route Families

## Purpose

Group related routes into passenger-facing families.

## Input

```
route_relationships.csv
```

## Output

```
route_families.csv
```

Examples

```
Great Western

    Paddington → Oxford

    Paddington → Banbury

    Slough → Windsor

    Twyford → Henley
```

Families should be derived from route relationships rather than hard-coded.

---

# Stage 6 – Route Classification

## Purpose

Assign passenger-friendly classifications.

## Input

```
routes.csv
route_families.csv
```

## Output

```
routes_classified.csv
```

Possible classifications include:

- Main Line
- Branch Line
- Metro
- Shuttle
- Circular
- Operational

These classifications should be derived from network structure wherever possible.

---

# Stage 7 – Gameplay Builder

## Purpose

Generate assets required by The Route.

Outputs may include:

```
station_facts.json

wordplay.json

difficulty.json

challenge_sets.json

network_statistics.json
```

Gameplay data should never influence Builder outputs.

The Builder is authoritative.

---

# Quality Assurance

QA should validate every canonical output independently.

Examples include:

```
Service QA

Pattern QA

Route QA

Relationship QA

Family QA

Gameplay QA
```

Each stage should be independently reproducible.

---

# Design Philosophy

The Builder is a railway analysis engine.

Each stage transforms raw operational data into increasingly meaningful network objects.

```
Services
        │
        ▼
Service Patterns
        │
        ▼
Routes
        │
        ▼
Route Relationships
        │
        ▼
Route Families
        │
        ▼
Passenger Network
        │
        ▼
Gameplay
```

The Builder should derive knowledge from railway topology wherever possible rather than relying on manually maintained rules or network-specific assumptions.

Every stage should have:

- One responsibility
- One canonical output
- Well-defined inputs
- Deterministic behaviour
- Generic implementation

This architecture allows the Builder to scale across the entire National Rail network and provides a stable foundation for future gameplay, analytics, visualisation and quality assurance.