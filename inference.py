#!/data/project/.venv/bin/python
"""
Project 35: Crop Disease Expert System - Backward Chaining Inference Engine
Implements goal-driven Backward Chaining with hypothesis testing, working memory,
goal stack management, interactive symptom verification, and treatment recommendation.
Uses pandas for structured rule and knowledge base manipulation.
"""

import json
import os
from typing import Callable, Dict, List, Optional, Any
import pandas as pd

DEFAULT_KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


class BackwardChainingEngine:
    """
    Goal-driven Backward Chaining Expert System Engine.
    Starts with a suspected disease hypothesis and works backward to verify
    whether the required symptoms are present in the crop.
    """

    def __init__(self, kb_path: str = DEFAULT_KB_PATH):
        self.kb_path = kb_path
        self.kb = self._load_knowledge_base()
        self.rules_df = pd.DataFrame(self.kb.get("rules", []))
        self.symptoms_df = pd.DataFrame(self.kb.get("symptoms", []))
        self.diseases = self.kb.get("diseases", {})
        self.crops = [c["name"] for c in self.kb.get("crops", [])]

        # Build symptom metadata lookup
        self.symptom_meta = {}
        for _, row in self.symptoms_df.iterrows():
            self.symptom_meta[row["name"].strip().lower()] = {
                "id": row["id"],
                "name": row["name"],
                "category": row.get("category", "General Symptom"),
                "question": row.get("question", f"Does the crop show {row['name']}?")
            }

    def _load_knowledge_base(self) -> dict:
        """Loads knowledge base from JSON file."""
        if not os.path.exists(self.kb_path):
            from build_kb import build_knowledge_base
            return build_knowledge_base()
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_supported_crops(self) -> List[str]:
        """Returns list of supported crops."""
        return self.crops

    def get_crop_diseases(self, crop: str) -> List[str]:
        """Returns list of suspected disease hypotheses for a given crop."""
        filtered = self.rules_df[self.rules_df["crop"].str.lower() == crop.strip().lower()]
        return filtered["hypothesis"].tolist()

    def get_all_symptoms_for_crop(self, crop: str) -> List[str]:
        """Returns all distinct symptoms associated with a crop's disease rules."""
        filtered = self.rules_df[self.rules_df["crop"].str.lower() == crop.strip().lower()]
        symptoms_set = []
        for sym_list in filtered["required_symptoms"]:
            for s in sym_list:
                if s not in symptoms_set:
                    symptoms_set.append(s)
        return symptoms_set

    def get_symptom_category(self, symptom_name: str) -> str:
        """Returns the agricultural category of a symptom (e.g. Leaf Color, Stem Condition, Fruit Damage)."""
        key = symptom_name.strip().lower()
        if key in self.symptom_meta:
            return self.symptom_meta[key]["category"]
        return "General Observation"

    def get_symptom_question(self, symptom_name: str) -> str:
        """Returns a natural language question targeted to the farmer."""
        key = symptom_name.strip().lower()
        if key in self.symptom_meta:
            return self.symptom_meta[key]["question"]
        return f"Does the crop show {symptom_name}?"

    def diagnose(
        self,
        crop: str,
        initial_symptoms: Optional[List[str]] = None,
        suspected_disease: Optional[str] = None,
        ask_callback: Optional[Callable[[str, str, str], bool]] = None
    ) -> Dict[str, Any]:
        """
        Executes Goal-Driven Backward Chaining:
        1. Selects candidate disease hypotheses for the chosen crop.
        2. Sets each hypothesis as the top-level goal on the Goal Stack.
        3. Evaluates rules concluding that hypothesis.
        4. For each required symptom (sub-goal), checks Working Memory.
        5. If unknown, queries the user via ask_callback (interactive verification).
        6. Backtracks if a required symptom is refuted.
        7. Concludes when a hypothesis is verified or all candidates are exhausted.
        """
        crop_clean = crop.strip()
        filtered_rules = self.rules_df[self.rules_df["crop"].str.lower() == crop_clean.lower()]

        if filtered_rules.empty:
            return {
                "status": "ERROR",
                "crop": crop_clean,
                "disease_identified": "Crop Not Supported",
                "recommended_treatment": "Please select a supported crop: " + ", ".join(self.crops),
                "confidence": "None",
                "algorithm_used": "Backward Chaining",
                "reasoning_trace": [f"Crop '{crop_clean}' not found in knowledge base."],
                "goal_stack": [],
                "verified_symptoms": [],
                "questions_asked_count": 0
            }

        # Initialize Working Memory with initial observations
        working_memory: Dict[str, bool] = {}
        if initial_symptoms:
            for sym in initial_symptoms:
                working_memory[sym.strip()] = True

        reasoning_trace: List[Dict[str, Any]] = []
        goal_stack: List[str] = []
        questions_asked: List[str] = []

        # Determine hypothesis evaluation order
        candidate_rules = filtered_rules.to_dict(orient="records")

        # If user explicitly suspected a disease, evaluate it first
        if suspected_disease:
            suspected_clean = suspected_disease.strip().lower()
            candidate_rules.sort(
                key=lambda r: 0 if r["hypothesis"].strip().lower() == suspected_clean else 1
            )
        elif initial_symptoms:
            # Best-first heuristic: prioritize hypotheses sharing most initial symptoms
            def match_count(rule_record):
                req = set(rule_record.get("required_symptoms", []))
                init = set(initial_symptoms)
                return len(req.intersection(init))
            candidate_rules.sort(key=match_count, reverse=True)

        reasoning_trace.append({
            "step": 1,
            "action": "INITIALIZATION",
            "message": f"Starting Backward Chaining diagnostic engine for Crop: '{crop_clean}'.",
            "working_memory": dict(working_memory),
            "goal_stack": list(goal_stack)
        })

        step_counter = 2

        # Backward Chaining Loop over candidate hypotheses
        for rule in candidate_rules:
            hypothesis = rule["hypothesis"]
            rule_id = rule["id"]
            required_symptoms = rule["required_symptoms"]
            treatment = rule.get("treatment", "Apply Suitable Treatment")
            disease_id = rule.get("disease_id", "")
            disease_info = self.diseases.get(disease_id, {})

            # Push Top-Level Goal onto Goal Stack
            goal_stack.append(f"Goal: Prove '{hypothesis}'")
            reasoning_trace.append({
                "step": step_counter,
                "action": "PUSH_GOAL",
                "message": f"Selected Suspected Disease Hypothesis: '{hypothesis}' via {rule_id}. Pushing goal to stack.",
                "goal_stack": list(goal_stack),
                "working_memory": dict(working_memory)
            })
            step_counter += 1

            hypothesis_verified = True
            failed_symptom = None

            # Verify each required symptom as a sub-goal
            for symptom in required_symptoms:
                subgoal = f"Sub-Goal: Verify '{symptom}'"
                goal_stack.append(subgoal)

                category = self.get_symptom_category(symptom)
                question_text = self.get_symptom_question(symptom)

                # Check working memory
                if symptom in working_memory:
                    is_present = working_memory[symptom]
                    reasoning_trace.append({
                        "step": step_counter,
                        "action": "MEMORY_LOOKUP",
                        "message": f"Checking Working Memory for sub-goal '{symptom}': {'Present (True)' if is_present else 'Absent (False)'}.",
                        "goal_stack": list(goal_stack),
                        "working_memory": dict(working_memory)
                    })
                    step_counter += 1
                else:
                    # Interactive verification: ask the farmer targeted question
                    if ask_callback is not None:
                        questions_asked.append(symptom)
                        reasoning_trace.append({
                            "step": step_counter,
                            "action": "TARGETED_QUESTION",
                            "message": f"Asking farmer targeted question [{category}]: \"{question_text}\"",
                            "goal_stack": list(goal_stack),
                            "working_memory": dict(working_memory)
                        })
                        step_counter += 1

                        user_response = ask_callback(symptom, category, question_text)
                        is_present = bool(user_response)
                        working_memory[symptom] = is_present

                        reasoning_trace.append({
                            "step": step_counter,
                            "action": "FACT_RECORDED",
                            "message": f"Farmer response recorded for '{symptom}': {'YES (Confirmed)' if is_present else 'NO (Refuted)'}.",
                            "goal_stack": list(goal_stack),
                            "working_memory": dict(working_memory)
                        })
                        step_counter += 1
                    else:
                        # If no callback and not in initial symptoms, treat as not confirmed
                        is_present = False
                        working_memory[symptom] = False
                        reasoning_trace.append({
                            "step": step_counter,
                            "action": "UNVERIFIED_ABSENT",
                            "message": f"Sub-goal '{symptom}' not in initial facts and no interactive callback provided. Assumed Absent.",
                            "goal_stack": list(goal_stack),
                            "working_memory": dict(working_memory)
                        })
                        step_counter += 1

                # Pop Sub-Goal from stack
                goal_stack.pop()

                if not is_present:
                    hypothesis_verified = False
                    failed_symptom = symptom
                    reasoning_trace.append({
                        "step": step_counter,
                        "action": "BACKTRACKING",
                        "message": f"Hypothesis '{hypothesis}' rejected because required symptom '{symptom}' is absent. Backtracking to next candidate.",
                        "goal_stack": list(goal_stack),
                        "working_memory": dict(working_memory)
                    })
                    step_counter += 1
                    break

            # Pop Top-Level Goal from stack
            goal_stack.pop()

            if hypothesis_verified:
                # Goal proven! All required symptoms verified
                verified_symptoms_list = [s for s in required_symptoms if working_memory.get(s, False)]

                reasoning_trace.append({
                    "step": step_counter,
                    "action": "GOAL_SATISFIED",
                    "message": f"SUCCESS: All required symptoms for '{hypothesis}' verified via rule {rule_id}. Backward Chaining diagnostic goal fulfilled!",
                    "goal_stack": list(goal_stack),
                    "working_memory": dict(working_memory)
                })

                # Determine confidence
                confidence = "High" if len(verified_symptoms_list) == len(required_symptoms) else "Moderate"

                return {
                    "status": "DIAGNOSIS_SUCCESS",
                    "crop": crop_clean,
                    "disease_identified": hypothesis,
                    "recommended_treatment": treatment,
                    "confidence": confidence,
                    "algorithm_used": "Backward Chaining",
                    "rule_fired": rule_id,
                    "pathogen": disease_info.get("pathogen", "Agricultural Pathogen"),
                    "detailed_treatment": disease_info.get("detailed_treatment", treatment),
                    "prevention": disease_info.get("prevention", "Maintain balanced soil fertility and proper irrigation."),
                    "verified_symptoms": verified_symptoms_list,
                    "reasoning_trace": reasoning_trace,
                    "working_memory": working_memory,
                    "questions_asked_count": len(questions_asked),
                    "questions_asked": questions_asked,
                    "summary": f"Backward Chaining successfully identified '{hypothesis}' in {crop_clean} with {confidence} confidence."
                }

        # If all hypotheses were tested and refuted
        verified_positive = [k for k, v in working_memory.items() if v is True]
        reasoning_trace.append({
            "step": step_counter,
            "action": "EXHAUSTED",
            "message": "All suspected disease hypotheses for this crop have been evaluated and refuted based on symptom evidence.",
            "goal_stack": list(goal_stack),
            "working_memory": dict(working_memory)
        })

        return {
            "status": "NO_DISEASE_MATCH",
            "crop": crop_clean,
            "disease_identified": "Inconclusive / No Definite Disease Match",
            "recommended_treatment": "Consult a local agricultural extension officer. Monitor crop daily and submit plant tissue for laboratory pathogen testing.",
            "confidence": "Low",
            "algorithm_used": "Backward Chaining",
            "rule_fired": None,
            "pathogen": "Unknown / Unconfirmed",
            "detailed_treatment": "Isolate symptomatic plants to prevent potential spread. Ensure irrigation water is clean and avoid excessive nitrogen application.",
            "prevention": "Inspect leaf underside, roots, and stem collar regularly for emerging pest or fungal signs.",
            "verified_symptoms": verified_positive,
            "reasoning_trace": reasoning_trace,
            "working_memory": working_memory,
            "questions_asked_count": len(questions_asked),
            "questions_asked": questions_asked,
            "summary": "Backward Chaining was unable to confirm any known disease hypothesis with the provided symptoms."
        }


