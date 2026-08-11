# System Diagrams

This document contains the three core system diagrams for the Crop Disease Expert System: System Architecture, Activity Diagram, and Data Flow Diagram (DFD).

---

## 1. System Architecture Diagram

```mermaid
graph TD
    A[User] -->|Selects Crop & Symptoms| B[User Interface / Flask]
    B -->|Generates Initial Facts| C[Working Memory]
    D[Knowledge Base: API / JSON Fallback] -->|Loads Production Rules| E[Forward Chaining Engine]
    C -->|Pattern Match Conditions| E
    E -->|Fire Rule & Derive New Facts| C
    E -->|Output Diagnosis & Trace| B
    B -->|Display Results & Recommendation| A
```

---

## 2. Activity Diagram

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> SelectCropAndSymptoms: User inputs crop & symptoms
    SelectCropAndSymptoms --> LoadKnowledgeBase: Fetch rules (API or Local JSON)
    LoadKnowledgeBase --> InitWorkingMemory: Load initial facts
    
    state ForwardChainingPass {
        InitWorkingMemory --> ScanRules: Check un-fired rules
        ScanRules --> MatchConditions: Are rule conditions satisfied?
        MatchConditions --> FireRule: YES -> Fire Rule
        FireRule --> AddNewFacts: Add conclusions to working memory
        AddNewFacts --> ScanRules: Repeat pass
        MatchConditions --> StopPass: NO matching rules left
    }

    StopPass --> ExtractDiagnosis: Check if 'disease' fact exists
    ExtractDiagnosis --> RenderResults: Format reasoning trace & recommendation
    RenderResults --> [*]
```

---

## 3. Simple Data Flow Diagram (DFD Level 1)

```
[ User ] 
   │
   │ 1. Form Submission (Crop, Symptoms, Environment)
   ▼
( Process 1.0: Fact Collector )
   │
   │ 2. Initial Facts Dictionary
   ▼
( Process 2.0: Forward Chaining Engine ) ◄──── [ Knowledge Base Store (JSON/API) ]
   │                                              (Rules & Disease Metadata)
   │ 3. Working Memory Updates & Fired Rules
   ▼
( Process 3.0: Explanation Generator )
   │
   │ 4. Diagnosis, Reasoning Trace, Recommendation
   ▼
[ User ]
```
