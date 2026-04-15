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
laws_to_add = [
  {
    "article": "Art. 13",
    "title": "Definitions",
    "category": "Labor Law - Book 1",
    "simplified_text": "This article defines the official meanings of words used in labor, such as 'worker', 'employer', and what counts as 'recruitment and placement'.",
    "chunks": [
      "(a) 'Worker' means any member of the labor force, whether employed or unemployed.",
      "(b) 'Recruitment and placement' refers to any act of canvassing, enlisting, contracting, transporting, utilizing, hiring or procuring workers...",
      "(c) 'Private fee-charging employment agency' means any person or entity engaged in recruitment and placement of workers for a fee...",
      "(d) 'License' means a document issued by the Department of Labor authorizing a person or entity to operate a private employment agency.",
      "(e) 'Private recruitment entity' means any person or association engaged in the recruitment and placement of workers, locally or overseas, without charging a fee...",
      "(f) 'Authority' means a document issued by the Department of Labor authorizing a person or association to engage in recruitment and placement activities as a private recruitment entity.",
      "(g) 'Seaman' means any person employed in a vessel engaged in maritime navigation.",
      "(h) 'Overseas employment' means employment of a worker outside the Philippines.",
      "(i) 'Emigrant' means any person, worker or otherwise, who emigrates to a foreign country by virtue of an immigrant visa or resident permit..."
    ],
    "tags": ["definitions", "worker", "recruitment", "overseas employment", "seaman", "employer"],
    "language": "en"
  },
  {
    "article": "Art. 14",
    "title": "Employment promotion",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Secretary of Labor is responsible for creating programs to help people find jobs, organizing employment offices, and guiding workers to the right jobs.",
    "chunks": [
      "The Secretary of Labor shall have the power and authority:",
      "(a) To organize and establish new employment offices in addition to the existing ones as local needs may require;",
      "(b) To organize and establish a nationwide job clearance and information system to inform applicants registering with a particular employment office of job opportunities in other parts of the country as well as job opportunities abroad;",
      "(c) To develop and organize a program that will facilitate occupational, industrial and geographical mobility of labor and provide assistance in the relocation of workers from one area to another; and",
      "(d) To require any person, establishment, organization or institution to submit such employment information as may be prescribed by the Secretary of Labor."
    ],
    "tags": ["employment promotion", "secretary of labor", "job clearance", "DOLE", "job opportunities"],
    "language": "en"
  },
  {
    "article": "Art. 15",
    "title": "Bureau of Employment Services",
    "category": "Labor Law - Book 1",
    "simplified_text": "This creates the Bureau of Employment Services to oversee local job placement, monitor private recruitment agencies, and ensure fair employment practices.",
    "chunks": [
      "(a) The Bureau of Employment Services shall be primarily responsible for developing and monitoring a comprehensive employment program.",
      "(b) The Bureau shall have the following functions:",
      "1. Formulate and develop plans and programs to implement the employment promotion objectives of this Title;",
      "2. Establish and maintain a registration and/or licensing system to regulate private sector participation in the recruitment and placement of workers, locally and overseas...",
      "3. Formulate and develop employment programs designed to benefit disadvantaged groups and communities...",
      "4. Establish and maintain a registration and/or work permit system to regulate the employment of aliens..."
    ],
    "tags": ["bureau of employment services", "job placement", "aliens", "work permit", "recruitment agencies"],
    "language": "en"
  },
  {
    "article": "Art. 16",
    "title": "Private recruitment",
    "category": "Labor Law - Book 1",
    "simplified_text": "Private individuals or companies are generally not allowed to recruit workers unless they follow the strict rules set by the Secretary of Labor.",
    "chunks": [
      "Except as provided in Chapter II of this Title, no person or entity other than the public employment offices, shall engage in the recruitment and placement of workers."
    ],
    "tags": ["private recruitment", "placement of workers", "hiring", "recruitment restriction"],
    "language": "en"
  },
  {
    "article": "Art. 17",
    "title": "Overseas Employment Development Board",
    "category": "Labor Law - Book 1",
    "simplified_text": "This established the board (now absorbed by POEA/DMW) responsible for promoting overseas employment and protecting Filipino workers hired to work in other countries.",
    "chunks": [
      "An Overseas Employment Development Board is hereby created to undertake, in cooperation with relevant entities and agencies, a systematic program for overseas employment of Filipino workers in excess of domestic needs and to protect their rights to fair and equitable employment practices.",
      "It shall have the power and duty:",
      "1. To promote the overseas employment of Filipino workers through a comprehensive market promotion and development program;",
      "2. To secure the best possible terms and conditions of employment of Filipino contract workers...",
      "3. To recruit and place workers for overseas employment on a government-to-government arrangement...",
      "4. To act as secretariat for the Board of Trustees of the Welfare and Training Fund for Overseas Workers."
    ],
    "tags": ["overseas employment", "OEDB", "POEA", "OFW", "contract workers"],
    "language": "en"
  },
  {
    "article": "Art. 18",
    "title": "Ban on direct-hiring",
    "category": "Labor Law - Book 1",
    "simplified_text": "Foreign employers cannot directly hire Filipino workers. They must go through authorized government boards or agencies to protect the worker from scams or abuse.",
    "chunks": [
      "No employer may hire a Filipino worker for overseas employment except through the Boards and entities authorized by the Secretary of Labor.",
      "Direct-hiring by members of the diplomatic corps, international organizations and such other employers as may be allowed by the Secretary of Labor is exempted from this provision."
    ],
    "tags": ["direct hiring ban", "overseas employment", "foreign employer", "OFW protection"],
    "language": "en"
  },
  {
    "article": "Art. 19",
    "title": "Office of Emigrant Affairs",
    "category": "Labor Law - Book 1",
    "simplified_text": "This established an office to help Filipinos who are emigrating (moving permanently) to other countries, ensuring their paperwork, skills, and welfare are taken care of.",
    "chunks": [
      "(a) Pursuant to the national policy to maintain close ties with Filipino migrant communities and promote their welfare as well as establish a data bank in aid of national manpower policy formulation, an Office of Emigrant Affairs is hereby created in the Department of Labor.",
      "(b) The office shall, among others, promote the well-being of emigrants and maintain their close link to the homeland by:",
      "1. serving as a liaison with migrant communities;",
      "2. provision of welfare and cultural services;",
      "3. promote and facilitate re-integration of migrants into the national mainstream;",
      "4. promote economic; political and cultural ties with the communities; and",
      "5. generally to undertake such activities as may be appropriate to enhance such cooperative links."
    ],
    "tags": ["emigrant affairs", "migrant communities", "welfare", "emigration"],
    "language": "en"
  },
  {
    "article": "Art. 43",
    "title": "Statement of objective",
    "category": "Labor Law - Book 2",
    "simplified_text": "The main goal of this section is to develop the skills of the workforce, create training programs, and ensure the country's manpower is used efficiently to boost the economy.",
    "chunks": [
      "It is the objective of this Title to develop human resources, establish training institutions, and formulate such plans and programs as will ensure efficient allocation, development and utilization of the nation’s manpower and thereby promote employment and accelerate economic and social growth."
    ],
    "tags": ["objective", "human resources", "manpower", "training", "economic growth"],
    "language": "en"
  },
  {
    "article": "Art. 44",
    "title": "Definitions",
    "category": "Labor Law - Book 2",
    "simplified_text": "This article defines what 'manpower' (the people capable of producing goods/services) and 'entrepreneurship' (training for self-employment) mean in the context of the law.",
    "chunks": [
      "As used in this Title:",
      "(a) 'Manpower' shall mean that portion of the nation’s population which has actual or potential capability to contribute directly to the production of goods and services.",
      "(b) 'Entrepreneurship' shall mean training for self-employment or assisting individual or small industries within the purview of this Title."
    ],
    "tags": ["definitions", "manpower", "entrepreneurship", "workforce"],
    "language": "en"
  },
  {
    "article": "Art. 45",
    "title": "National Manpower and Youth Council; Composition",
    "category": "Labor Law - Book 2",
    "simplified_text": "This created a specific government council (which paved the way for TESDA today) attached to the Department of Labor to oversee and coordinate all manpower and youth training programs.",
    "chunks": [
      "To carry out the objectives of this Title, the National Manpower and Youth Council, which is attached to the Department of Labor for policy and program coordination and hereinafter referred to as the Council, is hereby created."
    ],
    "tags": ["NMYC", "council", "youth", "TESDA", "training"],
    "language": "en"
  },
  {
    "article": "Art. 46",
    "title": "National Manpower Plan",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council is required to create a long-term national plan to figure out how to best develop and use the skills of Filipino workers for jobs and businesses.",
    "chunks": [
      "The Council shall formulate a long-term national manpower plan for the optimum allocation, development and utilization of manpower for employment, entrepreneurship and economic and social growth.",
      "This manpower plan shall, after adoption by the NEDA, be updated annually and submitted to the President for his approval.",
      "Thereafter, it shall be the controlling plan for the development of manpower resources for the entire country in accordance with the national development plan."
    ],
    "tags": ["manpower plan", "NEDA", "development plan", "skills allocation"],
    "language": "en"
  },
  {
    "article": "Art. 47",
    "title": "National Manpower Skills Center",
    "category": "Labor Law - Book 2",
    "simplified_text": "The government must establish national, regional, and local skills centers to actively train people and research better training methods.",
    "chunks": [
      "The Council shall establish a National Manpower Skills Center and regional and local training centers for the purpose of promoting the development of skills.",
      "The centers shall be administered and operated under such rules and regulations as may be established by the Council."
    ],
    "tags": ["skills center", "training center", "regional training"],
    "language": "en"
  },
  {
    "article": "Art. 48",
    "title": "Establishment and formulation of skills standards",
    "category": "Labor Law - Book 2",
    "simplified_text": "The government, along with employers and workers, will set the official national standards for what skills are required for different industry trades and jobs.",
    "chunks": [
      "There shall be national skills standards for industry trades to be established by the Council in consultation with employers’ and workers’ organizations and appropriate government authorities.",
      "The Council shall thereafter administer the national skills standards."
    ],
    "tags": ["skills standards", "industry trades", "employer consultation", "qualifications"],
    "language": "en"
  },
  {
    "article": "Art. 49",
    "title": "Administration of training programs",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council is responsible for providing training for instructors, helping businesses train their own employees, and ensuring all training meets national standards.",
    "chunks": [
      "The Council shall provide, through the Secretariat, instructor training, entrepreneurship development, training in vocations, trades and other fields of employment, and assist any employer or organization in training schemes designed to attain its objectives under rules and regulations which the Council shall establish for this purpose."
    ],
    "tags": ["training programs", "instructor training", "employer assistance", "vocations"],
    "language": "en"
  }
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

# Run the script
if __name__ == "__main__":
    asyncio.run(run_seeder())