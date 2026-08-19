"""
Forward Chaining & Candidate Disease Ranking Inference Engine for Crop Disease Expert System.

Architecture (Two-Stage Reasoning):
Stage 1: Forward Chaining Engine (Primary AI Mechanism)
         Iteratively fires rules matching current working memory.
         If a rule concludes a definitive disease, return STATE 1 — STRONG MATCH.

Stage 2: Candidate Disease Ranking (Fallback Mechanism)
         Runs ONLY if Forward Chaining does not derive a definitive disease.
         Evaluates crop-compatible diseases by match score:
         match_score = (matched_symptoms / total_symptoms) * 100

         Thresholds:
         - Top Candidate Match Score >= 50%: return STATE 2 — POSSIBLE DISEASE.
         - Top Candidate Match Score < 50% or no symptoms: return STATE 3 — INSUFFICIENT EVIDENCE.
"""

THRESHOLD_STRONG = 80.0
THRESHOLD_POSSIBLE = 50.0


def get_symptom_label_map(knowledge_base):
    """Builds a mapping from symptom/environmental condition ID to human-readable label."""
    label_map = {}
    for sym in knowledge_base.get("symptoms", []):
        label_map[sym["id"]] = sym["label"]
    for env in knowledge_base.get("environmental_conditions", []):
        label_map[env["id"]] = env["label"]
    return label_map


def calculate_candidate_ranking(initial_facts, knowledge_base):
    """
    Ranks diseases based on partial symptom match scores for partial evidence fallback.
    Excludes diseases for unrelated crops if a crop is selected.
    
    Returns:
        list[dict]: Ranked list of disease candidates with match score, matched & missing symptoms.
    """
    selected_crop = initial_facts.get("crop", "").strip().lower()
    label_map = get_symptom_label_map(knowledge_base)

    # Collect active symptom and environmental condition IDs present in initial_facts
    user_symptom_ids = set()
    for key, val in initial_facts.items():
        if key != "crop" and val == "yes":
            user_symptom_ids.add(key)

    candidates = []
    diseases = knowledge_base.get("diseases", {})

    for disease_key, disease_info in diseases.items():
        crop_name = disease_info.get("crop", "").strip().lower()

        # Crop compatibility check: exclude diseases belonging to other crops
        if selected_crop and crop_name != selected_crop:
            continue

        req_symptom_ids = disease_info.get("symptom_ids", [])
        if not req_symptom_ids:
            # Fallback for mapping if symptom_ids is missing
            req_symptom_ids = []

        matched_ids = [sid for sid in req_symptom_ids if sid in user_symptom_ids]
        missing_ids = [sid for sid in req_symptom_ids if sid not in user_symptom_ids]

        matched_count = len(matched_ids)
        total_count = len(req_symptom_ids)
        score = (matched_count / total_count * 100.0) if total_count > 0 else 0.0

        if score >= THRESHOLD_STRONG:
            status = "Strong Candidate"
        elif score >= THRESHOLD_POSSIBLE:
            status = "Possible"
        else:
            status = "Low Evidence"

        candidates.append({
            "disease_key": disease_key,
            "name": disease_info.get("name", disease_key),
            "crop": disease_info.get("crop", ""),
            "match_score": round(score, 1),
            "score_formatted": f"{int(round(score))}%",
            "status": status,
            "matched_count": matched_count,
            "total_count": total_count,
            "matched_symptom_ids": matched_ids,
            "missing_symptom_ids": missing_ids,
            "matched_symptom_labels": [label_map.get(sid, sid) for sid in matched_ids],
            "missing_symptom_labels": [label_map.get(sid, sid) for sid in missing_ids],
            "recommendation": disease_info.get("recommendation", "Consult agricultural officer.")
        })

    # Sort candidates by match_score descending, then by matched_count descending
    candidates.sort(key=lambda c: (c["match_score"], c["matched_count"]), reverse=True)
    return candidates


