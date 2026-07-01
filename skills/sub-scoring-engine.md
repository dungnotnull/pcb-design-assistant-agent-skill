---
name: sub-scoring-engine
description: Score placement, routing, power delivery, and DFM against the rules; produce a layout quality grade.
---

## Role
Sub-skill of `pcb-design-assistant`. Score placement, routing, power delivery, and DFM against the rules; produce a comprehensive layout quality grade with evidence citations.

## Inputs
- **classification_result** (object, required): Output from `sub-evaluation-framework-selector`
- **board_description** (string, required): User-provided description of the PCB layout
- **component_list** (array, optional): List of components with types and footprints
- **net_list** (array, optional): List of critical nets with characteristics
- **power_requirements** (object, optional): Power rail specifications (voltage, current, tolerance)
- **layout_details** (object, optional): Specific layout information (trace widths, spacing, layer stackup)

## Procedure

### 1. Validate Inputs
- `classification_result` must contain valid board classification and frameworks
- `board_description` must be non-empty
- If critical inputs are missing, request them from the user

### 2. Multi-Dimensional Scoring

For each applicable framework from classification_result, score the implementation.

#### 2.1 Placement Scoring (0-100 points)

**Criteria from IPC-2221 and design best practices:**
- Component orientation consistency (10 pts)
- Placement flow (signal flow logic) (15 pts)
- Decoupling capacitor proximity (15 pts)
- Thermal management (15 pts)
- Test point access (10 pts)
- Assembly considerations (15 pts)
- Keep-out zone adherence (20 pts)

**Scoring Logic:**
- 90-100: Excellent placement, follows best practices
- 75-89: Good placement with minor issues
- 60-74: Adequate placement with notable concerns
- 40-59: Poor placement with significant issues
- <40: Critical placement problems

**Evidence Required:** Cite IPC-2221 section, design guideline, or industry reference for each deduction.

#### 2.2 Routing Scoring (0-100 points)

**Criteria from IPC-2221/IPC-2152 and SI principles:**
- Trace width adequacy for current (20 pts) - IPC-2152
- Trace spacing per voltage class (15 pts) - IPC-2221
- Via usage and count (15 pts)
- Layer transitions and return paths (15 pts) - SI principles
- Acute angle avoidance (10 pts)
- Differential pair matching (15 pts) - if applicable
- Critical net routing priority (10 pts)

**IPC-2152 Current Capacity Reference:**
- Use IPC-2152 formulas or charts to verify trace widths
- Account for temperature rise, copper weight, board thickness
- Score deduction for undersized traces with calculation evidence

**Evidence Required:** Specific IPC standard reference with section/paragraph.

#### 2.3 Power Delivery Scoring (0-100 points)

**Criteria from IPC-2152 and PI principles:**
- Power trace width adequacy (25 pts) - IPC-2152
- Power plane integrity (15 pts)
- Decoupling capacitor placement (20 pts) - PDN principles
- Decoupling capacitor quantity (15 pts) - device requirements
- PDN impedance considerations (15 pts)
- Ground return path quality (10 pts)

**Decoupling Scoring Logic:**
- Check capacitor placement distance from IC pins (<100mm ideal)
- Verify capacitor values match device requirements
- Score multiple capacitors per rail for frequency range coverage

**Evidence Required:** IPC-2152 calculations, device datasheet references.

#### 2.4 Signal Integrity Scoring (0-100 points)

**Criteria for high-speed and RF designs:**
- Controlled impedance implementation (25 pts)
- Return path continuity (20 pts)
- Length matching for matched groups (20 pts)
- Via stub management (10 pts)
- Reference plane integrity (15 pts)
- Termination implementation (10 pts)

**Impedance Control Reference:**
- Single-ended: 50Ω (common), 75Ω (video)
- Differential: 100Ω (common), 90Ω (USB)

**Evidence Required:** Industry SI references, transmission line theory.

#### 2.5 EMC/EMI Scoring (0-100 points)

**Criteria from EMC design practices:**
- Ground plane completeness (20 pts)
- Guard trace implementation (15 pts)
- Slot avoidance in ground planes (15 pts)
- Filtering and shielding (15 pts)
- Signal edge rate management (15 pts)
- Loop area minimization (20 pts)

