# Crop Disease Expert System using Forward Chaining

A minimal, deterministic, and easy-to-explain Foundations of AI mini-project built from scratch using **Python**, **Flask**, **HTML/CSS**, and **JSON**.

---

## 🌟 Core AI Concept: Forward Chaining

Unlike direct `IF symptom THEN disease` mapping, this system uses data-driven **Forward Chaining** to infer intermediate facts step-by-step:

```
User Input (Initial Facts)
        ↓
    Rule 1 Fired
        ↓
  Intermediate Fact 1
        ↓
    Rule 2 Fired
        ↓
  Intermediate Fact 2
        ↓
    Rule 3 Fired
        ↓
  Disease Diagnosis + Explanation
```

---

## 📁 Project Structure

```
crop-disease-expert-system/
│
├── app.py                  # Flask web application controller
├── inference.py            # Forward Chaining inference engine
├── api_connector.py        # Primary API fetcher with local JSON fallback
├── knowledge_base.json     # Local database fallback (3 crops, 6 diseases, ~20 rules)
├── requirements.txt        # Minimal Python dependencies (Flask, requests)
├── README.md               # Quickstart and viva defense guide
│
├── templates/
│   └── index.html          # Web application template
│
├── static/
│   └── style.css           # Styling for UI and reasoning trace
│
├── tests/
│   └── test_inference.py   # 8 automated unit test cases
│
└── docs/
    ├── problem_statement.md
    ├── abstract.md
    ├── literature_survey.md
    ├── architecture.md
    ├── diagrams.md
    ├── testing.md
    └── final_report.md
```

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
Ensure Python 3.8+ is installed on your machine.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 4. Run Automated Tests
```bash
python -m unittest discover tests
```

---

## 🌾 Demonstration Example (Viva Presentation)

1. Select Crop: **Tomato**
2. Check Symptoms:
   - `[x] Leaf Spots`
   - `[x] Brown Spot Color`
   - `[x] Lower Leaves Affected`
3. Check Environmental Condition:
   - `[x] High Humidity / Damp Weather`
4. Click **`[ DIAGNOSE ]`**

### Reasoning Trace Output Displayed:
- **Step 0**: Initial Facts: `crop = tomato`, `leaf_spots = yes`, `spot_color_brown = yes`, `lower_leaves_affected = yes`, `humidity_high = yes`
- **Step 1 (R1 Fired)**: `crop=tomato` + `leaf_spots=yes` $\rightarrow$ **`tomato_leaf_spots = true`**
- **Step 2 (R2 Fired)**: `tomato_leaf_spots=true` + `spot_color_brown=yes` $\rightarrow$ **`brown_lesions = true`**
- **Step 3 (R3 Fired)**: `brown_lesions=true` + `lower_leaves_affected=yes` $\rightarrow$ **`early_blight_pattern = true`**
- **Step 4 (R4 Fired)**: `early_blight_pattern=true` + `humidity_high=yes` $\rightarrow$ **`disease = Tomato Early Blight`**

---

## 🎓 Viva Explanation Guide (5-Minute Summary)

- **Q: What is Forward Chaining?**
  - *Answer*: Forward Chaining is a data-driven reasoning method starting from known initial facts (symptoms) to derive new facts by repeatedly matching rule conditions until reaching a conclusion (disease).
- **Q: How is the Knowledge Base structured?**
  - *Answer*: It is stored in `knowledge_base.json` (or fetched via `api_connector.py`) containing production rules formatted with `conditions` ($IF$) and `conclusions` ($THEN$).
- **Q: Where is Working Memory managed?**
  - *Answer*: In `inference.py`. It starts as a dictionary of user inputs and expands dynamically as rules fire.
- **Q: How does the engine handle rule firing?**
  - *Answer*: It scans rules sequentially per pass, checks if all rule conditions exist in working memory, fires matching un-fired rules, appends conclusions, logs the trace step, and halts when no new rules fire.
