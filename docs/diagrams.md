# System Diagrams

This document contains the three core system diagrams for the Crop Disease Expert System: System Architecture, Activity Diagram, and Data Flow Diagram (DFD Level 1), reflecting the Two-Stage Reasoning process and Three Result States.

---

## 1. System Architecture Diagram

```mermaid
graph TD
    A[User Inputs] -->|Crop & Symptoms| B[Flask Controller app.py]
    B -->|Initial Facts| C[Working Memory]
    D[Knowledge Base JSON] -->|Production Rules & Disease Profiles| E[Stage 1: Forward Chaining Engine]
    C -->|Pattern Match Conditions| E
    E -->|Definitive Rule Fired?| F{Rule Derived Disease?}
    F -->|YES| G[STATE 1: Strong Match]
    F -->|NO| H[Stage 2: Candidate Disease Ranking Engine]
    H -->|Filter by Selected Crop| I[Crop Compatibility Filter]
    I -->|Calculate Match Score %| J{Top Score >= 50%?}
    J -->|YES| K[STATE 2: Possible Disease]
    J -->|NO| L[STATE 3: Insufficient Evidence]
    G --> M[UI Output: Badges, Trace, Recommendation]
    K --> M
    L --> M
    M -->|Display Result| A
```

---

## 2. Activity Diagram

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> SelectCropAndSymptoms: User submits crop & symptoms
    SelectCropAndSymptoms --> LoadKnowledgeBase: Load knowledge_base.json
    LoadKnowledgeBase --> InitWorkingMemory: Initialize working memory facts

    state Stage1_ForwardChaining {
        InitWorkingMemory --> ScanRules: Inspect production rules
        ScanRules --> MatchConditions: Are rule conditions satisfied?
        MatchConditions --> FireRule: YES -> Fire Rule
        FireRule --> AddConclusions: Add conclusions to working memory
        AddConclusions --> ScanRules: Repeat pass
        MatchConditions --> EndStage1: NO un-fired rules match
    }

    EndStage1 --> CheckDefinitiveDisease: Did FC derive a disease?
    CheckDefinitiveDisease --> State1_StrongMatch: YES -> Set State 1 Strong Match

    state Stage2_CandidateRanking {
        CheckDefinitiveDisease --> FilterCropDiseases: NO -> Filter diseases by target crop
        FilterCropDiseases --> CalculateScores: Compute match_score = (matched / total) * 100
        CalculateScores --> CheckThreshold: Top Match Score >= 50%?
        CheckThreshold --> State2_PossibleDisease: YES -> Set State 2 Possible Disease
        CheckThreshold --> State3_InsufficientEvidence: NO -> Set State 3 Insufficient Evidence
    }

    State1_StrongMatch --> RenderUI: Format reasoning trace & strong recommendation
    State2_PossibleDisease --> RenderUI: Format match score, missing symptoms & alternatives
    State3_InsufficientEvidence --> RenderUI: Format prompt for additional observations
    RenderUI --> [*]
```

---

## 3. Data Flow Diagram (DFD Level 1)

```
[ User ] 
   │
   │ 1. Form Submission (Crop, Symptoms, Environmental Conditions)
   ▼
( Process 1.0: Fact Collector )
   │
   │ 2. Initial Facts Dictionary
   ▼
( Process 2.0: Two-Stage Inference Engine ) ◄──── [ Knowledge Base Store (JSON) ]
   │                                              (DigiGreen Rules & Disease Profiles)
   ├─► Stage 1: Forward Chaining Loop
   └─► Stage 2: Candidate Ranking Fallback (if no FC rule derived)
   │
   │ 3. State Output (Strong Match / Possible Disease / Insufficient Evidence)
   ▼
( Process 3.0: Explanation Generator )
   │
   │ 4. Matched/Missing Symptoms, Reasoning Trace, Alternatives, Recommendation
   ▼
[ User ]
```
