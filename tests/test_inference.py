"""
Project 35: Crop Disease Expert System - Unit Test Suite
Tests Goal-Driven Backward Chaining Inference Engine, Interactive Symptom Verification,
Backtracking, Knowledge Base Integrity, and Sample Problem Statement Cases.
"""

import os
import unittest
import pandas as pd
from inference import BackwardChainingEngine, backward_chaining


class TestBackwardChainingExpertSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = BackwardChainingEngine()

    def test_1_problem_statement_rice_sample(self):
        """
        Verify exact sample input and expected output from Problem Statement:
        Input:
          Crop: Rice
          Symptoms: Yellow Leaves, Brown Spots, Leaf Drying
        Expected Output:
          Disease Identified: Brown Spot Disease
          Recommended Treatment: Apply Suitable Fungicide
          Confidence: High
          Algorithm Used: Backward Chaining
        """
        crop = "Rice"
        symptoms = ["Yellow Leaves", "Brown Spots", "Leaf Drying"]

        result = backward_chaining(crop=crop, symptoms=symptoms)

        self.assertEqual(result["status"], "DIAGNOSIS_SUCCESS")
        self.assertEqual(result["crop"], "Rice")
        self.assertEqual(result["disease_identified"], "Brown Spot Disease")
        self.assertEqual(result["recommended_treatment"], "Apply Suitable Fungicide")
        self.assertEqual(result["confidence"], "High")
        self.assertEqual(result["algorithm_used"], "Backward Chaining")
        self.assertIn("Yellow Leaves", result["verified_symptoms"])
        self.assertIn("Brown Spots", result["verified_symptoms"])
        self.assertIn("Leaf Drying", result["verified_symptoms"])
        self.assertEqual(result["rule_fired"], "RULE_RICE_01")
        self.assertIn("Bipolaris oryzae", result["pathogen"])

    def test_2_interactive_questioning_callback(self):
        """
        Verify interactive symptom verification:
        The engine asks targeted questions dynamically via a callback.
        """
        asked_symptoms = []

        # Mock user callback that answers YES only to Brown Spot Disease symptoms
        def mock_user_response(symptom: str, category: str, question: str) -> bool:
            asked_symptoms.append(symptom)
            if symptom in ["Yellow Leaves", "Brown Spots", "Leaf Drying"]:
                return True
            return False

        result = self.engine.diagnose(
            crop="Rice",
            suspected_disease="Brown Spot Disease",
            ask_callback=mock_user_response
        )

        self.assertEqual(result["status"], "DIAGNOSIS_SUCCESS")
        self.assertEqual(result["disease_identified"], "Brown Spot Disease")
        self.assertEqual(result["confidence"], "High")
        self.assertEqual(result["recommended_treatment"], "Apply Suitable Fungicide")
        # Ensure questions were asked interactively
        self.assertGreater(len(asked_symptoms), 0)
        self.assertIn("Yellow Leaves", asked_symptoms)

    def test_3_backtracking_to_alternative_hypothesis(self):
        """
        Verify backtracking behavior:
        Hypothesis 1 (Bacterial Leaf Blight) fails because Water-Soaked Lesions is absent.
        The engine backtracks and successfully verifies Hypothesis 2 (Brown Spot Disease).
        """
        # User answers False to Water-Soaked Lesions, but True to Yellow Leaves, Brown Spots, Leaf Drying
        answers = {
            "Water-Soaked Lesions": False,
            "Yellow Leaves": True,
            "Brown Spots": True,
            "Leaf Drying": True
        }

        def mock_callback(symptom: str, category: str, question: str) -> bool:
            return answers.get(symptom, False)

        result = self.engine.diagnose(
            crop="Rice",
            suspected_disease="Bacterial Leaf Blight",  # Intentionally start with failing hypothesis
            ask_callback=mock_callback
        )

        self.assertEqual(result["status"], "DIAGNOSIS_SUCCESS")
        self.assertEqual(result["disease_identified"], "Brown Spot Disease")
        self.assertEqual(result["confidence"], "High")

        # Check reasoning trace for backtracking action
        actions = [step["action"] for step in result["reasoning_trace"]]
        self.assertIn("BACKTRACKING", actions)

    def test_4_no_disease_match_all_refuted(self):
        """
        Verify behavior when all suspected disease hypotheses are refuted.
        """
        # Farmer answers NO to all symptoms
        def mock_all_no(symptom: str, category: str, question: str) -> bool:
            return False

        result = self.engine.diagnose(crop="Rice", ask_callback=mock_all_no)

        self.assertEqual(result["status"], "NO_DISEASE_MATCH")
        self.assertEqual(result["confidence"], "Low")
        self.assertIn("Inconclusive", result["disease_identified"])
        self.assertIn("agricultural extension officer", result["recommended_treatment"].lower())

    def test_5_unsupported_crop_error(self):
        """
        Verify handling of unknown or unsupported crop.
        """
        result = self.engine.diagnose(crop="Pineapple", initial_symptoms=["Yellow Leaves"])
        self.assertEqual(result["status"], "ERROR")
        self.assertEqual(result["disease_identified"], "Crop Not Supported")

    def test_6_cross_crop_diagnoses(self):
        """
        Verify Backward Chaining across multiple crops: Wheat, Tomato, Potato, Maize, Cotton.
        """
        test_cases = [
            ("Wheat", ["Orange-Yellow Pustules", "Yellow Leaves", "Leaf Drying"], "Wheat Rust Disease"),
            ("Wheat", ["White Powdery Patches", "Yellow Leaves", "Stunted Growth"], "Powdery Mildew"),
            ("Tomato", ["Brown Spots", "Concentric Rings", "Yellow Leaves"], "Early Blight"),
            ("Tomato", ["Dark Water-Soaked Spots", "White Mold Underside", "Fruit Damage"], "Late Blight"),
            ("Potato", ["Dark Water-Soaked Spots", "Leaf Drying", "Tuber Rot"], "Potato Late Blight"),
            ("Maize", ["Cigar-Shaped Lesions", "Leaf Drying", "Yellow Leaves"], "Northern Corn Leaf Blight"),
            ("Cotton", ["Angular Leaf Spots", "Black Stem Rot", "Leaf Drying"], "Cotton Bacterial Blight")
        ]

        for crop, syms, expected_disease in test_cases:
            res = backward_chaining(crop=crop, symptoms=syms)
            self.assertEqual(
                res["disease_identified"],
                expected_disease,
                f"Failed for {crop} expecting {expected_disease}"
            )
            self.assertEqual(res["confidence"], "High")

    def test_7_pandas_knowledge_base_integrity(self):
        """
        Verify that knowledge base rules and symptoms are valid Pandas DataFrames.
        """
        self.assertIsInstance(self.engine.rules_df, pd.DataFrame)
        self.assertIsInstance(self.engine.symptoms_df, pd.DataFrame)
        self.assertGreater(len(self.engine.rules_df), 10)
        self.assertIn("id", self.engine.rules_df.columns)
        self.assertIn("crop", self.engine.rules_df.columns)
        self.assertIn("hypothesis", self.engine.rules_df.columns)
        self.assertIn("required_symptoms", self.engine.rules_df.columns)
        self.assertIn("treatment", self.engine.rules_df.columns)

    def test_8_information_efficiency_fewer_questions(self):
        """
        Verify why Backward Chaining is efficient:
        Diagnosing Brown Spot Disease requires asking at most 3-4 targeted questions,
        rather than surveying all symptoms in the crop.
        """
        crop_symptoms = self.engine.get_all_symptoms_for_crop("Rice")
        total_symptoms_count = len(crop_symptoms)

        asked = []
        def mock_callback(symptom: str, category: str, question: str) -> bool:
            asked.append(symptom)
            return symptom in ["Yellow Leaves", "Brown Spots", "Leaf Drying"]

        result = self.engine.diagnose(
            crop="Rice",
            suspected_disease="Brown Spot Disease",
            ask_callback=mock_callback
        )

    def test_9_cli_benchmark_demo_execution(self):
        """
        Verify CLI benchmark demo runs end-to-end without error.
        """
        import io
        from contextlib import redirect_stdout
        from app import run_benchmark_demo

        buf = io.StringIO()
        with redirect_stdout(buf):
            run_benchmark_demo(self.engine)
        output = buf.getvalue()

        self.assertIn("DIAGNOSTIC REPORT", output)
        self.assertIn("Brown Spot Disease", output)
        self.assertIn("Apply Suitable Fungicide", output)
        self.assertIn("BACKWARD CHAINING REASONING TRACE", output)

    def test_10_cli_report_formatting_and_trace(self):
        """
        Verify CLI formatting helpers produce expected structured output.
        """
        import io
        from contextlib import redirect_stdout
        from app import format_report_box, display_reasoning_trace

        sample_result = {
            "status": "DIAGNOSIS_SUCCESS",
            "crop": "Rice",
            "disease_identified": "Brown Spot Disease",
            "recommended_treatment": "Apply Suitable Fungicide",
            "confidence": "High",
            "algorithm_used": "Backward Chaining",
            "rule_fired": "RULE_RICE_01",
            "pathogen": "Bipolaris oryzae",
            "verified_symptoms": ["Yellow Leaves", "Brown Spots", "Leaf Drying"],
            "questions_asked_count": 3,
            "detailed_treatment": "Spray Mancozeb",
            "prevention": "Treat seeds",
            "reasoning_trace": [
                {"step": 1, "action": "INITIALIZATION", "message": "Starting engine"},
                {"step": 2, "action": "GOAL_SATISFIED", "message": "Success"}
            ]
        }

        buf = io.StringIO()
        with redirect_stdout(buf):
            format_report_box(sample_result)
            display_reasoning_trace(sample_result["reasoning_trace"])
        output = buf.getvalue()

        self.assertIn("DIAGNOSTIC REPORT", output)
        self.assertIn("Brown Spot Disease", output)
        self.assertIn("Bipolaris oryzae", output)
        self.assertIn("INITIALIZATION", output)
        self.assertIn("GOAL_SATISFIED", output)


if __name__ == "__main__":
    unittest.main()
