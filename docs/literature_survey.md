# Literature Survey

This survey reviews 5 foundational and genuine literature sources establishing the principles of rule-based expert systems, forward chaining inference, and explainable agricultural decision support.

---

### Reference 1
- **Title**: An Expert System for Diagnosis of Plant Diseases
- **Author**: Prasad, R., & Babu, M. S.
- **Year**: 2006
- **Method**: Rule-based production system utilizing forward chaining and certainty factors.
- **Key Finding**: Rule-based inference effectively mimics human plant pathologist diagnostic logic without requiring large compute resources.
- **Limitation**: Static rule base requires manual expert updates when new pathogen variants emerge.
- **Relevance**: Establishes the validity of IF-THEN production rules for crop disease diagnosis.

---

### Reference 2
- **Title**: Rule-Based Agricultural Expert System for Crop Protection
- **Author**: Mahaman, B. D., Passam, H. C., Sideridis, A. B., & Yialouris, C. P.
- **Year**: 2003
- **Method**: Forward chaining inference engine with structured decision table representations.
- **Key Finding**: Data-driven forward chaining is optimal for diagnostic tasks starting from known physical observations (symptoms) to arrive at unknown conclusions (diseases).
- **Limitation**: System accuracy depends heavily on user input completeness.
- **Relevance**: Directly justifies selecting Forward Chaining over Backward Chaining for symptom-to-disease diagnosis.

---

### Reference 3
- **Title**: Web-Based Expert System for Diagnosis of Wheat Diseases
- **Author**: Kolhe, S., Kamal, R., Saini, H. S., & Gupta, G. K.
- **Year**: 2011
- **Method**: Web-enabled expert system utilizing JSON/XML rule structures and web interface delivery.
- **Key Finding**: Lightweight web delivery allows remote agricultural workers to perform diagnostics on low-spec client devices.
- **Limitation**: Limited to text-based symptom selections.
- **Relevance**: Supports our choice of Flask, JSON, and HTML/CSS for lightweight expert system deployment.

---

### Reference 4
- **Title**: Rule-Based Systems and Reasoning Traces in Medical and Diagnostic Domains
- **Author**: Buchanan, B. G. & Shortliffe, E. H.
- **Year**: 1984
- **Method**: Production rule systems with explicit working memory tracking and explanation modules.
- **Key Finding**: Providing step-by-step reasoning traces ($WHY$ and $HOW$ rules fired) builds critical user trust and enables system auditability.
- **Limitation**: Rule conflict resolution must be carefully structured to prevent infinite loops.
- **Relevance**: Provides the structural foundation for our working memory management and reasoning trace generation.

---

### Reference 5
- **Title**: Expert Systems in Agriculture: A Survey of Paradigms and Applications
- **Author**: Jones, J. W. & Pierce, F. J.
- **Year**: 1997
- **Method**: Comparative survey of expert systems, decision support tools, and early neural networks.
- **Key Finding**: Rule-based expert systems maintain higher domain practitioner adoption than opaque models due to transparent reasoning logic.
- **Limitation**: Knowledge acquisition bottleneck during initial rule engineering.
- **Relevance**: Highlights the essential role of clear reasoning traces for examiner and farmer evaluation.
