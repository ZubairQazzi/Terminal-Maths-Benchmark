import json
import numpy as np
import scipy.stats as stats

with open('/app/data/calibration_cases.json') as f:
    calib = json.load(f)

print("Testing calibration cases...")
for case in calib['cases']:
    case_id = case['case_id']
    groups = case['groups']
    print(f"Case: {case_id}, groups keys: {list(groups.keys())}")
