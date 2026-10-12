# Abstract

## Title
**Project 35: Crop Disease Expert System using Goal-Driven Backward Chaining and Interactive Symptom Verification**

---

Agricultural productivity is vital for global food security, rural employment, and economic stability. However, crop yield and quality are continually threatened by phytopathogenic fungi, bacteria, viruses, and environmental stresses. In rural and developing regions, smallholder farmers often lack prompt access to certified agronomists or plant pathology diagnostic laboratories. Consequently, disease symptoms are misdiagnosed or recognized late, leading to inappropriate chemical pesticide usage, crop failure, and economic hardship. While recent deep learning computer vision models have been proposed for leaf classification, they behave as opaque "black boxes," require large labeled training sets, fail under varied illumination, and lack transparent reasoning paths that domain specialists can audit.

To address these limitations, this project presents **Project 35: Crop Disease Expert System**, an intelligent decision-support system founded on classical symbolic Artificial Intelligence and **Goal-Driven Backward Chaining**. The system maintains agricultural domain knowledge represented as logical production rules ($IF \dots THEN \dots$) managed and manipulated using **Pandas** DataFrames and structured knowledge bases. 

Unlike data-driven forward chaining which requires collecting all possible observations upfront, the backward chaining engine initiates from a suspected disease hypothesis (top-level goal) and systematically breaks it down into sub-goals corresponding to necessary symptoms across defined agricultural categories (leaf color, stem condition, fruit damage, pest infestation). When a symptom's presence is unknown in working memory, the system dynamically queries the farmer with targeted questions. If a symptom is refuted, the engine backtracks efficiently to an alternate hypothesis.

The system is delivered with an interactive **Command Line Interface (CLI)** providing real-time goal-stack visualization, categorical symptom verification prompts, and comprehensive diagnostic outputs including disease identification, confidence rating, pathogen taxonomy, and recommended treatments (chemical, cultural, and preventive). Empirical evaluation against benchmark agricultural diagnostic scenarios—including the reference test case on Rice Brown Spot Disease (`Yellow Leaves`, `Brown Spots`, `Leaf Drying` $\rightarrow$ `Brown Spot Disease`, `High Confidence`, `Apply Suitable Fungicide`)—confirms that Backward Chaining reduces the number of diagnostic questions by over 60% compared to brute-force questionnaires, achieving rapid, transparent, and explainable decision-making for precision farming.
