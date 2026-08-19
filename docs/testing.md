# Testing Report

This document records the automated testing strategy, 8 test case specifications, and verified execution results for the **Crop Disease Expert System**.

---

## Test Execution Summary

- **Test Suite**: `tests/test_inference.py`
- **Framework**: Python standard `unittest`
- **Total Test Cases**: 8
- **Passed**: 8
- **Failed**: 0
- **Execution Time**: 0.001s
- **Status**: PASSED (100% Success Rate)

```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
```

---

## Detailed Test Cases

### Test Case 1: Strong Disease Match through Forward Chaining
- **Objective**: Verify multi-step Forward Chaining derivation for Tomato Early Blight.
- **Input Facts**: `crop=tomato`, `leaf_spots=yes`, `brown_spots=yes`, `lower_leaves_affected=yes`, `high_humidity=yes`
- **Expected State**: `STRONG_MATCH` (`Strong Match`)
- **Expected Fired Rules**: `R1 -> R2 -> R3 -> R4`
- **Expected Conclusion**: `Tomato Early Blight` (`tomato_early_blight`)
- **Status**: PASSED

### Test Case 2: Partial Symptom Match (Stage 2 Fallback)
- **Objective**: Verify Stage 2 candidate ranking fallback when no rule fires.
- **Input Facts**: `crop=tomato`, `water_soaked_spots=yes`, `high_humidity=yes`
- **Expected State**: `POSSIBLE_DISEASE` (`Possible`)
- **Expected Top Candidate**: `Tomato Late Blight` (`tomato_late_blight` @ 50.0% match score)
- **Expected Flag**: `no_definitive_rule_triggered = True`
- **Status**: PASSED

### Test Case 3: Very Weak Symptoms (Insufficient Evidence)
- **Objective**: Verify handling when symptom match score is below 50% threshold.
- **Input Facts**: `crop=tomato`, `leaf_spots=yes` (1 symptom out of 4 = 25%)
- **Expected State**: `INSUFFICIENT_EVIDENCE` (`Insufficient Evidence`)
- **Expected Disease Name**: `Insufficient Evidence` (never displays `"Unknown / Healthy"`)
- **Status**: PASSED

### Test Case 4: Multiple Possible Diseases Ranking
- **Objective**: Verify candidate diseases are ranked in strict descending order of match scores.
- **Input Facts**: `crop=tomato`, `water_soaked_spots=yes`, `high_humidity=yes`
- **Expected Outcome**: Alternatives list sorted by `match_score` descending.
- **Status**: PASSED

### Test Case 5: Wrong Crop Exclusion
- **Objective**: Verify diseases belonging to unrelated crops are excluded from candidates.
- **Input Facts**: `crop=mango`, `black_stem=yes` (Potato symptom on Mango)
- **Expected Outcome**: Potato diseases (`potato_blackleg`) excluded from Mango candidate ranking.
- **Status**: PASSED

### Test Case 6: No Symptoms Input
- **Objective**: Verify engine handles empty symptom input dictionary safely.
- **Input Facts**: `crop=tomato`
- **Expected State**: `INSUFFICIENT_EVIDENCE`
- **Expected Fired Rules**: None
- **Status**: PASSED

### Test Case 7: Explanation Generation
- **Objective**: Verify matched and missing symptom lists are correctly populated in explanation dictionary.
- **Input Facts**: `crop=tomato`, `water_soaked_spots=yes`, `high_humidity=yes`
- **Expected Outcome**: `explanation["matched"]` contains verified inputs, `explanation["missing"]` contains missing symptoms.
- **Status**: PASSED

### Test Case 8: Forward Chaining Trace Accuracy
- **Objective**: Verify reasoning trace accurately logs only actually fired rules without fabricating firings.
- **Input Facts**: `crop=tomato`, `leaf_spots=yes`
- **Expected Outcome**: Only `R1` appears in `reasoning_trace` and `fired_rules`.
- **Status**: PASSED
