"""
Flask Application for Crop Disease Expert System.
Uses DigiGreen Crop Disease Dataset structured knowledge base.
"""

import json
import os
from flask import Flask, render_template, request
from inference import forward_chaining

app = Flask(__name__)

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_knowledge_base():
    """Loads the structured local knowledge base directly from JSON."""
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/", methods=["GET"])
def index():
    kb_data = load_knowledge_base()
    return render_template(
        "index.html",
        crops=kb_data.get("crops", []),
        symptoms=kb_data.get("symptoms", []),
        environmental_conditions=kb_data.get("environmental_conditions", []),
        source="DigiGreen Dataset (Hugging Face)",
        result=None,
        selected_crop="",
        selected_facts={}
    )


@app.route("/diagnose", methods=["POST"])
def diagnose():
    kb_data = load_knowledge_base()
    
    # Extract form inputs
    selected_crop = request.form.get("crop", "").strip()
    
    # Construct initial facts dictionary
    initial_facts = {}
    if selected_crop:
        initial_facts["crop"] = selected_crop.lower()
        
    selected_facts = {}
    
    # Extract symptoms checkboxes
    for sym in kb_data.get("symptoms", []):
        sym_id = sym["id"]
        if request.form.get(sym_id):
            initial_facts[sym_id] = "yes"
            selected_facts[sym_id] = True
            
    # Extract environmental conditions
    for env in kb_data.get("environmental_conditions", []):
        env_id = env["id"]
        if request.form.get(env_id):
            initial_facts[env_id] = "yes"
            selected_facts[env_id] = True

    # Run Forward Chaining Engine
    result = forward_chaining(initial_facts, kb_data)

    return render_template(
        "index.html",
        crops=kb_data.get("crops", []),
        symptoms=kb_data.get("symptoms", []),
        environmental_conditions=kb_data.get("environmental_conditions", []),
        source="DigiGreen Dataset (Hugging Face)",
        result=result,
        selected_crop=selected_crop,
        selected_facts=selected_facts
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
