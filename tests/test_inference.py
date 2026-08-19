"""
Unit Tests for Two-Stage Forward Chaining & Candidate Ranking Inference Engine.
Covers all 8 test scenarios specified in section 11.
"""

import json
import os
import unittest
from inference import forward_chaining, calculate_candidate_ranking


class TestForwardChainingInference(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        kb_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base.json")
        with open(kb_path, "r", encoding="utf-8") as f:
            cls.kb_data = json.load(f)

    def test_1_strong_disease_match_forward_chaining(self):
        """Test 1: Strong disease match through Forward Chaining (Tomato Early Blight)"""
        facts = {
            "crop": "tomato",
            "leaf_spots": "yes",
            "brown_spots": "yes",
            "lower_leaves_affected": "yes",
            "high_humidity": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["state"], "STRONG_MATCH")
        self.assertEqual(result["status_label"], "Strong Match")
        self.assertEqual(result["disease_key"], "tomato_early_blight")
        self.assertEqual(result["fired_rules"], ["R1", "R2", "R3", "R4"])
        self.assertFalse(result["no_definitive_rule_triggered"])
        self.assertIn("strongly match", result["recommendation"])

    def test_2_partial_symptom_match(self):
        """Test 2: Partial symptom match (No rule fires, suggests possible disease candidate)"""
        facts = {
            "crop": "tomato",
            "water_soaked_spots": "yes",
            "high_humidity": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["state"], "POSSIBLE_DISEASE")
        self.assertEqual(result["status_label"], "Possible")
        self.assertEqual(result["disease_key"], "tomato_late_blight")
        self.assertGreaterEqual(result["match_score"], 50.0)
        self.assertTrue(result["no_definitive_rule_triggered"])
        self.assertIn("suggest this disease as a possibility", result["recommendation"])

    def test_3_very_weak_symptoms(self):
        """Test 3: Very weak symptoms returning Insufficient Evidence"""
        facts = {
            "crop": "tomato",
            "leaf_spots": "yes"
            # Only 1 symptom out of 4 (25% < 50% threshold)
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["state"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["status_label"], "Insufficient Evidence")
        self.assertIsNone(result["disease_key"])
        self.assertEqual(result["disease_name"], "Insufficient Evidence")
        self.assertTrue(result["no_definitive_rule_triggered"])
        self.assertIn("Not enough information", result["recommendation"])

    def test_4_multiple_possible_diseases_ranking(self):
        """Test 4: Multiple possible diseases ranked correctly by match score"""
        facts = {
            "crop": "tomato",
            "water_soaked_spots": "yes",
            "high_humidity": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        alternatives = result["possible_alternatives"]
        self.assertGreater(len(alternatives), 1)
        # Verify descending order of match scores
        for i in range(len(alternatives) - 1):
            self.assertGreaterEqual(alternatives[i]["match_score"], alternatives[i + 1]["match_score"])

    def test_5_wrong_crop_exclusion(self):
        """Test 5: Diseases from unrelated crops are excluded"""
        facts = {
            "crop": "mango",
            "black_stem": "yes"
        }
        # potato_blackleg has black_stem, but crop is mango, so potato_blackleg should be excluded
        candidates = calculate_candidate_ranking(facts, self.kb_data)
        candidate_keys = [c["disease_key"] for c in candidates]
        self.assertNotIn("potato_blackleg", candidate_keys)
        for cand in candidates:
            self.assertEqual(cand["crop"].lower(), "mango")

    def test_6_no_symptoms(self):
        """Test 6: Empty symptoms input returning Insufficient Evidence"""
        facts = {"crop": "tomato"}
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["state"], "INSUFFICIENT_EVIDENCE")
        self.assertIsNone(result["disease_key"])
        self.assertEqual(len(result["fired_rules"]), 0)
        self.assertIn("Not enough information", result["recommendation"])

    def test_7_explanation_generation(self):
        """Test 7: Matched and missing symptoms correctly populated in explanation"""
        facts = {
            "crop": "tomato",
            "water_soaked_spots": "yes",
            "high_humidity": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        explanation = result["explanation"]
        self.assertIn("matched", explanation)
        self.assertIn("missing", explanation)
        self.assertTrue(any("Dark / Water-soaked Lesions" in item for item in explanation["matched"]))
        self.assertTrue(any("Powdery / Mold Growth" in item for item in explanation["missing"]))

    def test_8_forward_chaining_trace_accuracy(self):
        """Test 8: Reasoning trace accurately contains only actually fired rules"""
        facts = {
            "crop": "tomato",
            "leaf_spots": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(len(result["fired_rules"]), 1)
        self.assertEqual(result["fired_rules"], ["R1"])
        self.assertEqual(len(result["reasoning_trace"]), 1)
        self.assertEqual(result["reasoning_trace"][0]["rule_id"], "R1")
        # Ensure no fake rule firing was added to force a diagnosis
        self.assertNotEqual(result["state"], "STRONG_MATCH")


if __name__ == "__main__":
    unittest.main()
