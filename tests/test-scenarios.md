# tests/test-scenarios.md — PCB Design / Component Placement Assistant

Scenario-based regression tests for the `pcb-design-assistant` harness. Each scenario defines inputs, expected harness behavior, and validation criteria for regression testing.

## Test Format

Each scenario includes:
- **Test ID:** Unique identifier for regression tracking
- **Test Name:** Descriptive name
- **Given:** Input conditions and board description
- **Expected Behavior:** Step-by-step expected harness execution
- **Validation Criteria:** Specific pass/fail criteria
- **Regression Fixtures:** Expected data structures for comparison

---

## Scenario 1: High-Speed Clock Routing

**Test ID:** TS-001  
**Test Name:** High-Speed Clock Return-Path and Length-Matching Review

### Given
```json
{
  "board_description": "4-layer board with 100MHz oscillator routing to MCU. Clock signal is on top layer with ground plane on layer 2. Length is approximately 3 inches with multiple vias and layer transitions.",
  "layer_count": 4,
  "signal_speed": "high_speed",
  "application_type": "consumer",
  "component_list": [
    {"reference": "U1", "type": "MCU", "part_number": "STM32F407VGT6"},
    {"reference": "Y1", "type": "oscillator", "part_number": "ABM8-100MHz"}
  ],
  "net_list": [
    {"name": "CLK_100M", "type": "clock", "frequency": "100MHz", "source": "Y1", "destination": "U1-PH0"}
  ],
  "layout_details": {
    "clock_trace": {
      "layer": "Top",
      "length_inches": 3.0,
      "via_count": 3,
      "layer_transitions": ["Top->GND", "GND->Top", "Top->Bottom"]
    }
  }
}
```

### Expected Harness Behavior

**1. Intake & Framing:**
- Confirms inputs are sufficient
- Establishes scope: clock signal SI review

**2. Framework Selection:**
- Board classified as: High-Speed Digital
- Selected frameworks: IPC-2221, IPC-2152, Signal Integrity

**3. Scoring:**
- **Placement Score:** 70-80 (oscillator placement acceptable but could be closer to MCU)
- **Routing Score:** 55-65 (multiple concerns with clock routing)
- **SI Score:** 45-55 (significant return path issues)

**4. Critical Issues Identified:**
- Clock signal has 3 vias and 2 layer transitions without adjacent return vias
- Return path discontinuity at each layer transition
- No impedance control mentioned for 100MHz clock

**5. Roadmap:**
- Phase 1 critical: Add return path vias at layer transitions
- Phase 2 major: Implement impedance control, reroute to minimize vias

**6. Output Format:**
- Report includes executive summary with grade C or D
- All issues cite SI principles and IPC standards
- Roadmap prioritized by impact/effort

### Validation Criteria

**Quality Gates:**
- ✅ Evidence gate: All SI issues cite transmission line theory or reference
- ✅ Framework gate: Scoring uses Signal Integrity framework
- ✅ Challenge gate: Alternative interpretations considered

**Specific Assertions:**
- Clock via count >= 2 triggers major issue
- Layer transition without return via triggers critical issue
- Report includes reference to return path continuity principle
- Roadmap includes specific solution: return vias within 100mil of signal vias

**Expected Grade Range:** C-D (50-69)

### Regression Fixtures

**Expected Critical Issues Count:** 2-3
**Expected Major Issues Count:** 1-2

**Expected Finding Example:**
```json
{
  "issue_id": "SI-001",
  "severity": "critical",
  "framework": "Signal-Integrity",
  "issue": "Clock signal layer transition without return path via",
  "reference": "Johnson & Graham, High-Speed Digital Design, Ch. 4",
  "impact": "Return path discontinuity causes impedance discontinuity and EMI",
  "recommended_action": "Add ground return via within 100mil of each signal via"
}
```

---

## Scenario 2: Power Trace Current Capacity

**Test ID:** TS-002  
**Test Name:** IPC-2152 Power Trace Width Verification

### Given
```json
{
  "board_description": "2-layer board with 3.3V DC-DC converter supplying 3A maximum current to load. Power trace width is currently 0.8mm on 1oz copper external layer.",
  "layer_count": 2,
  "signal_speed": "low_speed",
  "application_type": "industrial",
  "power_requirements": {
    "rails": [
      {"name": "3.3V", "voltage": 3.3, "max_current": 3.0, "regulator": "U2 - LM2596"}
    ]
  },
  "layout_details": {
    "power_trace": {
      "width_mm": 0.8,
      "copper_weight": "1oz",
      "layer": "external",
      "temperature_rise_target": "10C"
    }
  }
}
```

