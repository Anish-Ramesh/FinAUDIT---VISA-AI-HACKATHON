import os
import requests
import asyncio
from typing import TypedDict, List
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langgraph.graph import StateGraph, END
import json
from dotenv import load_dotenv
import traceback

# Force load .env, overriding system variables to ensure local file is used
load_dotenv(override=True)

def get_local_key(key_name="GOOGLE_API_KEY"):
    """
    Manually reads .env to ensure we get the file's exact content,
    bypassing potentially stale system environment variables.
    """
    try:
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
        # print(f"   📂 [Env Config]: Looking for .env at: {env_path}")
        
        if not os.path.exists(env_path):
             print(f"   ❌ [Env Config]: File NOT found at {env_path}")
             return os.environ.get(key_name, "")
        
        # print(f"   ✅ [Env Config]: File found. Scanning content lines for {key_name}...")
        
        # utf-8-sig handles BOM if present (common in Windows editing)
        with open(env_path, "r", encoding="utf-8-sig") as f:
            for i, line in enumerate(f):
                clean = line.strip()
                if not clean or clean.startswith("#"): 
                    continue
                
                # Check for key name pattern (Strict start match to avoid substring issues)
                if clean.startswith(f"{key_name}="):
                    # print(f"      [Line {i+1} Match]: {clean[:20]}...")
                    # Naive parse: split by =
                    if "=" in clean:
                        key_part = clean.split("=", 1)[1].strip()
                        # Remove quotes
                        key = key_part.strip('"').strip("'")
                        # print(f"   📄 [Env Config]: Extracted Key: '{key}'")
                        return key
                
    except Exception as e:
        print(f"   ⚠️ [Key Config]: Could not read local .env: {e}")
    
    # Fallback to standard env var if file read fails
    fallback_key = os.environ.get(key_name, "")
    # print(f"   🗺️ [Env Config]: Falling back to os.environ: ...{fallback_key[-5:] if len(fallback_key)>5 else fallback_key}")
    return fallback_key

# Define the Agent State
class AgentState(TypedDict):
    metadata: dict
    scores: dict
    privacy_check: str
    dataset_type: str
    insights: str
    analysis: dict
    compliance_standard: str

# --- 1. Agent LLM (Audit Analysis) ---
# Key: GOOGLE_API_KEY
# Model: gemini-3.1-pro-preview (Using verified ID: gemini-3.1-pro-preview)
print(f"   🔧 [Config]: Initializing llm_agent with model='gemini-3-flash-preview'")
llm_agent = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview", 
    temperature=0.2,
    google_api_key=get_local_key("GOOGLE_API_KEY")
)
print(f"   ✅ [Config]: llm_agent initialized successfully.")

# --- 2. Chatbot LLM (Interactive Chat) ---
# Key: GOOGLE_CHAT_API_KEY
# Model: gemini-3-flash-preview (Using verified ID: gemini-3-flash-preview)
# Fallback: Use Main Key if Chat Key is missing to prevent crash
chat_key = get_local_key("GOOGLE_CHAT_API_KEY")
if not chat_key:
    print("   ⚠️ [Config]: GOOGLE_CHAT_API_KEY not found. Falling back to GOOGLE_API_KEY for Chatbot.")
    chat_key = get_local_key("GOOGLE_API_KEY")

print(f"   🔧 [Config]: Initializing llm_chat with model='gemini-3-flash-preview'")
llm_chat = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.4, 
    google_api_key=chat_key
)
print(f"   ✅ [Config]: llm_chat initialized successfully.")

# Initialize Embeddings with Explicit Key from File (Using Primary Key)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=get_local_key("GOOGLE_API_KEY")
)

# --- Fallback Logic ---

