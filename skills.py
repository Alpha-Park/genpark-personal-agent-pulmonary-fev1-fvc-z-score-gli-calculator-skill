# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-pulmonary-fev1-fvc-z-score-gli-calculator-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def calculate_gli_spirometry_zscores(fev1_liters, fvc_liters, age_years, height_cm, sex="MALE", ethnicity="CAUCASIAN"):
    if fev1_liters <= 0 or fvc_liters <= 0 or age_years <= 0 or height_cm <= 0:
        raise ValueError("Physiological measurements must be positive numbers")
        
    ratio = fev1_liters / fvc_liters
    
    # GLI simplified LMS regression coefficients (Caucasian standard reference)
    if sex.upper() == "MALE":
        pred_fev1 = 0.0430 * height_cm - 0.029 * age_years - 2.49
        pred_fvc = 0.0576 * height_cm - 0.026 * age_years - 4.34
        pred_ratio = 0.88 - 0.0018 * age_years
        sd_fev1 = 0.52
        sd_fvc = 0.61
        sd_ratio = 0.055
    else:
        pred_fev1 = 0.0395 * height_cm - 0.025 * age_years - 2.60
        pred_fvc = 0.0443 * height_cm - 0.026 * age_years - 2.89
        pred_ratio = 0.89 - 0.0019 * age_years
        sd_fev1 = 0.41
        sd_fvc = 0.49
        sd_ratio = 0.052
        
    z_fev1 = (fev1_liters - pred_fev1) / sd_fev1
    z_fvc = (fvc_liters - pred_fvc) / sd_fvc
    z_ratio = (ratio - pred_ratio) / sd_ratio
    
    lln_ratio = pred_ratio - 1.645 * sd_ratio
    lln_fev1 = pred_fev1 - 1.645 * sd_fev1
    lln_fvc = pred_fvc - 1.645 * sd_fvc
    
    # Classification: LLN threshold is z < -1.645
    is_obstructive = z_ratio < -1.645
    is_restrictive_pattern = (not is_obstructive) and (z_fvc < -1.645)
    
    if is_obstructive:
        pattern = "OBSTRUCTIVE_VENTILATORY_DEFECT"
        severity = "Mild" if z_fev1 >= -2.5 else ("Moderate" if z_fev1 >= -4.0 else "Severe")
    elif is_restrictive_pattern:
        pattern = "PR_RESTRICTIVE_PATTERN_SUSPECTED"
        severity = "Total lung capacity (TLC) plethysmography required to confirm true restriction"
    else:
        pattern = "NORMAL_SPIROMETRY"
        severity = "Preserved ventilatory capacity"
        
    return {
        "fev1_actual_liters": round(fev1_liters, 2),
        "fev1_predicted_liters": round(pred_fev1, 2),
        "fev1_zscore": round(z_fev1, 2),
        "fvc_actual_liters": round(fvc_liters, 2),
        "fvc_predicted_liters": round(pred_fvc, 2),
        "fvc_zscore": round(z_fvc, 2),
        "fev1_fvc_ratio_actual": round(ratio, 3),
        "fev1_fvc_ratio_lln": round(lln_ratio, 3),
        "ratio_zscore": round(z_ratio, 2),
        "spirometric_pattern": pattern,
        "defect_severity": severity,
        "fixed_ratio_070_discordant": (ratio < 0.70) != is_obstructive
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "calculate_gli_spirometry_zscores",
                        "description": """Calculate continuous z-scores and Lower Limit of Normal (LLN, 5th percentile, z = -1.645) for spirometry parameters.
Implements the multi-ethnic Global Lung Function Initiative (GLI-2012) LMS (Lambda-Mu-Sigma) methodology for FEV1, FVC, and FEV1/FVC.
Prevents false-positive COPD overdiagnosis in elderly and false-negative underdiagnosis in young athletes caused by fixed 0.70 ratio cutoffs.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = calculate_gli_spirometry_zscores(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'fev1_liters': 3.85, 'fvc_liters': 4.6, 'age_years': 42, 'height_cm': 178.0, 'sex': 'MALE', 'ethnicity': 'CAUCASIAN'}
        out = calculate_gli_spirometry_zscores(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