### Expected Harness Behavior

**1. Framework Selection:**
- Board classified as: Power Electronics
- Selected frameworks: IPC-2221, IPC-2152, DFM

**2. IPC-2152 Calculation:**
- 3A on external layer, 1oz, 10°C rise
- Expected width: ~1.4mm (per IPC-2152)
- Actual width: 0.8mm (undersized)

**3. Scoring:**
- **Power Delivery Score:** 40-50 (critical undersizing)
- **DFM Score:** 70-80 (otherwise acceptable)

**4. Critical Issues:**
- Power trace undersized per IPC-2152 calculation shown
- Temperature rise will exceed 10°C at 3A
- Potential trace damage or reliability concern

**5. Roadmap:**
- Immediate: Increase trace width to 1.4mm or use 2oz copper
- Alternative: Use parallel traces or internal layer with 2oz

### Validation Criteria

**Specific Assertions:**
- IPC-2152 calculation shown explicitly
- Formula reference: I = K × A^0.725 × ΔT^0.45
- Current vs. required width comparison shown
- Temperature rise estimate provided
- Solution includes specific width recommendation

**Expected Grade Range:** C (60-69) due to critical power issue

### Regression Fixtures

**Expected IPC-2152 Calculation:**
```
Required width for 3A, 1oz, external, 10°C rise:
Width = 1.40mm (55 mils)
Actual width = 0.80mm (31 mils)
Undersized by: 43%
Estimated temperature rise at 3A: ~30°C (unacceptable)
```

**Expected Critical Issue:**
```json
{
  "issue_id": "PI-001",
  "severity": "critical",
  "framework": "IPC-2152",
  "issue": "Power trace undersized for 3A current",
  "reference": "IPC-2152A, Table 5-3, External Conductors, 10°C Rise",
  "calculated": "Width 0.8mm adequate for ~1.6A",
  "required": "Width 1.4mm required for 3A",
  "impact": "Overheating, potential trace failure"
}
```

---

## Scenario 3: Decoupling Capacitor Placement

**Test ID:** TS-003  
**Test Name:** PDN Decoupling Capacitor Proximity Analysis

### Given
```json
{
  "board_description": "6-layer board with STM32 MCU running at 168MHz. Decoupling capacitors are placed on bottom layer, approximately 250mil from MCU power pins. MCU has 4 VDD/VSS pairs.",
  "layer_count": 6,
  "signal_speed": "high_speed",
  "application_type": "industrial",
  "component_list": [
    {"reference": "U1", "type": "MCU", "part_number": "STM32F407VGT6", "power_pins": 16}
  ],
  "layout_details": {
    "decoupling_capacitors": [
      {"reference": "C1", "value": "100nF", "location": "bottom_layer", "distance_from_pins_mils": 250},
      {"reference": "C2", "value": "100nF", "location": "bottom_layer", "distance_from_pins_mils": 300},
      {"reference": "C3", "value": "10uF", "location": "bottom_layer", "distance_from_pins_mils": 400}
    ]
  }
}
```

### Expected Harness Behavior

**1. Framework Selection:**
- Board classified as: High-Speed Digital
- Selected frameworks: IPC-2221, PI, DFM

**2. Decoupling Analysis:**
- Per STM32 datasheet, 100nF caps should be within 100mil
- Current placement: 250-400mil (excessive)
- Via inductance adds to poor placement

**3. Scoring:**
- **Placement Score:** 55-65 (decoupling too far)
- **PI Score:** 50-60 (PDN compromised)

**4. Major Issues:**
- Decoupling capacitors too far from IC pins
- Via inductance exacerbates placement problem
- Insufficient number of decoupling caps (16 pins, only 2x100nF)

**5. Roadmap:**
- Move capacitors to top layer close to pins
- Increase count to at least 8x100nF (one per pin pair)
- Consider using smaller package size (0402 vs 0805)

### Validation Criteria

**Specific Assertions:**
- Cites STM32 datasheet recommendation for placement
- References PDN principles for decoupling
- Calculates via inductance impact
- Recommends specific placement distance
- Suggests capacitor count based on pin count

**Expected Grade Range:** C (65-75)

### Regression Fixtures

**Expected Datasheet Reference:**
```
STM32F407 Datasheet, Section 4.3.1:
"Decoupling capacitors must be placed as close as possible to the VDD pins.
Recommended distance: <50mm (2mil) ideal, <100mm (4mil) acceptable."
```

