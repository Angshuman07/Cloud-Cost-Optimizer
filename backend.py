import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import re


load_dotenv()

hf_token = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct", 
    token=hf_token
)

def extract_json(text):
    """
    Extracts the first valid JSON object or array from a string 
    using a stack to match brackets.
    """
    start = None
    stack = []
    
    for i, ch in enumerate(text):
        if ch in ['{', '[']:
            if start is None:
                start = i
            stack.append(ch)

        elif ch in ['}', ']'] and stack:
            opening = stack.pop()
            if (opening == '{' and ch != '}') or (opening == '[' and ch != ']'):
                continue
            if not stack:
                return text[start:i+1]

    raise ValueError("No complete JSON found in model response")

def get_json_response(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=4000, 
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        json_text = extract_json(content)
        return json.loads(json_text)
    except Exception as e:
        print(f"Error communicating with LLM: {e}")
        return None

def save_json(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[OK] Saved: {filename}")
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARN]  File not found: {filename}")
        return None


def generate_profile(description_text):
    print("\n--- Step 1: Generating Project Profile ---")
    system_prompt = """
    You are a technical architect. Extract details from the project description and output strictly a valid JSON object.
    Do not include any markdown formatting or explanatory text outside the JSON.
    Required keys: "name", "budget_inr_per_month" (integer), "description", "tech_stack" (object), "non_functional_requirements" (list).
    """
    return get_json_response(system_prompt, description_text)

def generate_billing(profile_data):
    print("\n--- Step 2: Generating Synthetic Billing ---")

    system_prompt = """
    You are a cloud billing generator. Based on the project profile, generate a synthetic monthly billing dataset.
    The billing MUST match these rules:
    - Output ONLY valid JSON. No explanations. No markdown. No text outside JSON.
    - JSON must be a LIST of 12–20 objects.
    - Total monthly cost must NOT exceed the project's budget.
    - Use cloud-agnostic names (Compute Instance, Object Storage, Database Instance, Monitoring, Analytics, etc.)
    
    Each billing record MUST contain:
    "month": "2025-01",
    "service": "Compute Instance | Database Instance | Object Storage | Monitoring | Analytics | etc.",
    "resource_id": "string",
    "region": "string",
    "usage_type": "string",
    "usage_quantity": number,
    "unit": "hours | GB | requests | objects | rows | etc.",
    "cost_inr": integer,
    "desc": "short description of the resource"

    Return ONLY the JSON array.
    """
    user_prompt = f"Create a billing breakdown for this profile: {json.dumps(profile_data)}"
    return get_json_response(system_prompt, user_prompt)

def analyze_costs(profile_data, billing_data):
    print("\n--- Step 3: Analyzing Costs & Generating Report ---")
    
    system_prompt = """
    You are a Cloud FinOps Expert. Analyze the Project Profile and Billing Data.
    Output a detailed optimization report in strictly valid JSON format.
    
    The JSON must match this structure:
    {
        "project_name": "String",
        "analysis": {
            "total_monthly_cost": Int,
            "budget": Int,
            "budget_variance": Int,
            "is_over_budget": Boolean,
            "service_costs": { "ServiceName": Int, ... }
        },
        "recommendations": [
            {
                "title": "String",
                "service": "String",
                "current_cost": Int,
                "potential_savings": Int,
                "recommendation_type": "open_source" OR "right_sizing" OR "free_tier",
                "description": "String",
                "implementation_effort": "low/medium/high",
                "risk_level": "low/medium/high",
                "steps": ["Step 1", "Step 2"],
                "cloud_providers": ["AWS", "Azure", "GCP"]
            }
        ]
    }
    """
    user_prompt = f"Profile: {json.dumps(profile_data)}\n\nBilling: {json.dumps(billing_data)}"
    return get_json_response(system_prompt, user_prompt)