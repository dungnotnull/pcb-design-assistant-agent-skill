# SECOND-KNOWLEDGE-BRAIN.md — PCB Design / Component Placement Assistant

> Self-improving domain knowledge base for the `pcb-design-assistant` skill. Grown continuously by `tools/knowledge_updater.py`.

## Core Concepts & Frameworks

### IPC Standards Foundation

#### IPC-2221: Generic Standard on Printed Board Design
**Purpose:** Establishes generic requirements for the design of printed boards and other forms of component mounting or interconnecting structures.

**Current Revision:** IPC-2221B (as of 2024)

**Key Sections:**
- **Section 5:** Conductive Material Requirements
  - 5.2: Conductor Spacing Based on Voltage
  - 5.3: Conductor Width Based on Current Capacity
- **Section 6:** Dielectric Requirements
  - 6.2: Material Properties
  - 6.3: Dielectric Thickness
- **Section 9:** Solder Mask and Silkscreen
- **Section 10:** Test Point Requirements

**Application:** Applies to all rigid printed boards, regardless of technology.

#### IPC-2152: Standard for Determining Current-Carrying Capacity
**Purpose:** Provides standard methods for determining current-carrying capacity of conductors on printed boards.

**Current Revision:** IPC-2152A (as of 2024)

**Key Parameters:**
- External vs. internal conductors
- Copper thickness (0.5oz to 10oz)
- Temperature rise (10°C to 100°C)
- Board thickness effect
- Parallel conductor correction factors

**Formula Reference:**
I = K × A^0.725 × ΔT^0.45
Where: I=current (A), A=cross-sectional area (mils²), ΔT=temperature rise (°C)

#### IPC-A-600: Acceptability of Printed Boards
**Purpose:** Visual quality criteria for acceptability of printed boards.

**Current Revision:** IPC-A-600H (as of 2024)

**Key Sections:**
- **Section 2:** External Visual Inspection
- **Section 3:** Internal Visual Inspection (for microsections)
- **Section 4:** Measurement and Test

**Defect Classes:**
- Class 1: General Electronic Products (consumer)
- Class 2: Dedicated Service Electronic Products (industrial, telecom)
- Class 3: High Reliability Electronic Products (medical, aerospace, military)

### Signal Integrity Framework

#### Controlled Impedance Design

**Target Impedances:**
- Single-ended: 50Ω (most common), 75Ω (video, some RF)
- Differential: 100Ω (common), 90Ω (USB), 85Ω (PCIe)

**Impedance Calculation (Microstrip):**
Z0 = (87/√(εr+1.41)) × ln(5.98h/(0.8w+t))

**Impedance Calculation (Stripline):**
Z0 = (60/√εr) × ln(4b/(0.67π(w+t)(0.8+ t/b)))

Where: εr=dielectric constant, h=height, w=trace width, t=trace thickness, b=dielectric thickness

**Tolerance:**
- Standard: ±10%
- High-speed (DDR, SerDes): ±5%
- Very high-speed: ±3% or tighter

#### Return Path Continuity

**Principle:** High-frequency return current follows path of least impedance (closest reference plane).

**Critical Rules:**
- Never route over split planes
- Maintain continuous reference under high-speed traces
- Use stitching vias near layer transitions
- Keep return paths short and direct

**Layer Transition Guidance:**
- Provide return path via adjacent ground plane via
- Place transition via within 100mil of signal via
- Minimize loop area formed by return path

#### Length Matching

**Requirements:**
- DDR3/4: ±25mil (within byte lane), ±500mil (between lanes)
- PCIe: ±5mil within pair, ±200mil between pairs
- USB: ±150mil within pair
- Differential pairs generally: ±5-10mil within pair

**Matching Methods:**
- Serpentines (tuning patterns)
- Preferred inside layer (better SI, but adds loss)
- Match from source to load (including package length)

### Power Integrity Framework

#### PDN Target Impedance

**Formula:**
Z_target = ΔV / ΔI

**Common Targets:**
- Digital ICs: 5-50mΩ (depending on data rate and simultaneity)
- FPGAs: 1-10mΩ
- Memory (DDR): 10-50mΩ

