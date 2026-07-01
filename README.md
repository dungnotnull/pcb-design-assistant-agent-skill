# PCB Design Assistant

A professional-grade Claude skill for reviewing PCB placement, routing, and signal/power integrity against IPC standards and component datasheets. Every assessment is grounded in authoritative frameworks and delivers actionable insights.

## Overview

PCB Design Assistant transforms how you review circuit board layouts. It provides rigorous, evidence-based analysis across multiple dimensions - from signal integrity to manufacturability - and delivers a prioritized improvement roadmap with specific, actionable recommendations.

Built on industry standards including IPC-2221, IPC-2152, and proven signal integrity principles, this skill ensures your board designs meet professional quality standards before fabrication.

## What It Does

- Classifies your board (digital/analog/RF/power, layer count, speed) and selects applicable standards
- Scores placement, routing, power delivery, signal integrity, EMC/EMI, and DFM against named frameworks
- Ingests component datasheets to extract thermal limits, derating factors, and layout constraints
- Generates a prioritized improvement roadmap ranked by effort and impact
- Provides a professional-grade report suitable for design reviews and documentation

## Quick Start

### Basic Usage

Invoke the skill with a description of your PCB:

Review my 4-layer PCB with a 100MHz oscillator routed to an MCU. The board carries 3.3V at 2A and targets automotive application.

### What to Provide

For the most accurate review, include:

| Information | Example | Why It Matters |
|--------------|---------|----------------|
| Layer count | 4 layers | Determines stackup and routing options |
| Signal speeds | 100MHz clock | Selects SI framework and impedance requirements |
| Power requirements | 3.3V at 2A | Validates trace sizing per IPC-2152 |
| Application type | Automotive | Sets derating factors and compliance requirements |
| Component list | STM32F407 MCU | Enables datasheet-based constraint extraction |

### Sample Output

The skill delivers a structured report with six sections:

1. **Executive Summary** — Overall grade (A-F) and key findings at a glance
2. **Inputs & Assumptions** — What was analyzed and what conditions were assumed
3. **Multi-Dimensional Score** — Detailed scoring by dimension with framework citations
4. **Findings** — Strengths, critical issues, major issues, and informational notes
5. **Improvement Roadmap** — Prioritized actions with effort/impact analysis
6. **Sources & Limitations** — All citations and any constraints on the analysis

## Governing Frameworks

Every assessment is grounded in named, citable frameworks.

### Primary Frameworks

| Framework | Focus | Application |
|-----------|-------|-------------|
| IPC-2221 | Generic Standard on Printed Board Design | All boards |
| IPC-2152 | Current-Carrying Capacity of Conductors | Power traces |

### Secondary Frameworks

| Framework | Focus | Applied When |
|-----------|-------|--------------|
| Signal Integrity | Controlled impedance, return paths, length matching | High-speed designs |
| Power Integrity | Decoupling, PDN target impedance | Power-sensitive designs |
| EMC/EMI | Ground planes, guard traces, emission control | All designs, especially automotive |
| DFM | Design for Manufacturability | Production boards |
| Thermal Management | Component derating, heat dissipation | Power electronics |

## Skill Architecture

The skill implements a structured pipeline with four specialized sub-skills:

```
┌─────────────────────────────────────────────────────────────┐
│              PCB Design Assistant (Main Harness)            │
│                   Intake & Framing                           │
│            Framework Selection & Screening                   │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌─────────────┐ ┌────────────────┐
│  Sub-Skill 1   │ │ Sub-Skill 2 │ │  Sub-Skill 3   │
│  Framework    │ │   Scoring   │ │  Datasheet     │
│  Selector     │ │   Engine    │ │   Updater      │
└────────┬───────┘ └──────┬──────┘ └────────┬───────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
                ┌────────────────┐
                │  Sub-Skill 4   │
                │  Improvement   │
                │  Roadmap       │
                └────────┬───────┘
                         │
                         ▼
                ┌────────────────┐
                │  Quality Gates │
                │  + Synthesize  │
                └────────────────┘
```

### Quality Gates

Three gates ensure every deliverable meets professional standards:

| Gate | Purpose | What It Enforces |
|------|---------|------------------|
| Evidence | Traceability | Every claim cites a source or prior step |
| Framework | Consistency | All scoring uses named frameworks, never ad-hoc |
| Challenge | Rigor | Devil's advocate stress-testing before output |

## Use Cases

### High-Speed Digital Design

Check my DDR3 interface on 6 layers. The clock runs at 400MHz and I have 8 data lanes.

**What gets analyzed:** Impedance control, length matching, return path continuity, via transitions

### Power Electronics

My DC-DC converter supplies 5V at 5A. Are the power traces adequate for this current?

**What gets analyzed:** IPC-2152 calculations, temperature rise, copper weight adequacy