**EMC Reference Frameworks:**
- Henry Ott "Electromagnetic Compatibility Engineering"
- IEC 61000-4-x series
- FCC Part 15 (if applicable)

#### 2.6 DFM Scoring (0-100 points)

**Criteria from IPC-A-600 and DFM guidelines:**
- Minimum feature size compliance (15 pts) - IPC-A-600
- Solder mask design (10 pts)
- Silkscreen clarity (10 pts)
- Panelization efficiency (15 pts)
- Tooling strip inclusion (10 pts)
- Fiducial placement (10 pts)
- Copper pour clearance (15 pts)
- Manufacturing tolerance considerations (15 pts)

### 3. Aggregate Scoring

Calculate overall board quality grade:
- Weight dimensions by classification priorities
- RF/Mixed-signal: SI weight 1.5x, EMC weight 1.5x
- Power electronics: Power weight 1.5x, Thermal weight 1.3x
- High-speed digital: SI weight 1.5x, PI weight 1.3x

**Grade Calculation:**
```
Overall Score = Σ(Dimension Score × Weight) / Σ(Weights)
Grade = Overall Score mapped to letter grade:
  A: 90-100
  B: 80-89
  C: 70-79
  D: 60-69
  F: <60
```

### 4. Findings Generation

For each dimension:
- Identify strengths (what's done well)
- Identify risks (potential issues)
- Identify gaps (missing elements)

Each finding must include:
- Severity level (critical, major, minor, info)
- Framework reference
- Specific evidence or calculation
- Recommended action

### 5. Output Structured Result

```json
{
  "dimension_scores": {
    "placement": {"score": 85, "weight": 1.0, "findings": [...]},
    "routing": {"score": 72, "weight": 1.0, "findings": [...]},
    "power_delivery": {"score": 88, "weight": 1.3, "findings": [...]},
    "signal_integrity": {"score": 65, "weight": 1.5, "findings": [...]},
    "emc_emi": {"score": 70, "weight": 1.5, "findings": [...]},
    "dfm": {"score": 82, "weight": 1.0, "findings": [...]}
  },
  "overall_quality": {
    "score": 76.8,
    "grade": "C",
    "confidence": "medium"
  },
  "critical_issues": [
    {
      "dimension": "signal_integrity",
      "issue": "Differential pair length mismatch exceeds tolerance",
      "severity": "major",
      "framework": "Signal-Integrity",
      "evidence": "Length mismatch: 120mm, tolerance: ±5mm (0.5% of 10mm pair length)",
      "reference": "IEC 61188-5-1 Section 5.4.2"
    }
  ],
  "strengths": [
    "Power delivery well implemented with adequate trace sizing per IPC-2152",
    "DFM considerations strong with good manufacturability features"
  ],
  "risks": [
    "Signal integrity issues may cause data errors at high frequency",
    "EMC concerns may result in emissions test failures"
  ]
}
```

## Tools
WebSearch (for standard verification), Read (for knowledge base), Write (for output)

## Quality Gate
- ✅ All scoring dimensions have evidence citations
- ✅ Every score maps to a named framework
- ✅ Critical issues have explicit framework references
- ✅ Overall grade calculation is deterministic and traceable
- ✅ No ad-hoc scoring criteria
- ❌ Refuse to score if insufficient information for critical dimensions

## Scoring Reference Tables

### IPC-2152 Trace Width Quick Reference (External Layers, 10°C Rise)
| Current (A) | 1oz (35µm) | 2oz (70µm) |
|-------------|------------|------------|
| 1           | 0.30mm     | 0.20mm     |
| 2           | 0.80mm     | 0.50mm     |
| 3           | 1.40mm     | 0.90mm     |
| 5           | 2.80mm     | 1.80mm     |
| 10          | 7.00mm     | 4.50mm     |

### Minimum Trace Spacing per IPC-2221
| Voltage | Internal (mm) | External (mm) |
|---------|---------------|---------------|
| 0-50V   | 0.15          | 0.15          |
| 51-100V | 0.20          | 0.25          |
| 101-150V| 0.30          | 0.40          |

## Error Handling
If critical information is missing:
- Request specific layout details needed for scoring
- Provide partial scoring with clear confidence disclaimers
- State which dimensions could not be evaluated and why

