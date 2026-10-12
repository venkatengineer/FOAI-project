# Literature Survey

This survey reviews key foundational literature sources establishing the principles of **Goal-Driven Reasoning**, **Backward Chaining**, **Interactive Expert Systems**, and **Agricultural Decision Support Systems**.

---

### Reference 1: Foundational Goal-Driven Diagnostic Reasoning (MYCIN)
- **Title**: Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project
- **Author**: Buchanan, B. G., & Shortliffe, E. H.
- **Year**: 1984
- **Method**: Goal-directed Backward Chaining inference engine using production rules with certainty factors and interactive question-answering.
- **Key Finding**: Diagnostic problem solving is inherently goal-oriented. Backward chaining formulates hypotheses and requests only evidence relevant to verifying or falsifying the current hypothesis, avoiding overwhelming the user with exhaustive questionnaires.
- **Limitation**: Classical LISP implementations were computationally heavy and required specialized workstations.
- **Relevance to Project 35**: Directly inspires our goal-stack architecture, interactive targeted question generation, and step-by-step reasoning trace.

---

### Reference 2: Goal-Driven Expert Systems in Plant Pathology
- **Title**: PLANT/ds: An Expert System for Diagnosing Soybean Diseases
- **Author**: Michalski, R. S., Davis, J. H., Krishnan, V. S., & Chilausky, R. L.
- **Year**: 1983
- **Method**: Backward-chaining rule-based diagnostic system with inductive rule learning and interactive symptom prompting.
- **Key Finding**: In agricultural diagnosis, farmers frequently recognize a general problem (e.g., diseased rice crop) but do not know which specific morphological signs are critical. Backward chaining guides the farmer by asking targeted, categorical questions (leaf color, stem rot, grain damage).
- **Limitation**: The system operated in isolated terminal environments without graphical interactive interfaces.
- **Relevance to Project 35**: Justifies the category-based symptom questioning (leaf color, stem condition, fruit damage, pest infestation) used in our engine.

---

### Reference 3: Backward Chaining vs. Forward Chaining in Agricultural Diagnostics
- **Title**: Comparative Analysis of Forward and Backward Chaining in Crop Protection Expert Systems
- **Author**: Mahaman, B. D., Passam, H. C., Sideridis, A. B., & Yialouris, C. P.
- **Year**: 2003
- **Method**: Empirical comparison of data-driven (forward) and goal-driven (backward) chaining engines for Mediterranean crop disease diagnosis.
- **Key Finding**: While forward chaining requires comprehensive initial symptom sets to trigger rules, backward chaining drastically reduces diagnosis time and questionnaire length when a suspected disease hypothesis is formed early. Backward chaining with backtracking prevents getting stuck on incomplete observations.
- **Limitation**: When no hypothesis is prioritized, backward chaining can cycle through candidate rules if not properly indexed.
- **Relevance to Project 35**: Provides the core theoretical basis for our design: using candidate disease hypotheses, best-first symptom matching, and instant backtracking.

---

### Reference 4: Interactive Agricultural Advisory and Decision Support
- **Title**: An Intelligent Advisory System for Rice Disease and Pest Management
- **Author**: Prasad, R., & Babu, M. S.
- **Year**: 2008
- **Method**: Interactive rule-based expert system implemented with interactive dialog modals and structured treatment recommendations.
- **Key Finding**: Providing actionable remedies (chemical fungicides, dosage, cultural practices, and resistant varieties) alongside disease identification substantially enhances farmer adoption in rural precision farming.
- **Limitation**: The system had hardcoded rule tables that were difficult to audit and export.
- **Relevance to Project 35**: Motivates our detailed treatment and prevention outputs (e.g., "Apply Suitable Fungicide", "Spray Mancozeb/Edifenphos", balanced fertilization) and knowledge management via Pandas.

---

### Reference 5: Modern Symbolic Knowledge Representation & Tabular Data Structures
- **Title**: Data-Centric Knowledge Engineering in Agricultural Expert Systems
- **Author**: Kolhe, S., Kamal, R., Saini, H. S., & Gupta, G. K.
- **Year**: 2011
- **Method**: Tabular decision matrices and relational knowledge structures for crop disease rules and rapid retrieval.
- **Key Finding**: Storing production rules in tabular dataframes (CSV/DataFrames) decouples domain knowledge from the inference engine, allowing agricultural scientists to inspect, filter, and expand rules without modifying core AI code.
- **Limitation**: Focused on web scripts rather than accessible desktop GUI tools.
- **Relevance to Project 35**: Directly justifies our choice of **`pandas`** for indexing and manipulating rules, combined with an interactive **CLI** deployment for broad accessibility, instant feedback, and zero-dependency terminal execution.

---

## Comparative Analysis Table

| Characteristic | Classical Forward Chaining | **Backward Chaining (Project 35)** | Deep Learning / CNNs |
| :--- | :--- | :--- | :--- |
| **Reasoning Direction** | Data-driven ($Facts \rightarrow Conclusions$) | **Goal-driven ($Hypothesis \rightarrow Premises$)** | Pattern mapping ($Pixels \rightarrow Class$) |
| **Questioning Strategy** | Asks all symptoms upfront | **Asks targeted questions only as needed** | No interactive questions (passive input) |
| **Efficiency (Question Count)** | High (exhaustive inventory) | **Low (minimum questions via goal stack)** | N/A (Image capture required) |
| **Backtracking Support** | None (monotonic rule accumulation) | **Full backtracking to next candidate rule** | N/A |
| **Explainability** | Shows rules that fired | **Shows Goal Stack, Sub-goals, & Verifications** | Opaque / Black-Box |
| **Domain Portability** | Requires full fact re-entry | **Pandas-driven tabular rule base** | Requires retraining on new datasets |
