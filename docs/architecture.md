# System Architecture

The architecture of the **Crop Disease Expert System** is intentionally simple, modular, and easy to explain. It follows a clean data-driven pipeline where user inputs are transformed into initial facts, evaluated against rules in the Knowledge Base by the Forward Chaining Engine, and converted into a final diagnosis with a step-by-step reasoning explanation.

```
             USER
               ↓
        USER INTERFACE (Flask / HTML / CSS)
               ↓
        INITIAL FACTS (Working Memory)
               ↓
        KNOWLEDGE BASE (API / Local JSON Fallback)
               ↓
    FORWARD CHAINING ENGINE (inference.py)
               ↓
          DIAGNOSIS (Disease Identification)
               ↓
      EXPLANATION + ACTION (Reasoning Trace & Recommendation)
```

## Architectural Components

1. **User Interface (`app.py`, `index.html`, `style.css`)**:
   - Collects user inputs: Crop selection, observed symptoms, microclimate environmental conditions.
   - Formats inputs into key-value initial facts.

2. **Knowledge Base Loader (`api_connector.py` & `knowledge_base.json`)**:
   - Manages rules, disease definitions, symptom lists, and recommendations.
   - Primary: Fetches rules from external API if configured (`X-Api-Key`).
   - Fallback: Loads local zero-dependency `knowledge_base.json`.

3. **Forward Chaining Inference Engine (`inference.py`)**:
   - Maintains **Working Memory**.
   - Executes iterative condition matching against production rules.
   - Infers intermediate facts and appends them to working memory.
   - Logs execution steps in a **Reasoning Trace**.

4. **Diagnostic & Explanation Output**:
   - Displays final identified disease name.
   - Renders step-by-step rule firing trace ($R1 \rightarrow R2 \rightarrow R3 \rightarrow R4$).
   - Provides actionable remediation guidance.
