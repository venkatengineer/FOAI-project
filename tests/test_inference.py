"""
Unit Tests for Forward Chaining Inference Engine.
Covers 8 core test scenarios.
"""

import unittest
from api_connector import load_knowledge_base
from inference import forward_chaining


class TestForwardChainingInference(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kb_data, cls.source = load_knowledge_base()

    def test_1_tomato_early_blight(self):
        """Test 1: Correct disease identification (Tomato Early Blight multi-step chaining)"""
        facts = {
            "crop": "tomato",
            "leaf_spots": "yes",
            "spot_color_brown": "yes",
            "lower_leaves_affected": "yes",
            "humidity_high": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["disease_key"], "tomato_early_blight")
        self.assertEqual(result["disease_name"], "Tomato Early Blight")
        self.assertEqual(result["fired_rules"], ["R1", "R2", "R3", "R4"])

    def test_2_potato_blackleg(self):
        """Test 2: Different crop disease identification (Potato Blackleg)"""
        facts = {
            "crop": "potato",
            "black_stem": "yes",
            "wilting": "yes",
            "humidity_high": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["disease_key"], "potato_blackleg")
        self.assertEqual(result["disease_name"], "Potato Blackleg")
        self.assertEqual(result["fired_rules"], ["R12", "R13", "R14"])

    def test_3_rice_blast(self):
        """Test 3: Different crop disease identification (Rice Blast)"""
        facts = {
            "crop": "rice",
            "lesions": "yes",
            "spindle_spots": "yes",
            "humidity_high": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertEqual(result["disease_key"], "rice_blast")
        self.assertEqual(result["disease_name"], "Rice Blast")
        self.assertIn("R18", result["fired_rules"])

    def test_4_missing_symptoms(self):
        """Test 4: Missing symptoms (Incomplete facts)"""
        facts = {
            "crop": "tomato",
            "leaf_spots": "yes"
            # Missing spot color, lower leaves, humidity
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertIsNone(result["disease_key"])
        self.assertEqual(result["disease_name"], "Unknown / Healthy (No Disease Matched)")
        self.assertEqual(result["fired_rules"], ["R1"])  # Only R1 fires

    def test_5_no_matching_disease(self):
        """Test 5: Unmatched symptom combination"""
        facts = {
            "crop": "tomato",
            "black_stem": "yes" # Black stem is potato rule, not tomato
        }
        result = forward_chaining(facts, self.kb_data)
        self.assertIsNone(result["disease_key"])
        self.assertEqual(len(result["fired_rules"]), 0)

    def test_6_multi_step_chaining_trace(self):
        """Test 6: Multi-step rule chaining sequence trace validation"""
        facts = {
            "crop": "tomato",
            "leaf_spots": "yes",
            "spot_color_brown": "yes",
            "lower_leaves_affected": "yes",
            "humidity_high": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        trace = result["reasoning_trace"]
        self.assertEqual(len(trace), 4)
        self.assertEqual(trace[0]["rule_id"], "R1")
        self.assertEqual(trace[1]["rule_id"], "R2")
        self.assertEqual(trace[2]["rule_id"], "R3")
        self.assertEqual(trace[3]["rule_id"], "R4")

    def test_7_multiple_applicable_rules(self):
        """Test 7: Multiple applicable rules execution without infinite loops"""
        facts = {
            "crop": "potato",
            "leaf_spots": "yes",
            "concentric_rings": "yes",
            "lower_leaves_affected": "yes",
            "black_stem": "yes",
            "wilting": "yes",
            "humidity_high": "yes"
        }
        result = forward_chaining(facts, self.kb_data)
        # Should resolve rules deterministically
        self.assertIsNotNone(result["disease_key"])

    def test_8_invalid_input(self):
        """Test 8: Invalid / empty input handling"""
        facts = {}
        result = forward_chaining(facts, self.kb_data)
        self.assertIsNone(result["disease_key"])
        self.assertEqual(len(result["fired_rules"]), 0)


if __name__ == "__main__":
    unittest.main()