### EMC Pre-Compliance

My board failed EMC pre-scan at 150MHz. What layout issues might cause this?

**What gets analyzed:** Ground plane integrity, clock routing, loop areas, filtering needs

### Automotive Compliance

This board goes into a vehicle. What derating should I apply for the power components?

**What gets analyzed:** Component datasheets, AEC-Q100 requirements, thermal margins

### DFM Review

Check if my footprints meet IPC-7351 standards for production assembly.

**What gets analyzed:** Land pattern dimensions, solder mask clearances, panelization

## Scoring Dimensions

The skill evaluates six dimensions, each scored 0-100:

| Dimension | What It Checks | Key References |
|-----------|----------------|----------------|
| Placement | Component orientation, flow, decoupling proximity | IPC-2221, design guidelines |
| Routing | Trace widths, spacing, via usage, return paths | IPC-2221, IPC-2152, SI principles |
| Power Delivery | Trace sizing, decoupling adequacy, PDN quality | IPC-2152, PI principles |
| Signal Integrity | Impedance control, length matching, termination | Transmission line theory |
| EMC/EMI | Ground planes, guard traces, emission sources | Henry Ott EMC, IEC standards |
| DFM | Feature sizes, manufacturability, assembly | IPC-A-600, IPC-7351 |

Scores are weighted based on board type and combined into an overall grade:

- A (90-100): Production ready, minimal concerns
- B (80-89): Good quality, minor issues
- C (70-79): Adequate, notable concerns
- D (60-69): Poor quality, significant issues
- F (<60): Critical, requires redesign

## Installation

### As a Claude Skill

1. Clone this repository to your skills directory
2. The skill is self-contained and ready to use

### For Development

1. Clone the repository
2. Review the project structure in README.md
3. See PROJECT-detail.md for technical specifications

## Project Structure

```
pcb-design-assistant/
├── README.md                          # This file
├── CHANGELOG.md                       # Version history
├── CLAUDE.md                           # Project instructions
├── PROJECT-detail.md                   # Technical specification
├── CLUSTER-INTEGRATION.md             # Cluster standards
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Development tracking
├── SECOND-KNOWLEDGE-BRAIN.md           # Knowledge base
├── skills/
│   ├── main.md                        # Main harness
│   ├── sub-evaluation-framework-selector.md  # Board classification
│   ├── sub-scoring-engine.md          # Multi-dimensional scoring
│   ├── sub-datasheet-updater.md       # Datasheet processing
│   └── sub-improvement-roadmap.md     # Improvement planning
├── tests/
│   └── test-scenarios.md              # Test suite
└── tools/
    └── knowledge_updater.py           # Knowledge refresh script
```

## Knowledge Base

The skill maintains a comprehensive knowledge base (SECOND-KNOWLEDGE-BRAIN.md) with:

- Core concepts for all governing frameworks
- Key research papers with DOI references
- Quick reference tables (trace widths, spacing, vias)
- Authoritative data sources and how to use them
- State-of-the-art methods and tools

The knowledge base can be refreshed automatically using the provided updater script.

## Testing

Six comprehensive test scenarios validate the skill across diverse use cases:

| Scenario | Focus | What It Tests |
|----------|-------|---------------|
| TS-001 | High-speed clock routing | Return path analysis, length matching |
| TS-002 | Power trace capacity | IPC-2152 calculations |
| TS-003 | Decoupling placement | PDN analysis, capacitor proximity |
| TS-004 | EMC pre-scan failure | Emission source identification |
| TS-005 | Datasheet extraction | Thermal and derating analysis |
| TS-006 | DFM footprint review | IPC-7351 compliance |

Each scenario includes expected inputs, behavior, validation criteria, and regression fixtures.

## Documentation

- **README.md** (this file) — Overview and quick start
- **PROJECT-detail.md** — Complete technical specification
- **CLUSTER-INTEGRATION.md** — Science & Engineering cluster standards
- **CHANGELOG.md** — Version history and changes

## Version

Current version: 1.0.0

Released: 2026-07-01

## License

This skill is part of the Science, Engineering & Industry cluster and follows cluster standards documented in CLUSTER-INTEGRATION.md.

## Contributing

Contributions are welcome. Please maintain:

- Evidence-based analysis (all claims cite sources)
- Framework-grounded scoring (no ad-hoc criteria)
- Quality gate enforcement
- Test scenario coverage
- Documentation currency

## Support

For questions or issues:

1. Review the test scenarios for usage examples
2. Check PROJECT-detail.md for technical details
3. Consult CLUSTER-INTEGRATION.md for standards

---

**Skill Version:** 1.0.0  
**Cluster:** Science, Engineering & Industry  
**Last Updated:** 2026-07-01
