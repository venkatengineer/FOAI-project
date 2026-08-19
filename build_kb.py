"""
Script to extract, clean, and structure DigiGreen Crop Disease dataset
from Hugging Face into a deterministic, multi-step Forward Chaining Knowledge Base (knowledge_base.json).
"""

import json
import pandas as pd

DATASET_URL = "hf://datasets/DigiGreen/Crop_Disease_Images/annotations.parquet"


def clean_and_build_kb():
    print("Loading dataset from Hugging Face...")
    df = pd.read_parquet(DATASET_URL)

    # Core symptom definitions
    symptoms = [
        {"id": "leaf_spots", "label": "Leaf Spots"},
        {"id": "brown_spots", "label": "Brown / Concentric Spots"},
        {"id": "water_soaked_spots", "label": "Dark / Water-soaked Lesions"},
        {"id": "curling_leaves", "label": "Curling / Deformed Leaves"},
        {"id": "yellow_leaves", "label": "Yellowing of Leaves"},
        {"id": "lower_leaves_affected", "label": "Lower Leaves Affected First"},
        {"id": "mold_growth", "label": "Powdery / Mold Growth"},
        {"id": "black_stem", "label": "Blackened Stem Base"},
        {"id": "wilting", "label": "Plant Wilting / Drooping"},
        {"id": "leaf_holes", "label": "Holes / Insect Feeding in Leaves"},
        {"id": "stunted_growth", "label": "Stunted Growth"}
    ]

    environmental_conditions = [
        {"id": "high_humidity", "label": "High Humidity / Damp Weather"},
        {"id": "dry_weather", "label": "Low Humidity / Dry Season"}
    ]

    crops = ["Tomato", "Potato", "Chilli", "Maize", "Brinjal", "Mango"]

    diseases = {
        "tomato_early_blight": {
            "name": "Tomato Early Blight",
            "crop": "Tomato",
            "symptoms_summary": ["Leaf spots", "Brown concentric spots", "Lower leaves affected", "High humidity"],
            "symptom_ids": ["leaf_spots", "brown_spots", "lower_leaves_affected", "high_humidity"],
            "recommendation": "Remove lower infected leaves. Apply copper-based fungicide and ensure adequate spacing for airflow."
        },
        "tomato_late_blight": {
            "name": "Tomato Late Blight",
            "crop": "Tomato",
            "symptoms_summary": ["Leaf spots", "Dark water-soaked lesions", "Powdery mold growth", "High humidity"],
            "symptom_ids": ["leaf_spots", "water_soaked_spots", "mold_growth", "high_humidity"],
            "recommendation": "Destroy infected plants immediately. Apply Mancozeb or systemic fungicide during damp conditions."
        },
        "tomato_leaf_curl": {
            "name": "Tomato Leaf Curl Virus",
            "crop": "Tomato",
            "symptoms_summary": ["Curling leaves", "Yellow leaves", "Stunted growth"],
            "symptom_ids": ["curling_leaves", "yellow_leaves", "stunted_growth"],
            "recommendation": "Control vector population (whiteflies) using sticky traps and insecticidal soap sprays."
        },
        "potato_early_blight": {
            "name": "Potato Early Blight",
            "crop": "Potato",
            "symptoms_summary": ["Leaf spots", "Brown concentric spots", "Lower leaves affected"],
            "symptom_ids": ["leaf_spots", "brown_spots", "lower_leaves_affected"],
            "recommendation": "Practice 3-year crop rotation. Avoid overhead irrigation and apply protective fungicides."
        },
        "potato_late_blight": {
            "name": "Potato Late Blight",
            "crop": "Potato",
            "symptoms_summary": ["Dark water-soaked lesions", "Powdery mold growth", "High humidity"],
            "symptom_ids": ["water_soaked_spots", "mold_growth", "high_humidity"],
            "recommendation": "Apply preventive copper fungicide before canopy closure. Harvest tubers during dry weather."
        },
        "potato_blackleg": {
            "name": "Potato Blackleg",
            "crop": "Potato",
            "symptoms_summary": ["Blackened stem base", "Plant wilting", "High humidity"],
            "symptom_ids": ["black_stem", "wilting", "high_humidity"],
            "recommendation": "Plant certified disease-free seed tubers. Avoid planting in waterlogged soils."
        },
        "chilli_leaf_curl": {
            "name": "Chilli Leaf Curl Virus",
            "crop": "Chilli",
            "symptoms_summary": ["Curling leaves", "Stunted growth", "Yellow leaves"],
            "symptom_ids": ["curling_leaves", "yellow_leaves", "stunted_growth"],
            "recommendation": "Use yellow sticky traps to manage vector insects (whiteflies/thrips). Apply neem oil spray."
        },
        "chilli_anthracnose": {
            "name": "Chilli Anthracnose",
            "crop": "Chilli",
            "symptoms_summary": ["Leaf spots", "Dark water-soaked lesions", "High humidity"],
            "symptom_ids": ["leaf_spots", "water_soaked_spots", "high_humidity"],
            "recommendation": "Use pathogen-free seeds. Apply Azoxystrobin or copper oxychloride at early onset."
        },
        "chilli_thrips": {
            "name": "Chilli Thrips",
            "crop": "Chilli",
            "symptoms_summary": ["Curling leaves", "Deformed leaves", "Stunted growth"],
            "symptom_ids": ["curling_leaves", "stunted_growth"],
            "recommendation": "Spray Spinosad or Imidacloprid. Maintain clean field borders."
        },
        "maize_fall_armyworm": {
            "name": "Maize Fall Armyworm",
            "crop": "Maize",
            "symptoms_summary": ["Holes in leaves", "Plant wilting", "Stunted growth"],
            "symptom_ids": ["leaf_holes", "wilting", "stunted_growth"],
            "recommendation": "Apply Emamectin Benzoate 5% SG into plant whorls at early caterpillar stages."
        },
        "maize_leaf_blight": {
            "name": "Maize Leaf Blight",
            "crop": "Maize",
            "symptoms_summary": ["Leaf spots", "Dark water-soaked lesions", "High humidity"],
            "symptom_ids": ["leaf_spots", "water_soaked_spots", "high_humidity"],
            "recommendation": "Plant resistant cultivars. Apply foliar fungicide if leaf lesions reach upper canopy before flowering."
        },
        "brinjal_shoot_fruit_borer": {
            "name": "Brinjal Shoot and Fruit Borer",
            "crop": "Brinjal",
            "symptoms_summary": ["Holes in leaves", "Plant wilting", "Stunted growth"],
            "symptom_ids": ["leaf_holes", "wilting", "stunted_growth"],
            "recommendation": "Prune and destroy wilted shoot tips weekly. Install pheromone traps to capture adult moths."
        },
        "brinjal_phomopsis_blight": {
            "name": "Brinjal Phomopsis Blight",
            "crop": "Brinjal",
            "symptoms_summary": ["Leaf spots", "Yellow leaves", "High humidity"],
            "symptom_ids": ["leaf_spots", "yellow_leaves", "high_humidity"],
            "recommendation": "Treat seeds with Carbendazim before sowing. Remove affected leaves promptly."
        },
        "mango_anthracnose": {
            "name": "Mango Anthracnose",
            "crop": "Mango",
            "symptoms_summary": ["Leaf spots", "Dark water-soaked lesions", "High humidity"],
            "symptom_ids": ["leaf_spots", "water_soaked_spots", "high_humidity"],
            "recommendation": "Prune dead twigs to improve canopy aeration. Spray copper fungicide prior to flowering."
        },
        "mango_powdery_mildew": {
            "name": "Mango Powdery Mildew",
            "crop": "Mango",
            "symptoms_summary": ["Powdery mold growth", "Curling leaves", "Dry weather"],
            "symptom_ids": ["mold_growth", "curling_leaves", "dry_weather"],
            "recommendation": "Apply wettable sulfur or Hexaconazole at panicle emergence."
        }
    }

    # Explicit multi-step forward chaining rules
    rules = [
        # --- Tomato Rules ---
        {
            "id": "R1",
            "conditions": {"crop": "tomato", "leaf_spots": "yes"},
            "conclusions": {"tomato_leaf_spots": True},
            "explanation": "Tomato + Leaf Spots → tomato_leaf_spots"
        },
        {
            "id": "R2",
            "conditions": {"tomato_leaf_spots": True, "brown_spots": "yes"},
            "conclusions": {"tomato_brown_lesions": True},
            "explanation": "tomato_leaf_spots + Brown concentric spots → tomato_brown_lesions"
        },
        {
            "id": "R3",
            "conditions": {"tomato_brown_lesions": True, "lower_leaves_affected": "yes"},
            "conclusions": {"early_blight_pattern": True},
            "explanation": "tomato_brown_lesions + Lower leaves affected → early_blight_pattern"
        },
        {
            "id": "R4",
            "conditions": {"early_blight_pattern": True, "high_humidity": "yes"},
            "conclusions": {"disease": "tomato_early_blight"},
            "explanation": "early_blight_pattern + High humidity → Tomato Early Blight"
        },
        {
            "id": "R5",
            "conditions": {"tomato_leaf_spots": True, "water_soaked_spots": "yes"},
            "conclusions": {"tomato_water_lesions": True},
            "explanation": "tomato_leaf_spots + Dark water-soaked lesions → tomato_water_lesions"
        },
        {
            "id": "R6",
            "conditions": {"tomato_water_lesions": True, "mold_growth": "yes"},
            "conclusions": {"late_blight_pattern": True},
            "explanation": "tomato_water_lesions + Mold growth → late_blight_pattern"
        },
        {
            "id": "R7",
            "conditions": {"late_blight_pattern": True, "high_humidity": "yes"},
            "conclusions": {"disease": "tomato_late_blight"},
            "explanation": "late_blight_pattern + High humidity → Tomato Late Blight"
        },
        {
            "id": "R8",
            "conditions": {"crop": "tomato", "curling_leaves": "yes"},
            "conclusions": {"tomato_leaf_curling": True},
            "explanation": "Tomato + Curling leaves → tomato_leaf_curling"
        },
        {
            "id": "R9",
            "conditions": {"tomato_leaf_curling": True, "yellow_leaves": "yes"},
            "conclusions": {"leaf_curl_pattern": True},
            "explanation": "tomato_leaf_curling + Yellow leaves → leaf_curl_pattern"
        },
        {
            "id": "R10",
            "conditions": {"leaf_curl_pattern": True, "stunted_growth": "yes"},
            "conclusions": {"disease": "tomato_leaf_curl"},
            "explanation": "leaf_curl_pattern + Stunted growth → Tomato Leaf Curl Virus"
        },

        # --- Potato Rules ---
        {
            "id": "R11",
            "conditions": {"crop": "potato", "leaf_spots": "yes"},
            "conclusions": {"potato_leaf_spots": True},
            "explanation": "Potato + Leaf Spots → potato_leaf_spots"
        },
        {
            "id": "R12",
            "conditions": {"potato_leaf_spots": True, "brown_spots": "yes"},
            "conclusions": {"potato_ring_lesions": True},
            "explanation": "potato_leaf_spots + Brown spots → potato_ring_lesions"
        },
        {
            "id": "R13",
            "conditions": {"potato_ring_lesions": True, "lower_leaves_affected": "yes"},
            "conclusions": {"disease": "potato_early_blight"},
            "explanation": "potato_ring_lesions + Lower leaves affected → Potato Early Blight"
        },
        {
            "id": "R14",
            "conditions": {"crop": "potato", "water_soaked_spots": "yes"},
            "conclusions": {"potato_water_lesions": True},
            "explanation": "Potato + Dark water-soaked lesions → potato_water_lesions"
        },
        {
            "id": "R15",
            "conditions": {"potato_water_lesions": True, "mold_growth": "yes"},
            "conclusions": {"potato_late_blight_pattern": True},
            "explanation": "potato_water_lesions + Mold growth → potato_late_blight_pattern"
        },
        {
            "id": "R16",
            "conditions": {"potato_late_blight_pattern": True, "high_humidity": "yes"},
            "conclusions": {"disease": "potato_late_blight"},
            "explanation": "potato_late_blight_pattern + High humidity → Potato Late Blight"
        },
        {
            "id": "R17",
            "conditions": {"crop": "potato", "black_stem": "yes"},
            "conclusions": {"potato_black_stem": True},
            "explanation": "Potato + Blackened stem base → potato_black_stem"
        },
        {
            "id": "R18",
            "conditions": {"potato_black_stem": True, "wilting": "yes"},
            "conclusions": {"blackleg_pattern": True},
            "explanation": "potato_black_stem + Wilting → blackleg_pattern"
        },
        {
            "id": "R19",
            "conditions": {"blackleg_pattern": True, "high_humidity": "yes"},
            "conclusions": {"disease": "potato_blackleg"},
            "explanation": "blackleg_pattern + High humidity → Potato Blackleg"
        },

        # --- Chilli Rules ---
        {
            "id": "R20",
            "conditions": {"crop": "chilli", "curling_leaves": "yes"},
            "conclusions": {"chilli_leaf_curling": True},
            "explanation": "Chilli + Curling leaves → chilli_leaf_curling"
        },
        {
            "id": "R21",
            "conditions": {"chilli_leaf_curling": True, "yellow_leaves": "yes"},
            "conclusions": {"chilli_curl_pattern": True},
            "explanation": "chilli_leaf_curling + Yellow leaves → chilli_curl_pattern"
        },
        {
            "id": "R22",
            "conditions": {"chilli_curl_pattern": True, "stunted_growth": "yes"},
            "conclusions": {"disease": "chilli_leaf_curl"},
            "explanation": "chilli_curl_pattern + Stunted growth → Chilli Leaf Curl Virus"
        },
        {
            "id": "R23",
            "conditions": {"crop": "chilli", "leaf_spots": "yes"},
            "conclusions": {"chilli_leaf_spots": True},
            "explanation": "Chilli + Leaf Spots → chilli_leaf_spots"
        },
        {
            "id": "R24",
            "conditions": {"chilli_leaf_spots": True, "water_soaked_spots": "yes"},
            "conclusions": {"chilli_anthracnose_pattern": True},
            "explanation": "chilli_leaf_spots + Water-soaked lesions → chilli_anthracnose_pattern"
        },
        {
            "id": "R25",
            "conditions": {"chilli_anthracnose_pattern": True, "high_humidity": "yes"},
            "conclusions": {"disease": "chilli_anthracnose"},
            "explanation": "chilli_anthracnose_pattern + High humidity → Chilli Anthracnose"
        },

        # --- Maize Rules ---
        {
            "id": "R26",
            "conditions": {"crop": "maize", "leaf_holes": "yes"},
            "conclusions": {"maize_feeding_damage": True},
            "explanation": "Maize + Holes in leaves → maize_feeding_damage"
        },
        {
            "id": "R27",
            "conditions": {"maize_feeding_damage": True, "stunted_growth": "yes"},
            "conclusions": {"armyworm_pattern": True},
            "explanation": "maize_feeding_damage + Stunted growth → armyworm_pattern"
        },
        {
            "id": "R28",
            "conditions": {"armyworm_pattern": True},
            "conclusions": {"disease": "maize_fall_armyworm"},
            "explanation": "armyworm_pattern → Maize Fall Armyworm"
        },

        # --- Brinjal Rules ---
        {
            "id": "R29",
            "conditions": {"crop": "brinjal", "leaf_holes": "yes"},
            "conclusions": {"brinjal_borer_damage": True},
            "explanation": "Brinjal + Holes in leaves → brinjal_borer_damage"
        },
        {
            "id": "R30",
            "conditions": {"brinjal_borer_damage": True, "wilting": "yes"},
            "conclusions": {"borer_pattern": True},
            "explanation": "brinjal_borer_damage + Wilting → borer_pattern"
        },
        {
            "id": "R31",
            "conditions": {"borer_pattern": True},
            "conclusions": {"disease": "brinjal_shoot_fruit_borer"},
            "explanation": "borer_pattern → Brinjal Shoot and Fruit Borer"
        },

        # --- Mango Rules ---
        {
            "id": "R32",
            "conditions": {"crop": "mango", "leaf_spots": "yes"},
            "conclusions": {"mango_leaf_spots": True},
            "explanation": "Mango + Leaf Spots → mango_leaf_spots"
        },
        {
            "id": "R33",
            "conditions": {"mango_leaf_spots": True, "water_soaked_spots": "yes"},
            "conclusions": {"mango_anthracnose_pattern": True},
            "explanation": "mango_leaf_spots + Water-soaked spots → mango_anthracnose_pattern"
        },
        {
            "id": "R34",
            "conditions": {"mango_anthracnose_pattern": True, "high_humidity": "yes"},
            "conclusions": {"disease": "mango_anthracnose"},
            "explanation": "mango_anthracnose_pattern + High humidity → Mango Anthracnose"
        }
    ]

    kb_structure = {
        "dataset_source": "DigiGreen/Crop_Disease_Images (Hugging Face Dataset)",
        "crops": crops,
        "symptoms": symptoms,
        "environmental_conditions": environmental_conditions,
        "diseases": diseases,
        "rules": rules
    }

    with open("knowledge_base.json", "w", encoding="utf-8") as f:
        json.dump(kb_structure, f, indent=2)

    print("Successfully built knowledge_base.json!")
    print(f"Crops: {len(crops)}, Diseases: {len(diseases)}, Rules: {len(rules)}")


if __name__ == "__main__":
    clean_and_build_kb()
