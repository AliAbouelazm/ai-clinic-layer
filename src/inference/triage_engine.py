"""Triage decision engine."""

from typing import Dict, Any, Tuple

from src.config import RISK_THRESHOLD_URGENT, RISK_THRESHOLD_CONSULT, TRIAGE_LABELS
from src.models.risk_scoring import compute_risk_score
from src.llm_interface.llm_parser import generate_explanation


def classify_triage(risk_score: float) -> str:
    """
    Classify risk score into triage category.
    
    Args:
        risk_score: Risk score between 0 and 1
        
    Returns:
        Triage label: "urgent", "consult", or "self_care"
    """
    if risk_score >= RISK_THRESHOLD_URGENT:
        return "urgent"
    elif risk_score >= RISK_THRESHOLD_CONSULT:
        return "consult"
    else:
        return "self_care"


def _is_critical_text(text: str) -> bool:
    """
    Check if text contains critical symptoms.
    
    Args:
        text: Raw symptom text
        
    Returns:
        True if critical symptoms detected
    """
    if not text:
        return False
    
    text_lower = text.lower().strip()
    
    if "dying" in text_lower:
        return True
    
    if "heart" in text_lower and any(word in text_lower for word in ["hurt", "pain", "hurting", "hurts", "aching", "ache"]):
        return True
    
    if ("bleeding" in text_lower or "blood" in text_lower) and ("heart" in text_lower or "chest" in text_lower or "pain" in text_lower):
        return True
    
    if "chest" in text_lower and "pain" in text_lower and ("breath" in text_lower or "short" in text_lower):
        return True
    
    return False


def run_triage(
    parsed_symptoms: Dict[str, Any],
    age: int = None,
    sex: str = None,
    raw_text: str = None
) -> Tuple[float, str, str]:
    """
    Run complete triage pipeline.
    
    CRITICAL CHECK HAPPENS FIRST - if critical symptoms detected, returns urgent immediately.
    
    Args:
        parsed_symptoms: Parsed symptom dictionary
        age: Patient age
        sex: Patient sex
        raw_text: Raw symptom text (REQUIRED for critical detection)
        
    Returns:
        Tuple of (risk_score, triage_label, explanation)
    """
    if not raw_text:
        raw_text = parsed_symptoms.get("raw_text", "")
    
    if _is_critical_text(raw_text):
        return (
            0.95,
            "urgent",
            "CRITICAL: Critical symptoms detected (heart pain, chest pain, bleeding, or other severe indicators). Immediate medical attention is required. Please seek emergency care immediately."
        )
    
    symptom_categories = parsed_symptoms.get("symptom_categories", [])
    red_flags = parsed_symptoms.get("red_flags", [])
    severity = parsed_symptoms.get("severity", 0)
    
    if severity >= 9.0:
        return (
            0.95,
            "urgent",
            "CRITICAL: Very high severity detected. Immediate medical attention is required. Please seek emergency care immediately."
        )
    
    if len(red_flags) >= 2:
        return (
            0.95,
            "urgent",
            "CRITICAL: Multiple red flags detected. Immediate medical attention is required. Please seek emergency care immediately."
        )
    
    if "chest_pain" in symptom_categories and "shortness_of_breath" in symptom_categories:
        return (
            0.95,
            "urgent",
            "CRITICAL: Chest pain with shortness of breath is a medical emergency. Please seek emergency care immediately."
        )
    
    if any(flag in ["severe_chest_pain", "difficulty_breathing", "loss_of_consciousness", "critical_severity"] for flag in red_flags):
        return (
            0.95,
            "urgent",
            "CRITICAL: Severe red flags detected. Immediate medical attention is required. Please seek emergency care immediately."
        )
    
    if ("bleeding" in (raw_text or "").lower() or "blood" in (raw_text or "").lower()) and severity >= 7.0:
        return (
            0.95,
            "urgent",
            "CRITICAL: Bleeding with high severity detected. Immediate medical attention is required. Please seek emergency care immediately."
        )
    
    try:
        risk_score = compute_risk_score(parsed_symptoms, age, sex)
        triage_label = classify_triage(risk_score)
        explanation = generate_explanation(risk_score, triage_label, parsed_symptoms, red_flags)
    except Exception:
        risk_score = 0.3
        triage_label = "consult"
        explanation = "Unable to compute risk score. Please consult with a healthcare provider."
    
    return risk_score, triage_label, explanation
