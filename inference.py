"""
Forward Chaining Inference Engine for Crop Disease Expert System.

Algorithm:
1. Working memory is initialized with initial facts (User inputs).
2. Iteratively inspect rules in Knowledge Base.
3. If rule conditions are satisfied by working memory and rule hasn't fired yet:
   - Fire the rule
   - Add rule conclusions into working memory
   - Log execution step in reasoning trace
4. Repeat until no further rules match.
5. Extract disease diagnosis and return full explanation.
"""

def forward_chaining(initial_facts, knowledge_base):
    """
    Executes Forward Chaining algorithm.
    
    Args:
        initial_facts (dict): Dict of input facts (e.g. {'crop': 'tomato', 'leaf_spots': 'yes'})
        knowledge_base (dict): Knowledge base containing rules and disease definitions
        
    Returns:
        dict: Result containing diagnosis, matched symptoms, reasoning trace, and recommendation.
    """
    # Working memory initialized with initial facts
    working_memory = dict(initial_facts)
    fired_rules = []
    reasoning_trace = []
    rules = knowledge_base.get("rules", [])
    fired_rule_ids = set()

    # Iterative forward chaining loop
    while True:
        rule_fired_in_this_pass = False

        for rule in rules:
            rule_id = rule["id"]
            if rule_id in fired_rule_ids:
                continue

            conditions = rule["conditions"]
            # Check if all conditions of the rule match current working memory
            match = True
            for key, expected_value in conditions.items():
                if working_memory.get(key) != expected_value:
                    match = False
                    break

            if match:
                # Fire the rule
                fired_rule_ids.add(rule_id)
                conclusions = rule["conclusions"]

                # Add new facts to working memory
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
                # Break after firing one rule per pass to maintain strict execution order
                break

        # Stop when no new rule can be fired
        if not rule_fired_in_this_pass:
            break

    # Extract final disease diagnosis from working memory
    disease_key = working_memory.get("disease")
    diseases = knowledge_base.get("diseases", {})
    
    if disease_key and disease_key in diseases:
        disease_info = diseases[disease_key]
        diagnosis_name = disease_info["name"]
        recommendation = disease_info.get("recommendation", "Consult agricultural specialist.")
        symptoms_summary = disease_info.get("symptoms_summary", [])
    else:
        diagnosis_name = "Unknown / Healthy (No Disease Matched)"
        recommendation = "No specific disease pattern matched the provided symptoms. Monitor crop and consult agricultural officer if symptoms escalate."
        symptoms_summary = []

    # Compile user-facing matched symptoms summary
    matched_symptoms = []
    for sym in knowledge_base.get("symptoms", []):
        if initial_facts.get(sym["id"]) == "yes":
            matched_symptoms.append(sym["label"])
            
    for env in knowledge_base.get("environmental_conditions", []):
        if initial_facts.get(env["id"]) == "yes":
            matched_symptoms.append(env["label"])

    return {
        "disease_key": disease_key,
        "disease_name": diagnosis_name,
        "recommendation": recommendation,
        "matched_symptoms": matched_symptoms,
        "reasoning_trace": reasoning_trace,
        "fired_rules": [r["id"] for r in fired_rules],
        "working_memory": working_memory,
        "symptoms_summary": symptoms_summary
    }
