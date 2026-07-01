# PROJECT-detail.md — PCB Design / Component Placement Assistant

## Executive Summary
This skill is a full Claude harness that turns review PCB placement, routing, and signal/power integrity against IPC standards and datasheets. It operates research-first: every material judgment is grounded in a named, citable framework and, where possible, a freshly retrieved source. It produces a professional-grade deliverable: a multi-dimensional score against the chosen framework plus a prioritized, effort/impact-ranked improvement roadmap.

## Problem Statement
Designers lay out PCBs without rigorous attention to return paths, decoupling, controlled impedance, and manufacturability, producing boards that fail EMC or are hard to fabricate. This skill reviews a layout/netlist description, scores placement and routing against IPC and SI/PI/EMC principles, and continuously ingests component datasheets and design-rule updates.

## Target Users & Use Cases
Primary users are practitioners and decision-makers in the **Science, Engineering & Industry** domain. Trigger examples:
1. User describes a 4-layer board with a high-speed clock; skill checks return-path and length-matching rules.
2. A power trace is undersized for 3A; skill computes IPC-2152 width and flags it.
3. Decoupling caps are placed far from the IC; skill scores PDN risk and recommends placement.
4. Board fails EMC pre-scan; skill suggests ground-plane and guard-trace fixes.
5. User pastes a component datasheet; updater extracts thermal/derating constraints into the review.
6. Footprint mismatch risks an assembly defect; DFM check flags it before fabrication.

## Harness Architecture
```
/pcb-design-assistant (main.md harness)
  -> sub-evaluation-framework-selector              [intake / framing]
  -> sub-scoring-engine              [framework selection / risk-scope screen]
  -> knowledge refresh   [SECOND-KNOWLEDGE-BRAIN via knowledge_updater.py]
  -> sub-datasheet-updater              [multi-dimensional scoring]
  -> evidence + challenge gate
  -> improvement roadmap [prioritized, effort/impact]
  -> SYNTHESIZE          [final scored deliverable]
```

## Full Sub-Skill Catalog
### sub-evaluation-framework-selector
- **Purpose:** Classify the board (digital/analog/RF/power, layer count, speed) and select the governing IPC/SI/PI rule set.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-scoring-engine
- **Purpose:** Score placement, routing, power delivery, and DFM against the rules; produce a layout quality grade.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-datasheet-updater
- **Purpose:** Ingest component datasheets and IPC revisions to refine constraints (footprints, derating, thermal).
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-improvement-roadmap
- **Purpose:** Output a prioritized layout-fix roadmap (re-route, add decoupling, plane changes) with effort/impact.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.

## Skill File Format Specification
Every skill file uses YAML frontmatter (`name`, `description`) followed by the required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates. The main harness invokes sub-skills via the Skill tool in the order shown above.

## E2E Execution Flow
1. Parse the user request; if inputs are insufficient, `sub-evaluation-framework-selector` asks targeted intake questions.
2. `sub-scoring-engine` selects the governing framework(s) and screens scope/risk; branch to a refusal or disclaimer if out of scope.
3. Refresh knowledge if the brain is stale (>7 days) and WebSearch/WebFetch are available; otherwise degrade gracefully to internal knowledge with a stated limitation.
4. `sub-datasheet-updater` scores each dimension, citing evidence per claim.
5. Run the evidence/quality gate(s) and a devil's-advocate challenge pass.
6. Emit the scored report + roadmap in the Output Format below.

## SECOND-KNOWLEDGE-BRAIN Integration
- **Sources:** IPC standards (ipc.org) — IPC-2221/2152/A-600; Semiconductor manufacturer datasheets & app notes (TI, ST, Analog Devices); ArXiv (eess.SP) and IEEE for signal/power-integrity research; KiCad / Altium design-rule documentation; Reputable hardware design references (Henry Ott EMC, Howard Johnson SI)
- **Crawl config:** see `tools/knowledge_updater.py` (ArXiv categories eess.SP; domain queries seeded from the idea).
- **Append format:** date-stamped entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance note; deduplicated by URL/DOI hash.

## Supporting Tools Spec — knowledge_updater.py
- **Inputs:** search queries + source list (in-file config), optional `--since` date.
- **Outputs:** appended entries in `SECOND-KNOWLEDGE-BRAIN.md` + a run log.
- **Schedule:** weekly cron (graceful no-op when offline).

## Quality Gates
- **Evidence gate:** every material claim is traceable to a cited source or a prior step; prefer the highest evidence tier available.
- **Framework gate:** all scoring is grounded in the named frameworks below — never ad-hoc criteria.
- **Challenge gate:** a devil's-advocate pass has stress-tested the recommendation before it is shown.

## Test Scenarios
See `tests/test-scenarios.md` (>=5 concrete scenarios with expected harness behavior).

## Key Design Decisions
1. Framework-grounded scoring only — no ad-hoc rubrics.
2. Research-first with graceful degradation when offline.
3. Composable sub-skills (>=3) so cluster siblings can reuse them.
4. Deliverable is an artifact (scored report + roadmap), not a chat reply.
5. Evidence/quality gate enforced before any sensitive/regulated output.
