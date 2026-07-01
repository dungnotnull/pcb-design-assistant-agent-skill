---
name: sub-evaluation-framework-selector
description: Classify the board (digital/analog/RF/power, layer count, speed) and select the governing IPC/SI/PI rule set.
---

## Role
Sub-skill of `pcb-design-assistant`. Classify the board (digital/analog/RF/power, layer count, speed) and select the governing IPC/SI/PI rule set for accurate evaluation.

## Inputs
- **board_description** (string, required): User-provided description of the PCB layout
- **layer_count** (int, required): Number of board layers (1-16+)
- **operating_voltage** (float, optional): Operating voltage in volts
- **max_current** (float, optional): Maximum current in amperes
- **signal_speed** (string, optional): Speed category (low_speed, high_speed, very_high_speed, rf)
- **application_type** (string, optional): Application category (consumer, automotive, industrial, medical, aerospace)
- **additional_context** (string, optional): Any other relevant information

## Procedure

### 1. Validate Required Inputs
Check that required inputs are present and valid:
- `board_description` must be non-empty string (min 20 chars for meaningful context)
- `layer_count` must be integer between 1 and 32
- If any required input is missing or invalid, request it from the user before proceeding

### 2. Classify Board Characteristics

#### 2.1 Determine Board Type
Classify based on description and inputs using this decision tree:
- **RF Board**: presence of RF keywords (antenna, microwave, GHz, RF, wireless, radar)
- **Mixed-Signal**: both digital and analog components mentioned
- **Power Electronics**: high current (>5A), power components (DC-DC, MOSFET, inductor, transformer)
- **High-Speed Digital**: high-speed signals mentioned (>100 MHz, DDR, SerDes, differential pairs)
- **General Digital**: default classification for standard digital boards
- **Analog**: primarily analog circuits (op-amps, sensors, instrumentation)

#### 2.2 Determine Speed Category
Based on `signal_speed` and analysis:
- **RF**: >100 MHz RF signals, wireless applications
- **Very High Speed**: >1 GHz digital, SerDes, DDR4+, PCIe Gen3+
- **High Speed**: 100 MHz - 1 GHz, DDR, differential pairs
- **Low Speed**: <100 MHz, standard digital logic

#### 2.3 Determine Layer Count Category
- **Simple**: 1-2 layers
- **Standard**: 4 layers
- **Complex**: 6-8 layers
- **Very Complex**: 10+ layers

### 3. Select Governing Frameworks

Map board characteristics to applicable frameworks:

#### 3.1 Primary Frameworks (Always Applied)
- **IPC-2221**: Generic Standard on Printed Board Design
- **IPC-2152**: Standard for Determining Current-Carrying Capacity

#### 3.2 Secondary Frameworks (Conditional)
- **Signal Integrity**: controlled impedance, return-path continuity, length matching
  - Applied when: high_speed or very_high_speed or RF
- **Power Integrity**: decoupling-capacitor placement, PDN target impedance
  - Applied when: max_current > 1A or power electronics or high-speed digital
- **EMC/EMI**: ground planes, guard traces, slot avoidance
  - Applied when: RF or high-speed or automotive/aerospace application
- **DFM**: Design for Manufacturability and IPC-A-600 acceptability
  - Applied when: production intent or layer_count >= 4
- **Thermal Management**: component derating from datasheets
  - Applied when: power electronics or high current or automotive/aerospace

### 4. Determine Evaluation Scope

Based on board classification, define which dimensions to evaluate:
- **Placement**: component placement and orientation
- **Routing**: trace routing, via usage, layer transitions
- **Power Delivery**: power trace sizing, PDN quality
- **Signal Integrity**: impedance control, length matching
- **EMC/EMI**: emissions and susceptibility considerations
- **DFM**: manufacturability and assembly considerations
- **Thermal**: heat dissipation and component derating

### 5. Output Structured Result

Produce JSON-structured result for next stage:

```json
{
  "board_classification": {
    "type": "high_speed_digital",
    "speed_category": "high_speed",
    "layer_category": "standard",
    "complexity": "medium"
  },
  "applicable_frameworks": [
    "IPC-2221",
    "IPC-2152", 
    "Signal-Integrity",
    "Power-Integrity",
    "EMC-EMI",
    "DFM"
  ],
  "evaluation_scope": [
    "placement",
    "routing",
    "power_delivery",
    "signal_integrity",
    "emc_emi",
    "dfm"
  ],
  "risk_factors": [],
  "framework_sources": [
    {"framework": "IPC-2221", "source": "IPC Standards", "version": "current"},
    {"framework": "IPC-2152", "source": "IPC Standards", "version": "current"}
  ]
}
```

## Tools
WebSearch (for framework verification), Read, Write

## Quality Gate
- ✅ All required inputs validated and present
- ✅ Board classification is deterministic and consistent
- ✅ Framework selection maps to documented IPC/SI/PI standards
- ✅ Output structure is valid JSON with all required fields
- ✅ Each framework cites its source document and version
- ❌ Refuse to proceed if board description is insufficient or inputs are missing

## Error Handling
If inputs are insufficient, ask targeted questions:
- "What is the layer count of your PCB?"
- "What are the highest signal frequencies on this board?"
- "What is the maximum current your power traces must carry?"
- "What industry standards must this design comply with?"

## Framework Reference Standards
- **IPC-2221**: Generic Standard on Printed Board Design
- **IPC-2152**: Standard for Determining Current-Carrying Capacity in Printed Board Design
- **IPC-A-600**: Acceptability of Printed Boards
- **IPC-A-610**: Acceptability of Electronic Assemblies
- **IPC-6012**: Qualification and Performance Specification for Rigid Printed Boards
- **IEC 61188-5-1**: Design guide for high-speed PCBs
