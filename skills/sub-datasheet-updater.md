---
name: sub-datasheet-updater
description: Ingest component datasheets and IPC revisions to refine constraints (footprints, derating, thermal).
---

## Role
Sub-skill of `pcb-design-assistant`. Ingest component datasheets and IPC revisions to refine design constraints including footprints, derating factors, thermal limits, and electrical parameters.

## Inputs
- **scoring_result** (object, required): Output from `sub-scoring-engine`
- **datasheet_references** (array, optional): URLs or file references to component datasheets
- **component_list** (array, optional): List of critical components with manufacturer and part numbers
- **ipc_revision_level** (string, optional): Specific IPC revision to target (e.g., "IPC-2221B", "IPC-2152A")
- **additional_constraints** (object, optional): Any additional design constraints provided

## Procedure

### 1. Validate Inputs
- Verify scoring result is valid and contains dimension scores
- If datasheets provided, verify URLs are accessible or files exist
- If component list provided, verify manufacturer/pn format is valid

### 2. Datasheet Processing Pipeline

#### 2.1 Datasheet Acquisition and Parsing
For each component in the component list:

1. **Locate Datasheet:**
   - Use WebSearch to find official manufacturer datasheet
   - Prefer manufacturer website over distributor sites
   - Verify document authenticity

2. **Extract Key Parameters:**
   - **Electrical Parameters:**
     - Absolute maximum ratings (voltage, current, power)
     - Recommended operating conditions
     - Input/output characteristics
     - Timing parameters (for digital ICs)
   
   - **Thermal Parameters:**
     - Junction temperature limits (Tj max)
     - Thermal resistance (θJA, θJC)
     - Power dissipation limits
     - Derating curves if provided
   
   - **Package Information:**
     - Package type and dimensions
     - Footprint specifications
     - Land pattern recommendations
     - Thermal pad requirements
   
   - **Layout Recommendations:**
     - PCB layout guidelines
     - Bypass capacitor recommendations
     - Thermal pad connections
     - Via recommendations for thermal pads

3. **Parse and Structure Data:**
   - Extract numeric values with units
   - Identify test conditions for parameters
   - Capture application-specific recommendations

#### 2.2 Derating Analysis

Based on application type from classification, apply derating factors:

**Standard Derating Guidelines (per NASA, MIL-STD, industry practices):**

| Parameter | Commercial | Automotive | Industrial | Aerospace/Medical |
|-----------|------------|------------|------------|-------------------|
| Voltage    | 80%        | 75%        | 70%        | 60%                |
| Current    | 80%        | 75%        | 70%        | 60%                |
| Power      | 80%        | 70%        | 65%        | 50%                |
| Temperature| 90% of Tj  | 85% of Tj  | 80% of Tj  | 70% of Tj          |

**Derating Calculation:**
```
Maximum Allowed = Absolute Maximum × Derating Factor
If Design Value > Maximum Allowed: Flag as critical issue
```

### 3. IPC Revision Analysis

#### 3.1 Current IPC Standards Verification

Verify which IPC revision versions are current and relevant:
- **IPC-2221:** Generic Standard on Printed Board Design
- **IPC-2152:** Standard for Determining Current-Carrying Capacity
- **IPC-A-600:** Acceptability of Printed Boards
- **IPC-6012:** Qualification and Performance Specification for Rigid Printed Boards
- **IPC-7351:** Generic Requirements for Surface Mount Design and Land Pattern Standards

For each applicable standard:
1. Check current revision level via WebSearch if needed
2. Identify changes from previous revisions affecting this design
3. Extract specific requirements relevant to the board classification
4. Update constraint thresholds accordingly

#### 3.2 Constraint Refinement

Update scoring constraints based on latest IPC revisions:

**IPC-2152 Specific Updates:**
- Trace width formulas for modern board constructions
- Via current capacity considerations
- Multiple trace bundle corrections

**IPC-2221B Updates:**
- Updated spacing requirements for high-voltage applications
- New microvia rules for HDI designs
- Updated solder mask and silkscreen requirements

### 4. Constraint Database Update

Maintain structured constraint database for the review:

