# CHANGELOG.md — PCB Design Assistant

All notable changes to the `pcb-design-assistant` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-07-01

### Added
- Initial release of PCB Design Assistant skill
- **Main Harness** (`skills/main.md`)
  - Intake and framing with targeted questions
  - Framework selection and screening logic
  - Sub-skill orchestration in sequence
  - Knowledge refresh protocol with graceful degradation
  - Three quality gates (evidence, framework, challenge)
  - Professional output format specification
  - Error handling for all edge cases

- **Sub-Skill: Framework Selector** (`skills/sub-evaluation-framework-selector.md`)
  - Board classification (digital/analog/RF/power, layer count, speed)
  - Governing framework selection logic
  - Evaluation scope determination
  - Typed input/output schema
  - Quality gate implementation

- **Sub-Skill: Scoring Engine** (`skills/sub-scoring-engine.md`)
  - Multi-dimensional scoring (placement, routing, power, SI, EMC, DFM)
  - IPC-2152 current capacity calculations
  - Evidence-based scoring with citations
  - Weighted scoring based on board type
  - Grade calculation (A-F scale)
  - Critical issue identification

- **Sub-Skill: Datasheet Updater** (`skills/sub-datasheet-updater.md`)
  - Datasheet acquisition and parsing pipeline
  - Parameter extraction (electrical, thermal, package)
  - Derating analysis by application type
  - IPC revision verification and constraint refinement
  - Constraint database update

- **Sub-Skill: Improvement Roadmap** (`skills/sub-improvement-roadmap.md`)
  - Issue categorization by domain
  - Impact/effort scoring algorithm
  - Priority calculation and ranking
  - Solution generation with specific steps
  - Phased implementation planning
  - Risk assessment

- **Knowledge Base** (`SECOND-KNOWLEDGE-BRAIN.md`)
  - Core concepts and frameworks (IPC-2221, IPC-2152, SI/PI/EMC)
  - Key research papers with DOI references
  - Quick reference tables (trace width, spacing, vias)
  - Authoritative data sources
  - State-of-the-art methods and tools
  - Self-update protocol configuration

- **Knowledge Updater Tool** (`tools/knowledge_updater.py`)
  - ArXiv category crawling (eess.SP)
  - Domain-specific search queries
  - Relevance scoring algorithm
  - Deduplication by URL/DOI hash
  - Graceful degradation when offline
  - Run logging and statistics

- **Test Suite** (`tests/test-scenarios.md`)
  - 6 comprehensive test scenarios:
    - TS-001: High-Speed Clock Routing
    - TS-002: Power Trace Current Capacity
    - TS-003: Decoupling Capacitor Placement
    - TS-004: EMC Pre-Scan Failure
    - TS-005: Datasheet Constraint Extraction
    - TS-006: DFM Footprint Mismatch
  - Regression fixtures with expected outputs
  - Cross-cutting tests (degradation, refusal, determinism)
  - Test execution protocol

- **Documentation**
  - `README.md` — Quick start guide and overview
  - `CLAUDE.md` — Project-specific instructions
  - `PROJECT-detail.md` — Technical specification
  - `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — Phase tracking
  - `CLUSTER-INTEGRATION.md` — Cluster standards
  - `CHANGELOG.md` — Version history (this file)

### Governing Frameworks
- IPC-2221: Generic Standard on Printed Board Design
- IPC-2152: Standard for Determining Current-Carrying Capacity
- Signal Integrity: Controlled impedance, return paths, length matching
- Power Integrity: Decoupling, PDN target impedance
- EMC/EMI: Ground planes, guard traces, emission control
- DFM: Design for Manufacturability
- Thermal Management: Component derating and heat dissipation

### Quality Standards
- Evidence Gate: All claims cite sources
- Framework Gate: All scoring uses named frameworks
- Challenge Gate: Devil's advocate stress-testing

### Cluster Integration
- Science, Engineering & Industry cluster standards
- Shared scoring schema (0-100, weighted, A-F grades)
- Issue severity classification (Critical/Major/Minor/Info)
- Evidence tier hierarchy (7 levels)
- Sub-skill pattern standardization
- Knowledge base structure standardization

## [Unreleased]

### Planned
- Additional test scenarios as edge cases emerge
- Knowledge base updates as standards evolve
- Potential integration with CAD tools for direct file analysis

---

## Version History Summary

| Version | Date | Status | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-07-01 | Current | Initial production release |

---

**Maintained By:** PCB Design Assistant Team  
**Cluster:** Science, Engineering & Industry  
**Last Updated:** 2026-07-01
