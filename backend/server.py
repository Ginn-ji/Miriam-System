from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
import uuid
import bcrypt
from datetime import datetime, timezone

# Import from your new modular files
from database import client, db
from core.engine import train_search_models
from routers import auth, chat, knowledge, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LACBot Legal Awareness Chat Bot")

# Register the separated routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(knowledge.router)
app.include_router(admin.router)

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
    "https://lacbot.vercel.app", 
    "https://miriam-system.vercel.app"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    # Ensure superadmin exists with a hashed password
    if not await db.users.find_one({"role": "super_admin"}):
        hashed_admin_pw = bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = await db.users.find_one({"username": "admin"})
        
        if admin_user:
            await db.users.update_one(
                {"_id": admin_user["_id"]}, 
                {"$set": {"role": "super_admin", "password": hashed_admin_pw}}
            )
        else:
            await db.users.insert_one({
                "id": str(uuid.uuid4()), 
                "username": "superadmin", 
                "email": "admin@lacbot.system", 
                "password": hashed_admin_pw, 
                "role": "super_admin", 
                "created_at": datetime.now(timezone.utc).isoformat()
            })
    
    # Initialize the AI search models in memory
    await train_search_models()
    logger.info("LACBot API Started successfully!")

@app.on_event("shutdown")
async def shutdown_db_client(): 
    client.close()

@app.get("/api/")
async def root():
    return {"message": "LACBot Legal Awareness Chat Bot"}