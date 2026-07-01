---
name: sub-improvement-roadmap
description: Output a prioritized layout-fix roadmap (re-route, add decoupling, plane changes) with effort/impact.
---

## Role
Sub-skill of `pcb-design-assistant`. Output a prioritized, effort/impact-ranked improvement roadmap based on scoring findings and constraint violations.

## Inputs
- **refined_scoring_result** (object, required): Output from `sub-datasheet-updater` with refined scoring
- **critical_issues** (array, required): List of all identified critical and major issues
- **framework_violations** (array, optional): Specific framework violations identified
- **user_priority_factors** (object, optional): User-specified priorities (time_to_market, cost_sensitivity, quality_requirement, reliability_criticality)

## Procedure

### 1. Validate Inputs
- Verify refined scoring result is valid and complete
- Ensure critical issues array is present and populated
- Check that each issue has severity, framework reference, and description

### 2. Issue Categorization and Impact Assessment

#### 2.1 Categorize Issues by Domain

Organize issues into domain categories:
- **Signal Integrity Issues:** Impedance mismatches, length mismatches, return path problems
- **Power Integrity Issues:** Insufficient decoupling, inadequate trace widths, PDN problems
- **EMC/EMI Issues:** Ground plane discontinuities, insufficient filtering, loop area problems
- **DFM Issues:** Manufacturing constraints, assembly problems, yield risks
- **Thermal Issues:** Heat dissipation problems, inadequate thermal relief
- **Reliability Issues:** Derating violations, overstressed components

#### 2.2 Assign Impact Scores

For each issue, calculate impact score based on:

**Failure Impact Assessment:**
```
Impact = (Severity Weight × Failure Probability) + (Quality Impact) + (Cost of Rework)

Where:
- Severity Weight: Critical=10, Major=7, Minor=4, Info=1
- Failure Probability: 
  - Certain (>90%): 1.0
  - Likely (50-90%): 0.7
  - Possible (20-50%): 0.4
  - Unlikely (<20%): 0.1
- Quality Impact: 
  - Affects reliability/lifespan: +3
  - Affects performance marginally: +1
  - Cosmetic only: +0
- Cost of Rework:
  - Board respin required: +5
  - Rework possible but difficult: +3
  - Simple mod: +1
  - No rework: +0
```

**Application-Specific Impact Modifiers:**
- **Automotive:** Safety-related failures ×2, reliability-related ×1.5
- **Medical:** Patient safety related ×3, critical function ×2
- **Aerospace:** Flight-critical ×3, non-critical ×1.5
- **Industrial:** Safety ×1.5, reliability ×1.3
- **Consumer:** Functionality impact only ×1.0

### 3. Effort Assessment

For each issue, estimate effort required for resolution:

**Effort Scoring:**
```
Effort Score = (Design Effort) + (Validation Effort) + (Risk of Change)

Where:
- Design Effort:
  - Trivial (minutes): 1
  - Simple (hours): 3
  - Moderate (days): 7
  - Significant (weeks): 15
  - Major (months): 30

- Validation Effort:
  - Visual inspection only: 0
  - Simple measurement: 2
  - Simulation required: 5
  - Prototype testing: 10
  - Full re-qualification: 20

- Risk of Change:
  - No risk: 0
  - Low risk (localized): 3
  - Medium risk (affects subsystem): 7
  - High risk (affects system): 15
  - Very high risk (system redesign): 25
```

**Complexity Factors:**
- Layer stackup changes: +10
- Major component moves: +8
- Power plane modifications: +7
- High-speed net re-routing: +6
- BGA rework: +5

### 4. Priority Calculation

Calculate priority score for each issue:

```
Priority = Impact / Effort

Priority Levels:
- Very High: >3.0 (critical, quick wins)
- High: 1.5-3.0 (important, reasonable effort)
- Medium: 0.7-1.5 (worthwhile, significant effort)
- Low: 0.3-0.7 (marginal return)
- Very Low: <0.3 (not worth pursuing)
```

### 5. Solution Generation

For each prioritized issue, generate specific solution options:

#### 5.1 Solution Template
```json
{
  "issue_id": "SI-001",
  "issue": "Differential pair length mismatch",
  "impact_score": 8.5,
  "effort_score": 7,
  "priority": "high",
  "solutions": [
    {
      "approach": "Add tuning serpentines to shorter pair",
      "steps": [
        "Identify shorter trace in pair USB_DP/USB_DM",
        "Add serpentine pattern in inner layer (layer 2)",
        "Maintain 100Ω impedance throughout serpentine",
        "Verify with field solver"
      ],
      "estimated_effort": "4 hours",
      "required_tools": "Layout editor, impedance calculator",
      "risk_level": "low",
      "side_effects": "Slightly increased trace length, minor impact on timing margin"
    },
    {
      "approach": "Re-route both pairs with equal length from source",
      "steps": [
        "Remove existing routing",
        "Route new paths with length matching constraint enabled",
        "Use meander routing tool for final adjustment",
        "Verify with DRC and length checker"
      ],
      "estimated_effort": "1 day",
      "required_tools": "Layout editor with length matching",
      "risk_level": "medium",
      "side_effects": "May require layer changes, could affect other routing"
    }
  ]
}
```

#### 5.2 Solution Categories

**Signal Integrity Solutions:**
- Impedance adjustments (trace width, dielectric thickness)
- Length matching (serpentines, re-routing)
- Termination changes
- Layer stackup modifications
- Via optimization

**Power Integrity Solutions:**
- Decoupling capacitor additions
- Power plane improvements
- Trace width increases per IPC-2152
- Via additions for current capacity
- PDN restructuring