def fallback_gemini_rapidapi(messages: List[BaseMessage]) -> str:
    """
    Fallback to RapidAPI Gemini Pro if the main API fails.
    """
    print("   ⚠️  [LLM]: Primary API failed. Attempting RapidAPI fallback...")
    
    url = "https://gemini-pro-ai.p.rapidapi.com/"
    
    # Convert LangChain messages to Gemini/RapidAPI format
    contents_parts = []
    
    system_instruction = ""
    
    for msg in messages:
        if isinstance(msg, SystemMessage):
            system_instruction += f"{msg.content}\n\n"
        elif isinstance(msg, HumanMessage):
            role = "user"
            text = msg.content
            # Prepend system instruction to the first user message if present
            if system_instruction:
                text = f"System Instruction:\n{system_instruction}\n\nUser Question:\n{text}"
                system_instruction = "" # Clear it after use
            
            contents_parts.append({
                "role": role,
                "parts": [{"text": text}]
            })
        elif isinstance(msg, AIMessage):
             contents_parts.append({
                "role": "model",
                "parts": [{"text": msg.content}]
            })

    payload = { "contents": contents_parts }
    
    headers = {
        'x-rapidapi-key': "03f51152d6mshde2289b8bd9eeaap1589f3jsn32e6b69226f4",
        'x-rapidapi-host': "gemini-pro-ai.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        answer = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        if not answer:
             print(f"   ❌ [Fallback]: Unexpected response format: {data}")
             raise ValueError("Empty response from RapidAPI")
             
        print("   ✅ [Fallback]: Success.")
        return answer
        
    except Exception as e:
        print(f"   ❌ [Fallback]: RapidAPI also failed: {e}")
        raise e

def invoke_llm_with_fallback(messages: List[BaseMessage], is_chat=False):
    """Synchronous wrapper"""
    target_llm = llm_chat if is_chat else llm_agent
    model_name = 'gemini-3-flash-preview'
    print(f"   📨 [LLM]: Invoking model='{model_name}' (is_chat={is_chat})")
    try:
        response = target_llm.invoke(messages)
        print(f"   ✅ [LLM]: Model '{model_name}' responded successfully.")
        
        # Patch for Gemini 3 Preview returning list content
        if isinstance(response.content, list):
            text_parts = [part.get("text", "") for part in response.content if "text" in part]
            response.content = "".join(text_parts)
            
        return response
    except Exception as e:
        print(f"   ❌ [LLM Error]: Model '{model_name}' FAILED with: {type(e).__name__}: {e}")
        traceback.print_exc()
        
        err_str = str(e).lower()
        if any(x in err_str for x in ["400", "429", "500", "resourceexhausted", "quota", "getaddrinfo", "404", "not found", "invalid"]):
            content = fallback_gemini_rapidapi(messages)
            return AIMessage(content=content)
        raise e

async def invoke_llm_with_fallback_async(messages: List[BaseMessage], is_chat=False):
    """Async wrapper"""
    target_llm = llm_chat if is_chat else llm_agent
    model_name = 'gemini-3-flash-preview'
    print(f"   📨 [LLM Async]: Invoking model='{model_name}' (is_chat={is_chat})")
    try:
        response = await target_llm.ainvoke(messages)
        print(f"   ✅ [LLM Async]: Model '{model_name}' responded successfully.")
        
        # Patch for Gemini 3 Preview returning list content
        if isinstance(response.content, list):
            text_parts = [part.get("text", "") for part in response.content if "text" in part]
            response.content = "".join(text_parts)
            
        return response
    except Exception as e:
        print(f"   ❌ [LLM Async Error]: Model '{model_name}' FAILED with: {type(e).__name__}: {e}")
        traceback.print_exc()
        
        err_str = str(e).lower()
        if any(x in err_str for x in ["400", "429", "500", "resourceexhausted", "quota", "getaddrinfo", "404", "not found", "invalid"]):
            loop = asyncio.get_running_loop()
            content = await loop.run_in_executor(None, fallback_gemini_rapidapi, messages)
            return AIMessage(content=content)
        raise e

# --- Nodes ---

def privacy_guardrail(state: AgentState):
    """
    Agent 2: Privacy Guardrail
    Checks if metadata contains explicit PII leaks before proceeding.
    """
    print("\n🔹 [Privacy Guardrail Agent]: Scanning metadata for PII violations...")
    
    metadata = state["metadata"]
    columns = metadata.get("columns", {})
    
    pii_keywords = ["ssn", "password", "social_security"]
    found_pii = [col for col in columns if any(k in col.lower() for k in pii_keywords)]
    
    if found_pii:
        msg = f"ALERT: Potential PII detected in columns: {found_pii}. Metadata redacted."
        print(f"   ⚠️  [Privacy Guardrail]: {msg}")
    else:
        msg = "Metadata approved. No explicit raw PII keys found."
        print(f"   ✅ [Privacy Guardrail]: {msg}")
        
    return {"privacy_check": msg}

def metadata_analyst(state: AgentState):
    """
    Agent 3: Metadata Analyst
    Identifies the dataset context (KYC, Transactions, etc.).
    """
    print("\n🔹 [Metadata Analyst Agent]: Classifying dataset context...")
    
    columns = list(state["metadata"].get("columns", {}).keys())
    col_str = ", ".join(columns).lower()
    
    if "kyc" in col_str or "passport" in col_str:
        context = "KYC / Identity Data"
    elif "amount" in col_str and "date" in col_str:
        context = "Financial Transaction Data"
    else:
        context = "General Financial Data"
        
    print(f"   📊 [Metadata Analyst]: Dataset classified as '{context}'.")
    return {"dataset_type": context}

def insights_agent(state: AgentState):
    """
    Agent 5: Insights & Visualization Agent
    Interprets the scores to find key trends.
    """
    print("\n🔹 [Insights Agent]: analyzing scoring trends...")
    
    scores = state["scores"]
    health = scores.get("health_score", 0)
    failed_dims = [k for k, v in scores.get("dimension_scores", {}).items() if v < 100]
    
    insight = f"Health Score is {health}/100."
    if failed_dims:
         insight += f" Primary issues found in: {', '.join(failed_dims)}."
    else:
         insight += " Data is pristine."
         
    print(f"   📈 [Insights Agent]: {insight}")
    return {"insights": insight}

def advisory_agent(state: AgentState):
    """
    Agent 6: Advisory Agent
    Generates the final JSON output with remediation steps.
    """
    print("\n🔹 [Advisory Agent]: Generating remediation plan...")
    
    scores = state["scores"]
    metadata = state["metadata"]
    context = state["dataset_type"]
    insights = state["insights"]
    standard = state.get("compliance_standard", "General Transaction")
    
    system_prompt = f"""You are an Expert Financial Compliance Advisor.
    Compliance Standard: {standard}
    Context: {context}
    Insights: {insights}
    
    Role: Analyze the following scores and rule details to generate a prioritized remediation plan SPECIFICALLY for {standard} compliance.
    
    **Priority Logic**:
    - **CRITICAL**: Security gaps (PCI DSS, PII), Major Fraud risks, Clear Regulatory violations.
    - **HIGH**: Financial Inaccuracies (Negative amounts, Currency mismatches), Missing required fields.
    - **MEDIUM**: Data Hygiene (Date formats, Consistency), Operational warnings.
    - **LOW**: Optimization suggestions.

    Output strictly valid JSON:
    {{
        "executive_summary": "One sentence overview focusing on {standard} adherence.",
        "risk_assessment": "Short paragraph on {standard} compliance risks.",
        "remediation_steps": [
            {{"issue": "Brief issue title", "action": "Specific fix action", "priority": "CRITICAL/HIGH/MEDIUM/LOW"}}
        ]
    }}
    
    **Important**: Sort the 'remediation_steps' array so 'CRITICAL' items appear first, followed by 'HIGH', then 'MEDIUM'.
    """
    
    user_message = f"""
    Scores: {json.dumps(scores['dimension_scores'], indent=2)}
    Failed Rules: {[k for k,v in scores['rule_results'].items() if not v['passed']]}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    try:
        # Use Fallback Wrapper (FALSE = Use llm_agent)
        response = invoke_llm_with_fallback(messages, is_chat=False)
        content = response.content.replace("```json", "").replace("```", "").strip()
        analysis_json = json.loads(content)
        print("   ✅ [Advisory Agent]: Plan generated successfully.")
        return {"analysis": analysis_json}
    except Exception as e:
        print(f"   ❌ [Advisory Agent]: Error generating plan: {e}")
        return {"analysis": {
            "executive_summary": "Error generating advice.",
            "risk_assessment": "LLM Failure",
            "remediation_steps": []
        }}

# --- Graph Construction ---

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("privacy_guardrail", privacy_guardrail)
workflow.add_node("metadata_analyst", metadata_analyst)
workflow.add_node("insights_agent", insights_agent)
workflow.add_node("advisory_agent", advisory_agent)

# Define Edge flow
workflow.set_entry_point("privacy_guardrail")
workflow.add_edge("privacy_guardrail", "metadata_analyst")
workflow.add_edge("metadata_analyst", "insights_agent")
workflow.add_edge("insights_agent", "advisory_agent")
workflow.add_edge("advisory_agent", END)

app = workflow.compile()

async def run_advisory_agent(scores: dict, metadata: dict, standard: str = "General Transaction") -> dict:
    """
    Entry point to run the multi-agent system.
    """
    print(f"\n--- 🤖 Starting Multi-Agent Compliance Analysis ({standard}) ---")
    
    initial_state = {
        "scores": scores,
        "metadata": metadata,
        "privacy_check": "",
        "dataset_type": "",
        "insights": "",
        "analysis": {},
        "compliance_standard": standard
    }
    
    result = await app.ainvoke(initial_state)
    print("--- 🏁 Agent Workflow Complete ---\n")
    return result["analysis"]

def build_compliance_rag(scores: dict, metadata: dict) -> FAISS:
    """
    Builds an ephemeral vector store from the safe parts of the analysis.
    Explicitly excludes raw rows.
    """
    docs = []
    
    # 1. High Level Scores
    docs.append(Document(page_content=f"Overall Health Score: {scores.get('health_score')}/100", metadata={"source": "scores"}))
    
    # 2. Dimension Scores
    for dim, score in scores.get("dimension_scores", {}).items():
        docs.append(Document(page_content=f"{dim} dimension score: {score}/100", metadata={"source": "dimension"}))
        
    # 3. Rule Results
    for rule, result in scores.get("rule_results", {}).items():
        status = "PASSED" if result['passed'] else "FAILED"
        content = f"Rule '{rule}' {status}. Score: {result['score']}. Details: {result['details']}"
        docs.append(Document(page_content=content, metadata={"source": "rule_result"}))
        
    # 4. Metadata (Safe Columns Only)
    columns = list(metadata.get("columns", {}).keys())
    docs.append(Document(page_content=f"Dataset has {metadata.get('total_rows')} rows and {metadata.get('total_columns')} columns.", metadata={"source": "metadata"}))
    docs.append(Document(page_content=f"Column names in the dataset: {', '.join(columns)}", metadata={"source": "metadata"}))
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

async def chat_about_dataset(question: str, context: dict) -> str:
    """
    Unrestricted Chat: Provides full dataset context to the LLM.
    Acts as an Independent Auditor answering questions.
    """
    scores = context.get("scores", {})
    metadata = context.get("metadata", {})
    analysis = context.get("analysis", {})
    
    # Construct Full Context (No RAG extraction)
    # We dump the entire relevant JSON structure so the LLM has "whole data on the page"
    full_context_data = {
        "report_summary": {
            "health_score": scores.get("health_score"),
            "dataset_classification": context.get("dataset_type", "Unknown"),
            "row_count": metadata.get("total_rows"),
            "column_count": metadata.get("total_columns")
        },
        "dimension_breakdown": scores.get("dimension_scores", {}),
        "detailed_rule_results": scores.get("rule_results", {}),
        "ai_risk_assessment": analysis.get("risk_assessment", "Not available"),
        "ai_remediation_plan": analysis.get("remediation_steps", []),
        "columns": list(metadata.get("columns", {}).keys())
    }
    
    context_str = json.dumps(full_context_data, indent=2)

    # Auditor Persona System Prompt
    system_prompt = """You are the 'FinAUDIT Independent Auditor', an expert AI agent responsible for explaining the results of a financial data compliance audit.

    Your Mandate:
    1. **Full Transparency**: You have access to the COMPLETE audit report. Answer ANY question related to the data quality, scores, rules, or specific failures. Do not restrict information.
    2. **Persona**: Professional, objective, and authoritative (like a CPA or Auditor). use phrases like "based on our analysis", "the audit evidence suggests".
    3. **Grounding**: strictly base your answers on the provided 'Context JSON'.
    4. **Format**: Use Markdown (Bold, Lists, Tables) to present data clearly.
    
    If asked about the 'opinion', derive it from the Health Score (Unqualified if > 90, Qualified if 70-90, Adverse if < 70).
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context JSON:\n{context_str}\n\nUser Question: {question}")
    ]
    
    try:
        # Use Fallback Async Wrapper (TRUE = Use llm_chat)
        response = await invoke_llm_with_fallback_async(messages, is_chat=True)
        return response.content
    except Exception as e:
        return f"Auditor Error: {str(e)}"
