# System Diagrams & Flowcharts

This document provides visual diagrams modeling the **Backward Chaining Inference Engine**, interactive dialogue flow, class relationships, and hypothesis state lifecycles for **Project 35: Crop Disease Expert System**.

---

## 1. Backward Chaining Inference Flowchart

```mermaid
flowchart TD
    Start([Start Diagnostic Session]) --> SelectCrop[Farmer Selects Crop & Optional Clues]
    SelectCrop --> LoadRules[Engine Queries Rules for Crop via Pandas]
    LoadRules --> PickHypothesis[Select Suspected Disease Hypothesis H]
    
    PickHypothesis --> PushGoal[Push H onto Goal Stack]
    PushGoal --> GetPremises[Decompose Rule: Extract Required Symptoms S1..Sn]
    
    GetPremises --> NextSymptom{More Symptoms to Verify?}
    NextSymptom -- Yes --> PushSubGoal[Push Sub-Goal Si onto Stack]
    
    PushSubGoal --> CheckWM{Symptom in Working Memory?}
    CheckWM -- Known True --> PopSubGoalTrue[Sub-Goal Verified! Pop Sub-Goal]
    CheckWM -- Known False --> RefuteHypothesis[Sub-Goal Refuted! Pop Sub-Goal]
    
    CheckWM -- Unknown --> AskFarmer[Ask Farmer Targeted Question by Category]
    AskFarmer --> FarmerAnswer{Farmer Response?}
    FarmerAnswer -- Yes --> RecordTrue[Record Si = True in Working Memory]
    RecordTrue --> PopSubGoalTrue
    
    FarmerAnswer -- No --> RecordFalse[Record Si = False in Working Memory]
    RecordFalse --> RefuteHypothesis
    
    PopSubGoalTrue --> NextSymptom
    
    RefuteHypothesis --> Backtrack[Pop H from Stack: BACKTRACK]
    Backtrack --> MoreHypotheses{Remaining Disease Hypotheses?}
    MoreHypotheses -- Yes --> PickHypothesis
    MoreHypotheses -- No --> Inconclusive([Diagnosis Inconclusive: Refer to Agronomist])
    
    NextSymptom -- No (All True) --> GoalSatisfied[Goal H Satisfied! All Premises Proven]
    GoalSatisfied --> DeriveOutput[Output Identified Disease, Confidence: High, & Treatment]
    DeriveOutput --> Done([End Session])
```

---

## 2. Interactive Sequence Diagram (Rice Sample Case)

```mermaid
sequenceDiagram
    autonumber
    actor Farmer as Farmer / Examiner
    participant UI as Command Line Interface (CLI)
    participant Engine as BackwardChainingEngine
    participant Pandas as Pandas Rule DataFrame
    participant WM as Working Memory

    Farmer->>UI: Selects Crop: 'Rice'
    UI->>Engine: diagnose(crop='Rice', ask_callback)
    Engine->>Pandas: filter(crop == 'Rice')
    Pandas-->>Engine: Rules: [RULE_RICE_01: Brown Spot, RULE_RICE_02: Bacterial Blight, ...]
    
    rect rgb(240, 248, 255)
        Note over Engine: Goal Stack: [Goal: Brown Spot Disease]
        Engine->>WM: Check 'Yellow Leaves'
        WM-->>Engine: Unknown
        Engine->>UI: Targeted Question [Leaf Color]: "Are leaves turning yellow?"
        UI->>Farmer: Prompt: "Are leaves turning yellow?" (Yes/No)
        Farmer-->>UI: Response: YES
        UI-->>Engine: True
        Engine->>WM: Save 'Yellow Leaves' = True
    end

    rect rgb(240, 248, 255)
        Note over Engine: Sub-Goal: Verify 'Brown Spots'
        Engine->>WM: Check 'Brown Spots'
        WM-->>Engine: Unknown
        Engine->>UI: Targeted Question [Leaf Condition]: "Are distinct brown spots visible?"
        UI->>Farmer: Prompt: "Are distinct brown spots visible?" (Yes/No)
        Farmer-->>UI: Response: YES
        UI-->>Engine: True
        Engine->>WM: Save 'Brown Spots' = True
    end

    rect rgb(240, 248, 255)
        Note over Engine: Sub-Goal: Verify 'Leaf Drying'
        Engine->>WM: Check 'Leaf Drying'
        WM-->>Engine: Unknown
        Engine->>UI: Targeted Question [Stem Condition]: "Are leaf margins/tips drying?"
        UI->>Farmer: Prompt: "Are leaf margins/tips drying?" (Yes/No)
        Farmer-->>UI: Response: YES
        UI-->>Engine: True
        Engine->>WM: Save 'Leaf Drying' = True
    end

    Note over Engine: All required premises for RULE_RICE_01 satisfied!
    Engine-->>UI: Result: Brown Spot Disease, High Confidence, "Apply Suitable Fungicide"
    UI->>Farmer: Displays Disease Identified, Treatment Plan, & Reasoning Trace
```

---

## 3. Class Diagram

```mermaid
classDiagram
    class BackwardChainingEngine {
        -str kb_path
        -dict kb
        -DataFrame rules_df
        -DataFrame symptoms_df
        -dict diseases
        -list crops
        -dict symptom_meta
        +load_knowledge_base() dict
        +get_supported_crops() list
        +get_crop_diseases(crop) list
        +get_all_symptoms_for_crop(crop) list
        +get_symptom_category(symptom_name) str
        +get_symptom_question(symptom_name) str
        +diagnose(crop, initial_symptoms, suspected_disease, ask_callback) dict
    }

    class CommandLineInterface {
        +print_banner()
        +main_menu_loop(engine)
        +run_cli_interactive_diagnosis(engine)
        +run_benchmark_demo(engine)
        +run_batch_symptoms_diagnosis(engine)
        +explore_knowledge_base(engine)
        +format_report_box(result)
        +display_reasoning_trace(trace)
    }

    class KnowledgeBaseBuilder {
        +build_knowledge_base() dict
        +export_to_csv()
    }

    CommandLineInterface --> BackwardChainingEngine : invokes inference & queries
    KnowledgeBaseBuilder ..> BackwardChainingEngine : produces KB data
```

---

## 4. State Transition Diagram: Hypothesis Lifecycle

```mermaid
stateDiagram-v2
    [*] --> UNTESTED : Hypothesis Selected
    UNTESTED --> EVALUATING_SUBGOALS : Pushed to Goal Stack
    
    state EVALUATING_SUBGOALS {
        [*] --> CHECKING_WORKING_MEMORY
        CHECKING_WORKING_MEMORY --> SUBGOAL_VERIFIED : Fact in Memory (True)
        CHECKING_WORKING_MEMORY --> SUBGOAL_REFUTED : Fact in Memory (False)
        CHECKING_WORKING_MEMORY --> ASKING_FARMER : Fact Unknown
        ASKING_FARMER --> SUBGOAL_VERIFIED : Farmer answers Yes
        ASKING_FARMER --> SUBGOAL_REFUTED : Farmer answers No
    }
    
    EVALUATING_SUBGOALS --> BACKTRACKING : Any Required Sub-Goal Refuted
    BACKTRACKING --> UNTESTED : Next Candidate Rule/Hypothesis Available
    BACKTRACKING --> INCONCLUSIVE : All Hypotheses Exhausted
    
    EVALUATING_SUBGOALS --> HYPOTHESIS_CONFIRMED : All Sub-Goals Verified True
    
    HYPOTHESIS_CONFIRMED --> [*] : Output Diagnosis & Treatment
    INCONCLUSIVE --> [*] : Refer to Agricultural Officer
```