```json
{
  "component_constraints": [
    {
      "component": "U1 - MCU",
      "manufacturer": "STMicroelectronics",
      "part_number": "STM32F407VGT6",
      "datasheet_version": "DocID13587 Rev 8",
      "absolute_maximums": {
        "voltage_dd": "4.0V",
        "input_voltage": "5.5V",
        "total_current": "150mA"
      },
      "thermal_limits": {
        "tj_max": "125°C",
        "theta_ja": "38°C/W",
        "theta_jc": "7°C/W"
      },
      "derated_maximums": {
        "voltage_dd": "3.0V (automotive 75%)",
        "power_dissipation": "0.6W (automotive 70%)"
      },
      "layout_recommendations": {
        "decoupling": "100nF × 2 per VDD pair, 10uF bulk",
        "thermal_pad": "Connect to ground plane with 4-8 vias",
        "recommended_footprint": "LQFP100, IPC-7351 LAND PATERN NAME"
      }
    }
  ],
  "ipc_constraints": {
    "ipc_2221": {
      "revision": "B",
      "applied_sections": ["5.2.1", "6.3", "9.2"],
      "trace_spacing_minimum": "0.15mm for 0-50V external",
      "via_aspect_ratio": "Maximum 8:1 for standard fabrication"
    },
    "ipc_2152": {
      "revision": "A", 
      "trace_width_for_3a": "1.40mm for 1oz, 10°C rise",
      "correction_factors": "Applied: board thickness, copper weight"
    }
  },
  "application_specific_constraints": {
    "derating_standard": "Automotive (AEC-Q100)",
    "temperature_range": "-40°C to +85°C",
    "vibration_requirements": "Per IEC 60068-2-6",
    "additional_tests": "Required: 100% HTOL, HAST per AEC-Q100"
  }
}
```

### 5. Scoring Refinement

Update the scoring result with refined constraints:

1. **Re-evaluate critical dimensions** with new constraints:
   - Power delivery scoring updated with datasheet-verified current limits
   - Thermal scoring updated with component Tj limits
   - DFM scoring updated with footprint-verified land patterns

2. **Flag constraint violations:**
   - Any design parameter exceeding derated maximums
   - Layout deviations from datasheet recommendations
   - IPC standard violations based on latest revision

3. **Generate specific findings:**
   - Each constraint violation gets a specific finding with:
     - Datasheet or IPC reference
     - Calculated vs. allowed values
     - Recommended corrective action

### 6. Output Structured Result

```json
{
  "constraint_updates": {
    "components_processed": 12,
    "ipc_revisions_checked": ["IPC-2221B", "IPC-2152A"],
    "derating_standard_applied": "Automotive"
  },
  "refined_scoring": {
    "original_power_score": 88,
    "refined_power_score": 76,
    "adjustment_reason": "Datasheet current limits tighter than generic assumptions"
  },
  "new_critical_issues": [
    {
      "component": "U5 - DC-DC Converter",
      "issue": "Switch current exceeds datasheet derated limit",
      "calculated": "2.8A peak",
      "allowed": "2.5A (75% of 3.3A absolute max)",
      "reference": "Texas Instruments LM2596 datasheet, Table 7.1",
      "severity": "critical"
    }
  ],
  "layout_recommendations_refined": [
    "Add thermal relief pads per IPC-7351 for all through-hole components",
    "Increase decoupling to 2×100nF per VDD pin per STM32 datasheet section 4.3.1",
    "Connect EPAD to GND plane with minimum 8 vias (0.3mm diameter)"
  ],
  "datasheet_sources": [
    {"component": "STM32F407VGT6", "url": "https://www.st.com/resource/en/datasheet/stm32f407vg.pdf", "accessed": "2026-07-01"},
    {"component": "LM2596S-ADJ", "url": "https://www.ti.com/lit/ds/symlink/lm2596.pdf", "accessed": "2026-07-01"}
  ]
}
```

## Tools
WebSearch (datasheet location, standard verification), WebFetch (datasheet retrieval), Read (knowledge base), Write (output generation)

## Quality Gate
- ✅ All datasheet references verified and accessible
- ✅ Extracted parameters include units and test conditions
- ✅ Derating factors match application type
- ✅ IPC revision references are current and specific
- ✅ Each constraint cites its source document and section
- ✅ Refined scoring shows before/after comparison
- ❌ Refuse to apply constraints if datasheet cannot be verified

## Component Priority Levels

Process components in priority order:
1. **Critical:** Power management ICs, processors, FPGAs, high-current devices
2. **High:** Memory, interface ICs, sensors
3. **Medium:** Passive components (if high-voltage or high-power)
4. **Low:** Standard passives (processed generically)

## Datasheet Extraction Templates

### Power IC Template
```
Priority Parameters:
- Input voltage range
- Output current capability  
- Switching frequency
- Thermal pad requirements
- Layout recommendations (input capacitor proximity, trace sizing)
- Component placement requirements
```

### Digital IC Template
```
Priority Parameters:
- Supply voltage tolerance
- I/O voltage levels
- Power sequencing requirements
- Decoupling requirements (quantity, placement, values)
- Thermal specifications
- Pin-specific layout requirements
```

### Passive Component Template (High-Power/High-Voltage)
```
Priority Parameters:
- Voltage rating
- Current/power rating
- Derating curves
- Physical size/tolerance
- PCB footprint considerations
```

## Error Handling

If datasheet cannot be found or accessed:
- Flag component as "datasheet not verified" in output
- Apply conservative generic constraints
- Recommend manual datasheet review
- Do not proceed without explicit acknowledgment if component is critical

If IPC revision cannot be verified:
- Use most conservative interpretation of requirements
- Flag in output with "IPC revision not verified" note
- Recommend verification before production

