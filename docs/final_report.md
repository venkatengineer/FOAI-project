# Final Project Report

## 1. Title
**Crop Disease Expert System using Two-Stage Forward Chaining & Candidate Ranking**

---

## 2. Abstract
This mini-project develops a lightweight, rule-based expert system for identifying crop diseases based on observational field symptoms and microclimate environmental conditions. Built using Python, Flask, HTML/CSS, and JSON, the core contribution is a **Two-Stage Reasoning Inference Engine** combining primary **Forward Chaining** ($Fact \rightarrow Rule_1 \rightarrow New\ Fact \rightarrow Rule_2 \rightarrow Disease$) with a transparent **Candidate Disease Ranking Fallback** ($\text{score} = \frac{\text{matched}}{\text{total}} \times 100$). The system evaluates diseases across 6 crop types (Tomato, Potato, Chilli, Maize, Brinjal, Mango) and yields three distinct diagnostic states: **Strong Match**, **Possible Disease**, and **Insufficient Evidence**, completely eliminating misleading `"Unknown / Healthy"` false negatives. Evaluated across 8 automated test scenarios, the system demonstrates 100% accuracy in rule-chaining and candidate ranking while providing farmers and examiners with clear step-by-step reasoning traces, matched vs. missing symptom analysis, and actionable state-dependent remediation guidance.

---

## 3. Introduction
Agricultural disease management is vital for global food security. Smallholder farmers frequently observe physical symptoms on leaves, stems, or fruits but lack instant access to plant pathologists. While modern machine learning methods require massive labeled datasets and function as unexplainable "black boxes," Rule-Based Expert Systems replicate human domain expert reasoning through explicit production rules. This project demonstrates data-driven AI inference using Forward Chaining combined with partial evidence candidate ranking in a minimal, highly explainable architecture.

---

## 4. Problem Statement
Farmers face difficulty identifying crop diseases due to overlapping initial symptoms across different pathogens. External expert advice is often unavailable in rural areas. Machine learning approaches lack transparent reasoning paths, while traditional expert systems produce misleading `"Unknown / Healthy"` outputs whenever a user enters incomplete symptoms that do not trigger a full rule chain. This project addresses these challenges by building a deterministic, two-stage expert system that chains forward when full evidence is present and ranks candidate diseases when partial evidence is supplied.

---

## 5. Objectives
1. Implement a clean Two-Stage Reasoning Algorithm in Python without heavy external ML dependencies.
2. Maintain Forward Chaining as the primary symbolic AI mechanism for full rule matches (**STATE 1 — STRONG MATCH**).
3. Implement candidate disease ranking fallback ($\text{score} = \frac{\text{matched}}{\text{total}} \times 100$) for partial evidence inputs (**STATE 2 — POSSIBLE DISEASE** $\ge 50\%$).
4. Eliminate misleading `"Unknown / Healthy"` false negatives by providing an **INSUFFICIENT EVIDENCE** state ($< 50\%$) that prompts users for additional observations.
5. Enforce crop compatibility filtering to prevent recommending diseases belonging to unrelated crops.
6. Develop an intuitive web interface rendering state badges, evidence match progress bars, matched vs. missing symptom lists, reasoning trace timelines, candidate alternative comparison tables, and actionable recommendations.
7. Validate system reliability through 8 automated unit test cases.

---

## 6. Literature Survey
The system draws upon 5 foundational studies:
1. **Prasad & Babu (2006)**: Validated rule-based production systems for plant disease diagnosis.
2. **Mahaman et al. (2003)**: Demonstrated that data-driven Forward Chaining is optimal when reasoning from observed symptoms to unknown diagnoses.
3. **Kolhe et al. (2011)**: Established the efficacy of lightweight web architectures using JSON rule representations.
4. **Buchanan & Shortliffe (1984)**: Formulated working memory tracking and explanation traces ($WHY$ / $HOW$).
5. **Jones & Pierce (1997)**: Showed higher domain practitioner adoption for transparent expert systems over black-box models.

---

## 7. Proposed System
The system acts as an interactive agricultural advisor. The user selects the target crop, checks observed physical symptoms, and specifies environmental conditions. The Flask backend initializes working memory with these initial facts and passes them to the Two-Stage Inference Engine:
- **Stage 1 (Forward Chaining)**: Iteratively fires matching production rules from the Knowledge Base. If a disease conclusion rule fires, return **STATE 1 — STRONG MATCH**.
- **Stage 2 (Candidate Ranking Fallback)**: If no disease rule fires, candidate diseases matching the target crop are evaluated by match score $\text{score} = (\text{matched} / \text{total}) \times 100$. If score $\ge 50\%$, return **STATE 2 — POSSIBLE DISEASE**; otherwise return **STATE 3 — INSUFFICIENT EVIDENCE**.

---

## 8. Architecture
```
USER ──► UI (Flask/HTML) ──► INITIAL FACTS ──► KNOWLEDGE BASE (JSON)
                                                    │
                                                    ▼
EXPLANATION + ACTION ◄── DIAGNOSIS STATE ◄── TWO-STAGE INFERENCE ENGINE
 (1. Strong Match / 2. Possible Disease / 3. Insufficient Evidence)
```

