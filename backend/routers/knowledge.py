from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from typing import Optional
import uuid
from datetime import datetime, timezone
from database import db
from schemas import LegalKnowledge, BulkDeleteRequest
from core.engine import train_search_models
from core.nlp_utils import extract_text_from_pdf

router = APIRouter(prefix="/api/legal-knowledge", tags=["Knowledge"])

@router.get("")
async def get_laws(
    q: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    match_query = {}

    if category and category.lower() != 'all':
        match_query['category'] = category

    if q and q.strip():
        match_query["$or"] = [
            {"title":   {"$regex": q.strip(), "$options": "i"}},
            {"article": {"$regex": q.strip(), "$options": "i"}},
        ]

    # Total count for pagination
    total = await db.legal_knowledge.count_documents(match_query)

    # Aggregation pipeline with NUMERIC sort on the article number
    # e.g. "Art. 2" sorts before "Art. 10" (string sort would fail here)
    pipeline = [
        {"$match": match_query},
        {
            # Extract the first integer found in the 'article' field for sorting
            "$addFields": {
                "_sort_num": {
                    "$let": {
                        "vars": {
                            "m": {
                                "$regexFind": {
                                    "input": {"$ifNull": ["$article", ""]},
                                    "regex": "\\d+"
                                }
                            }
                        },
                        "in": {
                            "$cond": {
                                "if":   {"$gt": ["$$m", None]},
                                "then": {"$toInt": "$$m.match"},
                                "else": 999999      # articles with no number go last
                            }
                        }
                    }
                }
            }
        },
        {"$sort":    {"_sort_num": 1}},   # ← true numeric ascending order
        {"$skip":    skip},
        {"$limit":   limit},
        {"$project": {"_id": 0, "_sort_num": 0}}   # strip the temp field
    ]

    laws = await db.legal_knowledge.aggregate(pipeline).to_list(limit)

    for l in laws:
        l['title']   = f"{l.get('article')} - {l.get('title')}" if l.get('article') else l.get('title', 'Untitled')
        l['content'] = "\n\n".join(l.get('chunks', [])) if l.get('chunks') else l.get('simplified_text', 'No content')

    return {"laws": laws, "total": total}

@router.post("")
async def add_law(law: LegalKnowledge, bg: BackgroundTasks):
    ld = law.model_dump()
    ld['created_at'] = datetime.now(timezone.utc).isoformat()
    ld.pop('_id', None)
    await db.legal_knowledge.insert_one(ld)
    bg.add_task(train_search_models)
    return {"message": "Added", "id": ld['id']}

@router.post("/upload")
async def upload_law(bg: BackgroundTasks, file: UploadFile = File(...), title: str = Form(...), category: str = Form(...), tags: str = Form(...), language: str = Form(...)):
    content = await file.read()
    txt = await extract_text_from_pdf(content) if file.filename.endswith('.pdf') else content.decode('utf-8')
    law = {
        "id": str(uuid.uuid4()), "title": title, "category": category,
        "content": txt, "simplified_text": "Extracted",
        "tags": [t.strip() for t in tags.split(',')],
        "language": language,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.legal_knowledge.insert_one(law)
    bg.add_task(train_search_models)
    return {"message": "Uploaded"}

@router.post("/bulk-delete")
async def bulk_delete(req: BulkDeleteRequest, bg: BackgroundTasks):
    res = await db.legal_knowledge.delete_many({"id": {"$in": req.ids}})
    bg.add_task(train_search_models)
    return {"message": f"Deleted {res.deleted_count}"}

@router.delete("/delete-all")
async def delete_all_laws(bg: BackgroundTasks):
    await db.legal_knowledge.delete_many({})
    bg.add_task(train_search_models)
    return {"message": "All laws deleted"}

@router.put("/{law_id}")
async def update_law(law_id: str, law: LegalKnowledge, bg: BackgroundTasks):
    ld = law.model_dump()
    ld.pop('_id', None)
    result = await db.legal_knowledge.update_one({"id": law_id}, {"$set": ld})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Law not found")
    bg.add_task(train_search_models)
    return {"message": "Updated"}

@router.delete("/{law_id}")
async def delete_law(law_id: str, bg: BackgroundTasks):
    if (await db.legal_knowledge.delete_one({"id": law_id})).deleted_count == 0:
        raise HTTPException(404, "Not found")
    bg.add_task(train_search_models)
    return {"message": "Deleted"}