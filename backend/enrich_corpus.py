import asyncio
import os
import re
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('backend/.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

# Domain-specific intent descriptors mapping for Philippine Labor Code
INTENT_MAPPINGS = {
    # Coverage & Exclusions
    "Art. 82": [
        "government employees", "kawani ng gobyerno", "empleyado ng gobyerno", 
        "sahod ng gobyerno", "sahod para sa mga government employees", 
        "civil service", "public sector", "hindi sakop", "exclusions", 
        "managerial employees", "field personnel", "domestic helpers", "kasambahay"
    ],
    "Art. 276": [
        "government employees", "kawani ng gobyerno", "empleyado ng gobyerno", 
        "civil service law", "civil service commission", "public sector workers", 
        "terms and conditions of government employees"
    ],
    
    # Hours of work & Overtime
    "Art. 83": ["normal hours of work", "eight hours", "walong oras", "oras ng trabaho"],
    "Art. 85": ["meal periods", "meal break", "kain", "tanghalian", "pahinga sa trabaho", "oras ng pagkain"],
    "Art. 86": [
        "night shift differential", "night differential", "pang gabi", "panggabi", 
        "gabi nagtatrabaho", "night work", "night worker"
    ],
    "Art. 87": [
        "overtime", "overtime pay", "sobrang oras", "lampas walong oras", 
        "nagovertime", "overtime work", "bayad sa overtime"
    ],
    "Art. 91": [
        "weekly rest day", "rest day", "day off", "dayoff", "pahinga", 
        "lingguhang pahinga", "pinapasok sa rest day"
    ],
    "Art. 94": [
        "holiday pay", "regular holiday", "special holiday", "pista opisyal", 
        "bayad sa holiday", "pinapasok ng holiday"
    ],
    "Art. 95": [
        "service incentive leave", "sil", "leave", "vacation leave", 
        "sick leave", "limang araw na leave", "paid leave", "leave credits"
    ],

    # Wages & Deductions
    "Art. 99": [
        "regional minimum wages", "minimum wage", "mababang sahod", 
        "kulang ang sahod", "hindi umabot sa minimum wage", "sahod"
    ],
    "Art. 103": [
        "time of payment", "kailan dapat magpasahod", "release ng sweldo", 
        "mag-release ng sweldo", "delayed sahod", "late sweldo", "bimonthly payment"
    ],
    "Art. 106": [
        "contractor or subcontractor", "agency worker", "subcontracting", 
        "labor only contracting", "manpower agency", "kontraktwal"
    ],
    "Art. 113": [
        "wage deductions", "deduction", "kaltas", "kinaltasan", 
        "binawas sa sahod", "unauthorized deductions", "bawas sweldo"
    ],
    "Art. 116": [
        "withholding of wages", "withholding", "ipit sahod", "ipitin ang sahod", 
        "hindi ibigay ang sahod", "hindi ibigay ang sweldo", "pinigil na sweldo"
    ],

    # Women & Special Groups
    "Art. 131": ["facilities for women", "babae sa trabaho", "buntis", "women workers"],
    "Art. 133": ["maternity leave benefits", "maternity leave", "buntis", "panganganak"],
    "Art. 135": ["discrimination prohibited", "diskriminasyon sa babae", "pantay na sahod"],
    "Art. 137": [
        "prohibited acts", "discrimination prohibited", "tanggalin dahil buntis", 
        "pinaalis dahil buntis", "buntis", "maternity"
    ],
    "Art. 139": [
        "minimum employable age", "child labor", "menor de edad", 
        "bata nagtatrabaho", "edad para magtrabaho"
    ],
    "Art. 141": [
        "coverage", "domestic helpers", "kasambahay", "katulong sa bahay", 
        "contract of domestic service"
    ],
    "Art. 143": [
        "minimum cash wage", "minimum wage ng kasambahay", "sahod ng katulong", 
        "sweldo ng kasambahay", "househelpers"
    ],
    "Art. 148": ["opportunity for education", "kasambahay makapag aral", "pag-aaral ng kasambahay"],

    # Health & Disability
    "Art. 162": [
        "safety and health standards", "safe workplace", "kaligtasan sa trabaho", 
        "protective equipment", "delikadong lugar ng trabaho"
    ],
    "Art. 168": [
        "compulsory coverage", "employees compensation commission", "ecc", 
        "aksidente sa trabaho", "nasaktan sa trabaho"
    ],
    "Art. 197": [
        "temporary total disability", "pansamantalang disability", 
        "injury sa trabaho", "medical benefits"
    ],
    "Art. 198": [
        "permanent total disability", "habang buhay na disability", 
        "lumpo dahil sa trabaho", "disability compensation"
    ],

    # Jurisdiction & Complaints
    "Art. 128": [
        "visitorial and enforcement power", "dole inspection", "mag-inspect ang dole", 
        "inspeksyon ng dole", "inspection", "dole"
    ],
    "Art. 224": [
        "jurisdiction of the labor arbiters and the commission", "magsampa ng reklamo", 
        "reklamo sa employer", "kaso sa boss", "nlrc", "labor arbiter", 
        "money claims", "illegal dismissal case"
    ],

    # Termination & Tenure
    "Art. 294": [
        "security of tenure", "tinanggal nang walang dahilan", "walang dahilan", 
        "illegal dismissal", "karapatan sa trabaho", "hindi pwedeng basta tanggalin"
    ],
    "Art. 296": ["probationary employment", "regularization", "probationary period", "anim na buwan"],
    "Art. 297": [
        "termination by employer", "just causes", "sinibak", "tinanggal", 
        "pinaalis", "serious misconduct", "willful disobedience", "gross neglect"
    ],
    "Art. 298": [
        "closure of establishment and reduction of personnel", "authorized causes", 
        "retrenchment", "redundancy", "nagsara ang kompanya", "separation pay"
    ],
    "Art. 299": [
        "disease as ground for termination", "may sakit", "tinanggal dahil may sakit", 
        "pinaalis dahil nagkasakit", "karamdaman", "nagkasakit", "illness", 
        "medical condition", "unfit to work"
    ],
    "Art. 300": ["termination by employee", "resignation", "nagresign", "magresign", "30 days notice"],
    "Art. 302": [
        "retirement", "retirement pay", "magreretiro", "edad ng pagreretiro", 
        "retirement benefits", "benepisyo sa pagtanda"
    ]
}

async def enrich_database():
    print("Starting Knowledge Base Document Expansion in MongoDB...")
    updated = 0
    all_laws = await db.legal_knowledge.find().to_list(None)
    for law in all_laws:
        art_str = law.get('article', '') or ''
        match = re.search(r'\d+', art_str)
        if not match:
            continue
        art_num = match.group()
        canonical_key = f"Art. {art_num}"
        
        keywords = INTENT_MAPPINGS.get(canonical_key, [])
        if keywords:
            res = await db.legal_knowledge.update_one(
                {"_id": law["_id"]},
                {"$set": {"intent_keywords": keywords}}
            )
            if res.modified_count > 0:
                updated += 1
                
    print(f"Document Expansion complete! Updated {updated} statutory articles with intent_keywords.")

if __name__ == "__main__":
    asyncio.run(enrich_database())