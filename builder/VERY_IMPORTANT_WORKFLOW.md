Project objective
Produce a complete, playable UK network from national datasets with the generic Builder.
New networks should require data and configuration, not new code.
Canonical data sources
Darwin timetable: service extraction and operator membership.
CORPUS: TIPLOC → CRS translation only.
National Rail Stations JSON: canonical station metadata (name, CRS, coordinates, accessibility, etc.).
Builder pipeline
Service Builder reads Darwin.
CORPUS resolves TIPLOCs.
Extract operator-specific services.
Generate *_master.csv.
Generate route_membership.csv.
Enrichment.
JSON.
Wordplay analysis.
Clue generation.
Validation.
Live page.
Current Builder components
service_builder.py is the primary extraction engine.
Avoid creating duplicate extraction scripts.
Any extraction should build on existing Builder outputs.
Lessons learned from ScotRail
Builder bugs should be fixed once, not worked around.
Avoid hard-coded network names and folder paths.
Use configuration rather than assumptions.
Network build philosophy
One Builder.
One workflow.
One set of national datasets.
One canonical station source.
No network-specific code unless there is a genuine operational difference (e.g. bilingual output).
Future multilingual support
TFW will generate parallel English and Cymraeg outputs from the same master data.
This is an enhancement to the Builder, not a special-case workflow.
Working practices
Read existing Builder components before writing new ones.
Reuse existing data products where possible.
Don't create parallel pipelines that duplicate existing functionality.
When a new network exposes a Builder bug, fix the Builder rather than adding network-specific logic.