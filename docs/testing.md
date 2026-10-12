# Test Plan and Verification Report

## Overview
The testing framework for **Project 35: Crop Disease Expert System** verifies the correctness, efficiency, and robustness of the **Backward Chaining Inference Engine**, interactive targeted symptom verification, backtracking behavior, pandas knowledge base integration, and the **Command Line Interface (CLI)** presentation.

The test suite is implemented using `pytest` and Python's standard `unittest` framework in [`tests/test_inference.py`](file:///data/project/foai/tests/test_inference.py).

---

## Test Matrix

| Test ID | Test Name | Target Functionality | Input | Expected Output | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | `test_1_problem_statement_rice_sample` | Problem statement reference verification | Crop: `Rice`<br>Symptoms: `["Yellow Leaves", "Brown Spots", "Leaf Drying"]` | Disease: `Brown Spot Disease`<br>Treatment: `Apply Suitable Fungicide`<br>Confidence: `High`<br>Algorithm: `Backward Chaining` | **PASSED** |
| **TC-02** | `test_2_interactive_questioning_callback` | Dynamic interactive question generation | Crop: `Rice`<br>Callback responding `Yes` to Brown Spot sub-goals | Targeted questions triggered; Disease confirmed | **PASSED** |
| **TC-03** | `test_3_backtracking_to_alternative_hypothesis` | Goal refutation & backtracking | Refute initial hypothesis (`Bacterial Leaf Blight`), confirm alternative | Trace contains `BACKTRACKING`; `Brown Spot Disease` confirmed | **PASSED** |
| **TC-04** | `test_4_no_disease_match_all_refuted` | Negative symptom boundary | All symptoms refuted (`No` to all) | Status: `NO_DISEASE_MATCH`<br>Referral to agricultural officer | **PASSED** |
| **TC-05** | `test_5_unsupported_crop_error` | Input validation & boundary handling | Crop: `Pineapple` (Unsupported) | Status: `ERROR`<br>Informative supported crops message | **PASSED** |
| **TC-06** | `test_6_cross_crop_diagnoses` | Multi-crop generalization | Diagnostic cases for Wheat, Tomato, Potato, Maize, Cotton | All 7 distinct crop diseases correctly diagnosed with High confidence | **PASSED** |
| **TC-07** | `test_7_pandas_knowledge_base_integrity` | Pandas DataFrame schema validation | Rules & symptoms DataFrames | DataFrames non-empty; valid column schema (`id`, `crop`, `hypothesis`, etc.) | **PASSED** |
| **TC-08** | `test_8_information_efficiency_fewer_questions` | Question reduction & diagnostic efficiency | Rice with 9 candidate symptoms | Questions asked = 3 (strictly fewer than total crop symptoms) | **PASSED** |
| **TC-09** | `test_9_cli_benchmark_demo_execution` | CLI Benchmark Demo execution | `app.run_benchmark_demo(engine)` | Diagnostic report & trace generated cleanly without error | **PASSED** |
| **TC-10** | `test_10_cli_report_formatting_and_trace` | CLI Report card & trace formatting | Sample diagnostic dictionary | Formats report box, disease card, and reasoning timeline correctly | **PASSED** |

---

## Detailed Test Case Walkthroughs

### 1. TC-01: Problem Statement Rice Benchmark Case
- **Purpose**: Validates the explicit input and output mandated by the project specification.
- **Verification Code**:
  ```python
  result = backward_chaining(crop="Rice", symptoms=["Yellow Leaves", "Brown Spots", "Leaf Drying"])
  assert result["disease_identified"] == "Brown Spot Disease"
  assert result["recommended_treatment"] == "Apply Suitable Fungicide"
  assert result["confidence"] == "High"
  assert result["algorithm_used"] == "Backward Chaining"
  ```
- **Result**: PASSED in 0.01s.

### 2. TC-03: Backtracking Verification
- **Purpose**: Confirms that when a sub-goal fails, the engine correctly rolls back the goal stack without crashing and evaluates the next rule in the candidate list.
- **Trace Output**:
  ```text
  Step 2 [PUSH_GOAL]: Selected Suspected Disease Hypothesis: 'Bacterial Leaf Blight' via RULE_RICE_02.
  Step 3 [MEMORY_LOOKUP]: Checking Working Memory for sub-goal 'Yellow Leaves': Present (True).
  Step 4 [TARGETED_QUESTION]: Asking farmer targeted question [Leaf Condition]: "Do you observe translucent, water-soaked streaks?"
  Step 5 [FACT_RECORDED]: Farmer response recorded for 'Water-Soaked Lesions': NO (Refuted).
  Step 6 [BACKTRACKING]: Hypothesis 'Bacterial Leaf Blight' rejected because required symptom 'Water-Soaked Lesions' is absent. Backtracking to next candidate.
  Step 7 [PUSH_GOAL]: Selected Suspected Disease Hypothesis: 'Brown Spot Disease' via RULE_RICE_01.
  Step 8 [MEMORY_LOOKUP]: Checking Working Memory for sub-goal 'Yellow Leaves': Present (True).
  Step 9 [FACT_RECORDED]: Farmer response recorded for 'Brown Spots': YES (Confirmed).
  Step 10 [FACT_RECORDED]: Farmer response recorded for 'Leaf Drying': YES (Confirmed).
  Step 11 [GOAL_SATISFIED]: SUCCESS: All required symptoms for 'Brown Spot Disease' verified.
  ```
- **Result**: PASSED. Demonstrates deterministic, explainable backtracking.

### 3. TC-08: Information Efficiency Test
- **Purpose**: Quantifies the benefit of Backward Chaining over exhaustive fact collection.
- **Metrics**:
  - Total Rice symptoms in catalog: 9
  - Exhaustive checklist questions: 9
  - Backward Chaining questions asked: 3
  - **Reduction in Farmer Diagnostic Questions**: $66.7\%$ reduction!

### 4. TC-09 & TC-10: Command Line Interface Verification
- **Purpose**: Verifies that the CLI presentation layer accurately formats diagnostic output, prints structured ASCII/Unicode report cards, generates tabular trace logs, and runs the benchmark demo end-to-end without crashing.
- **Result**: PASSED.

---

## Test Execution Log

```text
$ python -m pytest -v tests/test_inference.py

============================= test session starts ==============================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- /data/project/.venv/bin/python
cachedir: .pytest_cache
rootdir: /data/project/foai
collecting ... collected 10 items

tests/test_inference.py::TestBackwardChainingExpertSystem::test_10_cli_report_formatting_and_trace PASSED [ 10%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_1_problem_statement_rice_sample PASSED [ 20%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_2_interactive_questioning_callback PASSED [ 30%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_3_backtracking_to_alternative_hypothesis PASSED [ 40%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_4_no_disease_match_all_refuted PASSED [ 50%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_5_unsupported_crop_error PASSED [ 60%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_6_cross_crop_diagnoses PASSED [ 70%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_7_pandas_knowledge_base_integrity PASSED [ 80%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_8_information_efficiency_fewer_questions PASSED [ 90%]
tests/test_inference.py::TestBackwardChainingExpertSystem::test_9_cli_benchmark_demo_execution PASSED [100%]

============================== 10 passed in 0.17s ==============================
```
