# Problem Statement

## Title
**Crop Disease Diagnosis using Rule-Based Expert Systems and Forward Chaining**

## Context & Background
Agriculture remains the backbone of the global economy, yet crop loss due to plant diseases poses a severe threat to food security and farm yield. Smallholder farmers often struggle with early and accurate identification of crop diseases because:
1. Different diseases present visually overlapping initial symptoms (e.g., leaf spots, wilting, discoloration).
2. Agricultural extension officers and domain experts are rarely available immediately in rural regions.
3. Machine learning approaches require massive image datasets, heavy compute resources, and lack explainable reasoning paths that farmers and agricultural experts can audit.

## Proposed Solution
This project implements a lightweight, deterministic **Rule-Based Expert System** using **Forward Chaining** inference. By starting from observed initial facts (crop type, leaf symptoms, environmental conditions), the system applies production rules stored in a Knowledge Base to derive new intermediate facts, eventually concluding a probable crop disease diagnosis with a complete step-by-step reasoning trace and remediation recommendation.

## Key Objectives
- Demonstrate data-driven AI reasoning using **Forward Chaining**.
- Show multi-step rule dependencies ($Fact \rightarrow Rule_1 \rightarrow New\ Fact \rightarrow Rule_2 \rightarrow Disease$).
- Provide a clear, transparent reasoning trace for complete explainability.
- Maintain an offline-capable architecture with fallback support for external knowledge APIs.
