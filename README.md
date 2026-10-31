# genpark-personal-agent-pulmonary-fev1-fvc-z-score-gli-calculator-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Global Lung Function Initiative (GLI-2012) spirometry multi-ethnic continuous z-score and LLN obstructive/restrictive classifier.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `calculate_gli_spirometry_zscores`
- **Category**: `personal_agent`

### Method Documentation
Calculate continuous z-scores and Lower Limit of Normal (LLN, 5th percentile, z = -1.645) for spirometry parameters.
Implements the multi-ethnic Global Lung Function Initiative (GLI-2012) LMS (Lambda-Mu-Sigma) methodology for FEV1, FVC, and FEV1/FVC.
Prevents false-positive COPD overdiagnosis in elderly and false-negative underdiagnosis in young athletes caused by fixed 0.70 ratio cutoffs.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate_gli_spirometry_zscores",
    "arguments": {
    "fev1_liters": 3.85,
    "fvc_liters": 4.6,
    "age_years": 42,
    "height_cm": 178.0,
    "sex": "MALE",
    "ethnicity": "CAUCASIAN"
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
