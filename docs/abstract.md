# Abstract

Plant disease identification is a critical domain where automated artificial intelligence tools can assist agricultural decision-making. While contemporary machine learning models function as opaque "black boxes," expert systems provide transparent, explainable reasoning paths essential for high-stakes domain diagnostics.

This project presents a **Crop Disease Expert System** built from scratch using Python, Flask, HTML/CSS, and JSON to demonstrate the fundamental AI reasoning technique of **Forward Chaining**. The system processes user-selected field observations (crop type, observed symptoms, and microclimate conditions) as initial facts in working memory. Through iterative pattern matching against production rules in a structured Knowledge Base, the inference engine fires matching rules, infers intermediate anatomical/pathological facts, and chains forward until a conclusive disease diagnosis is derived.

The system features a dual knowledge architecture supporting primary external API knowledge fetching with a zero-dependency local JSON database fallback. Evaluation across 8 distinct test scenarios proves that multi-step rule chaining accurately isolates diseases such as Tomato Early Blight, Potato Blackleg, and Rice Blast while presenting farmers and examiners with a step-by-step reasoning trace and tailored remediation guidance.