**Expected Issue:**
```json
{
  "issue_id": "PI-002",
  "severity": "major",
  "framework": "Power-Integrity",
  "issue": "Decoupling capacitors placed too far from IC power pins",
  "reference": "STM32F407 Datasheet DocID13587 Rev 8, Section 4.3.1",
  "current_state": "C1, C2 at 250-300mil distance",
  "recommended": "<100mil distance, top layer",
  "impact": "PDN impedance excessive at high frequency, potential instability"
}
```

---

## Scenario 4: EMC Pre-Scan Failure

**Test ID:** TS-004  
**Test Name:** EMC Emission Mitigation Recommendations

### Given
```json
{
  "board_description": "4-layer board that failed EMC pre-compliance scan. Radiated emissions exceed limits at 150MHz and harmonics. Board has 20MHz crystal oscillator routed with long traces over split ground plane.",
  "layer_count": 4,
  "signal_speed": "low_speed",
  "application_type": "consumer",
  "emc_status": {
    "test_status": "failed_pre_scan",
    "failure_frequencies_mhz": [150, 300, 450],
    "limit_exceeded_db": "5-8dB"
  },
  "layout_details": {
    "clock_signal": {
      "frequency": "20MHz",
      "trace_length_inches": 8,
      "routing_issue": "crosses ground plane split"
    }
  }
}
```

### Expected Harness Behavior

**1. Framework Selection:**
- Board classified as: General Digital with EMC concerns
- Selected frameworks: IPC-2221, EMC/EMI

**2. EMC Analysis:**
- 20MHz clock harmonics (3rd, 5th, 7th) align with failure frequencies
- Long clock trace acts as antenna
- Ground plane split exacerbates emissions

**3. Scoring:**
- **EMC/EMI Score:** 35-45 (major emission issues)
- **Routing Score:** 50-60 (long clock trace problematic)

**4. Critical Issues:**
- Clock trace routed over ground plane split
- Excessive clock trace length (8 inches)
- No shielding or filtering on clock output

**5. Roadmap:**
- Critical: Reroute clock away from plane split, shorten trace
- Critical: Add guard traces or shield can
- Major: Add series damping resistor or filter

### Validation Criteria

**Specific Assertions:**
- Identifies harmonic relationship (20MHz × 7.5 = 150MHz)
- References Henry Ott EMC principles
- Cites ground plane return path issues
- Recommends specific EMC mitigation techniques
- Calculates harmonic series for clock

**Expected Grade Range:** D (50-60) due to EMC failure

### Regression Fixtures

**Expected Harmonic Analysis:**
```
Fundamental: 20MHz
3rd harmonic: 60MHz
5th harmonic: 100MHz
7th harmonic: 140MHz
9th harmonic: 180MHz
Failure at 150MHz suggests 20MHz × 7.5 harmonic (likely from rise time harmonics)
```

**Expected Issue:**
```json
{
  "issue_id": "EMC-001",
  "severity": "critical",
  "framework": "EMC-EMI",
  "issue": "Clock trace routed over ground plane discontinuity",
  "reference": "Henry Ott, Electromagnetic Compatibility Engineering, Ch. 6",
  "mechanism": "Return path forced around split creates large loop area → increased emissions",
  "frequencies_affected": "150MHz, 300MHz, 450MHz harmonics",
  "recommended_action": "Reroute clock over continuous ground plane, shorten to <2 inches"
}
```

---

## Scenario 5: Datasheet Constraint Extraction

**Test ID:** TS-005  
**Test Name:** Component Datasheet Thermal and Derating Analysis

### Given
```json
{
  "board_description": "4-layer automotive board with DC-DC converter supplying 5V at 2A. Component is rated for 3A absolute maximum, operates at 85°C ambient temperature.",
  "layer_count": 4,
  "signal_speed": "low_speed",
  "application_type": "automotive",
  "component_list": [
    {
      "reference": "U5",
      "type": "DC-DC",
      "manufacturer": "Texas Instruments",
      "part_number": "LM2596S-ADJ"
    }
  ],
  "power_requirements": {
    "rails": [
      {"name": "5V", "voltage": 5, "max_current": 2.0, "regulator": "U5"}
    ]
  },
  "operating_conditions": {
    "ambient_temperature_c": 85,
    "automotive_standard": "AEC-Q100"
  }
}
```

### Expected Harness Behavior

**1. Framework Selection:**
- Board classified as: Power Electronics, Automotive
- Selected frameworks: IPC-2221, IPC-2152, DFM, Thermal Management

**2. Datasheet Processing:**
- Fetch LM2596 datasheet from TI website
- Extract absolute maximum ratings: 3A switch current, 125°C Tj max
- Extract thermal resistance: θJA ~45°C/W (TO-263)

