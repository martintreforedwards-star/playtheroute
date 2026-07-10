# The Route - Ontology

## Purpose

This document defines the core concepts used throughout **The Route** ecosystem.

It provides a common vocabulary for the Builder, game engine, Routepedia and future tooling.

The aim is to distinguish between objective railway data (which can be derived automatically) and editorial concepts (which are maintained by the project).

---

# Core Principles

The Builder should derive everything that can be calculated objectively from authoritative railway data.

Editorial concepts such as line names, historical information, articles and narratives should remain separate from the Builder and be maintained within Routepedia.

This separation allows the operational railway to evolve automatically as timetables change, whilst preserving human knowledge and storytelling.

---

# Core Objects

## Network

A **Network** is the highest-level collection of railway services represented within **The Route**.

Examples include:

- Southeastern
- Northern
- Southern
- ScotRail
- Elizabeth line

A Network contains Stations, Services and Service Patterns.

A Station may belong to more than one Network.

---

## Station

A **Station** is the fundamental geographic object within **The Route**.

Stations are uniquely identified by their CRS code and corresponding `station_id`.

A Station may contain:

- Name
- CRS
- Coordinates
- Attributes
- Landmarks
- Statistics
- Memberships

Stations belong to one or more Networks.

---

## Service

A **Service** is a single scheduled train operating within a timetable.

Examples include:

- 08:17 Liverpool Central → West Kirby
- 14:05 London Victoria → Brighton

Services are obtained directly from Darwin timetable data.

Services are timetable-specific and may change over time.

---

## Service Pattern

A **Service Pattern** is a unique sequence of station calls shared by one or more Services.

Many individual Services may share the same Service Pattern.

Example:

Liverpool Central

↓

Moorfields

↓

Sandhills

↓

...

↓

West Kirby

Service Patterns are automatically derived from Darwin timetable data.

Service Patterns form the operational representation of the railway used by the Builder.

---

## Line

A **Line** is a named railway corridor recognised by passengers or the railway industry.

Examples include:

- Brighton Main Line
- North Kent Line
- Calder Valley Line
- West Highland Line

Unlike Service Patterns, Lines are editorial concepts.

A Line may contain many Service Patterns.

Likewise, a Service Pattern may traverse multiple Lines.

Lines therefore form a many-to-many relationship with Service Patterns.

---

## Landmark

A **Landmark** is a notable place associated with one or more Stations.

Examples include:

- Canterbury Cathedral
- Angel of the North
- Brighton Palace Pier

Landmarks support gameplay, Routepedia and educational content.

---

## Routepedia Article

A **Routepedia Article** is an editorial object.

Articles may describe any railway concept, including:

- Stations
- Networks
- Lines
- Landmarks
- Service Patterns
- Historical railways
- Railway infrastructure

Routepedia therefore acts as the encyclopaedia of **The Route**.

---

# Relationships

The principal relationships within the system are:

Network

- contains Stations
- contains Services
- contains Service Patterns

Station

- belongs to one or more Networks
- belongs to one or more Service Patterns
- contains one or more Landmarks

Service

- belongs to a single Service Pattern

Service Pattern

- contains many Stations
- contains many Services
- may traverse multiple Lines

Line

- contains many Service Patterns
- may share Service Patterns with other Lines

Routepedia

- documents every object within the ecosystem.

---

# Data Layers

The Route consists of three logical layers.

## Reference Layer

Stable information.

Examples include:

- Stations
- Networks
- CORPUS reference data
- Landmarks

---

## Operational Layer

Information derived automatically from the timetable.

Examples include:

- Services
- Service Patterns
- Connectivity
- Service frequency
- Station usage

---

## Gameplay Layer

Information generated specifically for gameplay.

Examples include:

- Clue generation
- Puzzle generation
- Difficulty scoring
- Statistics
- Achievements
- Daily puzzles

---

# Builder Philosophy

The Builder exists to model the operational railway.

It should derive everything that can be calculated objectively from authoritative railway data.

Examples include:

- Service Patterns
- Connectivity
- Route membership
- Service counts
- Station statistics

The Builder should avoid storing editorial knowledge where possible.

---

# Routepedia Philosophy

Routepedia exists to explain the railway.

It provides the human layer that sits above the operational model.

Examples include:

- History
- Line descriptions
- Landmark articles
- Railway trivia
- Travel inspiration
- Photography
- Local knowledge

---

# Overall Philosophy

The Route consists of three complementary components.

- **The Builder** models the railway.
- **Routepedia** explains the railway.
- **The Game** allows players to explore the railway.

Each layer builds upon the one beneath it.