**Frequency Range of Interest:**
- DC to 100MHz for most digital ICs
- Up to 1GHz for very high-speed devices

#### Decoupling Capacitor Strategy

**Placement Hierarchy:**
1. **Bulk Capacitors (10-100µF):**
   - Near power entry
   - Supplies low-frequency decoupling
   - One per board or major power section

2. **Mid-frequency (0.1-1µF):**
   - Distributed across IC power pins
   - Supplies mid-range frequencies
   - Typical: 1-3 per IC or power rail section

3. **High-frequency (0.01-0.1µF):**
   - Closest to IC pins
   - Supplies high-frequency transients
   - One per power pin pair or every 2-3 pins

**Placement Guidelines:**
- Place on same layer as component if possible
- Within 100mil (2.54mm) of IC pin ideal
- Via in, via out pattern for multi-layer
- Minimize loop area between capacitor, via, and IC pin

**Via Inductance (L_via ≈ 1nH per mm):**
L = 5.08h [ln(4h/d) + 1] × 10^-9 Henries

Where: h=via length (mils), d=via diameter (mils)

### EMC/EMI Framework

#### Emission Sources

**Differential Mode:**
- Signal currents flowing out and back
- Proportional to signal current and loop area
- Reduced by minimizing loop area

**Common Mode:**
- Currents flowing in same direction on all conductors
- Proportional to cable/trace length above ground
- Reduced by proper grounding and shielding

#### Control Techniques

**Ground Plane Design:**
- Continuous, unbroken ground plane on adjacent layer
- No slots or splits under high-speed traces
- Ground plane stitching at regular intervals (<λ/10)

**Guard Traces:**
- Grounded traces on either side of critical signals
- Provide return path containment
- Effective for sensitive analog or high-speed clocks

**Filtering:**
- Power supply inputs: π-filter (C-L-C) or ferrite beads
- Interface cables: common-mode chokes
- Connectors: EMI filter arrays

**Shielding Considerations:**
- Shield cans for high-noise or high-sensitivity circuits
- PCB edge shielding: ground fill with vias
- Connector shield connection to chassis ground

**Reference:** Henry Ott, "Electromagnetic Compatibility Engineering"
- Chapter 6: Emission Control
- Chapter 7: Susceptibility Reduction

### DFM Framework

#### Minimum Feature Sizes

**Trace Width/Spacing:**
- Standard (most fabs): 6mil/6mil (0.15mm/0.15mm)
- Advanced: 4mil/4mil (0.1mm/0.1mm)
- HDI: 3mil/3mil (0.075mm/0.075mm)

**Via Sizes:**
- Standard through-hole: 12-24mm drill, 23-35mm pad
- Microvia (laser): 3-6mm drill, 8-12mm pad
**Via Aspect Ratio:**
- Standard fabrication: ≤8:1 (drill depth / drill diameter)
- Advanced: ≤10:1 with special process

**Solder Mask:**
- Minimum web between pads: 4mil (0.1mm)
- Clearance from non-soldermask defined pads: 3-4mil (0.075-0.1mm)

#### Panelization Considerations

