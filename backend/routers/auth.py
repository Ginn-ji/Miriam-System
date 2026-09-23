from fastapi import APIRouter, HTTPException
import bcrypt
import random
from datetime import datetime, timezone, timedelta
import logging
from fastapi import HTTPException

from database import db
from schemas import User, LoginRequest, RoleUpdateRequest, ForgotPasswordRequest, VerifyCodeRequest, ResetPasswordRequest, VerifyRegistrationRequest
# Import the updated email utility
from core.nlp_utils import is_valid_password, is_valid_email
from core.email_utils import send_otp_email

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Auth"])

@router.post("/login")
async def login(request: LoginRequest):
    query = {"email": request.identifier} if request.login_type == "email" else {"username": request.identifier}
    user = await db.users.find_one(query, {"_id": 0})
    if not user: raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_password = user.get("password", "")
    # Opportunistic hashing for old plaintext passwords
    if not stored_password.startswith("$2b$"):
        if stored_password == request.password:
            hashed_pw = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            await db.users.update_one({"id": user["id"]}, {"$set": {"password": hashed_pw}})
            user["password"] = hashed_pw 
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        try:
            if not bcrypt.checkpw(request.password.encode('utf-8'), stored_password.encode('utf-8')): 
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except ValueError:
            raise HTTPException(status_code=401, detail="Corrupted password hash")
    return user

@router.post("/users/register")
async def request_registration(user: User):
    """Step 1: Validates details, generates OTP, and stores pending data."""
    if not is_valid_email(user.email): 
        raise HTTPException(status_code=400, detail="Invalid email format.")
    if not is_valid_password(user.password): 
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters and include a number or special character.")
    
    if await db.users.find_one({"username": user.username}): 
        raise HTTPException(status_code=400, detail="Username already taken")
    if await db.users.find_one({"email": user.email}): 
        raise HTTPException(status_code=400, detail="Email already registered")

    code = str(random.randint(100000, 999999))
    
    new_user_data = user.model_dump()
    new_user_data["password"] = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Store temporarily in pending_users collection
    await db.pending_users.update_one(
        {"email": user.email},
        {"$set": {
            "user_data": new_user_data,
            "code": code,
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()
        }},
        upsert=True
    )
    
    send_otp_email(user.email, code, purpose="Registration")
    return {"message": "Verification code sent to email."}

@router.post("/users/register/verify")
async def verify_registration(request: VerifyRegistrationRequest):
    """Step 2: Verifies OTP and officially creates the account."""
    pending = await db.pending_users.find_one({"email": request.email})
    
    if not pending:
        raise HTTPException(status_code=400, detail="No pending registration found for this email.")
    if pending["code"] != request.code:
        raise HTTPException(status_code=400, detail="Invalid verification code.")
    if datetime.fromisoformat(pending["expires_at"]) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Verification code has expired. Please register again.")
        
    user_data = pending["user_data"]
    
    # Final safety check before inserting
    if await db.users.find_one({"username": user_data["username"]}): 
        raise HTTPException(status_code=400, detail="Username was taken while verifying.")
    if await db.users.find_one({"email": user_data["email"]}): 
        raise HTTPException(status_code=400, detail="Email was registered while verifying.")
        
    await db.users.insert_one(user_data)
    await db.pending_users.delete_one({"email": request.email})
    
    return {
        "message": "User registered successfully", 
        "id": user_data["id"], 
        "username": user_data["username"], 
        "role": user_data["role"]
    }

@router.post("/users/forgot-password")
async def request_password_reset(request: ForgotPasswordRequest):
    # 1. Check if email is valid
    if not is_valid_email(request.email): 
        raise HTTPException(status_code=400, detail="Invalid email format.")
        
    # 2. Look for the user in the database
    user = await db.users.find_one({"email": request.email})
    
    # 3. 🛑 THE FIX: If the user doesn't exist, CRASH the request deliberately.
    # This throws an error to React, stopping the screen from changing.
    if not user:
        raise HTTPException(status_code=404, detail="This email is not registered in our database.")

    # 4. Only generate the code if the user exists
    code = str(random.randint(100000, 999999))
    
    await db.password_resets.update_one(
        {"user_id": user["id"]}, 
        {"$set": {
            "code": code, 
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()
        }}, 
        upsert=True
    )
    
    send_otp_email(user["email"], code, purpose="Password Reset")
    
    # 5. Return success ONLY for real users
    return {"message": "A recovery code has been sent to your email."}
    
@router.post("/users/verify-reset-code")
async def verify_reset_code(request: VerifyCodeRequest):
    user = await db.users.find_one({"email": request.email})
    if not user: raise HTTPException(status_code=400, detail="Invalid request.")
    reset_record = await db.password_resets.find_one({"user_id": user["id"], "code": request.code})
    if not reset_record or datetime.fromisoformat(reset_record["expires_at"]) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")
    return {"message": "Code verified."}

@router.post("/users/reset-password")
async def reset_password(request: ResetPasswordRequest):
    if not is_valid_password(request.new_password): raise HTTPException(status_code=400, detail="Invalid Password format.")
    user = await db.users.find_one({"email": request.email})
    if not user: raise HTTPException(status_code=400, detail="Invalid request.")
    reset_record = await db.password_resets.find_one({"user_id": user["id"], "code": request.code})
    if not reset_record or datetime.fromisoformat(reset_record["expires_at"]) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

    hashed_pw = bcrypt.hashpw(request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    await db.users.update_one({"id": user["id"]}, {"$set": {"password": hashed_pw}})
    await db.password_resets.delete_one({"user_id": user["id"]})
    return {"message": "Password reset."}

@router.get("/users")
async def get_all_users(requester_id: str):
    requester = await db.users.find_one({"id": requester_id})
    # UPDATE: Allow both admin and super_admin to view the list
    if not requester or requester.get("role") not in ["admin", "super_admin"]: 
        raise HTTPException(status_code=403, detail="Access Denied.")
    return {"users": await db.users.find({}, {"_id": 0, "password": 0}).to_list(1000)}

@router.put("/users/{target_id}/role")
async def update_user_role(target_id: str, request: RoleUpdateRequest):
    requester = await db.users.find_one({"id": request.requester_id})
    if not requester or requester.get("role") != "super_admin": raise HTTPException(status_code=403, detail="Access Denied.")
    if request.new_role not in ["user", "admin", "super_admin"]: raise HTTPException(status_code=400, detail="Invalid role.")
    await db.users.update_one({"id": target_id}, {"$set": {"role": request.new_role}})
    return {"message": "Role updated"}