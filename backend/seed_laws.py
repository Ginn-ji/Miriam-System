import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

#laws 
laws_to_add =[
]

async def run_seeder():
    print(f"Starting seeder... found {len(laws_to_add)} laws to process.")
    
    added_count = 0
    for law in laws_to_add:
        # Check if the law already exists so we don't create duplicates
        existing_law = await db.legal_knowledge.find_one({"article": law["article"]})
        
        if existing_law:
            print(f"Skipped: {law['article']} (Already in database)")
            continue
            
        # Add required backend fields
        law["id"] = str(uuid.uuid4())
        law["created_at"] = datetime.now(timezone.utc).isoformat()
        
        # Insert into MongoDB
        await db.legal_knowledge.insert_one(law)
        print(f"Added: {law['article']} - {law['title']}")
        added_count += 1
        
    print(f"\nSeeding complete! Successfully added {added_count} new laws.")

if __name__ == "__main__":
    asyncio.run(run_seeder())