# Quick function wrapper for standard calls
def backward_chaining(
    crop: str,
    symptoms: Optional[List[str]] = None,
    suspected_disease: Optional[str] = None,
    ask_callback: Optional[Callable[[str, str, str], bool]] = None,
    kb_path: str = DEFAULT_KB_PATH
) -> Dict[str, Any]:
    """Convenience helper function to run Backward Chaining inference."""
    engine = BackwardChainingEngine(kb_path=kb_path)
    return engine.diagnose(
        crop=crop,
        initial_symptoms=symptoms,
        suspected_disease=suspected_disease,
        ask_callback=ask_callback
    )


if __name__ == "__main__":
    print("=" * 74)
    print(" 🌾  PROJECT 35: CROP DISEASE EXPERT SYSTEM - INFERENCE ENGINE")
    print("     Goal-Driven Reasoning via Backward Chaining • Symbolic AI")
    print("=" * 74)
    print("\nRunning diagnosis on benchmark Rice sample input...")
    sample_crop = "Rice"
    sample_symptoms = ["Yellow Leaves", "Brown Spots", "Leaf Drying"]

    result = backward_chaining(crop=sample_crop, symptoms=sample_symptoms)

    print("\n" + "=" * 74)
    print("📋 EXACT DIAGNOSTIC OUTPUT")
    print("=" * 74)
    print(f"  Diagnostic Status:     {result['status']}")
    print(f"  Target Crop:           {result['crop']}")
    print(f"  Disease Identified:    {result['disease_identified']}")
    print(f"  Recommended Treatment: {result['recommended_treatment']}")
    print(f"  Confidence Rating:     {result['confidence']}")
    print(f"  Algorithm Used:        {result['algorithm_used']}")
    print(f"  Knowledge Base Rule:   {result.get('rule_fired', 'N/A')}")
    print(f"  Verified Symptoms:     {', '.join(result['verified_symptoms'])}")

    print("\n" + "=" * 74)
    print("🧠 HOW THE BACKWARD CHAINING ALGORITHM WORKS")
    print("=" * 74)
    print("  1. Goal-Driven Hypothesis: Sets suspected disease hypothesis as the top goal.")
    print("  2. Sub-Goal Decomposition: Breaks hypothesis into premise symptoms via rules.")
    print("  3. Working Memory Checks : Evaluates known facts; queries farmer only for unknowns.")
    print("  4. Immediate Backtrack   : If any required symptom is absent, refutes hypothesis.")
    print("  5. Deduction & Firing    : Proves goal when all premises hold True and fires rule.")

    print("\n" + "=" * 74)
    print("🔍 HOW THE SYSTEM ARRIVED AT THIS OUTPUT (STEP-BY-STEP DERIVATION)")
    print("=" * 74)
    print(f"  Target Crop: '{result['crop']}'")
    print(f"  Active Rule: {result.get('rule_fired', 'N/A')}")
    print("  Production Rule Formula:")
    print(f"    IF Crop is '{result['crop']}'")
    for s in result['verified_symptoms']:
        print(f"      AND Symptom '{s}' is PRESENT")
    print(f"    THEN Disease is '{result['disease_identified']}' (Confidence: {result['confidence']})")
    print(f"      AND Treatment is '{result['recommended_treatment']}'\n")
    print("  Derivation Walkthrough:")
    print(f"    • Step 1: Pushed Top Goal -> Prove '{result['disease_identified']}'")
    for idx, s in enumerate(result['verified_symptoms'], 1):
        print(f"    • Step {idx+1}: Evaluated Sub-Goal '{s}' -> Found in Working Memory [TRUE]")
    print(f"    • Conclusion: All required premises satisfied -> Rule {result.get('rule_fired')} fired!")

    print("\n" + "=" * 74)
    print("📜 BACKWARD CHAINING EXECUTION TRACE")
    print("=" * 74)
    print(f"{'Step':<6} {'Action':<20} {'Reasoning Details'}")
    print("-" * 74)
    for step in result.get("reasoning_trace", []):
        print(f"#{step.get('step', ''):<5} {step.get('action', ''):<20} {step.get('message', '')}")
    print("=" * 74 + "\n")
