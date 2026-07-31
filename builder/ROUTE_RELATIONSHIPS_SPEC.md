# Route Relationships Specification

## Purpose

The Route Relationship Engine analyses the canonical route catalogue and discovers
structural relationships between routes.

Unlike the Route Graph (which relates service patterns within a route), the
Relationship Engine analyses relationships between complete routes.

The output becomes the authoritative source for route families, network
classification and future visualisation.

---

# Inputs

The relationship engine consumes only canonical Builder outputs.

## Required

routes.csv

## Optional

pattern_routes.csv

service_patterns.csv

station_graph.csv (future)

No network-specific knowledge should be required.

---

# Output

route_relationships.csv

Each row represents one discovered relationship between two routes.

Relationships are directional where appropriate.

---

# Schema

| Field | Description |
|---------|-------------|
| relationship_id | Unique identifier |
| route_a | Primary route |
| route_b | Related route |
| relationship | Relationship type |
| confidence | Confidence (0.0–1.0) |
| evidence | Human-readable explanation |

---

# Shared Metrics

These values explain why the relationship exists.

| Field | Description |
|---------|-------------|
| shared_station_count | Number of shared stations |
| shared_prefix_length | Shared stations from origin |
| shared_suffix_length | Shared stations from destination |
| overlap_percent | Percentage overlap |
| divergence_station | First differing station |
| merge_station | First common station after divergence |

These values should be generated for every relationship where possible.

---

# Relationship Types

## Parent

Definition

Route A completely contains Route B.

Characteristics

- Child is a complete subset.
- Child has fewer stations.
- Child shares the same origin.

Example

London → Oxford

contains

London → Banbury

---

## Child

Reverse of Parent.

---

## Branch

Definition

Routes share a common trunk before permanently diverging.

Characteristics

- Long shared prefix.
- Different destinations.
- No subsequent merge.

Example

Reading

├── Oxford

└── Newbury

---

## Merge

Definition

Independent routes join to form a common corridor.

Example

Caterham

and

Tattenham Corner

joining towards London.

---

## Parallel

Definition

Routes serve substantially the same corridor but follow different paths.

Example

Fast and stopping variants.

---

## Continuation

Definition

One route naturally extends another.

Example

Cardiff → Swansea

continues as

Swansea → Carmarthen

---

## Intersect

Definition

Routes cross but neither contains the other.

---

## Independent

Definition

No meaningful structural relationship.

Independent relationships do not need to be written to the output.

---

# Confidence

Every relationship receives a confidence score.

100%

Relationship proven exactly.

90%

Very strong structural evidence.

75%

Likely relationship.

Below 50%

Relationship should not normally be emitted.

---

# Evidence

Every generated relationship should explain itself.

Examples

Shared first 18 stations.

Child route is complete prefix.

Routes diverge after Reading.

Routes merge at East Croydon.

91% station overlap.

The Builder should never generate relationships that cannot be explained.

---

# Design Principles

The Relationship Engine should derive relationships from railway topology.

It should not rely upon:

- operator names
- manually maintained lists
- network-specific rules
- geographical assumptions

The same algorithms should operate successfully on every UK railway network.

---

# Future Uses

The relationship engine provides the foundation for:

- Route Families
- Main Line identification
- Branch detection
- Automatic maps
- Gameplay generation
- Network QA
- Visualisation