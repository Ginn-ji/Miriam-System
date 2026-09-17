import asyncio
import os
import re
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def augment_database():
    # 1. Load environment variables
    load_dotenv()
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME')
    
    if not mongo_url or not db_name:
        print("Error: MONGO_URL or DB_NAME not found in .env file.")
        return

    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    collection = db.legal_knowledge

    # 2. Load the Gold Standard Excel file
    # (Header is set to row 3 based on the file structure)
    print("Loading Excel file...")
    try:
        df = pd.read_excel('LACBot_Gold_Standard_Test_Cases-2.xlsx', sheet_name='Gold_Standard_Test_Cases', header=3)
        df = df.fillna("") # Clean missing values
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # 3. Fetch all existing laws to map Article numbers to Database IDs
    print("Fetching current laws from database...")
    laws = await collection.find({}, {"_id": 1, "id": 1, "article": 1}).to_list(None)
    
    article_map = {}
    for law in laws:
        art_str = law.get('article', '')
        if art_str:
            # Extract just the digits (e.g., "Art. 1" -> "1") for safe matching
            digits = re.search(r'\d+', art_str)
            if digits:
                article_map[digits.group()] = law.get('id')

    print(f"Found {len(article_map)} uniquely numbered articles in the database.")

    updated_count = 0

    # 4. Iterate through the Excel rows and push queries to MongoDB
    for index, row in df.iterrows():
        gold_article = str(row.get('Gold Article', ''))
        
        digits_match = re.search(r'\d+', gold_article)
        if not digits_match:
            continue
            
        art_num = digits_match.group()
        
        if art_num in article_map:
            law_id = article_map[art_num]
            
            # Extract the 3 query variations
            queries = [
                str(row.get('Query (English)', '')).strip(),
                str(row.get('Query (Tagalog)', '')).strip(),
                str(row.get('Query (Taglish)', '')).strip()
            ]
            
            # Remove empty strings
            valid_queries = [q for q in queries if q]
            
            if valid_queries:
                # Use $addToSet with $each to safely append without creating duplicates
                await collection.update_one(
                    {"id": law_id},
                    {"$addToSet": {"tags": {"$each": valid_queries}}}
                )
                updated_count += 1
                print(f"Augmented Article {art_num} with {len(valid_queries)} conversational queries.")
        else:
            print(f"Warning: Article {art_num} found in Excel but not currently in Database. Skipping.")

    print(f"\nSuccess! Augmented {updated_count} test cases into the database.")
    client.close()

if __name__ == "__main__":
    asyncio.run(augment_database())