---

## 9. Methodology
1. **Fact Acquisition**: User inputs are parsed into key-value facts (e.g., `crop=tomato`, `leaf_spots=yes`).
2. **Knowledge Loading**: `knowledge_base.json` loaded with 6 crops, 15 diseases (with `symptom_ids`), and 34 rules.
3. **Stage 1 Execution**: `inference.py` evaluates production rule conditions against working memory.
4. **Stage 2 Execution (Fallback)**: If no rule derives `disease`, evaluate crop-compatible diseases by symptom overlap.
5. **State Classification**: Classify result as `STRONG_MATCH`, `POSSIBLE_DISEASE`, or `INSUFFICIENT_EVIDENCE`.
6. **Output Rendering**: Format explanation (matched vs. missing symptoms), reasoning trace, alternative candidates, and recommendation.

---

## 10. Two-Stage Reasoning Algorithm
```python
function forward_chaining(initial_facts, knowledge_base):
    working_memory = copy(initial_facts)
    fired_rule_ids = set()
    reasoning_trace = []

    # STAGE 1: Forward Chaining Loop
    repeat:
        rule_fired = false
        for rule in knowledge_base.rules:
            if rule.id in fired_rule_ids: continue
            
            if all conditions in rule match working_memory:
                fired_rule_ids.add(rule.id)
                add rule.conclusions to working_memory
                record step in reasoning_trace
                rule_fired = true
                break

    until not rule_fired

    disease_key = working_memory.get("disease")
    if disease_key exists in knowledge_base.diseases:
        return STATE_1_STRONG_MATCH(disease_key, reasoning_trace)

    # STAGE 2: Candidate Ranking Fallback
    selected_crop = initial_facts.get("crop")
    candidates = []
    for disease in knowledge_base.diseases:
        if selected_crop and disease.crop != selected_crop:
            continue
            
        score = (matched_symptoms / total_symptoms) * 100
        candidates.append((disease, score))

    sort candidates by score descending
    top_candidate = candidates[0]

    if top_candidate.score >= 50.0:
        return STATE_2_POSSIBLE_DISEASE(top_candidate, candidates)
    else:
        return STATE_3_INSUFFICIENT_EVIDENCE(candidates)
```

---

## 11. Implementation
- **Backend**: Python 3, Flask (`app.py`)
- **Engine**: Pure Python (`inference.py`)
- **Knowledge Layer**: `knowledge_base.json` (generated by `build_kb.py`)
- **Frontend**: HTML5, CSS3, Google Fonts (`Outfit`)
- **Testing**: Python `unittest` (`tests/test_inference.py`)

---

## 12. Testing
Automated testing verified 8 core test scenarios:
1. Strong disease match through Forward Chaining (`Tomato Early Blight`)
2. Partial symptom match returning `Possible` state (`Tomato Late Blight` @ 50%)
3. Very weak symptoms returning `Insufficient Evidence`
4. Descending score ranking for multiple possible candidate diseases
5. Unrelated crop disease exclusion (e.g. Potato Blackleg for Mango)
6. Empty symptom input handling
7. Dynamic explanation generation (matched vs missing symptoms)
8. Reasoning trace accuracy (only actually fired rules logged)

All 8 tests passed in 0.001 seconds.

---

## 13. Results & Case Studies
- **Case 1 (Full Match — State 1 Strong Match)**:
  - `Inputs`: Tomato + Leaf Spots + Brown Spots + Lower Leaves + High Humidity
  - `Result`: **Strong Match: Tomato Early Blight** ($R1 \rightarrow R2 \rightarrow R3 \rightarrow R4$).
- **Case 2 (Partial Match — State 2 Possible Disease)**:
  - `Inputs`: Tomato + Dark Water-soaked Lesions + High Humidity (Missing Mold Growth)
  - `Result`: **Possible: Tomato Late Blight (50% Evidence Match)**. Prompts to check for Powdery Mold Growth.
- **Case 3 (Weak Match — State 3 Insufficient Evidence)**:
  - `Inputs`: Tomato + Leaf Spots
  - `Result`: **Insufficient Evidence**. Replaces `"Unknown / Healthy"` with request for further field observations.

---

## 14. Advantages
- **100% Explainable**: Complete reasoning trace and symptom breakdown for every diagnosis.
- **No False Healthy Diagnoses**: Eliminates confusing `"Unknown / Healthy"` false negatives.
- **Zero Heavy Dependencies**: Runs instantly on any machine with standard Python and Flask.
- **Deterministic AI**: Keeps Forward Chaining as core mechanism while handling partial evidence gracefully.

---

## 15. Conclusion
The updated Crop Disease Expert System demonstrates that classical symbolic AI techniques like Forward Chaining, when paired with simple candidate disease ranking fallbacks, provide a robust, practical, and fully explainable decision support system for agriculture.
