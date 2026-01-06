from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from services.ingestion import load_data, profile_dataset
from core.rules_engine import RulesEngine
from services.scoring import calculate_scores
from ai.agent import run_advisory_agent

router = APIRouter()

from services.provenance import provenance_service

@router.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    # 1. Ingestion & Profiling (Metadata Extraction)
    try:
        df = await load_data(file)
        metadata = profile_dataset(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Rule Execution (Deterministic)
    engine = RulesEngine(metadata)
    rule_results = engine.run_compliance() # Default: General Transaction

    # 3. Scoring
    scores = calculate_scores(rule_results)

    # 4. Agent Analysis
    try:
        if os.environ.get("GOOGLE_API_KEY"):
            analysis = await run_advisory_agent(scores, metadata)
        else:
            analysis = {
                "executive_summary": "AI analysis skipped (GOOGLE_API_KEY not set).",
                "risk_assessment": "Configure the API key to enable GenAI insights.",
                "remediation_steps": []
            }
    except Exception as e:
         # Fallback to prevent API failure
         analysis = {
            "executive_summary": "AI analysis failed temporarily.",
            "risk_assessment": str(e),
            "remediation_steps": []
        }

    # 5. Provenance Attestation
    attestation_data = {
        "filename": file.filename,
        "health_score": scores["health_score"],
        "overall_score": scores["overall_score"],
        "metadata_hash": provenance_service.compute_fingerprint(metadata),
        "analysis_summary_hash": provenance_service.compute_fingerprint(analysis) if analysis else None
    }
    provenance = provenance_service.sign_record(attestation_data)

    return {
        "filename": file.filename,
        "metadata": metadata, # Frontend might need this for visualization
        "scores": scores,
        "analysis": analysis,
        "provenance": provenance
    }

from pydantic import BaseModel
from ai.agent import chat_about_dataset

class ReEvaluateRequest(BaseModel):
    metadata: dict
    standard: str = "General Transaction"

@router.post("/analyze/re-evaluate")
async def re_evaluate_compliance(request: ReEvaluateRequest):
    print(f"\n🔹 [API]: Re-evaluating for standard: {request.standard}")
    try:
        # Re-run rule engine with new standard
        engine = RulesEngine(request.metadata)
        rule_results = engine.run_compliance(request.standard)
        
        scores = calculate_scores(rule_results)
        
        # Re-run AI Agent
        if os.environ.get("GOOGLE_API_KEY"):
            from ai.agent import get_local_key # Ensure key check
            if get_local_key():
                 analysis = await run_advisory_agent(scores, request.metadata, request.standard)
            else:
                 analysis = {"executive_summary": "Skipped (No Key)", "remediation_steps": []}
        else:
            analysis = {"executive_summary": "Skipped (No Key)", "remediation_steps": []}
            
        return {
            "scores": scores,
            "analysis": analysis
        }
    except Exception as e:
        print(f"   ❌ [API Error]: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    question: str
    context: dict

from fastapi import Request

@router.post("/chat")
async def chat(raw_request: Request):
# ... (rest of chat endpoint)
    print("\n🔹 [API DEBUG]: /api/chat hit")
    try:
        body = await raw_request.json()
        print(f"   📨 [API RAW BODY]: {body}")
        
        # Manual Validation for Debugging
        try:
            request = ChatRequest(**body)
            print("   ✅ [API Model]: Validation Successful")
        except Exception as vals_err:
            print(f"   ❌ [API Model]: Validation FAILED: {vals_err}")
            raise vals_err

        if not os.environ.get("GOOGLE_API_KEY"):
             # Double check local read
             from ai.agent import get_local_key
             if not get_local_key():
                print("   ❌ [API Config]: No API KEY found.")
                return {"response": "I need a Google API Key to chat! Please configure backend/.env."}
             
        print("   🤖 [API Agent]: Calling chat_about_dataset...")
        response = await chat_about_dataset(request.question, request.context)
        print(f"   ✅ [API Agent]: Response generated (Length: {len(response)})")
        return {"response": response}
    except Exception as e:
        print(f"   ❌ [API Error]: {str(e)}")
        # traceback.print_exc() # verify if traceback is imported or add it
        raise HTTPException(status_code=500, detail=str(e))