**3. Derating Analysis:**
- Automotive derating: 75% for current, 85% for temperature
- Derated maximum: 3A × 0.75 = 2.25A
- Operating current: 2.0A (within derated limit but marginal)

**4. Thermal Analysis:**
- Power dissipation: P = V_in × I_in - V_out × I_out ≈ 2W
- Junction temp: Tj = 85°C + (2W × 45°C/W) = 175°C
- Tj exceeds maximum (125°C)

**5. Critical Issues:**
- Junction temperature exceeds maximum under operating conditions
- Derated current margin insufficient (2.25A vs 2.0A = 12.5% margin)
- Insufficient heatsinking or thermal relief

**6. Roadmap:**
- Critical: Add heatsink or improve thermal pad connection
- Major: Reduce ambient temperature or power dissipation
- Consider automotive-grade alternative with better thermal characteristics

### Validation Criteria

**Specific Assertions:**
- Datasheet reference includes manufacturer, part number, revision
- Thermal calculation shown explicitly
- Automotive derating factors applied correctly
- Cites AEC-Q100 derating guidelines
- Recommends specific thermal improvements

**Expected Grade Range:** D (50-60) due to thermal violation

### Regression Fixtures

**Expected Datasheet Extract:**
```json
{
  "component": "LM2596S-ADJ",
  "manufacturer": "Texas Instruments",
  "datasheet": "SNVS087E, October 2015, Revised January 2022",
  "absolute_maximums": {
    "switch_current": "3.0A",
    "junction_temperature": "125°C",
    "thermal_resistance": "θJA = 45°C/W (TO-263)"
  }
}
```

**Expected Thermal Calculation:**
```
Power Dissipation:
P_in = 12V × 0.9A = 10.8W
P_out = 5V × 2.0A = 10.0W
P_dissipated = 10.8W - 10.0W = 0.8W (switching losses ≈ 1.2W additional)
Total P ≈ 2.0W

Junction Temperature:
Tj = Ta + (P × θJA) = 85°C + (2.0W × 45°C/W) = 175°C
Status: EXCEEDS MAXIMUM (125°C)
```

**Expected Issue:**
```json
{
  "issue_id": "THERM-001",
  "severity": "critical",
  "framework": "Thermal-Management",
  "issue": "Junction temperature exceeds absolute maximum under operating conditions",
  "reference": "LM2596 Datasheet, SNVS087E, Table 7.1; AEC-Q100 derating guidelines",
  "calculated_tj": "175°C",
  "maximum_tj": "125°C (derated: 106°C for automotive 85% of Tj)",
  "recommended": "Add heatsink (target θJA <15°C/W), reduce ambient, or select alternative device"
}
```

---

## Scenario 6: DFM Footprint Mismatch

**Test ID:** TS-006  
**Test Name:** IPC-7351 Footprint and Assembly Defect Prevention

### Given
```json
{
  "board_description": "Production board with 0805 capacitor footprints that are slightly undersized. Manufacturer reports component placement issues and solder joint defects during assembly.",
  "layer_count": 4,
  "signal_speed": "low_speed",
  "application_type": "consumer",
  "assembly_status": {
    "status": "production_issues",
    "defect_rate": "3-5%",
    "issue_type": "solder_joint_insufficient"
  },
  "component_list": [
    {
      "reference": "C10-C100",
      "package": "0805",
      "footprint_source": "custom"
    }
  ],
  "layout_details": {
    "footprint_dimensions": {
      "pad_width_mil": "45",
      "pad_length_mil": "55",
      "pad_spacing_mil": "45"
    }
  }
}
```

### Expected Harness Behavior

**1. Framework Selection:**
- Board classified as: General Digital, Production
- Selected frameworks: IPC-2221, IPC-7351, DFM

**2. Footprint Analysis:**
- IPC-7351 0805 footprint specification:
  - Land pattern name: CAPC2012X95N (0805)
  - Pad width: 50mil (1.27mm)
  - Pad length: 60mil (1.52mm)
  - Toe/heel/side fillet requirements

**3. Comparison:**
- Custom footprint: 45mil × 55mil
- IPC-7351 recommendation: 50mil × 60mil
- Under-sized by 10-15%

**4. Scoring:**
- **DFM Score:** 55-65 (footprint non-compliant)
- **Placement Score:** 70-80 (otherwise acceptable)

**5. Major Issues:**
- Footprint does not follow IPC-7351 standard
- Undersized pads cause insufficient solder joints
- 3-5% assembly defect rate consistent with undersized pads

**6. Roadmap:**
- Major: Update footprint to IPC-7351 specification
- Immediate for next revision: Change to standard footprint
- For current production: Work with assembler on process window adjustments

