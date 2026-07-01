# CLUSTER-INTEGRATION.md — Science, Engineering & Industry Cluster

> Integration standards and shared components for `science-industry` cluster skills.

## Cluster Overview

The `science-industry` cluster includes skills for technical domains in science, engineering, and industrial applications. Skills share common patterns for evaluation, scoring, and knowledge management.

### Cluster Skills

1. **pcb-design-assistant** — PCB layout review against IPC and SI/PI standards
2. *(Future skills to be added)*

## Shared Component Architecture

### Scoring Schema Standard

All cluster skills use this standardized scoring schema for multi-dimensional evaluation:

```json
{
  "dimension_scores": {
    "<dimension_name>": {
      "score": 0-100,
      "weight": 0.5-2.0,
      "findings": [...],
      "framework": "<named_framework>"
    }
  },
  "overall_quality": {
    "score": "<weighted_average>",
    "grade": "<A/B/C/D/F>",
    "confidence": "<high/medium/low>"
  }
}
```

**Standard Dimension Categories:**
- Design Quality (implementation against standards)
- Performance (functionality and metrics)
- Reliability (robustness and failure modes)
- Compliance (regulatory and safety)
- Maintainability (future support and modification)

**Standard Grade Scale:**
- A: 90-100 — Production ready, minimal concerns
- B: 80-89 — Good quality, minor issues
- C: 70-79 — Adequate, notable concerns
- D: 60-69 — Poor quality, significant issues
- F: <60 — Critical, requires redesign

### Issue Severity Standard

All cluster skills use this severity classification:

| Severity | Weight | Description | Timeframe |
|----------|--------|-------------|-----------|
| Critical | 10 | Will cause failure or safety hazard | Immediate |
| Major | 7 | Significant impact on performance/reliability | Short-term |
| Minor | 4 | Marginal impact, cosmetic | Medium-term |
| Info | 1 | Informational, no action required | None |

### Evidence Tiers

All cluster skills prefer these evidence tiers (highest to lowest):

1. **Systematic Review** — Meta-analysis of multiple studies
2. **Meta-Analysis** — Statistical analysis of multiple studies
3. **RCT/Benchmark** — Controlled experiments or standardized tests
4. **Cohort/Field Study** — Real-world observations
5. **Expert Consensus** — Industry expert agreement
6. **Expert Opinion** — Individual expert view
7. **Blog/Vendor Content** — Commercial or informal sources

### Sub-Skill Pattern Standard

All cluster sub-skills follow this template:

```markdown
---
name: sub-<skill-name>
description: <One-line description>
---

## Role
Sub-skill of `<parent-skill>`. <Extended description>.

## Inputs
- **<input_name>** (type, required/optional): Description

## Procedure
1. Validate inputs
2. Apply framework
3. Generate structured output
4. Self-check against quality gate

## Outputs
- Structured result object for next stage

## Tools
[List of tools]

## Quality Gate
- Specific gate requirements
```

## Knowledge Base Standard

All cluster skills use SECOND-KNOWLEDGE-BRAIN.md with this structure:

```markdown
## Core Concepts & Frameworks
## Key Research Papers (table format)
## State-of-the-Art Methods & Tools
## Authoritative Data Sources
## Analytical Frameworks (Scoring Backbone)
## Self-Update Protocol
## Knowledge Update Log
```

**Citation Format:**
- Standards: `[Standard Name] [Revision], [Section/Paragraph]`
- Papers: `[Authors], [Title], [Venue], [Year]`
- Datasheets: `[Manufacturer] [Part Number], [Document ID], [Revision]`
- Books: `[Author], [Book Title], [Publisher], [Year], [Chapter]`

## Quality Gates Standard

All cluster skills implement these quality gates:

### 1. Evidence Gate
- Every material claim traces to cited source
- Evidence tier explicitly stated
- No "best practices" without citation

### 2. Framework Gate
- All scoring grounded in named frameworks
- No ad-hoc criteria
- Framework sources documented

### 3. Challenge Gate
- Devil's advocate pass completed
- Alternative interpretations considered
- Risks and limitations documented

## Output Format Standard

All cluster skills produce structured reports with:

1. **Executive Summary** — Verdict and key findings
2. **Inputs & Assumptions** — What was provided and assumed
3. **Multi-Dimensional Score** — Scores by dimension with evidence
4. **Findings** — Strengths, risks, and gaps
5. **Improvement Roadmap** — Prioritized actions with effort/impact
6. **Sources & Limitations** — Citations and constraints

## Tool Standardization

All cluster skills support:

- **WebSearch** — Framework verification, latest standards lookup
- **WebFetch** — Document retrieval, datasheet access
- **Read** — Knowledge base and file review
- **Write** — Report generation
- **Bash** — Optional tool execution

## Error Handling Standard

All cluster skills handle errors consistently:

### Graceful Degradation
- If external tools unavailable, continue with existing knowledge
- State limitation explicitly
- Set confidence level appropriately

### Out-of-Scope Handling
- Politely refuse out-of-scope requests
- Explain scope boundaries
- Suggest alternative resources
- Offer in-scope alternatives if available

### Insufficient Information
- Request specific missing information
- Provide partial assessment with disclaimers
- State what cannot be evaluated
- Offer re-evaluation when information available

## Testing Standard

All cluster skills include:

1. **Test Scenarios** — Minimum 6 scenarios covering:
   - Common use cases
   - Edge cases
   - Out-of-scope requests
   - Error conditions

2. **Regression Fixtures** — Expected outputs for:
   - Scoring results
   - Issue identification
   - Framework citations
   - Grade assignments

3. **Cross-Cutting Tests** — Verify:
   - Graceful degradation
   - Out-of-scope handling
   - Determinism
   - Quality gate enforcement

## Version Control Standard

All cluster skills use:

- **Semantic Versioning** — Major.Minor.Patch
- **CHANGELOG.md** — Document all changes
- **Tagging** — Tag releases in git
- **Backward Compatibility** — Maintain where possible

## Documentation Standard

All cluster skills include:

1. **README.md** — Quick start guide
2. **PROJECT-detail.md** — Technical specification
3. **PROJECT-DEVELOPMENT-PHASE-TRACKING.md** — Phase tracking
4. **CLAUDE.md** — Project-specific instructions
5. **CLUSTER-INTEGRATION.md** — This file

## Inter-Skill Communication

When skills need to reference each other:

1. Use skill names as constants
2. Document expected input/output formats
3. Handle failures gracefully
4. Provide clear error messages

## Future Cluster Skills

When adding new skills to `science-industry` cluster:

1. Follow all cluster standards
2. Reuse shared components where applicable
3. Update this file with skill-specific additions
4. Maintain backward compatibility
5. Add test scenarios for integration

## Maintenance Protocol

### Regular Updates
- Review standards annually for revisions
- Update knowledge bases quarterly
- Refresh test scenarios as needed

### Deprecation
- Document deprecated components
- Provide migration path
- Maintain 6-month deprecation notice

---

**Cluster Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Maintainer:** PCB Design Assistant Team