def forward_chaining(initial_facts, knowledge_base):
    """
    Executes the Two-Stage Inference Algorithm:
    Stage 1: Forward Chaining Engine
    Stage 2: Candidate Ranking Fallback (if no definitive disease derived in Stage 1)
    
    Args:
        initial_facts (dict): Dict of input facts (e.g. {'crop': 'tomato', 'leaf_spots': 'yes'})
        knowledge_base (dict): Knowledge base containing rules and disease definitions
        
    Returns:
        dict: Diagnostic result adhering to one of three states:
              - STRONG_MATCH
              - POSSIBLE_DISEASE
              - INSUFFICIENT_EVIDENCE
    """
    label_map = get_symptom_label_map(knowledge_base)
    working_memory = dict(initial_facts)
    fired_rules = []
    reasoning_trace = []
    rules = knowledge_base.get("rules", [])
    fired_rule_ids = set()

    # Stage 1: Forward Chaining Loop
    while True:
        rule_fired_in_this_pass = False

        for rule in rules:
            rule_id = rule["id"]
            if rule_id in fired_rule_ids:
                continue

            conditions = rule["conditions"]
            match = True
            for key, expected_value in conditions.items():
                if working_memory.get(key) != expected_value:
                    match = False
                    break

            if match:
                fired_rule_ids.add(rule_id)
                conclusions = rule["conclusions"]

                for c_key, c_val in conclusions.items():
                    working_memory[c_key] = c_val

                fired_rules.append(rule)
                reasoning_trace.append({
                    "rule_id": rule_id,
                    "explanation": rule.get("explanation", f"Rule {rule_id} fired"),
                    "conditions": conditions,
                    "conclusions": conclusions
                })
                rule_fired_in_this_pass = True
                break

        if not rule_fired_in_this_pass:
            break

    # Compile user-facing matched symptoms summary from initial_facts
    user_matched_symptoms = []
    for key, val in initial_facts.items():
        if key != "crop" and val == "yes" and key in label_map:
            user_matched_symptoms.append(label_map[key])

    disease_key = working_memory.get("disease")
    diseases = knowledge_base.get("diseases", {})

    # Evaluate Stage 1 Result vs Stage 2 Fallback
    if disease_key and disease_key in diseases:
        # STATE 1 — STRONG MATCH (Forward Chaining Derived Disease)
        disease_info = diseases[disease_key]
        disease_name = disease_info["name"]
        req_symptom_ids = disease_info.get("symptom_ids", [])

        user_symptom_ids = {k for k, v in initial_facts.items() if k != "crop" and v == "yes"}
        disease_matched_ids = [sid for sid in req_symptom_ids if sid in user_symptom_ids]
        disease_missing_ids = [sid for sid in req_symptom_ids if sid not in user_symptom_ids]

        disease_matched_labels = [label_map.get(sid, sid) for sid in disease_matched_ids]
        disease_missing_labels = [label_map.get(sid, sid) for sid in disease_missing_ids]

        explanation_matched = [f"{lbl} matches the disease profile." for lbl in disease_matched_labels]
        explanation_missing = [f"{lbl} were not reported." for lbl in disease_missing_labels]

        recommendation = (
            "Symptoms strongly match this disease pattern. "
            "Remove or isolate affected plant material where appropriate and follow reliable agricultural disease-management guidance."
        )

        return {
            "state": "STRONG_MATCH",
            "status_label": "Strong Match",
            "disease_key": disease_key,
            "disease_name": disease_name,
            "match_score": 100.0,
            "score_formatted": "Strong Match",
            "matched_symptoms": user_matched_symptoms,
            "disease_matched_symptoms": disease_matched_labels,
            "disease_missing_symptoms": disease_missing_labels,
            "explanation": {
                "matched": explanation_matched,
                "missing": explanation_missing
            },
            "reasoning_trace": reasoning_trace,
            "fired_rules": [r["id"] for r in fired_rules],
            "working_memory": working_memory,
            "no_definitive_rule_triggered": False,
            "possible_alternatives": [],
            "recommendation": recommendation
        }

    else:
        # Stage 2: Candidate Disease Ranking Fallback
        candidates = calculate_candidate_ranking(initial_facts, knowledge_base)
        top_candidate = candidates[0] if candidates else None

        if top_candidate and top_candidate["match_score"] >= THRESHOLD_POSSIBLE:
            # STATE 2 — POSSIBLE DISEASE
            explanation_matched = [f"{lbl} matches the disease profile." for lbl in top_candidate["matched_symptom_labels"]]
            explanation_missing = [f"{lbl} were not reported." for lbl in top_candidate["missing_symptom_labels"]]

            recommendation = (
                "The available symptoms suggest this disease as a possibility, "
                "but additional symptoms are needed before making a confident assessment."
            )

            # Alternatives list excludes top candidate from main view
            alternatives = candidates

            return {
                "state": "POSSIBLE_DISEASE",
                "status_label": top_candidate["status"],  # "Possible"
                "disease_key": top_candidate["disease_key"],
                "disease_name": top_candidate["name"],
                "match_score": top_candidate["match_score"],
                "score_formatted": top_candidate["score_formatted"],
                "matched_symptoms": user_matched_symptoms,
                "disease_matched_symptoms": top_candidate["matched_symptom_labels"],
                "disease_missing_symptoms": top_candidate["missing_symptom_labels"],
                "explanation": {
                    "matched": explanation_matched,
                    "missing": explanation_missing
                },
                "reasoning_trace": reasoning_trace,
                "fired_rules": [r["id"] for r in fired_rules],
                "working_memory": working_memory,
                "no_definitive_rule_triggered": True,
                "possible_alternatives": alternatives,
                "recommendation": recommendation
            }
        else:
            # STATE 3 — INSUFFICIENT EVIDENCE
            recommendation = (
                "Not enough information is available to identify a meaningful disease candidate. "
                "Provide additional symptoms."
            )

            return {
                "state": "INSUFFICIENT_EVIDENCE",
                "status_label": "Insufficient Evidence",
                "disease_key": None,
                "disease_name": "Insufficient Evidence",
                "match_score": 0.0,
                "score_formatted": "N/A",
                "matched_symptoms": user_matched_symptoms,
                "disease_matched_symptoms": [],
                "disease_missing_symptoms": [],
                "explanation": {
                    "matched": [],
                    "missing": ["Provided observations are insufficient for a reliable disease candidate ranking."]
                },
                "reasoning_trace": reasoning_trace,
                "fired_rules": [r["id"] for r in fired_rules],
                "working_memory": working_memory,
                "no_definitive_rule_triggered": True,
                "possible_alternatives": candidates if candidates else [],
                "recommendation": recommendation
            }
