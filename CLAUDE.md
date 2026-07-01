# CLAUDE.md — PCB Design / Component Placement Assistant

**Skill slug:** `pcb-design-assistant`
**Source idea:** #175 (Vietnamese backlog `ideas.md`)
**Cluster:** science-industry — Science, Engineering & Industry
**Tagline:** Review PCB placement, routing, and signal/power integrity against IPC standards and datasheets.
**Current phase:** Phase 4 — Testing & Validation (initial build complete)

## Problem This Skill Solves
Designers lay out PCBs without rigorous attention to return paths, decoupling, controlled impedance, and manufacturability, producing boards that fail EMC or are hard to fabricate. This skill reviews a layout/netlist description, scores placement and routing against IPC and SI/PI/EMC principles, and continuously ingests component datasheets and design-rule updates.

## Harness Flow (Summary)
1. **Intake** → `sub-evaluation-framework-selector` gathers inputs and frames the problem.
2. **Screen / select** → `sub-scoring-engine` selects the governing framework and screens risk/scope.
3. **Score / analyze** → `sub-datasheet-updater` produces a multi-dimensional score against named frameworks.
4. **Knowledge refresh** → optional `tools/knowledge_updater.py` run keeps SECOND-KNOWLEDGE-BRAIN.md current.
5. **Gate** → quality / evidence gates must pass.
6. **Synthesize** → main harness emits the scored deliverable + prioritized improvement roadmap.

## Sub-skills
- `skills/sub-evaluation-framework-selector.md` — Classify the board (digital/analog/RF/power, layer count, speed) and select the governing IPC/SI/PI rule set.
- `skills/sub-scoring-engine.md` — Score placement, routing, power delivery, and DFM against the rules; produce a layout quality grade.
- `skills/sub-datasheet-updater.md` — Ingest component datasheets and IPC revisions to refine constraints (footprints, derating, thermal).
- `skills/sub-improvement-roadmap.md` — Output a prioritized layout-fix roadmap (re-route, add decoupling, plane changes) with effort/impact.

## Tools Required
WebSearch, WebFetch, Read, Write, Bash

## Knowledge Sources (for crawl + reasoning)
- IPC standards (ipc.org) — IPC-2221/2152/A-600
- Semiconductor manufacturer datasheets & app notes (TI, ST, Analog Devices)
- ArXiv (eess.SP) and IEEE for signal/power-integrity research
- KiCad / Altium design-rule documentation
- Reputable hardware design references (Henry Ott EMC, Howard Johnson SI)

## Supporting Python Tools
- `tools/knowledge_updater.py` — crawl4ai + WebSearch pipeline that fetches latest papers/reports from the domain sources above, scores by recency + relevance, deduplicates by URL/DOI hash, and appends to `SECOND-KNOWLEDGE-BRAIN.md`. Recommended schedule: weekly cron.

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Define >=3 sub-skills with quality gates
- [x] Ground scoring in named world-renowned frameworks
- [x] Wire knowledge_updater crawl sources
- [ ] Expand SECOND-KNOWLEDGE-BRAIN with first live crawl batch
- [ ] Add regression fixtures from the test scenarios

## Reference Docs (this folder)
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base
- `skills/main.md` — harness entry point
