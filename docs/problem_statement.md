# Problem Statement

## Title
**Crop Disease Diagnosis using Two-Stage Rule-Based Expert Systems (Forward Chaining & Candidate Ranking)**

## Context & Background
Agriculture remains the backbone of the global economy, yet crop loss due to plant diseases poses a severe threat to food security and farm yield. Smallholder farmers often struggle with early and accurate identification of crop diseases because:
1. Different diseases present visually overlapping initial symptoms (e.g., leaf spots, wilting, discoloration).
2. Agricultural extension officers and domain experts are rarely available immediately in rural regions.
3. Machine learning approaches require massive image datasets, heavy compute resources, and lack explainable reasoning paths that farmers and agricultural experts can audit.
4. Traditional expert systems often output misleading `"Unknown / Healthy"` false negatives whenever no single rule matches 100% of conditions.

## Proposed Solution
This project implements a lightweight, deterministic **Two-Stage Rule-Based Expert System**:
1. **Stage 1 (Forward Chaining)**: Executes data-driven forward chaining as the primary reasoning mechanism. If a disease conclusion rule fires, the system yields a **Strong Match**.
2. **Stage 2 (Candidate Disease Ranking Fallback)**: If Forward Chaining does not yield a definitive rule match, the engine ranks crop-compatible diseases by partial evidence match score:
   $$\text{match\_score} = \frac{\text{matched\_symptoms}}{\text{total\_symptoms}} \times 100$$
   - Scores $\ge 50\%$ yield **Possible Disease**.
   - Scores $< 50\%$ yield **Insufficient Evidence** (eliminating false healthy diagnoses).

## Key Objectives
- Demonstrate data-driven AI reasoning using **Forward Chaining** as the core mechanism.
- Implement partial evidence candidate ranking fallback for incomplete symptom inputs.
- Establish three meaningful diagnostic states: **Strong Match**, **Possible Disease**, and **Insufficient Evidence**.
- Enforce strict crop compatibility filtering (e.g., excluding Potato diseases when diagnosing Tomato).
- Provide transparent reasoning traces, matched vs. missing symptom analysis, and actionable state-dependent recommendations.
