# Project 35: Crop Disease Expert System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![AI-Reasoning](https://img.shields.io/badge/Algorithm-Backward%20Chaining-green.svg)]()
[![UI](https://img.shields.io/badge/UI-Command%20Line%20Interface%20(CLI)-blue.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)]()
[![Libraries](https://img.shields.io/badge/Libraries-Pandas%20%7C%20Pytest-orange.svg)]()
[![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passed-brightgreen.svg)]()

An intelligent, goal-driven **Crop Disease Expert System** with an interactive **Command Line Interface (CLI)** that identifies crop diseases using symptom-based reasoning. The system stores agricultural knowledge as logical production rules and begins with a suspected disease hypothesis. It then asks the farmer targeted questions regarding symptoms (such as leaf color, stem condition, fruit damage, or pest infestation), verifies hypotheses interactively, and recommends suitable treatment methods.

The project is fully **Dockerized** for seamless, zero-dependency deployment across any operating system or cloud environment.

---

## 🌾 Problem Statement
Agriculture is one of the most important sectors supporting food production and rural livelihoods. Farmers frequently encounter crop diseases caused by fungi, bacteria, viruses, pests, and environmental conditions. In many rural regions, agricultural experts may not be readily available to identify diseases accurately, resulting in delayed treatment and reduced crop yield. 

An intelligent expert system can assist farmers by analyzing crop symptoms and recommending appropriate treatments. The objective of this project is to develop an AI-based **Crop Disease Expert System** that identifies crop diseases using symptom-based reasoning.

The system stores agricultural knowledge as logical rules and begins with a suspected disease hypothesis. It then asks the farmer targeted questions regarding symptoms such as leaf color, stem condition, fruit damage, or pest infestation. Based on the responses, the system verifies whether the hypothesis is correct and recommends suitable treatment methods. This project demonstrates goal-driven reasoning using **Backward Chaining**, enabling efficient diagnosis with fewer questions.

---

## 🎯 Objectives
- **Identify crop diseases**: Accurately diagnose fungal, bacterial, and viral diseases across major crops (Rice, Wheat, Tomato, Potato, Maize, Cotton).
- **Verify symptoms interactively**: Formulate targeted questions categorized by visual indicators (leaf color, stem condition, fruit damage, pest infestation) directly in the CLI.
- **Recommend suitable treatments**: Output actionable agricultural remedies, chemical fungicides/bactericides, biological controls, and cultural prevention measures.
- **Reduce diagnosis time**: Minimize the number of questions asked through goal-directed hypothesis verification and prompt backtracking.
- **Improve agricultural decision-making**: Empower smallholder farmers and extension workers with transparent, explainable AI reasoning and live reasoning traces.

---

## 🧠 AI Algorithm Used: Backward Chaining

### Why Backward Chaining?
> **Backward chaining starts with a possible disease hypothesis and works backward to verify whether the required symptoms are present, making it efficient for diagnostic expert systems.**

```
                        [ Suspected Disease Hypothesis ]
                                      │
                                      ▼
                        [ Push Goal to Goal Stack ]
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
        [ Sub-Goal 1: Symptom A ]             [ Sub-Goal 2: Symptom B ]
                   │                                     │
           Is in Working Memory?                 Is in Working Memory?
             ├─ YES ──► Value Used                 ├─ YES ──► Value Used
             └─ NO  ──► Ask Farmer                 └─ NO  ──► Ask Farmer
                   │                                     │
           Confirmed? (True/False)               Confirmed? (True/False)
                   │                                     │
         ┌─────────┴─────────┐                           │
       True                False                         │
         │                   │                           │
         ▼                   ▼                           ▼
   Proceed to Next      BACKTRACK!             All Sub-Goals True?
      Sub-Goal         Try Alternative                   │
                          Hypothesis             ┌───────┴───────┐
                                                YES             NO
                                                 │               │
                                                 ▼               ▼
                                           DISEASE PROVEN   BACKTRACK /
                                          (High Confidence) INCONCLUSIVE
```

### Key Advantages:
1. **Fewer Questions**: Asks only symptoms relevant to proving or disproving the current disease hypothesis.
2. **Cognitive Ease**: The farmer evaluates one specific suspected condition at a time rather than a confusing 30-item checklist.
3. **Immediate Backtracking**: If a required symptom is refuted (e.g. leaf drying is absent), the system immediately abandons that hypothesis and tests the next candidate.

---

## 📋 Sample Input & Expected Output

### Sample Input
- **Crop**: `Rice`
- **Symptoms**: `Yellow Leaves`, `Brown Spots`, `Leaf Drying`

### Expected Output
- **Disease Identified**: `Brown Spot Disease`
- **Recommended Treatment**: `Apply Suitable Fungicide`
- **Confidence**: `High`
- **Algorithm Used**: `Backward Chaining`

---

## 📦 Python Libraries & Interface
- **Command Line Interface (CLI)**: Interactive, accessible terminal user interface featuring structured menus, ANSI color highlights, categorical targeted questions, and step-by-step reasoning trace logs.
- **`pandas`**: High-performance tabular data structures used to store, filter, index, and query agricultural production rules and symptom catalogs.
- **`pytest`**: Automated unit test suite verifying backward chaining, backtracking, and CLI workflows.
- **Docker**: Containerized runtime ensuring complete portability and zero-host-dependency execution.

---

## 📁 Project Structure

```
crop-disease-expert-system/
│
├── app.py                      # Interactive Command Line Interface (CLI) Application
├── inference.py                # Backward Chaining Inference Engine & Goal Stack
├── build_kb.py                 # Pandas-based Knowledge Base Generator & CSV Exporter
├── knowledge_base.json         # Structured Agricultural Knowledge Base (JSON)
├── knowledge_base_rules.csv    # Exported Rules DataFrame (CSV)
├── requirements.txt            # Dependencies (pandas, pytest)
├── Dockerfile                  # Production container definition (python:3.11-slim)
├── .dockerignore               # Docker build exclusions
├── docker-compose.yml          # Multi-service configuration (app, demo, test)
├── README.md                   # Project documentation & user guide
│
├── tests/
│   └── test_inference.py       # 10 Automated Unit Tests for Backward Chaining & CLI
│
└── docs/
    ├── problem_statement.md    # Detailed Problem Statement & Objectives
    ├── abstract.md             # Formal Project Abstract
    ├── literature_survey.md    # Survey on Backward Chaining & Expert Systems
    ├── architecture.md         # Detailed System Architecture Specification
    ├── diagrams.md             # Mermaid Flowcharts, Sequence, & Class Diagrams
    ├── testing.md              # Test Matrix and Validation Log
    └── final_report.md         # End-to-End Final Project Report & Viva Q&A
```

---

## 🐳 Docker Deployment & Usage

### 1. Build the Docker Image
```bash
docker build -t crop-disease-expert-system .
```

### 2. Run Interactive CLI in Docker
Use `-it` to connect your terminal interactively:
```bash
docker run -it --rm crop-disease-expert-system
```

### 3. Run Benchmark Rice Demo in Docker
```bash
docker run --rm crop-disease-expert-system --demo
```

### 4. Run Direct Batch Diagnosis in Docker
```bash
docker run --rm crop-disease-expert-system --crop Rice --symptoms "Yellow Leaves" "Brown Spots" "Leaf Drying" --trace
```

### 5. Inspect Knowledge Base Rules via Docker
```bash
docker run --rm crop-disease-expert-system --rules Rice
```

### 6. Run Test Suite Inside Docker
```bash
docker run --rm --entrypoint pytest crop-disease-expert-system -v tests/test_inference.py
```

### 7. Using Docker Compose (Optional)
```bash
# Launch interactive CLI
docker compose run --rm app

# Run problem statement demo
docker compose run --rm demo

# Run test suite
docker compose run --rm test
```

---

## 🚀 Local Quickstart (Without Docker)

### 1. Prerequisites
Python 3.8+ installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the CLI Application

#### Option A: Launch Interactive CLI Menu (Primary UI)
```bash
python app.py
```
Provides an interactive menu:
1. 🔍 **Interactive Symptom Verification**: Select a crop and answer targeted questions.
2. 🌾 **Quick Demo (Rice Benchmark Sample)**: 1-click verification of the problem statement case.
3. 📋 **Direct Batch Symptom Diagnosis**: Select observed symptoms from an indexed list.
4. 📚 **Knowledge Base & Rule Explorer**: Inspect rules and symptoms using Pandas DataFrames.
5. 🔬 **Technical Architecture Summary**: View core AI algorithm mechanics.

#### Option B: Run 1-Click Benchmark Demo
```bash
python app.py --demo
```

#### Option C: Direct Interactive Diagnosis
```bash
python app.py --interactive
```

#### Option D: Direct Batch Diagnosis via CLI Arguments
```bash
python app.py --crop Rice --symptoms "Yellow Leaves" "Brown Spots" "Leaf Drying" --trace
```

#### Option E: Inspect Knowledge Base Rules via Pandas
```bash
python app.py --rules Rice
```

---

## 🧪 Automated Unit Testing

Run the comprehensive unit test suite:
```bash
python -m pytest -v tests/test_inference.py
```

### Verified Test Cases (10/10 Passed):
1. `test_1_problem_statement_rice_sample`: Matches exact problem statement sample input and expected output.
2. `test_2_interactive_questioning_callback`: Confirms dynamic interactive question callback triggers.
3. `test_3_backtracking_to_alternative_hypothesis`: Proves hypothesis refutation and rollback.
4. `test_4_no_disease_match_all_refuted`: Handles negative symptom boundaries gracefully.
5. `test_5_unsupported_crop_error`: Handles invalid input crops with helpful guidance.
6. `test_6_cross_crop_diagnoses`: Verifies multi-crop rules across Wheat, Tomato, Potato, Maize, and Cotton.
7. `test_7_pandas_knowledge_base_integrity`: Validates Pandas DataFrame schema and indexing.
8. `test_8_information_efficiency_fewer_questions`: Verifies $66.7\%$ question reduction over exhaustive polling.
9. `test_9_cli_benchmark_demo_execution`: Confirms end-to-end execution of CLI demo mode.
10. `test_10_cli_report_formatting_and_trace`: Validates CLI diagnostic card formatting and reasoning trace output.

---

## 🎓 Learning Outcome
Students understand:
- **Goal-driven reasoning** vs. data-driven forward reasoning.
- **Backward Chaining** algorithm implementation using an explicit Goal Stack and Working Memory.
- **Dynamic question generation** by categorizing agricultural symptoms (leaf color, stem condition, fruit damage, pest infestation).
- **Rule management with Pandas** DataFrames for production AI systems.
- **Containerization with Docker** for reproducible, isolated, and cloud-ready AI deployments.
- **Precision farming** applications and transparent, explainable decision support.
