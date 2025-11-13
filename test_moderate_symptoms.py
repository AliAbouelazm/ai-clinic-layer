"""Test moderate symptoms (50-70% risk range)."""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.llm_interface.llm_parser import parse_symptom_text
from src.inference.triage_engine import run_triage

moderate_test_cases = [
    "persistent fever for 3 days with body aches",
    "moderate abdominal pain that's getting worse",
    "chest discomfort when breathing deeply",
    "significant bleeding from a cut that won't stop",
    "severe headache with nausea",
    "moderate chest pain without breathing issues",
    "fever with severe fatigue",
    "abdominal pain with vomiting",
    "moderate injury to wrist with swelling",
    "persistent cough with chest tightness",
]

print("Testing moderate symptoms (target: 50-70% risk):")
print("=" * 80)

for symptom_text in moderate_test_cases:
    try:
        parsed = parse_symptom_text(symptom_text)
        parsed["raw_text"] = symptom_text
        
        risk_score, triage_label, explanation = run_triage(
            parsed_symptoms=parsed,
            age=30,
            sex="M",
            raw_text=symptom_text
        )
        
        status = "✓" if 0.50 <= risk_score <= 0.70 else "✗"
        print(f"{status} {symptom_text[:60]}")
        print(f"   Risk: {risk_score:.2%} | Triage: {triage_label} | Severity: {parsed.get('severity', 0):.1f}/10")
        print()
    except Exception as e:
        print(f"ERROR: {e}")
        print()