### Validation Criteria

**Specific Assertions:**
- Cites IPC-7351 standard and revision
- Provides specific land pattern name (CAPC2012X95N)
- Calculates pad size difference percentage
- References solder joint fillet requirements
- Relates footprint to reported assembly defects

**Expected Grade Range:** C (65-75) due to DFM issues

### Regression Fixtures

**Expected IPC-7351 Reference:**
```
Component: 0805 capacitor (metric 2012)
IPC-7351 Land Pattern: CAPC2012X95N
Dimensions:
- Pad Width (X): 1.27mm (50mil)
- Pad Length (Y): 1.52mm (60mil)
- Toe Extension: 0.25mm (10mil)
- Heel Extension: 0.25mm (10mil)
- Side Extension: 0.10mm (4mil)
```

**Expected Comparison:**
```
Current Custom Footprint:
- Pad Width: 45mil (10% undersized)
- Pad Length: 55mil (8% undersized)

IPC-7351 Standard:
- Pad Width: 50mil
- Pad Length: 60mil

Impact: Insufficient solder volume leads to weak joints, tombstoning risk
```

**Expected Issue:**
```json
{
  "issue_id": "DFM-001",
  "severity": "major",
  "framework": "IPC-7351",
  "issue": "Component footprint does not conform to IPC-7351 standard",
  "reference": "IPC-7351B, Section 5, Land Pattern Design",
  "current_footprint": "45mil × 55mil custom",
  "recommended": "50mil × 60mil per IPC-7351 CAPC2012X95N",
  "impact": "3-5% assembly defect rate due to insufficient solder joints",
  "recommended_action": "Update footprint to IPC-7351 standard for next revision"
}
```

---

## Cross-Cutting Validation

### Graceful Degradation Test

**Scenario:** WebSearch/WebFetch disabled during harness execution

**Expected Behavior:**
- Harness completes with existing knowledge base
- Report includes limitation statement: "Knowledge base not refreshed due to offline mode"
- Confidence level set to "medium" or lower
- No failure or crash
- Report still includes all required sections

**Validation:**
- ✅ Harness executes successfully
- ✅ Limitation clearly stated
- ✅ All framework citations still work (from SECOND-KNOWLEDGE-BRAIN.md)
- ✅ Quality gates still pass with existing knowledge

### Out-of-Scope Refusal Test

**Scenario:** User requests complete board design from scratch

**Expected Behavior:**
- Harness politely explains this is outside scope
- Redirects to design resources
- Offers to review design once layout is available
- Does not attempt to generate full design

**Validation:**
- ✅ Refusal is polite and helpful
- ✅ Scope boundaries clearly explained
- ✅ Alternative resources suggested
- ✅ Offer to help with in-scope tasks

### Determinism Test

**Scenario:** Run same inputs multiple times

**Expected Behavior:**
- Same scores produced each run
- Same grade assigned
- Same critical issues identified
- Same roadmap structure

**Validation:**
- ✅ Scoring is deterministic
- ✅ No random elements in evaluation
- ✅ Framework application is consistent

---

## Test Execution Protocol

### Running Tests

For each scenario:
1. Provide input JSON to harness
2. Capture full output report
3. Extract scoring, issues, and roadmap
4. Compare against expected validation criteria
5. Verify quality gates passed
6. Check output format compliance

### Regression Detection

Track these metrics across runs:
- Grade variance (should be 0 for same inputs)
- Issue count variance
- Critical issue detection consistency
- Framework citation completeness

### Batch Testing

Run all scenarios in sequence to verify:
- Harness handles diverse board types
- Framework selection works for all classifications
- All quality gates pass consistently
- Output format is stable

### Test Maintenance

When adding features:
- Add new scenario covering the feature
- Update expected validation criteria
- Ensure cross-cutting tests still pass
- Document any new framework citations

---

## Test Summary Matrix

| Test ID | Board Type | Primary Frameworks | Expected Grade | Key Issues |
|---------|------------|-------------------|----------------|------------|
| TS-001 | High-Speed Digital | SI, IPC-2221 | C-D | Return path, length matching |
| TS-002 | Power Electronics | IPC-2152, DFM | C | Trace width undersized |
| TS-003 | High-Speed Industrial | PI, DFM | C | Decoupling placement |
| TS-004 | Consumer EMC | EMC/EMI, IPC-2221 | D | Ground plane, clock routing |
| TS-005 | Automotive Power | Thermal, Derating | D | Junction temperature |
| TS-006 | Consumer DFM | IPC-7351, DFM | C | Footprint non-compliance |

---

**End of test-scenarios.md**