**Rails:** 10-15mm (0.4-0.6") on opposite sides
**Tooling holes:** 2-4 non-plated holes, 1.5-3mm diameter
**Fiducials:** 1-3 per panel, 1mm round, copper with solder mask opening
**Breakout tabs:** 2-3mm wide, spacing determined by board thickness
**Scoring depth:** 1/3 thickness typical for V-score

**Reference:** IPC-7351, Generic Requirements for Surface Mount Design and Land Pattern Standards

### Thermal Management

#### Component Derating Guidelines

**Standard Derating:**
| Parameter | Commercial | Automotive | Industrial | Aerospace |
|-----------|------------|------------|------------|-----------|
| Voltage    | 80%        | 75%        | 70%        | 60%        |
| Current    | 80%        | 75%        | 70%        | 60%        |
| Power      | 80%        | 70%        | 65%        | 50%        |
| Temperature| 90% of Tj  | 85% of Tj  | 80% of Tj  | 70% of Tj  |

**Junction Temperature Calculation:**
Tj = Ta + (P × θJA)

Where: Tj=junction temp, Ta=ambient temp, P=power dissipation, θJA=thermal resistance junction-to-ambient

#### Thermal Relief Pads

**Purpose:** Prevent heat sinking during soldering while maintaining electrical connection.

**Design:**
- 4-spoke typical for through-hole
- Spoke width: 10-20mil (0.25-0.5mm)
- Thermal relief for ground planes: 4 spokes minimum
- For high-current: use direct connection, no relief

## Key Research Papers

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|----------|-----------|
| Effects of Return Path Discontinuity on Signal Integrity | Johnson, Graham | 1993 | IEEE EMC Symposium | 10.1109/ISEMC.1993.285326 | Foundational return path analysis |
| Power Distribution Network Design for High-Speed Digital Systems | Bogatin, et al. | 2002 | DesignCon | N/A | PDN design methodology |
| Decoupling Capacitor Placement Optimization | Smith, Bogatin | 2005 | DesignCon | N/A | Capacitor placement guidelines |
| Via Inductance and its Impact on PDN | Novak, Istvan | 2007 | DesignCon | N/A | Via modeling for PDN |
| Differential Pair Routing and Length Matching | Hall, Heck | 2011 | IEEE EMC | 10.1109/ISEMC.2011.6068493 | Length matching tolerances |
| Ground Plane Slot Effects on Signal Integrity | Oh, et al. | 2015 | IEEE Transactions on EMC | 10.1109/TEMC.2015.2433973 | Return path discontinuity |
| High-Speed PCB Material Selection | Ritchey, et al. | 2018 | DesignCon | N/A | Dielectric material properties |
| IPC-2152 Validation Study | IPC Task Force | 2020 | IPC White Paper | N/A | Current capacity verification |

## State-of-the-Art Methods & Tools

### Simulation Tools
- **SI Simulation:** HyperLynx, Sigrity, ADS
- **PI Simulation:** Redhawk, PowerSI, Ansys SIwave
- **EMC Simulation:** CST, HFSS, FEKO
- **Thermal Simulation:** Ansys Icepak, Mentor Flotherm

### Design Rule Checkers
- **CAD Tools:** Altium, Cadence, Mentor, KiCad
- **Integrated DRC:** Spacing, width, manufacturability
- **SI-specific DRC:** Length matching, impedance check, return path

### Measurement and Verification
- **TDR:** Impedance profiling
- **VNA:** S-parameter measurement
- **Oscilloscope:** Signal quality verification
- **EMC Pre-Scan:** Emissions testing
- **Thermal Imaging:** Hotspot identification

## Authoritative Data Sources

### IPC Standards (ipc.org)
- IPC-2221B: Generic Standard on Printed Board Design
- IPC-2152A: Standard for Determining Current-Carrying Capacity
- IPC-A-600H: Acceptability of Printed Boards
- IPC-6012E: Qualification and Performance Specification for Rigid Printed Boards
- IPC-7351B: Generic Requirements for Surface Mount Design and Land Pattern Standards

### Semiconductor Manufacturer Resources
**Texas Instruments (ti.com):**
- Application Reports: PCB layout for power converters
- Analog Design Journal: PDN and decoupling

**Analog Devices (analog.com):**
- MT-094: Keeping EMI/RFI out of high-speed ADC systems
- Linear Technology Design Notes: Power supply layout

**STMicroelectronics (st.com):**
- Application notes: STM32 PCB design guidelines
- MEMS layout guidelines

### Industry References
**Signal Integrity:**
- "High-Speed Digital Design: A Handbook of Black Magic" — Johnson & Graham
- "Signal Integrity Simplified" — Eric Bogatin
- "Signal and Power Integrity — Simplified" — Eric Bogatin & Larry Smith

**Power Integrity:**
- "Power Integrity Modeling and Simulation" — Ladd & Telbindi
- "Power Distribution Network Design Methodologies" — Istvan Novak

**EMC/EMI:**
- "Electromagnetic Compatibility Engineering" — Henry Ott
- "EMC and the Printed Circuit Board" — Mark Montrose

### Standards Organizations
- **IEC:** IEC 61000-4-x (EMC testing)
- **IEEE:** IEEE 802.3 (Ethernet physical layer)
- **JEDEC:** Memory standards, packaging specifications

## Analytical Frameworks (Scoring Backbone)

### Scoring Dimensions

**1. Placement (0-100 points)**
- Framework: IPC-2221, design guidelines
- Weight: 1.0-1.5 based on board type

**2. Routing (0-100 points)**
- Framework: IPC-2221, IPC-2152, SI principles
- Weight: 1.0-1.3 based on speed

**3. Power Delivery (0-100 points)**
- Framework: IPC-2152, PI principles
- Weight: 1.3-1.5 for power-sensitive applications

**4. Signal Integrity (0-100 points)**
- Framework: SI principles, transmission line theory
- Weight: 1.5 for high-speed/RF designs

**5. EMC/EMI (0-100 points)**
- Framework: EMC principles, regulatory standards
- Weight: 1.3-1.5 depending on application

**6. DFM (0-100 points)**
- Framework: IPC-A-600, IPC-7351
- Weight: 1.0-1.3 for production boards

### Grade Scale
- A: 90-100 (Production ready)
- B: 80-89 (Good, minor issues)
- C: 70-79 (Adequate, notable concerns)
- D: 60-69 (Poor, significant issues)
- F: <60 (Critical, requires redesign)

## Quick Reference Tables

### IPC-2152 Trace Width Quick Reference (External Layers, 10°C Rise, 1oz Copper)
| Current (A) | Width (mm) | Width (mil) |
|-------------|------------|-------------|
| 0.5 | 0.10 | 4 |
| 1.0 | 0.30 | 12 |
| 2.0 | 0.80 | 31 |
| 3.0 | 1.40 | 55 |
| 5.0 | 2.80 | 110 |
| 10.0 | 7.00 | 276 |

### Minimum Trace Spacing per IPC-2221B
| Voltage | Internal (mm) | External (mm) |
|---------|---------------|---------------|
| 0-50V | 0.15 | 0.15 |
| 51-100V | 0.20 | 0.25 |
| 101-150V | 0.30 | 0.40 |
| 151-250V | 0.40 | 0.80 |
| 251-500V | 0.60 | 1.20 |

### Via Current Capacity (Approximate)
| Via Size | Current (A) |
|----------|-------------|
| 0.3mm (12mil) drill | 0.5 |
| 0.5mm (20mil) drill | 1.0 |
| 0.8mm (31mil) drill | 2.0 |
| 1.0mm (39mil) drill | 3.0 |

Note: Multiple vias parallelize current capacity.

### Dielectric Constants (εr) for Common Materials
| Material | εr (1 MHz) | Loss Tangent |
|----------|------------|--------------|
| FR-4 (standard) | 4.3-4.8 | 0.02 |
| FR-4 (high-speed) | 4.0-4.3 | 0.015 |
| Rogers RO4350B | 3.48 | 0.0037 |
| Rogers RO4003C | 3.38 | 0.0027 |
| Isola FR408HR | 3.68 | 0.011 |
| Nelco N4000-13 | 3.7 | 0.009 |

## Self-Update Protocol

**Tool:** `tools/knowledge_updater.py`

**ArXiv Categories:**
- eess.SP (Signal Processing)
- physics.app-ph (Applied Physics)

**Search Queries:**
- "PCB signal integrity return path"
- "power distribution network decoupling capacitor placement"
- "PCB EMC design guidelines"
- "IPC trace width current capacity"
- "high-speed PCB design guidelines"

**Domains:**
- ipc.org
- ti.com
- analog.com
- st.com
- ieee.org

**Frequency:** Weekly cron (graceful no-op when offline)

**Append Format:**
- Date-stamped row in *Key Research Papers* table
- Deduplicated by URL/DOI hash
- Includes relevance score based on recency and keyword match

## Knowledge Update Log

### 2026-06-18
- Brain initialized with core frameworks and seed sources
- Added IPC standards foundation
- Added SI/PI frameworks
- Added EMC/EMI principles
- Added DFM guidelines
- Added reference tables for trace width, spacing, vias

### 2026-07-01
- Expanded framework descriptions
- Added scoring backbone details
- Added quick reference tables
- Added authoritative sources
- Self-update protocol established

<!-- End of SECOND-KNOWLEDGE-BRAIN.md -->
