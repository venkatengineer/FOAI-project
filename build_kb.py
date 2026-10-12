#!/data/project/.venv/bin/python
"""
Project 35: Crop Disease Expert System - Knowledge Base Builder
Builds and validates the structured agricultural knowledge base using pandas.
Exports to both JSON (knowledge_base.json) and CSV (knowledge_base_rules.csv).
"""

import json
import os
import pandas as pd

OUTPUT_JSON_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
OUTPUT_CSV_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base_rules.csv")


def build_knowledge_base():
    """
    Constructs a rich agricultural knowledge base covering multiple crops,
    diseases, logical rules, targeted symptom categories, and treatments.
    """
    # 1. Supported Crops
    crops = [
        {"id": "rice", "name": "Rice", "description": "Oryza sativa - Staple cereal crop"},
        {"id": "wheat", "name": "Wheat", "description": "Triticum aestivum - Major grain crop"},
        {"id": "tomato", "name": "Tomato", "description": "Solanum lycopersicum - Key horticultural crop"},
        {"id": "potato", "name": "Potato", "description": "Solanum tuberosum - Major tuber crop"},
        {"id": "maize", "name": "Maize", "description": "Zea mays - Versatile cereal crop"},
        {"id": "cotton", "name": "Cotton", "description": "Gossypium hirsutum - Essential fiber crop"}
    ]

    # 2. Symptom Definitions with Categories (Leaf Color, Stem Condition, Fruit Damage, Pest Infestation)
    symptoms = [
        # Rice Symptoms
        {"id": "yellow_leaves", "name": "Yellow Leaves", "category": "Leaf Color", "question": "Are the leaves turning yellow or pale chlorotic?"},
        {"id": "brown_spots", "name": "Brown Spots", "category": "Leaf Condition", "question": "Are there distinct brown oval/circular spots visible on the leaves?"},
        {"id": "leaf_drying", "name": "Leaf Drying", "category": "Stem Condition", "question": "Are the leaf margins or tips drying up and withering?"},
        {"id": "water_soaked_lesions", "name": "Water-Soaked Lesions", "category": "Leaf Condition", "question": "Do you observe translucent, water-soaked streaks or lesions on foliage?"},
        {"id": "spindle_shaped_spots", "name": "Spindle-Shaped Spots", "category": "Leaf Condition", "question": "Are spots diamond/spindle-shaped with pointed ends?"},
        {"id": "ash_gray_center", "name": "Ash Gray Center", "category": "Leaf Color", "question": "Do the leaf lesions have a characteristic grayish or whitish center?"},
        {"id": "panicle_rot", "name": "Panicle Rot", "category": "Fruit Damage", "question": "Is there neck rotting or grain discoloration on the panicles?"},
        {"id": "sheath_lesions", "name": "Sheath Lesions", "category": "Stem Condition", "question": "Are there greenish-gray oval lesions banding on the leaf sheath near waterline?"},
        {"id": "stem_lodging", "name": "Stem Lodging", "category": "Stem Condition", "question": "Is the stem weakened or collapsing (lodging)?"},

        # Wheat Symptoms
        {"id": "orange_yellow_pustules", "name": "Orange-Yellow Pustules", "category": "Leaf Color", "question": "Are powdery orange or yellow pustules present on the leaf surface?"},
        {"id": "white_powdery_patches", "name": "White Powdery Patches", "category": "Leaf Condition", "question": "Are there white talcum-like powdery patches on leaves or stems?"},
        {"id": "black_powdery_spores", "name": "Black Powdery Spores", "category": "Fruit Damage", "question": "Are grains replaced by masses of dark black powdery fungal spores?"},
        {"id": "stunted_growth", "name": "Stunted Growth", "category": "Stem Condition", "question": "Is the plant noticeably stunted in height with delayed development?"},

        # Tomato Symptoms
        {"id": "concentric_rings", "name": "Concentric Rings", "category": "Leaf Condition", "question": "Do leaf spots display concentric circular target-board rings?"},
        {"id": "dark_water_soaked_spots", "name": "Dark Water-Soaked Spots", "category": "Leaf Condition", "question": "Are dark, rapidly expanding water-soaked spots present on leaves and stems?"},
        {"id": "white_mold_underside", "name": "White Mold Underside", "category": "Leaf Condition", "question": "Is there fine white velvety mold growth on the underside of affected leaves?"},
        {"id": "curling_leaves", "name": "Curling Leaves", "category": "Stem Condition", "question": "Are leaves curling upward and becoming leathery or distorted?"},
        {"id": "whitefly_infestation", "name": "Whitefly Infestation", "category": "Pest Infestation", "question": "Are small white insects (whiteflies) fluttering when leaves are shaken?"},
        {"id": "fruit_rot", "name": "Fruit Damage", "category": "Fruit Damage", "question": "Are there sunken dark rot patches on the developing fruits?"},

        # Potato Symptoms
        {"id": "black_stem_rot", "name": "Black Stem Rot", "category": "Stem Condition", "question": "Is the base of the stem turning inky black and rotting?"},
        {"id": "plant_wilting", "name": "Plant Wilting", "category": "Stem Condition", "question": "Are the plants rapidly wilting and collapsing during warm daytime hours?"},
        {"id": "tuber_rot", "name": "Tuber Rot", "category": "Fruit Damage", "question": "Are harvested tubers showing brownish internal dry rot or foul smelling soft rot?"},

        # Maize Symptoms
        {"id": "cigar_shaped_lesions", "name": "Cigar-Shaped Lesions", "category": "Leaf Condition", "question": "Are long, elliptical cigar-shaped grayish lesions visible on leaves?"},
        {"id": "cinnamon_brown_pustules", "name": "Cinnamon-Brown Pustules", "category": "Leaf Color", "question": "Are reddish-brown or cinnamon pustules scattered across both leaf surfaces?"},

        # Cotton Symptoms
        {"id": "angular_leaf_spots", "name": "Angular Leaf Spots", "category": "Leaf Condition", "question": "Are lesions sharply delimited by leaf veinlets, forming angular spots?"},
        {"id": "vascular_browning", "name": "Vascular Browning", "category": "Stem Condition", "question": "When stem is sliced open, do you see brown discolored vascular bundles?"}
    ]

    # 3. Disease Profiles with Recommended Treatments and Pathogens
    diseases = {
        # Rice
        "rice_brown_spot": {
            "id": "rice_brown_spot",
            "name": "Brown Spot Disease",
            "crop": "Rice",
            "pathogen": "Bipolaris oryzae (Fungus)",
            "primary_symptoms": ["Yellow Leaves", "Brown Spots", "Leaf Drying"],
            "treatment": "Apply Suitable Fungicide",
            "detailed_treatment": "Spray Mancozeb (2.5 g/L) or Edifenphos (1 ml/L). Correct soil nutrient imbalance with potassium and nitrogen. Ensure proper drainage.",
            "prevention": "Treat seeds with Carbendazim (2 g/kg). Use balanced fertilizer application and avoid prolonged water stress."
        },
        "rice_bacterial_leaf_blight": {
            "id": "rice_bacterial_leaf_blight",
            "name": "Bacterial Leaf Blight",
            "crop": "Rice",
            "pathogen": "Xanthomonas oryzae pv. oryzae (Bacterium)",
            "primary_symptoms": ["Yellow Leaves", "Water-Soaked Lesions", "Leaf Drying"],
            "treatment": "Spray Copper Hydroxide or Streptocycline",
            "detailed_treatment": "Spray Streptocycline (150 mg/L) combined with Copper Oxychloride (2 g/L). Drain excess standing water from infected fields.",
            "prevention": "Grow resistant rice cultivars (e.g., IR64). Avoid high nitrogen top-dressing during disease outbreaks."
        },
        "rice_blast": {
            "id": "rice_blast",
            "name": "Rice Blast Disease",
            "crop": "Rice",
            "pathogen": "Magnaporthe oryzae (Fungus)",
            "primary_symptoms": ["Spindle-Shaped Spots", "Ash Gray Center", "Panicle Rot"],
            "treatment": "Apply Tricyclazole or Azoxystrobin Fungicide",
            "detailed_treatment": "Foliar spray with Tricyclazole 75 WP (0.6 g/L) or Azoxystrobin (1 ml/L) at booting and panicle emergence stages.",
            "prevention": "Avoid excess nitrogen fertilization; practice clean seed selection and treat seeds with Tricyclazole."
        },
        "rice_sheath_blight": {
            "id": "rice_sheath_blight",
            "name": "Sheath Blight Disease",
            "crop": "Rice",
            "pathogen": "Rhizoctonia solani (Fungus)",
            "primary_symptoms": ["Sheath Lesions", "Yellow Leaves", "Stem Lodging"],
            "treatment": "Apply Hexaconazole or Validamycin",
            "detailed_treatment": "Spray Validamycin 3L (2.5 ml/L) or Hexaconazole 5 EC (2 ml/L) targeted towards the plant base/sheaths.",
            "prevention": "Maintain wider plant spacing to allow ventilation; eliminate alternate weed hosts on field bunds."
        },

        # Wheat
        "wheat_rust": {
            "id": "wheat_rust",
            "name": "Wheat Rust Disease",
            "crop": "Wheat",
            "pathogen": "Puccinia striiformis / Puccinia triticina (Fungus)",
            "primary_symptoms": ["Orange-Yellow Pustules", "Yellow Leaves", "Leaf Drying"],
            "treatment": "Apply Propiconazole Fungicide",
            "detailed_treatment": "Apply Propiconazole 25 EC (1 ml/L) or Tebuconazole upon first appearance of pustules.",
            "prevention": "Sow resistant rust-tolerant certified varieties and avoid unseasonably late planting."
        },
        "wheat_powdery_mildew": {
            "id": "wheat_powdery_mildew",
            "name": "Powdery Mildew",
            "crop": "Wheat",
            "pathogen": "Blumeria graminis f. sp. tritici (Fungus)",
            "primary_symptoms": ["White Powdery Patches", "Yellow Leaves", "Stunted Growth"],
            "treatment": "Apply Wettable Sulfur or Triazole Fungicide",
            "detailed_treatment": "Spray Wettable Sulfur (3 g/L) or Triadimefon (1 g/L) covering both upper and lower canopy surfaces.",
            "prevention": "Ensure good crop aeration and avoid excessively high seed rates."
        },
        "wheat_loose_smut": {
            "id": "wheat_loose_smut",
            "name": "Loose Smut Disease",
            "crop": "Wheat",
            "pathogen": "Ustilago tritici (Fungus)",
            "primary_symptoms": ["Black Powdery Spores", "Panicle Rot", "Stunted Growth"],
            "treatment": "Seed Treatment with Systemic Fungicides",
            "detailed_treatment": "Rogue out infected smutted ear-heads carefully in plastic bags before spores disperse.",
            "prevention": "Solar heat treatment of seeds or chemical dressing with Carboxin / Thiram (2.5 g/kg seed)."
        },

        # Tomato
        "tomato_early_blight": {
            "id": "tomato_early_blight",
            "name": "Early Blight",
            "crop": "Tomato",
            "pathogen": "Alternaria solani (Fungus)",
            "primary_symptoms": ["Brown Spots", "Concentric Rings", "Yellow Leaves"],
            "treatment": "Apply Mancozeb or Chlorothalonil Fungicide",
            "detailed_treatment": "Spray Chlorothalonil (2 g/L) or Mancozeb (2.5 g/L). Prune lower infected leaves touching the soil.",
            "prevention": "Mulch soil around plants and stake tomato vines to avoid soil splash."
        },
        "tomato_late_blight": {
            "id": "tomato_late_blight",
            "name": "Late Blight",
            "crop": "Tomato",
            "pathogen": "Phytophthora infestans (Oomycete)",
            "primary_symptoms": ["Dark Water-Soaked Spots", "White Mold Underside", "Fruit Damage"],
            "treatment": "Apply Metalaxyl or Cymoxanil Fungicide",
            "detailed_treatment": "Spray Metalaxyl + Mancozeb (2 g/L) or Cymoxanil immediately upon dark lesion discovery.",
            "prevention": "Avoid overhead sprinkler irrigation; remove and burn infected plant debris."
        },
        "tomato_leaf_curl": {
            "id": "tomato_leaf_curl",
            "name": "Tomato Leaf Curl Virus",
            "crop": "Tomato",
            "pathogen": "Tomato Leaf Curl New Delhi Virus (Begomovirus)",
            "primary_symptoms": ["Curling Leaves", "Yellow Leaves", "Whitefly Infestation"],
            "treatment": "Control Whitefly Vectors and Rogue Plants",
            "detailed_treatment": "Spray Imidacloprid 17.8 SL (0.3 ml/L) or Neem seed kernel extract (5%) to manage whitefly populations.",
            "prevention": "Install yellow sticky traps (15 traps/acre) and use insect-proof nylon netting in nurseries."
        },

        # Potato
        "potato_late_blight": {
            "id": "potato_late_blight",
            "name": "Potato Late Blight",
            "crop": "Potato",
            "pathogen": "Phytophthora infestans (Oomycete)",
            "primary_symptoms": ["Dark Water-Soaked Spots", "Leaf Drying", "Tuber Rot"],
            "treatment": "Apply Systemic Fungicide (Dimethomorph / Mancozeb)",
            "detailed_treatment": "Foliar spray with Dimethomorph (1 g/L) + Mancozeb (2 g/L) at 7-10 day intervals during cool, humid weather.",
            "prevention": "Plant certified disease-free seed tubers; destroy haulms 10 days before harvesting."
        },
        "potato_blackleg": {
            "id": "potato_blackleg",
            "name": "Blackleg and Soft Rot",
            "crop": "Potato",
            "pathogen": "Pectobacterium carotovorum (Bacterium)",
            "primary_symptoms": ["Black Stem Rot", "Yellow Leaves", "Plant Wilting"],
            "treatment": "Apply Copper Bactericide and Improve Drainage",
            "detailed_treatment": "Drench stem bases with Copper Oxychloride (2.5 g/L). Avoid handling tubers under wet conditions.",
            "prevention": "Ensure well-drained planting beds, avoid bruising tubers during harvesting and storage."
        },

        # Maize
        "maize_northern_leaf_blight": {
            "id": "maize_northern_leaf_blight",
            "name": "Northern Corn Leaf Blight",
            "crop": "Maize",
            "pathogen": "Exserohilum turcicum (Fungus)",
            "primary_symptoms": ["Cigar-Shaped Lesions", "Leaf Drying", "Yellow Leaves"],
            "treatment": "Apply Azoxystrobin or Mancozeb Fungicide",
            "detailed_treatment": "Apply Azoxystrobin + Difenoconazole (1 ml/L) or Mancozeb (2.5 g/L) at onset of lesions.",
            "prevention": "Rotate with non-host crops (soybean/pulses) and plow under old crop residues."
        },
        "maize_common_rust": {
            "id": "maize_common_rust",
            "name": "Common Rust",
            "crop": "Maize",
            "pathogen": "Puccinia sorghi (Fungus)",
            "primary_symptoms": ["Cinnamon-Brown Pustules", "Brown Spots", "Leaf Drying"],
            "treatment": "Apply Pyraclostrobin or Tebuconazole",
            "detailed_treatment": "Spray Tebuconazole 250 EC (1 ml/L) if rust lesions appear on upper leaves before silking.",
            "prevention": "Use resistant maize hybrids and practice early planting to escape peak spore dispersal."
        },

        # Cotton
        "cotton_bacterial_blight": {
            "id": "cotton_bacterial_blight",
            "name": "Cotton Bacterial Blight",
            "crop": "Cotton",
            "pathogen": "Xanthomonas citri pv. malvacearum (Bacterium)",
            "primary_symptoms": ["Angular Leaf Spots", "Black Stem Rot", "Leaf Drying"],
            "treatment": "Spray Streptocycline and Copper Oxychloride",
            "detailed_treatment": "Spray Streptocycline (100 mg/L) + Copper Oxychloride (2.5 g/L) at 12-day intervals.",
            "prevention": "Use acid-delinted certified seeds treated with Streptocycline (1 g/kg seed)."
        },
        "cotton_fusarium_wilt": {
            "id": "cotton_fusarium_wilt",
            "name": "Fusarium Wilt",
            "crop": "Cotton",
            "pathogen": "Fusarium oxysporum f. sp. vasinfectum (Fungus)",
            "primary_symptoms": ["Yellow Leaves", "Plant Wilting", "Vascular Browning"],
            "treatment": "Soil Drenching with Carbendazim / Trichoderma",
            "detailed_treatment": "Drench root zone with Carbendazim (1 g/L) or apply biocontrol agent Trichoderma viride enriched in compost.",
            "prevention": "Practice 3-year crop rotation; use resistant cotton varieties and balance potash fertilization."
        }
    }

    # 4. Production Rules for Backward Chaining
    # Each rule defines:
    #   id, crop, hypothesis (disease), required_symptoms, certainty, explanation
    rules = [
        # Rice Rules
        {
            "id": "RULE_RICE_01",
            "crop": "Rice",
            "hypothesis": "Brown Spot Disease",
            "disease_id": "rice_brown_spot",
            "required_symptoms": ["Yellow Leaves", "Brown Spots", "Leaf Drying"],
            "confidence": "High",
            "treatment": "Apply Suitable Fungicide",
            "explanation": "If crop is Rice and leaves are yellow with brown circular spots and leaf drying, then disease is Brown Spot Disease."
        },
        {
            "id": "RULE_RICE_02",
            "crop": "Rice",
            "hypothesis": "Bacterial Leaf Blight",
            "disease_id": "rice_bacterial_leaf_blight",
            "required_symptoms": ["Yellow Leaves", "Water-Soaked Lesions", "Leaf Drying"],
            "confidence": "High",
            "treatment": "Spray Copper Hydroxide or Streptocycline",
            "explanation": "If crop is Rice and leaves exhibit yellowing with water-soaked streaks and marginal leaf drying, then disease is Bacterial Leaf Blight."
        },
        {
            "id": "RULE_RICE_03",
            "crop": "Rice",
            "hypothesis": "Rice Blast Disease",
            "disease_id": "rice_blast",
            "required_symptoms": ["Spindle-Shaped Spots", "Ash Gray Center", "Panicle Rot"],
            "confidence": "High",
            "treatment": "Apply Tricyclazole or Azoxystrobin Fungicide",
            "explanation": "If crop is Rice with spindle-shaped spots having ash-gray centers and panicle rot, then disease is Rice Blast Disease."
        },
        {
            "id": "RULE_RICE_04",
            "crop": "Rice",
            "hypothesis": "Sheath Blight Disease",
            "disease_id": "rice_sheath_blight",
            "required_symptoms": ["Sheath Lesions", "Yellow Leaves", "Stem Lodging"],
            "confidence": "High",
            "treatment": "Apply Hexaconazole or Validamycin",
            "explanation": "If crop is Rice with banded lesions on leaf sheath, yellowing leaves, and stem lodging, then disease is Sheath Blight Disease."
        },

        # Wheat Rules
        {
            "id": "RULE_WHEAT_01",
            "crop": "Wheat",
            "hypothesis": "Wheat Rust Disease",
            "disease_id": "wheat_rust",
            "required_symptoms": ["Orange-Yellow Pustules", "Yellow Leaves", "Leaf Drying"],
            "confidence": "High",
            "treatment": "Apply Propiconazole Fungicide",
            "explanation": "If crop is Wheat and orange-yellow powdery pustules occur with leaf chlorosis and drying, then disease is Wheat Rust."
        },
        {
            "id": "RULE_WHEAT_02",
            "crop": "Wheat",
            "hypothesis": "Powdery Mildew",
            "disease_id": "wheat_powdery_mildew",
            "required_symptoms": ["White Powdery Patches", "Yellow Leaves", "Stunted Growth"],
            "confidence": "High",
            "treatment": "Apply Wettable Sulfur or Triazole Fungicide",
            "explanation": "If crop is Wheat with white powdery fungal patches, yellow leaves, and stunted growth, then disease is Powdery Mildew."
        },
        {
            "id": "RULE_WHEAT_03",
            "crop": "Wheat",
            "hypothesis": "Loose Smut Disease",
            "disease_id": "wheat_loose_smut",
            "required_symptoms": ["Black Powdery Spores", "Panicle Rot", "Stunted Growth"],
            "confidence": "High",
            "treatment": "Seed Treatment with Systemic Fungicides",
            "explanation": "If crop is Wheat and ear heads are transformed into masses of black powdery spores, then disease is Loose Smut."
        },

        # Tomato Rules
        {
            "id": "RULE_TOMATO_01",
            "crop": "Tomato",
            "hypothesis": "Early Blight",
            "disease_id": "tomato_early_blight",
            "required_symptoms": ["Brown Spots", "Concentric Rings", "Yellow Leaves"],
            "confidence": "High",
            "treatment": "Apply Mancozeb or Chlorothalonil Fungicide",
            "explanation": "If crop is Tomato with brown target-like concentric rings on yellowing lower leaves, then disease is Early Blight."
        },
        {
            "id": "RULE_TOMATO_02",
            "crop": "Tomato",
            "hypothesis": "Late Blight",
            "disease_id": "tomato_late_blight",
            "required_symptoms": ["Dark Water-Soaked Spots", "White Mold Underside", "Fruit Damage"],
            "confidence": "High",
            "treatment": "Apply Metalaxyl or Cymoxanil Fungicide",
            "explanation": "If crop is Tomato with water-soaked lesions, white mold on leaf underside, and fruit rot, then disease is Late Blight."
        },
        {
            "id": "RULE_TOMATO_03",
            "crop": "Tomato",
            "hypothesis": "Tomato Leaf Curl Virus",
            "disease_id": "tomato_leaf_curl",
            "required_symptoms": ["Curling Leaves", "Yellow Leaves", "Whitefly Infestation"],
            "confidence": "High",
            "treatment": "Control Whitefly Vectors and Rogue Plants",
            "explanation": "If crop is Tomato with upward curling deformed leaves, chlorosis, and whitefly infestation, then disease is Tomato Leaf Curl Virus."
        },

        # Potato Rules
        {
            "id": "RULE_POTATO_01",
            "crop": "Potato",
            "hypothesis": "Potato Late Blight",
            "disease_id": "potato_late_blight",
            "required_symptoms": ["Dark Water-Soaked Spots", "Leaf Drying", "Tuber Rot"],
            "confidence": "High",
            "treatment": "Apply Systemic Fungicide (Dimethomorph / Mancozeb)",
            "explanation": "If crop is Potato with rapidly spreading water-soaked leaf spots, foliage drying, and rotting tubers, then disease is Potato Late Blight."
        },
        {
            "id": "RULE_POTATO_02",
            "crop": "Potato",
            "hypothesis": "Blackleg and Soft Rot",
            "disease_id": "potato_blackleg",
            "required_symptoms": ["Black Stem Rot", "Yellow Leaves", "Plant Wilting"],
            "confidence": "High",
            "treatment": "Apply Copper Bactericide and Improve Drainage",
            "explanation": "If crop is Potato with inky black stem rot, yellow leaves, and rapid plant wilting, then disease is Blackleg and Soft Rot."
        },

        # Maize Rules
        {
            "id": "RULE_MAIZE_01",
            "crop": "Maize",
            "hypothesis": "Northern Corn Leaf Blight",
            "disease_id": "maize_northern_leaf_blight",
            "required_symptoms": ["Cigar-Shaped Lesions", "Leaf Drying", "Yellow Leaves"],
            "confidence": "High",
            "treatment": "Apply Azoxystrobin or Mancozeb Fungicide",
            "explanation": "If crop is Maize with elongated cigar-shaped grayish lesions and extensive leaf drying, then disease is Northern Corn Leaf Blight."
        },
        {
            "id": "RULE_MAIZE_02",
            "crop": "Maize",
            "hypothesis": "Common Rust",
            "disease_id": "maize_common_rust",
            "required_symptoms": ["Cinnamon-Brown Pustules", "Brown Spots", "Leaf Drying"],
            "confidence": "High",
            "treatment": "Apply Pyraclostrobin or Tebuconazole",
            "explanation": "If crop is Maize with scattered cinnamon-brown pustules, brown spots, and leaf drying, then disease is Common Rust."
        },

        # Cotton Rules
        {
            "id": "RULE_COTTON_01",
            "crop": "Cotton",
            "hypothesis": "Cotton Bacterial Blight",
            "disease_id": "cotton_bacterial_blight",
            "required_symptoms": ["Angular Leaf Spots", "Black Stem Rot", "Leaf Drying"],
            "confidence": "High",
            "treatment": "Spray Streptocycline and Copper Oxychloride",
            "explanation": "If crop is Cotton with angular vein-bound leaf spots, black stem cankers, and leaf drying, then disease is Cotton Bacterial Blight."
        },
        {
            "id": "RULE_COTTON_02",
            "crop": "Cotton",
            "hypothesis": "Fusarium Wilt",
            "disease_id": "cotton_fusarium_wilt",
            "required_symptoms": ["Yellow Leaves", "Plant Wilting", "Vascular Browning"],
            "confidence": "High",
            "treatment": "Soil Drenching with Carbendazim / Trichoderma",
            "explanation": "If crop is Cotton with yellowing leaves, daytime wilting, and brown internal stem vascular discoloration, then disease is Fusarium Wilt."
        }
    ]

    # Convert rules to pandas DataFrame to demonstrate pandas manipulation
    rules_df = pd.DataFrame(rules)
    # Serialize symptoms list to string for CSV
    rules_df_export = rules_df.copy()
    rules_df_export["required_symptoms"] = rules_df_export["required_symptoms"].apply(lambda s: "; ".join(s))
    rules_df_export.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Exported {len(rules_df)} rules to CSV: {OUTPUT_CSV_PATH}")

    # Build comprehensive JSON knowledge base
    kb = {
        "metadata": {
            "project": "Project 35: Crop Disease Expert System",
            "algorithm": "Backward Chaining",
            "version": "2.0.0",
            "total_crops": len(crops),
            "total_diseases": len(diseases),
            "total_symptoms": len(symptoms),
            "total_rules": len(rules)
        },
        "crops": crops,
        "symptoms": symptoms,
        "diseases": diseases,
        "rules": rules
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2)

    print(f"Knowledge base successfully saved to JSON: {OUTPUT_JSON_PATH}")
    print(f"Summary: {len(crops)} Crops, {len(diseases)} Diseases, {len(symptoms)} Symptoms, {len(rules)} Rules.")
    return kb


if __name__ == "__main__":
    build_knowledge_base()
