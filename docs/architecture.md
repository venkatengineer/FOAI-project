# System Architecture

## Overview
**Project 35: Crop Disease Expert System** is architected as an interactive, goal-driven symbolic AI system. The application coordinates between a **Knowledge Base** managed via **Pandas**, a **Backward Chaining Inference Engine** with an explicit **Goal Stack**, and an **Interactive Command Line Interface (CLI)**.

```
                                  +---------------------------------------+
                                  |                FARMER                 |
                                  +---------------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |     USER INTERFACE LAYER (CLI)        |
                                  | - Interactive Menu & Crop Selector    |
                                  | - Categorized Symptom Prompts (y/n)   |
                                  | - Live Reasoning Trace & Goal Stack   |
                                  | - Pandas KB Data Table Explorer       |
                                  +---------------------------------------+
                                           |                      ^
                         Symptom Responses |                      | Diagnostic Report & Trace
                                           v                      |
+-------------------------------------------------------------------------------------------------+
|                                 BACKWARD CHAINING INFERENCE ENGINE                              |
|                                                                                                 |
|   1. Hypothesis Generator / Candidate Selector                                                  |
|      - Generates suspected disease hypotheses for target crop                                   |
|      - Prioritizes user suspected disease or best-first matching candidates                     |
|                                                                                                 |
|   2. Goal Stack & Sub-Goal Decomposer                                                           |
|      - Pushes Goal: [Prove Disease H]                                                           |
|      - Decomposes into Sub-Goals: [Verify Symptom S1, S2, ...]                                  |
|                                                                                                 |
|   3. Working Memory & Interactive Verification                                                  |
|      - Checks Working Memory (known facts)                                                      |
|      - Formulates targeted questions by category:                                               |
|        * Leaf Color        * Stem Condition                                                     |
|        * Fruit Damage      * Pest Infestation                                                   |
|      - Prompts farmer interactively for unknown symptoms                                        |
|                                                                                                 |
|   4. Backtracking Controller                                                                    |
|      - If any required symptom is refuted: Pops sub-goal and goal                               |
|      - Backtracks immediately to next candidate hypothesis                                      |
|                                                                                                 |
|   5. Conclusion & Action Planner                                                                |
|      - Confirms disease when all sub-goals are verified                                         |
|      - Calculates Confidence (High / Moderate)                                                  |
|      - Formulates treatment recommendations & preventive measures                               |
+-------------------------------------------------------------------------------------------------+
                                           ^
                                           | Filter & Index Rules
                                           v
+-------------------------------------------------------------------------------------------------+
|                               KNOWLEDGE BASE LAYER (Pandas & JSON)                              |
|                                                                                                 |
|   - Rules DataFrame (rule_id, crop, hypothesis, required_symptoms, confidence, treatment)       |
|   - Symptoms DataFrame (id, name, category, targeted_question)                                  |
|   - Disease Catalog (pathogen, detailed_treatment, preventive_measures)                         |
|   - Supported Crops: Rice, Wheat, Tomato, Potato, Maize, Cotton                                 |
+-------------------------------------------------------------------------------------------------+
```

---

## Architectural Components

### 1. Knowledge Base Layer (`build_kb.py`, `knowledge_base.json`, `knowledge_base_rules.csv`)
- **Pandas Representation**: Production rules are loaded into a `pandas.DataFrame`. This allows vector operations, rapid column indexing, and filtering by crop:
  ```python
  filtered_rules = rules_df[rules_df["crop"].str.lower() == crop.lower()]
  ```
- **Rule Structure**:
  - `id`: Unique identifier (e.g. `RULE_RICE_01`).
  - `crop`: Target crop (`Rice`, `Wheat`, `Tomato`, `Potato`, `Maize`, `Cotton`).
  - `hypothesis`: Suspected disease goal (`Brown Spot Disease`).
  - `required_symptoms`: Ordered list of sub-goals (`["Yellow Leaves", "Brown Spots", "Leaf Drying"]`).
  - `confidence`: Certainty rating when verified (`High`).
  - `treatment`: Actionable remedy (`Apply Suitable Fungicide`).

### 2. Backward Chaining Engine (`inference.py`)
- **Goal Stack ($GS$)**: An explicit LIFO stack tracking the active reasoning state:
  - Push $Goal(H)$
  - Push $SubGoal(S_i)$
  - Verify $S_i$ against Working Memory or query farmer
  - Pop $SubGoal(S_i)$
  - If satisfied for all $S_i \in Rule$, Goal $H$ is fulfilled!
  - If any $S_i$ is refuted, Goal $H$ fails, and engine backtracks to $Goal(H_{next})$.
- **Working Memory ($WM$)**: Key-value map of established facts (`{Symptom: True/False}`). Facts established during prior sub-goals are remembered, so the farmer is never asked the same symptom twice.
- **Categorical Targeted Questioning**: Formulates questions based on the biological category of the symptom:
  - *Leaf Color*: "Are the leaves turning yellow or pale chlorotic?"
  - *Leaf Condition*: "Are there distinct brown oval/circular spots visible on the leaves?"
  - *Stem Condition*: "Are the leaf margins or tips drying up and withering?"
  - *Fruit Damage*: "Is there neck rotting or grain discoloration on the panicles?"
  - *Pest Infestation*: "Are small white insects (whiteflies) fluttering when leaves are shaken?"

### 3. User Interface Layer (`app.py`)
- **Interactive Command Line Interface (CLI)**:
  - **Main Menu**: Clean numbered navigation supporting interactive diagnosis, benchmark demo, direct symptom entry, KB explorer, and architecture review.
  - **Categorized Question Prompts**: Clear terminal boxes displaying the current sub-goal, biological category, and targeted question with input validation (`y`/`n`/`q`).
  - **Real-Time Backtracking Feedback**: Instantly informs the user when a symptom refutes a hypothesis and indicates the next candidate rule being tested.
  - **Diagnostic Report Card**: Formats diagnostic findings into an organized terminal summary detailing identified disease, confidence rating, pathogen taxonomy, chemical remedies, and cultural prevention measures.
  - **Reasoning Trace Viewer**: Formats step-by-step goal stack activations, memory lookups, and backtracking logs.
  - **CLI Arguments & Automation**: Supports non-interactive flags (`--demo`, `--crop`, `--symptoms`, `--rules`, `--interactive`) for scripted execution and automated testing.