**EMC/EMI Solutions:**
- Ground plane repairs
- Guard trace additions
- Filter component additions
- Shielding implementation
- Loop area reduction

**DFM Solutions:**
- Feature size adjustments
- Solder mask modifications
- Silkscreen improvements
- Panelization changes
- Test point additions

### 6. Roadmap Structure

Organize solutions into a structured roadmap:

```json
{
  "roadmap_summary": {
    "total_issues": 15,
    "critical_issues": 3,
    "major_issues": 7,
    "estimated_total_effort": "3-4 weeks",
    "recommended_approach": "phased_implementation",
    "projected_quality_improvement": "C → A"
  },
  "phased_implementation": [
    {
      "phase": 1,
      "name": "Critical Fixes - Immediate",
      "duration": "1 week",
      "priority_range": "very_high",
      "issues": ["SI-001", "PI-003", "EMC-002"],
      "total_effort": "40 hours",
      "quality_impact": "Eliminates board respin risk",
      "deliverables": [
        "All signal integrity critical violations resolved",
        "Power delivery meets derated requirements",
        "EMC pre-compliance likely to pass"
      ]
    },
    {
      "phase": 2,
      "name": "Major Improvements - Short Term",
      "duration": "2 weeks",
      "priority_range": "high",
      "issues": ["SI-003", "PI-004", "DFM-001", "DFM-002"],
      "total_effort": "80 hours",
      "quality_impact": "Moves from C to B grade",
      "deliverables": [
        "All major issues resolved",
        "Manufacturability significantly improved",
        "Reliability margins adequate"
      ]
    },
    {
      "phase": 3,
      "name": "Enhancements - Medium Term",
      "duration": "1 week",
      "priority_range": "medium",
      "issues": ["SI-005", "THERMAL-001", "DFM-003"],
      "total_effort": "40 hours",
      "quality_impact": "Achieves A grade quality",
      "deliverables": [
        "Optimization and margin improvements",
        "Production yield maximization",
        "Long-term reliability assurance"
      ]
    }
  ],
  "prioritized_actions": [
    {
      "rank": 1,
      "issue": "SI-001: Differential pair length mismatch exceeds tolerance",
      "impact": 8.5,
      "effort": 7,
      "priority": "high",
      "recommended_solution": "Add tuning serpentines to shorter pair",
      "estimated_time": "4 hours",
      "responsible": "Layout engineer",
      "validation": "Length measurement, impedance check"
    }
    // ... more actions ranked by priority
  ],
  "quick_wins": [
    {
      "issue": "DFM-007: Add fiducial markers for assembly",
      "effort": 2,
      "impact": 4,
      "priority": "high",
      "solution": "Add 2 fiducials per panel per IPC-7351"
    }
  ],
  "resource_requirements": {
    "personnel": ["Layout engineer", "Hardware engineer for validation"],
    "tools": ["PCB CAD tool", "Impedance calculator", "SI simulation tool (recommended)"],
    "fabrication_support": "Early fab review for Phase 1 changes recommended"
  }
}
```

### 7. Risk Assessment

Assess risks associated with the improvement plan:

**Change Risks:**
- Each solution lists potential side effects
- Identify risks of introducing new issues
- Assess rework difficulty for each change

**Schedule Risks:**
- Identify dependencies between fixes
- Flag any solutions requiring expertise not available
- Note any solutions requiring external resources

**Validation Risks:**
- Identify which changes require re-simulation
- Flag changes requiring prototype re-test
- Note any changes affecting certification status

### 8. Output Structured Result

Produce comprehensive roadmap document with:
- Executive summary of improvements
- Prioritized action list with effort/impact
- Phased implementation plan
- Resource requirements
- Risk assessment
- Success metrics

## Tools
Read (input processing), Write (roadmap generation), optional WebSearch (solution verification)

## Quality Gate
- ✅ Every issue has calculated impact and effort scores
- ✅ Priority ranking is deterministic and traceable
- ✅ Solutions include specific, actionable steps
- ✅ Roadmap includes realistic effort estimates
- ✅ Risk assessment covers change, schedule, and validation risks
- ✅ All framework violations have remediation paths
- ❌ Refuse to generate roadmap if insufficient issue information

## Impact/Effort Reference Tables

### Severity Impact Weights
| Severity | Weight | Description |
|---------|--------|-------------|
| Critical | 10 | Will cause board respin or field failure |
| Major | 7 | Significant performance/reliability impact |
| Minor | 4 | Marginal performance/reliability impact |
| Info | 1 | Informational, no direct impact |

### Effort Category Definitions
| Category | Hours | Examples |
|----------|-------|----------|
| Trivial | <1 | Add test point, move label |
| Simple | 1-8 | Change trace width, add component |
| Moderate | 8-40 | Re-route nets, modify stackup |
| Significant | 40-160 | Move major components, re-plane |
| Major | 160+ | Partial board redesign |

## Application-Specific Prioritization

### Automotive (AEC-Q100)
- Safety-related functions: impact ×2
- Reliability issues: impact ×1.5
- Regulatory compliance: critical priority

### Medical (FDA/IEC 60601)
- Patient safety: impact ×3
- Essential performance: impact ×2
- Documentation requirements: mandatory

### Industrial (IEC 61010)
- Safety-related: impact ×1.5
- Reliability: impact ×1.3
- Environmental considerations: high priority

## Error Handling

If issue information is insufficient:
- Request missing severity or impact information
- Provide conservative estimates with clear disclaimers
- Flag roadmap as "preliminary" pending complete information

If effort cannot be reasonably estimated:
- Assign highest reasonable effort category
- Recommend detailed review before committing to schedule
- Flag as "effort uncertain" in roadmap

