# Project 35: Crop Disease Expert System

## Problem Statement
Agriculture is one of the most important sectors supporting food production and rural livelihoods. Farmers frequently encounter crop diseases caused by fungi, bacteria, viruses, pests, and environmental conditions. In many rural regions, agricultural experts may not be readily available to identify diseases accurately, resulting in delayed treatment and reduced crop yield. 

An intelligent expert system can assist farmers by analyzing crop symptoms and recommending appropriate treatments. The objective of this project is to develop an AI-based **Crop Disease Expert System** that identifies crop diseases using symptom-based reasoning.

The system stores agricultural knowledge as logical rules and begins with a suspected disease hypothesis. It then asks the farmer targeted questions regarding symptoms such as leaf color, stem condition, fruit damage, or pest infestation. Based on the responses, the system verifies whether the hypothesis is correct and recommends suitable treatment methods. This project demonstrates goal-driven reasoning using **Backward Chaining**, enabling efficient diagnosis with fewer questions.

---

## Objectives
- **Identify crop diseases**: Accurately diagnose fungal, bacterial, and viral diseases across major crops (Rice, Wheat, Tomato, Potato, Maize, Cotton).
- **Verify symptoms interactively**: Formulate targeted questions categorized by visual indicators (leaf color, stem condition, fruit damage, pest infestation) rather than querying unrelated symptoms.
- **Recommend suitable treatments**: Output actionable agricultural remedies, chemical fungicides/bactericides, biological controls, and cultural prevention measures.
- **Reduce diagnosis time**: Minimize the number of questions asked through goal-directed hypothesis verification and prompt backtracking.
- **Improve agricultural decision-making**: Empower smallholder farmers and extension workers with transparent, explainable AI reasoning.

---

## AI Algorithm Used: Backward Chaining

### Why Backward Chaining?
Backward chaining is a **goal-driven reasoning technique** that starts with a potential disease hypothesis (goal) and works backward to verify whether the required premise symptoms are present in the crop. 

1. **Efficiency**: Instead of querying the farmer about every possible symptom across all crops and diseases (as in naive forward chaining), backward chaining only asks for symptoms relevant to the suspected hypothesis.
2. **Targeted Interaction**: Reduces cognitive load on the farmer by focusing on one disease candidate at a time.
3. **Natural Diagnostic Fit**: Real-world agricultural pathologists first form a working hypothesis based on crop type and primary observations, then look for confirmatory signs.
4. **Fast Backtracking**: If a critical symptom is absent, the engine immediately abandons the current hypothesis and moves to the next viable candidate without unnecessary questions.

---

## Sample Input & Expected Output

### Sample Input
- **Crop**: `Rice`
- **Symptoms**: `Yellow Leaves`, `Brown Spots`, `Leaf Drying`

### Expected Output
- **Disease Identified**: `Brown Spot Disease`
- **Recommended Treatment**: `Apply Suitable Fungicide`
- **Confidence**: `High`
- **Algorithm Used**: `Backward Chaining`

---

## Python Libraries & Interface
- **Command Line Interface (CLI)**: Interactive terminal user interface for targeted questioning, goal-stack tracking, and real-time reasoning inspection.
- **`pandas`**: High-performance data structure library for managing, filtering, and indexing agricultural rule bases, disease catalogs, and symptom matrices.

---

## Learning Outcome
Students understand goal-driven reasoning, Backward Chaining, agricultural expert systems, working memory management, goal stack execution, and AI applications in precision farming.
