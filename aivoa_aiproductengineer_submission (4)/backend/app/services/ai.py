import json
import re
from typing import TypedDict

from langgraph.graph import END, StateGraph

from ..config import settings
from ..schemas import AIExtraction, CompletenessResult, RiskAssessment, RootCauseResult, SimilarityResult

class ComplaintState(TypedDict, total=False):
    text: str
    extracted: dict
    risk: dict
    completeness: dict
    root_cause: dict
    duplicates: dict


def _json_from_text(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.S)
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start:end + 1])
    raise ValueError("No JSON object found in model output")


def _mock_extract(text: str) -> AIExtraction:
    lower = text.lower()
    priority = "High" if any(w in lower for w in ["serious", "hospital", "adverse", "death", "injury"]) else "Medium"
    return AIExtraction(
        complaint_source="Customer Email",
        customer_name="Acme Pharma Distributor",
        product_name="Paracetamol Tablets",
        product_strength="500 mg",
        batch_number="PCM-25A014",
        manufacturing_date="2025-01-14",
        expiry_date="2027-01-13",
        complaint_details=text[:1000],
        patient_or_consumer="Adult patient; non-life-threatening symptoms reported.",
        initial_assessment="Possible quality complaint requiring QA review and batch investigation.",
        priority=priority,
    )


def _mock_risk(data: dict) -> RiskAssessment:
    txt = json.dumps(data).lower()
    high = any(w in txt for w in ["hospital", "adverse", "injury", "death", "serious"])
    score = 82 if high else 58
    return RiskAssessment(
        risk_level="High" if high else "Medium",
        priority="High" if high else data.get("priority", "Medium"),
        score=score,
        rationale="Potential patient impact and product-quality concern require documented triage, QA review, and traceability.",
        recommended_actions=[
            "Verify batch/lot traceability and complaint authenticity.",
            "Review retained samples and batch release/production records.",
            "Escalate to QA/pharmacovigilance when patient impact is confirmed.",
        ],
    )


def _mock_complete(data: dict) -> CompletenessResult:
    labels = {
        "customer_name": "Customer Name",
        "product_name": "Product Name",
        "batch_number": "Batch/Lot Number",
        "complaint_details": "Complaint Details",
        "patient_or_consumer": "Patient/Consumer",
    }
    missing = [label for key, label in labels.items() if not str(data.get(key, "")).strip()]
    score = round((len(labels) - len(missing)) / len(labels) * 100)
    return CompletenessResult(
        complete=not missing,
        score=score,
        missing_fields=missing,
        notes=["Required traceability fields are the first review gate.", "Capture missing facts before final QA disposition."] if missing else ["Core intake fields are populated."]
    )


def _mock_root(data: dict) -> RootCauseResult:
    return RootCauseResult(
        likely_causes=[
            "Packaging or labeling variation",
            "Manufacturing-process deviation",
            "Storage/transport handling issue",
        ],
        capa_recommendations=[
            "Quarantine affected inventory when warranted by QA assessment.",
            "Perform batch-record and retain-sample review.",
            "Document CAPA owner, due date, and effectiveness check.",
        ],
        investigation_questions=[
            "Does the complaint cluster by batch, market, or distributor?",
            "Were temperature/humidity excursions recorded?",
            "Are there related complaints for the same product or batch?",
        ],
    )


def _get_llm():
    if settings.ai_provider.lower() != "gemini" or not settings.gemini_api_key:
        return None
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model=settings.gemini_model, google_api_key=settings.gemini_api_key, temperature=0)


def extract(text: str) -> AIExtraction:
    llm = _get_llm()
    if llm is None:
        return _mock_extract(text)
    prompt = f"""Extract a pharmaceutical customer complaint into strict JSON. Use empty strings when unknown.\nFields: complaint_source, customer_name, product_name, product_strength, batch_number, manufacturing_date, expiry_date, complaint_details, patient_or_consumer, initial_assessment, priority.\nComplaint:\n{text[:settings.max_text_chars]}"""
    result = llm.invoke(prompt)
    return AIExtraction.model_validate(_json_from_text(result.content))


def risk(data: dict) -> RiskAssessment:
    llm = _get_llm()
    if llm is None:
        return _mock_risk(data)
    prompt = f"Assess complaint risk. Return JSON with risk_level (Low/Medium/High/Critical), priority, score 0-100, rationale, recommended_actions.\nData: {json.dumps(data)}"
    result = llm.invoke(prompt)
    return RiskAssessment.model_validate(_json_from_text(result.content))


def complete(data: dict) -> CompletenessResult:
    llm = _get_llm()
    if llm is None:
        return _mock_complete(data)
    prompt = f"Check complaint completeness. Return JSON with complete boolean, score 0-100, missing_fields array, notes array.\nData: {json.dumps(data)}"
    result = llm.invoke(prompt)
    return CompletenessResult.model_validate(_json_from_text(result.content))


def root_cause(data: dict) -> RootCauseResult:
    llm = _get_llm()
    if llm is None:
        return _mock_root(data)
    prompt = f"Suggest likely root causes, CAPA recommendations, and investigation questions for this pharma complaint. Return JSON with likely_causes, capa_recommendations, investigation_questions arrays.\nData: {json.dumps(data)}"
    result = llm.invoke(prompt)
    return RootCauseResult.model_validate(_json_from_text(result.content))


def duplicate_check(candidate: dict, existing: list[dict]) -> SimilarityResult:
    def tokens(value: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]{3,}", str(value).lower()))
    best_id, best_score, best_reason = None, 0, "No close match found."
    base = tokens(" ".join([candidate.get("complaint_details", ""), candidate.get("product_name", ""), candidate.get("batch_number", "")]))
    for item in existing:
        other = tokens(" ".join([item.get("complaint_details", ""), item.get("product_name", ""), item.get("batch_number", "")]))
        if not base or not other:
            continue
        score = len(base & other) / max(1, len(base | other))
        if candidate.get("batch_number") and candidate.get("batch_number") == item.get("batch_number"):
            score = max(score, 0.9)
        if score > best_score:
            best_score = score
            best_id = item.get("id")
            best_reason = "High lexical overlap and/or the same batch/lot suggests the complaint may be related."
    confidence = min(99, round(best_score * 100))
    return SimilarityResult(duplicate=best_score >= 0.72, confidence=confidence, matched_complaint_id=best_id, explanation=best_reason)


def _extract_node(state: ComplaintState):
    e = extract(state["text"])
    return {"extracted": e.model_dump()}


def _risk_node(state: ComplaintState):
    return {"risk": risk(state["extracted"]).model_dump()}


def _complete_node(state: ComplaintState):
    return {"completeness": complete(state["extracted"]).model_dump()}


def build_graph():
    graph = StateGraph(ComplaintState)
    graph.add_node("extract", _extract_node)
    graph.add_node("risk", _risk_node)
    graph.add_node("complete", _complete_node)
    graph.set_entry_point("extract")
    graph.add_edge("extract", "risk")
    graph.add_edge("risk", "complete")
    graph.add_edge("complete", END)
    return graph.compile()


def run_pipeline(text: str) -> dict:
    return build_graph().invoke({"text": text})
