# System Architecture

The architecture of the **Crop Disease Expert System** follows a clean two-stage data-driven pipeline where user inputs are transformed into initial facts, evaluated against rules in the Knowledge Base (structured from the **DigiGreen Crop Disease Dataset**), and processed into one of three diagnostic result states with complete explainability.

```
                            USER
                              ↓
               USER INTERFACE (Flask / HTML / CSS)
                              ↓
               INITIAL FACTS (Working Memory)
                              ↓
         KNOWLEDGE BASE (knowledge_base.json from DigiGreen Dataset)
                              ↓
              TWO-STAGE INFERENCE ENGINE (inference.py)
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
 1. FORWARD CHAINING                       2. CANDIDATE RANKING
  (Primary AI Mechanism)                  (Fallback for Partial Evidence)
         │                                         │
         ▼                                         ▼
   Definitive Rule Fired?                 Crop Compatibility Filter & Score %
         │                                         │
 ┌───────┴───────┐                         ┌───────┴───────┐
YES             NO                        ≥50%            <50%
 │               │                         │               │
 ▼               └──────────────┐          ▼               ▼
STATE 1:                     STATE 2:                  STATE 3:
STRONG MATCH             POSSIBLE DISEASE        INSUFFICIENT EVIDENCE
(R1→R2→R3→R4)            (Partial Score %)       (Prompt for Symptoms)
```

## Architectural Components

1. **User Interface (`app.py`, `index.html`, `style.css`)**:
   - Collects user inputs: Crop selection, observed symptoms, environmental conditions.
   - Formats inputs into boolean initial facts.
   - Renders visual result states using color-coded status badges, progress bars, matched vs. missing symptom lists, reasoning trace timelines, and candidate alternative comparison tables.

2. **Knowledge Base Store (`knowledge_base.json` & `build_kb.py`)**:
   - Structured directly from Hugging Face `DigiGreen/Crop_Disease_Images` dataset.
   - Contains 6 crops (Tomato, Potato, Chilli, Maize, Brinjal, Mango), 15 diseases with explicit `symptom_ids`, 34 multi-step production rules, and state-dependent recommendations.

3. **Two-Stage Inference Engine (`inference.py`)**:
   - **Stage 1 (Forward Chaining)**: Maintains working memory, matches rule conditions, fires rules, logs steps in reasoning trace, and checks for direct disease derivation.
   - **Stage 2 (Candidate Ranking Fallback)**: Evaluates crop-compatible candidate diseases when no rule fires, calculating match score $\text{score} = (\text{matched} / \text{total}) \times 100$.

4. **Diagnostic Result States**:
   - **STATE 1 — STRONG MATCH**: Forward Chaining derived disease ($100\%$ match confidence).
   - **STATE 2 — POSSIBLE DISEASE**: Top candidate match score $\ge 50\%$ with missing symptom suggestions.
   - **STATE 3 — INSUFFICIENT EVIDENCE**: Match score $< 50\%$, prompting user for additional field observations.
