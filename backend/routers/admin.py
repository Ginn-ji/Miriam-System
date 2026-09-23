from fastapi import APIRouter, HTTPException
from database import db
from schemas import ChatLimitRequest, SavedTestCase
from metrics import ManualEvaluationRequest, calculate_ir_metrics
from core.engine import search_engine

router = APIRouter(prefix="/api", tags=["Admin"])

@router.get("/settings/chat-limit")
async def get_limit():
    setting = await db.settings.find_one({"key": "chat_limit"}, {"_id": 0})
    return {"limit": setting["value"] if setting else 5}

@router.post("/settings/chat-limit")
async def set_limit(req: ChatLimitRequest):
    if not 1 <= req.new_limit <= 10: 
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 10")
        
    await db.settings.update_one(
        {"key": "chat_limit"}, 
        {"$set": {"value": req.new_limit}}, 
        upsert=True
    )
    return {"message": "Chat limit updated successfully", "limit": req.new_limit}

@router.get("/stats")
async def get_stats():
    sessions = len(await db.chat_history.distinct("session_id"))
    laws = await db.legal_knowledge.count_documents({})
    return {"chat_sessions": sessions, "legal_articles": laws}

@router.get("/admin/metrics/test-cases")
async def get_test_cases():
    cases = await db.test_cases.find({}, {"_id": 0}).to_list(1000)
    return {"test_cases": cases}

@router.post("/admin/metrics/test-cases")
async def add_test_case(test_case: SavedTestCase):
    case_dict = test_case.model_dump()
    existing = await db.test_cases.find_one({"test_id": case_dict["test_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Test ID already exists.")
        
    await db.test_cases.insert_one(case_dict)
    return {"message": "Test case saved to cloud database."}

@router.delete("/admin/metrics/test-cases/{test_id}")
async def delete_test_case(test_id: str):
    result = await db.test_cases.delete_one({"test_id": test_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test case not found.")
    return {"message": "Test case deleted."}

@router.post("/admin/metrics/evaluate")
async def evaluate_search_metrics(payload: ManualEvaluationRequest, requester_id: str):
    requester = await db.users.find_one({"id": requester_id})
    if not requester or requester.get("role") not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Access Denied: Only Admins can run metric evaluations.")
        
    if not payload.test_cases:
        raise HTTPException(status_code=400, detail="No test cases provided.")
        
    if search_engine.vectorizer is None or search_engine.bm25 is None:
        raise HTTPException(status_code=400, detail="Search models are not trained yet. Add legal knowledge first.")
        
    try:
        limit_setting = await db.settings.find_one({"key": "chat_limit"})
        chat_limit = int(limit_setting.get("value", 3)) if limit_setting else 3
    except:
        chat_limit = 3
        
    return calculate_ir_metrics(search_engine, payload.test_cases, k=chat_limit)