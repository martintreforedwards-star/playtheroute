# The Route Builder Framework

## Vision

The Route Builder is responsible for transforming authoritative railway data into complete, playable game datasets.

The framework exists so that adding a new operator requires only configuration and data, **not new Python code**.

---

# Core Principles

1. One builder for every operator.
2. One authoritative source of station information.
3. Configuration-driven builds.
4. Automatically calculated metadata wherever possible.
5. No duplicated logic between operators.

---

# Canonical Data Model

## CRS Source of Truth

The foundation of every build is the national CRS Source of Truth.

This contains permanent station information including:

* CRS code
* Canonical station name
* Latitude
* Longitude
* Region
* Country
* Airport links
* Future permanent metadata

No operator dataset should duplicate this information.

---

# Builder Pipeline

```
CRS Source of Truth
        │
        ▼
Network Membership
        │
        ▼
Master Dataset
        │
        ▼
Network Enrichment
        │
        ▼
Wordplay Engine
        │
        ▼
JSON Export
        │
        ▼
Game Assets
```

---

## Stage 1 — Network Assembly

Inputs:

* CRS Source of Truth
* Network membership
* Route definitions

Output:

operator_master_v1.csv

This stage extracts only the stations belonging to the selected operator.

---

## Stage 2 — Network Enrichment

Adds operational and gameplay metadata.

Examples:

* route groups
* regions
* branch/mainline
* coastal
* interchange
* terminus
* accessibility
* journey times
* distance bands
* difficulty
* puzzle metadata

Output:

operator_v1_enriched.csv

---

## Stage 3 — Wordplay Engine

The Wordplay Engine analyses every station name and creates reusable clue attributes.

### Structural

* first letter
* last letter
* first word
* last word
* word count
* character count
* vowel count
* consonant count
* punctuation
* numbers

### Prefixes

Examples:

* New
* Old
* Great
* Little
* North
* South
* East
* West
* Upper
* Lower

### Suffixes

Examples:

* Bridge
* Road
* Green
* Hill
* Gate
* Cross
* Junction
* Central
* Street
* Market
* Airport

### Themes

* Nature
* Water
* Animals
* Colours
* Religion
* Royal
* Transport
* Settlement
* Geography
* Numbers
* Personal names

Each theme should support multiple subcategories.

### Regional Linguistics

Examples:

#### Welsh

* Aber
* Llan
* Tre
* Pont

#### Scottish

* Inver
* Glen
* Loch
* Kil
* Ben
* Strath

#### English

* Ham
* Ton
* Worth
* Wick
* Chester
* Cester
* Bury
* Hurst
* Stead

These lists should evolve from analysing the complete CRS dataset rather than being manually invented.

---

## Stage 4 — JSON Export

Converts the enriched dataset into the format consumed by the game.

Output:

operator.json

---

# Discovery

The framework should include a discovery mode which analyses the entire CRS Source of Truth.

Example reports:

* Most common prefixes
* Most common suffixes
* Most common words
* Regional linguistic patterns
* Theme frequencies
* Candidate clue categories
* Rare but interesting words

The aim is for the builder to discover future clue opportunities automatically.

---

# Future Builder Modules

```
builder/

build_network.py
assemble.py
enrichment.py
wordplay.py
json_builder.py
validators.py
config.py
loaders.py
exporters.py
```

---

# Success Criteria

To add a new network:

1. Define membership.
2. Define routes.
3. Add configuration.
4. Run:

python builder/build_network.py operator

No operator-specific Python should be written.
