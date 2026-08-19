# Abstract

Plant disease identification is a critical domain where automated artificial intelligence tools can assist agricultural decision-making. While contemporary machine learning models function as opaque "black boxes," expert systems provide transparent, explainable reasoning paths essential for high-stakes domain diagnostics.

This project presents an enhanced **Crop Disease Expert System** built from scratch using Python, Flask, HTML/CSS, and JSON to demonstrate the core symbolic AI reasoning technique of **Forward Chaining** combined with a transparent **Candidate Disease Ranking Fallback**.

The inference engine operates via a **Two-Stage Reasoning Architecture**:
1. **Stage 1 (Forward Chaining)**: Processes user observations (crop type, observed symptoms, and environmental conditions) as initial facts in working memory. Through iterative pattern matching against production rules in a structured Knowledge Base (derived from the Hugging Face `DigiGreen/Crop_Disease_Images` dataset), matching rules fire sequentially to infer intermediate facts and conclude a definitive **Strong Match** diagnosis.
2. **Stage 2 (Candidate Disease Ranking Fallback)**: If Forward Chaining does not reach a definitive rule match, candidate diseases matching the target crop are evaluated by partial evidence match score ($\text{score} = \frac{\text{matched}}{\text{total}} \times 100$). Matches $\ge 50\%$ yield a **Possible Disease** state with missing symptom suggestions, while scores $< 50\%$ yield **Insufficient Evidence**, completely eliminating misleading `"Unknown / Healthy"` false negatives.

Evaluation across 8 automated unit test scenarios proves that multi-step rule chaining and fallback candidate ranking accurately diagnose diseases across 6 crop types while presenting farmers and examiners with clear step-by-step reasoning traces, matched vs. missing symptom analysis, and state-dependent remediation guidance.
