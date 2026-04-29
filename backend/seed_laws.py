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
  },
  {
    "article": "Art. 82",
    "title": "Coverage",
    "category": "Labor Law - Book 3",
    "simplified_text": "This section on working hours applies to almost all employees, but excludes government workers, managers, field personnel, and family members dependent on the employer.",
    "chunks": [
      "The provisions of this Title shall apply to employees in all establishments and undertakings whether for profit or not, but not to government employees, managerial employees, field personnel, members of the family of the employer who are dependent on him for support, domestic helpers, persons in the personal service of another, and workers who are paid by results as determined by the Secretary of Labor in appropriate regulations."
    ],
    "tags": ["coverage", "hours of work", "exemptions", "managerial employees"],
    "language": "en"
  },
  {
    "article": "Art. 83",
    "title": "Normal hours of work",
    "category": "Labor Law - Book 3",
    "simplified_text": "The standard legal working time for an employee is a maximum of 8 hours per day.",
    "chunks": [
      "The normal hours of work of any employee shall not exceed eight (8) hours a day.",
      "Health personnel in cities and municipalities with a population of at least one million or in hospitals with a bed capacity of at least one hundred (100) shall hold regular office hours for eight (8) hours a day, for five (5) days a week, exclusive of time for meals, except where the exigencies of the service require that such personnel work for six (6) days or forty-eight (48) hours, in which case, they shall be entitled to an additional compensation of at least thirty percent (30%) of their regular wage for work on the sixth day."
    ],
    "tags": ["working hours", "8 hours", "health personnel", "hospital workers"],
    "language": "en"
  },
  {
    "article": "Art. 84",
    "title": "Hours worked",
    "category": "Labor Law - Book 3",
    "simplified_text": "Working hours include all the time you are required to be at work, as well as short rest periods or 'coffee breaks.'",
    "chunks": [
      "Hours worked shall include (a) all time during which an employee is required to be on duty or to be at a prescribed workplace; and (b) all time during which an employee is suffered or permitted to work.",
      "Rest periods of short duration during working hours shall be considered as hours worked."
    ],
    "tags": ["hours worked", "rest periods", "on duty", "coffee breaks"],
    "language": "en"
  },
  {
    "article": "Art. 85",
    "title": "Meal periods",
    "category": "Labor Law - Book 3",
    "simplified_text": "Employers must give employees at least 60 minutes (1 hour) of unpaid time for their regular meals.",
    "chunks": [
      "Subject to such regulations as the Secretary of Labor may prescribe, it shall be the duty of every employer to allow his employees not less than sixty (60) minutes time-off for their regular meals."
    ],
    "tags": ["meal period", "lunch break", "break time"],
    "language": "en"
  },
  {
    "article": "Art. 86",
    "title": "Night shift differential",
    "category": "Labor Law - Book 3",
    "simplified_text": "If you work between 10:00 PM and 6:00 AM, you are entitled to an extra 10% of your regular wage for every hour worked.",
    "chunks": [
      "Every employee shall be paid a night shift differential of not less than ten percent (10%) of his regular wage for each hour of work performed between ten o’clock in the evening and six o’clock in the morning."
    ],
    "tags": ["night differential", "overnight work", "extra pay", "shift work"],
    "language": "en"
  },
  {
    "article": "Art. 87",
    "title": "Overtime work",
    "category": "Labor Law - Book 3",
    "simplified_text": "Work done beyond 8 hours a day must be paid an extra 25%. If the overtime is on a holiday or rest day, the extra pay is 30%.",
    "chunks": [
      "Work may be performed beyond eight (8) hours a day provided that the employee is paid for the overtime work, an additional compensation equivalent to his regular wage plus at least twenty-five percent (25%) thereof.",
      "Work performed beyond eight hours on a holiday or rest day shall be paid an additional compensation equivalent to the rate of the first eight hours on a holiday or rest day plus at least thirty percent (30%) thereof."
    ],
    "tags": ["overtime", "OT pay", "holiday pay", "rest day work"],
    "language": "en"
  },
  {
    "article": "Art. 88",
    "title": "Undertime not offset by overtime",
    "category": "Labor Law - Book 3",
    "simplified_text": "If you are late or leave early (undertime), the employer cannot 'cancel' it out by making you work overtime on another day. Overtime must always be paid extra.",
    "chunks": [
      "Undertime work on any particular day shall not be offset by overtime work on any other day. Permission given to the employee to go on leave on some other day of the week shall not exempt the employer from paying the additional compensation herein prescribed."
    ],
    "tags": ["undertime", "offsetting", "overtime pay", "leave"],
    "language": "en"
  },
  {
    "article": "Art. 156",
    "title": "First-aid treatment",
    "category": "Labor Law - Book 4",
    "simplified_text": "Every employer is required to keep a stock of first-aid medicines and equipment for the immediate treatment of workers in case of injury or emergency.",
    "chunks": [
      "Every employer shall keep in his establishment such first-aid medicines and equipment as the nature and conditions of work may require, in accordance with such regulations as the Department of Labor shall prescribe.",
      "The employer shall take steps for the training of a sufficient number of employees in first-aid treatment."
    ],
    "tags": ["first aid", "emergency", "safety", "medical supplies", "workplace safety"],
    "language": "en"
  },
  {
    "article": "Art. 157",
    "title": "Emergency medical and dental services",
    "category": "Labor Law - Book 4",
    "simplified_text": "Depending on the number of employees, employers must hire graduate first-aiders, nurses, dentists, or physicians to be available for health emergencies.",
    "chunks": [
      "It shall be the duty of every employer to furnish his employees in any locality with free medical and dental attendance and facilities consisting of:",
      "(a) The services of a graduate first-aider when the number of workers exceeds fifty (50) but not more than two hundred (200);",
      "(b) The services of a full-time registered nurse when the number of employees exceeds two hundred (200) but not more than three hundred (300);",
      "(c) The services of a graduate licensed physician and a dentist on a part-time basis when the number of employees exceeds three hundred (300)...",
      "(d) The services of a full-time physician, a dentist and a nurse when the number of employees exceeds three hundred (300) and the workplace is hazardous."
    ],
    "tags": ["medical services", "dental services", "company nurse", "company doctor", "hazardous workplace"],
    "language": "en"
  },
  {
    "article": "Art. 158",
    "title": "When emergency hospital is not required",
    "category": "Labor Law - Book 4",
    "simplified_text": "If there is a hospital or clinic very close to the workplace (accessible within 5 kilometers or 25 minutes), the employer doesn't need to build their own emergency hospital.",
    "chunks": [
      "The requirement for an emergency hospital or dental clinic shall not be applicable in case there is a hospital or dental clinic which is accessible from the establishment and whose facilities and services may be utilized by the employees.",
      "Accessible shall mean within five (5) kilometers from the establishment or can be reached within twenty-five (25) minutes of travel."
    ],
    "tags": ["emergency hospital", "accessibility", "clinic", "hospital proximity"],
    "language": "en"
  },
  {
    "article": "Art. 159",
    "title": "Health program",
    "category": "Labor Law - Book 4",
    "simplified_text": "Physicians and dentists in companies are required to create and follow a health program for the employees' well-being.",
    "chunks": [
      "The physician engaged by an employer shall, in addition to his duties under this Chapter, develop and implement a comprehensive occupational health program for the benefit of the employees of his employer."
    ],
    "tags": ["health program", "occupational health", "employee wellness"],
    "language": "en"
  },
  {
    "article": "Art. 160",
    "title": "Qualifications of health personnel",
    "category": "Labor Law - Book 4",
    "simplified_text": "The medical staff hired by the company must be properly licensed and meet the standards set by the Secretary of Labor.",
    "chunks": [
      "The physicians, dentists and nurses employed by an employer pursuant to this Chapter shall possess the qualifications required by law, and their salaries shall not be less than those provided for by existing laws and regulations."
    ],
    "tags": ["qualifications", "medical license", "nursing", "salaries"],
    "language": "en"
  },
  {
    "article": "Art. 161",
    "title": "Assistance of employer",
    "category": "Labor Law - Book 4",
    "simplified_text": "Employers must provide the necessary space and equipment to ensure the health personnel can do their jobs effectively.",
    "chunks": [
      "It shall be the duty of any employer to provide all the necessary assistance and facilities as may be required by the health personnel in the performance of their duties."
    ],
    "tags": ["employer duty", "medical facilities", "workplace health"],
    "language": "en"
  },
  {
    "article": "Art. 162",
    "title": "Safety and health standards",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Secretary of Labor sets the mandatory rules for safety and health in all workplaces to prevent accidents and illness.",
    "chunks": [
      "The Secretary of Labor shall, by appropriate orders, set and enforce mandatory occupational safety and health standards to eliminate or reduce occupational safety and health hazards in all workplaces and institute new, and update existing, programs to ensure safe and healthful working conditions in all places of employment."
    ],
    "tags": ["safety standards", "OSH", "hazards", "working conditions"],
    "language": "en"
  },
  {
    "article": "Art. 211",
    "title": "Declaration of Policy",
    "category": "Labor Law - Book 5",
    "simplified_text": "The government promotes free collective bargaining, unionism, and social justice as the best ways to keep peace between workers and employers.",
    "chunks": [
      "(a) To promote and emphasize the primacy of free collective bargaining and negotiations...",
      "(b) To promote free trade unionism as an instrument for the enhancement of democracy and the promotion of social justice and development;",
      "(c) To foster the free and voluntary organization of a strong and united labor movement;",
      "(d) To promote the enlightenment of workers concerning their rights and obligations as union members and as employees;",
      "(e) To provide an adequate administrative machinery for the expeditious settlement of labor or industrial disputes."
    ],
    "tags": ["policy", "labor relations", "unionism", "collective bargaining", "social justice"],
    "language": "en"
  },
  {
    "article": "Art. 212",
    "title": "Definitions",
    "category": "Labor Law - Book 5",
    "simplified_text": "This defines important terms like 'Employer', 'Employee', 'Labor Organization', and 'Strike' specifically for labor relations cases.",
    "chunks": [
      "(f) 'Labor organization' means any union or association of employees which exists in whole or in part for the purpose of collective bargaining...",
      "(g) 'Legitimate labor organization' means any labor organization duly registered with the Department of Labor and Employment...",
      "(l) 'Strike' means any temporary stoppage of work by the concerted action of employees as a result of an industrial or labor dispute.",
      "(m) 'Lockout' means the temporary refusal of an employer to furnish work as a result of an industrial or labor dispute."
    ],
    "tags": ["definitions", "strike", "lockout", "labor organization", "union"],
    "language": "en"
  },
  {
    "article": "Art. 213",
    "title": "National Labor Relations Commission",
    "category": "Labor Law - Book 5",
    "simplified_text": "This creates the NLRC, the special 'court' that decides on labor cases and disputes between workers and companies.",
    "chunks": [
      "There shall be a National Labor Relations Commission which shall be attached to the Department of Labor and Employment for program and policy coordination only, composed of a Chairman and fourteen (14) Members."
    ],
    "tags": ["NLRC", "commission", "labor court", "DOLE"],
    "language": "en"
  },
  {
    "article": "Art. 214",
    "title": "Headquarters, Branches and Units",
    "category": "Labor Law - Book 5",
    "simplified_text": "The main office of the NLRC is in Manila, but it has several branches (Regional Arbitration Branches) all over the country to handle local cases.",
    "chunks": [
      "The Commission and its eight (8) divisions shall have their main office in Metropolitan Manila...",
      "The Commission shall establish as many regional arbitration branches as there are regional offices of the Department of Labor and Employment sub-units as may be necessary."
    ],
    "tags": ["NLRC branches", "headquarters", "regional arbitration", "arbitrator"],
    "language": "en"
  },
  {
    "article": "Art. 215",
    "title": "Appointment and Qualifications",
    "category": "Labor Law - Book 5",
    "simplified_text": "People who sit as judges in the NLRC must be members of the Philippine Bar (lawyers) and have experience in labor law for at least 15 years.",
    "chunks": [
      "The Chairman and other Commissioners shall be members of the Philippine Bar and must have been engaged in the practice of law in the Philippines for at least fifteen (15) years...",
      "They shall be appointed by the President, subject to confirmation by the Commission on Appointments."
    ],
    "tags": ["qualifications", "commissioners", "lawyer", "appointment"],
    "language": "en"
  },
  {
    "article": "Art. 216",
    "title": "Salaries, benefits and other emoluments",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Chairman and Commissioners of the NLRC receive the same salaries and benefits as judges in the Court of Appeals.",
    "chunks": [
      "The Chairman and members of the Commission shall receive an annual salary at least equivalent to, and be entitled to the same allowances and benefits as those of the Presiding Justice and Associate Justices of the Court of Appeals, respectively."
    ],
    "tags": ["salary", "benefits", "commissioner pay", "NLRC"],
    "language": "en"
  },
  {
    "article": "Art. 217",
    "title": "Jurisdiction of Labor Arbiters and the Commission",
    "category": "Labor Law - Book 5",
    "simplified_text": "This lists what cases the NLRC can handle, including illegal dismissal, unpaid wages, and damages arising from employer-employee relations.",
    "chunks": [
      "The Labor Arbiters shall have original and exclusive jurisdiction to hear and decide... the following cases involving all workers:",
      "1. Unfair labor practice cases;",
      "2. Termination disputes;",
      "3. If accompanied with a claim for reinstatement, those cases that workers may file involving wages, rates of pay, hours of work and other terms and conditions of employment;",
      "4. Claims for actual, moral, exemplary and other forms of damages arising from the employer-employee relations."
    ],
    "tags": ["jurisdiction", "illegal dismissal", "termination", "unfair labor practice", "unpaid wages"],
    "language": "en"
  },
  {
    "article": "Art. 278",
    "title": "Coverage",
    "category": "Labor Law - Book 6",
    "simplified_text": "The rules regarding the end of employment apply to all establishments, including non-profit organizations.",
    "chunks": [
      "The provisions of this Title shall apply to all establishments or undertakings, whether for profit or not."
    ],
    "tags": ["coverage", "post-employment", "termination", "applicability"],
    "language": "en"
  },
  {
    "article": "Art. 279",
    "title": "Security of Tenure",
    "category": "Labor Law - Book 6",
    "simplified_text": "In regular employment, an employer cannot fire a worker without a 'just cause' or 'authorized cause' provided by law. If a worker is fired illegally, they must be reinstated with full backwages.",
    "chunks": [
      "In cases of regular employment, the employer shall not terminate the services of an employee except for a just cause or when authorized by this Title.",
      "An employee who is unjustly dismissed from work shall be entitled to reinstatement without loss of seniority rights and other privileges and to his full backwages, inclusive of allowances, and to his other benefits or their monetary equivalent computed from the time his compensation was withheld from him up to the time of his actual reinstatement."
    ],
    "tags": ["security of tenure", "just cause", "illegal dismissal", "backwages", "reinstatement"],
    "language": "en"
  },
  {
    "article": "Art. 280",
    "title": "Regular and Casual Employment",
    "category": "Labor Law - Book 6",
    "simplified_text": "An employee is considered 'regular' if their work is necessary for the business. Even if there is a contract saying otherwise, if a person has worked for at least one year, they are considered regular for that specific activity.",
    "chunks": [
      "The provisions of written agreement to the contrary notwithstanding and regardless of the oral agreement of the parties, an employment shall be deemed to be regular where the employee has been engaged to perform activities which are usually necessary or desirable in the usual business or trade of the employer...",
      "Any employee who has rendered at least one year of service, whether such service is continuous or broken, shall be considered a regular employee with respect to the activity in which he is employed and his employment shall continue while such activity exists."
    ],
    "tags": ["regular employee", "casual employee", "employment status", "tenure"],
    "language": "en"
  },
  {
    "article": "Art. 281",
    "title": "Probationary Employment",
    "category": "Labor Law - Book 6",
    "simplified_text": "Probationary periods cannot exceed 6 months. If you continue working after the 6 months, you automatically become a regular employee.",
    "chunks": [
      "Probationary employment shall not exceed six (6) months from the date the employee started working, unless it is covered by an apprenticeship agreement stipulating a longer period.",
      "An employee who is allowed to work after a probationary period shall be considered a regular employee."
    ],
    "tags": ["probationary", "6 months", "regularization", "training period"],
    "language": "en"
  },
  {
    "article": "Art. 282",
    "title": "Termination by Employer (Just Causes)",
    "category": "Labor Law - Book 6",
    "simplified_text": "An employer can legally fire an employee for serious misconduct, willful disobedience, gross neglect of duties, fraud, or committing a crime against the employer.",
    "chunks": [
      "An employer may terminate an employment for any of the following causes:",
      "(a) Serious misconduct or willful disobedience by the employee of the lawful orders of his employer or representative in connection with his work;",
      "(b) Gross and habitual neglect by the employee of his duties;",
      "(c) Fraud or willful breach by the employee of the trust reposed in him by his employer or duly authorized representative;",
      "(d) Commission of a crime or offense by the employee against the person of his employer or any immediate member of his family or his duly authorized representatives."
    ],
    "tags": ["just causes", "firing", "misconduct", "negligence", "termination"],
    "language": "en"
  },
  {
    "article": "Art. 283",
    "title": "Closure of Establishment and Reduction of Personnel",
    "category": "Labor Law - Book 6",
    "simplified_text": "An employer can let go of workers due to business closure or to save the company (retrenchment), but they must give 1-month notice and pay separation pay (usually 1 month pay or 1/2 month pay per year of service).",
    "chunks": [
      "The employer may also terminate the employment of any employee due to the installation of labor-saving devices, redundancy, retrenchment to prevent losses or the closing or cessation of operation of the establishment...",
      "The employer shall serve a written notice on the workers and the Ministry of Labor and Employment at least one (1) month before the intended date thereof.",
      "In case of retrenchment to prevent losses and in cases of closures or cessation of operations of establishment... the separation pay shall be equivalent to one (1) month pay or at least one-half (1/2) month pay for every year of service, whichever is higher."
    ],
    "tags": ["authorized causes", "retrenchment", "redundancy", "separation pay", "closure"],
    "language": "en"
  },
  {
    "article": "Art. 284",
    "title": "Disease as ground for termination",
    "category": "Labor Law - Book 6",
    "simplified_text": "An employer can terminate an employee who has a disease that is prohibited by law or prejudicial to their health/co-workers, but only if it cannot be cured within 6 months. Separation pay is required.",
    "chunks": [
      "An employer may terminate the services of an employee who has been found to be suffering from any disease and whose continued employment is prohibited by law or is prejudicial to his health as well as to the health of his co-employees:",
      "Provided, That he is paid separation pay equivalent to at least one (1) month salary or to one-half (1/2) month salary for every year of service, whichever is greater, a fraction of at least six (6) months being considered as one (1) whole year."
    ],
    "tags": ["disease", "termination", "health", "separation pay", "medical grounds"],
    "language": "en"
  },
  {
    "article": "Art. 288",
    "title": "Penalties",
    "category": "Labor Law - Book 7",
    "simplified_text": "Anyone who violates any provision of the Labor Code can be punished with a fine or imprisonment, or both, depending on the court's decision.",
    "chunks": [
      "Except as otherwise provided in this Code, or unless the acts complained of hinge on a question of interpretation or implementation of ambiguous provisions of an existing collective bargaining agreement, any violation of the provisions of this Code declared to be unlawful or penal in nature shall be punished with a fine of not less than One Thousand Pesos (P1,000.00) nor more than Ten Thousand Pesos (P10,000.00) or imprisonment of not less than three months nor more than three years, or both such fine and imprisonment at the discretion of the court."
    ],
    "tags": ["penalties", "fines", "imprisonment", "violations", "enforcement"],
    "language": "en"
  },
  {
    "article": "Art. 289",
    "title": "Who are liable when committed by other than natural person",
    "category": "Labor Law - Book 7",
    "simplified_text": "If a corporation or organization breaks the law, the officers responsible (like the president or manager) are the ones who will face the penalties.",
    "chunks": [
      "If the offense is committed by a corporation, trust, firm, partnership, association or any other entity, the penalty shall be imposed upon the guilty officer or officers of such corporation, trust, firm, partnership, association or entity."
    ],
    "tags": ["liability", "corporations", "officers", "responsibility"],
    "language": "en"
  },
  {
    "article": "Art. 290",
    "title": "Offenses",
    "category": "Labor Law - Book 7",
    "simplified_text": "Criminal offenses under this Code (like illegal recruitment) must be filed in court within 3 years, otherwise, the case can no longer be pursued.",
    "chunks": [
      "Offenses penalized under this Code and the rules and regulations issued pursuant thereto shall prescribe in three (3) years.",
      "All unfair labor practice cases shall be filed with the appropriate agency within one (1) year from the occurrence of such unfair labor practice; otherwise, they shall be forever barred."
    ],
    "tags": ["prescription", "offenses", "statute of limitations", "unfair labor practice"],
    "language": "en"
  },
  {
    "article": "Art. 291",
    "title": "Money claims",
    "category": "Labor Law - Book 7",
    "simplified_text": "All money claims (unpaid wages, benefits, etc.) must be filed within 3 years from the time the worker was supposed to receive them.",
    "chunks": [
      "All money claims arising from employer-employee relations accruing during the effectivity of this Code shall be filed within three (3) years from the time the cause of action accrued; otherwise they shall be forever barred."
    ],
    "tags": ["money claims", "unpaid wages", "claims period", "backwages"],
    "language": "en"
  },
  {
    "article": "Art. 292",
    "title": "Institution of money claims",
    "category": "Labor Law - Book 7",
    "simplified_text": "Money claims are usually filed with the Regional Director of the Department of Labor, especially if they involve multiple workers in one establishment.",
    "chunks": [
      "Money claims specified in the immediately preceding Article shall be filed before the appropriate regional director or the authorized hearing officer of the Department of Labor and Employment in the region where the employer's establishment is located."
    ],
    "tags": ["filing claims", "regional director", "DOLE", "procedure"],
    "language": "en"
  },
  {
    "article": "Art. 293",
    "title": "Disposition of pending cases",
    "category": "Labor Law - Book 7",
    "simplified_text": "Any labor cases that were already started before this Code was enacted will still be finished based on the old laws that were in place at that time.",
    "chunks": [
      "All cases, involving administration and enforcement of labor laws under the jurisdiction of the units of the Department of Labor and Employment at the time of the enactment of this Code, shall be allowed to continue to be processed and decided by such units and the corresponding rules and regulations shall continue to apply."
    ],
    "tags": ["pending cases", "enactment", "transition", "legal procedure"],
    "language": "en"
  },
  {
    "article": "Art. 294",
    "title": "Personnel of defunct organization",
    "category": "Labor Law - Book 7",
    "simplified_text": "If a government labor office is closed or replaced, its employees are usually absorbed into the new office or given priority for new positions.",
    "chunks": [
      "The personnel of agencies or units of the Department of Labor and Employment which are abolished or reorganized by this Code shall be absorbed by the appropriate units of the Department or given priority in filling the positions within the new setups."
    ],
    "tags": ["reorganization", "government personnel", "DOLE", "employment"],
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