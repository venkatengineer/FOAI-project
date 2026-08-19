# Crop Disease Expert System using Two-Stage Forward Chaining & Candidate Ranking

A minimal, deterministic, and easy-to-explain Foundations of AI mini-project built from scratch using **Python**, **Flask**, **HTML/CSS**, and **JSON**, powered by the **DigiGreen Crop Disease Dataset** (`DigiGreen/Crop_Disease_Images` on Hugging Face).

---

## 🌟 Core AI Concept: Two-Stage Reasoning Engine

The system implements a simple, transparent **Two-Stage Reasoning Engine**:

```
                  User Observed Symptoms & Crop Selection
                                     ↓
                           Initial Facts in Memory
                                     ↓
                    STAGE 1: Forward Chaining Engine
                                     ↓
                        Definitive Disease Rule Fired?
                                     │
                 ┌───────────────────┴───────────────────┐
                YES                                     NO
                 ↓                                       ↓
     STATE 1: STRONG MATCH              STAGE 2: Candidate Disease Ranking
  - Rule Trace (R1→R2→R3→R4)                             ↓
  - 100% Derived Match                         Crop Compatibility Filter
  - Strong Remediation Guidance                          ↓
                                              Calculate Match Score %
                                      score = (matched / total) * 100
                                                         ↓
                                            Highest Match Score ≥ 50%?
                                             │
                         ┌───────────────────┴───────────────────┐
                        YES                                     NO
                         ↓                                       ↓
             STATE 2: POSSIBLE DISEASE              STATE 3: INSUFFICIENT EVIDENCE
          - Evidence Match %                     - Prompt for Additional Symptoms
          - Matched & Missing Symptoms           - Avoids False "Unknown / Healthy"
          - Ranked Alternative Candidates
```

### Three Diagnostic States:
1. **STATE 1 — STRONG MATCH**: Triggered directly when Forward Chaining derives a disease rule ($R1 \rightarrow R2 \rightarrow R3 \rightarrow R4$).
2. **STATE 2 — POSSIBLE DISEASE**: Triggered when no rule fires, but crop-compatible candidate diseases have a match score $\ge 50\%$.
3. **STATE 3 — INSUFFICIENT EVIDENCE**: Triggered when symptoms are too weak ($< 50\%$) or missing. Avoids displaying `"Unknown / Healthy"` simply because no rule fired.

---

## 📊 Dataset & Knowledge Base

The Knowledge Base (`knowledge_base.json`) is constructed directly by cleaning and structuring annotations from the **DigiGreen Crop Disease Dataset** on Hugging Face:
- **Crops**: Tomato, Potato, Chilli, Maize, Brinjal, Mango
- **Diseases**: 15 distinct crop disease profiles with explicit `symptom_ids`
- **Rules**: 34 multi-step production rules ($IF \rightarrow THEN$)
- **Recommendations**: Context-aware remediation guidance adapted per diagnostic state.

---

## 📁 Project Structure

```
crop-disease-expert-system/
│
├── app.py                  # Flask web application controller
├── inference.py            # Two-Stage Reasoning engine (Forward Chaining + Candidate Ranking)
├── build_kb.py             # Dataset cleaning & KB generator script
├── knowledge_base.json     # DigiGreen dataset-derived Knowledge Base
├── requirements.txt        # Minimal Python dependencies (Flask, pandas, pyarrow)
├── README.md               # Quickstart and viva defense guide
│
├── templates/
│   └── index.html          # Redesigned web application template
│
├── static/
│   └── style.css           # Styling for status badges, progress bars, & reasoning trace
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
Python 3.8+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

### 4. Run Automated Tests
```bash
python -m unittest discover tests
```

---

## 🎓 Viva Explanation Guide

- **Q: How does the system handle partial symptom matches without ML?**
  - *Answer*: It uses a Two-Stage Reasoning Engine. Forward Chaining runs first as the primary AI mechanism. If no definitive rule fires, Stage 2 candidate ranking evaluates crop-compatible diseases by match score $\text{score} = (\text{matched} / \text{total}) \times 100$ and presents possible diseases ($\ge 50\%$) or requests more evidence ($< 50\%$).
- **Q: Why does the system avoid displaying "Unknown / Healthy"?**
  - *Answer*: Lack of a full rule match does NOT mean the crop is healthy. The system distinguishes between a definitive match (`Strong Match`), partial evidence (`Possible`), and missing data (`Insufficient Evidence`), providing actionable safety warnings.
- **Q: How does crop compatibility filtering work?**
  - *Answer*: When a target crop (e.g. Tomato) is selected, diseases of unrelated crops (e.g. Potato, Mango) are excluded from candidate ranking to ensure relevant diagnostic suggestions.
