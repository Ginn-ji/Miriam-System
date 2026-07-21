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
  {
    "article": "Art. 1",
    "title": "Name of Decree",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "This decree shall be known as the “Labor Code of the\nPhilippines.”",
    "chunks": [
      "This decree shall be known as the “Labor Code of the\nPhilippines.”"
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 2",
    "title": "Date of Effectivity",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "This Code shall take effect six (6) months after its\npromulgation.",
    "chunks": [
      "This Code shall take effect six (6) months after its\npromulgation."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 3",
    "title": "Declaration of Basic Policy",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "The State shall afford protection to labor, promote\nfull employment, ensure equal work opportunities regardless of sex, race or creed, and\nregulate the relations between workers and employers. The State shall assure the rights of\nworkers to self-organization, collective bargaining, security of tenure, and just and humane\nconditions of work.",
    "chunks": [
      "The State shall afford protection to labor, promote\nfull employment, ensure equal work opportunities regardless of sex, race or creed, and\nregulate the relations between workers and employers. The State shall assure the rights of\nworkers to self-organization, collective bargaining, security of tenure, and just and humane\nconditions of work."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 4",
    "title": "Construction in Favor of Labor",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "All doubts in the implementation and\ninterpretation of the provisions of this Code, including its implementing rules and regulations,\nshall be resolved in favor of labor.",
    "chunks": [
      "All doubts in the implementation and\ninterpretation of the provisions of this Code, including its implementing rules and regulations,\nshall be resolved in favor of labor."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 5",
    "title": "Rules and Regulations",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "The Department of Labor and other government\nagencies charged with the administration and enforcement of this Code or any of its parts shall\npromulgate the necessary implementing rules and regulations. Such rules and regulations shall\nbecome effective fifteen (15) days after announcement of their adoption in newspapers of\ngeneral circulation.",
    "chunks": [
      "The Department of Labor and other government\nagencies charged with the administration and enforcement of this Code or any of its parts shall\npromulgate the necessary implementing rules and regulations. Such rules and regulations shall\nbecome effective fifteen (15) days after announcement of their adoption in newspapers of\ngeneral circulation."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 6",
    "title": "Applicability",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "All rights and benefits granted to workers under this Code shall,\nexcept as may otherwise be provided herein, apply alike to all workers, whether agricultural\nor non-agricultural.",
    "chunks": [
      "All rights and benefits granted to workers under this Code shall,\nexcept as may otherwise be provided herein, apply alike to all workers, whether agricultural\nor non-agricultural."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 7",
    "title": "Statement of Objectives",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "Inasmuch as the old concept of land ownership by a\nfew has spawned valid and legitimate grievances that gave rise to violent conflict and social\ntension and the redress of such legitimate grievances being one of the fundamental objectives\nof the New Society, it has become imperative to start reformation with the emancipation of\nthe tiller of the soil from his bondage.",
    "chunks": [
      "Inasmuch as the old concept of land ownership by a\nfew has spawned valid and legitimate grievances that gave rise to violent conflict and social\ntension and the redress of such legitimate grievances being one of the fundamental objectives\nof the New Society, it has become imperative to start reformation with the emancipation of\nthe tiller of the soil from his bondage."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter II - EMANCIPATION OF TENANTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 8",
    "title": "Transfer of Lands to Tenant-Workers",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "Being a vital part of the labor force,\ntenant-farmers on private agricultural lands primarily devoted to rice and corn under a system\nof share crop or lease tenancy whether classified as landed estate or not shall be deemed\nowner of a portion constituting a family-size farm of five (5) hectares if not irrigated and three\n(3) hectares if irrigated.\n\nIn all cases, the land owner may retain an area of not more than seven (7) hectares if such\nlandowner is cultivating such area or will now cultivate it.",
    "chunks": [
      "Being a vital part of the labor force,\ntenant-farmers on private agricultural lands primarily devoted to rice and corn under a system\nof share crop or lease tenancy whether classified as landed estate or not shall be deemed\nowner of a portion constituting a family-size farm of five (5) hectares if not irrigated and three\n(3) hectares if irrigated.",
      "In all cases, the land owner may retain an area of not more than seven (7) hectares if such\nlandowner is cultivating such area or will now cultivate it."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter II - EMANCIPATION OF TENANTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 9",
    "title": "Determination of Land Value",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "For the purpose of determining the cost of the\nland to be transferred to the tenant-farmer, the value of the land shall be equivalent to two\nand one-half (2-1/2) times the average harvest of three (3) normal crop years immediately\npreceding the promulgation of Presidential Decree No. 27 on October 21, 1972.\n\nThe total cost of the land, including interest at the rate of six percent (6%) per annum,\nshall be paid by the tenant in fifteen (15) years of fifteen (15) equal annual amortizations.\n\nIn case of default, the amortization due shall be paid by the farmers’ cooperative in which\nthe defaulting tenant-farmer is a member, with the cooperative having a right of recourse\nagainst him.\n\nThe government shall guarantee such amortizations with shares of stock in government-\nowned and government-controlled corporations.",
    "chunks": [
      "For the purpose of determining the cost of the\nland to be transferred to the tenant-farmer, the value of the land shall be equivalent to two\nand one-half (2-1/2) times the average harvest of three (3) normal crop years immediately\npreceding the promulgation of Presidential Decree No. 27 on October 21, 1972.",
      "The total cost of the land, including interest at the rate of six percent (6%) per annum,\nshall be paid by the tenant in fifteen (15) years of fifteen (15) equal annual amortizations.",
      "In case of default, the amortization due shall be paid by the farmers’ cooperative in which\nthe defaulting tenant-farmer is a member, with the cooperative having a right of recourse\nagainst him.",
      "The government shall guarantee such amortizations with shares of stock in government-\nowned and government-controlled corporations."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter II - EMANCIPATION OF TENANTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 10",
    "title": "Conditions of Ownership",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "No title to the land acquired by the tenant-farmer\nunder Presidential Decree No. 27 shall be actually issued to him unless and until he has become\na full-fledged member of a duly recognized farmers’ cooperative.\n\nTitle to the land acquired pursuant to Presidential Decree No. 27 or the Land Reform\nProgram of the Government shall not be transferable except by hereditary succession or to\nthe Government in accordance with the provisions of Presidential Decree No. 27, the Code of\nAgrarian Reforms and other existing laws and regulations.",
    "chunks": [
      "No title to the land acquired by the tenant-farmer\nunder Presidential Decree No. 27 shall be actually issued to him unless and until he has become\na full-fledged member of a duly recognized farmers’ cooperative.",
      "Title to the land acquired pursuant to Presidential Decree No. 27 or the Land Reform\nProgram of the Government shall not be transferable except by hereditary succession or to\nthe Government in accordance with the provisions of Presidential Decree No. 27, the Code of\nAgrarian Reforms and other existing laws and regulations."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter II - EMANCIPATION OF TENANTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 11",
    "title": "Implementing Agency",
    "category": "Labor Law - Preliminary Title",
    "simplified_text": "The Department of Agrarian Reform shall promulgate\nthe necessary rules and regulations to implement the provisions of this Chapter.",
    "chunks": [
      "The Department of Agrarian Reform shall promulgate\nthe necessary rules and regulations to implement the provisions of this Chapter."
    ],
    "tags": [
      "PRELIMINARY TITLE",
      "Chapter II - EMANCIPATION OF TENANTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 12",
    "title": "Statement of Objectives",
    "category": "Labor Law - Book 1",
    "simplified_text": "It is the policy of the State:\n\na) To promote and maintain a state of full employment through improved manpower\ntraining, allocation and utilization;\n\nb) To protect every citizen desiring to work locally or overseas by securing for him the\nbest possible terms and conditions of employment;\n\nc) To facilitate a free choice of available employment by persons seeking work in\nconformity with the national interest;\n\nd) To facilitate and regulate the movement of workers in conformity with the national\ninterest;\n\ne) To regulate the employment of aliens, including the establishment of a registration\nand/or work permit system;\n\nf) To strengthen the network of public employment offices and rationalize the\nparticipation of the private sector in the recruitment and placement of workers, locally and\noverseas, to serve national development objectives;\n\ng) To insure careful selection of Filipino workers for overseas employment in order to\nprotect the good name of the Philippines abroad.",
    "chunks": [
      "It is the policy of the State:",
      "a) To promote and maintain a state of full employment through improved manpower\ntraining, allocation and utilization;",
      "b) To protect every citizen desiring to work locally or overseas by securing for him the\nbest possible terms and conditions of employment;",
      "c) To facilitate a free choice of available employment by persons seeking work in\nconformity with the national interest;",
      "d) To facilitate and regulate the movement of workers in conformity with the national\ninterest;",
      "e) To regulate the employment of aliens, including the establishment of a registration\nand/or work permit system;",
      "f) To strengthen the network of public employment offices and rationalize the\nparticipation of the private sector in the recruitment and placement of workers, locally and\noverseas, to serve national development objectives;",
      "g) To insure careful selection of Filipino workers for overseas employment in order to\nprotect the good name of the Philippines abroad."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT"
    ],
    "language": "en"
  },
  {
    "article": "Art. 13",
    "title": "Definitions",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) \"Worker\" means any member of the labor force, whether\nemployed or unemployed.\n\n(b) \"Recruitment and placement\" refers to any act of canvassing, enlisting, contracting,\ntransporting, utilizing, hiring or procuring workers, and includes referrals, contract services,\npromising or advertising for employment, locally or abroad, whether for profit or not:\nProvided, That any person or entity which, in any manner, offers or promises for a fee,\nemployment to two or more persons shall be deemed engaged in recruitment and placement.\n\n(c) \"Private fee-charging employment agency\" means any person or entity engaged in\nrecruitment and placement of workers for a fee which is charged, directly or indirectly, from\nthe workers or employers or both.\n\n(d) \"License\" means a document issued by the Department of Labor authorizing a person\nor entity to operate a private employment agency.\n\n(e) \"Private recruitment entity\" means any person or association engaged in the\nrecruitment and placement of workers, locally or overseas, without charging, directly or\nindirectly, any fee from the workers or employers.\n\n(f) \"Authority\" means a document issued by the Department of Labor authorizing a person\nor association to engage in recruitment and placement activities as a private recruitment\nentity.\n\n(g) \"Seaman\" means any person employed in a vessel engaged in maritime navigation.\n\n(h) \"Overseas employment\" means employment of a worker outside the Philippines.\n\n(i) \"Emigrant\" means any person, worker or otherwise, who emigrates to a foreign\ncountry by virtue of an immigrant visa or resident permit or its equivalent in the country of\ndestination.",
    "chunks": [
      "(a) \"Worker\" means any member of the labor force, whether\nemployed or unemployed.",
      "(b) \"Recruitment and placement\" refers to any act of canvassing, enlisting, contracting,\ntransporting, utilizing, hiring or procuring workers, and includes referrals, contract services,\npromising or advertising for employment, locally or abroad, whether for profit or not:\nProvided, That any person or entity which, in any manner, offers or promises for a fee,\nemployment to two or more persons shall be deemed engaged in recruitment and placement.",
      "(c) \"Private fee-charging employment agency\" means any person or entity engaged in\nrecruitment and placement of workers for a fee which is charged, directly or indirectly, from\nthe workers or employers or both.",
      "(d) \"License\" means a document issued by the Department of Labor authorizing a person\nor entity to operate a private employment agency.",
      "(e) \"Private recruitment entity\" means any person or association engaged in the\nrecruitment and placement of workers, locally or overseas, without charging, directly or\nindirectly, any fee from the workers or employers.",
      "(f) \"Authority\" means a document issued by the Department of Labor authorizing a person\nor association to engage in recruitment and placement activities as a private recruitment\nentity.",
      "(g) \"Seaman\" means any person employed in a vessel engaged in maritime navigation.",
      "(h) \"Overseas employment\" means employment of a worker outside the Philippines.",
      "(i) \"Emigrant\" means any person, worker or otherwise, who emigrates to a foreign\ncountry by virtue of an immigrant visa or resident permit or its equivalent in the country of\ndestination."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 14",
    "title": "Employment Promotion",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Secretary of Labor shall have the power and\nauthority:\n\n(a) To organize and establish new employment offices in addition to the existing\nemployment offices under the Department of Labor as the need arises;\n\n(b) To organize and establish a nationwide job clearance and information system to\ninform applicants registering with a particular employment office of job opportunities in other\nparts of the country as well as job opportunities abroad;\n\n(c) To develop and organize a program that will facilitate occupational, industrial and\ngeographical mobility of labor and provide assistance in the relocation of workers from one\narea to another; and\n\n(d) To require any person, establishment, organization or institution to submit such\nemployment information as may be prescribed by the Secretary of Labor.",
    "chunks": [
      "The Secretary of Labor shall have the power and\nauthority:",
      "(a) To organize and establish new employment offices in addition to the existing\nemployment offices under the Department of Labor as the need arises;",
      "(b) To organize and establish a nationwide job clearance and information system to\ninform applicants registering with a particular employment office of job opportunities in other\nparts of the country as well as job opportunities abroad;",
      "(c) To develop and organize a program that will facilitate occupational, industrial and\ngeographical mobility of labor and provide assistance in the relocation of workers from one\narea to another; and",
      "(d) To require any person, establishment, organization or institution to submit such\nemployment information as may be prescribed by the Secretary of Labor."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 15",
    "title": "Bureau of Employment Services",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) The Bureau of Employment Services shall\nbe primarily responsible for developing and monitoring a comprehensive employment\nprogram. It shall have the power and duty:\n\n1.To formulate and develop plans and programs to implement the employment\npromotion objectives of this Title;\n\n2.To establish and maintain a registration and/or licensing system to regulate\nprivate sector participation in the recruitment and placement of workers, locally and\noverseas, and to secure the best possible terms and conditions of employment for Filipino\ncontract workers and compliance therewith under such rules and regulations as may be\nissued by the Minister of Labor;\n\n3.To formulate and develop employment programs designed to benefit\ndisadvantaged groups and communities;\n\n4.To establish and maintain a registration and/or work permit system to regulate\nthe employment of aliens;\n\n5.To develop a labor market information system in aid of proper manpower and\ndevelopment planning;\n\n6.To develop a responsive vocational guidance and testing system in aid of proper\nhuman resources allocation; and\n\n7.To maintain a central registry of skills, except seamen.\n\n[(b) The regional offices of the Ministry of Labor shall have the original and exclusive\njurisdiction over all matters or cases involving employer-employee relations including money\nclaims, arising out of or by virtue of any law or contracts involving Filipino workers for overseas\nemployment except seamen: Provided, That the Bureau of Employment Services may, in the\ncase of the National Capital Region, exercise such power, whenever the Minister of Labor\ndeems it appropriate. The decisions of the regional offices of the Bureau of Employment\nServices, if so authorized by the Minister of Labor as provided in this Article, shall be\nappealable to the National Labor Relations Commission upon the same grounds provided in\nArticle 223 hereof. The decisions of the National Labor Relations Commission shall be final and\nunappealable.]\n\n(c) The Minister of Labor shall have the power to impose and collect fees based on rates\nrecommended by the Bureau of Employment Services. Such fees shall be deposited in the\nNational Treasury as a special account of the General Fund, for the promotion of the objectives\nof the Bureau of Employment Services, subject to the provisions of Section 40 of Presidential\nDecree No. 1177.",
    "chunks": [
      "(a) The Bureau of Employment Services shall\nbe primarily responsible for developing and monitoring a comprehensive employment\nprogram. It shall have the power and duty:",
      "1.To formulate and develop plans and programs to implement the employment\npromotion objectives of this Title;",
      "2.To establish and maintain a registration and/or licensing system to regulate\nprivate sector participation in the recruitment and placement of workers, locally and\noverseas, and to secure the best possible terms and conditions of employment for Filipino\ncontract workers and compliance therewith under such rules and regulations as may be\nissued by the Minister of Labor;",
      "3.To formulate and develop employment programs designed to benefit\ndisadvantaged groups and communities;",
      "4.To establish and maintain a registration and/or work permit system to regulate\nthe employment of aliens;",
      "5.To develop a labor market information system in aid of proper manpower and\ndevelopment planning;",
      "6.To develop a responsive vocational guidance and testing system in aid of proper\nhuman resources allocation; and",
      "7.To maintain a central registry of skills, except seamen.",
      "[(b) The regional offices of the Ministry of Labor shall have the original and exclusive\njurisdiction over all matters or cases involving employer-employee relations including money\nclaims, arising out of or by virtue of any law or contracts involving Filipino workers for overseas\nemployment except seamen: Provided, That the Bureau of Employment Services may, in the\ncase of the National Capital Region, exercise such power, whenever the Minister of Labor\ndeems it appropriate. The decisions of the regional offices of the Bureau of Employment\nServices, if so authorized by the Minister of Labor as provided in this Article, shall be\nappealable to the National Labor Relations Commission upon the same grounds provided in\nArticle 223 hereof. The decisions of the National Labor Relations Commission shall be final and\nunappealable.]",
      "(c) The Minister of Labor shall have the power to impose and collect fees based on rates\nrecommended by the Bureau of Employment Services. Such fees shall be deposited in the\nNational Treasury as a special account of the General Fund, for the promotion of the objectives\nof the Bureau of Employment Services, subject to the provisions of Section 40 of Presidential\nDecree No. 1177."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 16",
    "title": "Private Recruitment",
    "category": "Labor Law - Book 1",
    "simplified_text": "Except as provided in Chapter II of this Title, no person\nor entity other than the public employment offices, shall engage in the recruitment and\nplacement of workers.",
    "chunks": [
      "Except as provided in Chapter II of this Title, no person\nor entity other than the public employment offices, shall engage in the recruitment and\nplacement of workers."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 17",
    "title": "Overseas Employment Development Board",
    "category": "Labor Law - Book 1",
    "simplified_text": "An Overseas Employment\nDevelopment Board is hereby created to undertake, in cooperation with relevant entities and\n\nagencies, a systematic program for overseas employment of Filipino workers in excess of\ndomestic needs and to protect their rights to fair and equitable employment practices. It shall\nhave the power and duty:\n\n1.To promote the overseas employment of Filipino workers through a comprehensive\nmarket promotion and development program;\n\n2.To secure the best possible terms and conditions of employment of Filipino contract\nworkers on a government-to-government basis and to ensure compliance therewith;\n\n3.To recruit and place workers for overseas employment on a government-to-\ngovernment arrangement and in such other sectors as policy may dictate; and\n\n4.To act as secretariat for the Board of Trustees of the Welfare and Training Fund for\nOverseas Workers.",
    "chunks": [
      "An Overseas Employment\nDevelopment Board is hereby created to undertake, in cooperation with relevant entities and",
      "agencies, a systematic program for overseas employment of Filipino workers in excess of\ndomestic needs and to protect their rights to fair and equitable employment practices. It shall\nhave the power and duty:",
      "1.To promote the overseas employment of Filipino workers through a comprehensive\nmarket promotion and development program;",
      "2.To secure the best possible terms and conditions of employment of Filipino contract\nworkers on a government-to-government basis and to ensure compliance therewith;",
      "3.To recruit and place workers for overseas employment on a government-to-\ngovernment arrangement and in such other sectors as policy may dictate; and",
      "4.To act as secretariat for the Board of Trustees of the Welfare and Training Fund for\nOverseas Workers."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 18",
    "title": "Ban on Direct-Hiring",
    "category": "Labor Law - Book 1",
    "simplified_text": "No employer may hire a Filipino worker for overseas\nemployment except through the Boards and entities authorized by the Secretary of Labor.\nDirect-hiring by members of the diplomatic corps, international organizations and such other\nemployers as may be allowed by the Secretary of Labor is exempted from this provision.",
    "chunks": [
      "No employer may hire a Filipino worker for overseas\nemployment except through the Boards and entities authorized by the Secretary of Labor.\nDirect-hiring by members of the diplomatic corps, international organizations and such other\nemployers as may be allowed by the Secretary of Labor is exempted from this provision."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 19",
    "title": "Office of Emigrant Affairs",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) Pursuant to the national policy to maintain\nclose ties with Filipino migrant communities and promote their welfare as well as establish a\ndata bank in aid of national manpower policy formulation, an Office of Emigrant Affairs is\nhereby created in the Department of Labor. The Office shall be a unit at the Office of the\nSecretary and shall initially be manned and operated by such personnel and through such\nfunding as are available within the Department and its attached agencies. Thereafter, its\n\nappropriation shall be made part of the regular General Appropriations Decree.\n\n(b) The office shall, among others, promote the well-being of emigrants and maintain\ntheir close link to the homeland by:\n\n1)serving as a liaison with migrant communities;\n\n2)provision of welfare and cultural services;\n\n3)promote and facilitate re-integration of migrants into the national mainstream;\n\n4)promote economic, political and cultural ties with the communities; and\n\n5)generally to undertake such activities as may be appropriate to enhance such\ncooperative links.",
    "chunks": [
      "(a) Pursuant to the national policy to maintain\nclose ties with Filipino migrant communities and promote their welfare as well as establish a\ndata bank in aid of national manpower policy formulation, an Office of Emigrant Affairs is\nhereby created in the Department of Labor. The Office shall be a unit at the Office of the\nSecretary and shall initially be manned and operated by such personnel and through such\nfunding as are available within the Department and its attached agencies. Thereafter, its",
      "appropriation shall be made part of the regular General Appropriations Decree.",
      "(b) The office shall, among others, promote the well-being of emigrants and maintain\ntheir close link to the homeland by:",
      "1)serving as a liaison with migrant communities;",
      "2)provision of welfare and cultural services;",
      "3)promote and facilitate re-integration of migrants into the national mainstream;",
      "4)promote economic, political and cultural ties with the communities; and",
      "5)generally to undertake such activities as may be appropriate to enhance such\ncooperative links."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 20",
    "title": "National Seamen Board",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) A National Seamen Board is hereby created\nwhich shall develop and maintain a comprehensive program for Filipino seamen employed\noverseas. It shall have the power and duty:\n\n1.To provide free placement services for seamen;\n\n2.To regulate and supervise the activities of agents or representatives of shipping\ncompanies in the hiring of seamen for overseas employment and secure the best possible\nterms of employment for contract seamen workers and secure compliance therewith;\n\n3.To maintain a complete registry of all Filipino seamen.\n\n(b) The Board shall have original and exclusive jurisdiction over all matters or cases\nincluding money claims, involving employer-employee relations, arising out of or by virtue of\nany law or contracts involving Filipino seamen for overseas employment. The decisions of the\nBoard shall be appealable to the National Labor Relations Commission upon the same grounds\nprovided in Article 223 hereof. The decisions of the National Labor Relations Commission\nshall be final and unappealable.",
    "chunks": [
      "(a) A National Seamen Board is hereby created\nwhich shall develop and maintain a comprehensive program for Filipino seamen employed\noverseas. It shall have the power and duty:",
      "1.To provide free placement services for seamen;",
      "2.To regulate and supervise the activities of agents or representatives of shipping\ncompanies in the hiring of seamen for overseas employment and secure the best possible\nterms of employment for contract seamen workers and secure compliance therewith;",
      "3.To maintain a complete registry of all Filipino seamen.",
      "(b) The Board shall have original and exclusive jurisdiction over all matters or cases\nincluding money claims, involving employer-employee relations, arising out of or by virtue of\nany law or contracts involving Filipino seamen for overseas employment. The decisions of the\nBoard shall be appealable to the National Labor Relations Commission upon the same grounds\nprovided in Article 223 hereof. The decisions of the National Labor Relations Commission\nshall be final and unappealable."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 21",
    "title": "Foreign Service Role and Participation",
    "category": "Labor Law - Book 1",
    "simplified_text": "To provide ample protection to\nFilipino workers abroad, the labor attachés, the labor reporting officers duly designated by the\nSecretary of Labor and the Philippine diplomatic or consular officials concerned shall, even\nwithout prior instruction or advice from the home office, exercise the power and duty:\n\n(a) To provide all Filipino workers within their jurisdiction assistance on all matters\narising out of employment;\n\n(b) To insure that Filipino workers are not exploited or discriminated against;\n\n(c) To verify and certify as requisite to authentication that the terms and conditions of\nemployment in contracts involving Filipino workers are in accordance with the Labor Code and\nrules and regulations of the Overseas Employment Development Board and National Seamen\nBoard;\n\n(d) To make continuing studies or researches and recommendations on the various\naspects of the employment market within their jurisdiction;\n\n(e) To gather and analyze information on the employment situation and its probable\ntrends, and to make such information available; and\n\n(f) To perform such other duties as may be required of them from time to time.",
    "chunks": [
      "To provide ample protection to\nFilipino workers abroad, the labor attachés, the labor reporting officers duly designated by the\nSecretary of Labor and the Philippine diplomatic or consular officials concerned shall, even\nwithout prior instruction or advice from the home office, exercise the power and duty:",
      "(a) To provide all Filipino workers within their jurisdiction assistance on all matters\narising out of employment;",
      "(b) To insure that Filipino workers are not exploited or discriminated against;",
      "(c) To verify and certify as requisite to authentication that the terms and conditions of\nemployment in contracts involving Filipino workers are in accordance with the Labor Code and\nrules and regulations of the Overseas Employment Development Board and National Seamen\nBoard;",
      "(d) To make continuing studies or researches and recommendations on the various\naspects of the employment market within their jurisdiction;",
      "(e) To gather and analyze information on the employment situation and its probable\ntrends, and to make such information available; and",
      "(f) To perform such other duties as may be required of them from time to time."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 22",
    "title": "Mandatory Remittance of Foreign Exchange Earnings",
    "category": "Labor Law - Book 1",
    "simplified_text": "It shall be mandatory\nfor all Filipino workers abroad to remit a portion of their foreign exchange earnings to their\nfamilies, dependents, and/or beneficiaries in the country in accordance with rules and\nregulations prescribed by the Secretary of Labor.",
    "chunks": [
      "It shall be mandatory\nfor all Filipino workers abroad to remit a portion of their foreign exchange earnings to their\nfamilies, dependents, and/or beneficiaries in the country in accordance with rules and\nregulations prescribed by the Secretary of Labor."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 23",
    "title": "Composition of the Boards",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) The OEDB shall be composed of the Secretary\nof Labor and Employment as Chairman, the Undersecretary of Labor as Vice-Chairman, and a\nrepresentative each of the Department of Foreign Affairs, the Department of National\nDefense, the Central Bank, the Department of Education, Culture and Sports, the National\nManpower and Youth Council, the Bureau of Employment Services, a workers’ organization\nand an employers’ organization and the Executive Director of the OEDB as members.\n\n(b) The National Seamen Board shall be composed of the Secretary of Labor and\nEmployment as Chairman, the Undersecretary of Labor as Vice-Chairman, the Commandant\nof the Philippine Coast Guard, and a representative each of the Department of Foreign Affairs,\nthe Department of Education, Culture and Sports, the Central Bank, the Maritime Industry\nAuthority, the Bureau of Employment Services, a national shipping association and the\nExecutive Director of the NSB as members.\n\nThe members of the Boards shall receive allowances to be determined by the Board which\nshall not be more than P2,000.00 per month.\n\n(c) The Boards shall be attached to the Department of Labor for policy and program\ncoordination. They shall each be assisted by a Secretariat headed by an Executive Director who\nshall be a Filipino citizen with sufficient experience in manpower administration, including\noverseas employment activities. The Executive Director shall be appointed by the President of\nthe Philippines upon the recommendation of the Secretary of Labor and shall receive an\nannual salary as fixed by law. The Secretary of Labor shall appoint the other members of the\nSecretariat.\n\n(d) The Auditor General shall appoint his representative to the Boards to audit their\nrespective accounts in accordance with auditing laws and pertinent rules and regulations.",
    "chunks": [
      "(a) The OEDB shall be composed of the Secretary\nof Labor and Employment as Chairman, the Undersecretary of Labor as Vice-Chairman, and a\nrepresentative each of the Department of Foreign Affairs, the Department of National\nDefense, the Central Bank, the Department of Education, Culture and Sports, the National\nManpower and Youth Council, the Bureau of Employment Services, a workers’ organization\nand an employers’ organization and the Executive Director of the OEDB as members.",
      "(b) The National Seamen Board shall be composed of the Secretary of Labor and\nEmployment as Chairman, the Undersecretary of Labor as Vice-Chairman, the Commandant\nof the Philippine Coast Guard, and a representative each of the Department of Foreign Affairs,\nthe Department of Education, Culture and Sports, the Central Bank, the Maritime Industry\nAuthority, the Bureau of Employment Services, a national shipping association and the\nExecutive Director of the NSB as members.",
      "The members of the Boards shall receive allowances to be determined by the Board which\nshall not be more than P2,000.00 per month.",
      "(c) The Boards shall be attached to the Department of Labor for policy and program\ncoordination. They shall each be assisted by a Secretariat headed by an Executive Director who\nshall be a Filipino citizen with sufficient experience in manpower administration, including\noverseas employment activities. The Executive Director shall be appointed by the President of\nthe Philippines upon the recommendation of the Secretary of Labor and shall receive an\nannual salary as fixed by law. The Secretary of Labor shall appoint the other members of the\nSecretariat.",
      "(d) The Auditor General shall appoint his representative to the Boards to audit their\nrespective accounts in accordance with auditing laws and pertinent rules and regulations."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 24",
    "title": "Boards to Issue Rules and Collect Fees",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Boards shall issue appropriate\nrules and regulations to carry out their functions. They shall have the power to impose and\ncollect fees from employers concerned, which shall be deposited in the respective accounts of\nsaid Boards and be used by them exclusively to promote their objectives.",
    "chunks": [
      "The Boards shall issue appropriate\nrules and regulations to carry out their functions. They shall have the power to impose and\ncollect fees from employers concerned, which shall be deposited in the respective accounts of\nsaid Boards and be used by them exclusively to promote their objectives."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter I - GENERAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 25",
    "title": "Private Sector Participation in the Recruitment and Placement of Workers",
    "category": "Labor Law - Book 1",
    "simplified_text": "Pursuant to national development objectives and in order to harness and maximize the use of\nprivate sector resources and initiative in the development and implementation of a\ncomprehensive employment program, the private employment sector shall participate in the\nrecruitment and placement of workers, locally and overseas, under such guidelines, rules and\nregulations as may be issued by the Secretary of Labor.",
    "chunks": [
      "Pursuant to national development objectives and in order to harness and maximize the use of\nprivate sector resources and initiative in the development and implementation of a\ncomprehensive employment program, the private employment sector shall participate in the\nrecruitment and placement of workers, locally and overseas, under such guidelines, rules and\nregulations as may be issued by the Secretary of Labor."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 26",
    "title": "Travel Agencies Prohibited to Recruit",
    "category": "Labor Law - Book 1",
    "simplified_text": "Travel agencies and sales agencies of\nairline companies are prohibited from engaging in the business of recruitment and placement\nof workers for overseas employment whether for profit or not.",
    "chunks": [
      "Travel agencies and sales agencies of\nairline companies are prohibited from engaging in the business of recruitment and placement\nof workers for overseas employment whether for profit or not."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 27",
    "title": "Citizenship Requirement",
    "category": "Labor Law - Book 1",
    "simplified_text": "Only Filipino citizens or corporations, partnerships\nor entities at least seventy-five percent (75%) of the authorized and voting capital stock of\nwhich is owned and controlled by Filipino citizens shall be permitted to participate in the\nrecruitment and placement of workers, locally or overseas.",
    "chunks": [
      "Only Filipino citizens or corporations, partnerships\nor entities at least seventy-five percent (75%) of the authorized and voting capital stock of\nwhich is owned and controlled by Filipino citizens shall be permitted to participate in the\nrecruitment and placement of workers, locally or overseas."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 28",
    "title": "Capitalization",
    "category": "Labor Law - Book 1",
    "simplified_text": "All applicants for authority to hire or renewal of license to\nrecruit are required to have such substantial capitalization as determined by the Secretary of\nLabor.",
    "chunks": [
      "All applicants for authority to hire or renewal of license to\nrecruit are required to have such substantial capitalization as determined by the Secretary of\nLabor."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 29",
    "title": "Non-transferability of License or Authority",
    "category": "Labor Law - Book 1",
    "simplified_text": "No license or authority shall be\nused directly or indirectly by any person other than the one in whose favor it was issued or at\nany place other than that stated in the license or authority be transferred, conveyed or\nassigned to any other person or entity. Any transfer of business address, appointment or\ndesignation of any agent or representative including the establishment of additional offices\nanywhere shall be subject to the prior approval of the Department of Labor.",
    "chunks": [
      "No license or authority shall be\nused directly or indirectly by any person other than the one in whose favor it was issued or at\nany place other than that stated in the license or authority be transferred, conveyed or\nassigned to any other person or entity. Any transfer of business address, appointment or\ndesignation of any agent or representative including the establishment of additional offices\nanywhere shall be subject to the prior approval of the Department of Labor."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 30",
    "title": "Registration Fees",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Secretary of Labor shall promulgate a schedule of fees\nfor the registration of all applicants for license or authority.",
    "chunks": [
      "The Secretary of Labor shall promulgate a schedule of fees\nfor the registration of all applicants for license or authority."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 31",
    "title": "Bonds",
    "category": "Labor Law - Book 1",
    "simplified_text": "All applicants for license or authority shall post such cash and surety\nbonds as determined by the Secretary of Labor to guarantee compliance with prescribed\nrecruitment procedures, rules and regulations, and terms and conditions of employment as\nmay be appropriate.",
    "chunks": [
      "All applicants for license or authority shall post such cash and surety\nbonds as determined by the Secretary of Labor to guarantee compliance with prescribed\nrecruitment procedures, rules and regulations, and terms and conditions of employment as\nmay be appropriate."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 32",
    "title": "Fees to be Paid by Workers",
    "category": "Labor Law - Book 1",
    "simplified_text": "Any person applying with a private fee-charging\nemployment agency for employment assistance shall not be charged any fee until he has\nobtained employment through its efforts or has actually commenced employment. Such fee\nshall be always covered with the appropriate receipt clearly showing the amount paid. The\nSecretary of Labor shall promulgate a schedule of allowable fees.",
    "chunks": [
      "Any person applying with a private fee-charging\nemployment agency for employment assistance shall not be charged any fee until he has\nobtained employment through its efforts or has actually commenced employment. Such fee\nshall be always covered with the appropriate receipt clearly showing the amount paid. The\nSecretary of Labor shall promulgate a schedule of allowable fees."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 33",
    "title": "Reports on Employment Status",
    "category": "Labor Law - Book 1",
    "simplified_text": "Whenever the public interest requires, the\nSecretary of Labor may direct all persons or entities within the coverage of this Title to submit\na report on the status of employment, including job vacancies, details of job requisitions,\nseparation from jobs, wages, other terms and conditions and other employment data.",
    "chunks": [
      "Whenever the public interest requires, the\nSecretary of Labor may direct all persons or entities within the coverage of this Title to submit\na report on the status of employment, including job vacancies, details of job requisitions,\nseparation from jobs, wages, other terms and conditions and other employment data."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 34",
    "title": "Prohibited Practices",
    "category": "Labor Law - Book 1",
    "simplified_text": "It shall be unlawful for any individual, entity, licensee,\nor holder of authority:\n\n(a) To charge or accept, directly or indirectly, any amount greater than that specified in\nthe schedule of allowable fees prescribed by the Secretary of Labor, or to make a worker pay\nany amount greater than that actually received by him as a loan or advance;\n\n(b) To furnish or publish any false notice or information or document in relation to\nrecruitment or employment;\n\n(c) To give any false notice, testimony, information or document or commit any act of\nmisrepresentation for the purpose of securing a license or authority under this Code;\n\n(d) To induce or attempt to induce a worker already employed to quit his employment\nin order to offer him to another unless the transfer is designed to liberate the worker from\noppressive terms and conditions of employment;\n\n(e) To influence or to attempt to influence any person or entity not to employ any\nworker who has not applied for employment through his agency;\n\n(f) To engage in the recruitment or placement of workers in jobs harmful to public\nhealth or morality or to the dignity of the Republic of the Philippines;\n\n(g) To obstruct or attempt to obstruct inspection by the Secretary of Labor or by his duly\nauthorized representatives;\n\n(h) To fail to file reports on the status of employment, placement vacancies, remittance\nof foreign exchange earnings, separation from jobs, departures and such other matters or\ninformation as may be required by the Secretary of Labor;\n\n(i) To substitute or alter employment contracts approved and verified by the\nDepartment of Labor from the time of actual signing thereof by the parties up to and including\nthe periods of expiration of the same without the approval of the Secretary of Labor;\n\n(j) To become an officer or member of the Board of any corporation engaged in travel\nagency or to be engaged directly or indirectly in the management of a travel agency; and\n\n(k) To withhold or deny travel documents from applicant workers before departure for\nmonetary or financial considerations other than those authorized under this Code and its\nimplementing rules and regulations.",
    "chunks": [
      "It shall be unlawful for any individual, entity, licensee,\nor holder of authority:",
      "(a) To charge or accept, directly or indirectly, any amount greater than that specified in\nthe schedule of allowable fees prescribed by the Secretary of Labor, or to make a worker pay\nany amount greater than that actually received by him as a loan or advance;",
      "(b) To furnish or publish any false notice or information or document in relation to\nrecruitment or employment;",
      "(c) To give any false notice, testimony, information or document or commit any act of\nmisrepresentation for the purpose of securing a license or authority under this Code;",
      "(d) To induce or attempt to induce a worker already employed to quit his employment\nin order to offer him to another unless the transfer is designed to liberate the worker from\noppressive terms and conditions of employment;",
      "(e) To influence or to attempt to influence any person or entity not to employ any\nworker who has not applied for employment through his agency;",
      "(f) To engage in the recruitment or placement of workers in jobs harmful to public\nhealth or morality or to the dignity of the Republic of the Philippines;",
      "(g) To obstruct or attempt to obstruct inspection by the Secretary of Labor or by his duly\nauthorized representatives;",
      "(h) To fail to file reports on the status of employment, placement vacancies, remittance\nof foreign exchange earnings, separation from jobs, departures and such other matters or\ninformation as may be required by the Secretary of Labor;",
      "(i) To substitute or alter employment contracts approved and verified by the\nDepartment of Labor from the time of actual signing thereof by the parties up to and including\nthe periods of expiration of the same without the approval of the Secretary of Labor;",
      "(j) To become an officer or member of the Board of any corporation engaged in travel\nagency or to be engaged directly or indirectly in the management of a travel agency; and",
      "(k) To withhold or deny travel documents from applicant workers before departure for\nmonetary or financial considerations other than those authorized under this Code and its\nimplementing rules and regulations."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 35",
    "title": "Suspension and/or Cancellation of License or Authority",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Minister of\nLabor shall have the power to suspend or cancel any license or authority to recruit employees\nfor overseas employment for violation of rules and regulations issued by the Ministry of Labor,\nthe Overseas Employment Development Board, or for violation of the provisions of this and\nother applicable laws, General Orders and Letters of Instructions.",
    "chunks": [
      "The Minister of\nLabor shall have the power to suspend or cancel any license or authority to recruit employees\nfor overseas employment for violation of rules and regulations issued by the Ministry of Labor,\nthe Overseas Employment Development Board, or for violation of the provisions of this and\nother applicable laws, General Orders and Letters of Instructions."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter II - REGULATION OF RECRUITMENT AND PLACEMENT ACTIVITIES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 36",
    "title": "Regulatory Power",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Secretary of Labor shall have the power to restrict\nand regulate the recruitment and placement activities of all agencies within the coverage of\nthis Title and is hereby authorized to issue orders and promulgate rules and regulations to\ncarry out the objectives and implement the provisions of this Title.",
    "chunks": [
      "The Secretary of Labor shall have the power to restrict\nand regulate the recruitment and placement activities of all agencies within the coverage of\nthis Title and is hereby authorized to issue orders and promulgate rules and regulations to\ncarry out the objectives and implement the provisions of this Title."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter III - MISCELLANEOUS PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 37",
    "title": "Visitorial Power",
    "category": "Labor Law - Book 1",
    "simplified_text": "The Secretary of Labor or his duly authorized\nrepresentatives may, at any time, inspect the premises, books of accounts and records of any\nperson or entity covered by this Title, require it to submit reports regularly on prescribed\nforms, and act on violation of any provisions of this Title.",
    "chunks": [
      "The Secretary of Labor or his duly authorized\nrepresentatives may, at any time, inspect the premises, books of accounts and records of any\nperson or entity covered by this Title, require it to submit reports regularly on prescribed\nforms, and act on violation of any provisions of this Title."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter III - MISCELLANEOUS PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 38",
    "title": "Illegal Recruitment",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) Any recruitment activities, including the prohibited\npractices enumerated under Article 34 of this Code, to be undertaken by non-licensees or non-\nholders of authority, shall be deemed illegal and punishable under Article 39 of this Code. The\nDepartment of Labor and Employment or any law enforcement officer may initiate complaints\nunder this Article.\n\n(b) Illegal recruitment when committed by a syndicate or in large scale shall be considered\nan offense involving economic sabotage and shall be penalized in accordance with Article 39\nhereof.\n\nIllegal recruitment is deemed committed by a syndicate if carried out by a group of three\n(3) or more persons conspiring and/or confederating with one another in carrying out any\nunlawful or illegal transaction, enterprise or scheme defined under the first paragraph hereof.\nIllegal recruitment is deemed committed in large scale if committed against three (3) or more\npersons individually or as a group.\n\n[(c) The Secretary of Labor and Employment or his duly authorized representatives shall\nhave the power to cause the arrest and detention of such non-licensee or non-holder of\nauthority if after investigation it is determined that his activities constitute a danger to national\nsecurity and public order or will lead to further exploitation of job-seekers. The Secretary shall\norder the search of the office or premises and seizure of documents, paraphernalia, properties\nand other implements used in illegal recruitment activities and the closure of companies,\nestablishments and entities found to be engaged in the recruitment of workers for overseas\nemployment, without having been licensed or authorized to do so.]",
    "chunks": [
      "(a) Any recruitment activities, including the prohibited\npractices enumerated under Article 34 of this Code, to be undertaken by non-licensees or non-\nholders of authority, shall be deemed illegal and punishable under Article 39 of this Code. The\nDepartment of Labor and Employment or any law enforcement officer may initiate complaints\nunder this Article.",
      "(b) Illegal recruitment when committed by a syndicate or in large scale shall be considered\nan offense involving economic sabotage and shall be penalized in accordance with Article 39\nhereof.",
      "Illegal recruitment is deemed committed by a syndicate if carried out by a group of three\n(3) or more persons conspiring and/or confederating with one another in carrying out any\nunlawful or illegal transaction, enterprise or scheme defined under the first paragraph hereof.\nIllegal recruitment is deemed committed in large scale if committed against three (3) or more\npersons individually or as a group.",
      "[(c) The Secretary of Labor and Employment or his duly authorized representatives shall\nhave the power to cause the arrest and detention of such non-licensee or non-holder of\nauthority if after investigation it is determined that his activities constitute a danger to national\nsecurity and public order or will lead to further exploitation of job-seekers. The Secretary shall\norder the search of the office or premises and seizure of documents, paraphernalia, properties\nand other implements used in illegal recruitment activities and the closure of companies,\nestablishments and entities found to be engaged in the recruitment of workers for overseas\nemployment, without having been licensed or authorized to do so.]"
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter III - MISCELLANEOUS PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 39",
    "title": "Penalties",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) The penalty of life imprisonment and a fine of One Hundred\nThousand Pesos (P100,000.00) shall be imposed if illegal recruitment constitutes economic\nsabotage as defined herein;\n\n(b) Any licensee or holder of authority found violating or causing another to violate any\nprovision of this Title or its implementing rules and regulations shall, upon conviction thereof,\nsuffer the penalty of imprisonment of not less than two years nor more than five years or a\nfine of not less than P10,000 nor more than P50,000, or both such imprisonment and fine, at\nthe discretion of the court;\n\n(c) Any person who is neither a licensee nor a holder of authority under this Title found\nviolating any provision thereof or its implementing rules and regulations shall, upon conviction\nthereof, suffer the penalty of imprisonment of not less than four years nor more than eight\nyears or a fine of not less than P20,000 nor more than P100,000 or both such imprisonment\nand fine, at the discretion of the court;\n\n(d) If the offender is a corporation, partnership, association or entity, the penalty shall be\nimposed upon the officer or officers of the corporation, partnership, association or entity\nresponsible for violation; and if such officer is an alien, he shall, in addition to the penalties\nherein prescribed, be deported without further proceedings;\n\n(e) In every case, conviction shall cause and carry the automatic revocation of the license\nor authority and all the permits and privileges granted to such person or entity under this Title,\nand the forfeiture of the cash and surety bonds in favor of the Overseas Employment\nDevelopment Board or the National Seamen Board, as the case may be, both of which are\nauthorized to use the same exclusively to promote their objectives.",
    "chunks": [
      "(a) The penalty of life imprisonment and a fine of One Hundred\nThousand Pesos (P100,000.00) shall be imposed if illegal recruitment constitutes economic\nsabotage as defined herein;",
      "(b) Any licensee or holder of authority found violating or causing another to violate any\nprovision of this Title or its implementing rules and regulations shall, upon conviction thereof,\nsuffer the penalty of imprisonment of not less than two years nor more than five years or a\nfine of not less than P10,000 nor more than P50,000, or both such imprisonment and fine, at\nthe discretion of the court;",
      "(c) Any person who is neither a licensee nor a holder of authority under this Title found\nviolating any provision thereof or its implementing rules and regulations shall, upon conviction\nthereof, suffer the penalty of imprisonment of not less than four years nor more than eight\nyears or a fine of not less than P20,000 nor more than P100,000 or both such imprisonment\nand fine, at the discretion of the court;",
      "(d) If the offender is a corporation, partnership, association or entity, the penalty shall be\nimposed upon the officer or officers of the corporation, partnership, association or entity\nresponsible for violation; and if such officer is an alien, he shall, in addition to the penalties\nherein prescribed, be deported without further proceedings;",
      "(e) In every case, conviction shall cause and carry the automatic revocation of the license\nor authority and all the permits and privileges granted to such person or entity under this Title,\nand the forfeiture of the cash and surety bonds in favor of the Overseas Employment\nDevelopment Board or the National Seamen Board, as the case may be, both of which are\nauthorized to use the same exclusively to promote their objectives."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title I - RECRUITMENT AND PLACEMENT OF WORKERS",
      "Chapter III - MISCELLANEOUS PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 40",
    "title": "Employment Permit of Non-resident Aliens",
    "category": "Labor Law - Book 1",
    "simplified_text": "Any alien seeking admission to\nthe Philippines for employment purposes and any domestic or foreign employer who desires\nto engage an alien for employment in the Philippines shall obtain an employment permit from\nthe Department of Labor.\n\nThe employment permit may be issued to a non-resident alien or to the applicant\nemployer after a determination of the non-availability of a person in the Philippines who is\ncompetent, able and willing at the time of application to perform the services for which the\nalien is desired.\n\nFor an enterprise registered in preferred areas of investments, said employment permit\nmay be issued upon recommendation of the government agency charged with the supervision\nof said registered enterprise.",
    "chunks": [
      "Any alien seeking admission to\nthe Philippines for employment purposes and any domestic or foreign employer who desires\nto engage an alien for employment in the Philippines shall obtain an employment permit from\nthe Department of Labor.",
      "The employment permit may be issued to a non-resident alien or to the applicant\nemployer after a determination of the non-availability of a person in the Philippines who is\ncompetent, able and willing at the time of application to perform the services for which the\nalien is desired.",
      "For an enterprise registered in preferred areas of investments, said employment permit\nmay be issued upon recommendation of the government agency charged with the supervision\nof said registered enterprise."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title II - EMPLOYMENT OF NON-RESIDENT ALIENS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 41",
    "title": "Prohibition Against Transfer of Employment",
    "category": "Labor Law - Book 1",
    "simplified_text": "(a) After the issuance of an\nemployment permit, the alien shall not transfer to another job or change his employer without\nprior approval of the Secretary of Labor.\n\n(b) Any non-resident alien who shall take up employment in violation of the provision of\nthis Title and its implementing rules and regulations shall be punished in accordance with the\nprovisions of Articles 289 and 290 of the Labor Code.\n\nIn addition, the alien worker shall be subject to deportation after service of his sentence.",
    "chunks": [
      "(a) After the issuance of an\nemployment permit, the alien shall not transfer to another job or change his employer without\nprior approval of the Secretary of Labor.",
      "(b) Any non-resident alien who shall take up employment in violation of the provision of\nthis Title and its implementing rules and regulations shall be punished in accordance with the\nprovisions of Articles 289 and 290 of the Labor Code.",
      "In addition, the alien worker shall be subject to deportation after service of his sentence."
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title II - EMPLOYMENT OF NON-RESIDENT ALIENS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 42",
    "title": "Submission of List",
    "category": "Labor Law - Book 1",
    "simplified_text": "Any employer employing non-resident foreign nationals on\nthe effective date of this Code shall submit a list of such nationals to the Secretary of Labor\nwithin thirty (30) days after such date indicating their names, citizenship, foreign and local\naddresses, nature of employment and status of stay in the country. The Secretary of Labor\nshall then determine if they are entitled to an employment permit.\n\nPROGRAM",
    "chunks": [
      "Any employer employing non-resident foreign nationals on\nthe effective date of this Code shall submit a list of such nationals to the Secretary of Labor\nwithin thirty (30) days after such date indicating their names, citizenship, foreign and local\naddresses, nature of employment and status of stay in the country. The Secretary of Labor\nshall then determine if they are entitled to an employment permit.",
      "PROGRAM"
    ],
    "tags": [
      "Book One - PRE-EMPLOYMENT",
      "Title II - EMPLOYMENT OF NON-RESIDENT ALIENS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 43",
    "title": "Statement of Objective",
    "category": "Labor Law - Book 2",
    "simplified_text": "It is the objective of this Title to develop human\nresources, establish training institutions, and formulate such plans and programs as will ensure\nefficient allocation, development and utilization of the nation’s manpower and thereby\npromote employment and accelerate economic and social growth.",
    "chunks": [
      "It is the objective of this Title to develop human\nresources, establish training institutions, and formulate such plans and programs as will ensure\nefficient allocation, development and utilization of the nation’s manpower and thereby\npromote employment and accelerate economic and social growth."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 44",
    "title": "Definitions",
    "category": "Labor Law - Book 2",
    "simplified_text": "As used in this Title:\n\n(a) \"Manpower\" shall mean that portion of the nation’s population which has actual or\npotential capability to contribute directly to the production of goods and services.\n\n(b) \"Entrepreneurship\" shall mean training for self-employment or assisting individual or\nsmall industries within the purview of this Title.",
    "chunks": [
      "As used in this Title:",
      "(a) \"Manpower\" shall mean that portion of the nation’s population which has actual or\npotential capability to contribute directly to the production of goods and services.",
      "(b) \"Entrepreneurship\" shall mean training for self-employment or assisting individual or\nsmall industries within the purview of this Title."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 45",
    "title": "National Manpower and Youth Council; Composition",
    "category": "Labor Law - Book 2",
    "simplified_text": "To carry out the\nobjectives of this Title, the National Manpower and Youth Council, which is attached to the\nDepartment of Labor for policy and program coordination and hereinafter referred to as the\nCouncil, shall be composed of the Secretary of Labor as ex-officio chairman, the Secretary of\nEducation and Culture as ex-officio vice-chairman, and as ex-officio members, the Secretary of\nEconomic Planning, the Secretary of Natural Resources, the Chairman of the Civil Service\nCommission, the Secretary of Social Welfare, the Secretary of Local Government, the Secretary\nof Science and Technology, the Secretary of Trade and Industry and the Director-General of\nthe Council. The Director General shall have no vote.\n\nIn addition, the President shall appoint the following members from the private sector:\ntwo (2) representatives of national organizations of employers; two (2) representatives of\nnational workers’ organizations; and one representative of national family and youth\norganizations, each for a term of three (3) years.",
    "chunks": [
      "To carry out the\nobjectives of this Title, the National Manpower and Youth Council, which is attached to the\nDepartment of Labor for policy and program coordination and hereinafter referred to as the\nCouncil, shall be composed of the Secretary of Labor as ex-officio chairman, the Secretary of\nEducation and Culture as ex-officio vice-chairman, and as ex-officio members, the Secretary of\nEconomic Planning, the Secretary of Natural Resources, the Chairman of the Civil Service\nCommission, the Secretary of Social Welfare, the Secretary of Local Government, the Secretary\nof Science and Technology, the Secretary of Trade and Industry and the Director-General of\nthe Council. The Director General shall have no vote.",
      "In addition, the President shall appoint the following members from the private sector:\ntwo (2) representatives of national organizations of employers; two (2) representatives of\nnational workers’ organizations; and one representative of national family and youth\norganizations, each for a term of three (3) years."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 46",
    "title": "National Manpower Plan",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall formulate a long-term national\nmanpower plan for the optimum allocation, development and utilization of manpower for\nemployment, entrepreneurship and economic and social growth. This manpower plan shall,\nafter adoption by the Council, be updated annually and submitted to the President for his\napproval. Thereafter, it shall be the controlling plan for the development of manpower\nresources for the entire country in accordance with the national development plan. The\nCouncil shall call upon any agency of the Government or the private sector to assist in this\neffort.",
    "chunks": [
      "The Council shall formulate a long-term national\nmanpower plan for the optimum allocation, development and utilization of manpower for\nemployment, entrepreneurship and economic and social growth. This manpower plan shall,\nafter adoption by the Council, be updated annually and submitted to the President for his\napproval. Thereafter, it shall be the controlling plan for the development of manpower\nresources for the entire country in accordance with the national development plan. The\nCouncil shall call upon any agency of the Government or the private sector to assist in this\neffort."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 47",
    "title": "National Manpower Skills Center",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall establish a National\nManpower Skills Center and regional and local training centers for the purpose of promoting\nthe development of skills. The centers shall be administered and operated under such rules\nand regulations as may be established by the Council.",
    "chunks": [
      "The Council shall establish a National\nManpower Skills Center and regional and local training centers for the purpose of promoting\nthe development of skills. The centers shall be administered and operated under such rules\nand regulations as may be established by the Council."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 48",
    "title": "Establishment and Formulation of Skills Standards",
    "category": "Labor Law - Book 2",
    "simplified_text": "There shall be national\nskills standards for industry trades to be established by the Council in consultation with\nemployers’ and workers’ organizations and appropriate government authorities. The Council\nshall thereafter administer the national skills standards.",
    "chunks": [
      "There shall be national\nskills standards for industry trades to be established by the Council in consultation with\nemployers’ and workers’ organizations and appropriate government authorities. The Council\nshall thereafter administer the national skills standards."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 49",
    "title": "Administration of Training Programs",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall provide, through the\nSecretariat, instructor training, entrepreneurship development, training in vocations, trades\nand other fields of employment, and assist any employer or organization in training schemes\ndesigned to attain its objectives under rules and regulations which the Council shall establish\nfor this purpose.\n\nThe Council shall exercise, through the Secretariat, authority and jurisdiction over, and\nadminister, on-going technical assistance programs and/or grants-in-aid for manpower and\nyouth development including those which may be entered into between the Government of\nthe Philippines and international and foreign organizations and nations, as well as persons and\norganizations in the Philippines.\n\nIn order to integrate the national manpower development efforts, all manpower training\nschemes as provided for in this Code shall be coordinated with the Council, particularly those\nhaving to do with the setting of skills standards. For this purpose, existing manpower training\nprograms in the government and in the private sector shall be reported to the Council which\nmay regulate such programs to make them conform with national development programs.\n\nThis Article shall not include apprentices, learners and handicapped workers as\ngoverned by appropriate provisions of this Code.",
    "chunks": [
      "The Council shall provide, through the\nSecretariat, instructor training, entrepreneurship development, training in vocations, trades\nand other fields of employment, and assist any employer or organization in training schemes\ndesigned to attain its objectives under rules and regulations which the Council shall establish\nfor this purpose.",
      "The Council shall exercise, through the Secretariat, authority and jurisdiction over, and\nadminister, on-going technical assistance programs and/or grants-in-aid for manpower and\nyouth development including those which may be entered into between the Government of\nthe Philippines and international and foreign organizations and nations, as well as persons and\norganizations in the Philippines.",
      "In order to integrate the national manpower development efforts, all manpower training\nschemes as provided for in this Code shall be coordinated with the Council, particularly those\nhaving to do with the setting of skills standards. For this purpose, existing manpower training\nprograms in the government and in the private sector shall be reported to the Council which\nmay regulate such programs to make them conform with national development programs.",
      "This Article shall not include apprentices, learners and handicapped workers as\ngoverned by appropriate provisions of this Code."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 50",
    "title": "Industry Boards",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall establish industry boards to assist in the\nestablishment of manpower development schemes, trades and skills standards and such other\nfunctions as will provide direct participation of employers and workers in the fulfillment of the\nCouncil’s objectives, in accordance with guidelines to be established by the Council and in\nconsultation with the National Economic and Development Authority.\n\nThe maintenance and operations of the industry boards shall be financed through a\nfunding scheme under such rates of fees and manners of collection and disbursements as may\nbe determined by the Council.",
    "chunks": [
      "The Council shall establish industry boards to assist in the\nestablishment of manpower development schemes, trades and skills standards and such other\nfunctions as will provide direct participation of employers and workers in the fulfillment of the\nCouncil’s objectives, in accordance with guidelines to be established by the Council and in\nconsultation with the National Economic and Development Authority.",
      "The maintenance and operations of the industry boards shall be financed through a\nfunding scheme under such rates of fees and manners of collection and disbursements as may\nbe determined by the Council."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 51",
    "title": "Employment Service Training Functions",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall utilize the\nemployment service of the Department of Labor for the placement of its graduates. The\nBureau of Employment Services shall render assistance to the Council in the measurement of\nunemployment and underemployment, conduct of local manpower resource surveys and\noccupational studies including an inventory of the labor force, establishment and maintenance\nwithout charge of a national register of technicians who have successfully completed a training\nprogram under this Act, and skilled manpower including its publication, maintenance of an\nadequate and up-to-date system of employment information.",
    "chunks": [
      "The Council shall utilize the\nemployment service of the Department of Labor for the placement of its graduates. The\nBureau of Employment Services shall render assistance to the Council in the measurement of\nunemployment and underemployment, conduct of local manpower resource surveys and\noccupational studies including an inventory of the labor force, establishment and maintenance\nwithout charge of a national register of technicians who have successfully completed a training\nprogram under this Act, and skilled manpower including its publication, maintenance of an\nadequate and up-to-date system of employment information."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 52",
    "title": "Incentive Scheme",
    "category": "Labor Law - Book 2",
    "simplified_text": "An additional deduction from taxable income of one-half\n(1/2) of the value of labor training expenses incurred for development programs shall be\ngranted to the person or enterprise concerned provided that such development programs,\nother than apprenticeship, are approved by the Council and the deduction does not exceed\nten percent (10%) of the direct labor wage.\n\nThere shall be a review of the said scheme two years after its implementation.",
    "chunks": [
      "An additional deduction from taxable income of one-half\n(1/2) of the value of labor training expenses incurred for development programs shall be\ngranted to the person or enterprise concerned provided that such development programs,\nother than apprenticeship, are approved by the Council and the deduction does not exceed\nten percent (10%) of the direct labor wage.",
      "There shall be a review of the said scheme two years after its implementation."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 53",
    "title": "Council Secretariat",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall have a Secretariat headed by a Director-\nGeneral who shall be assisted by a Deputy Director-General, both of whom shall be career\nadministrators appointed by the President of the Philippines on recommendation of the\nSecretary of Labor. The Secretariat shall be under the administrative supervision of the\nSecretary of Labor and shall have an Office of Manpower Planning and Development, an Office\nof Vocational Preparation, a National Manpower Skills Center, regional manpower\ndevelopment offices and such other offices as may be necessary.\n\nThe Director-General shall have the rank and emoluments of an undersecretary and shall\nserve for a term of ten (10) years. The Executive-Directors of the Office of Manpower Planning\nand Development, the Office of Vocational Preparation and the National Manpower Skills\nCenter shall have the rank and emoluments of a bureau director and shall be subject to Civil\nService Law, rules and regulations. The Director-General, Deputy Director-General and\nExecutive Directors shall be natural-born citizens, between thirty and fifty years of age at the\ntime of appointment, with a master’s degree or its equivalent, and experience in national\nplanning and development of human resources. The Executive Director of the National\nManpower Skills Center shall, in addition to the foregoing qualifications, have undergone\ntraining in center management. Executive Directors shall be appointed by the President on the\nrecommendations of the Secretary of Labor and Employment.\n\nThe Director-General shall appoint such personnel necessary to carry out the objectives,\npolicies and functions of the Council subject to Civil Service rules. The regular professional and\ntechnical personnel shall be exempt from WAPCO rules and regulations.\n\nThe Secretariat shall have the following functions and responsibilities:\n\n1.To prepare and recommend the manpower plan for approval by the Council;\n\n2.To recommend allocation of resources for the implementation of the manpower plan\nas approved by the Council;\n\n3.To carry out the manpower plan as the implementing arm of the Council;\n\n4.To effect the efficient performance of the functions of the Council and the\nachievement of the objectives of this Title;\n\n5.To determine specific allocation of resources for the projects to be undertaken\npursuant to approved manpower plans;\n\n6.To submit to the Council periodic reports on progress and accomplishment of work\nprograms;\n\n7.To prepare for approval by the Council an annual report to the President on plans,\nprograms and projects on manpower and out-of-school youth development;\n\n8.To enter into agreements to implement approved plans and programs and perform\nany and all such acts as will fulfill the objectives of this Code as well as ensure the efficient\nperformance of the functions of the Council; and\n\n9.To perform such other functions as may be authorized by the Council.",
    "chunks": [
      "The Council shall have a Secretariat headed by a Director-\nGeneral who shall be assisted by a Deputy Director-General, both of whom shall be career\nadministrators appointed by the President of the Philippines on recommendation of the\nSecretary of Labor. The Secretariat shall be under the administrative supervision of the\nSecretary of Labor and shall have an Office of Manpower Planning and Development, an Office\nof Vocational Preparation, a National Manpower Skills Center, regional manpower\ndevelopment offices and such other offices as may be necessary.",
      "The Director-General shall have the rank and emoluments of an undersecretary and shall\nserve for a term of ten (10) years. The Executive-Directors of the Office of Manpower Planning\nand Development, the Office of Vocational Preparation and the National Manpower Skills\nCenter shall have the rank and emoluments of a bureau director and shall be subject to Civil\nService Law, rules and regulations. The Director-General, Deputy Director-General and\nExecutive Directors shall be natural-born citizens, between thirty and fifty years of age at the\ntime of appointment, with a master’s degree or its equivalent, and experience in national\nplanning and development of human resources. The Executive Director of the National\nManpower Skills Center shall, in addition to the foregoing qualifications, have undergone\ntraining in center management. Executive Directors shall be appointed by the President on the\nrecommendations of the Secretary of Labor and Employment.",
      "The Director-General shall appoint such personnel necessary to carry out the objectives,\npolicies and functions of the Council subject to Civil Service rules. The regular professional and\ntechnical personnel shall be exempt from WAPCO rules and regulations.",
      "The Secretariat shall have the following functions and responsibilities:",
      "1.To prepare and recommend the manpower plan for approval by the Council;",
      "2.To recommend allocation of resources for the implementation of the manpower plan\nas approved by the Council;",
      "3.To carry out the manpower plan as the implementing arm of the Council;",
      "4.To effect the efficient performance of the functions of the Council and the\nachievement of the objectives of this Title;",
      "5.To determine specific allocation of resources for the projects to be undertaken\npursuant to approved manpower plans;",
      "6.To submit to the Council periodic reports on progress and accomplishment of work\nprograms;",
      "7.To prepare for approval by the Council an annual report to the President on plans,\nprograms and projects on manpower and out-of-school youth development;",
      "8.To enter into agreements to implement approved plans and programs and perform\nany and all such acts as will fulfill the objectives of this Code as well as ensure the efficient\nperformance of the functions of the Council; and",
      "9.To perform such other functions as may be authorized by the Council."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 54",
    "title": "Regional Manpower Development Offices",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall create regional\nmanpower development offices which shall determine the manpower needs of the industry,\nagriculture and other sectors of the economy within their respective jurisdictions; provide the\nCouncil’s central planners with the data for updating the national manpower plan; recommend\nprograms for the regional level agencies engaged in manpower and youth development within\nthe policies formulated by the Council; and administer and supervise Secretariat training\nprograms within the region and perform such other functions as may be authorized by the\nCouncil.",
    "chunks": [
      "The Council shall create regional\nmanpower development offices which shall determine the manpower needs of the industry,\nagriculture and other sectors of the economy within their respective jurisdictions; provide the\nCouncil’s central planners with the data for updating the national manpower plan; recommend\nprograms for the regional level agencies engaged in manpower and youth development within\nthe policies formulated by the Council; and administer and supervise Secretariat training\nprograms within the region and perform such other functions as may be authorized by the\nCouncil."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 55",
    "title": "Consultants and Technical Assistance, Publication, and Research",
    "category": "Labor Law - Book 2",
    "simplified_text": "In pursuing\nits objectives, the Council is authorized to set aside a portion of its appropriation for the hiring\nof the services of qualified consultants, and/or private organizations for research work and\npublication. It shall avail itself of the services of the Government as may be required.",
    "chunks": [
      "In pursuing\nits objectives, the Council is authorized to set aside a portion of its appropriation for the hiring\nof the services of qualified consultants, and/or private organizations for research work and\npublication. It shall avail itself of the services of the Government as may be required."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 56",
    "title": "Rules and Regulations",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Council shall define its broad functions and issue\nappropriate rules and regulations necessary to implement the provision of this Code.",
    "chunks": [
      "The Council shall define its broad functions and issue\nappropriate rules and regulations necessary to implement the provision of this Code."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title I - NATIONAL MANPOWER DEVELOPMENT",
      "Chapter I - NATIONAL POLICIES AND ADMINISTRATIVE MACHINERY FOR THEIR IMPLEMENTATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 57",
    "title": "Statement of Objectives",
    "category": "Labor Law - Book 2",
    "simplified_text": "This Title aims:\n\n1.To help meet the demand of the economy for trained manpower;\n\n2.To establish a national apprenticeship program through the participation of\nemployers, workers and government and non-government agencies; and\n\n3.To establish apprenticeship standards for the protection of apprentices.",
    "chunks": [
      "This Title aims:",
      "1.To help meet the demand of the economy for trained manpower;",
      "2.To establish a national apprenticeship program through the participation of\nemployers, workers and government and non-government agencies; and",
      "3.To establish apprenticeship standards for the protection of apprentices."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 58",
    "title": "Definition of Terms",
    "category": "Labor Law - Book 2",
    "simplified_text": "As used in this Title:\n\n(a)\"Apprenticeship\" means practical training on the job supplemented by related\ntheoretical instruction.\n\n(b) An \"apprentice\" is a worker who is covered by a written apprenticeship agreement\nwith an individual employer or any of the entities recognized under this Chapter.\n\n(c) An \"apprenticeable occupation\" means any trade, form of employment or\noccupation which requires more than three (3) months of practical training on the job\nsupplemented by related theoretical instruction.\n\n(d)\"Apprenticeship agreement\" is an employment contract wherein the employer binds\nhimself to train the apprentice and the apprentice in turn accepts the terms of training.",
    "chunks": [
      "As used in this Title:",
      "(a)\"Apprenticeship\" means practical training on the job supplemented by related\ntheoretical instruction.",
      "(b) An \"apprentice\" is a worker who is covered by a written apprenticeship agreement\nwith an individual employer or any of the entities recognized under this Chapter.",
      "(c) An \"apprenticeable occupation\" means any trade, form of employment or\noccupation which requires more than three (3) months of practical training on the job\nsupplemented by related theoretical instruction.",
      "(d)\"Apprenticeship agreement\" is an employment contract wherein the employer binds\nhimself to train the apprentice and the apprentice in turn accepts the terms of training."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 59",
    "title": "Qualifications of Apprentice",
    "category": "Labor Law - Book 2",
    "simplified_text": "To qualify as an apprentice, a person shall:\n\n(a) Be at least fourteen (14) years of age;\n\n(b) Possess vocational aptitude and capacity for appropriate tests; and\n\n(c) Possess the ability to comprehend and follow oral and written instructions.\n\nTrade and industry associations may recommend to the Secretary of Labor appropriate\neducational requirements for different occupations.",
    "chunks": [
      "To qualify as an apprentice, a person shall:",
      "(a) Be at least fourteen (14) years of age;",
      "(b) Possess vocational aptitude and capacity for appropriate tests; and",
      "(c) Possess the ability to comprehend and follow oral and written instructions.",
      "Trade and industry associations may recommend to the Secretary of Labor appropriate\neducational requirements for different occupations."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 60",
    "title": "Employment of Apprentices",
    "category": "Labor Law - Book 2",
    "simplified_text": "Only employers in the highly technical\nindustries may employ apprentices and only in apprenticeable occupations approved by the\nMinister of Labor and Employment.",
    "chunks": [
      "Only employers in the highly technical\nindustries may employ apprentices and only in apprenticeable occupations approved by the\nMinister of Labor and Employment."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 61",
    "title": "Contents of Apprenticeship Agreements",
    "category": "Labor Law - Book 2",
    "simplified_text": "Apprenticeship agreements,\nincluding wage rates of apprentices, shall conform to the rules issued by the Minister of Labor\nand Employment. The period of apprenticeship shall not exceed six months. Apprenticeship\nagreements providing for wage rates below the legal minimum wage, which in no case shall\nstart below 75 per cent of the applicable minimum wage, may be entered into only in\naccordance with apprenticeship programs duly approved by the Minister of Labor and\nEmployment. The Ministry shall develop standard model programs of apprenticeship.",
    "chunks": [
      "Apprenticeship agreements,\nincluding wage rates of apprentices, shall conform to the rules issued by the Minister of Labor\nand Employment. The period of apprenticeship shall not exceed six months. Apprenticeship\nagreements providing for wage rates below the legal minimum wage, which in no case shall\nstart below 75 per cent of the applicable minimum wage, may be entered into only in\naccordance with apprenticeship programs duly approved by the Minister of Labor and\nEmployment. The Ministry shall develop standard model programs of apprenticeship."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 62",
    "title": "Signing of Apprenticeship Agreement",
    "category": "Labor Law - Book 2",
    "simplified_text": "Every apprenticeship agreement shall\nbe signed by the employer or his agent, or by an authorized representative of any of the\nrecognized organizations, associations or groups and by the apprentice.\n\nAn apprenticeship agreement with a minor shall be signed in his behalf by his parent or\nguardian or, if the latter is not available, by an authorized representative of the Department\nof Labor, and the same shall be binding during its lifetime.\n\nEvery apprenticeship agreement entered into under this Title shall be ratified by the\nappropriate apprenticeship committees, if any, and a copy thereof shall be furnished both the\nemployer and the apprentice.",
    "chunks": [
      "Every apprenticeship agreement shall\nbe signed by the employer or his agent, or by an authorized representative of any of the\nrecognized organizations, associations or groups and by the apprentice.",
      "An apprenticeship agreement with a minor shall be signed in his behalf by his parent or\nguardian or, if the latter is not available, by an authorized representative of the Department\nof Labor, and the same shall be binding during its lifetime.",
      "Every apprenticeship agreement entered into under this Title shall be ratified by the\nappropriate apprenticeship committees, if any, and a copy thereof shall be furnished both the\nemployer and the apprentice."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 63",
    "title": "Venue of Apprenticeship Programs",
    "category": "Labor Law - Book 2",
    "simplified_text": "Any firm, employer, group or association,\nindustry organization or civic group wishing to organize an apprenticeship program may\nchoose from any of the following apprenticeship schemes as the training venue for apprentice:\n\n(a) Apprenticeship conducted entirely by and within the sponsoring firm, establishment\nor entity;\n\n(b) Apprenticeship entirely within a Department of Labor and Employment training\ncenter or other public training institution; or\n\n(c) Initial training in trade fundamentals in a training center or other institution with\nsubsequent actual work participation within the sponsoring firm or entity during the final stage\nof training.",
    "chunks": [
      "Any firm, employer, group or association,\nindustry organization or civic group wishing to organize an apprenticeship program may\nchoose from any of the following apprenticeship schemes as the training venue for apprentice:",
      "(a) Apprenticeship conducted entirely by and within the sponsoring firm, establishment\nor entity;",
      "(b) Apprenticeship entirely within a Department of Labor and Employment training\ncenter or other public training institution; or",
      "(c) Initial training in trade fundamentals in a training center or other institution with\nsubsequent actual work participation within the sponsoring firm or entity during the final stage\nof training."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 64",
    "title": "Sponsoring of Apprenticeship Program",
    "category": "Labor Law - Book 2",
    "simplified_text": "Any of the apprenticeship schemes\nrecognized herein may be undertaken or sponsored by a single employer or firm or by a group\nor association thereof or by a civic organization. Actual training of apprentices may be\nundertaken:\n\n(a) In the premises of the sponsoring employer in the case of individual apprenticeship\nprograms;\n\n(b) In the premises of one or several designated firms in the case of programs sponsored\nby a group or association of employers or by a civic organization; or\n\n(c) In a Department of Labor and Employment training center or other public training\ninstitution.",
    "chunks": [
      "Any of the apprenticeship schemes\nrecognized herein may be undertaken or sponsored by a single employer or firm or by a group\nor association thereof or by a civic organization. Actual training of apprentices may be\nundertaken:",
      "(a) In the premises of the sponsoring employer in the case of individual apprenticeship\nprograms;",
      "(b) In the premises of one or several designated firms in the case of programs sponsored\nby a group or association of employers or by a civic organization; or",
      "(c) In a Department of Labor and Employment training center or other public training\ninstitution."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 65",
    "title": "Investigation of Violation of Apprenticeship Agreement",
    "category": "Labor Law - Book 2",
    "simplified_text": "Upon complaint of\nany interested person or upon its own initiative, the appropriate agency of the Department of\nLabor and Employment or its authorized representative shall investigate any violation of an\napprenticeship agreement pursuant to such rules and regulations as may be prescribed by the\nSecretary of Labor and Employment.",
    "chunks": [
      "Upon complaint of\nany interested person or upon its own initiative, the appropriate agency of the Department of\nLabor and Employment or its authorized representative shall investigate any violation of an\napprenticeship agreement pursuant to such rules and regulations as may be prescribed by the\nSecretary of Labor and Employment."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 66",
    "title": "Appeal to the Secretary of Labor and Employment",
    "category": "Labor Law - Book 2",
    "simplified_text": "The decision of the\nauthorized agency of the Department of Labor and Employment may be appealed by any\naggrieved person to the Secretary of Labor and Employment within five (5) days from receipt\nof the decision. The decision of the Secretary of Labor and Employment shall be final and\nexecutory.",
    "chunks": [
      "The decision of the\nauthorized agency of the Department of Labor and Employment may be appealed by any\naggrieved person to the Secretary of Labor and Employment within five (5) days from receipt\nof the decision. The decision of the Secretary of Labor and Employment shall be final and\nexecutory."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 67",
    "title": "Exhaustion of Administrative Remedies",
    "category": "Labor Law - Book 2",
    "simplified_text": "No person shall institute any action\nfor the enforcement of any apprenticeship agreement or damages for breach of any such\nagreement, unless he has exhausted all available administrative remedies.",
    "chunks": [
      "No person shall institute any action\nfor the enforcement of any apprenticeship agreement or damages for breach of any such\nagreement, unless he has exhausted all available administrative remedies."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 68",
    "title": "Aptitude Testing of Applicants",
    "category": "Labor Law - Book 2",
    "simplified_text": "Consonant with the minimum qualifications of\napprentice-applicants required under this Chapter, employers or entities with duly recognized\napprenticeship programs shall have primary responsibility for providing appropriate aptitude\ntests in the selection of apprentices. If they do not have adequate facilities for the purpose,\nthe Department of Labor and Employment shall perform the service free of charge.",
    "chunks": [
      "Consonant with the minimum qualifications of\napprentice-applicants required under this Chapter, employers or entities with duly recognized\napprenticeship programs shall have primary responsibility for providing appropriate aptitude\ntests in the selection of apprentices. If they do not have adequate facilities for the purpose,\nthe Department of Labor and Employment shall perform the service free of charge."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 69",
    "title": "Responsibility for Theoretical Instruction",
    "category": "Labor Law - Book 2",
    "simplified_text": "Supplementary theoretical\ninstruction to apprentices in cases where the program is undertaken in the plant may be done\nby the employer. If the latter is not prepared to assume the responsibility, the same may be\ndelegated to an appropriate government agency.",
    "chunks": [
      "Supplementary theoretical\ninstruction to apprentices in cases where the program is undertaken in the plant may be done\nby the employer. If the latter is not prepared to assume the responsibility, the same may be\ndelegated to an appropriate government agency."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 70",
    "title": "Voluntary Organization of Apprenticeship Programs; Exemptions",
    "category": "Labor Law - Book 2",
    "simplified_text": "(a) The\norganization of apprenticeship program shall be primarily a voluntary undertaking by\nemployers;\n\n(b) When national security or particular requirements of economic development so\ndemand, the President of the Philippines may require compulsory training of apprentices in\ncertain trades, occupations, jobs or employment levels where shortage of trained manpower\nis deemed critical as determined by the Secretary of Labor and Employment. Appropriate rules\nin this connection shall be promulgated by the Secretary of Labor and Employment as the need\narises; and\n\n(c) Where services of foreign technicians are utilized by private companies in\napprenticeable trades, said companies are required to set up appropriate apprenticeship\nprograms.",
    "chunks": [
      "(a) The\norganization of apprenticeship program shall be primarily a voluntary undertaking by\nemployers;",
      "(b) When national security or particular requirements of economic development so\ndemand, the President of the Philippines may require compulsory training of apprentices in\ncertain trades, occupations, jobs or employment levels where shortage of trained manpower\nis deemed critical as determined by the Secretary of Labor and Employment. Appropriate rules\nin this connection shall be promulgated by the Secretary of Labor and Employment as the need\narises; and",
      "(c) Where services of foreign technicians are utilized by private companies in\napprenticeable trades, said companies are required to set up appropriate apprenticeship\nprograms."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 71",
    "title": "Deductibility of Training Costs",
    "category": "Labor Law - Book 2",
    "simplified_text": "An additional deduction from taxable income\nof one-half (1/2) of the value of labor training expenses incurred for developing the\nproductivity and efficiency of apprentices shall be granted to the person or enterprise\norganizing an apprenticeship program: Provided, That such program is duly recognized by the\nDepartment of Labor and Employment: Provided, further, That such deduction shall not\nexceed ten (10%) percent of direct labor wage; and Provided, finally, That the person or\nenterprise who wishes to avail himself or itself of this incentive should pay his apprentices the\nminimum wage.",
    "chunks": [
      "An additional deduction from taxable income\nof one-half (1/2) of the value of labor training expenses incurred for developing the\nproductivity and efficiency of apprentices shall be granted to the person or enterprise\norganizing an apprenticeship program: Provided, That such program is duly recognized by the\nDepartment of Labor and Employment: Provided, further, That such deduction shall not\nexceed ten (10%) percent of direct labor wage; and Provided, finally, That the person or\nenterprise who wishes to avail himself or itself of this incentive should pay his apprentices the\nminimum wage."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 72",
    "title": "Apprentices Without Compensation",
    "category": "Labor Law - Book 2",
    "simplified_text": "The Secretary of Labor and\nEmployment may authorize the hiring of apprentices without compensation whose training\n\non the job is required by the school or training program curriculum or as requisite for\ngraduation or board examination.",
    "chunks": [
      "The Secretary of Labor and\nEmployment may authorize the hiring of apprentices without compensation whose training",
      "on the job is required by the school or training program curriculum or as requisite for\ngraduation or board examination."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter I - APPRENTICES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 73",
    "title": "Learners Defined",
    "category": "Labor Law - Book 2",
    "simplified_text": "Learners are persons hired as trainees in semi-skilled and\nother industrial occupations which are non-apprenticeable and which may be learned through\npractical training on the job in a relatively short period of time which shall not exceed three\n(3) months.",
    "chunks": [
      "Learners are persons hired as trainees in semi-skilled and\nother industrial occupations which are non-apprenticeable and which may be learned through\npractical training on the job in a relatively short period of time which shall not exceed three\n(3) months."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter II - LEARNERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 74",
    "title": "When Learners May Be Hired",
    "category": "Labor Law - Book 2",
    "simplified_text": "Learners may be employed when no\nexperienced workers are available, the employment of learners is necessary to prevent\ncurtailment of employment opportunities, and the employment does not create unfair\ncompetition in terms of labor costs or impair or lower working standards.",
    "chunks": [
      "Learners may be employed when no\nexperienced workers are available, the employment of learners is necessary to prevent\ncurtailment of employment opportunities, and the employment does not create unfair\ncompetition in terms of labor costs or impair or lower working standards."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter II - LEARNERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 75",
    "title": "Learnership Agreement",
    "category": "Labor Law - Book 2",
    "simplified_text": "Any employer desiring to employ learners shall enter\ninto a learnership agreement with them, which agreement shall include:\n\n(a) The names and addresses of the learners;\n\n(b) The duration of the learnership period, which shall not exceed three (3) months;\n\n(c) The wages or salary rates of the learners which shall begin at not less than seventy-\nfive percent (75%) of the applicable minimum wage; and\n\n(d) A commitment to employ the learners if they so desire, as regular employees upon\ncompletion of the learnership. All learners who have been allowed or suffered to work during\nthe first two (2) months shall be deemed regular employees if training is terminated by the\nemployer before the end of the stipulated period through no fault of the learners.\n\nThe learnership agreement shall be subject to inspection by the Secretary of Labor and\nEmployment or his duly authorized representative.",
    "chunks": [
      "Any employer desiring to employ learners shall enter\ninto a learnership agreement with them, which agreement shall include:",
      "(a) The names and addresses of the learners;",
      "(b) The duration of the learnership period, which shall not exceed three (3) months;",
      "(c) The wages or salary rates of the learners which shall begin at not less than seventy-\nfive percent (75%) of the applicable minimum wage; and",
      "(d) A commitment to employ the learners if they so desire, as regular employees upon\ncompletion of the learnership. All learners who have been allowed or suffered to work during\nthe first two (2) months shall be deemed regular employees if training is terminated by the\nemployer before the end of the stipulated period through no fault of the learners.",
      "The learnership agreement shall be subject to inspection by the Secretary of Labor and\nEmployment or his duly authorized representative."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter II - LEARNERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 76",
    "title": "Learners in Piecework",
    "category": "Labor Law - Book 2",
    "simplified_text": "Learners employed in piece or incentive-rate jobs\nduring the training period shall be paid in full for the work done.",
    "chunks": [
      "Learners employed in piece or incentive-rate jobs\nduring the training period shall be paid in full for the work done."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter II - LEARNERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 77",
    "title": "Penalty Clause",
    "category": "Labor Law - Book 2",
    "simplified_text": "Any violation of this Chapter or its implementing rules and\nregulations shall be subject to the general penalty clause provided for in this Code.",
    "chunks": [
      "Any violation of this Chapter or its implementing rules and\nregulations shall be subject to the general penalty clause provided for in this Code."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter II - LEARNERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 78",
    "title": "Definition",
    "category": "Labor Law - Book 2",
    "simplified_text": "Handicapped workers are those whose earning capacity is\nimpaired by age or physical or mental deficiency or injury.",
    "chunks": [
      "Handicapped workers are those whose earning capacity is\nimpaired by age or physical or mental deficiency or injury."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter III - HANDICAPPED WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 79",
    "title": "When Employable",
    "category": "Labor Law - Book 2",
    "simplified_text": "Handicapped workers may be employed when their\nemployment is necessary to prevent curtailment of employment opportunities and when it\ndoes not create unfair competition in labor costs or impair or lower working standards.",
    "chunks": [
      "Handicapped workers may be employed when their\nemployment is necessary to prevent curtailment of employment opportunities and when it\ndoes not create unfair competition in labor costs or impair or lower working standards."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter III - HANDICAPPED WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 80",
    "title": "Employment Agreement",
    "category": "Labor Law - Book 2",
    "simplified_text": "Any employer who employs handicapped workers\nshall enter into an employment agreement with them, which agreement shall include:\n\n1.The names and addresses of the handicapped workers to be employed;\n\n2.The rate to be paid the handicapped workers which shall not be less than seventy\nfive (75%) percent of the applicable legal minimum wage;\n\n3.The duration of employment period; and\n\n4.The work to be performed by handicapped workers.\n\nThe employment agreement shall be subject to inspection by the Secretary of Labor or\nhis duly authorized representative.",
    "chunks": [
      "Any employer who employs handicapped workers\nshall enter into an employment agreement with them, which agreement shall include:",
      "1.The names and addresses of the handicapped workers to be employed;",
      "2.The rate to be paid the handicapped workers which shall not be less than seventy\nfive (75%) percent of the applicable legal minimum wage;",
      "3.The duration of employment period; and",
      "4.The work to be performed by handicapped workers.",
      "The employment agreement shall be subject to inspection by the Secretary of Labor or\nhis duly authorized representative."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter III - HANDICAPPED WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 81",
    "title": "Eligibility for Apprenticeship",
    "category": "Labor Law - Book 2",
    "simplified_text": "Subject to the appropriate provisions of this\nCode, handicapped workers may be hired as apprentices or learners if their handicap is not\nsuch as to effectively impede the performance of job operations in the particular occupations\nfor which they are hired.",
    "chunks": [
      "Subject to the appropriate provisions of this\nCode, handicapped workers may be hired as apprentices or learners if their handicap is not\nsuch as to effectively impede the performance of job operations in the particular occupations\nfor which they are hired."
    ],
    "tags": [
      "Book Two - HUMAN RESOURCES DEVELOPMENT PROGRAM",
      "Title II - TRAINING AND EMPLOYMENT OF SPECIAL WORKERS",
      "Chapter III - HANDICAPPED WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 82",
    "title": "Coverage",
    "category": "Labor Law - Book 3",
    "simplified_text": "The provisions of this Title shall apply to employees in all\nestablishments and undertakings whether for profit or not, but not to government employees,\nmanagerial employees, field personnel, members of the family of the employer who are\ndependent on him for support, domestic helpers, persons in the personal service of another,\nand workers who are paid by results as determined by the Secretary of Labor in appropriate\nregulations.\n\nAs used herein, \"managerial employees\" refer to those whose primary duty consists of\nthe management of the establishment in which they are employed or of a department or\nsubdivision thereof, and to other officers or members of the managerial staff.\n\n\"Field personnel\" shall refer to non-agricultural employees who regularly perform their\nduties away from the principal place of business or branch office of the employer and whose\nactual hours of work in the field cannot be determined with reasonable certainty.",
    "chunks": [
      "The provisions of this Title shall apply to employees in all\nestablishments and undertakings whether for profit or not, but not to government employees,\nmanagerial employees, field personnel, members of the family of the employer who are\ndependent on him for support, domestic helpers, persons in the personal service of another,\nand workers who are paid by results as determined by the Secretary of Labor in appropriate\nregulations.",
      "As used herein, \"managerial employees\" refer to those whose primary duty consists of\nthe management of the establishment in which they are employed or of a department or\nsubdivision thereof, and to other officers or members of the managerial staff.",
      "\"Field personnel\" shall refer to non-agricultural employees who regularly perform their\nduties away from the principal place of business or branch office of the employer and whose\nactual hours of work in the field cannot be determined with reasonable certainty."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 83",
    "title": "Normal Hours of Work",
    "category": "Labor Law - Book 3",
    "simplified_text": "The normal hours of work of any employee shall not\nexceed eight (8) hours a day.\n\nHealth personnel in cities and municipalities with a population of at least one million\n(1,000,000) or in hospitals and clinics with a bed capacity of at least one hundred (100) shall\nhold regular office hours for eight (8) hours a day, for five (5) days a week, exclusive of time\nfor meals, except where the exigencies of the service require that such personnel work for six\n(6) days or forty-eight (48) hours, in which case, they shall be entitled to an additional\ncompensation of at least thirty percent (30%) of their regular wage for work on the sixth day.\nFor purposes of this Article, \"health personnel\" shall include resident physicians, nurses,\nnutritionists, dieticians, pharmacists, social workers, laboratory technicians, paramedical\ntechnicians, psychologists, midwives, attendants and all other hospital or clinic personnel.",
    "chunks": [
      "The normal hours of work of any employee shall not\nexceed eight (8) hours a day.",
      "Health personnel in cities and municipalities with a population of at least one million\n(1,000,000) or in hospitals and clinics with a bed capacity of at least one hundred (100) shall\nhold regular office hours for eight (8) hours a day, for five (5) days a week, exclusive of time\nfor meals, except where the exigencies of the service require that such personnel work for six\n(6) days or forty-eight (48) hours, in which case, they shall be entitled to an additional\ncompensation of at least thirty percent (30%) of their regular wage for work on the sixth day.\nFor purposes of this Article, \"health personnel\" shall include resident physicians, nurses,\nnutritionists, dieticians, pharmacists, social workers, laboratory technicians, paramedical\ntechnicians, psychologists, midwives, attendants and all other hospital or clinic personnel."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 84",
    "title": "Hours Worked",
    "category": "Labor Law - Book 3",
    "simplified_text": "Hours worked shall include (a) all time during which an\nemployee is required to be on duty or to be at a prescribed workplace; and (b) all time during\nwhich an employee is suffered or permitted to work.\n\nRest periods of short duration during working hours shall be counted as hours worked.",
    "chunks": [
      "Hours worked shall include (a) all time during which an\nemployee is required to be on duty or to be at a prescribed workplace; and (b) all time during\nwhich an employee is suffered or permitted to work.",
      "Rest periods of short duration during working hours shall be counted as hours worked."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 85",
    "title": "Meal Periods",
    "category": "Labor Law - Book 3",
    "simplified_text": "Subject to such regulations as the Secretary of Labor may\nprescribe, it shall be the duty of every employer to give his employees not less than sixty (60)\nminutes time-off for their regular meals.",
    "chunks": [
      "Subject to such regulations as the Secretary of Labor may\nprescribe, it shall be the duty of every employer to give his employees not less than sixty (60)\nminutes time-off for their regular meals."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 86",
    "title": "Night-Shift Differential",
    "category": "Labor Law - Book 3",
    "simplified_text": "Every employee shall be paid a night shift differential\nof not less than ten percent (10%) of his regular wage for each hour of work performed\nbetween ten o’clock in the evening and six o’clock in the morning.",
    "chunks": [
      "Every employee shall be paid a night shift differential\nof not less than ten percent (10%) of his regular wage for each hour of work performed\nbetween ten o’clock in the evening and six o’clock in the morning."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 87",
    "title": "Overtime Work",
    "category": "Labor Law - Book 3",
    "simplified_text": "Work may be performed beyond eight (8) hours a day\nprovided that the employee is paid for the overtime work, an additional compensation\nequivalent to his regular wage plus at least twenty-five percent (25%) thereof. Work\nperformed beyond eight hours on a holiday or rest day shall be paid an additional\ncompensation equivalent to the rate of the first eight hours on a holiday or rest day plus at\nleast thirty percent (30%) thereof.",
    "chunks": [
      "Work may be performed beyond eight (8) hours a day\nprovided that the employee is paid for the overtime work, an additional compensation\nequivalent to his regular wage plus at least twenty-five percent (25%) thereof. Work\nperformed beyond eight hours on a holiday or rest day shall be paid an additional\ncompensation equivalent to the rate of the first eight hours on a holiday or rest day plus at\nleast thirty percent (30%) thereof."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 88",
    "title": "Undertime Not Offset by Overtime",
    "category": "Labor Law - Book 3",
    "simplified_text": "Undertime work on any particular day\nshall not be offset by overtime work on any other day. Permission given to the employee to\ngo on leave on some other day of the week shall not exempt the employer from paying the\nadditional compensation required in this Chapter.",
    "chunks": [
      "Undertime work on any particular day\nshall not be offset by overtime work on any other day. Permission given to the employee to\ngo on leave on some other day of the week shall not exempt the employer from paying the\nadditional compensation required in this Chapter."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 89",
    "title": "Emergency Overtime Work",
    "category": "Labor Law - Book 3",
    "simplified_text": "Any employee may be required by the employer\nto perform overtime work in any of the following cases:\n\n(a) When the country is at war or when any other national or local emergency has been\ndeclared by the National Assembly or the Chief Executive;\n\n(b) When it is necessary to prevent loss of life or property or in case of imminent danger\nto public safety due to an actual or impending emergency in the locality caused by serious\naccidents, fire, flood, typhoon, earthquake, epidemic, or other disaster or calamity;\n\n(c) When there is urgent work to be performed on machines, installations, or\nequipment, in order to avoid serious loss or damage to the employer or some other cause of\nsimilar nature;\n\n(d) When the work is necessary to prevent loss or damage to perishable goods; and\n\n(e) Where the completion or continuation of the work started before the eighth hour is\nnecessary to prevent serious obstruction or prejudice to the business or operations of the\nemployer.\n\nAny employee required to render overtime work under this Article shall be paid the\nadditional compensation required in this Chapter.",
    "chunks": [
      "Any employee may be required by the employer\nto perform overtime work in any of the following cases:",
      "(a) When the country is at war or when any other national or local emergency has been\ndeclared by the National Assembly or the Chief Executive;",
      "(b) When it is necessary to prevent loss of life or property or in case of imminent danger\nto public safety due to an actual or impending emergency in the locality caused by serious\naccidents, fire, flood, typhoon, earthquake, epidemic, or other disaster or calamity;",
      "(c) When there is urgent work to be performed on machines, installations, or\nequipment, in order to avoid serious loss or damage to the employer or some other cause of\nsimilar nature;",
      "(d) When the work is necessary to prevent loss or damage to perishable goods; and",
      "(e) Where the completion or continuation of the work started before the eighth hour is\nnecessary to prevent serious obstruction or prejudice to the business or operations of the\nemployer.",
      "Any employee required to render overtime work under this Article shall be paid the\nadditional compensation required in this Chapter."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 90",
    "title": "Computation of Additional Compensation",
    "category": "Labor Law - Book 3",
    "simplified_text": "For purposes of computing\novertime and other additional remuneration as required by this Chapter, the \"regular wage\"\nof an employee shall include the cash wage only, without deduction on account of facilities\nprovided by the employer.",
    "chunks": [
      "For purposes of computing\novertime and other additional remuneration as required by this Chapter, the \"regular wage\"\nof an employee shall include the cash wage only, without deduction on account of facilities\nprovided by the employer."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter I - HOURS OF WORK"
    ],
    "language": "en"
  },
  {
    "article": "Art. 91",
    "title": "Right to Weekly Rest Day",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) It shall be the duty of every employer, whether\noperating for profit or not, to provide each of his employees a rest period of not less than\ntwenty-four (24) consecutive hours after every six (6) consecutive normal work days.\n\n(b) The employer shall determine and schedule the weekly rest day of his employees\nsubject to collective bargaining agreement and to such rules and regulations as the Secretary\nof Labor and Employment may provide. However, the employer shall respect the preference\nof employees as to their weekly rest day when such preference is based on religious grounds.",
    "chunks": [
      "(a) It shall be the duty of every employer, whether\noperating for profit or not, to provide each of his employees a rest period of not less than\ntwenty-four (24) consecutive hours after every six (6) consecutive normal work days.",
      "(b) The employer shall determine and schedule the weekly rest day of his employees\nsubject to collective bargaining agreement and to such rules and regulations as the Secretary\nof Labor and Employment may provide. However, the employer shall respect the preference\nof employees as to their weekly rest day when such preference is based on religious grounds."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter II - WEEKLY REST PERIODS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 92",
    "title": "When Employer May Require Work on a Rest Day",
    "category": "Labor Law - Book 3",
    "simplified_text": "The employer may require\nhis employees to work on any day:\n\n(a) In case of actual or impending emergencies caused by serious accident, fire, flood,\ntyphoon, earthquake, epidemic or other disaster or calamity to prevent loss of life and\nproperty, or imminent danger to public safety;\n\n(b) In cases of urgent work to be performed on the machinery, equipment, or\ninstallation, to avoid serious loss which the employer would otherwise suffer;\n\n(c) In the event of abnormal pressure of work due to special circumstances, where the\nemployer cannot ordinarily be expected to resort to other measures;\n\n(d) To prevent loss or damage to perishable goods;\n\n(e) Where the nature of the work requires continuous operations and the stoppage of\nwork may result in irreparable injury or loss to the employer; and\n\n(f) Under other circumstances analogous or similar to the foregoing as determined by\nthe Secretary of Labor and Employment.",
    "chunks": [
      "The employer may require\nhis employees to work on any day:",
      "(a) In case of actual or impending emergencies caused by serious accident, fire, flood,\ntyphoon, earthquake, epidemic or other disaster or calamity to prevent loss of life and\nproperty, or imminent danger to public safety;",
      "(b) In cases of urgent work to be performed on the machinery, equipment, or\ninstallation, to avoid serious loss which the employer would otherwise suffer;",
      "(c) In the event of abnormal pressure of work due to special circumstances, where the\nemployer cannot ordinarily be expected to resort to other measures;",
      "(d) To prevent loss or damage to perishable goods;",
      "(e) Where the nature of the work requires continuous operations and the stoppage of\nwork may result in irreparable injury or loss to the employer; and",
      "(f) Under other circumstances analogous or similar to the foregoing as determined by\nthe Secretary of Labor and Employment."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter II - WEEKLY REST PERIODS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 93",
    "title": "Compensation for Rest Day, Sunday or Holiday Work",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) Where an employee\nis made or permitted to work on his scheduled rest day, he shall be paid an additional\ncompensation of at least thirty percent (30%) of his regular wage. An employee shall be\nentitled to such additional compensation for work performed on Sunday only when it is his\nestablished rest day.\n\n(b) When the nature of the work of the employee is such that he has no regular workdays\nand no regular rest days can be scheduled, he shall be paid an additional compensation of at\nleast thirty percent (30%) of his regular wage for work performed on Sundays and holidays.\n\n(c) Work performed on any special holiday shall be paid an additional compensation of\nat least thirty percent (30%) of the regular wage of the employee. Where such holiday work\nfalls on the employee’s scheduled rest day, he shall be entitled to an additional compensation\nof at least fifty per cent (50%) of his regular wage.\n\n(d) Where the collective bargaining agreement or other applicable employment contract\nstipulates the payment of a higher premium pay than that prescribed under this Article, the\nemployer shall pay such higher rate.",
    "chunks": [
      "(a) Where an employee\nis made or permitted to work on his scheduled rest day, he shall be paid an additional\ncompensation of at least thirty percent (30%) of his regular wage. An employee shall be\nentitled to such additional compensation for work performed on Sunday only when it is his\nestablished rest day.",
      "(b) When the nature of the work of the employee is such that he has no regular workdays\nand no regular rest days can be scheduled, he shall be paid an additional compensation of at\nleast thirty percent (30%) of his regular wage for work performed on Sundays and holidays.",
      "(c) Work performed on any special holiday shall be paid an additional compensation of\nat least thirty percent (30%) of the regular wage of the employee. Where such holiday work\nfalls on the employee’s scheduled rest day, he shall be entitled to an additional compensation\nof at least fifty per cent (50%) of his regular wage.",
      "(d) Where the collective bargaining agreement or other applicable employment contract\nstipulates the payment of a higher premium pay than that prescribed under this Article, the\nemployer shall pay such higher rate."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter II - WEEKLY REST PERIODS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 94",
    "title": "Right to Holiday Pay",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) Every worker shall be paid his regular daily wage\nduring regular holidays, except in retail and service establishments regularly employing less\nthan ten (10) workers;\n\n(b) The employer may require an employee to work on any holiday but such employee\nshall be paid a compensation equivalent to twice his regular rate; and\n\n(c) As used in this Article, \"holiday\" includes: New Year’s Day, Maundy Thursday, Good\nFriday, the ninth of April, the first of May, the twelfth of June, the fourth of July, the thirtieth\nof November, the twenty-fifth and thirtieth of December and the day designated by law for\nholding a general election.",
    "chunks": [
      "(a) Every worker shall be paid his regular daily wage\nduring regular holidays, except in retail and service establishments regularly employing less\nthan ten (10) workers;",
      "(b) The employer may require an employee to work on any holiday but such employee\nshall be paid a compensation equivalent to twice his regular rate; and",
      "(c) As used in this Article, \"holiday\" includes: New Year’s Day, Maundy Thursday, Good\nFriday, the ninth of April, the first of May, the twelfth of June, the fourth of July, the thirtieth\nof November, the twenty-fifth and thirtieth of December and the day designated by law for\nholding a general election."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter III - HOLIDAYS, SERVICE INCENTIVE LEAVES, AND SERVICE CHARGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 95",
    "title": "Right to Service Incentive Leave",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) Every employee who has rendered at\nleast one year of service shall be entitled to a yearly service incentive leave of five days with\npay.\n\n(b) This provision shall not apply to those who are already enjoying the benefit herein\nprovided, those enjoying vacation leave with pay of at least five days and those employed in\nestablishments regularly employing less than ten employees or in establishments exempted\nfrom granting this benefit by the Secretary of Labor and Employment after considering the\nviability or financial condition of such establishment.\n\n(c) The grant of benefit in excess of that provided herein shall not be made a subject of\narbitration or any court or administrative action.",
    "chunks": [
      "(a) Every employee who has rendered at\nleast one year of service shall be entitled to a yearly service incentive leave of five days with\npay.",
      "(b) This provision shall not apply to those who are already enjoying the benefit herein\nprovided, those enjoying vacation leave with pay of at least five days and those employed in\nestablishments regularly employing less than ten employees or in establishments exempted\nfrom granting this benefit by the Secretary of Labor and Employment after considering the\nviability or financial condition of such establishment.",
      "(c) The grant of benefit in excess of that provided herein shall not be made a subject of\narbitration or any court or administrative action."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter III - HOLIDAYS, SERVICE INCENTIVE LEAVES, AND SERVICE CHARGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 96",
    "title": "Service Charges",
    "category": "Labor Law - Book 3",
    "simplified_text": "All service charges collected by hotels, restaurants and\nsimilar establishments shall be distributed completely and equally among the covered workers\nexcept managerial employees.\n\nIn the event that the minimum wage is increased by law or wage order, service charges\npaid to the covered employees shall not be considered in determining the employer’s\ncompliance with the increased minimum wage.\n\nTo facilitate resolution of any dispute between the management and the employees on\nthe distribution of service charges, a grievance mechanism shall be established. If no grievance\nis established or if inadequate, the grievance shall be referred to the regional office of the\nDepartment of Labor and Employment which has jurisdiction over the workplace for\nconciliation.\n\nFor purposes of this Article, managerial employees refer to any person vested with\npowers or prerogatives to lay down and execute management polices or hire, transfer\nsuspend, lay-off, recall, discharge, assign or discipline employees or to effectively recommend\nsuch managerial actions.",
    "chunks": [
      "All service charges collected by hotels, restaurants and\nsimilar establishments shall be distributed completely and equally among the covered workers\nexcept managerial employees.",
      "In the event that the minimum wage is increased by law or wage order, service charges\npaid to the covered employees shall not be considered in determining the employer’s\ncompliance with the increased minimum wage.",
      "To facilitate resolution of any dispute between the management and the employees on\nthe distribution of service charges, a grievance mechanism shall be established. If no grievance\nis established or if inadequate, the grievance shall be referred to the regional office of the\nDepartment of Labor and Employment which has jurisdiction over the workplace for\nconciliation.",
      "For purposes of this Article, managerial employees refer to any person vested with\npowers or prerogatives to lay down and execute management polices or hire, transfer\nsuspend, lay-off, recall, discharge, assign or discipline employees or to effectively recommend\nsuch managerial actions."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title I - WORKING CONDITIONS AND REST PERIODS",
      "Chapter III - HOLIDAYS, SERVICE INCENTIVE LEAVES, AND SERVICE CHARGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 97",
    "title": "Definitions",
    "category": "Labor Law - Book 3",
    "simplified_text": "As used in this Title:\n\n(a)\"Person\" means an individual, partnership, association, corporation, business trust,\nlegal representatives, or any organized group of persons.\n\n(b)\"Employer\" includes any person acting directly or indirectly in the interest of an\nemployer in relation to an employee and shall include the government and all its branches,\nsubdivisions and instrumentalities, all government-owned or controlled corporations and\ninstitutions, as well as non-profit private institutions, or organizations.\n\n(c)\"Employee\" includes any individual employed by an employer.\n\n(d)\"Agriculture\" includes farming in all its branches and, among other things, includes\ncultivation and tillage of soil, dairying, the production, cultivation, growing and harvesting of\nany agricultural and horticultural commodities, the raising of livestock or poultry, and any\npractices performed by a farmer on a farm as an incident to or in conjunction with such\nfarming operations, but does not include the manufacturing or processing of sugar, coconuts,\nabaca, tobacco, pineapples or other farm products.\n\n(e)\"Employ\" includes to suffer or permit to work.\n\n(f)\"Wage\" paid to any employee shall mean the remuneration or earnings, however\ndesignated, capable of being expressed in terms of money, whether fixed or ascertained on a\ntime, task, piece, or commission basis, or other method of calculating the same, which is\npayable by an employer to an employee under a written or unwritten contract of employment\n\nfor work done or to be done, or for services rendered or to be rendered and includes the fair\nand reasonable value, as determined by the Secretary of Labor and Employment, of board,\nlodging, or other facilities customarily furnished by the employer to the employee. \"Fair and\nreasonable value\" shall not include any profit to the employer, or to any person affiliated with\nthe employer.",
    "chunks": [
      "As used in this Title:",
      "(a)\"Person\" means an individual, partnership, association, corporation, business trust,\nlegal representatives, or any organized group of persons.",
      "(b)\"Employer\" includes any person acting directly or indirectly in the interest of an\nemployer in relation to an employee and shall include the government and all its branches,\nsubdivisions and instrumentalities, all government-owned or controlled corporations and\ninstitutions, as well as non-profit private institutions, or organizations.",
      "(c)\"Employee\" includes any individual employed by an employer.",
      "(d)\"Agriculture\" includes farming in all its branches and, among other things, includes\ncultivation and tillage of soil, dairying, the production, cultivation, growing and harvesting of\nany agricultural and horticultural commodities, the raising of livestock or poultry, and any\npractices performed by a farmer on a farm as an incident to or in conjunction with such\nfarming operations, but does not include the manufacturing or processing of sugar, coconuts,\nabaca, tobacco, pineapples or other farm products.",
      "(e)\"Employ\" includes to suffer or permit to work.",
      "(f)\"Wage\" paid to any employee shall mean the remuneration or earnings, however\ndesignated, capable of being expressed in terms of money, whether fixed or ascertained on a\ntime, task, piece, or commission basis, or other method of calculating the same, which is\npayable by an employer to an employee under a written or unwritten contract of employment",
      "for work done or to be done, or for services rendered or to be rendered and includes the fair\nand reasonable value, as determined by the Secretary of Labor and Employment, of board,\nlodging, or other facilities customarily furnished by the employer to the employee. \"Fair and\nreasonable value\" shall not include any profit to the employer, or to any person affiliated with\nthe employer."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter I - PRELIMINARY MATTERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 98",
    "title": "Application of Title",
    "category": "Labor Law - Book 3",
    "simplified_text": "This Title shall not apply to farm tenancy or leasehold,\ndomestic service and persons working in their respective homes in needle work or in any\ncottage industry duly registered in accordance with law.",
    "chunks": [
      "This Title shall not apply to farm tenancy or leasehold,\ndomestic service and persons working in their respective homes in needle work or in any\ncottage industry duly registered in accordance with law."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter I - PRELIMINARY MATTERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 99",
    "title": "Regional Minimum Wages",
    "category": "Labor Law - Book 3",
    "simplified_text": "The minimum wage rates for agricultural and\nnon-agricultural employees and workers in each and every region of the country shall be those\nprescribed by the Regional Tripartite Wages and Productivity Boards.",
    "chunks": [
      "The minimum wage rates for agricultural and\nnon-agricultural employees and workers in each and every region of the country shall be those\nprescribed by the Regional Tripartite Wages and Productivity Boards."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter II - MINIMUM WAGE RATES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 100",
    "title": "Prohibition Against Elimination or Diminution of Benefits",
    "category": "Labor Law - Book 3",
    "simplified_text": "Nothing in this\nBook shall be construed to eliminate or in any way diminish supplements, or other employee\nbenefits being enjoyed at the time of promulgation of this Code.",
    "chunks": [
      "Nothing in this\nBook shall be construed to eliminate or in any way diminish supplements, or other employee\nbenefits being enjoyed at the time of promulgation of this Code."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter II - MINIMUM WAGE RATES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 101",
    "title": "Payment by Results",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) The Secretary of Labor and Employment shall\nregulate the payment of wages by results, including pakyao, piecework, and other non-time\nwork, in order to ensure the payment of fair and reasonable wage rates, preferably through\ntime and motion studies or in consultation with representatives of workers’ and employers’\norganizations.",
    "chunks": [
      "(a) The Secretary of Labor and Employment shall\nregulate the payment of wages by results, including pakyao, piecework, and other non-time\nwork, in order to ensure the payment of fair and reasonable wage rates, preferably through\ntime and motion studies or in consultation with representatives of workers’ and employers’\norganizations."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter II - MINIMUM WAGE RATES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 102",
    "title": "Forms of Payment",
    "category": "Labor Law - Book 3",
    "simplified_text": "No employer shall pay the wages of an employee by\nmeans of promissory notes, vouchers, coupons, tokens, tickets, chits, or any object other than\nlegal tender, even when expressly requested by the employee.\n\nPayment of wages by check or money order shall be allowed when such manner of\npayment is customary on the date of effectivity of this Code, or is necessary because of special\n\ncircumstances as specified in appropriate regulations to be issued by the Secretary of Labor\nand Employment or as stipulated in a collective bargaining agreement.",
    "chunks": [
      "No employer shall pay the wages of an employee by\nmeans of promissory notes, vouchers, coupons, tokens, tickets, chits, or any object other than\nlegal tender, even when expressly requested by the employee.",
      "Payment of wages by check or money order shall be allowed when such manner of\npayment is customary on the date of effectivity of this Code, or is necessary because of special",
      "circumstances as specified in appropriate regulations to be issued by the Secretary of Labor\nand Employment or as stipulated in a collective bargaining agreement."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 103",
    "title": "Time of Payment",
    "category": "Labor Law - Book 3",
    "simplified_text": "Wages shall be paid at least once every two (2) weeks or\ntwice a month at intervals not exceeding sixteen (16) days. If on account of force majeure or\ncircumstances beyond the employer’s control, payment of wages on or within the time herein\nprovided cannot be made, the employer shall pay the wages immediately after such force\nmajeure or circumstances have ceased. No employer shall make payment with less frequency\nthan once a month.\n\nThe payment of wages of employees engaged to perform a task which cannot be\ncompleted in two (2) weeks shall be subject to the following conditions, in the absence of a\ncollective bargaining agreement or arbitration award:\n\n1.That payments are made at intervals not exceeding sixteen (16) days, in proportion\nto the amount of work completed;\n\n2.That final settlement is made upon completion of the work.",
    "chunks": [
      "Wages shall be paid at least once every two (2) weeks or\ntwice a month at intervals not exceeding sixteen (16) days. If on account of force majeure or\ncircumstances beyond the employer’s control, payment of wages on or within the time herein\nprovided cannot be made, the employer shall pay the wages immediately after such force\nmajeure or circumstances have ceased. No employer shall make payment with less frequency\nthan once a month.",
      "The payment of wages of employees engaged to perform a task which cannot be\ncompleted in two (2) weeks shall be subject to the following conditions, in the absence of a\ncollective bargaining agreement or arbitration award:",
      "1.That payments are made at intervals not exceeding sixteen (16) days, in proportion\nto the amount of work completed;",
      "2.That final settlement is made upon completion of the work."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 104",
    "title": "Place of Payment",
    "category": "Labor Law - Book 3",
    "simplified_text": "Payment of wages shall be made at or near the place of\nundertaking, except as otherwise provided by such regulations as the Secretary of Labor and\nEmployment may prescribe under conditions to ensure greater protection of wages.",
    "chunks": [
      "Payment of wages shall be made at or near the place of\nundertaking, except as otherwise provided by such regulations as the Secretary of Labor and\nEmployment may prescribe under conditions to ensure greater protection of wages."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 105",
    "title": "Direct Payment of Wages",
    "category": "Labor Law - Book 3",
    "simplified_text": "Wages shall be paid directly to the workers to\nwhom they are due, except:\n\n(a) In cases of force majeure rendering such payment impossible or under other special\ncircumstances to be determined by the Secretary of Labor and Employment in appropriate\nregulations, in which case, the worker may be paid through another person under written\nauthority given by the worker for the purpose; or\n\n(b) Where the worker has died, in which case, the employer may pay the wages of the\ndeceased worker to the heirs of the latter without the necessity of intestate proceedings. The\nclaimants, if they are all of age, shall execute an affidavit attesting to their relationship to the\ndeceased and the fact that they are his heirs, to the exclusion of all other persons. If any of the\n\nheirs is a minor, the affidavit shall be executed on his behalf by his natural guardian or next-\nof-kin. The affidavit shall be presented to the employer who shall make payment through the\nSecretary of Labor and Employment or his representative. The representative of the Secretary\nof Labor and Employment shall act as referee in dividing the amount paid among the heirs.\nThe payment of wages under this Article shall absolve the employer of any further liability with\nrespect to the amount paid.",
    "chunks": [
      "Wages shall be paid directly to the workers to\nwhom they are due, except:",
      "(a) In cases of force majeure rendering such payment impossible or under other special\ncircumstances to be determined by the Secretary of Labor and Employment in appropriate\nregulations, in which case, the worker may be paid through another person under written\nauthority given by the worker for the purpose; or",
      "(b) Where the worker has died, in which case, the employer may pay the wages of the\ndeceased worker to the heirs of the latter without the necessity of intestate proceedings. The\nclaimants, if they are all of age, shall execute an affidavit attesting to their relationship to the\ndeceased and the fact that they are his heirs, to the exclusion of all other persons. If any of the",
      "heirs is a minor, the affidavit shall be executed on his behalf by his natural guardian or next-\nof-kin. The affidavit shall be presented to the employer who shall make payment through the\nSecretary of Labor and Employment or his representative. The representative of the Secretary\nof Labor and Employment shall act as referee in dividing the amount paid among the heirs.\nThe payment of wages under this Article shall absolve the employer of any further liability with\nrespect to the amount paid."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 106",
    "title": "Contractor or Subcontractor",
    "category": "Labor Law - Book 3",
    "simplified_text": "Whenever an employer enters into a contract\nwith another person for the performance of the former’s work, the employees of the\ncontractor and of the latter’s subcontractor, if any, shall be paid in accordance with the\nprovisions of this Code.\n\nIn the event that the contractor or subcontractor fails to pay the wages of his employees\nin accordance with this Code, the employer shall be jointly and severally liable with his\ncontractor or subcontractor to such employees to the extent of the work performed under the\ncontract, in the same manner and extent that he is liable to employees directly employed by\nhim.\n\nThe Secretary of Labor and Employment may, by appropriate regulations, restrict or\nprohibit the contracting-out of labor to protect the rights of workers established under this\nCode. In so prohibiting or restricting, he may make appropriate distinctions between labor-\nonly contracting and job contracting as well as differentiations within these types of\ncontracting and determine who among the parties involved shall be considered the employer\nfor purposes of this Code, to prevent any violation or circumvention of any provision of this\nCode.\n\nThere is \"labor-only\" contracting where the person supplying workers to an employer\ndoes not have substantial capital or investment in the form of tools, equipment, machineries,\nwork premises, among others, and the workers recruited and placed by such person are\nperforming activities which are directly related to the principal business of such employer. In\nsuch cases, the person or intermediary shall be considered merely as an agent of the employer\nwho shall be responsible to the workers in the same manner and extent as if the latter were\ndirectly employed by him.",
    "chunks": [
      "Whenever an employer enters into a contract\nwith another person for the performance of the former’s work, the employees of the\ncontractor and of the latter’s subcontractor, if any, shall be paid in accordance with the\nprovisions of this Code.",
      "In the event that the contractor or subcontractor fails to pay the wages of his employees\nin accordance with this Code, the employer shall be jointly and severally liable with his\ncontractor or subcontractor to such employees to the extent of the work performed under the\ncontract, in the same manner and extent that he is liable to employees directly employed by\nhim.",
      "The Secretary of Labor and Employment may, by appropriate regulations, restrict or\nprohibit the contracting-out of labor to protect the rights of workers established under this\nCode. In so prohibiting or restricting, he may make appropriate distinctions between labor-\nonly contracting and job contracting as well as differentiations within these types of\ncontracting and determine who among the parties involved shall be considered the employer\nfor purposes of this Code, to prevent any violation or circumvention of any provision of this\nCode.",
      "There is \"labor-only\" contracting where the person supplying workers to an employer\ndoes not have substantial capital or investment in the form of tools, equipment, machineries,\nwork premises, among others, and the workers recruited and placed by such person are\nperforming activities which are directly related to the principal business of such employer. In\nsuch cases, the person or intermediary shall be considered merely as an agent of the employer\nwho shall be responsible to the workers in the same manner and extent as if the latter were\ndirectly employed by him."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 107",
    "title": "Indirect Employer",
    "category": "Labor Law - Book 3",
    "simplified_text": "The provisions of the immediately preceding article shall\nlikewise apply to any person, partnership, association or corporation which, not being an\nemployer, contracts with an independent contractor for the performance of any work, task,\njob or project.",
    "chunks": [
      "The provisions of the immediately preceding article shall\nlikewise apply to any person, partnership, association or corporation which, not being an\nemployer, contracts with an independent contractor for the performance of any work, task,\njob or project."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 108",
    "title": "Posting of Bond",
    "category": "Labor Law - Book 3",
    "simplified_text": "An employer or indirect employer may require the\ncontractor or subcontractor to furnish a bond equal to the cost of labor under contract, on\n\ncondition that the bond will answer for the wages due the employees should the contractor\nor subcontractor, as the case may be, fail to pay the same.",
    "chunks": [
      "An employer or indirect employer may require the\ncontractor or subcontractor to furnish a bond equal to the cost of labor under contract, on",
      "condition that the bond will answer for the wages due the employees should the contractor\nor subcontractor, as the case may be, fail to pay the same."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 109",
    "title": "Solidary Liability",
    "category": "Labor Law - Book 3",
    "simplified_text": "The provisions of existing laws to the contrary\nnotwithstanding, every employer or indirect employer shall be held responsible with his\ncontractor or subcontractor for any violation of any provision of this Code. For purposes of\ndetermining the extent of their civil liability under this Chapter, they shall be considered as\ndirect employers.",
    "chunks": [
      "The provisions of existing laws to the contrary\nnotwithstanding, every employer or indirect employer shall be held responsible with his\ncontractor or subcontractor for any violation of any provision of this Code. For purposes of\ndetermining the extent of their civil liability under this Chapter, they shall be considered as\ndirect employers."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 110",
    "title": "Worker Preference in Case of Bankruptcy",
    "category": "Labor Law - Book 3",
    "simplified_text": "In the event of bankruptcy or\nliquidation of an employer’s business, his workers shall enjoy first preference as regards their\nwages and other monetary claims, any provisions of law to the contrary notwithstanding. Such\nunpaid wages and claims shall be paid in full before claims of the government and\nmonetary\nother creditors may be paid.",
    "chunks": [
      "In the event of bankruptcy or\nliquidation of an employer’s business, his workers shall enjoy first preference as regards their\nwages and other monetary claims, any provisions of law to the contrary notwithstanding. Such\nunpaid wages and claims shall be paid in full before claims of the government and\nmonetary\nother creditors may be paid."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 111",
    "title": "Attorney's Fees",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) In cases of unlawful withholding of wages, the culpable\nparty may be assessed attorney’s fees equivalent to ten percent of the amount of wages\nrecovered.\n\n(b) It shall be unlawful for any person to demand or accept, in any judicial or\nadministrative proceedings for the recovery of wages, attorney’s fees which exceed ten\npercent of the amount of wages recovered.",
    "chunks": [
      "(a) In cases of unlawful withholding of wages, the culpable\nparty may be assessed attorney’s fees equivalent to ten percent of the amount of wages\nrecovered.",
      "(b) It shall be unlawful for any person to demand or accept, in any judicial or\nadministrative proceedings for the recovery of wages, attorney’s fees which exceed ten\npercent of the amount of wages recovered."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter III - PAYMENT OF WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 112",
    "title": "Non-Interference in Disposal of Wages",
    "category": "Labor Law - Book 3",
    "simplified_text": "No employer shall limit or otherwise\ninterfere with the freedom of any employee to dispose of his wages. He shall not in any\nmanner force, compel, or oblige his employees to purchase merchandise, commodities or\nother property from any other person, or otherwise make use of any store or services of such\nemployer or any other person.",
    "chunks": [
      "No employer shall limit or otherwise\ninterfere with the freedom of any employee to dispose of his wages. He shall not in any\nmanner force, compel, or oblige his employees to purchase merchandise, commodities or\nother property from any other person, or otherwise make use of any store or services of such\nemployer or any other person."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 113",
    "title": "Wage Deduction",
    "category": "Labor Law - Book 3",
    "simplified_text": "No employer, in his own behalf or in behalf of any person,\nshall make any deduction from the wages of his employees, except:\n\n(a) In cases where the worker is insured with his consent by the employer, and the\ndeduction is to recompense the employer for the amount paid by him as premium on the\ninsurance;\n\n(b) For union dues, in cases where the right of the worker or his union to check-off has\nbeen recognized by the employer or authorized in writing by the individual worker concerned;\nand\n\n(c) In cases where the employer is authorized by law or regulations issued by the\nSecretary of Labor and Employment.",
    "chunks": [
      "No employer, in his own behalf or in behalf of any person,\nshall make any deduction from the wages of his employees, except:",
      "(a) In cases where the worker is insured with his consent by the employer, and the\ndeduction is to recompense the employer for the amount paid by him as premium on the\ninsurance;",
      "(b) For union dues, in cases where the right of the worker or his union to check-off has\nbeen recognized by the employer or authorized in writing by the individual worker concerned;\nand",
      "(c) In cases where the employer is authorized by law or regulations issued by the\nSecretary of Labor and Employment."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 114",
    "title": "Deposits for Loss or Damage",
    "category": "Labor Law - Book 3",
    "simplified_text": "No employer shall require his worker to make\ndeposits from which deductions shall be made for the reimbursement of loss of or damage to\ntools, materials, or equipment supplied by the employer, except when the employer is\nengaged in such trades, occupations or business where the practice of making deductions or\nrequiring deposits is a recognized one, or is necessary or desirable as determined by the\nSecretary of Labor and Employment in appropriate rules and regulations.",
    "chunks": [
      "No employer shall require his worker to make\ndeposits from which deductions shall be made for the reimbursement of loss of or damage to\ntools, materials, or equipment supplied by the employer, except when the employer is\nengaged in such trades, occupations or business where the practice of making deductions or\nrequiring deposits is a recognized one, or is necessary or desirable as determined by the\nSecretary of Labor and Employment in appropriate rules and regulations."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 115",
    "title": "Limitations",
    "category": "Labor Law - Book 3",
    "simplified_text": "No deduction from the deposits of an employee for the actual\namount of the loss or damage shall be made unless the employee has been heard thereon,\nand his responsibility has been clearly shown.",
    "chunks": [
      "No deduction from the deposits of an employee for the actual\namount of the loss or damage shall be made unless the employee has been heard thereon,\nand his responsibility has been clearly shown."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 116",
    "title": "Withholding of Wages and Kickbacks Prohibited",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful for any\nperson, directly or indirectly, to withhold any amount from the wages of a worker or induce\nhim to give up any part of his wages by force, stealth, intimidation, threat or by any other\nmeans whatsoever without the worker’s consent.",
    "chunks": [
      "It shall be unlawful for any\nperson, directly or indirectly, to withhold any amount from the wages of a worker or induce\nhim to give up any part of his wages by force, stealth, intimidation, threat or by any other\nmeans whatsoever without the worker’s consent."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 117",
    "title": "Deduction to Ensure Employment",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful to make any deduction\nfrom the wages of any employee for the benefit of the employer or his representative or\nintermediary as consideration of a promise of employment or retention in employment.",
    "chunks": [
      "It shall be unlawful to make any deduction\nfrom the wages of any employee for the benefit of the employer or his representative or\nintermediary as consideration of a promise of employment or retention in employment."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 118",
    "title": "Retaliatory Measures",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful for an employer to refuse to pay or\nreduce the wages and benefits, discharge or in any manner discriminate against any employee\nwho has filed any complaint or instituted any proceeding under this Title or has testified or is\nabout to testify in such proceedings.",
    "chunks": [
      "It shall be unlawful for an employer to refuse to pay or\nreduce the wages and benefits, discharge or in any manner discriminate against any employee\nwho has filed any complaint or instituted any proceeding under this Title or has testified or is\nabout to testify in such proceedings."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 119",
    "title": "False Reporting",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful for any person to make any statement,\nreport, or record filed or kept pursuant to the provisions of this Code knowing such statement,\nreport or record to be false in any material respect.\n\nDETERMINATION",
    "chunks": [
      "It shall be unlawful for any person to make any statement,\nreport, or record filed or kept pursuant to the provisions of this Code knowing such statement,\nreport or record to be false in any material respect.",
      "DETERMINATION"
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter IV - PROHIBITIONS REGARDING WAGES"
    ],
    "language": "en"
  },
  {
    "article": "Art. 120",
    "title": "Creation of National Wages and Productivity Commission",
    "category": "Labor Law - Book 3",
    "simplified_text": "There is hereby\ncreated a National Wages and Productivity Commission, hereinafter referred to as the\n\nCommission, which shall be attached to the Department of Labor and Employment (DOLE) for\npolicy and program coordination.",
    "chunks": [
      "There is hereby\ncreated a National Wages and Productivity Commission, hereinafter referred to as the",
      "Commission, which shall be attached to the Department of Labor and Employment (DOLE) for\npolicy and program coordination."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 121",
    "title": "Powers and Functions of the Commission",
    "category": "Labor Law - Book 3",
    "simplified_text": "The Commission shall have the\nfollowing powers and functions:\n\n(a) To act as the national consultative and advisory body to the President of the\nPhilippines and Congress on matters relating to wages, incomes and productivity;\n\n(b) To formulate policies and guidelines on wages, incomes and productivity\nimprovement at the enterprise, industry and national levels;\n\n(c) To prescribe rules and guidelines for the determination of appropriate minimum\nwage and productivity measures at the regional, provincial, or industry levels;\n\n(d) To review regional wage levels set by the Regional Tripartite Wages and Productivity\nBoards to determine if these are in accordance with prescribed guidelines and national\ndevelopment plans;\n\n(e) To undertake studies, researches and surveys necessary for the attainment of its\nfunctions and objectives, and to collect and compile data and periodically disseminate\ninformation on wages and productivity and other related information, including, but not\nlimited to, employment, cost-of-living, labor costs, investments and returns;\n\n(f) To review plans and programs of the Regional Tripartite Wages and Productivity\nBoards to determine whether these are consistent with national development plans;\n\n(g) To exercise technical and administrative supervision over the Regional Tripartite\nWages and Productivity Boards;\n\n(h) To call, from time to time, a national tripartite conference of representatives of\ngovernment, workers and employers for the consideration of measures to promote wage\nrationalization and productivity; and\n\n(i) To exercise such powers and functions as may be necessary to implement this Act.\n\nThe Commission shall be composed of the Secretary of Labor and Employment as ex-\nofficio chairman, the Director-General of the National Economic and Development Authority\n(NEDA) as ex-officio vice-chairman, and two (2) members each from workers and employers\nsectors who shall be appointed by the President of the Philippines upon recommendation of\nthe Secretary of Labor and Employment to be made on the basis of the list of nominees\nsubmitted by the workers and employers sectors, respectively, and who shall serve for a term\nof five (5) years. The Executive Director of the Commission shall also be a member of the\nCommission.\n\nThe Commission shall be assisted by a Secretariat to be headed by an Executive Director\nand two (2) Deputy Directors, who shall be appointed by the President of the Philippines, upon\nthe recommendation of the Secretary of Labor and Employment.\n\nThe Executive Director shall have the same rank, salary, benefits and other emoluments\nas that of a Department Assistant Secretary, while the Deputy Directors shall have the same\nrank, salary, benefits and other emoluments as that of a Bureau Director. The members of the\nCommission representing labor and management shall have the same rank, emoluments,\nallowances and other benefits as those prescribed by law for labor and management\nrepresentatives in the Employees’ Compensation Commission.",
    "chunks": [
      "The Commission shall have the\nfollowing powers and functions:",
      "(a) To act as the national consultative and advisory body to the President of the\nPhilippines and Congress on matters relating to wages, incomes and productivity;",
      "(b) To formulate policies and guidelines on wages, incomes and productivity\nimprovement at the enterprise, industry and national levels;",
      "(c) To prescribe rules and guidelines for the determination of appropriate minimum\nwage and productivity measures at the regional, provincial, or industry levels;",
      "(d) To review regional wage levels set by the Regional Tripartite Wages and Productivity\nBoards to determine if these are in accordance with prescribed guidelines and national\ndevelopment plans;",
      "(e) To undertake studies, researches and surveys necessary for the attainment of its\nfunctions and objectives, and to collect and compile data and periodically disseminate\ninformation on wages and productivity and other related information, including, but not\nlimited to, employment, cost-of-living, labor costs, investments and returns;",
      "(f) To review plans and programs of the Regional Tripartite Wages and Productivity\nBoards to determine whether these are consistent with national development plans;",
      "(g) To exercise technical and administrative supervision over the Regional Tripartite\nWages and Productivity Boards;",
      "(h) To call, from time to time, a national tripartite conference of representatives of\ngovernment, workers and employers for the consideration of measures to promote wage\nrationalization and productivity; and",
      "(i) To exercise such powers and functions as may be necessary to implement this Act.",
      "The Commission shall be composed of the Secretary of Labor and Employment as ex-\nofficio chairman, the Director-General of the National Economic and Development Authority\n(NEDA) as ex-officio vice-chairman, and two (2) members each from workers and employers\nsectors who shall be appointed by the President of the Philippines upon recommendation of\nthe Secretary of Labor and Employment to be made on the basis of the list of nominees\nsubmitted by the workers and employers sectors, respectively, and who shall serve for a term\nof five (5) years. The Executive Director of the Commission shall also be a member of the\nCommission.",
      "The Commission shall be assisted by a Secretariat to be headed by an Executive Director\nand two (2) Deputy Directors, who shall be appointed by the President of the Philippines, upon\nthe recommendation of the Secretary of Labor and Employment.",
      "The Executive Director shall have the same rank, salary, benefits and other emoluments\nas that of a Department Assistant Secretary, while the Deputy Directors shall have the same\nrank, salary, benefits and other emoluments as that of a Bureau Director. The members of the\nCommission representing labor and management shall have the same rank, emoluments,\nallowances and other benefits as those prescribed by law for labor and management\nrepresentatives in the Employees’ Compensation Commission."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 122",
    "title": "Creation of Regional Tripartite Wages and Productivity Boards",
    "category": "Labor Law - Book 3",
    "simplified_text": "There is\nhereby created Regional Tripartite Wages and Productivity Boards, hereinafter referred to as\nRegional Boards, in all regions, including autonomous regions as may be established by law.\nThe Commission shall determine the offices/headquarters of the respective Regional Boards.\n\nThe Regional Boards shall have the following powers and functions in their respective\nterritorial jurisdictions:\n\n(a) To develop plans, programs and projects relative to wages, incomes and productivity\nimprovement for their respective regions;\n\n(b) To determine and fix minimum wage rates applicable in their regions, provinces or\nindustries therein and to issue the corresponding wage orders, subject to guidelines issued by\nthe Commission;\n\n(c) To undertake studies, researches, and surveys necessary for the attainment of their\nfunctions, objectives and programs, and to collect and compile data on wages, incomes,\nproductivity and other related information and periodically disseminate the same;\n\n(d) To coordinate with the other Regional Boards as may be necessary to attain the\npolicy and intention of this Code;\n\n(e) To receive, process and act on applications for exemption from prescribed wage\nrates as may be provided by law or any Wage Order; and\n\n(f) To exercise such other powers and functions as may be necessary to carry out their\nmandate under this Code.\n\nImplementation of the plans, programs, and projects of the Regional Boards referred to\nin the second paragraph, letter (a) of this Article, shall be through the respective regional\noffices of the Department of Labor and Employment within their territorial jurisdiction;\n\nProvided, however, That the Regional Boards shall have technical supervision over the regional\noffice of the Department of Labor and Employment with respect to the implementation of said\nplans, programs and projects.\n\nEach Regional Board shall be composed of the Regional Director of the Department of\nLabor and Employment as chairman, the Regional Directors of the National Economic and\nDevelopment Authority and the Department of Trade and Industry as vice-chairmen and two\n(2) members each from workers’ and employers’ sectors who shall be appointed by the\nPresident of the Philippines, upon the recommendation of the Secretary of Labor and\nEmployment, to be made on the basis of the list of nominees submitted by the workers’ and\nemployers’ sectors, respectively, and who shall serve for a term of five (5) years.\n\nEach Regional Board to be headed by its chairman shall be assisted by a Secretariat.",
    "chunks": [
      "There is\nhereby created Regional Tripartite Wages and Productivity Boards, hereinafter referred to as\nRegional Boards, in all regions, including autonomous regions as may be established by law.\nThe Commission shall determine the offices/headquarters of the respective Regional Boards.",
      "The Regional Boards shall have the following powers and functions in their respective\nterritorial jurisdictions:",
      "(a) To develop plans, programs and projects relative to wages, incomes and productivity\nimprovement for their respective regions;",
      "(b) To determine and fix minimum wage rates applicable in their regions, provinces or\nindustries therein and to issue the corresponding wage orders, subject to guidelines issued by\nthe Commission;",
      "(c) To undertake studies, researches, and surveys necessary for the attainment of their\nfunctions, objectives and programs, and to collect and compile data on wages, incomes,\nproductivity and other related information and periodically disseminate the same;",
      "(d) To coordinate with the other Regional Boards as may be necessary to attain the\npolicy and intention of this Code;",
      "(e) To receive, process and act on applications for exemption from prescribed wage\nrates as may be provided by law or any Wage Order; and",
      "(f) To exercise such other powers and functions as may be necessary to carry out their\nmandate under this Code.",
      "Implementation of the plans, programs, and projects of the Regional Boards referred to\nin the second paragraph, letter (a) of this Article, shall be through the respective regional\noffices of the Department of Labor and Employment within their territorial jurisdiction;",
      "Provided, however, That the Regional Boards shall have technical supervision over the regional\noffice of the Department of Labor and Employment with respect to the implementation of said\nplans, programs and projects.",
      "Each Regional Board shall be composed of the Regional Director of the Department of\nLabor and Employment as chairman, the Regional Directors of the National Economic and\nDevelopment Authority and the Department of Trade and Industry as vice-chairmen and two\n(2) members each from workers’ and employers’ sectors who shall be appointed by the\nPresident of the Philippines, upon the recommendation of the Secretary of Labor and\nEmployment, to be made on the basis of the list of nominees submitted by the workers’ and\nemployers’ sectors, respectively, and who shall serve for a term of five (5) years.",
      "Each Regional Board to be headed by its chairman shall be assisted by a Secretariat."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 123",
    "title": "Wage Order",
    "category": "Labor Law - Book 3",
    "simplified_text": "Whenever conditions in the region so warrant, the Regional\nBoard shall investigate and study all pertinent facts; and based on the standards and criteria\nherein prescribed, shall proceed to determine whether a Wage Order should be issued. Any\nsuch Wage Order shall take effect after fifteen (15) days from its complete publication in at\nleast one (1) newspaper of general circulation in the region.\n\nIn the performance of its wage-determining functions, the Regional Board shall conduct\npublic hearings/consultations, giving notices to employees’ and employers’ groups, provincial,\ncity and municipal officials and other interested parties.\n\nAny party aggrieved by the Wage Order issued by the Regional Board may appeal such\norder to the Commission within ten (10) calendar days from the publication of such order. It\nshall be mandatory for the Commission to decide such appeal within sixty (60) calendar days\nfrom the filing thereof.\n\nThe filing of the appeal does not stay the order unless the person appealing such order\nshall file with the Commission, an undertaking with a surety or sureties satisfactory to the\nCommission for the payment to the employees affected by the order of the corresponding\nincrease, in the event such order is affirmed.",
    "chunks": [
      "Whenever conditions in the region so warrant, the Regional\nBoard shall investigate and study all pertinent facts; and based on the standards and criteria\nherein prescribed, shall proceed to determine whether a Wage Order should be issued. Any\nsuch Wage Order shall take effect after fifteen (15) days from its complete publication in at\nleast one (1) newspaper of general circulation in the region.",
      "In the performance of its wage-determining functions, the Regional Board shall conduct\npublic hearings/consultations, giving notices to employees’ and employers’ groups, provincial,\ncity and municipal officials and other interested parties.",
      "Any party aggrieved by the Wage Order issued by the Regional Board may appeal such\norder to the Commission within ten (10) calendar days from the publication of such order. It\nshall be mandatory for the Commission to decide such appeal within sixty (60) calendar days\nfrom the filing thereof.",
      "The filing of the appeal does not stay the order unless the person appealing such order\nshall file with the Commission, an undertaking with a surety or sureties satisfactory to the\nCommission for the payment to the employees affected by the order of the corresponding\nincrease, in the event such order is affirmed."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 124",
    "title": "Standards/Criteria for Minimum Wage Fixing",
    "category": "Labor Law - Book 3",
    "simplified_text": "The regional minimum wages\nto be established by the Regional Board shall be as nearly adequate as is economically feasible\nto maintain the minimum standards of living necessary for the health, efficiency and general\nwell-being of the employees within the framework of the national economic and social\ndevelopment program. In the determination of such regional minimum wages, the Regional\nBoard shall, among other relevant factors, consider the following:\n\n(a) The demand for living wages;\n\n(b) Wage adjustment vis-à-vis the consumer price index;\n\n(c) The cost of living and changes or increases therein;\n\n(d) The needs of workers and their families;\n\n(e) The need to induce industries to invest in the countryside;\n\n(f) Improvements in standards of living;\n\n(g) The prevailing wage levels;\n\n(h) Fair return of the capital invested and capacity to pay of employers;\n\n(i) Effects on employment generation and family income; and\n\n(j) The equitable distribution of income and wealth along the imperatives of economic\nand social development.\n\nThe wages prescribed in accordance with the provisions of this Title shall be the standard\nprevailing minimum wages in every region. These wages shall include wages varying with\nindustries, provinces or localities if in the judgment of the Regional Board, conditions make\nsuch local differentiation proper and necessary to effectuate the purpose of this Title.\n\nAny person, company, corporation, partnership or any other entity engaged in business\nshall file and register annually with the appropriate Regional Board, Commission and the\nNational Statistics Office, an itemized listing of their labor component, specifying the names\nof their workers and employees below the managerial level, including learners, apprentices\nand disabled/handicapped workers who were hired under the terms prescribed in the\nemployment contracts, and their corresponding salaries and wages.\n\nWhere the application of any prescribed wage increase by virtue of a law or wage order\nissued by any Regional Board results in distortions of the wage structure within an\nestablishment, the employer and the union shall negotiate to correct the distortions. Any\ndispute arising from wage distortions shall be resolved through the grievance procedure under\ntheir collective bargaining agreement and, if it remains unresolved, through voluntary\narbitration. Unless otherwise agreed by the parties in writing, such dispute shall be decided by\nthe voluntary arbitrators within ten (10) calendar days from the time said dispute was referred\nto voluntary arbitration.\n\nIn cases where there are no collective agreements or recognized labor unions, the\nemployers and workers shall endeavor to correct such distortions. Any dispute arising\ntherefrom shall be settled through the National Conciliation and Mediation Board and, if it\n\nremains unresolved after ten (10) calendar days of conciliation, shall be referred to the\nappropriate branch of the National Labor Relations Commission (NLRC). It shall be mandatory\nfor the NLRC to conduct continuous hearings and decide the dispute within twenty (20)\ncalendar days from the time said dispute is submitted for compulsory arbitration.\n\nThe pendency of a dispute arising from a wage distortion shall not in any way delay the\napplicability of any increase in prescribed wage rates pursuant to the provisions of law or wage\norder.\n\nAs used herein, a wage distortion shall mean a situation where an increase in prescribed\nwage rates results in the elimination or severe contraction of intentional quantitative\ndifferences in wage or salary rates between and among employee groups in an establishment\nas to effectively obliterate the distinctions embodied in such wage structure based on skills,\nlength of service, or other logical bases of differentiation.\n\nAll workers paid by result, including those who are paid on piecework, takay, pakyaw or\ntask basis, shall receive not less than the prescribed wage rates per eight (8) hours of work a\nday, or a proportion thereof for working less than eight (8) hours.\n\nAll recognized learnership and apprenticeship agreements shall be considered\nautomatically modified insofar as their wage clauses are concerned to reflect the prescribed\nwage rates.",
    "chunks": [
      "The regional minimum wages\nto be established by the Regional Board shall be as nearly adequate as is economically feasible\nto maintain the minimum standards of living necessary for the health, efficiency and general\nwell-being of the employees within the framework of the national economic and social\ndevelopment program. In the determination of such regional minimum wages, the Regional\nBoard shall, among other relevant factors, consider the following:",
      "(a) The demand for living wages;",
      "(b) Wage adjustment vis-à-vis the consumer price index;",
      "(c) The cost of living and changes or increases therein;",
      "(d) The needs of workers and their families;",
      "(e) The need to induce industries to invest in the countryside;",
      "(f) Improvements in standards of living;",
      "(g) The prevailing wage levels;",
      "(h) Fair return of the capital invested and capacity to pay of employers;",
      "(i) Effects on employment generation and family income; and",
      "(j) The equitable distribution of income and wealth along the imperatives of economic\nand social development.",
      "The wages prescribed in accordance with the provisions of this Title shall be the standard\nprevailing minimum wages in every region. These wages shall include wages varying with\nindustries, provinces or localities if in the judgment of the Regional Board, conditions make\nsuch local differentiation proper and necessary to effectuate the purpose of this Title.",
      "Any person, company, corporation, partnership or any other entity engaged in business\nshall file and register annually with the appropriate Regional Board, Commission and the\nNational Statistics Office, an itemized listing of their labor component, specifying the names\nof their workers and employees below the managerial level, including learners, apprentices\nand disabled/handicapped workers who were hired under the terms prescribed in the\nemployment contracts, and their corresponding salaries and wages.",
      "Where the application of any prescribed wage increase by virtue of a law or wage order\nissued by any Regional Board results in distortions of the wage structure within an\nestablishment, the employer and the union shall negotiate to correct the distortions. Any\ndispute arising from wage distortions shall be resolved through the grievance procedure under\ntheir collective bargaining agreement and, if it remains unresolved, through voluntary\narbitration. Unless otherwise agreed by the parties in writing, such dispute shall be decided by\nthe voluntary arbitrators within ten (10) calendar days from the time said dispute was referred\nto voluntary arbitration.",
      "In cases where there are no collective agreements or recognized labor unions, the\nemployers and workers shall endeavor to correct such distortions. Any dispute arising\ntherefrom shall be settled through the National Conciliation and Mediation Board and, if it",
      "remains unresolved after ten (10) calendar days of conciliation, shall be referred to the\nappropriate branch of the National Labor Relations Commission (NLRC). It shall be mandatory\nfor the NLRC to conduct continuous hearings and decide the dispute within twenty (20)\ncalendar days from the time said dispute is submitted for compulsory arbitration.",
      "The pendency of a dispute arising from a wage distortion shall not in any way delay the\napplicability of any increase in prescribed wage rates pursuant to the provisions of law or wage\norder.",
      "As used herein, a wage distortion shall mean a situation where an increase in prescribed\nwage rates results in the elimination or severe contraction of intentional quantitative\ndifferences in wage or salary rates between and among employee groups in an establishment\nas to effectively obliterate the distinctions embodied in such wage structure based on skills,\nlength of service, or other logical bases of differentiation.",
      "All workers paid by result, including those who are paid on piecework, takay, pakyaw or\ntask basis, shall receive not less than the prescribed wage rates per eight (8) hours of work a\nday, or a proportion thereof for working less than eight (8) hours.",
      "All recognized learnership and apprenticeship agreements shall be considered\nautomatically modified insofar as their wage clauses are concerned to reflect the prescribed\nwage rates."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 125",
    "title": "Freedom to Bargain",
    "category": "Labor Law - Book 3",
    "simplified_text": "No wage order shall be construed to prevent workers in\nparticular firms or enterprises or industries from bargaining for higher wages with their\nrespective employers.",
    "chunks": [
      "No wage order shall be construed to prevent workers in\nparticular firms or enterprises or industries from bargaining for higher wages with their\nrespective employers."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 126",
    "title": "Prohibition Against Injunction",
    "category": "Labor Law - Book 3",
    "simplified_text": "No preliminary or permanent injunction or\ntemporary restraining order may be issued by any court, tribunal or other entity against any\nproceedings before the Commission or the Regional Boards.",
    "chunks": [
      "No preliminary or permanent injunction or\ntemporary restraining order may be issued by any court, tribunal or other entity against any\nproceedings before the Commission or the Regional Boards."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 127",
    "title": "Non-Diminution of Benefits",
    "category": "Labor Law - Book 3",
    "simplified_text": "No wage order issued by any regional board shall\nprovide for wage rates lower than the statutory minimum wage rates prescribed by Congress.",
    "chunks": [
      "No wage order issued by any regional board shall\nprovide for wage rates lower than the statutory minimum wage rates prescribed by Congress."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter V - WAGE STUDIES, WAGE AGREEMENTS, AND WAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 128",
    "title": "Visitorial and Enforcement Power",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) The Secretary of Labor and\nEmployment or his duly authorized representatives, including labor regulation officers, shall\nhave access to employer’s records and premises at any time of the day or night whenever work\nis being undertaken therein, and the right to copy therefrom, to question any employee and\ninvestigate any fact, condition or matter which may be necessary to determine violations or\nwhich may aid in the enforcement of this Code and of any labor law, wage order or rules and\nregulations issued pursuant thereto.\n\n(b) Notwithstanding the provisions of Articles 129 and 217 of this Code to the contrary,\nand in cases where the relationship of employer-employee still exists, the Secretary of Labor\nand Employment or his duly authorized representatives shall have the power to issue\ncompliance orders to give effect to the labor standards provisions of this Code and other labor\nlegislation based on the findings of labor employment and enforcement officers or industrial\nsafety engineers made in the course of inspection. The Secretary or his duly authorized\nrepresentatives shall issue writs of execution to the appropriate authority for the enforcement\nof their orders, except in cases where the employer contests the findings of the labor\nemployment and enforcement officer and raises issues supported by documentary proofs\nwhich were not considered in the course of inspection.\n\nAn order issued by the duly authorized representative of the Secretary of Labor and\nEmployment under this Article may be appealed to the latter. In case said order involves a\nmonetary award, an appeal by the employer may be perfected only upon the posting of a cash\nor surety bond issued by a reputable bonding company duly accredited by the Secretary of\nLabor and Employment in the amount equivalent to the monetary award in the order appealed\nfrom.\n\n(c) The Secretary of Labor and Employment may likewise order stoppage of work or\nsuspension of operations of any unit or department of an establishment when non-compliance\nwith the law or implementing rules and regulations poses grave and imminent danger to the\nhealth and safety of workers in the workplace. Within twenty-four hours, a hearing shall be\nconducted to determine whether an order for the stoppage of work or suspension of\noperations shall be lifted or not. In case the violation is attributable to the fault of the\nemployer, he shall pay the employees concerned their salaries or wages during the period of\nsuch stoppage of work or suspension of operation.\n\n(d) It shall be unlawful for any person or entity to obstruct, impede, delay or otherwise\nrender ineffective the orders of the Secretary of Labor and Employment or his duly authorized\nrepresentatives issued pursuant to the authority granted under this Article, and no inferior\ncourt or entity shall issue temporary or permanent injunction or restraining order or otherwise\nassume jurisdiction over any case involving the enforcement orders issued in accordance with\nthis Article.\n\n(e) Any government employee found guilty of violation of, or abuse of authority, under\nthis Article shall, after appropriate administrative investigation, be subject to summary\ndismissal from the service.\n\n(f) The Secretary of Labor and Employment may, by appropriate regulations, require\nemployers to keep and maintain such employment records as may be necessary in aid of his\nvisitorial and enforcement powers under this Code.",
    "chunks": [
      "(a) The Secretary of Labor and\nEmployment or his duly authorized representatives, including labor regulation officers, shall\nhave access to employer’s records and premises at any time of the day or night whenever work\nis being undertaken therein, and the right to copy therefrom, to question any employee and\ninvestigate any fact, condition or matter which may be necessary to determine violations or\nwhich may aid in the enforcement of this Code and of any labor law, wage order or rules and\nregulations issued pursuant thereto.",
      "(b) Notwithstanding the provisions of Articles 129 and 217 of this Code to the contrary,\nand in cases where the relationship of employer-employee still exists, the Secretary of Labor\nand Employment or his duly authorized representatives shall have the power to issue\ncompliance orders to give effect to the labor standards provisions of this Code and other labor\nlegislation based on the findings of labor employment and enforcement officers or industrial\nsafety engineers made in the course of inspection. The Secretary or his duly authorized\nrepresentatives shall issue writs of execution to the appropriate authority for the enforcement\nof their orders, except in cases where the employer contests the findings of the labor\nemployment and enforcement officer and raises issues supported by documentary proofs\nwhich were not considered in the course of inspection.",
      "An order issued by the duly authorized representative of the Secretary of Labor and\nEmployment under this Article may be appealed to the latter. In case said order involves a\nmonetary award, an appeal by the employer may be perfected only upon the posting of a cash\nor surety bond issued by a reputable bonding company duly accredited by the Secretary of\nLabor and Employment in the amount equivalent to the monetary award in the order appealed\nfrom.",
      "(c) The Secretary of Labor and Employment may likewise order stoppage of work or\nsuspension of operations of any unit or department of an establishment when non-compliance\nwith the law or implementing rules and regulations poses grave and imminent danger to the\nhealth and safety of workers in the workplace. Within twenty-four hours, a hearing shall be\nconducted to determine whether an order for the stoppage of work or suspension of\noperations shall be lifted or not. In case the violation is attributable to the fault of the\nemployer, he shall pay the employees concerned their salaries or wages during the period of\nsuch stoppage of work or suspension of operation.",
      "(d) It shall be unlawful for any person or entity to obstruct, impede, delay or otherwise\nrender ineffective the orders of the Secretary of Labor and Employment or his duly authorized\nrepresentatives issued pursuant to the authority granted under this Article, and no inferior\ncourt or entity shall issue temporary or permanent injunction or restraining order or otherwise\nassume jurisdiction over any case involving the enforcement orders issued in accordance with\nthis Article.",
      "(e) Any government employee found guilty of violation of, or abuse of authority, under\nthis Article shall, after appropriate administrative investigation, be subject to summary\ndismissal from the service.",
      "(f) The Secretary of Labor and Employment may, by appropriate regulations, require\nemployers to keep and maintain such employment records as may be necessary in aid of his\nvisitorial and enforcement powers under this Code."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter VI - ADMINISTRATION AND ENFORCEMENT"
    ],
    "language": "en"
  },
  {
    "article": "Art. 129",
    "title": "Recovery of Wages, Simple Money Claims and Other Benefits",
    "category": "Labor Law - Book 3",
    "simplified_text": "Upon\ncomplaint of any interested party, the Regional Director of the Department of Labor and\nEmployment or any of the duly authorized hearing officers of the Department is empowered,\nthrough summary proceeding and after due notice, to hear and decide any matter involving\nthe recovery of wages and other monetary claims and benefits, including legal interest, owing\nto an employee or person employed in domestic or household service or househelper under\nthis Code, arising from employer-employee relations: Provided, That such complaint does not\ninclude a claim for reinstatement: Provided, further, That the aggregate money claims of each\nemployee or househelper do not exceed five thousand pesos (P5,000.00). The Regional\nDirector or hearing officer shall decide or resolve the complaint within thirty (30) calendar\ndays from the date of the filing of the same. Any sum thus recovered on behalf of any\nemployee or househelper pursuant to this Article shall be held in a special deposit account,\nand shall be paid, on order of the Secretary of Labor and Employment or the Regional Director\ndirectly to the employee or househelper concerned. Any such sum not paid to the employee\nor househelper, because he cannot be located after diligent and reasonable effort to locate\nhim within a period of three (3) years, shall be held as a special fund of the Department of\nLabor and Employment to be used exclusively for the amelioration and benefit of workers.\n\nAny decision or resolution of the Regional Director or hearing officer pursuant to this\nprovision may be appealed on the same grounds provided in Article 223 of this Code, within\nfive (5) calendar days from receipt of a copy of said decision or resolution, to the National\nLabor Relations Commission which shall resolve the appeal within ten (10) calendar days from\nthe submission of the last pleading required or allowed under its rules.\n\nThe Secretary of Labor and Employment or his duly authorized representative may\nsupervise the payment of unpaid wages and other monetary claims and benefits, including\nlegal interest, found owing to any employee or house helper under this Code.\n\nOF EMPLOYEES",
    "chunks": [
      "Upon\ncomplaint of any interested party, the Regional Director of the Department of Labor and\nEmployment or any of the duly authorized hearing officers of the Department is empowered,\nthrough summary proceeding and after due notice, to hear and decide any matter involving\nthe recovery of wages and other monetary claims and benefits, including legal interest, owing\nto an employee or person employed in domestic or household service or househelper under\nthis Code, arising from employer-employee relations: Provided, That such complaint does not\ninclude a claim for reinstatement: Provided, further, That the aggregate money claims of each\nemployee or househelper do not exceed five thousand pesos (P5,000.00). The Regional\nDirector or hearing officer shall decide or resolve the complaint within thirty (30) calendar\ndays from the date of the filing of the same. Any sum thus recovered on behalf of any\nemployee or househelper pursuant to this Article shall be held in a special deposit account,\nand shall be paid, on order of the Secretary of Labor and Employment or the Regional Director\ndirectly to the employee or househelper concerned. Any such sum not paid to the employee\nor househelper, because he cannot be located after diligent and reasonable effort to locate\nhim within a period of three (3) years, shall be held as a special fund of the Department of\nLabor and Employment to be used exclusively for the amelioration and benefit of workers.",
      "Any decision or resolution of the Regional Director or hearing officer pursuant to this\nprovision may be appealed on the same grounds provided in Article 223 of this Code, within\nfive (5) calendar days from receipt of a copy of said decision or resolution, to the National\nLabor Relations Commission which shall resolve the appeal within ten (10) calendar days from\nthe submission of the last pleading required or allowed under its rules.",
      "The Secretary of Labor and Employment or his duly authorized representative may\nsupervise the payment of unpaid wages and other monetary claims and benefits, including\nlegal interest, found owing to any employee or house helper under this Code.",
      "OF EMPLOYEES"
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title II - WAGES",
      "Chapter VI - ADMINISTRATION AND ENFORCEMENT"
    ],
    "language": "en"
  },
  {
    "article": "Art. 130",
    "title": "Facilities for Women",
    "category": "Labor Law - Book 3",
    "simplified_text": "The Secretary of Labor and Employment shall\nestablish standards that will ensure the safety and health of women employees. In appropriate\ncases, he shall, by regulations, require any employer to:\n\n(a) Provide seats proper for women and permit them to use such seats when they are\nfree from work and during working hours, provided they can perform their duties in this\nposition without detriment to efficiency;\n\n(b) To establish separate toilet rooms and lavatories for men and women and provide at\nleast a dressing room for women;\n\n(c) To establish a nursery in a workplace for the benefit of the women employees\ntherein; and\n\n(d) To determine appropriate minimum age and other standards for retirement or\ntermination in special occupations such as those of flight attendants and the like.",
    "chunks": [
      "The Secretary of Labor and Employment shall\nestablish standards that will ensure the safety and health of women employees. In appropriate\ncases, he shall, by regulations, require any employer to:",
      "(a) Provide seats proper for women and permit them to use such seats when they are\nfree from work and during working hours, provided they can perform their duties in this\nposition without detriment to efficiency;",
      "(b) To establish separate toilet rooms and lavatories for men and women and provide at\nleast a dressing room for women;",
      "(c) To establish a nursery in a workplace for the benefit of the women employees\ntherein; and",
      "(d) To determine appropriate minimum age and other standards for retirement or\ntermination in special occupations such as those of flight attendants and the like."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "132"
  },
  {
    "article": "Art. 131",
    "title": "Maternity Leave Benefits",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) Every employer shall grant to any\npregnant woman employee who has rendered an aggregate service of at least six (6) months\nfor the last twelve (12) months, maternity leave of at least two (2) weeks prior to the expected\ndate of delivery and another four (4) weeks after normal delivery or abortion with full pay\nbased on her regular or average weekly wages. The employer may require from any woman\nemployee applying for maternity leave the production of a medical certificate stating that\ndelivery will probably take place within two weeks.\n\n(b) The maternity leave shall be extended without pay on account of illness medically\ncertified to arise out of the pregnancy, delivery, abortion or miscarriage, which renders the\nwoman unfit for work, unless she has earned unused leave credits from which such extended\nleave may be charged.\n\n(c) The maternity leave provided in this Article shall be paid by the employer only for the\nfirst four (4) deliveries by a woman employee after the effectivity of this Code.",
    "chunks": [
      "(a) Every employer shall grant to any\npregnant woman employee who has rendered an aggregate service of at least six (6) months\nfor the last twelve (12) months, maternity leave of at least two (2) weeks prior to the expected\ndate of delivery and another four (4) weeks after normal delivery or abortion with full pay\nbased on her regular or average weekly wages. The employer may require from any woman\nemployee applying for maternity leave the production of a medical certificate stating that\ndelivery will probably take place within two weeks.",
      "(b) The maternity leave shall be extended without pay on account of illness medically\ncertified to arise out of the pregnancy, delivery, abortion or miscarriage, which renders the\nwoman unfit for work, unless she has earned unused leave credits from which such extended\nleave may be charged.",
      "(c) The maternity leave provided in this Article shall be paid by the employer only for the\nfirst four (4) deliveries by a woman employee after the effectivity of this Code."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "133"
  },
  {
    "article": "Art. 132",
    "title": "Family Planning Services; Incentives for Family Planning",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a)\nEstablishments which are required by law to maintain a clinic or infirmary shall provide free\nfamily planning services to their employees which shall include, but not be limited to, the\napplication or use of contraceptive pills and intrauterine devices.\n\n(b) In coordination with other agencies of the government engaged in the promotion of\nfamily planning, the Department of Labor and Employment shall develop and prescribe\nincentive bonus schemes to encourage family planning among female workers in any\nestablishment or enterprise.",
    "chunks": [
      "(a)\nEstablishments which are required by law to maintain a clinic or infirmary shall provide free\nfamily planning services to their employees which shall include, but not be limited to, the\napplication or use of contraceptive pills and intrauterine devices.",
      "(b) In coordination with other agencies of the government engaged in the promotion of\nfamily planning, the Department of Labor and Employment shall develop and prescribe\nincentive bonus schemes to encourage family planning among female workers in any\nestablishment or enterprise."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "134"
  },
  {
    "article": "Art. 133",
    "title": "Discrimination Prohibited",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful for any employer to\ndiscriminate against any woman employee with respect to terms and conditions of\nemployment solely on account of her sex.\n\nThe following are acts of discrimination:\n\n(a) Payment of a lesser compensation, including wage, salary or other form of\nremuneration and fringe benefits, to a female employee as against a male employee, for work\nof equal value; and\n\n(b) Favoring a male employee over a female employee with respect to promotion, training\nopportunities, study and scholarship grants solely on account of their sexes.\n\nCriminal liability for the willful commission of any unlawful act as provided in this article\nor any violation of the rules and regulations issued pursuant to Section 2 hereof shall be\npenalized as provided in Articles 288 and 289 of this Code: Provided, That the institution of\nany criminal action under this provision shall not bar the aggrieved employee from filing an\nentirely separate and distinct action for money claims, which may include claims for damages\nand other affirmative reliefs. The actions hereby authorized shall proceed independently of\neach other.",
    "chunks": [
      "It shall be unlawful for any employer to\ndiscriminate against any woman employee with respect to terms and conditions of\nemployment solely on account of her sex.",
      "The following are acts of discrimination:",
      "(a) Payment of a lesser compensation, including wage, salary or other form of\nremuneration and fringe benefits, to a female employee as against a male employee, for work\nof equal value; and",
      "(b) Favoring a male employee over a female employee with respect to promotion, training\nopportunities, study and scholarship grants solely on account of their sexes.",
      "Criminal liability for the willful commission of any unlawful act as provided in this article\nor any violation of the rules and regulations issued pursuant to Section 2 hereof shall be\npenalized as provided in Articles 288 and 289 of this Code: Provided, That the institution of\nany criminal action under this provision shall not bar the aggrieved employee from filing an\nentirely separate and distinct action for money claims, which may include claims for damages\nand other affirmative reliefs. The actions hereby authorized shall proceed independently of\neach other."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "135"
  },
  {
    "article": "Art. 134",
    "title": "Stipulation Against Marriage",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful for an employer to\nrequire as a condition of employment or continuation of employment that a woman employee\nshall not get married, or to stipulate expressly or tacitly that upon getting married, a woman\nemployee shall be deemed resigned or separated, or to actually dismiss, discharge,\ndiscriminate or otherwise prejudice a woman employee merely by reason of her marriage.",
    "chunks": [
      "It shall be unlawful for an employer to\nrequire as a condition of employment or continuation of employment that a woman employee\nshall not get married, or to stipulate expressly or tacitly that upon getting married, a woman\nemployee shall be deemed resigned or separated, or to actually dismiss, discharge,\ndiscriminate or otherwise prejudice a woman employee merely by reason of her marriage."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "136"
  },
  {
    "article": "Art. 135",
    "title": "Prohibited Acts",
    "category": "Labor Law - Book 3",
    "simplified_text": "It shall be unlawful for any employer:\n\n(1) To deny any woman employee the benefits provided for in this Chapter or to discharge\nany woman employed by him for the purpose of preventing her from enjoying any of the\nbenefits provided under this Code;\n\n(2) To discharge such woman on account of her pregnancy, or while on leave or in\nconfinement due to her pregnancy;\n\n(3) To discharge or refuse the admission of such woman upon returning to her work for\nfear that she may again be pregnant.",
    "chunks": [
      "It shall be unlawful for any employer:",
      "(1) To deny any woman employee the benefits provided for in this Chapter or to discharge\nany woman employed by him for the purpose of preventing her from enjoying any of the\nbenefits provided under this Code;",
      "(2) To discharge such woman on account of her pregnancy, or while on leave or in\nconfinement due to her pregnancy;",
      "(3) To discharge or refuse the admission of such woman upon returning to her work for\nfear that she may again be pregnant."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "137"
  },
  {
    "article": "Art. 136",
    "title": "Classification of Certain Women Workers",
    "category": "Labor Law - Book 3",
    "simplified_text": "Any woman who is permitted\nor suffered to work, with or without compensation, in any night club, cocktail lounge, massage\nclinic, bar or similar establishments under the effective control or supervision of the employer\nfor a substantial period of time as determined by the Secretary of Labor and Employment, shall\nbe considered as an employee of such establishment for purposes of labor and social\nlegislation.",
    "chunks": [
      "Any woman who is permitted\nor suffered to work, with or without compensation, in any night club, cocktail lounge, massage\nclinic, bar or similar establishments under the effective control or supervision of the employer\nfor a substantial period of time as determined by the Secretary of Labor and Employment, shall\nbe considered as an employee of such establishment for purposes of labor and social\nlegislation."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter I - EMPLOYMENT OF WOMEN"
    ],
    "language": "en",
    "old_article_number": "138"
  },
  {
    "article": "Art. 137",
    "title": "Minimum Employable Age",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) No child below fifteen (15) years of\nage shall be employed, except when he works directly under the sole responsibility of his\nparents or guardian, and his employment does not in any way interfere with his schooling.\n\n(b) Any person between fifteen (15) and eighteen (18) years of age may be employed for\nsuch number of hours and such periods of the day as determined by the Secretary of Labor\nand Employment in appropriate regulations.\n\n(c) The foregoing provisions shall in no case allow the employment of a person below\neighteen (18) years of age in an undertaking which is hazardous or deleterious in nature as\ndetermined by the Secretary of Labor and Employment.",
    "chunks": [
      "(a) No child below fifteen (15) years of\nage shall be employed, except when he works directly under the sole responsibility of his\nparents or guardian, and his employment does not in any way interfere with his schooling.",
      "(b) Any person between fifteen (15) and eighteen (18) years of age may be employed for\nsuch number of hours and such periods of the day as determined by the Secretary of Labor\nand Employment in appropriate regulations.",
      "(c) The foregoing provisions shall in no case allow the employment of a person below\neighteen (18) years of age in an undertaking which is hazardous or deleterious in nature as\ndetermined by the Secretary of Labor and Employment."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter II - EMPLOYMENT OF MINORS"
    ],
    "language": "en",
    "old_article_number": "139"
  },
  {
    "article": "Art. 138",
    "title": "Prohibition Against Child Discrimination",
    "category": "Labor Law - Book 3",
    "simplified_text": "No employer shall\ndiscriminate against any person in respect to terms and conditions of employment on account\nof his age.",
    "chunks": [
      "No employer shall\ndiscriminate against any person in respect to terms and conditions of employment on account\nof his age."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter II - EMPLOYMENT OF MINORS"
    ],
    "language": "en",
    "old_article_number": "140"
  },
  {
    "article": "Art. 139",
    "title": "Coverage",
    "category": "Labor Law - Book 3",
    "simplified_text": "This Chapter shall apply to all persons rendering services\nin households for compensation.\n\n\"Domestic or household service\" shall mean service in the employer’s home which is\nusually necessary or desirable for the maintenance and enjoyment thereof and includes\nministering to the personal comfort and convenience of the members of the employer’s\nhousehold, including services of family drivers.",
    "chunks": [
      "This Chapter shall apply to all persons rendering services\nin households for compensation.",
      "\"Domestic or household service\" shall mean service in the employer’s home which is\nusually necessary or desirable for the maintenance and enjoyment thereof and includes\nministering to the personal comfort and convenience of the members of the employer’s\nhousehold, including services of family drivers."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "141"
  },
  {
    "article": "Art. 140",
    "title": "Contract of Domestic Service",
    "category": "Labor Law - Book 3",
    "simplified_text": "The original contract of domestic\nservice shall not last for more than two (2) years but it may be renewed for such periods as\nmay be agreed upon by the parties.",
    "chunks": [
      "The original contract of domestic\nservice shall not last for more than two (2) years but it may be renewed for such periods as\nmay be agreed upon by the parties."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "142"
  },
  {
    "article": "Art. 141",
    "title": "Minimum Wage",
    "category": "Labor Law - Book 3",
    "simplified_text": "(a) Househelpers shall be paid the following\nminimum wage rates:\n\n(1) Eight hundred pesos (P800.00) a month for househelpers in Manila, Quezon, Pasay,\nand Caloocan cities and municipalities of Makati, San Juan, Mandaluyong, Muntinlupa,\nNavotas, Malabon, Parañaque, Las Piñas, Pasig, Marikina, Valenzuela, Taguig and Pateros in\nMetro Manila and in highly urbanized cities;\n\n(2) Six hundred fifty pesos (P650.00) a month for those in other chartered cities and first-\nclass municipalities; and\n\n(3) Five hundred fifty pesos (P550.00) a month for those in other municipalities.\n\nProvided, That the employers shall review the employment contracts of their\nhousehelpers every three (3) years with the end in view of improving the terms and conditions\nthereof.\n\nProvided, further, That those househelpers who are receiving at least One Thousand\npesos (P1,000.00) shall be covered by the Social Security System (SSS) and be entitled to all\nthe benefits provided thereunder.",
    "chunks": [
      "(a) Househelpers shall be paid the following\nminimum wage rates:",
      "(1) Eight hundred pesos (P800.00) a month for househelpers in Manila, Quezon, Pasay,\nand Caloocan cities and municipalities of Makati, San Juan, Mandaluyong, Muntinlupa,\nNavotas, Malabon, Parañaque, Las Piñas, Pasig, Marikina, Valenzuela, Taguig and Pateros in\nMetro Manila and in highly urbanized cities;",
      "(2) Six hundred fifty pesos (P650.00) a month for those in other chartered cities and first-\nclass municipalities; and",
      "(3) Five hundred fifty pesos (P550.00) a month for those in other municipalities.",
      "Provided, That the employers shall review the employment contracts of their\nhousehelpers every three (3) years with the end in view of improving the terms and conditions\nthereof.",
      "Provided, further, That those househelpers who are receiving at least One Thousand\npesos (P1,000.00) shall be covered by the Social Security System (SSS) and be entitled to all\nthe benefits provided thereunder."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "143"
  },
  {
    "article": "Art. 142",
    "title": "Minimum Cash Wage",
    "category": "Labor Law - Book 3",
    "simplified_text": "The minimum wage rates prescribed under this\nChapter shall be the basic cash wages which shall be paid to the househelpers in addition to\nlodging, food and medical attendance.",
    "chunks": [
      "The minimum wage rates prescribed under this\nChapter shall be the basic cash wages which shall be paid to the househelpers in addition to\nlodging, food and medical attendance."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "144"
  },
  {
    "article": "Art. 143",
    "title": "Assignment to Non-Household Work",
    "category": "Labor Law - Book 3",
    "simplified_text": "No househelper shall be\nassigned to work in a commercial, industrial or agricultural enterprise at a wage or salary rate\nlower than that provided for agricultural or non-agricultural workers as prescribed herein.",
    "chunks": [
      "No househelper shall be\nassigned to work in a commercial, industrial or agricultural enterprise at a wage or salary rate\nlower than that provided for agricultural or non-agricultural workers as prescribed herein."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "145"
  },
  {
    "article": "Art. 144",
    "title": "Opportunity for Education",
    "category": "Labor Law - Book 3",
    "simplified_text": "If the househelper is under the age of\neighteen (18) years, the employer shall give him or her an opportunity for at least elementary\n\neducation. The cost of education shall be part of the househelper’s compensation, unless\nthere is a stipulation to the contrary.",
    "chunks": [
      "If the househelper is under the age of\neighteen (18) years, the employer shall give him or her an opportunity for at least elementary",
      "education. The cost of education shall be part of the househelper’s compensation, unless\nthere is a stipulation to the contrary."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "146"
  },
  {
    "article": "Art. 145",
    "title": "Treatment of Househelpers",
    "category": "Labor Law - Book 3",
    "simplified_text": "The employer shall treat the\nhousehelper in a just and humane manner. In no case shall physical violence be used upon the\nhousehelper.",
    "chunks": [
      "The employer shall treat the\nhousehelper in a just and humane manner. In no case shall physical violence be used upon the\nhousehelper."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "147"
  },
  {
    "article": "Art. 146",
    "title": "Board, Lodging, and Medical Attendance",
    "category": "Labor Law - Book 3",
    "simplified_text": "The employer shall furnish\nthe househelper, free of charge, suitable and sanitary living quarters as well as adequate food\nand medical attendance.",
    "chunks": [
      "The employer shall furnish\nthe househelper, free of charge, suitable and sanitary living quarters as well as adequate food\nand medical attendance."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "148"
  },
  {
    "article": "Art. 147",
    "title": "Indemnity for Unjust Termination of Services",
    "category": "Labor Law - Book 3",
    "simplified_text": "If the period of\nhousehold service is fixed, neither the employer nor the househelper may terminate the\ncontract before the expiration of the term, except for a just cause. If the househelper is\nunjustly dismissed, he or she shall be paid the compensation already earned plus that for\n\nfifteen (15) days by way of indemnity.\n\nIf the househelper leaves without justifiable reason, he or she shall forfeit any unpaid\nsalary due him or her not exceeding fifteen (15) days.",
    "chunks": [
      "If the period of\nhousehold service is fixed, neither the employer nor the househelper may terminate the\ncontract before the expiration of the term, except for a just cause. If the househelper is\nunjustly dismissed, he or she shall be paid the compensation already earned plus that for",
      "fifteen (15) days by way of indemnity.",
      "If the househelper leaves without justifiable reason, he or she shall forfeit any unpaid\nsalary due him or her not exceeding fifteen (15) days."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "149"
  },
  {
    "article": "Art. 148",
    "title": "Service of Termination Notice",
    "category": "Labor Law - Book 3",
    "simplified_text": "If the duration of the household\nservice is not determined either in stipulation or by the nature of the service, the employer or\nthe househelper may give notice to put an end to the relationship five (5) days before the\nintended termination of the service.",
    "chunks": [
      "If the duration of the household\nservice is not determined either in stipulation or by the nature of the service, the employer or\nthe househelper may give notice to put an end to the relationship five (5) days before the\nintended termination of the service."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "150"
  },
  {
    "article": "Art. 149",
    "title": "Employment Certification",
    "category": "Labor Law - Book 3",
    "simplified_text": "Upon the severance of the household\nservice relation, the employer shall give the househelper a written statement of the nature\nand duration of the service and his or her efficiency and conduct as househelper.",
    "chunks": [
      "Upon the severance of the household\nservice relation, the employer shall give the househelper a written statement of the nature\nand duration of the service and his or her efficiency and conduct as househelper."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "151"
  },
  {
    "article": "Art. 150",
    "title": "Employment Record",
    "category": "Labor Law - Book 3",
    "simplified_text": "The employer may keep such records as he may\ndeem necessary to reflect the actual terms and conditions of employment of his househelper,\nwhich the latter shall authenticate by signature or thumbmark upon request of the employer.",
    "chunks": [
      "The employer may keep such records as he may\ndeem necessary to reflect the actual terms and conditions of employment of his househelper,\nwhich the latter shall authenticate by signature or thumbmark upon request of the employer."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter III - EMPLOYMENT OF HOUSEHELPERS"
    ],
    "language": "en",
    "old_article_number": "152"
  },
  {
    "article": "Art. 151",
    "title": "Regulation of Industrial Homeworkers",
    "category": "Labor Law - Book 3",
    "simplified_text": "The employment of industrial\nhomeworkers and field personnel shall be regulated by the government through the\nappropriate regulations issued by the Secretary of Labor and Employment to ensure the\ngeneral welfare and protection of homeworkers and field personnel and the industries\nemploying them.",
    "chunks": [
      "The employment of industrial\nhomeworkers and field personnel shall be regulated by the government through the\nappropriate regulations issued by the Secretary of Labor and Employment to ensure the\ngeneral welfare and protection of homeworkers and field personnel and the industries\nemploying them."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter IV - EMPLOYMENT OF HOMEWORKERS"
    ],
    "language": "en",
    "old_article_number": "153"
  },
  {
    "article": "Art. 152",
    "title": "Regulations of Secretary of Labor",
    "category": "Labor Law - Book 3",
    "simplified_text": "The regulations or orders to be issued\npursuant to this Chapter shall be designed to assure the minimum terms and conditions of\nemployment applicable to the industrial homeworkers or field personnel involved.",
    "chunks": [
      "The regulations or orders to be issued\npursuant to this Chapter shall be designed to assure the minimum terms and conditions of\nemployment applicable to the industrial homeworkers or field personnel involved."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter IV - EMPLOYMENT OF HOMEWORKERS"
    ],
    "language": "en",
    "old_article_number": "154"
  },
  {
    "article": "Art. 153",
    "title": "Distribution of Homework",
    "category": "Labor Law - Book 3",
    "simplified_text": "For purposes of this Chapter, the\n\"employer\" of homeworkers includes any person, natural or artificial who, for his account or\nbenefit, or on behalf of any person residing outside the country, directly or indirectly, or\nthrough an employee, agent contractor, sub-contractor or any other person:\n\n(1) Delivers, or causes to be delivered, any goods, articles or materials to be processed\nor fabricated in or about a home and thereafter to be returned or to be disposed of or\ndistributed in accordance with his directions; or\n\n(2) Sells any goods, articles or materials to be processed or fabricated in or about a home\nand then rebuys them after such processing or fabrication, either by himself or through some\nother person.",
    "chunks": [
      "For purposes of this Chapter, the\n\"employer\" of homeworkers includes any person, natural or artificial who, for his account or\nbenefit, or on behalf of any person residing outside the country, directly or indirectly, or\nthrough an employee, agent contractor, sub-contractor or any other person:",
      "(1) Delivers, or causes to be delivered, any goods, articles or materials to be processed\nor fabricated in or about a home and thereafter to be returned or to be disposed of or\ndistributed in accordance with his directions; or",
      "(2) Sells any goods, articles or materials to be processed or fabricated in or about a home\nand then rebuys them after such processing or fabrication, either by himself or through some\nother person."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter IV - EMPLOYMENT OF HOMEWORKERS"
    ],
    "language": "en",
    "old_article_number": "155"
  },
  {
    "article": "Art. 154",
    "title": "Coverage",
    "category": "Labor Law - Book 3",
    "simplified_text": "This chapter shall apply to all persons, who shall be employed or\npermitted or suffered to work at night, except those employed in agriculture, stock raising,\nfishing, maritime transport and inland navigation, during a period of not less than seven (7)\nconsecutive hours, including the interval from midnight to five o’clock in the morning, to be\ndetermined by the Secretary of Labor and Employment, after consulting the workers’\nrepresentatives/labor organizations and employers.\n\n“Night worker” means any employed person whose work requires performance of a\nsubstantial number of hours of night work which exceeds a specified limit. This limit shall be\n\nfixed by the Secretary of Labor after consulting the workers’ representatives/labor\norganizations and employers.",
    "chunks": [
      "This chapter shall apply to all persons, who shall be employed or\npermitted or suffered to work at night, except those employed in agriculture, stock raising,\nfishing, maritime transport and inland navigation, during a period of not less than seven (7)\nconsecutive hours, including the interval from midnight to five o’clock in the morning, to be\ndetermined by the Secretary of Labor and Employment, after consulting the workers’\nrepresentatives/labor organizations and employers.",
      "“Night worker” means any employed person whose work requires performance of a\nsubstantial number of hours of night work which exceeds a specified limit. This limit shall be",
      "fixed by the Secretary of Labor after consulting the workers’ representatives/labor\norganizations and employers."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 155",
    "title": "Health Assessment",
    "category": "Labor Law - Book 3",
    "simplified_text": "At their request, workers shall have the right to undergo\na health assessment without charge and to receive advice on how to reduce or avoid health\nproblems associated with their work:\n\n(a) Before taking up an assignment as a night worker;\n\n(b) At regular intervals during such an assignment; and\n\n(c) If they experience health problems during such an assignment which are not caused\nby factors other than the performance of night work.\n\nWith the exception of a finding of unfitness for night work, the findings of such\nassessments shall not be transmitted to others without the workers’ consent and shall not be\nused to their detriment.",
    "chunks": [
      "At their request, workers shall have the right to undergo\na health assessment without charge and to receive advice on how to reduce or avoid health\nproblems associated with their work:",
      "(a) Before taking up an assignment as a night worker;",
      "(b) At regular intervals during such an assignment; and",
      "(c) If they experience health problems during such an assignment which are not caused\nby factors other than the performance of night work.",
      "With the exception of a finding of unfitness for night work, the findings of such\nassessments shall not be transmitted to others without the workers’ consent and shall not be\nused to their detriment."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 156",
    "title": "Mandatory Facilities",
    "category": "Labor Law - Book 3",
    "simplified_text": "Suitable first-aid facilities shall be made available for\nworkers performing night work, including arrangements where such workers, where\nnecessary, can be taken immediately to a place for appropriate treatment. The employers are\nlikewise required to provide safe and healthful working conditions and adequate or reasonable\nfacilities such as sleeping or resting quarters in the establishment and transportation from the\nwork premises to the nearest point of their residence subject to exceptions and guidelines to\nbe provided by the DOLE.",
    "chunks": [
      "Suitable first-aid facilities shall be made available for\nworkers performing night work, including arrangements where such workers, where\nnecessary, can be taken immediately to a place for appropriate treatment. The employers are\nlikewise required to provide safe and healthful working conditions and adequate or reasonable\nfacilities such as sleeping or resting quarters in the establishment and transportation from the\nwork premises to the nearest point of their residence subject to exceptions and guidelines to\nbe provided by the DOLE."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 157",
    "title": "Transfer",
    "category": "Labor Law - Book 3",
    "simplified_text": "Night workers who are certified as unfit for night work, due to health\nreasons, shall be transferred, whenever practicable, to a similar job for which they are fit to\nwork.\n\nIf such transfer to a similar job is not practicable, these workers shall be granted the same\nbenefits as other workers who are unable to work, or to secure employment during such\nperiod.\n\nA night worker certified as temporarily unfit for night work shall be given the same\nprotection against dismissal or notice of dismissal as other workers who are prevented from\nworking for reasons of health.",
    "chunks": [
      "Night workers who are certified as unfit for night work, due to health\nreasons, shall be transferred, whenever practicable, to a similar job for which they are fit to\nwork.",
      "If such transfer to a similar job is not practicable, these workers shall be granted the same\nbenefits as other workers who are unable to work, or to secure employment during such\nperiod.",
      "A night worker certified as temporarily unfit for night work shall be given the same\nprotection against dismissal or notice of dismissal as other workers who are prevented from\nworking for reasons of health."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 158",
    "title": "Women Night Workers",
    "category": "Labor Law - Book 3",
    "simplified_text": "Measures shall be taken to ensure that an alternative\nto night work is available to women workers who would otherwise be called upon to perform\nsuch work:\n\n(a) Before and after childbirth, for a period of at least sixteen (16) weeks, which shall be\ndivided between the time before and after childbirth;\n\n(b) For additional periods, in respect of which a medical certificate is produced stating\nthat said additional periods are necessary for the health of the mother or child:\n\n(1) During pregnancy;\n\n(2) During a specified time beyond the period, after childbirth is fixed pursuant to\nsubparagraph (a) above, the length of which shall be determined by the DOLE after\nconsulting the labor organizations and employers.\n\nDuring the periods referred to in this article:\n\n(i) A woman worker shall not be dismissed or given notice of dismissal, except for\njust or authorized causes provided for in this Code that are not connected with pregnancy,\nchildbirth and childcare responsibilities.\n\n(ii) A woman worker shall not lose the benefits regarding her status, seniority, and\naccess to promotion which may attach to her regular night work position.\n\nPregnant women and nursing mothers may be allowed to work at night only if a\ncompetent physician, other than the company physician, shall certify their fitness to render\nnight work, and specify, in the case of pregnant employees, the period of the pregnancy that\nthey can safely work.\n\nThe measures referred to in this article may include transfer to day work where this is\npossible, the provision of social security benefits or an extension of maternity leave.\n\nThe provisions of this article shall not have the effect of reducing the protection and\nbenefits connected with maternity leave under existing laws.",
    "chunks": [
      "Measures shall be taken to ensure that an alternative\nto night work is available to women workers who would otherwise be called upon to perform\nsuch work:",
      "(a) Before and after childbirth, for a period of at least sixteen (16) weeks, which shall be\ndivided between the time before and after childbirth;",
      "(b) For additional periods, in respect of which a medical certificate is produced stating\nthat said additional periods are necessary for the health of the mother or child:",
      "(1) During pregnancy;",
      "(2) During a specified time beyond the period, after childbirth is fixed pursuant to\nsubparagraph (a) above, the length of which shall be determined by the DOLE after\nconsulting the labor organizations and employers.",
      "During the periods referred to in this article:",
      "(i) A woman worker shall not be dismissed or given notice of dismissal, except for\njust or authorized causes provided for in this Code that are not connected with pregnancy,\nchildbirth and childcare responsibilities.",
      "(ii) A woman worker shall not lose the benefits regarding her status, seniority, and\naccess to promotion which may attach to her regular night work position.",
      "Pregnant women and nursing mothers may be allowed to work at night only if a\ncompetent physician, other than the company physician, shall certify their fitness to render\nnight work, and specify, in the case of pregnant employees, the period of the pregnancy that\nthey can safely work.",
      "The measures referred to in this article may include transfer to day work where this is\npossible, the provision of social security benefits or an extension of maternity leave.",
      "The provisions of this article shall not have the effect of reducing the protection and\nbenefits connected with maternity leave under existing laws."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 159",
    "title": "Compensation",
    "category": "Labor Law - Book 3",
    "simplified_text": "The compensation for night workers in the form of working\ntime, pay or similar benefits shall recognize the exceptional nature of night work.",
    "chunks": [
      "The compensation for night workers in the form of working\ntime, pay or similar benefits shall recognize the exceptional nature of night work."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 160",
    "title": "Social Services",
    "category": "Labor Law - Book 3",
    "simplified_text": "Appropriate social services shall be provided for night workers\nand, where necessary, for workers performing night work.",
    "chunks": [
      "Appropriate social services shall be provided for night workers\nand, where necessary, for workers performing night work."
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 161",
    "title": "Night Work Schedules",
    "category": "Labor Law - Book 3",
    "simplified_text": "Before introducing work schedules requiring the\nservices of night workers, the employer shall consult the workers' representatives/labor\norganizations concerned on the details of such schedules and the forms of organization of\nnight work that are best adapted to the establishment and its personnel, as well as on the\n\noccupational health measures and social services which are required. In establishments\n\nemploying night workers, consultation shall take place regularly.\n\nSAFETY",
    "chunks": [
      "Before introducing work schedules requiring the\nservices of night workers, the employer shall consult the workers' representatives/labor\norganizations concerned on the details of such schedules and the forms of organization of\nnight work that are best adapted to the establishment and its personnel, as well as on the",
      "occupational health measures and social services which are required. In establishments",
      "employing night workers, consultation shall take place regularly.",
      "SAFETY"
    ],
    "tags": [
      "Book Three - CONDITIONS OF EMPLOYMENT",
      "Title III - WORKING CONDITIONS FOR SPECIAL GROUPS",
      "Chapter V - EMPLOYMENT OF NIGHT WORKERS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 162",
    "title": "First-Aid Treatment",
    "category": "Labor Law - Book 4",
    "simplified_text": "Every employer shall keep in his establishment\nsuch first-aid medicines and equipment as the nature and conditions of work may require, in\n\naccordance with suchregulations as the Department of Labor and Employment shall prescribe.\n\nThe employer shall take steps for the training of a sufficient number of employees in first-\naid treatment.",
    "chunks": [
      "Every employer shall keep in his establishment\nsuch first-aid medicines and equipment as the nature and conditions of work may require, in",
      "accordance with suchregulations as the Department of Labor and Employment shall prescribe.",
      "The employer shall take steps for the training of a sufficient number of employees in first-\naid treatment."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter I - MEDICAL AND DENTAL SERVICES"
    ],
    "language": "en",
    "old_article_number": "156"
  },
  {
    "article": "Art. 163",
    "title": "Emergency Medical and Dental Services",
    "category": "Labor Law - Book 4",
    "simplified_text": "It shall be the duty of every\nemployer to furnish his employees in any locality with free medical and dental attendance and\nfacilities consisting of:\n\n(a) The services of a full-time registered nurse when the number of employees exceeds\nfifty (50) but not more than two hundred (200) except when the employer does not maintain\nhazardous workplaces, in which case, the services of a graduate first-aider shall be provided\nfor the protection of workers, where no registered nurse is available. The Secretary of Labor\nand Employment shall provide by appropriate regulations the services that shall be required\nwhere the number of employees does not exceed fifty (50) and shall determine by appropriate\norder, hazardous workplaces for purposes of this Article;\n\n(b) The services of a full-time registered nurse, a part-time physician and dentist, and an\nemergency clinic, when the number of employees exceeds two hundred (200) but not more\nthan three hundred (300); and\n\n(c) The services of a full-time physician, dentist and a full-time registered nurse as well as\na dental clinic and an infirmary or emergency hospital with one bed capacity for every one\nhundred (100) employees when the number of employees exceeds three hundred (300).\n\nIn cases of hazardous workplaces, no employer shall engage the services of a physician or\na dentist who cannot stay in the premises of the establishment for at least two (2) hours, in\nthe case of those engaged on part-time basis, and not less than eight (8) hours, in the case of\nthose employed on full-time basis. Where the undertaking is non-hazardous in nature, the\nphysician and dentist may be engaged on retained basis, subject to such regulations as the\nSecretary of Labor and Employment may prescribe to insure immediate availability of medical\nand dental treatment and attendance in case of emergency.",
    "chunks": [
      "It shall be the duty of every\nemployer to furnish his employees in any locality with free medical and dental attendance and\nfacilities consisting of:",
      "(a) The services of a full-time registered nurse when the number of employees exceeds\nfifty (50) but not more than two hundred (200) except when the employer does not maintain\nhazardous workplaces, in which case, the services of a graduate first-aider shall be provided\nfor the protection of workers, where no registered nurse is available. The Secretary of Labor\nand Employment shall provide by appropriate regulations the services that shall be required\nwhere the number of employees does not exceed fifty (50) and shall determine by appropriate\norder, hazardous workplaces for purposes of this Article;",
      "(b) The services of a full-time registered nurse, a part-time physician and dentist, and an\nemergency clinic, when the number of employees exceeds two hundred (200) but not more\nthan three hundred (300); and",
      "(c) The services of a full-time physician, dentist and a full-time registered nurse as well as\na dental clinic and an infirmary or emergency hospital with one bed capacity for every one\nhundred (100) employees when the number of employees exceeds three hundred (300).",
      "In cases of hazardous workplaces, no employer shall engage the services of a physician or\na dentist who cannot stay in the premises of the establishment for at least two (2) hours, in\nthe case of those engaged on part-time basis, and not less than eight (8) hours, in the case of\nthose employed on full-time basis. Where the undertaking is non-hazardous in nature, the\nphysician and dentist may be engaged on retained basis, subject to such regulations as the\nSecretary of Labor and Employment may prescribe to insure immediate availability of medical\nand dental treatment and attendance in case of emergency."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter I - MEDICAL AND DENTAL SERVICES"
    ],
    "language": "en",
    "old_article_number": "157"
  },
  {
    "article": "Art. 164",
    "title": "When Emergency Hospital Not Required",
    "category": "Labor Law - Book 4",
    "simplified_text": "The requirement for an\nemergency hospital or dental clinic shall not be applicable in case there is a hospital or dental\nclinic which is accessible from the employer’s establishment and he makes arrangement for\nthe reservation therein of the necessary beds and dental facilities for the use of his employees.",
    "chunks": [
      "The requirement for an\nemergency hospital or dental clinic shall not be applicable in case there is a hospital or dental\nclinic which is accessible from the employer’s establishment and he makes arrangement for\nthe reservation therein of the necessary beds and dental facilities for the use of his employees."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter I - MEDICAL AND DENTAL SERVICES"
    ],
    "language": "en",
    "old_article_number": "158"
  },
  {
    "article": "Art. 165",
    "title": "Health Program",
    "category": "Labor Law - Book 4",
    "simplified_text": "The physician engaged by an employer shall, in\naddition to his duties under this Chapter, develop and implement a comprehensive\noccupational health program for the benefit of the employees of his employer.",
    "chunks": [
      "The physician engaged by an employer shall, in\naddition to his duties under this Chapter, develop and implement a comprehensive\noccupational health program for the benefit of the employees of his employer."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter I - MEDICAL AND DENTAL SERVICES"
    ],
    "language": "en",
    "old_article_number": "159"
  },
  {
    "article": "Art. 166",
    "title": "Qualifications of Health Personnel",
    "category": "Labor Law - Book 4",
    "simplified_text": "The physicians, dentists and nurses\nemployed by employers pursuant to this Chapter shall have the necessary training in industrial\nmedicine and occupational safety and health. The Secretary of Labor and Employment, in\nconsultation with industrial, medical, and occupational safety and health associations, shall\nestablish the qualifications, criteria and conditions of employment of such health personnel.",
    "chunks": [
      "The physicians, dentists and nurses\nemployed by employers pursuant to this Chapter shall have the necessary training in industrial\nmedicine and occupational safety and health. The Secretary of Labor and Employment, in\nconsultation with industrial, medical, and occupational safety and health associations, shall\nestablish the qualifications, criteria and conditions of employment of such health personnel."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter I - MEDICAL AND DENTAL SERVICES"
    ],
    "language": "en",
    "old_article_number": "160"
  },
  {
    "article": "Art. 167",
    "title": "Assistance of Employer",
    "category": "Labor Law - Book 4",
    "simplified_text": "It shall be the duty of any employer to provide\nall the necessary assistance to ensure the adequate and immediate medical and dental\nattendance and treatment to an injured or sick employee in case of emergency.",
    "chunks": [
      "It shall be the duty of any employer to provide\nall the necessary assistance to ensure the adequate and immediate medical and dental\nattendance and treatment to an injured or sick employee in case of emergency."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter I - MEDICAL AND DENTAL SERVICES"
    ],
    "language": "en",
    "old_article_number": "161"
  },
  {
    "article": "Art. 168",
    "title": "Safety and Health Standards",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Secretary of Labor and Employment\nshall, by appropriate orders, set and enforce mandatory occupational safety and health\nstandards to eliminate or reduce occupational safety and health hazards in all workplaces and\ninstitute new, and update existing, programs to ensure safe and healthful working conditions\nin all places of employment.",
    "chunks": [
      "The Secretary of Labor and Employment\nshall, by appropriate orders, set and enforce mandatory occupational safety and health\nstandards to eliminate or reduce occupational safety and health hazards in all workplaces and\ninstitute new, and update existing, programs to ensure safe and healthful working conditions\nin all places of employment."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter II - OCCUPATIONAL HEALTH AND SAFETY"
    ],
    "language": "en",
    "old_article_number": "162"
  },
  {
    "article": "Art. 169",
    "title": "Research",
    "category": "Labor Law - Book 4",
    "simplified_text": "It shall be the responsibility of the Department of Labor and\nEmployment to conduct continuing studies and research to develop innovative methods,\ntechniques and approaches for dealing with occupational safety and health problems; to\ndiscover latent diseases by establishing causal connections between diseases and work in\nenvironmental conditions; and to develop medical criteria which will assure insofar as\npracticable that no employee will suffer impairment or diminution in health, functional\ncapacity, or life expectancy as a result of his work and working conditions.",
    "chunks": [
      "It shall be the responsibility of the Department of Labor and\nEmployment to conduct continuing studies and research to develop innovative methods,\ntechniques and approaches for dealing with occupational safety and health problems; to\ndiscover latent diseases by establishing causal connections between diseases and work in\nenvironmental conditions; and to develop medical criteria which will assure insofar as\npracticable that no employee will suffer impairment or diminution in health, functional\ncapacity, or life expectancy as a result of his work and working conditions."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter II - OCCUPATIONAL HEALTH AND SAFETY"
    ],
    "language": "en",
    "old_article_number": "163"
  },
  {
    "article": "Art. 170",
    "title": "Training Programs",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Department of Labor and Employment shall\ndevelop and implement training programs to increase the number and competence of\npersonnel in the field of occupational safety and industrial health.",
    "chunks": [
      "The Department of Labor and Employment shall\ndevelop and implement training programs to increase the number and competence of\npersonnel in the field of occupational safety and industrial health."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter II - OCCUPATIONAL HEALTH AND SAFETY"
    ],
    "language": "en",
    "old_article_number": "164"
  },
  {
    "article": "Art. 171",
    "title": "Administration of Safety and Health Laws",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) The Department of\nLabor shall be solely responsible for the administration and enforcement of occupational\nsafety and health laws, regulations and standards in all establishments and workplaces\nwherever they may be located; however, chartered cities may be allowed to conduct industrial\nsafety inspections of establishments within their respective jurisdictions where they have\nadequate facilities and competent personnel for the purpose as determined by the\nDepartment of Labor and subject to national standards established by the latter.\n\n(b) The Secretary of Labor may, through appropriate regulations, collect reasonable fees\nfor the inspection of steam boilers, pressure vessels and pipings and electrical installations,\nthe test and approval for safe use of materials, equipment and other safety devices and the\napproval of plans for such materials, equipment and devices. The fee so collected shall be\ndeposited in the national treasury to the credit of the occupational safety and health fund and\nshall be expended exclusively for the administration and enforcement of safety and other\nlabor laws administered by the Department of Labor.",
    "chunks": [
      "(a) The Department of\nLabor shall be solely responsible for the administration and enforcement of occupational\nsafety and health laws, regulations and standards in all establishments and workplaces\nwherever they may be located; however, chartered cities may be allowed to conduct industrial\nsafety inspections of establishments within their respective jurisdictions where they have\nadequate facilities and competent personnel for the purpose as determined by the\nDepartment of Labor and subject to national standards established by the latter.",
      "(b) The Secretary of Labor may, through appropriate regulations, collect reasonable fees\nfor the inspection of steam boilers, pressure vessels and pipings and electrical installations,\nthe test and approval for safe use of materials, equipment and other safety devices and the\napproval of plans for such materials, equipment and devices. The fee so collected shall be\ndeposited in the national treasury to the credit of the occupational safety and health fund and\nshall be expended exclusively for the administration and enforcement of safety and other\nlabor laws administered by the Department of Labor."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title I - MEDICAL, DENTAL AND OCCUPATIONAL",
      "Chapter II - OCCUPATIONAL HEALTH AND SAFETY"
    ],
    "language": "en",
    "old_article_number": "165"
  },
  {
    "article": "Art. 172",
    "title": "Policy",
    "category": "Labor Law - Book 4",
    "simplified_text": "The State shall promote and develop a tax-exempt employees’\ncompensation program whereby employees and their dependents, in the event of work-\nconnected disability or death, may promptly secure adequate income benefit and medical\nrelated benefits.",
    "chunks": [
      "The State shall promote and develop a tax-exempt employees’\ncompensation program whereby employees and their dependents, in the event of work-\nconnected disability or death, may promptly secure adequate income benefit and medical\nrelated benefits."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter I - POLICY AND DEFINITIONS"
    ],
    "language": "en",
    "old_article_number": "166"
  },
  {
    "article": "Art. 173",
    "title": "Definition of Terms",
    "category": "Labor Law - Book 4",
    "simplified_text": "As used in this Title, unless the context indicates\notherwise:\n\n(a) \"Code\" means the Labor Code of the Philippines instituted under Presidential Decree\nNumbered Four Hundred Forty-Two, as amended.\n\n(b) \"Commission\" means the Employees’ Compensation Commission created under this\nTitle.\n\n(c) \"SSS\" means the Social Security System created under Republic Act Numbered Eleven\nHundred Sixty-One, as amended.\n\n(d) \"GSIS\" means the Government Service Insurance System created under\nCommonwealth Act Numbered One Hundred Eighty-Six, as amended.\n\n(e) \"System\" means the SSS or GSIS, as the case may be.\n\n(f) \"Employer\" means any person, natural or juridical, employing the services of the\nemployee.\n\n(g) \"Employee\" means any person compulsorily covered by the GSIS under\nCommonwealth Act Numbered One Hundred Eighty-Six, as amended, including the members\nof the Armed Forces of the Philippines, and any person employed as casual, emergency,\ntemporary, substitute or contractual, or any person compulsorily covered by the SSS under\nRepublic Act Numbered Eleven Hundred Sixty-One, as amended.\n\n(h) \"Person\" means any individual, partnership, firm, association, trust, corporation or\nlegal representative thereof.\n\n(i) \"Dependents\" means the legitimate, legitimated, legally adopted or acknowledged\nnatural child who is unmarried, not gainfully employed, and not over twenty-one years of age\nor over twenty-one years of age provided he is incapable of self-support due to a physical or\nmental defect which is congenital or acquired during minority; the legitimate spouse living\nwith the employee; and the parents of said employee wholly dependent upon him for regular\nsupport.\n\n(j) \"Beneficiaries\" means the dependent spouse until he/she remarries and dependent\nchildren, who are the primary beneficiaries. In their absence, the dependent parents and\nsubject to the restrictions imposed on dependent children, the illegitimate children and\nlegitimate descendants, who are the secondary beneficiaries: Provided, That the dependent\nacknowledged natural child shall be considered as a primary beneficiary when there are no\nother dependent children who are qualified and eligible for monthly income benefit.\n\n(k) \"Injury\" means any harmful change in the human organism from any accident arising\nout of and in the course of the employment.\n\n(l) \"Sickness\" means any illness definitely accepted as an occupational disease listed by\nthe Commission, or any illness caused by employment subject to proof that the risk of\ncontracting the same is increased by working conditions. For this purpose, the Commission is\n\nempowered to determine and approve occupational diseases and work-related illnesses that\nmay be considered compensable based on peculiar hazards of employment.\n\n(m) \"Death\" means loss of life resulting from injury or sickness.\n\n(n) \"Disability\" means loss or impairment of a physical or mental function resulting from\ninjury or sickness.\n\n(o) \"Compensation\" means all payments made under this Title for income benefits and\nmedical or related benefits.\n\n(p) \"Income benefit\" means all payments made under this Title to the employee or his\ndependents.\n\n(q) \"Medical benefit\" means all payments made under this Title to the providers of\nmedical care, rehabilitation services and hospital care.\n\n(r) \"Related benefit\" means all payments made under this Title for appliances and\nsupplies.\n\n(s) \"Appliances\" means crutches, artificial aids and other similar devices.\n\n(t) \"Supplies\" means medicine and other medical, dental or surgical items.\n\n(u) \"Hospital\" means any medical facility, government or private, authorized by law, an\nactive member in good standing of the Philippine Hospital Association and accredited by the\nCommission.\n\n(v) \"Physician\" means any doctor of medicine duly licensed to practice in the Philippines,\nan active member in good standing of the Philippine Medical Association and accredited by\nthe Commission.\n\n(w) \"Wages\" or \"Salary\", insofar as they refer to the computation of benefits, means the\nmonthly remuneration as defined in Republic Act No. 1161, as amended, for SSS and\nPresidential Decree No. 1146, as amended, for GSIS, respectively, except that part in excess of\nThree Thousand Pesos.\n\n(x) \"Monthly salary credit\" means the wage or salary base for contributions as provided\nin Republic Act Numbered Eleven hundred sixty-one, as amended, or the wages or salary.\n\n(y) \"Average monthly salary credit\" in the case of the SSS means the result obtained by\ndividing the sum of the monthly salary credits in the sixty-month period immediately\n\npreceding the semester of death or permanent disability by sixty (60), except where the month\nof death or permanent disability falls within eighteen (18) calendar months from the month\nof coverage, in which case it is the result obtained by dividing the sum of all monthly salary\ncredits paid prior to the month of the contingency by the total number of calendar months of\ncoverage in the same period.\n\n(z) \"Average daily salary credit\" in the case of the SSS means the result obtained by\ndividing the sum of the six (6) highest monthly salary credits in the twelve-month period\nimmediately preceding the semester of sickness or injury by one hundred eighty (180), except\nwhere the month of injury falls within twelve (12) calendar months from the first month of\ncoverage, in which case it is the result obtained by dividing the sum of all monthly salary credits\nby thirty (30) times the number of calendar months of coverage in the period.\n\nIn the case of the GSIS, the average daily salary credit shall be the actual daily salary or\nwage, or the monthly salary or wage divided by the actual number of working days of the\nmonth of contingency.\n\n(aa) \"Quarter\" means a period of three (3) consecutive months ending on the last days of\nMarch, June, September and December.\n\n(bb) \"Semester\" means a period of two consecutive quarters ending in the quarter of\ndeath, permanent disability, injury or sickness.\n\n(cc) \"Replacement ratio\" - The sum of twenty percent and the quotient obtained by\ndividing three hundred by the sum of three hundred forty and the average monthly salary\ncredit.\n\n(dd) \"Credited years of service\" - For a member covered prior to January, 1975, nineteen\nhundred seventy-five minus the calendar year of coverage, plus the number of calendar years\nin which six or more contributions have been paid from January, 1975 up to the calendar year\ncontaining the semester prior to the contingency. For a member covered on or after January,\n1975, the number of calendar years in which six or more contributions have been paid from\nthe year of coverage up to the calendar year containing the semester prior to the contingency.\n\n(ee) \"Monthly income benefit\" means the amount equivalent to one hundred fifteen\npercent of the sum of:\n\nThe average monthly salary credit multiplied by the replacement ratio; and\n\nOne and a half percent of the average monthly salary credit for each credited year of\nservice in excess of ten years;\n\nProvided, That the monthly income benefit shall in no case be less than Two Hundred Fifty\nPesos (P250.00).",
    "chunks": [
      "As used in this Title, unless the context indicates\notherwise:",
      "(a) \"Code\" means the Labor Code of the Philippines instituted under Presidential Decree\nNumbered Four Hundred Forty-Two, as amended.",
      "(b) \"Commission\" means the Employees’ Compensation Commission created under this\nTitle.",
      "(c) \"SSS\" means the Social Security System created under Republic Act Numbered Eleven\nHundred Sixty-One, as amended.",
      "(d) \"GSIS\" means the Government Service Insurance System created under\nCommonwealth Act Numbered One Hundred Eighty-Six, as amended.",
      "(e) \"System\" means the SSS or GSIS, as the case may be.",
      "(f) \"Employer\" means any person, natural or juridical, employing the services of the\nemployee.",
      "(g) \"Employee\" means any person compulsorily covered by the GSIS under\nCommonwealth Act Numbered One Hundred Eighty-Six, as amended, including the members\nof the Armed Forces of the Philippines, and any person employed as casual, emergency,\ntemporary, substitute or contractual, or any person compulsorily covered by the SSS under\nRepublic Act Numbered Eleven Hundred Sixty-One, as amended.",
      "(h) \"Person\" means any individual, partnership, firm, association, trust, corporation or\nlegal representative thereof.",
      "(i) \"Dependents\" means the legitimate, legitimated, legally adopted or acknowledged\nnatural child who is unmarried, not gainfully employed, and not over twenty-one years of age\nor over twenty-one years of age provided he is incapable of self-support due to a physical or\nmental defect which is congenital or acquired during minority; the legitimate spouse living\nwith the employee; and the parents of said employee wholly dependent upon him for regular\nsupport.",
      "(j) \"Beneficiaries\" means the dependent spouse until he/she remarries and dependent\nchildren, who are the primary beneficiaries. In their absence, the dependent parents and\nsubject to the restrictions imposed on dependent children, the illegitimate children and\nlegitimate descendants, who are the secondary beneficiaries: Provided, That the dependent\nacknowledged natural child shall be considered as a primary beneficiary when there are no\nother dependent children who are qualified and eligible for monthly income benefit.",
      "(k) \"Injury\" means any harmful change in the human organism from any accident arising\nout of and in the course of the employment.",
      "(l) \"Sickness\" means any illness definitely accepted as an occupational disease listed by\nthe Commission, or any illness caused by employment subject to proof that the risk of\ncontracting the same is increased by working conditions. For this purpose, the Commission is",
      "empowered to determine and approve occupational diseases and work-related illnesses that\nmay be considered compensable based on peculiar hazards of employment.",
      "(m) \"Death\" means loss of life resulting from injury or sickness.",
      "(n) \"Disability\" means loss or impairment of a physical or mental function resulting from\ninjury or sickness.",
      "(o) \"Compensation\" means all payments made under this Title for income benefits and\nmedical or related benefits.",
      "(p) \"Income benefit\" means all payments made under this Title to the employee or his\ndependents.",
      "(q) \"Medical benefit\" means all payments made under this Title to the providers of\nmedical care, rehabilitation services and hospital care.",
      "(r) \"Related benefit\" means all payments made under this Title for appliances and\nsupplies.",
      "(s) \"Appliances\" means crutches, artificial aids and other similar devices.",
      "(t) \"Supplies\" means medicine and other medical, dental or surgical items.",
      "(u) \"Hospital\" means any medical facility, government or private, authorized by law, an\nactive member in good standing of the Philippine Hospital Association and accredited by the\nCommission.",
      "(v) \"Physician\" means any doctor of medicine duly licensed to practice in the Philippines,\nan active member in good standing of the Philippine Medical Association and accredited by\nthe Commission.",
      "(w) \"Wages\" or \"Salary\", insofar as they refer to the computation of benefits, means the\nmonthly remuneration as defined in Republic Act No. 1161, as amended, for SSS and\nPresidential Decree No. 1146, as amended, for GSIS, respectively, except that part in excess of\nThree Thousand Pesos.",
      "(x) \"Monthly salary credit\" means the wage or salary base for contributions as provided\nin Republic Act Numbered Eleven hundred sixty-one, as amended, or the wages or salary.",
      "(y) \"Average monthly salary credit\" in the case of the SSS means the result obtained by\ndividing the sum of the monthly salary credits in the sixty-month period immediately",
      "preceding the semester of death or permanent disability by sixty (60), except where the month\nof death or permanent disability falls within eighteen (18) calendar months from the month\nof coverage, in which case it is the result obtained by dividing the sum of all monthly salary\ncredits paid prior to the month of the contingency by the total number of calendar months of\ncoverage in the same period.",
      "(z) \"Average daily salary credit\" in the case of the SSS means the result obtained by\ndividing the sum of the six (6) highest monthly salary credits in the twelve-month period\nimmediately preceding the semester of sickness or injury by one hundred eighty (180), except\nwhere the month of injury falls within twelve (12) calendar months from the first month of\ncoverage, in which case it is the result obtained by dividing the sum of all monthly salary credits\nby thirty (30) times the number of calendar months of coverage in the period.",
      "In the case of the GSIS, the average daily salary credit shall be the actual daily salary or\nwage, or the monthly salary or wage divided by the actual number of working days of the\nmonth of contingency.",
      "(aa) \"Quarter\" means a period of three (3) consecutive months ending on the last days of\nMarch, June, September and December.",
      "(bb) \"Semester\" means a period of two consecutive quarters ending in the quarter of\ndeath, permanent disability, injury or sickness.",
      "(cc) \"Replacement ratio\" - The sum of twenty percent and the quotient obtained by\ndividing three hundred by the sum of three hundred forty and the average monthly salary\ncredit.",
      "(dd) \"Credited years of service\" - For a member covered prior to January, 1975, nineteen\nhundred seventy-five minus the calendar year of coverage, plus the number of calendar years\nin which six or more contributions have been paid from January, 1975 up to the calendar year\ncontaining the semester prior to the contingency. For a member covered on or after January,\n1975, the number of calendar years in which six or more contributions have been paid from\nthe year of coverage up to the calendar year containing the semester prior to the contingency.",
      "(ee) \"Monthly income benefit\" means the amount equivalent to one hundred fifteen\npercent of the sum of:",
      "The average monthly salary credit multiplied by the replacement ratio; and",
      "One and a half percent of the average monthly salary credit for each credited year of\nservice in excess of ten years;",
      "Provided, That the monthly income benefit shall in no case be less than Two Hundred Fifty\nPesos (P250.00)."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter I - POLICY AND DEFINITIONS"
    ],
    "language": "en",
    "old_article_number": "167"
  },
  {
    "article": "Art. 174",
    "title": "Compulsory Coverage",
    "category": "Labor Law - Book 4",
    "simplified_text": "Coverage in the State Insurance Fund shall be\ncompulsory upon all employers and their employees not over sixty (60) years of age; Provided,\nThat an employee who is over sixty (60) years of age and paying contributions to qualify for\nthe retirement or life insurance benefit administered by the System shall be subject to\ncompulsory coverage.",
    "chunks": [
      "Coverage in the State Insurance Fund shall be\ncompulsory upon all employers and their employees not over sixty (60) years of age; Provided,\nThat an employee who is over sixty (60) years of age and paying contributions to qualify for\nthe retirement or life insurance benefit administered by the System shall be subject to\ncompulsory coverage."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "168"
  },
  {
    "article": "Art. 175",
    "title": "Foreign Employment",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Commission shall ensure adequate\ncoverage of Filipino employees employed abroad, subject to regulations as it may prescribe.",
    "chunks": [
      "The Commission shall ensure adequate\ncoverage of Filipino employees employed abroad, subject to regulations as it may prescribe."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "169"
  },
  {
    "article": "Art. 176",
    "title": "Effective Date of Coverage",
    "category": "Labor Law - Book 4",
    "simplified_text": "Compulsory coverage of the employer\nduring the effectivity of this Title shall take effect on the first day of his operation, and that of\nthe employee, on the date of his employment.",
    "chunks": [
      "Compulsory coverage of the employer\nduring the effectivity of this Title shall take effect on the first day of his operation, and that of\nthe employee, on the date of his employment."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "170"
  },
  {
    "article": "Art. 177",
    "title": "Registration",
    "category": "Labor Law - Book 4",
    "simplified_text": "Each employer and his employees shall register with the\nSystem in accordance with its regulations.",
    "chunks": [
      "Each employer and his employees shall register with the\nSystem in accordance with its regulations."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "171"
  },
  {
    "article": "Art. 178",
    "title": "Limitation of Liability",
    "category": "Labor Law - Book 4",
    "simplified_text": "The State Insurance Fund shall be liable for\ncompensation to the employee or his dependents, except when the disability or death was\noccasioned by the employee’s intoxication, willful intention to injure or kill himself or another,\nnotorious negligence, or otherwise provided under this Title.",
    "chunks": [
      "The State Insurance Fund shall be liable for\ncompensation to the employee or his dependents, except when the disability or death was\noccasioned by the employee’s intoxication, willful intention to injure or kill himself or another,\nnotorious negligence, or otherwise provided under this Title."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "172"
  },
  {
    "article": "Art. 179",
    "title": "Extent of Liability",
    "category": "Labor Law - Book 4",
    "simplified_text": "Unless otherwise provided, the liability of the State\nInsurance Fund under this Title shall be exclusive and in place of all other liabilities of the\nemployer to the employee, his dependents or anyone otherwise entitled to receive damages\non behalf of the employee or his dependents. The payment of compensation under this Title\nshall not bar the recovery of benefits as provided for in Section 699 of the Revised\n\nAdministrative Code, Republic Act Numbered Eleven Hundred Sixty-One, as amended,\nRepublic Act Numbered Six Hundred Ten, as amended, Republic Act Numbered Forty-Eight\nHundred Sixty-Four, as amended, and other laws whose benefits are administered by the\nSystem or by other agencies of the government.",
    "chunks": [
      "Unless otherwise provided, the liability of the State\nInsurance Fund under this Title shall be exclusive and in place of all other liabilities of the\nemployer to the employee, his dependents or anyone otherwise entitled to receive damages\non behalf of the employee or his dependents. The payment of compensation under this Title\nshall not bar the recovery of benefits as provided for in Section 699 of the Revised",
      "Administrative Code, Republic Act Numbered Eleven Hundred Sixty-One, as amended,\nRepublic Act Numbered Six Hundred Ten, as amended, Republic Act Numbered Forty-Eight\nHundred Sixty-Four, as amended, and other laws whose benefits are administered by the\nSystem or by other agencies of the government."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "173"
  },
  {
    "article": "Art. 180",
    "title": "Liability of Third Parties",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) When the disability or death is caused\nby circumstances creating a legal liability against a third party, the disabled employee or the\ndependents, in case of his death, shall be paid by the System under this Title. In case benefit\nis paid under this Title, the System shall be subrogated to the rights of the disabled employee\nor the dependents, in case of his death, in accordance with the general law.\n\n(b) Where the System recovers from such third party damages in excess of those paid or\nallowed under this Title, such excess shall be delivered to the disabled employee or other\npersons entitled thereto, after deducting the cost of proceedings and expenses of the System.",
    "chunks": [
      "(a) When the disability or death is caused\nby circumstances creating a legal liability against a third party, the disabled employee or the\ndependents, in case of his death, shall be paid by the System under this Title. In case benefit\nis paid under this Title, the System shall be subrogated to the rights of the disabled employee\nor the dependents, in case of his death, in accordance with the general law.",
      "(b) Where the System recovers from such third party damages in excess of those paid or\nallowed under this Title, such excess shall be delivered to the disabled employee or other\npersons entitled thereto, after deducting the cost of proceedings and expenses of the System."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "174"
  },
  {
    "article": "Art. 181",
    "title": "Deprivation of the Benefits",
    "category": "Labor Law - Book 4",
    "simplified_text": "Except as otherwise provided under this\nTitle, no contract, regulation or device whatsoever shall operate to deprive the employee or\nhis dependents of any part of the income benefits and medical or related services granted\nunder this Title. Existing medical services being provided by the employer shall be maintained\nand continued to be enjoyed by their employees.",
    "chunks": [
      "Except as otherwise provided under this\nTitle, no contract, regulation or device whatsoever shall operate to deprive the employee or\nhis dependents of any part of the income benefits and medical or related services granted\nunder this Title. Existing medical services being provided by the employer shall be maintained\nand continued to be enjoyed by their employees."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter II - COVERAGE AND LIABILITY"
    ],
    "language": "en",
    "old_article_number": "175"
  },
  {
    "article": "Art. 182",
    "title": "Employees’ Compensation Commission",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) To initiate, rationalize, and\ncoordinate the policies of the employees’ compensation program, the Employees’\nCompensation Commission is hereby created to be composed of five ex-officio members,\nnamely: the Secretary of Labor and Employment as Chairman, the GSIS General Manager, the\nSSS Administrator, the Chairman of the Philippine Medical Care Commission, and the\nExecutive Director of the ECC Secretariat, and two appointive members, one of whom shall\nrepresent the employees and the other, the employers, to be appointed by the President of\nthe Philippines for a term of six years. The appointive member shall have at least five years’\n\nexperience in workmen’s compensation or social security programs. All vacancies shall be filled\nfor the unexpired term only.\n\n(b) The Vice Chairman of the Commission shall be alternated each year between the GSIS\nGeneral Manager and the SSS Administrator. The presence of four members shall constitute a\nquorum. Each member shall receive a per diem of two hundred pesos for every meeting that\nis actually attended by him, exclusive of actual, ordinary and necessary travel and\nrepresentation expenses. In his absence, any member may designate an official of the\ninstitution he serves on full-time basis as his representative to act in his behalf.\n\n(c) The general conduct of the operations and management functions of the GSIS or SSS\nunder this Title shall be vested in its respective chief executive officers, who shall be\nimmediately responsible for carrying out the policies of the Commission.\n\n(d) The Commission shall have the status and category of a government corporation, and\nit is hereby deemed attached to the Department of Labor for policy coordination and\nguidance.",
    "chunks": [
      "(a) To initiate, rationalize, and\ncoordinate the policies of the employees’ compensation program, the Employees’\nCompensation Commission is hereby created to be composed of five ex-officio members,\nnamely: the Secretary of Labor and Employment as Chairman, the GSIS General Manager, the\nSSS Administrator, the Chairman of the Philippine Medical Care Commission, and the\nExecutive Director of the ECC Secretariat, and two appointive members, one of whom shall\nrepresent the employees and the other, the employers, to be appointed by the President of\nthe Philippines for a term of six years. The appointive member shall have at least five years’",
      "experience in workmen’s compensation or social security programs. All vacancies shall be filled\nfor the unexpired term only.",
      "(b) The Vice Chairman of the Commission shall be alternated each year between the GSIS\nGeneral Manager and the SSS Administrator. The presence of four members shall constitute a\nquorum. Each member shall receive a per diem of two hundred pesos for every meeting that\nis actually attended by him, exclusive of actual, ordinary and necessary travel and\nrepresentation expenses. In his absence, any member may designate an official of the\ninstitution he serves on full-time basis as his representative to act in his behalf.",
      "(c) The general conduct of the operations and management functions of the GSIS or SSS\nunder this Title shall be vested in its respective chief executive officers, who shall be\nimmediately responsible for carrying out the policies of the Commission.",
      "(d) The Commission shall have the status and category of a government corporation, and\nit is hereby deemed attached to the Department of Labor for policy coordination and\nguidance."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "176"
  },
  {
    "article": "Art. 183",
    "title": "Powers and Duties",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Commission shall have the following powers\nand duties:\n\n(a) To assess and fix a rate of contribution from all employers;\n\n(b) To determine the rate of contribution payable by an employer whose records show a\nhigh frequency of work accidents or occupational diseases due to failure by the said employer\nto observe adequate safety measures;\n\n(c) To approve rules and regulations governing the processing of claims and the\nsettlement of disputes arising therefrom as prescribed by the System;\n\n(d) To initiate policies and programs toward adequate occupational health and safety and\naccident prevention in the working environment, rehabilitation other than those provided for\nunder Article 190 hereof, and other related programs and activities, and to appropriate\nfunds therefor;\n\n(e) To make the necessary actuarial studies and calculations concerning the grant of\nconstant help and income benefits for permanent disability or death and the rationalization\nof the benefits for permanent disability and death under the Title with benefits payable by the\nSystem for similar contingencies: Provided, That the Commission may upgrade benefits and\n\nadd new ones subject to approval of the President; and Provided, further, That the actuarial\nstability of the State Insurance Fund shall be guaranteed; Provided, finally, That such increases\nin benefits shall not require any increases in contribution, except as provided for in paragraph\n(b) hereof;\n\n(f) To appoint the personnel of its staff, subject to civil service law and rules, but exempt\nfrom WAPCO law and regulations;\n\n(g) To adopt annually a budget of expenditures of the Commission and its staff chargeable\nagainst the State Insurance Fund: Provided, That the SSS and GSIS shall advance on a quarterly\nbasis the remittances of allotment of the loading fund for the Commission’s operational\nexpenses based on its annual budget as duly approved by the Ministry of Budget and\nManagement;\n\n(h) To have the power to administer oath and affirmation, and to issue subpoena and\nsubpoena duces tecum in connection with any question or issue arising from appealed cases\nunder this Title;\n\n(i) To sue and be sued in court;\n\n(j) To acquire property, real or personal, which may be necessary or expedient for the\nattainment of the purposes of this Title;\n\n(k) To enter into agreements or contracts for such services and as may be needed for the\nproper, efficient and stable administration of the program;\n\n(l) To perform such other acts as it may deem appropriate for the attainment of the\npurposes of the Commission and proper enforcement of the provisions of this Title.",
    "chunks": [
      "The Commission shall have the following powers\nand duties:",
      "(a) To assess and fix a rate of contribution from all employers;",
      "(b) To determine the rate of contribution payable by an employer whose records show a\nhigh frequency of work accidents or occupational diseases due to failure by the said employer\nto observe adequate safety measures;",
      "(c) To approve rules and regulations governing the processing of claims and the\nsettlement of disputes arising therefrom as prescribed by the System;",
      "(d) To initiate policies and programs toward adequate occupational health and safety and\naccident prevention in the working environment, rehabilitation other than those provided for\nunder Article 190 hereof, and other related programs and activities, and to appropriate\nfunds therefor;",
      "(e) To make the necessary actuarial studies and calculations concerning the grant of\nconstant help and income benefits for permanent disability or death and the rationalization\nof the benefits for permanent disability and death under the Title with benefits payable by the\nSystem for similar contingencies: Provided, That the Commission may upgrade benefits and",
      "add new ones subject to approval of the President; and Provided, further, That the actuarial\nstability of the State Insurance Fund shall be guaranteed; Provided, finally, That such increases\nin benefits shall not require any increases in contribution, except as provided for in paragraph\n(b) hereof;",
      "(f) To appoint the personnel of its staff, subject to civil service law and rules, but exempt\nfrom WAPCO law and regulations;",
      "(g) To adopt annually a budget of expenditures of the Commission and its staff chargeable\nagainst the State Insurance Fund: Provided, That the SSS and GSIS shall advance on a quarterly\nbasis the remittances of allotment of the loading fund for the Commission’s operational\nexpenses based on its annual budget as duly approved by the Ministry of Budget and\nManagement;",
      "(h) To have the power to administer oath and affirmation, and to issue subpoena and\nsubpoena duces tecum in connection with any question or issue arising from appealed cases\nunder this Title;",
      "(i) To sue and be sued in court;",
      "(j) To acquire property, real or personal, which may be necessary or expedient for the\nattainment of the purposes of this Title;",
      "(k) To enter into agreements or contracts for such services and as may be needed for the\nproper, efficient and stable administration of the program;",
      "(l) To perform such other acts as it may deem appropriate for the attainment of the\npurposes of the Commission and proper enforcement of the provisions of this Title."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "177"
  },
  {
    "article": "Art. 184",
    "title": "Management of Funds",
    "category": "Labor Law - Book 4",
    "simplified_text": "All revenues collected by the System under this\nTitle shall be deposited, invested, administered and disbursed in the same manner and under\nthe same conditions, requirements and safeguards as provided by Republic Act Numbered\nEleven Hundred Sixty-One, as amended, with regard to such other funds as are thereunder\nbeing paid to or collected by the SSS and GSIS, respectively: Provided, That the Commission,\nSSS and GSIS may disburse each year not more than twelve percent of the contribution and\ninvestment earnings collected for operational expenses, including occupational health and\nsafety programs, incidental to the carrying out of this Title.",
    "chunks": [
      "All revenues collected by the System under this\nTitle shall be deposited, invested, administered and disbursed in the same manner and under\nthe same conditions, requirements and safeguards as provided by Republic Act Numbered\nEleven Hundred Sixty-One, as amended, with regard to such other funds as are thereunder\nbeing paid to or collected by the SSS and GSIS, respectively: Provided, That the Commission,\nSSS and GSIS may disburse each year not more than twelve percent of the contribution and\ninvestment earnings collected for operational expenses, including occupational health and\nsafety programs, incidental to the carrying out of this Title."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "178"
  },
  {
    "article": "Art. 185",
    "title": "Investment of Funds",
    "category": "Labor Law - Book 4",
    "simplified_text": "Provisions of existing laws to the contrary\nnotwithstanding, all revenues as are not needed to meet current operational expenses under\nthis Title shall be accumulated in a fund to be known as the State Insurance Fund, which shall\n\nbe used exclusively for payment of the benefits under this Title, and no amount thereof shall\nbe used for any other purpose. All amounts accruing to the State Insurance Fund, which is\nhereby established in the SSS and GSIS, respectively, shall be deposited with any authorized\ndepository bank approved by the Commission, or invested with due and prudent regard for\nthe liquidity needs of the System.",
    "chunks": [
      "Provisions of existing laws to the contrary\nnotwithstanding, all revenues as are not needed to meet current operational expenses under\nthis Title shall be accumulated in a fund to be known as the State Insurance Fund, which shall",
      "be used exclusively for payment of the benefits under this Title, and no amount thereof shall\nbe used for any other purpose. All amounts accruing to the State Insurance Fund, which is\nhereby established in the SSS and GSIS, respectively, shall be deposited with any authorized\ndepository bank approved by the Commission, or invested with due and prudent regard for\nthe liquidity needs of the System."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "179"
  },
  {
    "article": "Art. 186",
    "title": "Settlement of Claims",
    "category": "Labor Law - Book 4",
    "simplified_text": "The System shall have original and exclusive\njurisdiction to settle any dispute arising from this Title with respect to coverage, entitlement\nto benefits, collection and payment of contributions and penalties thereon, or any other\nmatter related thereto, subject to appeal to the Commission, which shall decide appealed\ncases within twenty (20) working days from the submission of the evidence.",
    "chunks": [
      "The System shall have original and exclusive\njurisdiction to settle any dispute arising from this Title with respect to coverage, entitlement\nto benefits, collection and payment of contributions and penalties thereon, or any other\nmatter related thereto, subject to appeal to the Commission, which shall decide appealed\ncases within twenty (20) working days from the submission of the evidence."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "180"
  },
  {
    "article": "Art. 187",
    "title": "Review",
    "category": "Labor Law - Book 4",
    "simplified_text": "Decisions, orders or resolutions of the Commission may be\nreviewed on certiorari by the Supreme Court on question of law upon petition of an aggrieved\nparty within ten (10) days from notice thereof.",
    "chunks": [
      "Decisions, orders or resolutions of the Commission may be\nreviewed on certiorari by the Supreme Court on question of law upon petition of an aggrieved\nparty within ten (10) days from notice thereof."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "181"
  },
  {
    "article": "Art. 188",
    "title": "Enforcement of Decisions",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) Any decision, order or resolution of the\nCommission shall become final and executory if no appeal is taken therefrom within ten (10)\ndays from notice thereof. All awards granted by the Commission in cases appealed from\ndecisions of the System shall be effected within fifteen days from receipt of notice.\n\n(b) In all other cases, decisions, orders and resolutions of the Commission which have\nbecome final and executory shall be enforced and executed in the same manner as decisions\nof the Court of First Instance, and the Commission shall have the power to issue to the city or\nprovincial sheriff or to the sheriff whom it may appoint, such writs of execution as may be\nnecessary for the enforcement of such decisions, orders or resolutions, and any person who\nshall fail or refuse to comply therewith shall, upon application by the Commission, be punished\nby the proper court for contempt.",
    "chunks": [
      "(a) Any decision, order or resolution of the\nCommission shall become final and executory if no appeal is taken therefrom within ten (10)\ndays from notice thereof. All awards granted by the Commission in cases appealed from\ndecisions of the System shall be effected within fifteen days from receipt of notice.",
      "(b) In all other cases, decisions, orders and resolutions of the Commission which have\nbecome final and executory shall be enforced and executed in the same manner as decisions\nof the Court of First Instance, and the Commission shall have the power to issue to the city or\nprovincial sheriff or to the sheriff whom it may appoint, such writs of execution as may be\nnecessary for the enforcement of such decisions, orders or resolutions, and any person who\nshall fail or refuse to comply therewith shall, upon application by the Commission, be punished\nby the proper court for contempt."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter III - ADMINISTRATION"
    ],
    "language": "en",
    "old_article_number": "182"
  },
  {
    "article": "Art. 189",
    "title": "Employers' Contributions",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) Under such regulations as the System\nmay prescribe, beginning as of the last day of the month when an employee’s compulsory\ncoverage takes effect and every month thereafter during his employment, his employer shall\nprepare to remit to the System a contribution equivalent to one (1) percent of his monthly\nsalary credit.\n\n(b) The rate of contribution shall be reviewed periodically and, subject to the limitations\nherein provided, may be revised as the experience in risk, cost of administration, and actual\nor anticipated as well as unexpected losses, may require.\n\n(c) Contributions under this Title shall be paid in their entirety by the employer and any\ncontract or device for the deduction of any portion thereof from the wages or salaries of the\nemployees shall be null and void.\n\n(d) When a covered employee dies, becomes disabled or is separated from employment,\nhis employer’s obligation to pay the monthly contribution arising from that employment shall\ncease at the end of the month of contingency and during such months that he is not receiving\nwages or salary.",
    "chunks": [
      "(a) Under such regulations as the System\nmay prescribe, beginning as of the last day of the month when an employee’s compulsory\ncoverage takes effect and every month thereafter during his employment, his employer shall\nprepare to remit to the System a contribution equivalent to one (1) percent of his monthly\nsalary credit.",
      "(b) The rate of contribution shall be reviewed periodically and, subject to the limitations\nherein provided, may be revised as the experience in risk, cost of administration, and actual\nor anticipated as well as unexpected losses, may require.",
      "(c) Contributions under this Title shall be paid in their entirety by the employer and any\ncontract or device for the deduction of any portion thereof from the wages or salaries of the\nemployees shall be null and void.",
      "(d) When a covered employee dies, becomes disabled or is separated from employment,\nhis employer’s obligation to pay the monthly contribution arising from that employment shall\ncease at the end of the month of contingency and during such months that he is not receiving\nwages or salary."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IV - CONTRIBUTIONS"
    ],
    "language": "en",
    "old_article_number": "183"
  },
  {
    "article": "Art. 190",
    "title": "Government Guarantee",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Republic of the Philippines guarantees the\nbenefits prescribed under this Title, and accepts general responsibility for the solvency of the\nState Insurance Fund. In case of any deficiency, the same shall be covered by supplemental\nappropriations from the national government.",
    "chunks": [
      "The Republic of the Philippines guarantees the\nbenefits prescribed under this Title, and accepts general responsibility for the solvency of the\nState Insurance Fund. In case of any deficiency, the same shall be covered by supplemental\nappropriations from the national government."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IV - CONTRIBUTIONS"
    ],
    "language": "en",
    "old_article_number": "184"
  },
  {
    "article": "Art. 191",
    "title": "Medical Services",
    "category": "Labor Law - Book 4",
    "simplified_text": "Immediately after an employee contracts sickness or\nsustains an injury, he shall be provided by the System during the subsequent period of his\ndisability with such medical services and appliances as the nature of his sickness or injury and\nprogress of his recovery may require, subject to the expense limitation prescribed by the\nCommission.",
    "chunks": [
      "Immediately after an employee contracts sickness or\nsustains an injury, he shall be provided by the System during the subsequent period of his\ndisability with such medical services and appliances as the nature of his sickness or injury and\nprogress of his recovery may require, subject to the expense limitation prescribed by the\nCommission."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter V - MEDICAL BENEFITS"
    ],
    "language": "en",
    "old_article_number": "185"
  },
  {
    "article": "Art. 192",
    "title": "Liability",
    "category": "Labor Law - Book 4",
    "simplified_text": "The System shall have the authority to choose or order a\nchange of physician, hospital or rehabilitation facility for the employee, and shall not be liable\nfor compensation for any aggravation of the employee’s injury or sickness resulting from\nunauthorized changes by the employee of medical services, appliances, supplies, hospitals,\nrehabilitation facilities or physicians.",
    "chunks": [
      "The System shall have the authority to choose or order a\nchange of physician, hospital or rehabilitation facility for the employee, and shall not be liable\nfor compensation for any aggravation of the employee’s injury or sickness resulting from\nunauthorized changes by the employee of medical services, appliances, supplies, hospitals,\nrehabilitation facilities or physicians."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter V - MEDICAL BENEFITS"
    ],
    "language": "en",
    "old_article_number": "186"
  },
  {
    "article": "Art. 193",
    "title": "Attending Physician",
    "category": "Labor Law - Book 4",
    "simplified_text": "Any physician attending an injured or sick\nemployee shall comply with all the regulations of the System and submit reports in prescribed\nforms at such time as may be required concerning his condition or treatment. All medical\ninformation relevant to the particular injury or sickness shall, on demand, be made available\nto the employee or the System. No information developed in connection with treatment or\nexamination for which compensation is sought shall be considered as privileged\ncommunication.",
    "chunks": [
      "Any physician attending an injured or sick\nemployee shall comply with all the regulations of the System and submit reports in prescribed\nforms at such time as may be required concerning his condition or treatment. All medical\ninformation relevant to the particular injury or sickness shall, on demand, be made available\nto the employee or the System. No information developed in connection with treatment or\nexamination for which compensation is sought shall be considered as privileged\ncommunication."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter V - MEDICAL BENEFITS"
    ],
    "language": "en",
    "old_article_number": "187"
  },
  {
    "article": "Art. 194",
    "title": "Refusal of Examination or Treatment",
    "category": "Labor Law - Book 4",
    "simplified_text": "If the employee unreasonably\nrefuses to submit to medical examination or treatment, the System shall stop the payment of\nfurther compensation during such time as such refusal continues. What constitutes an\nunreasonable refusal shall be determined by the System which may, on its own initiative,\ndetermine the necessity, character and sufficiency of any medical services furnished or to be\nfurnished.",
    "chunks": [
      "If the employee unreasonably\nrefuses to submit to medical examination or treatment, the System shall stop the payment of\nfurther compensation during such time as such refusal continues. What constitutes an\nunreasonable refusal shall be determined by the System which may, on its own initiative,\ndetermine the necessity, character and sufficiency of any medical services furnished or to be\nfurnished."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter V - MEDICAL BENEFITS"
    ],
    "language": "en",
    "old_article_number": "188"
  },
  {
    "article": "Art. 195",
    "title": "Fees and Other Charges",
    "category": "Labor Law - Book 4",
    "simplified_text": "All fees and other charges for hospital\nservices, medical care and appliances, including professional fees, shall not be higher than\nthose prevailing in wards of hospitals for similar services to injured or sick persons in general\n\nand shall be subject to the regulations of the Commission. Professional fees shall only be\nappreciably higher than those prescribed under Republic Act Numbered Sixty-One Hundred\nEleven, as amended, otherwise known as the Philippine Medical Care Act of 1969.",
    "chunks": [
      "All fees and other charges for hospital\nservices, medical care and appliances, including professional fees, shall not be higher than\nthose prevailing in wards of hospitals for similar services to injured or sick persons in general",
      "and shall be subject to the regulations of the Commission. Professional fees shall only be\nappreciably higher than those prescribed under Republic Act Numbered Sixty-One Hundred\nEleven, as amended, otherwise known as the Philippine Medical Care Act of 1969."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter V - MEDICAL BENEFITS"
    ],
    "language": "en",
    "old_article_number": "189"
  },
  {
    "article": "Art. 196",
    "title": "Rehabilitation Services",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) The System shall, as soon as practicable,\nestablish a continuing program, for the rehabilitation of injured and handicapped employees\nwho shall be entitled to rehabilitation services, which shall consist of medical, surgical or\nhospital treatment, including appliances if they have been handicapped by the injury, to help\nthem become physically independent.\n\n(b) As soon as practicable, the System shall establish centers equipped and staffed to\nprovide a balanced program of remedial treatment, vocational assessment and preparation\ndesigned to meet the individual needs of each handicapped employee to restore him to\nsuitable employment, including assistance as may be within its resources, to help each\nrehabilitee to develop his mental, vocational or social potential.",
    "chunks": [
      "(a) The System shall, as soon as practicable,\nestablish a continuing program, for the rehabilitation of injured and handicapped employees\nwho shall be entitled to rehabilitation services, which shall consist of medical, surgical or\nhospital treatment, including appliances if they have been handicapped by the injury, to help\nthem become physically independent.",
      "(b) As soon as practicable, the System shall establish centers equipped and staffed to\nprovide a balanced program of remedial treatment, vocational assessment and preparation\ndesigned to meet the individual needs of each handicapped employee to restore him to\nsuitable employment, including assistance as may be within its resources, to help each\nrehabilitee to develop his mental, vocational or social potential."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter V - MEDICAL BENEFITS"
    ],
    "language": "en",
    "old_article_number": "190"
  },
  {
    "article": "Art. 197",
    "title": "Temporary Total Disability",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) Under such regulations as the\nCommission may approve, any employee under this Title who sustains an injury or contracts\nsickness resulting in temporary total disability shall, for each day of such a disability or fraction\nthereof, be paid by the System an income benefit equivalent to ninety percent of his average\ndaily salary credit, subject to the following conditions: the daily income benefit shall not be\nless than Ten Pesos nor more than Ninety Pesos, nor paid for a continuous period longer\nthan one hundred twenty days, except as otherwise provided for in the Rules, and the System\nshall be notified of the injury or sickness.\n\n(b) The payment of such income benefit shall be in accordance with the regulations of the\nCommission.",
    "chunks": [
      "(a) Under such regulations as the\nCommission may approve, any employee under this Title who sustains an injury or contracts\nsickness resulting in temporary total disability shall, for each day of such a disability or fraction\nthereof, be paid by the System an income benefit equivalent to ninety percent of his average\ndaily salary credit, subject to the following conditions: the daily income benefit shall not be\nless than Ten Pesos nor more than Ninety Pesos, nor paid for a continuous period longer\nthan one hundred twenty days, except as otherwise provided for in the Rules, and the System\nshall be notified of the injury or sickness.",
      "(b) The payment of such income benefit shall be in accordance with the regulations of the\nCommission."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VI - DISABILITY BENEFITS"
    ],
    "language": "en",
    "old_article_number": "191"
  },
  {
    "article": "Art. 198",
    "title": "Permanent Total Disability",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) Under such regulations as the\nCommission may approve, any employee under this Title who contracts sickness or sustains\nan injury resulting in his permanent total disability shall, for each month until his death, be\npaid by the System during such a disability, an amount equivalent to the monthly income\nbenefit, plus ten percent thereof for each dependent child, but not exceeding five, beginning\nwith the youngest and without substitution: Provided, That the monthly income benefit shall\nbe the new amount of the monthly benefit for all covered pensioners, effective upon approval\nof this Decree.\n\n(b) The monthly income benefit shall be guaranteed for five years, and shall be suspended\nif the employee is gainfully employed, or recovers from his permanent total disability, or fails\nto present himself for examination at least once a year upon notice by the System, except as\notherwise provided for in other laws, decrees, orders or Letters of Instructions.\n\n(c) The following disabilities shall be deemed total and permanent:\n\n(1) Temporary total disability lasting continuously for more than one hundred twenty\ndays, except as otherwise provided for in the Rules;\n\n(2) Complete loss of sight of both eyes;\n\n(3) Loss of two limbs at or above the ankle or wrist;\n\n(4) Permanent complete paralysis of two limbs;\n\n(5) Brain injury resulting in incurable imbecility or insanity; and\n\n(6) Such cases as determined by the Medical Director of the System and approved by\nthe Commission.\n\n(d) The number of months of paid coverage shall be defined and approximated by a\nformula to be approved by the Commission.",
    "chunks": [
      "(a) Under such regulations as the\nCommission may approve, any employee under this Title who contracts sickness or sustains\nan injury resulting in his permanent total disability shall, for each month until his death, be\npaid by the System during such a disability, an amount equivalent to the monthly income\nbenefit, plus ten percent thereof for each dependent child, but not exceeding five, beginning\nwith the youngest and without substitution: Provided, That the monthly income benefit shall\nbe the new amount of the monthly benefit for all covered pensioners, effective upon approval\nof this Decree.",
      "(b) The monthly income benefit shall be guaranteed for five years, and shall be suspended\nif the employee is gainfully employed, or recovers from his permanent total disability, or fails\nto present himself for examination at least once a year upon notice by the System, except as\notherwise provided for in other laws, decrees, orders or Letters of Instructions.",
      "(c) The following disabilities shall be deemed total and permanent:",
      "(1) Temporary total disability lasting continuously for more than one hundred twenty\ndays, except as otherwise provided for in the Rules;",
      "(2) Complete loss of sight of both eyes;",
      "(3) Loss of two limbs at or above the ankle or wrist;",
      "(4) Permanent complete paralysis of two limbs;",
      "(5) Brain injury resulting in incurable imbecility or insanity; and",
      "(6) Such cases as determined by the Medical Director of the System and approved by\nthe Commission.",
      "(d) The number of months of paid coverage shall be defined and approximated by a\nformula to be approved by the Commission."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VI - DISABILITY BENEFITS"
    ],
    "language": "en",
    "old_article_number": "192"
  },
  {
    "article": "Art. 199",
    "title": "Permanent Partial Disability",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) Under such regulations as the\nCommission may approve, any employee under this Title who contracts sickness or sustains\nan injury resulting in permanent partial disability shall, for each month not exceeding the\nperiod designated herein, be paid by the System during such a disability an income benefit for\npermanent total disability.\n\n(b) The benefit shall be paid for not more than the period designated in the following\nschedules:\n\nComplete and permanent loss No. of Months\nof the use of:\nOne thumb - 10\nOne index finger - 8\nOne middle finger - 6\nOne ring finger - 5\nOne little finger - 3\nOne big toe - 6\n\nOne toe - 3\nOne arm - 50\nOne hand - 39\nOne foot - 31\nOne leg - 46\nOne ear - 10\nBoth ears - 20\nHearing of one ear - 10\nHearing of both ears - 50\nSight of one eye - 25\n\n(c) A loss of a wrist shall be considered as a loss of the hand, and a loss of an elbow shall\nbe considered as a loss of the arm. A loss of an ankle shall be considered as loss of a foot, and\na loss of a knee shall be considered as a loss of the leg. A loss of more than one joint shall be\nconsidered as a loss of one-half of the whole finger or toe: Provided, That such a loss shall be\neither the functional loss of the use or physical loss of the member.\n\n(d) In case of permanent partial disability less than the total loss of the member specified\nin the preceding paragraph, the same monthly income benefit shall be paid for a portion of\nthe period established for the total loss of the member in accordance with the proportion that\nthe partial loss bears to the total loss. If the result is a decimal fraction, the same shall be\nrounded off to the next higher integer.\n\n(e) In cases of simultaneous loss of more than one member or a part thereof as specified\nin this Article, the same monthly income benefit shall be paid for a period equivalent to the\nsum of the periods established for the loss of the member or the part thereof. If the result is\na decimal fraction, the same shall be rounded off to the next higher integer.\n\n(f) In cases of injuries or illnesses resulting in a permanent partial disability not listed in\nthe preceding schedule, the benefit shall be an income benefit equivalent to the percentage\nof the permanent loss of the capacity to work.\n\n(g) Under such regulations as the Commission may approve, the income benefit payable\nin case of permanent partial disability may be paid in monthly pension or in lump sum if the\nperiod covered does not exceed one year.",
    "chunks": [
      "(a) Under such regulations as the\nCommission may approve, any employee under this Title who contracts sickness or sustains\nan injury resulting in permanent partial disability shall, for each month not exceeding the\nperiod designated herein, be paid by the System during such a disability an income benefit for\npermanent total disability.",
      "(b) The benefit shall be paid for not more than the period designated in the following\nschedules:",
      "Complete and permanent loss No. of Months\nof the use of:\nOne thumb - 10\nOne index finger - 8\nOne middle finger - 6\nOne ring finger - 5\nOne little finger - 3\nOne big toe - 6",
      "One toe - 3\nOne arm - 50\nOne hand - 39\nOne foot - 31\nOne leg - 46\nOne ear - 10\nBoth ears - 20\nHearing of one ear - 10\nHearing of both ears - 50\nSight of one eye - 25",
      "(c) A loss of a wrist shall be considered as a loss of the hand, and a loss of an elbow shall\nbe considered as a loss of the arm. A loss of an ankle shall be considered as loss of a foot, and\na loss of a knee shall be considered as a loss of the leg. A loss of more than one joint shall be\nconsidered as a loss of one-half of the whole finger or toe: Provided, That such a loss shall be\neither the functional loss of the use or physical loss of the member.",
      "(d) In case of permanent partial disability less than the total loss of the member specified\nin the preceding paragraph, the same monthly income benefit shall be paid for a portion of\nthe period established for the total loss of the member in accordance with the proportion that\nthe partial loss bears to the total loss. If the result is a decimal fraction, the same shall be\nrounded off to the next higher integer.",
      "(e) In cases of simultaneous loss of more than one member or a part thereof as specified\nin this Article, the same monthly income benefit shall be paid for a period equivalent to the\nsum of the periods established for the loss of the member or the part thereof. If the result is\na decimal fraction, the same shall be rounded off to the next higher integer.",
      "(f) In cases of injuries or illnesses resulting in a permanent partial disability not listed in\nthe preceding schedule, the benefit shall be an income benefit equivalent to the percentage\nof the permanent loss of the capacity to work.",
      "(g) Under such regulations as the Commission may approve, the income benefit payable\nin case of permanent partial disability may be paid in monthly pension or in lump sum if the\nperiod covered does not exceed one year."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VI - DISABILITY BENEFITS"
    ],
    "language": "en",
    "old_article_number": "193"
  },
  {
    "article": "Art. 200",
    "title": "Death",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) Under such regulations as the Commission may approve,\nthe System shall pay to the primary beneficiaries upon the death of the covered employee\nunder this Title, an amount equivalent to his monthly income benefit, plus ten percent thereof\n\nfor each dependent child, but not exceeding five, beginning with the youngest and without\nsubstitution, except as provided for in paragraph (j) of Article 167 hereof: Provided,\nhowever, That the monthly income benefit shall be guaranteed for five years: Provided,\nfurther, That if he has no primary beneficiary, the System shall pay to his secondary\nbeneficiaries the monthly income benefit but not to exceed sixty months: Provided, finally,\nThat the minimum death benefit shall not be less than fifteen thousand pesos.\n\n(b) Under such regulations as the Commission may approve, the System shall pay to the\nprimary beneficiaries upon the death of a covered employee who is under permanent total\ndisability under this Title, eighty percent of the monthly income benefit and his dependents to\nthe dependents’ pension: Provided, That the marriage must have been validly subsisting at the\ntime of disability: Provided, further, That if he has no primary beneficiary, the System shall pay\nto his secondary beneficiaries the monthly pension excluding the dependents’ pension, of the\nremaining balance of the five-year guaranteed period: Provided, finally, That the minimum\ndeath benefit shall not be less than fifteen thousand pesos.\n\n(c) The monthly income benefit provided herein shall be the new amount of the monthly\nincome benefit for the surviving beneficiaries upon the approval of this decree.\n\n(d) Funeral benefit. - A funeral benefit of Three Thousand Pesos (P3,000.00) shall be paid\nupon the death of a covered employee or permanently totally disabled pensioner.",
    "chunks": [
      "(a) Under such regulations as the Commission may approve,\nthe System shall pay to the primary beneficiaries upon the death of the covered employee\nunder this Title, an amount equivalent to his monthly income benefit, plus ten percent thereof",
      "for each dependent child, but not exceeding five, beginning with the youngest and without\nsubstitution, except as provided for in paragraph (j) of Article 167 hereof: Provided,\nhowever, That the monthly income benefit shall be guaranteed for five years: Provided,\nfurther, That if he has no primary beneficiary, the System shall pay to his secondary\nbeneficiaries the monthly income benefit but not to exceed sixty months: Provided, finally,\nThat the minimum death benefit shall not be less than fifteen thousand pesos.",
      "(b) Under such regulations as the Commission may approve, the System shall pay to the\nprimary beneficiaries upon the death of a covered employee who is under permanent total\ndisability under this Title, eighty percent of the monthly income benefit and his dependents to\nthe dependents’ pension: Provided, That the marriage must have been validly subsisting at the\ntime of disability: Provided, further, That if he has no primary beneficiary, the System shall pay\nto his secondary beneficiaries the monthly pension excluding the dependents’ pension, of the\nremaining balance of the five-year guaranteed period: Provided, finally, That the minimum\ndeath benefit shall not be less than fifteen thousand pesos.",
      "(c) The monthly income benefit provided herein shall be the new amount of the monthly\nincome benefit for the surviving beneficiaries upon the approval of this decree.",
      "(d) Funeral benefit. - A funeral benefit of Three Thousand Pesos (P3,000.00) shall be paid\nupon the death of a covered employee or permanently totally disabled pensioner."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VII - DEATH BENEFITS"
    ],
    "language": "en",
    "old_article_number": "194"
  },
  {
    "article": "Art. 201",
    "title": "Relationship and Dependency",
    "category": "Labor Law - Book 4",
    "simplified_text": "All questions of relationship and\ndependency shall be determined as of the time of death.",
    "chunks": [
      "All questions of relationship and\ndependency shall be determined as of the time of death."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "195"
  },
  {
    "article": "Art. 202",
    "title": "Delinquent Contributions",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) An employer who is delinquent in his\ncontributions shall be liable to the System for the benefits which may have been paid by the\nSystem to his employees or their dependents, and any benefit and expenses to which such\nemployer is liable shall constitute a lien on all his property, real or personal, which is hereby\ndeclared to be preferred to any credit, except taxes. The payment by the employer of the lump\nsum equivalent of such liability shall absolve him from the payment of the delinquent\ncontribution and penalty thereon with respect to the employee concerned.\n\n(b) Failure or refusal of the employer to pay or remit the contribution herein prescribed\nshall not prejudice the right of the employee or his dependents to the benefits under this Title.\nIf the sickness, injury, disability or death occurs before the System receives any report of the\n\nname of his employee, the employer shall be liable to the System for the lump sum equivalent\nto the benefits to which such employee or his dependents may be entitled.",
    "chunks": [
      "(a) An employer who is delinquent in his\ncontributions shall be liable to the System for the benefits which may have been paid by the\nSystem to his employees or their dependents, and any benefit and expenses to which such\nemployer is liable shall constitute a lien on all his property, real or personal, which is hereby\ndeclared to be preferred to any credit, except taxes. The payment by the employer of the lump\nsum equivalent of such liability shall absolve him from the payment of the delinquent\ncontribution and penalty thereon with respect to the employee concerned.",
      "(b) Failure or refusal of the employer to pay or remit the contribution herein prescribed\nshall not prejudice the right of the employee or his dependents to the benefits under this Title.\nIf the sickness, injury, disability or death occurs before the System receives any report of the",
      "name of his employee, the employer shall be liable to the System for the lump sum equivalent\nto the benefits to which such employee or his dependents may be entitled."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "196"
  },
  {
    "article": "Art. 203",
    "title": "Second Injuries",
    "category": "Labor Law - Book 4",
    "simplified_text": "If any employee under permanent partial disability\nsuffers another injury which results in a compensable disability greater than the previous\ninjury, the State Insurance Fund shall be liable for the income benefit of the new disability:\nProvided, That if the new disability is related to the previous disability, the System shall be\nliable only for the difference in income benefits.",
    "chunks": [
      "If any employee under permanent partial disability\nsuffers another injury which results in a compensable disability greater than the previous\ninjury, the State Insurance Fund shall be liable for the income benefit of the new disability:\nProvided, That if the new disability is related to the previous disability, the System shall be\nliable only for the difference in income benefits."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "197"
  },
  {
    "article": "Art. 204",
    "title": "Assignment of Benefits",
    "category": "Labor Law - Book 4",
    "simplified_text": "No claim for compensation under this Title is\ntransferable or liable to tax, attachment, garnishment, levy or seizure by or under any legal\nprocess whatsoever, either before or after receipt by the person or persons entitled thereto,\nexcept to pay any debt of the employee to the System.",
    "chunks": [
      "No claim for compensation under this Title is\ntransferable or liable to tax, attachment, garnishment, levy or seizure by or under any legal\nprocess whatsoever, either before or after receipt by the person or persons entitled thereto,\nexcept to pay any debt of the employee to the System."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "198"
  },
  {
    "article": "Art. 205",
    "title": "Earned Benefits",
    "category": "Labor Law - Book 4",
    "simplified_text": "Income benefits shall, with respect to any period of\ndisability, be payable in accordance with this Title to an employee who is entitled to receive\nwages, salaries or allowances for holidays, vacation or sick leaves and any other award of\nbenefit under a collective bargaining or other agreement.",
    "chunks": [
      "Income benefits shall, with respect to any period of\ndisability, be payable in accordance with this Title to an employee who is entitled to receive\nwages, salaries or allowances for holidays, vacation or sick leaves and any other award of\nbenefit under a collective bargaining or other agreement."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "199"
  },
  {
    "article": "Art. 206",
    "title": "Safety Devices",
    "category": "Labor Law - Book 4",
    "simplified_text": "In case the employee’s injury or death was due to the\nfailure of the employer to comply with any law or to install and maintain safety devices or to\ntake other precautions for the prevention of injury, said employer shall pay the State Insurance\nFund a penalty of twenty-five percent (25%) of the lump sum equivalent of the income benefit\npayable by the System to the employee. All employers, especially those who should have been\npaying a rate of contribution higher than required of them under this Title, are enjoined to\nundertake and strengthen measures for the occupational health and safety of their\nemployees.",
    "chunks": [
      "In case the employee’s injury or death was due to the\nfailure of the employer to comply with any law or to install and maintain safety devices or to\ntake other precautions for the prevention of injury, said employer shall pay the State Insurance\nFund a penalty of twenty-five percent (25%) of the lump sum equivalent of the income benefit\npayable by the System to the employee. All employers, especially those who should have been\npaying a rate of contribution higher than required of them under this Title, are enjoined to\nundertake and strengthen measures for the occupational health and safety of their\nemployees."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "200"
  },
  {
    "article": "Art. 207",
    "title": "Prescriptive Period",
    "category": "Labor Law - Book 4",
    "simplified_text": "No claim for compensation shall be given due\ncourse unless said claim is filed with the System within three (3) years from the time the cause\nof action accrued.",
    "chunks": [
      "No claim for compensation shall be given due\ncourse unless said claim is filed with the System within three (3) years from the time the cause\nof action accrued."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "201"
  },
  {
    "article": "Art. 208",
    "title": "Erroneous Payment",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) If the System in good faith pays income benefit\nto a dependent who is inferior in right to another dependent or with whom another\ndependent is entitled to share, such payments shall discharge the System from liability, unless\nand until such other dependent notifies the System of his claim prior to the payments.\n\n(b) In case of doubt as to the respective rights of rival claimants, the System is hereby\nempowered to determine as to whom payments should be made in accordance with such\nregulations as the Commission may approve. If the money is payable to a minor or\nincompetent, payment shall be made by the System to such person or persons as it may\nconsider to be best qualified to take care and dispose of the minor’s or incompetent’s property\nfor his benefit.",
    "chunks": [
      "(a) If the System in good faith pays income benefit\nto a dependent who is inferior in right to another dependent or with whom another\ndependent is entitled to share, such payments shall discharge the System from liability, unless\nand until such other dependent notifies the System of his claim prior to the payments.",
      "(b) In case of doubt as to the respective rights of rival claimants, the System is hereby\nempowered to determine as to whom payments should be made in accordance with such\nregulations as the Commission may approve. If the money is payable to a minor or\nincompetent, payment shall be made by the System to such person or persons as it may\nconsider to be best qualified to take care and dispose of the minor’s or incompetent’s property\nfor his benefit."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "202"
  },
  {
    "article": "Art. 209",
    "title": "Prohibition",
    "category": "Labor Law - Book 4",
    "simplified_text": "No agent, attorney or other person pursuing or in charge\nof the preparation or filing of any claim for benefit under this Title shall demand or charge for\nhis services any fee, and any stipulation to the contrary shall be null and void. The retention\nor deduction of any amount from any benefit granted under this Title for the payment of fees\nfor such services is prohibited. Violation of any provision of this Article shall be punished by a\nfine of not less than Five Hundred Pesos nor more than Five Thousand Pesos, or imprisonment\nfor not less than six months nor more than one year, or both, at the discretion of the court.",
    "chunks": [
      "No agent, attorney or other person pursuing or in charge\nof the preparation or filing of any claim for benefit under this Title shall demand or charge for\nhis services any fee, and any stipulation to the contrary shall be null and void. The retention\nor deduction of any amount from any benefit granted under this Title for the payment of fees\nfor such services is prohibited. Violation of any provision of this Article shall be punished by a\nfine of not less than Five Hundred Pesos nor more than Five Thousand Pesos, or imprisonment\nfor not less than six months nor more than one year, or both, at the discretion of the court."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "203"
  },
  {
    "article": "Art. 210",
    "title": "Exemption from Levy, Tax, etc",
    "category": "Labor Law - Book 4",
    "simplified_text": "All laws to the contrary notwithstanding,\nthe State Insurance Fund and all its assets shall be exempt from any tax, fee, charge, levy, or\ncustoms or import duty and no law hereafter enacted shall apply to the State Insurance Fund\nunless it is provided therein that the same is applicable by expressly stating its name.",
    "chunks": [
      "All laws to the contrary notwithstanding,\nthe State Insurance Fund and all its assets shall be exempt from any tax, fee, charge, levy, or\ncustoms or import duty and no law hereafter enacted shall apply to the State Insurance Fund\nunless it is provided therein that the same is applicable by expressly stating its name."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter VIII - PROVISIONS COMMON TO INCOME BENEFITS"
    ],
    "language": "en",
    "old_article_number": "204"
  },
  {
    "article": "Art. 211",
    "title": "Record of Death or Disability",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) All employers shall keep a logbook to\nrecord chronologically the sickness, injury or death of their employees, setting forth therein\ntheir names, dates and places of the contingency, nature of the contingency and absences.\nEntries in the logbook shall be made within five days from notice or knowledge of the\noccurrence of the contingency. Within five days after entry in the logbook, the employer shall\nreport to the System only those contingencies he deems to be work-connected.\n\n(b) All entries in the employer’s logbook shall be made by the employer or any of his\nauthorized officials after verification of the contingencies or the employees’ absences for a\nperiod of a day or more. Upon request by the System, the employer shall furnish the necessary\ncertificate regarding information about any contingency appearing in the logbook, citing the\nentry number, page number and date. Such logbook shall be made available for inspection to\nthe duly authorized representatives of the System.\n\n(c) Should any employer fail to record in the logbook an actual sickness, injury or death of\nany of his employees within the period prescribed herein, give false information or withhold\nmaterial information already in his possession, he shall be held liable for fifty percent of the\nlump sum equivalent of the income benefit to which the employee may be found to be\nentitled, the payment of which shall accrue to the State Insurance Fund.\n\n(d) In case of payment of benefits for any claim which is later determined to be fraudulent\nand the employer is found to be a party to the fraud, such employer shall reimburse the System\nthe full amount of the compensation paid.",
    "chunks": [
      "(a) All employers shall keep a logbook to\nrecord chronologically the sickness, injury or death of their employees, setting forth therein\ntheir names, dates and places of the contingency, nature of the contingency and absences.\nEntries in the logbook shall be made within five days from notice or knowledge of the\noccurrence of the contingency. Within five days after entry in the logbook, the employer shall\nreport to the System only those contingencies he deems to be work-connected.",
      "(b) All entries in the employer’s logbook shall be made by the employer or any of his\nauthorized officials after verification of the contingencies or the employees’ absences for a\nperiod of a day or more. Upon request by the System, the employer shall furnish the necessary\ncertificate regarding information about any contingency appearing in the logbook, citing the\nentry number, page number and date. Such logbook shall be made available for inspection to\nthe duly authorized representatives of the System.",
      "(c) Should any employer fail to record in the logbook an actual sickness, injury or death of\nany of his employees within the period prescribed herein, give false information or withhold\nmaterial information already in his possession, he shall be held liable for fifty percent of the\nlump sum equivalent of the income benefit to which the employee may be found to be\nentitled, the payment of which shall accrue to the State Insurance Fund.",
      "(d) In case of payment of benefits for any claim which is later determined to be fraudulent\nand the employer is found to be a party to the fraud, such employer shall reimburse the System\nthe full amount of the compensation paid."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IX - RECORDS, REPORTS AND PENAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "205"
  },
  {
    "article": "Art. 212",
    "title": "Notice of Sickness, Injury or Death",
    "category": "Labor Law - Book 4",
    "simplified_text": "Notice of sickness, injury or death\nshall be given to the employer by the employee or by his dependents or anybody on his behalf\nwithin five days from the occurrence of the contingency. No notice to the employer shall be\nrequired if the contingency is known to the employer or his agents or representatives.",
    "chunks": [
      "Notice of sickness, injury or death\nshall be given to the employer by the employee or by his dependents or anybody on his behalf\nwithin five days from the occurrence of the contingency. No notice to the employer shall be\nrequired if the contingency is known to the employer or his agents or representatives."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IX - RECORDS, REPORTS AND PENAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "206"
  },
  {
    "article": "Art. 213",
    "title": "Penal Provisions",
    "category": "Labor Law - Book 4",
    "simplified_text": "(a) The penal provisions of Republic Act Numbered\nEleven Hundred Sixty-One, as amended, and Commonwealth Act Numbered One Hundred\nEighty-Six, as amended, with regard to the funds as are thereunder being paid to, collected or\ndisbursed by the System, shall be applicable to the collection, administration and\ndisbursement of the Funds under this Title. The penal provisions on coverage shall also be\napplicable.\n\n(b) Any person who, for the purpose of securing entitlement to any benefit or payment\nunder this Title, or the issuance of any certificate or document for any purpose connected with\nthis Title, whether for him or for some other person, commits fraud, collusion, falsification,\nmisrepresentation of facts or any other kind of anomaly, shall be punished with a fine of not\nless than Five Hundred Pesos nor more than Five Thousand Pesos and an imprisonment for\nnot less than six months nor more than one year, at the discretion of the court.\n\n(c) If the act penalized by this Article is committed by any person who has been or is\nemployed by the Commission or System, or a recidivist, the imprisonment shall not be less\nthan one year; if committed by a lawyer, physician or other professional, he shall, in addition\nto the penalty prescribed herein, be disqualified from the practice of his profession; and if\ncommitted by any official, employee or personnel of the Commission, System or any\ngovernment agency, he shall, in addition to the penalty prescribed herein, be dismissed with\nprejudice to re-employment in the government service.",
    "chunks": [
      "(a) The penal provisions of Republic Act Numbered\nEleven Hundred Sixty-One, as amended, and Commonwealth Act Numbered One Hundred\nEighty-Six, as amended, with regard to the funds as are thereunder being paid to, collected or\ndisbursed by the System, shall be applicable to the collection, administration and\ndisbursement of the Funds under this Title. The penal provisions on coverage shall also be\napplicable.",
      "(b) Any person who, for the purpose of securing entitlement to any benefit or payment\nunder this Title, or the issuance of any certificate or document for any purpose connected with\nthis Title, whether for him or for some other person, commits fraud, collusion, falsification,\nmisrepresentation of facts or any other kind of anomaly, shall be punished with a fine of not\nless than Five Hundred Pesos nor more than Five Thousand Pesos and an imprisonment for\nnot less than six months nor more than one year, at the discretion of the court.",
      "(c) If the act penalized by this Article is committed by any person who has been or is\nemployed by the Commission or System, or a recidivist, the imprisonment shall not be less\nthan one year; if committed by a lawyer, physician or other professional, he shall, in addition\nto the penalty prescribed herein, be disqualified from the practice of his profession; and if\ncommitted by any official, employee or personnel of the Commission, System or any\ngovernment agency, he shall, in addition to the penalty prescribed herein, be dismissed with\nprejudice to re-employment in the government service."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IX - RECORDS, REPORTS AND PENAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "207"
  },
  {
    "article": "Art. 214",
    "title": "Applicability",
    "category": "Labor Law - Book 4",
    "simplified_text": "This Title shall apply only to injury, sickness, disability or\ndeath occurring on or after January 1, 1975.",
    "chunks": [
      "This Title shall apply only to injury, sickness, disability or\ndeath occurring on or after January 1, 1975."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IX - RECORDS, REPORTS AND PENAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "208"
  },
  {
    "article": "Art. 215",
    "title": "[208-A] Repeal",
    "category": "Labor Law - Book 4",
    "simplified_text": "All existing laws, Presidential Decrees and Letters of\nInstruction which are inconsistent with or contrary to this Decree, are hereby repealed:\nProvided, That in the case of the GSIS, conditions for entitlement to benefits shall be governed\nby the Labor Code, as amended: Provided, however, That the formulas for computation of\nbenefits, as well as the contribution base, shall be those provided under Commonwealth Act\nNumbered One Hundred Eighty-Six, as amended by Presidential Decree No. 1146, plus twenty\npercent (20%) thereof.",
    "chunks": [
      "All existing laws, Presidential Decrees and Letters of\nInstruction which are inconsistent with or contrary to this Decree, are hereby repealed:\nProvided, That in the case of the GSIS, conditions for entitlement to benefits shall be governed\nby the Labor Code, as amended: Provided, however, That the formulas for computation of\nbenefits, as well as the contribution base, shall be those provided under Commonwealth Act\nNumbered One Hundred Eighty-Six, as amended by Presidential Decree No. 1146, plus twenty\npercent (20%) thereof."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title II - EMPLOYEES COMPENSATION AND STATE INSURANCE FUND",
      "Chapter IX - RECORDS, REPORTS AND PENAL PROVISIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 216",
    "title": "Medical Care",
    "category": "Labor Law - Book 4",
    "simplified_text": "The Philippine Medical Care Plan shall be implemented\nas provided under Republic Act Numbered Sixty-One Hundred Eleven, as amended.",
    "chunks": [
      "The Philippine Medical Care Plan shall be implemented\nas provided under Republic Act Numbered Sixty-One Hundred Eleven, as amended."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title III - MEDICARE"
    ],
    "language": "en",
    "old_article_number": "209"
  },
  {
    "article": "Art. 217",
    "title": "Adult Education",
    "category": "Labor Law - Book 4",
    "simplified_text": "Every employer shall render assistance in the\nestablishment and operation of adult education programs for their workers and employees as\nprescribed by regulations jointly approved by the Department of Labor and Employment and\nthe Department of Education, Culture and Sports.",
    "chunks": [
      "Every employer shall render assistance in the\nestablishment and operation of adult education programs for their workers and employees as\nprescribed by regulations jointly approved by the Department of Labor and Employment and\nthe Department of Education, Culture and Sports."
    ],
    "tags": [
      "Book Four - HEALTH, SAFETY AND SOCIAL WELFARE BENEFITS",
      "Title IV - ADULT EDUCATION"
    ],
    "language": "en",
    "old_article_number": "210"
  },
  {
    "article": "Art. 218",
    "title": "Declaration of Policy",
    "category": "Labor Law - Book 5",
    "simplified_text": "A. It is the policy of the State:\n\n(a) To promote and emphasize the primacy of free collective bargaining and negotiations,\nincluding voluntary arbitration, mediation and conciliation, as modes of settling labor or\nindustrial disputes;\n\n(b) To promote free trade unionism as an instrument for the enhancement of democracy\nand the promotion of social justice and development;\n\n(c) To foster the free and voluntary organization of a strong and united labor movement;\n\n(d) To promote the enlightenment of workers concerning their rights and obligations as\nunion members and as employees;\n\n(e) To provide an adequate administrative machinery for the expeditious settlement of\nlabor or industrial disputes;\n\n(f) To ensure a stable but dynamic and just industrial peace; and\n\n(g) To ensure the participation of workers in decision and policy-making processes\naffecting their rights, duties and welfare.\n\nB. To encourage a truly democratic method of regulating the relations between the\nemployers and employees by means of agreements freely entered into through collective\nbargaining, no court or administrative agency or official shall have the power to set or fix\nwages, rates of pay, hours of work or other terms and conditions of employment, except as\notherwise provided under this Code.",
    "chunks": [
      "A. It is the policy of the State:",
      "(a) To promote and emphasize the primacy of free collective bargaining and negotiations,\nincluding voluntary arbitration, mediation and conciliation, as modes of settling labor or\nindustrial disputes;",
      "(b) To promote free trade unionism as an instrument for the enhancement of democracy\nand the promotion of social justice and development;",
      "(c) To foster the free and voluntary organization of a strong and united labor movement;",
      "(d) To promote the enlightenment of workers concerning their rights and obligations as\nunion members and as employees;",
      "(e) To provide an adequate administrative machinery for the expeditious settlement of\nlabor or industrial disputes;",
      "(f) To ensure a stable but dynamic and just industrial peace; and",
      "(g) To ensure the participation of workers in decision and policy-making processes\naffecting their rights, duties and welfare.",
      "B. To encourage a truly democratic method of regulating the relations between the\nemployers and employees by means of agreements freely entered into through collective\nbargaining, no court or administrative agency or official shall have the power to set or fix\nwages, rates of pay, hours of work or other terms and conditions of employment, except as\notherwise provided under this Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title I - POLICY AND DEFINITIONS",
      "Chapter I - POLICY"
    ],
    "language": "en",
    "old_article_number": "211"
  },
  {
    "article": "Art. 219",
    "title": "Definitions",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) \"Commission\" means the National Labor Relations\nCommission or any of its divisions, as the case may be, as provided under this Code.\n\n(b) \"Bureau\" means the Bureau of Labor Relations and/or the Labor Relations Divisions in\nthe regional offices established under Presidential Decree No. 1, in the Department of Labor.\n\n(c) \"Board\" means the National Conciliation and Mediation Board established under\nExecutive Order No. 126.\n\n(d) \"Council\" means the Tripartite Voluntary Arbitration Advisory Council established\nunder Executive Order No. 126, as amended.\n\n(e) \"Employer\" includes any person acting in the interest of an employer, directly or\nindirectly. The term shall not include any labor organization or any of its officers or agents\nexcept when acting as employer.\n\n(f) \"Employee\" includes any person in the employ of an employer. The term shall not be\nlimited to the employees of a particular employer, unless the Code so explicitly states. It shall\ninclude any individual whose work has ceased as a result of or in connection with any current\nlabor dispute or because of any unfair labor practice if he has not obtained any other\nsubstantially equivalent and regular employment.\n\n(g) \"Labor organization\" means any union or association of employees which exists in\nwhole or in part for the purpose of collective bargaining or of dealing with employers\nconcerning terms and conditions of employment.\n\n(h) \"Legitimate labor organization\" means any labor organization duly registered with the\nDepartment of Labor and Employment, and includes any branch or local thereof.\n\n(i) \"Company union\" means any labor organization whose formation, function or\nadministration has been assisted by any act defined as unfair labor practice by this Code.\n\n(j) \"Bargaining representative\" means a legitimate labor organization or any officer or\nagent of such organization whether or not employed by the employer.\n\n(k) \"Unfair labor practice\" means any unfair labor practice as expressly defined by this\nCode.\n\n(l) \"Labor dispute\" includes any controversy or matter concerning terms and conditions\nof employment or the association or representation of persons in negotiating, fixing,\nmaintaining, changing or arranging the terms and conditions of employment, regardless of\nwhether the disputants stand in the proximate relation of employer and employee.\n\n(m) \"Managerial employee\" is one who is vested with the powers or prerogatives to lay\ndown and execute management policies and/or to hire, transfer, suspend, lay-off, recall,\ndischarge, assign or discipline employees. Supervisory employees are those who, in the\ninterest of the employer, effectively recommend such managerial actions if the exercise of\nsuch authority is not merely routinary or clerical in nature but requires the use of independent\n\njudgment. All employees not falling within any of the above definitions are considered rank-\nand-file employees for purposes of this Book.\n\n(n) \"Voluntary Arbitrator\" means any person accredited by the Board as such, or any\nperson named or designated in the Collective Bargaining Agreement by the parties to act as\ntheir Voluntary Arbitrator, or one chosen with or without the assistance of the National\nConciliation and Mediation Board, pursuant to a selection procedure agreed upon in the\nCollective Bargaining Agreement, or any official that may be authorized by the Secretary of\nLabor and Employment to act as Voluntary Arbitrator upon the written request and agreement\nof the parties to a labor dispute.\n\n(o) \"Strike\" means any temporary stoppage of work by the concerted action of employees\nas a result of an industrial or labor dispute.\n\n(p) \"Lockout\" means any temporary refusal of an employer to furnish work as a result of\nan industrial or labor dispute.\n\n(q) \"Internal union dispute\" includes all disputes or grievances arising from any violation\nof or disagreement over any provision of the constitution and by laws of a union, including any\nviolation of the rights and conditions of union membership provided for in this Code.\n\n(r) \"Strike-breaker\" means any person who obstructs, impedes, or interferes with by\nforce, violence, coercion, threats, or intimidation any peaceful picketing affecting wages,\nhours or conditions of work or in the exercise of the right of self-organization or collective\nbargaining.\n\n(s) \"Strike area\" means the establishment, warehouses, depots, plants or offices,\nincluding the sites or premises used as runaway shops, of the employer struck against, as well\nas the immediate vicinity actually used by picketing strikers in moving to and fro before all\npoints of entrance to and exit from said establishment.",
    "chunks": [
      "(a) \"Commission\" means the National Labor Relations\nCommission or any of its divisions, as the case may be, as provided under this Code.",
      "(b) \"Bureau\" means the Bureau of Labor Relations and/or the Labor Relations Divisions in\nthe regional offices established under Presidential Decree No. 1, in the Department of Labor.",
      "(c) \"Board\" means the National Conciliation and Mediation Board established under\nExecutive Order No. 126.",
      "(d) \"Council\" means the Tripartite Voluntary Arbitration Advisory Council established\nunder Executive Order No. 126, as amended.",
      "(e) \"Employer\" includes any person acting in the interest of an employer, directly or\nindirectly. The term shall not include any labor organization or any of its officers or agents\nexcept when acting as employer.",
      "(f) \"Employee\" includes any person in the employ of an employer. The term shall not be\nlimited to the employees of a particular employer, unless the Code so explicitly states. It shall\ninclude any individual whose work has ceased as a result of or in connection with any current\nlabor dispute or because of any unfair labor practice if he has not obtained any other\nsubstantially equivalent and regular employment.",
      "(g) \"Labor organization\" means any union or association of employees which exists in\nwhole or in part for the purpose of collective bargaining or of dealing with employers\nconcerning terms and conditions of employment.",
      "(h) \"Legitimate labor organization\" means any labor organization duly registered with the\nDepartment of Labor and Employment, and includes any branch or local thereof.",
      "(i) \"Company union\" means any labor organization whose formation, function or\nadministration has been assisted by any act defined as unfair labor practice by this Code.",
      "(j) \"Bargaining representative\" means a legitimate labor organization or any officer or\nagent of such organization whether or not employed by the employer.",
      "(k) \"Unfair labor practice\" means any unfair labor practice as expressly defined by this\nCode.",
      "(l) \"Labor dispute\" includes any controversy or matter concerning terms and conditions\nof employment or the association or representation of persons in negotiating, fixing,\nmaintaining, changing or arranging the terms and conditions of employment, regardless of\nwhether the disputants stand in the proximate relation of employer and employee.",
      "(m) \"Managerial employee\" is one who is vested with the powers or prerogatives to lay\ndown and execute management policies and/or to hire, transfer, suspend, lay-off, recall,\ndischarge, assign or discipline employees. Supervisory employees are those who, in the\ninterest of the employer, effectively recommend such managerial actions if the exercise of\nsuch authority is not merely routinary or clerical in nature but requires the use of independent",
      "judgment. All employees not falling within any of the above definitions are considered rank-\nand-file employees for purposes of this Book.",
      "(n) \"Voluntary Arbitrator\" means any person accredited by the Board as such, or any\nperson named or designated in the Collective Bargaining Agreement by the parties to act as\ntheir Voluntary Arbitrator, or one chosen with or without the assistance of the National\nConciliation and Mediation Board, pursuant to a selection procedure agreed upon in the\nCollective Bargaining Agreement, or any official that may be authorized by the Secretary of\nLabor and Employment to act as Voluntary Arbitrator upon the written request and agreement\nof the parties to a labor dispute.",
      "(o) \"Strike\" means any temporary stoppage of work by the concerted action of employees\nas a result of an industrial or labor dispute.",
      "(p) \"Lockout\" means any temporary refusal of an employer to furnish work as a result of\nan industrial or labor dispute.",
      "(q) \"Internal union dispute\" includes all disputes or grievances arising from any violation\nof or disagreement over any provision of the constitution and by laws of a union, including any\nviolation of the rights and conditions of union membership provided for in this Code.",
      "(r) \"Strike-breaker\" means any person who obstructs, impedes, or interferes with by\nforce, violence, coercion, threats, or intimidation any peaceful picketing affecting wages,\nhours or conditions of work or in the exercise of the right of self-organization or collective\nbargaining.",
      "(s) \"Strike area\" means the establishment, warehouses, depots, plants or offices,\nincluding the sites or premises used as runaway shops, of the employer struck against, as well\nas the immediate vicinity actually used by picketing strikers in moving to and fro before all\npoints of entrance to and exit from said establishment."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title I - POLICY AND DEFINITIONS",
      "Chapter II - DEFINITIONS"
    ],
    "language": "en",
    "old_article_number": "212"
  },
  {
    "article": "Art. 220",
    "title": "National Labor Relations Commission",
    "category": "Labor Law - Book 5",
    "simplified_text": "There shall be a National Labor\nRelations Commission which shall be attached to the Department of Labor and Employment\nsolely for program and policy coordination, composed of a Chairman and twenty-three (23)\nmembers.\n\nEight (8) members each shall be chosen only from among the nominees of the workers\nand employers organizations, respectively. The Chairman and the seven (7) remaining\nmembers shall come from the public sector, with the latter to be chosen preferably from\namong the incumbent labor arbiters.\n\nUpon assumption into office, the members nominated by the workers and employers\norganizations shall divest themselves of any affiliation with or interest in the federation or\nassociation to which they belong.\n\nThe Commission may sit en banc or in eight (8) divisions, each composed of three (3)\nmembers. The Commission shall sit en banc only for purposes of promulgating rules and\nregulations governing the hearing and disposition of cases before any of its divisions and\nregional branches and formulating policies affecting its administration and operations. The\nCommission shall exercise its adjudicatory and all other powers, functions and duties through\nits divisions. Of the eight (8) divisions, the first, second, third, fourth, fifth and sixth divisions\nshall handle cases coming from the National Capital Region and other parts of Luzon, and the\nseventh and eighth divisions, cases from the Visayas and Mindanao, respectively: Provided,\nThat the Commission sitting en banc may, on temporary or emergency basis, allow cases\nwithin the jurisdiction of any division to be heard and decided by any other division whose\ndocket allows the additional workload and such transfer will not expose litigants to\nunnecessary additional expense. The divisions of the Commission shall have exclusive\nappellate jurisdiction over cases within their respective territorial jurisdiction.\n\nThe concurrence of two (2) Commissioners of a division shall be necessary for the\npronouncement of judgment or resolution. Whenever the required membership in a division\nis not complete and the concurrence of two (2) Commissioners to arrive at a judgment or\nresolution cannot be obtained, the Chairman shall designate such number of additional\nCommissioners from the other divisions as may be necessary.\n\nThe conclusions of a division on any case submitted to it for decision shall be reached in\nconsultation before the case is assigned to a member for the writing of the opinion. It shall be\nmandatory for the division to meet for purposes of the consultation ordained therein. A\ncertification to this effect signed by the Presiding Commissioner of the division shall be issued,\nand a copy thereof attached to the record of the case and served upon the parties.\n\nThe Chairman shall be the Presiding Commissioner of the first division, and the seven (7)\nother members from the public sector shall be the Presiding Commissioners of the second,\nthird, fourth, fifth, sixth, seventh and eighth divisions, respectively. In case of the effective\nabsence or incapacity of the Chairman, the Presiding Commissioner of the second division shall\nbe the Acting Chairman.\n\nThe Chairman, aided by the Executive Clerk of the Commission, shall have exclusive\nadministrative supervision over the Commission and its regional branches and all its\npersonnel, including the Labor Arbiters.\n\nThe Commission, when sitting en banc, shall be assisted by the same Executive Clerk, and,\nwhen acting thru its Divisions, by said Executive Clerk for its first division and seven (7) other\nDeputy Executive Clerks for the second, third, fourth fifth, sixth, seventh and eighth Divisions,\nrespectively, in the performance of such similar or equivalent functions and duties as are\ndischarged by the Clerk of Court and Deputy Clerks of Court of the Court of Appeals.\n\nThe Commission and its eight (8) divisions shall be assisted by the Commission Attorneys\nin its appellate and adjudicatory functions whose term shall be coterminous with the\nCommissioners with whom they are assigned. The Commission Attorneys shall be members of\nthe Philippine Bar with at least one (1) year experience or exposure in the field of labor-\nmanagement relations. They shall receive annual salaries and shall be entitled to the same\nallowances and benefits as those falling under Salary Grade twenty-six (SG 26). There shall be\nas many Commission Attorneys as may be necessary for the effective and efficient operation\nof the Commission but in no case more than five (5) assigned to the Office of the Chairman\nand each Commissioner.",
    "chunks": [
      "There shall be a National Labor\nRelations Commission which shall be attached to the Department of Labor and Employment\nsolely for program and policy coordination, composed of a Chairman and twenty-three (23)\nmembers.",
      "Eight (8) members each shall be chosen only from among the nominees of the workers\nand employers organizations, respectively. The Chairman and the seven (7) remaining\nmembers shall come from the public sector, with the latter to be chosen preferably from\namong the incumbent labor arbiters.",
      "Upon assumption into office, the members nominated by the workers and employers\norganizations shall divest themselves of any affiliation with or interest in the federation or\nassociation to which they belong.",
      "The Commission may sit en banc or in eight (8) divisions, each composed of three (3)\nmembers. The Commission shall sit en banc only for purposes of promulgating rules and\nregulations governing the hearing and disposition of cases before any of its divisions and\nregional branches and formulating policies affecting its administration and operations. The\nCommission shall exercise its adjudicatory and all other powers, functions and duties through\nits divisions. Of the eight (8) divisions, the first, second, third, fourth, fifth and sixth divisions\nshall handle cases coming from the National Capital Region and other parts of Luzon, and the\nseventh and eighth divisions, cases from the Visayas and Mindanao, respectively: Provided,\nThat the Commission sitting en banc may, on temporary or emergency basis, allow cases\nwithin the jurisdiction of any division to be heard and decided by any other division whose\ndocket allows the additional workload and such transfer will not expose litigants to\nunnecessary additional expense. The divisions of the Commission shall have exclusive\nappellate jurisdiction over cases within their respective territorial jurisdiction.",
      "The concurrence of two (2) Commissioners of a division shall be necessary for the\npronouncement of judgment or resolution. Whenever the required membership in a division\nis not complete and the concurrence of two (2) Commissioners to arrive at a judgment or\nresolution cannot be obtained, the Chairman shall designate such number of additional\nCommissioners from the other divisions as may be necessary.",
      "The conclusions of a division on any case submitted to it for decision shall be reached in\nconsultation before the case is assigned to a member for the writing of the opinion. It shall be\nmandatory for the division to meet for purposes of the consultation ordained therein. A\ncertification to this effect signed by the Presiding Commissioner of the division shall be issued,\nand a copy thereof attached to the record of the case and served upon the parties.",
      "The Chairman shall be the Presiding Commissioner of the first division, and the seven (7)\nother members from the public sector shall be the Presiding Commissioners of the second,\nthird, fourth, fifth, sixth, seventh and eighth divisions, respectively. In case of the effective\nabsence or incapacity of the Chairman, the Presiding Commissioner of the second division shall\nbe the Acting Chairman.",
      "The Chairman, aided by the Executive Clerk of the Commission, shall have exclusive\nadministrative supervision over the Commission and its regional branches and all its\npersonnel, including the Labor Arbiters.",
      "The Commission, when sitting en banc, shall be assisted by the same Executive Clerk, and,\nwhen acting thru its Divisions, by said Executive Clerk for its first division and seven (7) other\nDeputy Executive Clerks for the second, third, fourth fifth, sixth, seventh and eighth Divisions,\nrespectively, in the performance of such similar or equivalent functions and duties as are\ndischarged by the Clerk of Court and Deputy Clerks of Court of the Court of Appeals.",
      "The Commission and its eight (8) divisions shall be assisted by the Commission Attorneys\nin its appellate and adjudicatory functions whose term shall be coterminous with the\nCommissioners with whom they are assigned. The Commission Attorneys shall be members of\nthe Philippine Bar with at least one (1) year experience or exposure in the field of labor-\nmanagement relations. They shall receive annual salaries and shall be entitled to the same\nallowances and benefits as those falling under Salary Grade twenty-six (SG 26). There shall be\nas many Commission Attorneys as may be necessary for the effective and efficient operation\nof the Commission but in no case more than five (5) assigned to the Office of the Chairman\nand each Commissioner."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter I - CREATION AND COMPOSITION"
    ],
    "language": "en",
    "old_article_number": "213"
  },
  {
    "article": "Art. 221",
    "title": "Headquarters, Branches and Provincial Extension Units",
    "category": "Labor Law - Book 5",
    "simplified_text": "The\nCommission and its first, second, third, fourth, fifth and sixth divisions shall have their main\noffices in Metropolitan Manila, and the seventh and eight divisions in the cities of Cebu and\nCagayan de Oro, respectively. The Commission shall establish as many regional branches as\nthere are regional offices of the Department of Labor and Employment, sub-regional branches\nor provincial extension units. There shall be as many Labor Arbiters as may be necessary for\nthe effective and efficient operation of the Commission.",
    "chunks": [
      "The\nCommission and its first, second, third, fourth, fifth and sixth divisions shall have their main\noffices in Metropolitan Manila, and the seventh and eight divisions in the cities of Cebu and\nCagayan de Oro, respectively. The Commission shall establish as many regional branches as\nthere are regional offices of the Department of Labor and Employment, sub-regional branches\nor provincial extension units. There shall be as many Labor Arbiters as may be necessary for\nthe effective and efficient operation of the Commission."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter I - CREATION AND COMPOSITION"
    ],
    "language": "en",
    "old_article_number": "214"
  },
  {
    "article": "Art. 222",
    "title": "Appointment and Qualifications",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Chairman and other\nCommissioners shall be members of the Philippine Bar and must have been engaged in the\npractice of law in the Philippines for at least fifteen (15) years, with at least five (5) years\nexperience or exposure in the field of labor-management relations, and shall preferably be\nresidents of the region where they shall hold office. The Labor Arbiters shall likewise be\nmembers of the Philippine Bar and must have been engaged in the practice of law in the\nPhilippines for at least ten (10) years, with at least five (5) years experience or exposure in the\nfield of labor-management relations.\n\nThe Chairman, the other Commissioners and the Labor Arbiters shall hold office during\ngood behavior until they reach the age of sixty-five (65) years, unless sooner removed for\ncause as provided by law or become incapacitated to discharge the duties of their office:\nProvided, however, That the President of the Republic of the Philippines may extend the\nservices of the Commissioners and Labor Arbiters up to the maximum age of seventy (70) years\nupon the recommendation of the Commission en banc.\n\nThe Chairman, the Division Presiding Commissioners and other Commissioners shall all be\nappointed by the President. Appointment to any vacancy in a specific division shall come only\nfrom the nominees of the sector which nominated the predecessor. The Labor Arbiters shall\nalso be appointed by the President, upon recommendation of the Commission en banc, and\nshall be subject to the Civil Service Law, rules and regulations.\n\nThe Chairman of the Commission shall appoint the staff and employees of the\nCommission and its regional branches as the needs of the service may require, subject to the\nCivil Service Law, rules and regulations, and upgrade their current salaries, benefits and other\nemoluments in accordance with law.",
    "chunks": [
      "The Chairman and other\nCommissioners shall be members of the Philippine Bar and must have been engaged in the\npractice of law in the Philippines for at least fifteen (15) years, with at least five (5) years\nexperience or exposure in the field of labor-management relations, and shall preferably be\nresidents of the region where they shall hold office. The Labor Arbiters shall likewise be\nmembers of the Philippine Bar and must have been engaged in the practice of law in the\nPhilippines for at least ten (10) years, with at least five (5) years experience or exposure in the\nfield of labor-management relations.",
      "The Chairman, the other Commissioners and the Labor Arbiters shall hold office during\ngood behavior until they reach the age of sixty-five (65) years, unless sooner removed for\ncause as provided by law or become incapacitated to discharge the duties of their office:\nProvided, however, That the President of the Republic of the Philippines may extend the\nservices of the Commissioners and Labor Arbiters up to the maximum age of seventy (70) years\nupon the recommendation of the Commission en banc.",
      "The Chairman, the Division Presiding Commissioners and other Commissioners shall all be\nappointed by the President. Appointment to any vacancy in a specific division shall come only\nfrom the nominees of the sector which nominated the predecessor. The Labor Arbiters shall\nalso be appointed by the President, upon recommendation of the Commission en banc, and\nshall be subject to the Civil Service Law, rules and regulations.",
      "The Chairman of the Commission shall appoint the staff and employees of the\nCommission and its regional branches as the needs of the service may require, subject to the\nCivil Service Law, rules and regulations, and upgrade their current salaries, benefits and other\nemoluments in accordance with law."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter I - CREATION AND COMPOSITION"
    ],
    "language": "en",
    "old_article_number": "215"
  },
  {
    "article": "Art. 223",
    "title": "Salaries, Benefits and Emoluments",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Chairman and members of\nthe Commission shall have the same rank, receive an annual salary equivalent to, and be\nentitled to the same allowances, retirement and benefits as those of the Presiding Justice and\nAssociate Justices of the Court of Appeals, respectively. Labor Arbiters shall have the same\nrank, receive an annual salary equivalent to and be entitled to the same allowances,\nretirement and other benefits and privileges as those of the judges of the Regional Trial Courts.\nIn no case, however, shall the provision of this Article result in the diminution of the existing\nsalaries, allowances and benefits of the aforementioned officials.",
    "chunks": [
      "The Chairman and members of\nthe Commission shall have the same rank, receive an annual salary equivalent to, and be\nentitled to the same allowances, retirement and benefits as those of the Presiding Justice and\nAssociate Justices of the Court of Appeals, respectively. Labor Arbiters shall have the same\nrank, receive an annual salary equivalent to and be entitled to the same allowances,\nretirement and other benefits and privileges as those of the judges of the Regional Trial Courts.\nIn no case, however, shall the provision of this Article result in the diminution of the existing\nsalaries, allowances and benefits of the aforementioned officials."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter I - CREATION AND COMPOSITION"
    ],
    "language": "en",
    "old_article_number": "216"
  },
  {
    "article": "Art. 224",
    "title": "Jurisdiction of the Labor Arbiters and the Commission",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) Except as\notherwise provided under this Code, the Labor Arbiters shall have original and exclusive\njurisdiction to hear and decide, within thirty (30) calendar days after the submission of the\ncase by the parties for decision without extension, even in the absence of stenographic notes,\nthe following cases involving all workers, whether agricultural or non-agricultural:\n\n(1) Unfair labor practice cases;\n\n(2) Termination disputes;\n\n(3) If accompanied with a claim for reinstatement, those cases that workers may file\ninvolving wages, rates of pay, hours of work and other terms and conditions of\nemployment;\n\n(4) Claims for actual, moral, exemplary and other forms of damages arising from the\nemployer-employee relations;\n\n(5) Cases arising from any violation of Article 264 of this Code, including questions\ninvolving the legality of strikes and lockouts; and\n\n(6) Except claims for Employees Compensation, Social Security, Medicare and\nmaternity benefits, all other claims arising from employer-employee relations, including\nthose of persons in domestic or household service, involving an amount exceeding five\nthousand pesos (P5,000.00) regardless of whether accompanied with a claim for\nreinstatement.\n\n(b) The Commission shall have exclusive appellate jurisdiction over all cases decided by\nLabor Arbiters.\n\n(c) Cases arising from the interpretation or implementation of collective bargaining\nagreements and those arising from the interpretation or enforcement of company personnel\npolicies shall be disposed of by the Labor Arbiter by referring the same to the grievance\nmachinery and voluntary arbitration as may be provided in said agreements.",
    "chunks": [
      "(a) Except as\notherwise provided under this Code, the Labor Arbiters shall have original and exclusive\njurisdiction to hear and decide, within thirty (30) calendar days after the submission of the\ncase by the parties for decision without extension, even in the absence of stenographic notes,\nthe following cases involving all workers, whether agricultural or non-agricultural:",
      "(1) Unfair labor practice cases;",
      "(2) Termination disputes;",
      "(3) If accompanied with a claim for reinstatement, those cases that workers may file\ninvolving wages, rates of pay, hours of work and other terms and conditions of\nemployment;",
      "(4) Claims for actual, moral, exemplary and other forms of damages arising from the\nemployer-employee relations;",
      "(5) Cases arising from any violation of Article 264 of this Code, including questions\ninvolving the legality of strikes and lockouts; and",
      "(6) Except claims for Employees Compensation, Social Security, Medicare and\nmaternity benefits, all other claims arising from employer-employee relations, including\nthose of persons in domestic or household service, involving an amount exceeding five\nthousand pesos (P5,000.00) regardless of whether accompanied with a claim for\nreinstatement.",
      "(b) The Commission shall have exclusive appellate jurisdiction over all cases decided by\nLabor Arbiters.",
      "(c) Cases arising from the interpretation or implementation of collective bargaining\nagreements and those arising from the interpretation or enforcement of company personnel\npolicies shall be disposed of by the Labor Arbiter by referring the same to the grievance\nmachinery and voluntary arbitration as may be provided in said agreements."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter II - POWERS AND DUTIES"
    ],
    "language": "en",
    "old_article_number": "217"
  },
  {
    "article": "Art. 225",
    "title": "Powers of the Commission",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Commission shall have the power\nand authority:\n\n(a) To promulgate rules and regulations governing the hearing and disposition of cases\nbefore it and its regional branches, as well as those pertaining to its internal functions and\nsuch rules and regulations as may be necessary to carry out the purposes of this Code;\n\n(b) To administer oaths, summon the parties to a controversy, issue subpoenas requiring\nthe attendance and testimony of witnesses or the production of such books, papers, contracts,\nrecords, statement of accounts, agreements, and others as may be material to a just\ndetermination of the matter under investigation, and to testify in any investigation or hearing\nconducted in pursuance of this Code;\n\n(c) To conduct investigation for the determination of a question, matter or controversy\nwithin its jurisdiction, proceed to hear and determine the disputes in the absence of any party\nthereto who has been summoned or served with notice to appear, conduct its proceedings or\nany part thereof in public or in private, adjourn its hearings to any time and place, refer\ntechnical matters or accounts to an expert and to accept his report as evidence after hearing\nof the parties upon due notice, direct parties to be joined in or excluded from the proceedings,\ncorrect, amend, or waive any error, defect or irregularity whether in substance or in form, give\nall such directions as it may deem necessary or expedient in the determination of the dispute\nbefore it, and dismiss any matter or refrain from further hearing or from determining the\n\ndispute or part thereof, where it is trivial or where further proceedings by the Commission are\nnot necessary or desirable; and\n\n(d) To hold any person in contempt directly or indirectly and impose appropriate penalties\ntherefor in accordance with law.\n\nA person guilty of misbehavior in the presence of or so near the Chairman or any member\nof the Commission or any Labor Arbiter as to obstruct or interrupt the proceedings before the\nsame, including disrespect toward said officials, offensive personalities toward others, or\nrefusal to be sworn, or to answer as a witness or to subscribe an affidavit or deposition when\nlawfully required to do so, may be summarily adjudged in direct contempt by said officials and\npunished by fine not exceeding five hundred pesos (P500) or imprisonment not exceeding five\n(5) days, or both, if it be the Commission or a member thereof, or by a fine not exceeding one\nhundred pesos (P100) or imprisonment not exceeding one (1) day, or both, if it be a Labor\nArbiter.\n\nThe person adjudged in direct contempt by a Labor Arbiter may appeal to the Commission\nand the execution of the judgment shall be suspended pending the resolution of the appeal\nupon the filing by such person of a bond on condition that he will abide by and perform the\njudgment of the Commission should the appeal be decided against him. Judgment of the\nCommission on direct contempt is immediately executory and unappealable. Indirect\ncontempt shall be dealt with by the Commission or Labor Arbiter in the manner prescribed\nunder Rule 71 of the Revised Rules of Court; and\n\n(e) To enjoin or restrain any actual or threatened commission of any or all prohibited or\nunlawful acts or to require the performance of a particular act in any labor dispute which, if\nnot restrained or performed forthwith, may cause grave or irreparable damage to any party\nor render ineffectual any decision in favor of such party: Provided, That no temporary or\npermanent injunction in any case involving or growing out of a labor dispute as defined in this\nCode shall be issued except after hearing the testimony of witnesses, with opportunity for\ncross-examination, in support of the allegations of a complaint made under oath, and\ntestimony in opposition thereto, if offered, and only after a finding of fact by the Commission,\nto the effect:\n\n(1) That prohibited or unlawful acts have been threatened and will be committed unless\nrestrained, or have been committed and will be continued unless restrained, but no injunction\nor temporary restraining order shall be issued on account of any threat, prohibited or unlawful\nact, except against the person or persons, association or organization making the threat or\ncommitting the prohibited or unlawful act or actually authorizing or ratifying the same after\nactual knowledge thereof;\n\n(2) That substantial and irreparable injury to complainant’s property will follow;\n\n(3) That as to each item of relief to be granted, greater injury will be inflicted upon\ncomplainant by the denial of relief than will be inflicted upon defendants by the granting of\nrelief;\n\n(4) That complainant has no adequate remedy at law; and\n\n(5) That the public officers charged with the duty to protect complainant’s property are\nunable or unwilling to furnish adequate protection.\n\nSuch hearing shall be held after due and personal notice thereof has been served, in such\nmanner as the Commission shall direct, to all known persons against whom relief is sought,\nand also to the Chief Executive and other public officials of the province or city within which\nthe unlawful acts have been threatened or committed, charged with the duty to protect\ncomplainant’s property: Provided, however, That if a complainant shall also allege that, unless\na temporary restraining order shall be issued without notice, a substantial and irreparable\ninjury to complainant’s property will be unavoidable, such a temporary restraining order may\nbe issued upon testimony under oath, sufficient, if sustained, to justify the Commission in\nissuing a temporary injunction upon hearing after notice. Such a temporary restraining order\nshall be effective for no longer than twenty (20) days and shall become void at the expiration\nof said twenty (20) days. No such temporary restraining order or temporary injunction shall\nbe issued except on condition that complainant shall first file an undertaking with adequate\nsecurity in an amount to be fixed by the Commission sufficient to recompense those enjoined\nfor any loss, expense or damage caused by the improvident or erroneous issuance of such\norder or injunction, including all reasonable costs, together with a reasonable attorney’s fee,\nand expense of defense against the order or against the granting of any injunctive relief sought\nin the same proceeding and subsequently denied by the Commission.\n\nThe undertaking herein mentioned shall be understood to constitute an agreement\nentered into by the complainant and the surety upon which an order may be rendered in the\nsame suit or proceeding against said complainant and surety, upon a hearing to assess\ndamages, of which hearing, complainant and surety shall have reasonable notice, the said\ncomplainant and surety submitting themselves to the jurisdiction of the Commission for that\npurpose. But nothing herein contained shall deprive any party having a claim or cause of action\nunder or upon such undertaking from electing to pursue his ordinary remedy by suit at law or\nin equity: Provided, further, That the reception of evidence for the application of a writ of\ninjunction may be delegated by the Commission to any of its Labor Arbiters who shall conduct\nsuch hearings in such places as he may determine to be accessible to the parties and their\nwitnesses and shall submit thereafter his recommendation to the Commission.",
    "chunks": [
      "The Commission shall have the power\nand authority:",
      "(a) To promulgate rules and regulations governing the hearing and disposition of cases\nbefore it and its regional branches, as well as those pertaining to its internal functions and\nsuch rules and regulations as may be necessary to carry out the purposes of this Code;",
      "(b) To administer oaths, summon the parties to a controversy, issue subpoenas requiring\nthe attendance and testimony of witnesses or the production of such books, papers, contracts,\nrecords, statement of accounts, agreements, and others as may be material to a just\ndetermination of the matter under investigation, and to testify in any investigation or hearing\nconducted in pursuance of this Code;",
      "(c) To conduct investigation for the determination of a question, matter or controversy\nwithin its jurisdiction, proceed to hear and determine the disputes in the absence of any party\nthereto who has been summoned or served with notice to appear, conduct its proceedings or\nany part thereof in public or in private, adjourn its hearings to any time and place, refer\ntechnical matters or accounts to an expert and to accept his report as evidence after hearing\nof the parties upon due notice, direct parties to be joined in or excluded from the proceedings,\ncorrect, amend, or waive any error, defect or irregularity whether in substance or in form, give\nall such directions as it may deem necessary or expedient in the determination of the dispute\nbefore it, and dismiss any matter or refrain from further hearing or from determining the",
      "dispute or part thereof, where it is trivial or where further proceedings by the Commission are\nnot necessary or desirable; and",
      "(d) To hold any person in contempt directly or indirectly and impose appropriate penalties\ntherefor in accordance with law.",
      "A person guilty of misbehavior in the presence of or so near the Chairman or any member\nof the Commission or any Labor Arbiter as to obstruct or interrupt the proceedings before the\nsame, including disrespect toward said officials, offensive personalities toward others, or\nrefusal to be sworn, or to answer as a witness or to subscribe an affidavit or deposition when\nlawfully required to do so, may be summarily adjudged in direct contempt by said officials and\npunished by fine not exceeding five hundred pesos (P500) or imprisonment not exceeding five\n(5) days, or both, if it be the Commission or a member thereof, or by a fine not exceeding one\nhundred pesos (P100) or imprisonment not exceeding one (1) day, or both, if it be a Labor\nArbiter.",
      "The person adjudged in direct contempt by a Labor Arbiter may appeal to the Commission\nand the execution of the judgment shall be suspended pending the resolution of the appeal\nupon the filing by such person of a bond on condition that he will abide by and perform the\njudgment of the Commission should the appeal be decided against him. Judgment of the\nCommission on direct contempt is immediately executory and unappealable. Indirect\ncontempt shall be dealt with by the Commission or Labor Arbiter in the manner prescribed\nunder Rule 71 of the Revised Rules of Court; and",
      "(e) To enjoin or restrain any actual or threatened commission of any or all prohibited or\nunlawful acts or to require the performance of a particular act in any labor dispute which, if\nnot restrained or performed forthwith, may cause grave or irreparable damage to any party\nor render ineffectual any decision in favor of such party: Provided, That no temporary or\npermanent injunction in any case involving or growing out of a labor dispute as defined in this\nCode shall be issued except after hearing the testimony of witnesses, with opportunity for\ncross-examination, in support of the allegations of a complaint made under oath, and\ntestimony in opposition thereto, if offered, and only after a finding of fact by the Commission,\nto the effect:",
      "(1) That prohibited or unlawful acts have been threatened and will be committed unless\nrestrained, or have been committed and will be continued unless restrained, but no injunction\nor temporary restraining order shall be issued on account of any threat, prohibited or unlawful\nact, except against the person or persons, association or organization making the threat or\ncommitting the prohibited or unlawful act or actually authorizing or ratifying the same after\nactual knowledge thereof;",
      "(2) That substantial and irreparable injury to complainant’s property will follow;",
      "(3) That as to each item of relief to be granted, greater injury will be inflicted upon\ncomplainant by the denial of relief than will be inflicted upon defendants by the granting of\nrelief;",
      "(4) That complainant has no adequate remedy at law; and",
      "(5) That the public officers charged with the duty to protect complainant’s property are\nunable or unwilling to furnish adequate protection.",
      "Such hearing shall be held after due and personal notice thereof has been served, in such\nmanner as the Commission shall direct, to all known persons against whom relief is sought,\nand also to the Chief Executive and other public officials of the province or city within which\nthe unlawful acts have been threatened or committed, charged with the duty to protect\ncomplainant’s property: Provided, however, That if a complainant shall also allege that, unless\na temporary restraining order shall be issued without notice, a substantial and irreparable\ninjury to complainant’s property will be unavoidable, such a temporary restraining order may\nbe issued upon testimony under oath, sufficient, if sustained, to justify the Commission in\nissuing a temporary injunction upon hearing after notice. Such a temporary restraining order\nshall be effective for no longer than twenty (20) days and shall become void at the expiration\nof said twenty (20) days. No such temporary restraining order or temporary injunction shall\nbe issued except on condition that complainant shall first file an undertaking with adequate\nsecurity in an amount to be fixed by the Commission sufficient to recompense those enjoined\nfor any loss, expense or damage caused by the improvident or erroneous issuance of such\norder or injunction, including all reasonable costs, together with a reasonable attorney’s fee,\nand expense of defense against the order or against the granting of any injunctive relief sought\nin the same proceeding and subsequently denied by the Commission.",
      "The undertaking herein mentioned shall be understood to constitute an agreement\nentered into by the complainant and the surety upon which an order may be rendered in the\nsame suit or proceeding against said complainant and surety, upon a hearing to assess\ndamages, of which hearing, complainant and surety shall have reasonable notice, the said\ncomplainant and surety submitting themselves to the jurisdiction of the Commission for that\npurpose. But nothing herein contained shall deprive any party having a claim or cause of action\nunder or upon such undertaking from electing to pursue his ordinary remedy by suit at law or\nin equity: Provided, further, That the reception of evidence for the application of a writ of\ninjunction may be delegated by the Commission to any of its Labor Arbiters who shall conduct\nsuch hearings in such places as he may determine to be accessible to the parties and their\nwitnesses and shall submit thereafter his recommendation to the Commission."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter II - POWERS AND DUTIES"
    ],
    "language": "en",
    "old_article_number": "218"
  },
  {
    "article": "Art. 226",
    "title": "Ocular Inspection",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Chairman, any Commissioner, Labor Arbiter or\ntheir duly authorized representatives, may, at any time during working hours, conduct an\nocular inspection on any establishment, building, ship or vessel, place or premises, including\nany work, material, implement, machinery, appliance or any object therein, and ask any\n\nemployee, laborer, or any person, as the case may be, for any information or data concerning\nany matter or question relative to the object of the investigation.",
    "chunks": [
      "The Chairman, any Commissioner, Labor Arbiter or\ntheir duly authorized representatives, may, at any time during working hours, conduct an\nocular inspection on any establishment, building, ship or vessel, place or premises, including\nany work, material, implement, machinery, appliance or any object therein, and ask any",
      "employee, laborer, or any person, as the case may be, for any information or data concerning\nany matter or question relative to the object of the investigation."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter II - POWERS AND DUTIES"
    ],
    "language": "en",
    "old_article_number": "219"
  },
  {
    "article": "Art. 227",
    "title": "Technical Rules not Binding and Prior Resort to Amicable Settlement",
    "category": "Labor Law - Book 5",
    "simplified_text": "In any proceeding before the Commission or any of the Labor Arbiters, the rules of evidence\nprevailing in courts of law or equity shall not be controlling and it is the spirit and intention of\nthis Code that the Commission and its members and the Labor Arbiters shall use every and all\nreasonable means to ascertain the facts in each case speedily and objectively, without regard\nto technicalities of law or procedure, all in the interest of due process. In any proceeding\nbefore the Commission or any Labor Arbiter, the parties may be represented by legal counsel\nbut it shall be the duty of the Chairman, any Presiding Commissioner or Commissioner or any\nLabor Arbiter to exercise complete control of the proceedings at all stages.\n\nAny provision of law to the contrary notwithstanding, the Labor Arbiter shall exert all\nefforts towards the amicable settlement of a labor dispute within his jurisdiction on or before\nthe first hearing. The same rule shall apply to the Commission in the exercise of its original\njurisdiction.",
    "chunks": [
      "In any proceeding before the Commission or any of the Labor Arbiters, the rules of evidence\nprevailing in courts of law or equity shall not be controlling and it is the spirit and intention of\nthis Code that the Commission and its members and the Labor Arbiters shall use every and all\nreasonable means to ascertain the facts in each case speedily and objectively, without regard\nto technicalities of law or procedure, all in the interest of due process. In any proceeding\nbefore the Commission or any Labor Arbiter, the parties may be represented by legal counsel\nbut it shall be the duty of the Chairman, any Presiding Commissioner or Commissioner or any\nLabor Arbiter to exercise complete control of the proceedings at all stages.",
      "Any provision of law to the contrary notwithstanding, the Labor Arbiter shall exert all\nefforts towards the amicable settlement of a labor dispute within his jurisdiction on or before\nthe first hearing. The same rule shall apply to the Commission in the exercise of its original\njurisdiction."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter II - POWERS AND DUTIES"
    ],
    "language": "en",
    "old_article_number": "221"
  },
  {
    "article": "Art. 228",
    "title": "Appearances and Fees",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) Non-lawyers may appear before the\nCommission or any Labor Arbiter only:\n\n1. If they represent themselves; or\n\n2. If they represent their organization or members thereof.\n\n(b) No attorney’s fees, negotiation fees or similar charges of any kind arising from any\ncollective bargaining agreement shall be imposed on any individual member of the contracting\nunion: Provided, However, that attorney’s fees may be charged against union funds in an\namount to be agreed upon by the parties. Any contract, agreement or arrangement of any sort\nto the contrary shall be null and void.",
    "chunks": [
      "(a) Non-lawyers may appear before the\nCommission or any Labor Arbiter only:",
      "1. If they represent themselves; or",
      "2. If they represent their organization or members thereof.",
      "(b) No attorney’s fees, negotiation fees or similar charges of any kind arising from any\ncollective bargaining agreement shall be imposed on any individual member of the contracting\nunion: Provided, However, that attorney’s fees may be charged against union funds in an\namount to be agreed upon by the parties. Any contract, agreement or arrangement of any sort\nto the contrary shall be null and void."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter II - POWERS AND DUTIES"
    ],
    "language": "en",
    "old_article_number": "222"
  },
  {
    "article": "Art. 229",
    "title": "Appeal",
    "category": "Labor Law - Book 5",
    "simplified_text": "Decisions, awards, or orders of the Labor Arbiter are final and\nexecutory unless appealed to the Commission by any or both parties within ten (10) calendar\ndays from receipt of such decisions, awards, or orders. Such appeal may be entertained only\non any of the following grounds:\n\n(a) If there is prima facie evidence of abuse of discretion on the part of the Labor Arbiter;\n\n(b) If the decision, order or award was secured through fraud or coercion, including graft\nand corruption;\n\n(c) If made purely on questions of law; and\n\n(d) If serious errors in the findings of facts are raised which would cause grave or\nirreparable damage or injury to the appellant.\n\nIn case of a judgment involving a monetary award, an appeal by the employer may be\nperfected only upon the posting of a cash or surety bond issued by a reputable bonding\ncompany duly accredited by the Commission in the amount equivalent to the monetary award\nin the judgment appealed from.\n\nIn any event, the decision of the Labor Arbiter reinstating a dismissed or separated\nemployee, insofar as the reinstatement aspect is concerned, shall immediately be executory,\neven pending appeal. The employee shall either be admitted back to work under the same\nterms and conditions prevailing prior to his dismissal or separation or, at the option of the\nemployer, merely reinstated in the payroll. The posting of a bond by the employer shall not\nstay the execution for reinstatement provided herein.\n\nTo discourage frivolous or dilatory appeals, the Commission or the Labor Arbiter shall\nimpose reasonable penalty, including fines or censures, upon the erring parties.\n\nIn all cases, the appellant shall furnish a copy of the memorandum of appeal to the other\nparty who shall file an answer not later than ten (10) calendar days from receipt thereof.\n\nThe Commission shall decide all cases within twenty (20) calendar days from receipt of\nthe answer of the appellee.\n\nThe decision of the Commission shall be final and executory after ten (10) calendar days\nfrom receipt thereof by the parties.\n\nAny law enforcement agency may be deputized by the Secretary of Labor and\nEmployment or the Commission in the enforcement of decisions, awards or orders.",
    "chunks": [
      "Decisions, awards, or orders of the Labor Arbiter are final and\nexecutory unless appealed to the Commission by any or both parties within ten (10) calendar\ndays from receipt of such decisions, awards, or orders. Such appeal may be entertained only\non any of the following grounds:",
      "(a) If there is prima facie evidence of abuse of discretion on the part of the Labor Arbiter;",
      "(b) If the decision, order or award was secured through fraud or coercion, including graft\nand corruption;",
      "(c) If made purely on questions of law; and",
      "(d) If serious errors in the findings of facts are raised which would cause grave or\nirreparable damage or injury to the appellant.",
      "In case of a judgment involving a monetary award, an appeal by the employer may be\nperfected only upon the posting of a cash or surety bond issued by a reputable bonding\ncompany duly accredited by the Commission in the amount equivalent to the monetary award\nin the judgment appealed from.",
      "In any event, the decision of the Labor Arbiter reinstating a dismissed or separated\nemployee, insofar as the reinstatement aspect is concerned, shall immediately be executory,\neven pending appeal. The employee shall either be admitted back to work under the same\nterms and conditions prevailing prior to his dismissal or separation or, at the option of the\nemployer, merely reinstated in the payroll. The posting of a bond by the employer shall not\nstay the execution for reinstatement provided herein.",
      "To discourage frivolous or dilatory appeals, the Commission or the Labor Arbiter shall\nimpose reasonable penalty, including fines or censures, upon the erring parties.",
      "In all cases, the appellant shall furnish a copy of the memorandum of appeal to the other\nparty who shall file an answer not later than ten (10) calendar days from receipt thereof.",
      "The Commission shall decide all cases within twenty (20) calendar days from receipt of\nthe answer of the appellee.",
      "The decision of the Commission shall be final and executory after ten (10) calendar days\nfrom receipt thereof by the parties.",
      "Any law enforcement agency may be deputized by the Secretary of Labor and\nEmployment or the Commission in the enforcement of decisions, awards or orders."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter III - APPEAL"
    ],
    "language": "en",
    "old_article_number": "223"
  },
  {
    "article": "Art. 230",
    "title": "Execution of Decisions, Orders, or Awards",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) The Secretary of Labor\nand Employment or any Regional Director, the Commission or any Labor Arbiter, or Med-\nArbiter or Voluntary Arbitrator may, motu proprio or on motion of any interested party, issue\na writ of execution on a judgment within five (5) years from the date it becomes final and\nexecutory, requiring a sheriff or a duly deputized officer to execute or enforce final decisions,\norders or awards of the Secretary of Labor and Employment or Regional Director, the\nCommission, the Labor Arbiter or Med-Arbiter, or Voluntary Arbitrator or panel of Voluntary\nArbitrators. In any case, it shall be the duty of the responsible officer to separately furnish\nimmediately the counsels of record and the parties with copies of said decisions, orders or\nawards. Failure to comply with the duty prescribed herein shall subject such responsible\nofficer to appropriate administrative sanctions.\n\n(b) The Secretary of Labor and Employment, and the Chairman of the Commission may\ndesignate special sheriffs and take any measure under existing laws to ensure compliance with\ntheir decisions, orders or awards and those of Labor Arbiters and Voluntary Arbitrators or\npanel of Voluntary Arbitrators, including the imposition of administrative fines which shall not\nbe less than Five Hundred Pesos (P500.00) nor more than Ten Thousand Pesos (P10,000.00).",
    "chunks": [
      "(a) The Secretary of Labor\nand Employment or any Regional Director, the Commission or any Labor Arbiter, or Med-\nArbiter or Voluntary Arbitrator may, motu proprio or on motion of any interested party, issue\na writ of execution on a judgment within five (5) years from the date it becomes final and\nexecutory, requiring a sheriff or a duly deputized officer to execute or enforce final decisions,\norders or awards of the Secretary of Labor and Employment or Regional Director, the\nCommission, the Labor Arbiter or Med-Arbiter, or Voluntary Arbitrator or panel of Voluntary\nArbitrators. In any case, it shall be the duty of the responsible officer to separately furnish\nimmediately the counsels of record and the parties with copies of said decisions, orders or\nawards. Failure to comply with the duty prescribed herein shall subject such responsible\nofficer to appropriate administrative sanctions.",
      "(b) The Secretary of Labor and Employment, and the Chairman of the Commission may\ndesignate special sheriffs and take any measure under existing laws to ensure compliance with\ntheir decisions, orders or awards and those of Labor Arbiters and Voluntary Arbitrators or\npanel of Voluntary Arbitrators, including the imposition of administrative fines which shall not\nbe less than Five Hundred Pesos (P500.00) nor more than Ten Thousand Pesos (P10,000.00)."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter III - APPEAL"
    ],
    "language": "en",
    "old_article_number": "224"
  },
  {
    "article": "Art. 231",
    "title": "Contempt Powers of the Secretary",
    "category": "Labor Law - Book 5",
    "simplified_text": "In the exercise of his powers under\nthis Code, the Secretary of Labor may hold any person in direct or indirect contempt and\nimpose the appropriate penalties therefor.",
    "chunks": [
      "In the exercise of his powers under\nthis Code, the Secretary of Labor may hold any person in direct or indirect contempt and\nimpose the appropriate penalties therefor."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title II - NATIONAL LABOR RELATIONS COMMISSION",
      "Chapter III - APPEAL"
    ],
    "language": "en",
    "old_article_number": "225"
  },
  {
    "article": "Art. 232",
    "title": "Bureau of Labor Relations",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Bureau of Labor Relations and the\nLabor Relations Divisions in the regional offices of the Department of Labor shall have original\nand exclusive authority to act, at their own initiative or upon request of either or both parties,\non all inter-union and intra-union conflicts, and all disputes, grievances or problems arising\nfrom or affecting labor-management relations in all workplaces, whether agricultural or non-\nagricultural, except those arising from the implementation or interpretation of collective\nbargaining agreements which shall be the subject of grievance procedure and/or voluntary\narbitration.\n\nThe Bureau shall have fifteen (15) working days to act on labor cases before it, subject to\nextension by agreement of the parties.",
    "chunks": [
      "The Bureau of Labor Relations and the\nLabor Relations Divisions in the regional offices of the Department of Labor shall have original\nand exclusive authority to act, at their own initiative or upon request of either or both parties,\non all inter-union and intra-union conflicts, and all disputes, grievances or problems arising\nfrom or affecting labor-management relations in all workplaces, whether agricultural or non-\nagricultural, except those arising from the implementation or interpretation of collective\nbargaining agreements which shall be the subject of grievance procedure and/or voluntary\narbitration.",
      "The Bureau shall have fifteen (15) working days to act on labor cases before it, subject to\nextension by agreement of the parties."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "226"
  },
  {
    "article": "Art. 233",
    "title": "Compromise Agreements",
    "category": "Labor Law - Book 5",
    "simplified_text": "Any compromise settlement, including\nthose involving labor standard laws, voluntarily agreed upon by the parties with the assistance\nof the Bureau or the regional office of the Department of Labor, shall be final and binding upon\nthe parties. The National Labor Relations Commission or any court, shall not assume\njurisdiction over issues involved therein except in case of non-compliance thereof or if there\nis prima facie evidence that the settlement was obtained through fraud, misrepresentation,\nor coercion.",
    "chunks": [
      "Any compromise settlement, including\nthose involving labor standard laws, voluntarily agreed upon by the parties with the assistance\nof the Bureau or the regional office of the Department of Labor, shall be final and binding upon\nthe parties. The National Labor Relations Commission or any court, shall not assume\njurisdiction over issues involved therein except in case of non-compliance thereof or if there\nis prima facie evidence that the settlement was obtained through fraud, misrepresentation,\nor coercion."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "227"
  },
  {
    "article": "Art. 234",
    "title": "Mandatory Conciliation and Endorsement of Cases",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) Except as\nprovided in Title VII-A, Book V of this Code, as amended, or as may be excepted by the\nSecretary of Labor and Employment, all issues arising from labor and employment shall be\nsubject to mandatory conciliation-mediation. The labor arbiter or the appropriate DOLE\nagency or office that has jurisdiction over the dispute shall entertain only endorsed or referred\ncases by the duly authorized officer.\n\n(b) Any or both parties involved in the dispute may pre-terminate the conciliation-\nmediation proceedings and request referral or endorsement to the appropriate DOLE agency\nor office which has jurisdiction over the dispute, or if both parties so agree, refer the\nunresolved issues to voluntary arbitration.",
    "chunks": [
      "(a) Except as\nprovided in Title VII-A, Book V of this Code, as amended, or as may be excepted by the\nSecretary of Labor and Employment, all issues arising from labor and employment shall be\nsubject to mandatory conciliation-mediation. The labor arbiter or the appropriate DOLE\nagency or office that has jurisdiction over the dispute shall entertain only endorsed or referred\ncases by the duly authorized officer.",
      "(b) Any or both parties involved in the dispute may pre-terminate the conciliation-\nmediation proceedings and request referral or endorsement to the appropriate DOLE agency\nor office which has jurisdiction over the dispute, or if both parties so agree, refer the\nunresolved issues to voluntary arbitration."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "228"
  },
  {
    "article": "Art. 235",
    "title": "Issuance of Subpoenas",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Bureau shall have the power to require the\nappearance of any person or the production of any paper, document or matter relevant to a\nlabor dispute under its jurisdiction, either at the request of any interested party or at its own\ninitiative.",
    "chunks": [
      "The Bureau shall have the power to require the\nappearance of any person or the production of any paper, document or matter relevant to a\nlabor dispute under its jurisdiction, either at the request of any interested party or at its own\ninitiative."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "229"
  },
  {
    "article": "Art. 236",
    "title": "Appointment of Bureau Personnel",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Secretary of Labor and\nEmployment may appoint, in addition to the present personnel of the Bureau and the\nIndustrial Relations Divisions, such number of examiners and other assistants as may be\nnecessary to carry out the purpose of the Code.",
    "chunks": [
      "The Secretary of Labor and\nEmployment may appoint, in addition to the present personnel of the Bureau and the\nIndustrial Relations Divisions, such number of examiners and other assistants as may be\nnecessary to carry out the purpose of the Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "230"
  },
  {
    "article": "Art. 237",
    "title": "Registry of Unions and File of Collective Bargaining Agreements",
    "category": "Labor Law - Book 5",
    "simplified_text": "The\nBureau shall keep a registry of legitimate labor organizations.\n\nThe Bureau shall also maintain a file of all collective bargaining agreements and other\nrelated agreements and records of settlement of labor disputes and copies of orders and\ndecisions of voluntary arbitrators or panel of voluntary arbitrators. The file shall be open and\naccessible to interested parties under conditions prescribed by the Secretary of Labor and\nEmployment, provided that no specific information submitted in confidence shall be disclosed\nunless authorized by the Secretary, or when it is at issue in any judicial litigation, or when\npublic interest or national security so requires.\n\nWithin thirty (30) days from the execution of a Collective Bargaining Agreement, the\nparties shall submit copies of the same directly to the Bureau or the Regional Offices of the\nDepartment of Labor and Employment for registration accompanied with verified proofs of its\nposting in two conspicuous places in the place of work and ratification by the majority of all\nthe workers in the bargaining unit. The Bureau or Regional Offices shall act upon the\napplication for registration of such Collective Bargaining Agreement within five (5) calendar\ndays from receipt thereof. The Regional Offices shall furnish the Bureau with a copy of the\nCollective Bargaining Agreement within five (5) days from its submission.\n\nThe Bureau or Regional Office shall assess the employer for every Collective Bargaining\nAgreement a registration fee of not less than one thousand pesos (P1,000.00) or in any other\namount as may be deemed appropriate and necessary by the Secretary of Labor and\nEmployment for the effective and efficient administration of the Voluntary Arbitration\nProgram. Any amount collected under this provision shall accrue to the Special Voluntary\nArbitration Fund.\n\nThe Bureau shall also maintain a file, and shall undertake or assist in the publication of all\nfinal decisions, orders and awards of the Secretary of Labor and Employment, Regional\nDirectors and the Commission.",
    "chunks": [
      "The\nBureau shall keep a registry of legitimate labor organizations.",
      "The Bureau shall also maintain a file of all collective bargaining agreements and other\nrelated agreements and records of settlement of labor disputes and copies of orders and\ndecisions of voluntary arbitrators or panel of voluntary arbitrators. The file shall be open and\naccessible to interested parties under conditions prescribed by the Secretary of Labor and\nEmployment, provided that no specific information submitted in confidence shall be disclosed\nunless authorized by the Secretary, or when it is at issue in any judicial litigation, or when\npublic interest or national security so requires.",
      "Within thirty (30) days from the execution of a Collective Bargaining Agreement, the\nparties shall submit copies of the same directly to the Bureau or the Regional Offices of the\nDepartment of Labor and Employment for registration accompanied with verified proofs of its\nposting in two conspicuous places in the place of work and ratification by the majority of all\nthe workers in the bargaining unit. The Bureau or Regional Offices shall act upon the\napplication for registration of such Collective Bargaining Agreement within five (5) calendar\ndays from receipt thereof. The Regional Offices shall furnish the Bureau with a copy of the\nCollective Bargaining Agreement within five (5) days from its submission.",
      "The Bureau or Regional Office shall assess the employer for every Collective Bargaining\nAgreement a registration fee of not less than one thousand pesos (P1,000.00) or in any other\namount as may be deemed appropriate and necessary by the Secretary of Labor and\nEmployment for the effective and efficient administration of the Voluntary Arbitration\nProgram. Any amount collected under this provision shall accrue to the Special Voluntary\nArbitration Fund.",
      "The Bureau shall also maintain a file, and shall undertake or assist in the publication of all\nfinal decisions, orders and awards of the Secretary of Labor and Employment, Regional\nDirectors and the Commission."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "231"
  },
  {
    "article": "Art. 238",
    "title": "Prohibition on Certification Election",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Bureau shall not entertain\nany petition for certification election or any other action which may disturb the administration\nof duly registered existing collective bargaining agreements affecting the parties except under\nArticles 253, 253-A and 256 of this Code.",
    "chunks": [
      "The Bureau shall not entertain\nany petition for certification election or any other action which may disturb the administration\nof duly registered existing collective bargaining agreements affecting the parties except under\nArticles 253, 253-A and 256 of this Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "232"
  },
  {
    "article": "Art. 239",
    "title": "Privileged Communication",
    "category": "Labor Law - Book 5",
    "simplified_text": "Information and statements made at\nconciliation proceedings shall be treated as privileged communication and shall not be used\nas evidence in the Commission. Conciliators and similar officials shall not testify in any court\nor body regarding any matters taken up at conciliation proceedings conducted by them.",
    "chunks": [
      "Information and statements made at\nconciliation proceedings shall be treated as privileged communication and shall not be used\nas evidence in the Commission. Conciliators and similar officials shall not testify in any court\nor body regarding any matters taken up at conciliation proceedings conducted by them."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title III - BUREAU OF LABOR RELATIONS"
    ],
    "language": "en",
    "old_article_number": "233"
  },
  {
    "article": "Art. 240",
    "title": "Requirements of Registration",
    "category": "Labor Law - Book 5",
    "simplified_text": "A federation, national union or\nindustry or trade union center or an independent union shall acquire legal personality and\nshall be entitled to the rights and privileges granted by law to legitimate labor organizations\nupon issuance of the certificate of registration based on the following requirements:\n\n(a) Fifty pesos (P50.00) registration fee;\n\n(b) The names of its officers, their addresses, the principal address of the labor\norganization, the minutes of the organizational meetings and the list of the workers who\nparticipated in such meetings;\n\n(c) In case the applicant is an independent union, the names of all its members comprising\nat least twenty percent (20%) of all the employees in the bargaining unit where it seeks to\noperate;\n\n(d) If the applicant union has been in existence for one or more years, copies of its annual\nfinancial reports; and\n\n(e) Four copies of the constitution and by-laws of the applicant union, minutes of its\nadoption or ratification, and the list of the members who participated in it.",
    "chunks": [
      "A federation, national union or\nindustry or trade union center or an independent union shall acquire legal personality and\nshall be entitled to the rights and privileges granted by law to legitimate labor organizations\nupon issuance of the certificate of registration based on the following requirements:",
      "(a) Fifty pesos (P50.00) registration fee;",
      "(b) The names of its officers, their addresses, the principal address of the labor\norganization, the minutes of the organizational meetings and the list of the workers who\nparticipated in such meetings;",
      "(c) In case the applicant is an independent union, the names of all its members comprising\nat least twenty percent (20%) of all the employees in the bargaining unit where it seeks to\noperate;",
      "(d) If the applicant union has been in existence for one or more years, copies of its annual\nfinancial reports; and",
      "(e) Four copies of the constitution and by-laws of the applicant union, minutes of its\nadoption or ratification, and the list of the members who participated in it."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "234"
  },
  {
    "article": "Art. 241",
    "title": "[234-A] Chartering and Creation of a Local Chapter",
    "category": "Labor Law - Book 5",
    "simplified_text": "A duly registered\nfederation or national union may directly create a local chapter by issuing a charter certificate\nindicating the establishment of the local chapter. The chapter shall acquire legal personality\nonly for purposes of filing a petition for certification election from the date it was issued a\ncharter certificate.\n\nThe chapter shall be entitled to all other rights and privileges of a legitimate labor\norganization only upon the submission of the following documents in addition to its charter\ncertificate:\n\n(a) The names of the chapter's officers, their addresses, and the principal office of the\nchapter; and\n\n(b) The chapter's constitution and by-laws: Provided, That where the chapter's\nconstitution and by-laws are the same as that of the federation or the national union, this fact\nshall be indicated accordingly.\n\nThe additional supporting requirements shall be certified under oath by the secretary or\ntreasurer of the chapter and attested by its president.",
    "chunks": [
      "A duly registered\nfederation or national union may directly create a local chapter by issuing a charter certificate\nindicating the establishment of the local chapter. The chapter shall acquire legal personality\nonly for purposes of filing a petition for certification election from the date it was issued a\ncharter certificate.",
      "The chapter shall be entitled to all other rights and privileges of a legitimate labor\norganization only upon the submission of the following documents in addition to its charter\ncertificate:",
      "(a) The names of the chapter's officers, their addresses, and the principal office of the\nchapter; and",
      "(b) The chapter's constitution and by-laws: Provided, That where the chapter's\nconstitution and by-laws are the same as that of the federation or the national union, this fact\nshall be indicated accordingly.",
      "The additional supporting requirements shall be certified under oath by the secretary or\ntreasurer of the chapter and attested by its president."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 242",
    "title": "Action on Application",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Bureau shall act on all applications for\nregistration within thirty (30) days from filing.\n\nAll requisite documents and papers shall be certified under oath by the secretary or the\ntreasurer of the organization, as the case may be, and attested to by its president.",
    "chunks": [
      "The Bureau shall act on all applications for\nregistration within thirty (30) days from filing.",
      "All requisite documents and papers shall be certified under oath by the secretary or the\ntreasurer of the organization, as the case may be, and attested to by its president."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "235"
  },
  {
    "article": "Art. 243",
    "title": "Denial of Registration; Appeal",
    "category": "Labor Law - Book 5",
    "simplified_text": "The decision of the Labor Relations\nDivision in the regional office denying registration may be appealed by the applicant union to\nthe Bureau within ten (10) days from receipt of notice thereof.",
    "chunks": [
      "The decision of the Labor Relations\nDivision in the regional office denying registration may be appealed by the applicant union to\nthe Bureau within ten (10) days from receipt of notice thereof."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "236"
  },
  {
    "article": "Art. 244",
    "title": "Additional Requirements for Federations or National Unions",
    "category": "Labor Law - Book 5",
    "simplified_text": "Subject\nto Article 238, if the applicant for registration is a federation or a national union, it shall, in\naddition to the requirements of the preceding Articles, submit the following:\n\n(a) Proof of the affiliation of at least ten (10) locals or chapters, each of which must be a\nduly recognized collective bargaining agent in the establishment or industry in which it\noperates, supporting the registration of such applicant federation or national union; and\n\n(b) The names and addresses of the companies where the locals or chapters operate and\nthe list of all the members in each company involved.",
    "chunks": [
      "Subject\nto Article 238, if the applicant for registration is a federation or a national union, it shall, in\naddition to the requirements of the preceding Articles, submit the following:",
      "(a) Proof of the affiliation of at least ten (10) locals or chapters, each of which must be a\nduly recognized collective bargaining agent in the establishment or industry in which it\noperates, supporting the registration of such applicant federation or national union; and",
      "(b) The names and addresses of the companies where the locals or chapters operate and\nthe list of all the members in each company involved."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "237"
  },
  {
    "article": "Art. 245",
    "title": "Cancellation of Registration",
    "category": "Labor Law - Book 5",
    "simplified_text": "The certificate of registration of any\nlegitimate labor organization, whether national or local, may be cancelled by the Bureau, after\ndue hearing, only on the grounds specified in Article 239 hereof.",
    "chunks": [
      "The certificate of registration of any\nlegitimate labor organization, whether national or local, may be cancelled by the Bureau, after\ndue hearing, only on the grounds specified in Article 239 hereof."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "238"
  },
  {
    "article": "Art. 246",
    "title": "[238-A] Effect of a Petition for Cancellation of Registration",
    "category": "Labor Law - Book 5",
    "simplified_text": "A petition for\ncancellation of union registration shall not suspend the proceedings for certification election\nnor shall it prevent the filing of a petition for certification election.\n\nIn case of cancellation, nothing herein shall restrict the right of the union to seek just and\nequitable remedies in the appropriate courts.",
    "chunks": [
      "A petition for\ncancellation of union registration shall not suspend the proceedings for certification election\nnor shall it prevent the filing of a petition for certification election.",
      "In case of cancellation, nothing herein shall restrict the right of the union to seek just and\nequitable remedies in the appropriate courts."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 247",
    "title": "Grounds for Cancellation of Union Registration",
    "category": "Labor Law - Book 5",
    "simplified_text": "The following may\nconstitute grounds for cancellation of union registration:\n\n(a) Misrepresentation, false statement or fraud in connection with the adoption or\nratification of the constitution and by-laws or amendments thereto, the minutes of\nratification, and the list of members who took part in the ratification;\n\n(b) Misrepresentation, false statements or fraud in connection with the election of\nofficers, minutes of the election of officers, and the list of voters;\n\n(c) Voluntary dissolution by the members.",
    "chunks": [
      "The following may\nconstitute grounds for cancellation of union registration:",
      "(a) Misrepresentation, false statement or fraud in connection with the adoption or\nratification of the constitution and by-laws or amendments thereto, the minutes of\nratification, and the list of members who took part in the ratification;",
      "(b) Misrepresentation, false statements or fraud in connection with the election of\nofficers, minutes of the election of officers, and the list of voters;",
      "(c) Voluntary dissolution by the members."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "239"
  },
  {
    "article": "Art. 248",
    "title": "[239-A] Voluntary Cancellation of Registration",
    "category": "Labor Law - Book 5",
    "simplified_text": "The registration of a\nlegitimate labor organization may be cancelled by the organization itself: Provided, That at\nleast two-thirds of its general membership votes, in a meeting duly called for that purpose to\ndissolve the organization: Provided, further, That an application to cancel registration is\nthereafter submitted by the board of the organization, attested to by the president thereof.",
    "chunks": [
      "The registration of a\nlegitimate labor organization may be cancelled by the organization itself: Provided, That at\nleast two-thirds of its general membership votes, in a meeting duly called for that purpose to\ndissolve the organization: Provided, further, That an application to cancel registration is\nthereafter submitted by the board of the organization, attested to by the president thereof."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en"
  },
  {
    "article": "Art. 249",
    "title": "Equity of the Incumbent",
    "category": "Labor Law - Book 5",
    "simplified_text": "All existing federations and national unions\nwhich meet the qualifications of a legitimate labor organization and none of the grounds for\ncancellation shall continue to maintain their existing affiliates regardless of the nature of the\nindustry and the location of the affiliates.",
    "chunks": [
      "All existing federations and national unions\nwhich meet the qualifications of a legitimate labor organization and none of the grounds for\ncancellation shall continue to maintain their existing affiliates regardless of the nature of the\nindustry and the location of the affiliates."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter I - REGISTRATION AND CANCELLATION"
    ],
    "language": "en",
    "old_article_number": "240"
  },
  {
    "article": "Art. 250",
    "title": "Rights and Conditions of Membership in a Labor Organization",
    "category": "Labor Law - Book 5",
    "simplified_text": "The\nfollowing are the rights and conditions of membership in a labor organization:\n\n(a) No arbitrary or excessive initiation fees shall be required of the members of a\nlegitimate labor organization nor shall arbitrary, excessive or oppressive fine and forfeiture be\nimposed;\n\n(b) The members shall be entitled to full and detailed reports from their officers and\nrepresentatives of all financial transactions as provided for in the constitution and by-laws of\nthe organization;\n\n(c) The members shall directly elect their officers in the local union, as well as their\nnational officers in the national union or federation to which they or their local union is\naffiliated, by secret ballot at intervals of five (5) years. No qualification requirement for\ncandidacy to any position shall be imposed other than membership in good standing in subject\nlabor organization. The secretary or any other responsible union officer shall furnish the\nSecretary of Labor and Employment with a list of the newly-elected officers, together with the\nappointive officers or agents who are entrusted with the handling of funds within thirty (30)\ncalendar days after the election of officers or from the occurrence of any change in the list of\nofficers of the labor organization;\n\n(d) The members shall determine by secret ballot, after due deliberation, any question of\nmajor policy affecting the entire membership of the organization, unless the nature of the\norganization or force majeure renders such secret ballot impractical, in which case, the board\nof directors of the organization may make the decision in behalf of the general membership;\n\n(e) No labor organization shall knowingly admit as members or continue in membership\nany individual who belongs to a subversive organization or who is engaged directly or indirectly\nin any subversive activity;\n\n(f) No person who has been convicted of a crime involving moral turpitude shall be eligible\nfor election as a union officer or for appointment to any position in the union;\n\n(g) No officer, agent or member of a labor organization shall collect any fees, dues, or\nother contributions in its behalf or make any disbursement of its money or funds unless he is\nduly authorized pursuant to its constitution and by-laws;\n\n(h) Every payment of fees, dues or other contributions by a member shall be evidenced\nby a receipt signed by the officer or agent making the collection and entered into the record\nof the organization to be kept and maintained for the purpose;\n\n(i) The funds of the organization shall not be applied for any purpose or object other than\nthose expressly provided by its constitution and by-laws or those expressly authorized by\nwritten resolution adopted by the majority of the members at a general meeting duly called\nfor the purpose;\n\n(j) Every income or revenue of the organization shall be evidenced by a record showing\nits source, and every expenditure of its funds shall be evidenced by a receipt from the person\n\nto whom the payment is made, which shall state the date, place and purpose of such payment.\nSuch record or receipt shall form part of the financial records of the organization.\n\nAny action involving the funds of the organization shall prescribe after three (3) years\nfrom the date of submission of the annual financial report to the Department of Labor and\nEmployment or from the date the same should have been submitted as required by law,\nwhichever comes earlier: Provided, That this provision shall apply only to a legitimate labor\norganization which has submitted the financial report requirements under this Code: Provided,\nfurther, That failure of any labor organization to comply with the periodic financial reports\nrequired by law and such rules and regulations promulgated thereunder six (6) months after\nthe effectivity of this Act shall automatically result in the cancellation of union registration of\nsuch labor organization;\n\n(k) The officers of any labor organization shall not be paid any compensation other than\nthe salaries and expenses due to their positions as specifically provided for in its constitution\nand by-laws, or in a written resolution duly authorized by a majority of all the members at a\ngeneral membership meeting duly called for the purpose. The minutes of the meeting and the\nlist of participants and ballots cast shall be subject to inspection by the Secretary of Labor or\nhis duly authorized representatives. Any irregularities in the approval of the resolutions shall\nbe a ground for impeachment or expulsion from the organization;\n\n(l) The treasurer of any labor organization and every officer thereof who is responsible for\nthe account of such organization or for the collection, management, disbursement, custody or\ncontrol of the funds, moneys and other properties of the organization, shall render to the\norganization and to its members a true and correct account of all moneys received and paid\nby him since he assumed office or since the last day on which he rendered such account, and\nof all bonds, securities and other properties of the organization entrusted to his custody or\nunder his control. The rendering of such account shall be made:\n\n(1) At least once a year within thirty (30) days after the close of its fiscal year;\n\n(2) At such other times as may be required by a resolution of the majority of the\nmembers of the organization; and\n\n(3) Upon vacating his office.\n\nThe account shall be duly audited and verified by affidavit and a copy thereof shall be\nfurnished the Secretary of Labor.\n\n(m) The books of accounts and other records of the financial activities of any labor\norganization shall be open to inspection by any officer or member thereof during office hours;\n\n(n) No special assessment or other extraordinary fees may be levied upon the members\nof a labor organization unless authorized by a written resolution of a majority of all the\nmembers in a general membership meeting duly called for the purpose. The secretary of the\n\norganization shall record the minutes of the meeting including the list of all members present,\nthe votes cast, the purpose of the special assessment or fees and the recipient of such\nassessment or fees. The record shall be attested to by the president.\n\n(o) Other than for mandatory activities under the Code, no special assessments,\nattorney’s fees, negotiation fees or any other extraordinary fees may be checked off from any\namount due to an employee without an individual written authorization duly signed by the\nemployee. The authorization should specifically state the amount, purpose and beneficiary of\nthe deduction; and\n\n(p) It shall be the duty of any labor organization and its officers to inform its members on\nthe provisions of its constitution and by-laws, collective bargaining agreement, the prevailing\nlabor relations system and all their rights and obligations under existing labor laws.\n\nFor this purpose, registered labor organizations may assess reasonable dues to finance\nlabor relations seminars and other labor education activities.\n\nAny violation of the above rights and conditions of membership shall be a ground for\ncancellation of union registration or expulsion of officers from office, whichever is appropriate.\nAt least thirty percent (30%) of the members of a union or any member or members specially\nconcerned may report such violation to the Bureau. The Bureau shall have the power to hear\nand decide any reported violation to mete the appropriate penalty.\n\nCriminal and civil liabilities arising from violations of above rights and conditions of\nmembership shall continue to be under the jurisdiction of ordinary courts.",
    "chunks": [
      "The\nfollowing are the rights and conditions of membership in a labor organization:",
      "(a) No arbitrary or excessive initiation fees shall be required of the members of a\nlegitimate labor organization nor shall arbitrary, excessive or oppressive fine and forfeiture be\nimposed;",
      "(b) The members shall be entitled to full and detailed reports from their officers and\nrepresentatives of all financial transactions as provided for in the constitution and by-laws of\nthe organization;",
      "(c) The members shall directly elect their officers in the local union, as well as their\nnational officers in the national union or federation to which they or their local union is\naffiliated, by secret ballot at intervals of five (5) years. No qualification requirement for\ncandidacy to any position shall be imposed other than membership in good standing in subject\nlabor organization. The secretary or any other responsible union officer shall furnish the\nSecretary of Labor and Employment with a list of the newly-elected officers, together with the\nappointive officers or agents who are entrusted with the handling of funds within thirty (30)\ncalendar days after the election of officers or from the occurrence of any change in the list of\nofficers of the labor organization;",
      "(d) The members shall determine by secret ballot, after due deliberation, any question of\nmajor policy affecting the entire membership of the organization, unless the nature of the\norganization or force majeure renders such secret ballot impractical, in which case, the board\nof directors of the organization may make the decision in behalf of the general membership;",
      "(e) No labor organization shall knowingly admit as members or continue in membership\nany individual who belongs to a subversive organization or who is engaged directly or indirectly\nin any subversive activity;",
      "(f) No person who has been convicted of a crime involving moral turpitude shall be eligible\nfor election as a union officer or for appointment to any position in the union;",
      "(g) No officer, agent or member of a labor organization shall collect any fees, dues, or\nother contributions in its behalf or make any disbursement of its money or funds unless he is\nduly authorized pursuant to its constitution and by-laws;",
      "(h) Every payment of fees, dues or other contributions by a member shall be evidenced\nby a receipt signed by the officer or agent making the collection and entered into the record\nof the organization to be kept and maintained for the purpose;",
      "(i) The funds of the organization shall not be applied for any purpose or object other than\nthose expressly provided by its constitution and by-laws or those expressly authorized by\nwritten resolution adopted by the majority of the members at a general meeting duly called\nfor the purpose;",
      "(j) Every income or revenue of the organization shall be evidenced by a record showing\nits source, and every expenditure of its funds shall be evidenced by a receipt from the person",
      "to whom the payment is made, which shall state the date, place and purpose of such payment.\nSuch record or receipt shall form part of the financial records of the organization.",
      "Any action involving the funds of the organization shall prescribe after three (3) years\nfrom the date of submission of the annual financial report to the Department of Labor and\nEmployment or from the date the same should have been submitted as required by law,\nwhichever comes earlier: Provided, That this provision shall apply only to a legitimate labor\norganization which has submitted the financial report requirements under this Code: Provided,\nfurther, That failure of any labor organization to comply with the periodic financial reports\nrequired by law and such rules and regulations promulgated thereunder six (6) months after\nthe effectivity of this Act shall automatically result in the cancellation of union registration of\nsuch labor organization;",
      "(k) The officers of any labor organization shall not be paid any compensation other than\nthe salaries and expenses due to their positions as specifically provided for in its constitution\nand by-laws, or in a written resolution duly authorized by a majority of all the members at a\ngeneral membership meeting duly called for the purpose. The minutes of the meeting and the\nlist of participants and ballots cast shall be subject to inspection by the Secretary of Labor or\nhis duly authorized representatives. Any irregularities in the approval of the resolutions shall\nbe a ground for impeachment or expulsion from the organization;",
      "(l) The treasurer of any labor organization and every officer thereof who is responsible for\nthe account of such organization or for the collection, management, disbursement, custody or\ncontrol of the funds, moneys and other properties of the organization, shall render to the\norganization and to its members a true and correct account of all moneys received and paid\nby him since he assumed office or since the last day on which he rendered such account, and\nof all bonds, securities and other properties of the organization entrusted to his custody or\nunder his control. The rendering of such account shall be made:",
      "(1) At least once a year within thirty (30) days after the close of its fiscal year;",
      "(2) At such other times as may be required by a resolution of the majority of the\nmembers of the organization; and",
      "(3) Upon vacating his office.",
      "The account shall be duly audited and verified by affidavit and a copy thereof shall be\nfurnished the Secretary of Labor.",
      "(m) The books of accounts and other records of the financial activities of any labor\norganization shall be open to inspection by any officer or member thereof during office hours;",
      "(n) No special assessment or other extraordinary fees may be levied upon the members\nof a labor organization unless authorized by a written resolution of a majority of all the\nmembers in a general membership meeting duly called for the purpose. The secretary of the",
      "organization shall record the minutes of the meeting including the list of all members present,\nthe votes cast, the purpose of the special assessment or fees and the recipient of such\nassessment or fees. The record shall be attested to by the president.",
      "(o) Other than for mandatory activities under the Code, no special assessments,\nattorney’s fees, negotiation fees or any other extraordinary fees may be checked off from any\namount due to an employee without an individual written authorization duly signed by the\nemployee. The authorization should specifically state the amount, purpose and beneficiary of\nthe deduction; and",
      "(p) It shall be the duty of any labor organization and its officers to inform its members on\nthe provisions of its constitution and by-laws, collective bargaining agreement, the prevailing\nlabor relations system and all their rights and obligations under existing labor laws.",
      "For this purpose, registered labor organizations may assess reasonable dues to finance\nlabor relations seminars and other labor education activities.",
      "Any violation of the above rights and conditions of membership shall be a ground for\ncancellation of union registration or expulsion of officers from office, whichever is appropriate.\nAt least thirty percent (30%) of the members of a union or any member or members specially\nconcerned may report such violation to the Bureau. The Bureau shall have the power to hear\nand decide any reported violation to mete the appropriate penalty.",
      "Criminal and civil liabilities arising from violations of above rights and conditions of\nmembership shall continue to be under the jurisdiction of ordinary courts."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter II - RIGHTS AND CONDITIONS OF MEMBERSHIP"
    ],
    "language": "en",
    "old_article_number": "241"
  },
  {
    "article": "Art. 251",
    "title": "Rights of Legitimate Labor Organizations",
    "category": "Labor Law - Book 5",
    "simplified_text": "A legitimate labor\norganization shall have the right:\n\n(a) To act as the representative of its members for the purpose of collective bargaining;\n\n(b) To be certified as the exclusive representative of all the employees in an appropriate\nbargaining unit for purposes of collective bargaining;\n\n(c) To be furnished by the employer, upon written request, with its annual audited\nfinancial statements, including the balance sheet and the profit and loss statement, within\nthirty (30) calendar days from the date of receipt of the request, after the union has been duly\nrecognized by the employer or certified as the sole and exclusive bargaining representative of\nthe employees in the bargaining unit, or within sixty (60) calendar days before the expiration\nof the existing collective bargaining agreement, or during the collective bargaining\nnegotiation;\n\n(d) To own property, real or personal, for the use and benefit of the labor organization\nand its members;\n\n(e) To sue and be sued in its registered name; and\n\n(f) To undertake all other activities designed to benefit the organization and its members,\nincluding cooperative, housing, welfare and other projects not contrary to law.\n\nNotwithstanding any provision of a general or special law to the contrary, the income and\nthe properties of legitimate labor organizations, including grants, endowments, gifts,\ndonations and contributions they may receive from fraternal and similar organizations, local\nor foreign, which are actually, directly and exclusively used for their lawful purposes, shall be\nfree from taxes, duties and other assessments. The exemptions provided herein may be\nwithdrawn only by a special law expressly repealing this provision.",
    "chunks": [
      "A legitimate labor\norganization shall have the right:",
      "(a) To act as the representative of its members for the purpose of collective bargaining;",
      "(b) To be certified as the exclusive representative of all the employees in an appropriate\nbargaining unit for purposes of collective bargaining;",
      "(c) To be furnished by the employer, upon written request, with its annual audited\nfinancial statements, including the balance sheet and the profit and loss statement, within\nthirty (30) calendar days from the date of receipt of the request, after the union has been duly\nrecognized by the employer or certified as the sole and exclusive bargaining representative of\nthe employees in the bargaining unit, or within sixty (60) calendar days before the expiration\nof the existing collective bargaining agreement, or during the collective bargaining\nnegotiation;",
      "(d) To own property, real or personal, for the use and benefit of the labor organization\nand its members;",
      "(e) To sue and be sued in its registered name; and",
      "(f) To undertake all other activities designed to benefit the organization and its members,\nincluding cooperative, housing, welfare and other projects not contrary to law.",
      "Notwithstanding any provision of a general or special law to the contrary, the income and\nthe properties of legitimate labor organizations, including grants, endowments, gifts,\ndonations and contributions they may receive from fraternal and similar organizations, local\nor foreign, which are actually, directly and exclusively used for their lawful purposes, shall be\nfree from taxes, duties and other assessments. The exemptions provided herein may be\nwithdrawn only by a special law expressly repealing this provision."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter III - RIGHTS OF LEGITIMATE LABOR ORGANIZATIONS"
    ],
    "language": "en",
    "old_article_number": "242"
  },
  {
    "article": "Art. 252",
    "title": "[242-A] Reportorial Requirements",
    "category": "Labor Law - Book 5",
    "simplified_text": "The following are documents required\nto be submitted to the Bureau by the legitimate labor organization concerned:\n\n(a) Its constitution and by-laws, or amendments thereto, the minutes of ratification, and\nthe list of members who took part in the ratification of the constitution and by-laws within\nthirty (30) days from adoption or ratification of the constitution and by-laws or amendments\nthereto;\n\n(b) Its list of officers, minutes of the election of officers, and list of voters within thirty (30)\ndays from election;\n\n(c) Its annual financial report within thirty (30) days after the close of every fiscal year;\nand\n\n(d) Its list of members at least once a year or whenever required by the Bureau.\n\nFailure to comply with the above requirements shall not be a ground for cancellation of\nunion registration but shall subject the erring officers or members to suspension, expulsion\nfrom membership, or any appropriate penalty.",
    "chunks": [
      "The following are documents required\nto be submitted to the Bureau by the legitimate labor organization concerned:",
      "(a) Its constitution and by-laws, or amendments thereto, the minutes of ratification, and\nthe list of members who took part in the ratification of the constitution and by-laws within\nthirty (30) days from adoption or ratification of the constitution and by-laws or amendments\nthereto;",
      "(b) Its list of officers, minutes of the election of officers, and list of voters within thirty (30)\ndays from election;",
      "(c) Its annual financial report within thirty (30) days after the close of every fiscal year;\nand",
      "(d) Its list of members at least once a year or whenever required by the Bureau.",
      "Failure to comply with the above requirements shall not be a ground for cancellation of\nunion registration but shall subject the erring officers or members to suspension, expulsion\nfrom membership, or any appropriate penalty."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IV - LABOR ORGANIZATIONS",
      "Chapter III - RIGHTS OF LEGITIMATE LABOR ORGANIZATIONS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 253",
    "title": "Coverage and Employees' Right to Self-Organization",
    "category": "Labor Law - Book 5",
    "simplified_text": "All persons\nemployed in commercial, industrial and agricultural enterprises and in religious, charitable,\nmedical, or educational institutions, whether operating for profit or not, shall have the right\nto self-organization and to form, join, or assist labor organizations of their own choosing for\n\npurposes of collective bargaining. Ambulant, intermittent and itinerant workers, self-\nemployed people, rural workers and those without any definite employers may form labor\norganizations for their mutual aid and protection.",
    "chunks": [
      "All persons\nemployed in commercial, industrial and agricultural enterprises and in religious, charitable,\nmedical, or educational institutions, whether operating for profit or not, shall have the right\nto self-organization and to form, join, or assist labor organizations of their own choosing for",
      "purposes of collective bargaining. Ambulant, intermittent and itinerant workers, self-\nemployed people, rural workers and those without any definite employers may form labor\norganizations for their mutual aid and protection."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title V - COVERAGE"
    ],
    "language": "en",
    "old_article_number": "243"
  },
  {
    "article": "Art. 254",
    "title": "Right of Employees in the Public Service",
    "category": "Labor Law - Book 5",
    "simplified_text": "Employees of government\ncorporations established under the Corporation Code shall have the right to organize and to\nbargain collectively with their respective employers. All other employees in the civil service\nshall have the right to form associations for purposes not contrary to law.",
    "chunks": [
      "Employees of government\ncorporations established under the Corporation Code shall have the right to organize and to\nbargain collectively with their respective employers. All other employees in the civil service\nshall have the right to form associations for purposes not contrary to law."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title V - COVERAGE"
    ],
    "language": "en",
    "old_article_number": "244"
  },
  {
    "article": "Art. 255",
    "title": "Ineligibility of Managerial Employees to Join any Labor Organization; Right of Supervisory Employees",
    "category": "Labor Law - Book 5",
    "simplified_text": "Managerial employees are not eligible to join, assist or\nform any labor organization. Supervisory employees shall not be eligible for membership in\nthe collective bargaining unit of the rank-and-file employees but may join, assist or form\nseparate collective bargaining units and/or legitimate labor organizations of their own. The\nrank and file union and the supervisors' union operating within the same establishment may\njoin the same federation or national union.",
    "chunks": [
      "Managerial employees are not eligible to join, assist or\nform any labor organization. Supervisory employees shall not be eligible for membership in\nthe collective bargaining unit of the rank-and-file employees but may join, assist or form\nseparate collective bargaining units and/or legitimate labor organizations of their own. The\nrank and file union and the supervisors' union operating within the same establishment may\njoin the same federation or national union."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title V - COVERAGE"
    ],
    "language": "en",
    "old_article_number": "245"
  },
  {
    "article": "Art. 256",
    "title": "[245-A] Effect of Inclusion as Members of Employees Outside the Bargaining Unit",
    "category": "Labor Law - Book 5",
    "simplified_text": "The inclusion as union members of employees outside the bargaining unit shall not\nbe a ground for the cancellation of the registration of the union. Said employees are\nautomatically deemed removed from the list of membership of said union.",
    "chunks": [
      "The inclusion as union members of employees outside the bargaining unit shall not\nbe a ground for the cancellation of the registration of the union. Said employees are\nautomatically deemed removed from the list of membership of said union."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title V - COVERAGE"
    ],
    "language": "en"
  },
  {
    "article": "Art. 257",
    "title": "Non-Abridgment of Right to Self-Organization",
    "category": "Labor Law - Book 5",
    "simplified_text": "It shall be unlawful\nfor any person to restrain, coerce, discriminate against or unduly interfere with employees\nand workers in their exercise of the right to self-organization. Such right shall include the right\nto form, join, or assist labor organizations for the purpose of collective bargaining through\nrepresentatives of their own choosing and to engage in lawful concerted activities for the same\npurpose for their mutual aid and protection, subject to the provisions of Article 264 of this\nCode.",
    "chunks": [
      "It shall be unlawful\nfor any person to restrain, coerce, discriminate against or unduly interfere with employees\nand workers in their exercise of the right to self-organization. Such right shall include the right\nto form, join, or assist labor organizations for the purpose of collective bargaining through\nrepresentatives of their own choosing and to engage in lawful concerted activities for the same\npurpose for their mutual aid and protection, subject to the provisions of Article 264 of this\nCode."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title V - COVERAGE"
    ],
    "language": "en",
    "old_article_number": "246"
  },
  {
    "article": "Art. 258",
    "title": "Concept of Unfair Labor Practice and Procedure for Prosecution Thereof",
    "category": "Labor Law - Book 5",
    "simplified_text": "Unfair labor practices violate the constitutional right of workers and employees\nto self-organization, are inimical to the legitimate interests of both labor and management,\nincluding their right to bargain collectively and otherwise deal with each other in an\n\natmosphere of freedom and mutual respect, disrupt industrial peace and hinder the\npromotion of healthy and stable labor-management relations.\n\nConsequently, unfair labor practices are not only violations of the civil rights of both labor\nand management but are also criminal offenses against the State which shall be subject to\nprosecution and punishment as herein provided.\n\nSubject to the exercise by the President or by the Secretary of Labor and Employment of\nthe powers vested in them by Articles 263 and 264 of this Code, the civil aspects of all cases\ninvolving unfair labor practices, which may include claims for actual, moral, exemplary and\nother forms of damages, attorney’s fees and other affirmative relief, shall be under the\njurisdiction of the Labor Arbiters. The Labor Arbiters shall give utmost priority to the hearing\nand resolution of all cases involving unfair labor practices. They shall resolve such cases within\nthirty (30) calendar days from the time they are submitted for decision.\n\nRecovery of civil liability in the administrative proceedings shall bar recovery under the\nCivil Code.\n\nNo criminal prosecution under this Title may be instituted without a final judgment\nfinding that an unfair labor practice was committed, having been first obtained in the\npreceding paragraph. During the pendency of such administrative proceeding, the running of\nthe period of prescription of the criminal offense herein penalized shall be considered\ninterrupted: Provided, however, That the final judgment in the administrative proceedings\nshall not be binding in the criminal case nor be considered as evidence of guilt but merely as\nproof of compliance of the requirements therein set forth.",
    "chunks": [
      "Unfair labor practices violate the constitutional right of workers and employees\nto self-organization, are inimical to the legitimate interests of both labor and management,\nincluding their right to bargain collectively and otherwise deal with each other in an",
      "atmosphere of freedom and mutual respect, disrupt industrial peace and hinder the\npromotion of healthy and stable labor-management relations.",
      "Consequently, unfair labor practices are not only violations of the civil rights of both labor\nand management but are also criminal offenses against the State which shall be subject to\nprosecution and punishment as herein provided.",
      "Subject to the exercise by the President or by the Secretary of Labor and Employment of\nthe powers vested in them by Articles 263 and 264 of this Code, the civil aspects of all cases\ninvolving unfair labor practices, which may include claims for actual, moral, exemplary and\nother forms of damages, attorney’s fees and other affirmative relief, shall be under the\njurisdiction of the Labor Arbiters. The Labor Arbiters shall give utmost priority to the hearing\nand resolution of all cases involving unfair labor practices. They shall resolve such cases within\nthirty (30) calendar days from the time they are submitted for decision.",
      "Recovery of civil liability in the administrative proceedings shall bar recovery under the\nCivil Code.",
      "No criminal prosecution under this Title may be instituted without a final judgment\nfinding that an unfair labor practice was committed, having been first obtained in the\npreceding paragraph. During the pendency of such administrative proceeding, the running of\nthe period of prescription of the criminal offense herein penalized shall be considered\ninterrupted: Provided, however, That the final judgment in the administrative proceedings\nshall not be binding in the criminal case nor be considered as evidence of guilt but merely as\nproof of compliance of the requirements therein set forth."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VI - UNFAIR LABOR PRACTICES",
      "Chapter I - CONCEPT"
    ],
    "language": "en",
    "old_article_number": "247"
  },
  {
    "article": "Art. 259",
    "title": "Unfair Labor Practices of Employers",
    "category": "Labor Law - Book 5",
    "simplified_text": "It shall be unlawful for an\nemployer to commit any of the following unfair labor practices:\n\n(a) To interfere with, restrain or coerce employees in the exercise of their right to self-\norganization;\n\n(b) To require as a condition of employment that a person or an employee shall not join\na labor organization or shall withdraw from one to which he belongs;\n\n(c) To contract out services or functions being performed by union members when such\nwill interfere with, restrain or coerce employees in the exercise of their right to self-\norganization;\n\n(d) To initiate, dominate, assist or otherwise interfere with the formation or\nadministration of any labor organization, including the giving of financial or other support to\nit or its organizers or supporters;\n\n(e) To discriminate in regard to wages, hours of work and other terms and conditions of\nemployment in order to encourage or discourage membership in any labor organization.\nNothing in this Code or in any other law shall stop the parties from requiring membership in a\nrecognized collective bargaining agent as a condition for employment, except those\nemployees who are already members of another union at the time of the signing of the\ncollective bargaining agreement. Employees of an appropriate bargaining unit who are not\nmembers of the recognized collective bargaining agent may be assessed a reasonable fee\nequivalent to the dues and other fees paid by members of the recognized collective bargaining\nagent, if such non-union members accept the benefits under the collective bargaining\nagreement: Provided, That the individual authorization required under Article 242, paragraph\n(o) of this Code shall not apply to the non-members of the recognized collective bargaining\nagent;\n\n(f) To dismiss, discharge or otherwise prejudice or discriminate against an employee for\nhaving given or being about to give testimony under this Code;\n\n(g) To violate the duty to bargain collectively as prescribed by this Code;\n\n(h) To pay negotiation or attorney’s fees to the union or its officers or agents as part of\nthe settlement of any issue in collective bargaining or any other dispute; or\n\n(i) To violate a collective bargaining agreement.\n\nThe provisions of the preceding paragraph notwithstanding, only the officers and agents\nof corporations, associations or partnerships who have actually participated in, authorized or\nratified unfair labor practices shall be held criminally liable.",
    "chunks": [
      "It shall be unlawful for an\nemployer to commit any of the following unfair labor practices:",
      "(a) To interfere with, restrain or coerce employees in the exercise of their right to self-\norganization;",
      "(b) To require as a condition of employment that a person or an employee shall not join\na labor organization or shall withdraw from one to which he belongs;",
      "(c) To contract out services or functions being performed by union members when such\nwill interfere with, restrain or coerce employees in the exercise of their right to self-\norganization;",
      "(d) To initiate, dominate, assist or otherwise interfere with the formation or\nadministration of any labor organization, including the giving of financial or other support to\nit or its organizers or supporters;",
      "(e) To discriminate in regard to wages, hours of work and other terms and conditions of\nemployment in order to encourage or discourage membership in any labor organization.\nNothing in this Code or in any other law shall stop the parties from requiring membership in a\nrecognized collective bargaining agent as a condition for employment, except those\nemployees who are already members of another union at the time of the signing of the\ncollective bargaining agreement. Employees of an appropriate bargaining unit who are not\nmembers of the recognized collective bargaining agent may be assessed a reasonable fee\nequivalent to the dues and other fees paid by members of the recognized collective bargaining\nagent, if such non-union members accept the benefits under the collective bargaining\nagreement: Provided, That the individual authorization required under Article 242, paragraph\n(o) of this Code shall not apply to the non-members of the recognized collective bargaining\nagent;",
      "(f) To dismiss, discharge or otherwise prejudice or discriminate against an employee for\nhaving given or being about to give testimony under this Code;",
      "(g) To violate the duty to bargain collectively as prescribed by this Code;",
      "(h) To pay negotiation or attorney’s fees to the union or its officers or agents as part of\nthe settlement of any issue in collective bargaining or any other dispute; or",
      "(i) To violate a collective bargaining agreement.",
      "The provisions of the preceding paragraph notwithstanding, only the officers and agents\nof corporations, associations or partnerships who have actually participated in, authorized or\nratified unfair labor practices shall be held criminally liable."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VI - UNFAIR LABOR PRACTICES",
      "Chapter II - UNFAIR LABOR PRACTICES OF EMPLOYERS"
    ],
    "language": "en",
    "old_article_number": "248"
  },
  {
    "article": "Art. 260",
    "title": "Unfair Labor Practices of Labor Organizations",
    "category": "Labor Law - Book 5",
    "simplified_text": "It shall be unfair labor\npractice for a labor organization, its officers, agents or representatives:\n\n(a) To restrain or coerce employees in the exercise of their right to self-organization.\nHowever, a labor organization shall have the right to prescribe its own rules with respect to\nthe acquisition or retention of membership;\n\n(b) To cause or attempt to cause an employer to discriminate against an employee,\nincluding discrimination against an employee with respect to whom membership in such\norganization has been denied or to terminate an employee on any ground other than the usual\nterms and conditions under which membership or continuation of membership is made\navailable to other members;\n\n(c) To violate the duty, or refuse to bargain collectively with the employer, provided it is\nthe representative of the employees;\n\n(d) To cause or attempt to cause an employer to pay or deliver or agree to pay or deliver\nany money or other things of value, in the nature of an exaction, for services which are not\nperformed or not to be performed, including the demand for fee for union negotiations;\n\n(e) To ask for or accept negotiation or attorney’s fees from employers as part of the\nsettlement of any issue in collective bargaining or any other dispute; or\n\n(f) To violate a collective bargaining agreement.\n\nThe provisions of the preceding paragraph notwithstanding, only the officers, members\nof governing boards, representatives or agents or members of labor associations or\norganizations who have actually participated in, authorized or ratified unfair labor practices\nshall be held criminally liable.",
    "chunks": [
      "It shall be unfair labor\npractice for a labor organization, its officers, agents or representatives:",
      "(a) To restrain or coerce employees in the exercise of their right to self-organization.\nHowever, a labor organization shall have the right to prescribe its own rules with respect to\nthe acquisition or retention of membership;",
      "(b) To cause or attempt to cause an employer to discriminate against an employee,\nincluding discrimination against an employee with respect to whom membership in such\norganization has been denied or to terminate an employee on any ground other than the usual\nterms and conditions under which membership or continuation of membership is made\navailable to other members;",
      "(c) To violate the duty, or refuse to bargain collectively with the employer, provided it is\nthe representative of the employees;",
      "(d) To cause or attempt to cause an employer to pay or deliver or agree to pay or deliver\nany money or other things of value, in the nature of an exaction, for services which are not\nperformed or not to be performed, including the demand for fee for union negotiations;",
      "(e) To ask for or accept negotiation or attorney’s fees from employers as part of the\nsettlement of any issue in collective bargaining or any other dispute; or",
      "(f) To violate a collective bargaining agreement.",
      "The provisions of the preceding paragraph notwithstanding, only the officers, members\nof governing boards, representatives or agents or members of labor associations or\norganizations who have actually participated in, authorized or ratified unfair labor practices\nshall be held criminally liable."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VI - UNFAIR LABOR PRACTICES",
      "Chapter III - UNFAIR LABOR PRACTICES OF LABOR ORGANIZATIONS"
    ],
    "language": "en",
    "old_article_number": "249"
  },
  {
    "article": "Art. 261",
    "title": "Procedure in Collective Bargaining",
    "category": "Labor Law - Book 5",
    "simplified_text": "The following procedures shall\nbe observed in collective bargaining:\n\n(a) When a party desires to negotiate an agreement, it shall serve a written notice upon\nthe other party with a statement of its proposals. The other party shall make a reply thereto\nnot later than ten (10) calendar days from receipt of such notice;\n\n(b) Should differences arise on the basis of such notice and reply, either party may request\nfor a conference which shall begin not later than ten (10) calendar days from the date of\nrequest;\n\n(c) If the dispute is not settled, the Board shall intervene upon request of either or both\nparties or at its own initiative and immediately call the parties to conciliation meetings. The\nBoard shall have the power to issue subpoenas requiring the attendance of the parties to such\n\nmeetings. It shall be the duty of the parties to participate fully and promptly in the conciliation\nmeetings the Board may call;\n\n(d) During the conciliation proceedings in the Board, the parties are prohibited from doing\nany act which may disrupt or impede the early settlement of the disputes; and\n\n(e) The Board shall exert all efforts to settle disputes amicably and encourage the parties\nto submit their case to a voluntary arbitrator.",
    "chunks": [
      "The following procedures shall\nbe observed in collective bargaining:",
      "(a) When a party desires to negotiate an agreement, it shall serve a written notice upon\nthe other party with a statement of its proposals. The other party shall make a reply thereto\nnot later than ten (10) calendar days from receipt of such notice;",
      "(b) Should differences arise on the basis of such notice and reply, either party may request\nfor a conference which shall begin not later than ten (10) calendar days from the date of\nrequest;",
      "(c) If the dispute is not settled, the Board shall intervene upon request of either or both\nparties or at its own initiative and immediately call the parties to conciliation meetings. The\nBoard shall have the power to issue subpoenas requiring the attendance of the parties to such",
      "meetings. It shall be the duty of the parties to participate fully and promptly in the conciliation\nmeetings the Board may call;",
      "(d) During the conciliation proceedings in the Board, the parties are prohibited from doing\nany act which may disrupt or impede the early settlement of the disputes; and",
      "(e) The Board shall exert all efforts to settle disputes amicably and encourage the parties\nto submit their case to a voluntary arbitrator."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "250"
  },
  {
    "article": "Art. 262",
    "title": "Duty to Bargain Collectively in the Absence of Collective Bargaining Agreements",
    "category": "Labor Law - Book 5",
    "simplified_text": "In the absence of an agreement or other voluntary arrangement providing for\na more expeditious manner of collective bargaining, it shall be the duty of employer and the\nrepresentatives of the employees to bargain collectively in accordance with the provisions of\nthis Code.",
    "chunks": [
      "In the absence of an agreement or other voluntary arrangement providing for\na more expeditious manner of collective bargaining, it shall be the duty of employer and the\nrepresentatives of the employees to bargain collectively in accordance with the provisions of\nthis Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "251"
  },
  {
    "article": "Art. 263",
    "title": "Meaning of Duty to Bargain Collectively",
    "category": "Labor Law - Book 5",
    "simplified_text": "The duty to bargain\ncollectively means the performance of a mutual obligation to meet and convene promptly and\nexpeditiously in good faith for the purpose of negotiating an agreement with respect to wages,\nhours of work and all other terms and conditions of employment including proposals for\nadjusting any grievances or questions arising under such agreement and executing a contract\nincorporating such agreements if requested by either party but such duty does not compel any\nparty to agree to a proposal or to make any concession.",
    "chunks": [
      "The duty to bargain\ncollectively means the performance of a mutual obligation to meet and convene promptly and\nexpeditiously in good faith for the purpose of negotiating an agreement with respect to wages,\nhours of work and all other terms and conditions of employment including proposals for\nadjusting any grievances or questions arising under such agreement and executing a contract\nincorporating such agreements if requested by either party but such duty does not compel any\nparty to agree to a proposal or to make any concession."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "252"
  },
  {
    "article": "Art. 264",
    "title": "Duty to Bargain Collectively When There Exists a Collective Bargaining Agreement",
    "category": "Labor Law - Book 5",
    "simplified_text": "When there is a collective bargaining agreement, the duty to bargain collectively\nshall also mean that neither party shall terminate nor modify such agreement during its\nlifetime. However, either party can serve a written notice to terminate or modify the\nagreement at least sixty (60) days prior to its expiration date. It shall be the duty of both parties\nto keep the status quo and to continue in full force and effect the terms and conditions of the\nexisting agreement during the 60-day period and/or until a new agreement is reached by the\nparties.",
    "chunks": [
      "When there is a collective bargaining agreement, the duty to bargain collectively\nshall also mean that neither party shall terminate nor modify such agreement during its\nlifetime. However, either party can serve a written notice to terminate or modify the\nagreement at least sixty (60) days prior to its expiration date. It shall be the duty of both parties\nto keep the status quo and to continue in full force and effect the terms and conditions of the\nexisting agreement during the 60-day period and/or until a new agreement is reached by the\nparties."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "253"
  },
  {
    "article": "Art. 265",
    "title": "[253-A] Terms of a Collective Bargaining Agreement",
    "category": "Labor Law - Book 5",
    "simplified_text": "Any Collective\nBargaining Agreement that the parties may enter into shall, insofar as the representation\naspect is concerned, be for a term of five (5) years. No petition questioning the majority status\nof the incumbent bargaining agent shall be entertained and no certification election shall be\nconducted by the Department of Labor and Employment outside of the sixty-day period\nimmediately before the date of expiry of such five-year term of the Collective Bargaining\nAgreement. All other provisions of the Collective Bargaining Agreement shall be renegotiated\nnot later than three (3) years after its execution. Any agreement on such other provisions of\nthe Collective Bargaining Agreement entered into within six (6) months from the date of expiry\nof the term of such other provisions as fixed in such Collective Bargaining Agreement, shall\nretroact to the day immediately following such date. If any such agreement is entered into\n\nbeyond six months, the parties shall agree on the duration of retroactivity thereof. In case of\na deadlock in the renegotiation of the Collective Bargaining Agreement, the parties may\nexercise their rights under this Code.",
    "chunks": [
      "Any Collective\nBargaining Agreement that the parties may enter into shall, insofar as the representation\naspect is concerned, be for a term of five (5) years. No petition questioning the majority status\nof the incumbent bargaining agent shall be entertained and no certification election shall be\nconducted by the Department of Labor and Employment outside of the sixty-day period\nimmediately before the date of expiry of such five-year term of the Collective Bargaining\nAgreement. All other provisions of the Collective Bargaining Agreement shall be renegotiated\nnot later than three (3) years after its execution. Any agreement on such other provisions of\nthe Collective Bargaining Agreement entered into within six (6) months from the date of expiry\nof the term of such other provisions as fixed in such Collective Bargaining Agreement, shall\nretroact to the day immediately following such date. If any such agreement is entered into",
      "beyond six months, the parties shall agree on the duration of retroactivity thereof. In case of\na deadlock in the renegotiation of the Collective Bargaining Agreement, the parties may\nexercise their rights under this Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 266",
    "title": "Injunction Prohibited",
    "category": "Labor Law - Book 5",
    "simplified_text": "No temporary or permanent injunction or\nrestraining order in any case involving or growing out of labor disputes shall be issued by any\ncourt or other entity, except as otherwise provided in Articles 218 and 264 of this Code.",
    "chunks": [
      "No temporary or permanent injunction or\nrestraining order in any case involving or growing out of labor disputes shall be issued by any\ncourt or other entity, except as otherwise provided in Articles 218 and 264 of this Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "254"
  },
  {
    "article": "Art. 267",
    "title": "Exclusive Bargaining Representation and Workers' Participation in Policy and Decision-Making",
    "category": "Labor Law - Book 5",
    "simplified_text": "The labor organization designated or selected by the majority of\nthe employees in an appropriate collective bargaining unit shall be the exclusive\nrepresentative of the employees in such unit for the purpose of collective bargaining.\nHowever, an individual employee or group of employees shall have the right at any time to\npresent grievances to their employer.\n\nAny provision of law to the contrary notwithstanding, workers shall have the right, subject\nto such rules and regulations as the Secretary of Labor and Employment may promulgate, to\nparticipate in policy and decision-making processes of the establishment where they are\nemployed insofar as said processes will directly affect their rights, benefits and welfare. For\nthis purpose, workers and employers may form labor-management councils: Provided, That\nthe representatives of the workers in such labor-management councils shall be elected by at\nleast the majority of all employees in said establishment.",
    "chunks": [
      "The labor organization designated or selected by the majority of\nthe employees in an appropriate collective bargaining unit shall be the exclusive\nrepresentative of the employees in such unit for the purpose of collective bargaining.\nHowever, an individual employee or group of employees shall have the right at any time to\npresent grievances to their employer.",
      "Any provision of law to the contrary notwithstanding, workers shall have the right, subject\nto such rules and regulations as the Secretary of Labor and Employment may promulgate, to\nparticipate in policy and decision-making processes of the establishment where they are\nemployed insofar as said processes will directly affect their rights, benefits and welfare. For\nthis purpose, workers and employers may form labor-management councils: Provided, That\nthe representatives of the workers in such labor-management councils shall be elected by at\nleast the majority of all employees in said establishment."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "255"
  },
  {
    "article": "Art. 268",
    "title": "Representation Issue in Organized Establishments",
    "category": "Labor Law - Book 5",
    "simplified_text": "In organized\nestablishments, when a verified petition questioning the majority status of the incumbent\nbargaining agent is filed by any legitimate labor organization including a national union or\nfederation which has already issued a charter certificate to its local chapter participating in the\ncertification election or a local chapter which has been issued a charter certificate by the\nnational union or federation before the Department of Labor and Employment within the sixty\n(60)-day period before the expiration of the collective bargaining agreement, the Med-Arbiter\nshall automatically order an election by secret ballot when the verified petition is supported\nby the written consent of at least twenty-five percent (25%) of all the employees in the\nbargaining unit to ascertain the will of the employees in the appropriate bargaining unit. To\nhave a valid election, at least a majority of all eligible voters in the unit must have cast their\nvotes. The labor union receiving the majority of the valid votes cast shall be certified as the\nexclusive bargaining agent of all the workers in the unit. When an election which provides for\nthree or more choices results in no choice receiving a majority of the valid votes cast, a run-\n\noff election shall be conducted between the labor unions receiving the two highest number of\nvotes: Provided, That the total number of votes for all contending unions is at least fifty\npercent (50%) of the number of votes cast. In cases where the petition was filed by a national\nunion or federation, it shall not be required to disclose the names of the local chapter’s officers\nand members.\n\nAt the expiration of the freedom period, the employer shall continue to recognize the\nmajority status of the incumbent bargaining agent where no petition for certification election\nis filed.",
    "chunks": [
      "In organized\nestablishments, when a verified petition questioning the majority status of the incumbent\nbargaining agent is filed by any legitimate labor organization including a national union or\nfederation which has already issued a charter certificate to its local chapter participating in the\ncertification election or a local chapter which has been issued a charter certificate by the\nnational union or federation before the Department of Labor and Employment within the sixty\n(60)-day period before the expiration of the collective bargaining agreement, the Med-Arbiter\nshall automatically order an election by secret ballot when the verified petition is supported\nby the written consent of at least twenty-five percent (25%) of all the employees in the\nbargaining unit to ascertain the will of the employees in the appropriate bargaining unit. To\nhave a valid election, at least a majority of all eligible voters in the unit must have cast their\nvotes. The labor union receiving the majority of the valid votes cast shall be certified as the\nexclusive bargaining agent of all the workers in the unit. When an election which provides for\nthree or more choices results in no choice receiving a majority of the valid votes cast, a run-",
      "off election shall be conducted between the labor unions receiving the two highest number of\nvotes: Provided, That the total number of votes for all contending unions is at least fifty\npercent (50%) of the number of votes cast. In cases where the petition was filed by a national\nunion or federation, it shall not be required to disclose the names of the local chapter’s officers\nand members.",
      "At the expiration of the freedom period, the employer shall continue to recognize the\nmajority status of the incumbent bargaining agent where no petition for certification election\nis filed."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "256"
  },
  {
    "article": "Art. 269",
    "title": "Petitions in Unorganized Establishments",
    "category": "Labor Law - Book 5",
    "simplified_text": "In any establishment where\nthere is no certified bargaining agent, a certification election shall automatically be conducted\nby the Med-Arbiter upon the filing of a petition by any legitimate labor organization, including\na national union or federation which has already issued a charter certificate to its local/chapter\nparticipating in the certification election or a local/chapter which has been issued a charter\ncertificate by the national union or federation. In cases where the petition was filed by a\nnational union or federation, it shall not be required to disclose the names of the local\nchapter’s officers and members.",
    "chunks": [
      "In any establishment where\nthere is no certified bargaining agent, a certification election shall automatically be conducted\nby the Med-Arbiter upon the filing of a petition by any legitimate labor organization, including\na national union or federation which has already issued a charter certificate to its local/chapter\nparticipating in the certification election or a local/chapter which has been issued a charter\ncertificate by the national union or federation. In cases where the petition was filed by a\nnational union or federation, it shall not be required to disclose the names of the local\nchapter’s officers and members."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "257"
  },
  {
    "article": "Art. 270",
    "title": "When an Employer May File Petition",
    "category": "Labor Law - Book 5",
    "simplified_text": "When requested to bargain\ncollectively, an employer may petition the Bureau for an election. If there is no existing\ncertified collective bargaining agreement in the unit, the Bureau shall, after hearing, order a\ncertification election.\n\nAll certification cases shall be decided within twenty (20) working days.\n\nThe Bureau shall conduct a certification election within twenty (20) days in accordance\nwith the rules and regulations prescribed by the Secretary of Labor.",
    "chunks": [
      "When requested to bargain\ncollectively, an employer may petition the Bureau for an election. If there is no existing\ncertified collective bargaining agreement in the unit, the Bureau shall, after hearing, order a\ncertification election.",
      "All certification cases shall be decided within twenty (20) working days.",
      "The Bureau shall conduct a certification election within twenty (20) days in accordance\nwith the rules and regulations prescribed by the Secretary of Labor."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "258"
  },
  {
    "article": "Art. 271",
    "title": "[258-A] Employer as Bystander",
    "category": "Labor Law - Book 5",
    "simplified_text": "In all cases, whether the petition for\ncertification election is filed by an employer or a legitimate labor organization, the employer\nshall not be considered a party thereto with a concomitant right to oppose a petition for\ncertification election. The employer’s participation in such proceedings shall be limited to: (1)\nbeing notified or informed of petitions of such nature; and (2) submitting the list of employees\nduring the pre-election conference should the Med-Arbiter act favorably on the petition.",
    "chunks": [
      "In all cases, whether the petition for\ncertification election is filed by an employer or a legitimate labor organization, the employer\nshall not be considered a party thereto with a concomitant right to oppose a petition for\ncertification election. The employer’s participation in such proceedings shall be limited to: (1)\nbeing notified or informed of petitions of such nature; and (2) submitting the list of employees\nduring the pre-election conference should the Med-Arbiter act favorably on the petition."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en"
  },
  {
    "article": "Art. 272",
    "title": "Appeal from Certification Election Orders",
    "category": "Labor Law - Book 5",
    "simplified_text": "Any party to an election\nmay appeal the order or results of the election as determined by the Med-Arbiter directly to\nthe Secretary of Labor and Employment on the ground that the rules and regulations or parts\nthereof established by the Secretary of Labor and Employment for the conduct of the election\nhave been violated. Such appeal shall be decided within fifteen (15) calendar days.\n\nARBITRATION",
    "chunks": [
      "Any party to an election\nmay appeal the order or results of the election as determined by the Med-Arbiter directly to\nthe Secretary of Labor and Employment on the ground that the rules and regulations or parts\nthereof established by the Secretary of Labor and Employment for the conduct of the election\nhave been violated. Such appeal shall be decided within fifteen (15) calendar days.",
      "ARBITRATION"
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - COLLECTIVE BARGAINING AND ADMINISTRATION OF AGREEMENTS"
    ],
    "language": "en",
    "old_article_number": "259"
  },
  {
    "article": "Art. 273",
    "title": "Grievance Machinery and Voluntary Arbitration",
    "category": "Labor Law - Book 5",
    "simplified_text": "The parties to a\nCollective Bargaining Agreement shall include therein provisions that will ensure the mutual\nobservance of its terms and conditions. They shall establish a machinery for the adjustment\nand resolution of grievances arising from the interpretation or implementation of their\nCollective Bargaining Agreement and those arising from the interpretation or enforcement of\ncompany personnel policies.\n\nAll grievances submitted to the grievance machinery which are not settled within seven\n(7) calendar days from the date of its submission shall automatically be referred to voluntary\narbitration prescribed in the Collective Bargaining Agreement.\n\nFor this purpose, parties to a Collective Bargaining Agreement shall name and designate\nin advance a Voluntary Arbitrator or panel of Voluntary Arbitrators, or include in the\nagreement a procedure for the selection of such Voluntary Arbitrator or panel of Voluntary\nArbitrators, preferably from the listing of qualified Voluntary Arbitrators duly accredited by\nthe Board. In case the parties fail to select a Voluntary Arbitrator or panel of Voluntary\nArbitrators, the Board shall designate the Voluntary Arbitrator or panel of Voluntary\nArbitrators, as may be necessary, pursuant to the selection procedure agreed upon in the\nCollective Bargaining Agreement, which shall act with the same force and effect as if the\nArbitrator or panel of Arbitrators have been selected by the parties as described above.",
    "chunks": [
      "The parties to a\nCollective Bargaining Agreement shall include therein provisions that will ensure the mutual\nobservance of its terms and conditions. They shall establish a machinery for the adjustment\nand resolution of grievances arising from the interpretation or implementation of their\nCollective Bargaining Agreement and those arising from the interpretation or enforcement of\ncompany personnel policies.",
      "All grievances submitted to the grievance machinery which are not settled within seven\n(7) calendar days from the date of its submission shall automatically be referred to voluntary\narbitration prescribed in the Collective Bargaining Agreement.",
      "For this purpose, parties to a Collective Bargaining Agreement shall name and designate\nin advance a Voluntary Arbitrator or panel of Voluntary Arbitrators, or include in the\nagreement a procedure for the selection of such Voluntary Arbitrator or panel of Voluntary\nArbitrators, preferably from the listing of qualified Voluntary Arbitrators duly accredited by\nthe Board. In case the parties fail to select a Voluntary Arbitrator or panel of Voluntary\nArbitrators, the Board shall designate the Voluntary Arbitrator or panel of Voluntary\nArbitrators, as may be necessary, pursuant to the selection procedure agreed upon in the\nCollective Bargaining Agreement, which shall act with the same force and effect as if the\nArbitrator or panel of Arbitrators have been selected by the parties as described above."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - A – GRIEVANCE MACHINERY AND VOLUNTARY"
    ],
    "language": "en",
    "old_article_number": "260"
  },
  {
    "article": "Art. 274",
    "title": "Jurisdiction of Voluntary Arbitrators and Panel of Voluntary Arbitrators",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Voluntary Arbitrator or panel of Voluntary Arbitrators shall have original and exclusive\njurisdiction to hear and decide all unresolved grievances arising from the interpretation or\nimplementation of the Collective Bargaining Agreement and those arising from the\ninterpretation or enforcement of company personnel policies referred to in the immediately\npreceding article. Accordingly, violations of a Collective Bargaining Agreement, except those\nwhich are gross in character, shall no longer be treated as unfair labor practice and shall be\nresolved as grievances under the Collective Bargaining Agreement. For purposes of this article,\ngross violations of Collective Bargaining Agreement shall mean flagrant and/or malicious\nrefusal to comply with the economic provisions of such agreement.\n\nThe Commission, its Regional Offices and the Regional Directors of the Department of\nLabor and Employment shall not entertain disputes, grievances or matters under the exclusive\nand original jurisdiction of the Voluntary Arbitrator or panel of Voluntary Arbitrators and shall\n\nimmediately dispose and refer the same to the Grievance Machinery or Voluntary Arbitration\nprovided in the Collective Bargaining Agreement.",
    "chunks": [
      "The Voluntary Arbitrator or panel of Voluntary Arbitrators shall have original and exclusive\njurisdiction to hear and decide all unresolved grievances arising from the interpretation or\nimplementation of the Collective Bargaining Agreement and those arising from the\ninterpretation or enforcement of company personnel policies referred to in the immediately\npreceding article. Accordingly, violations of a Collective Bargaining Agreement, except those\nwhich are gross in character, shall no longer be treated as unfair labor practice and shall be\nresolved as grievances under the Collective Bargaining Agreement. For purposes of this article,\ngross violations of Collective Bargaining Agreement shall mean flagrant and/or malicious\nrefusal to comply with the economic provisions of such agreement.",
      "The Commission, its Regional Offices and the Regional Directors of the Department of\nLabor and Employment shall not entertain disputes, grievances or matters under the exclusive\nand original jurisdiction of the Voluntary Arbitrator or panel of Voluntary Arbitrators and shall",
      "immediately dispose and refer the same to the Grievance Machinery or Voluntary Arbitration\nprovided in the Collective Bargaining Agreement."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - A – GRIEVANCE MACHINERY AND VOLUNTARY"
    ],
    "language": "en",
    "old_article_number": "261"
  },
  {
    "article": "Art. 275",
    "title": "Jurisdiction over other Labor Disputes",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Voluntary Arbitrator or\npanel of Voluntary Arbitrators, upon agreement of the parties, shall also hear and decide all\nother labor disputes including unfair labor practices and bargaining deadlocks.",
    "chunks": [
      "The Voluntary Arbitrator or\npanel of Voluntary Arbitrators, upon agreement of the parties, shall also hear and decide all\nother labor disputes including unfair labor practices and bargaining deadlocks."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - A – GRIEVANCE MACHINERY AND VOLUNTARY"
    ],
    "language": "en",
    "old_article_number": "262"
  },
  {
    "article": "Art. 276",
    "title": "[262-A] Procedures",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Voluntary Arbitrator or panel of Voluntary\nArbitrators shall have the power to hold hearings, receive evidences and take whatever action\nis necessary to resolve the issue or issues subject of the dispute, including efforts to effect a\nvoluntary settlement between parties.\n\nAll parties to the dispute shall be entitled to attend the arbitration proceedings. The\nattendance of any third party or the exclusion of any witness from the proceedings shall be\ndetermined by the Voluntary Arbitrator or panel of Voluntary Arbitrators. Hearing may be\nadjourned for cause or upon agreement by the parties.\n\nUnless the parties agree otherwise, it shall be mandatory for the Voluntary Arbitrator or\npanel of Voluntary Arbitrators to render an award or decision within twenty (20) calendar days\nfrom the date of submission of the dispute to voluntary arbitration.\n\nThe award or decision of the Voluntary Arbitrator or panel of Voluntary Arbitrators shall\ncontain the facts and the law on which it is based. It shall be final and executory after ten (10)\ncalendar days from receipt of the copy of the award or decision by the parties.\n\nUpon motion of any interested party, the Voluntary Arbitrator or panel of Voluntary\nArbitrators or the Labor Arbiter in the region where the movant resides, in case of the absence\nor incapacity of the Voluntary Arbitrator or panel of Voluntary Arbitrators, for any reason, may\nissue a writ of execution requiring either the sheriff of the Commission or regular courts or\nany public official whom the parties may designate in the submission agreement to execute\nthe final decision, order or award.",
    "chunks": [
      "The Voluntary Arbitrator or panel of Voluntary\nArbitrators shall have the power to hold hearings, receive evidences and take whatever action\nis necessary to resolve the issue or issues subject of the dispute, including efforts to effect a\nvoluntary settlement between parties.",
      "All parties to the dispute shall be entitled to attend the arbitration proceedings. The\nattendance of any third party or the exclusion of any witness from the proceedings shall be\ndetermined by the Voluntary Arbitrator or panel of Voluntary Arbitrators. Hearing may be\nadjourned for cause or upon agreement by the parties.",
      "Unless the parties agree otherwise, it shall be mandatory for the Voluntary Arbitrator or\npanel of Voluntary Arbitrators to render an award or decision within twenty (20) calendar days\nfrom the date of submission of the dispute to voluntary arbitration.",
      "The award or decision of the Voluntary Arbitrator or panel of Voluntary Arbitrators shall\ncontain the facts and the law on which it is based. It shall be final and executory after ten (10)\ncalendar days from receipt of the copy of the award or decision by the parties.",
      "Upon motion of any interested party, the Voluntary Arbitrator or panel of Voluntary\nArbitrators or the Labor Arbiter in the region where the movant resides, in case of the absence\nor incapacity of the Voluntary Arbitrator or panel of Voluntary Arbitrators, for any reason, may\nissue a writ of execution requiring either the sheriff of the Commission or regular courts or\nany public official whom the parties may designate in the submission agreement to execute\nthe final decision, order or award."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - A – GRIEVANCE MACHINERY AND VOLUNTARY"
    ],
    "language": "en"
  },
  {
    "article": "Art. 277",
    "title": "[262-B] Cost of Voluntary Arbitration and Voluntary Arbitrator’s Fee",
    "category": "Labor Law - Book 5",
    "simplified_text": "The\nparties to a Collective Bargaining Agreement shall provide therein a proportionate sharing\nscheme on the cost of voluntary arbitration including the Voluntary Arbitrator’s fee. The fixing\nof fee of Voluntary Arbitrators, or panel of Voluntary Arbitrators, whether shouldered wholly\nby the parties or subsidized by the Special Voluntary Arbitration Fund, shall take into account\nthe following factors:\n\n(a) Nature of the case;\n\n(b) Time consumed in hearing the case;\n\n(c) Professional standing of the Voluntary Arbitrator;\n\n(d) Capacity to pay of the parties; and\n\n(e) Fees provided for in the Revised Rules of Court.",
    "chunks": [
      "The\nparties to a Collective Bargaining Agreement shall provide therein a proportionate sharing\nscheme on the cost of voluntary arbitration including the Voluntary Arbitrator’s fee. The fixing\nof fee of Voluntary Arbitrators, or panel of Voluntary Arbitrators, whether shouldered wholly\nby the parties or subsidized by the Special Voluntary Arbitration Fund, shall take into account\nthe following factors:",
      "(a) Nature of the case;",
      "(b) Time consumed in hearing the case;",
      "(c) Professional standing of the Voluntary Arbitrator;",
      "(d) Capacity to pay of the parties; and",
      "(e) Fees provided for in the Revised Rules of Court."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VII - A – GRIEVANCE MACHINERY AND VOLUNTARY"
    ],
    "language": "en"
  },
  {
    "article": "Art. 278",
    "title": "Strikes, Picketing, and Lockouts",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) It is the policy of the State to\nencourage free trade unionism and free collective bargaining.\n\n(b) Workers shall have the right to engage in concerted activities for purposes of collective\nbargaining or for their mutual benefit and protection. The right of legitimate labor\norganizations to strike and picket and of employers to lockout, consistent with the national\ninterest, shall continue to be recognized and respected. However, no labor union may strike\nand no employer may declare a lockout on grounds involving inter-union and intra-union\ndisputes.\n\n(c) In cases of bargaining deadlocks, the duly certified or recognized bargaining agent may\nfile a notice of strike or the employer may file a notice of lockout with the Ministry at least 30\ndays before the intended date thereof. In cases of unfair labor practice, the period of notice\nshall be 15 days and in the absence of a duly certified or recognized bargaining agent, the\nnotice of strike may be filed by any legitimate labor organization in behalf of its members.\nHowever, in case of dismissal from employment of union officers duly elected in accordance\nwith the union constitution and by-laws, which may constitute union busting where the\nexistence of the union is threatened, the 15-day cooling-off period shall not apply and the\nunion may take action immediately.\n\n(d) The notice must be in accordance with such implementing rules and regulations as the\nMinister of Labor and Employment may promulgate.\n\n(e) During the cooling-off period, it shall be the duty of the Ministry to exert all efforts at\nmediation and conciliation to effect a voluntary settlement. Should the dispute remain\nunsettled until the lapse of the requisite number of days from the mandatory filing of the\nnotice, the labor union may strike or the employer may declare a lockout.\n\n(f) A decision to declare a strike must be approved by a majority of the total union\nmembership in the bargaining unit concerned, obtained by secret ballot in meetings or\nreferenda called for that purpose. A decision to declare a lockout must be approved by a\n\nmajority of the board of directors of the corporation or association or of the partners in a\npartnership, obtained by secret ballot in a meeting called for that purpose. The decision shall\nbe valid for the duration of the dispute based on substantially the same grounds considered\nwhen the strike or lockout vote was taken. The Ministry may, at its own initiative or upon the\nrequest of any affected party, supervise the conduct of the secret balloting. In every case, the\nunion or the employer shall furnish the Ministry the results of the voting at least seven days\nbefore the intended strike or lockout, subject to the cooling-off period herein provided.\n\n(g) When, in his opinion, there exists a labor dispute causing or likely to cause a strike or\nlockout in an industry indispensable to the national interest, the Secretary of Labor and\nEmployment may assume jurisdiction over the dispute and decide it or certify the same to the\nCommission for compulsory arbitration. Such assumption or certification shall have the effect\nof automatically enjoining the intended or impending strike or lockout as specified in the\nassumption or certification order. If one has already taken place at the time of assumption or\ncertification, all striking or locked out employees shall immediately return to work and the\nemployer shall immediately resume operations and readmit all workers under the same terms\nand conditions prevailing before the strike or lockout. The Secretary of Labor and Employment\nor the Commission may seek the assistance of law enforcement agencies to ensure compliance\nwith this provision as well as with such orders as he may issue to enforce the same.\n\nIn line with the national concern for and the highest respect accorded to the right of\npatients to life and health, strikes and lockouts in hospitals, clinics and similar medical\ninstitutions shall, to every extent possible, be avoided, and all serious efforts, not only by labor\nand management but government as well, be exhausted to substantially minimize, if not\nprevent, their adverse effects on such life and health, through the exercise, however\nlegitimate, by labor of its right to strike and by management to lockout. In labor disputes\nadversely affecting the continued operation of such hospitals, clinics or medical institutions, it\nshall be the duty of the striking union or locking-out employer to provide and maintain an\neffective skeletal workforce of medical and other health personnel, whose movement and\nservices shall be unhampered and unrestricted, as are necessary to insure the proper and\nadequate protection of the life and health of its patients, most especially emergency cases, for\nthe duration of the strike or lockout. In such cases, therefore, the Secretary of Labor and\nEmployment may immediately assume, within twenty four (24) hours from knowledge of the\noccurrence of such a strike or lockout, jurisdiction over the same or certify it to the\nCommission for compulsory arbitration. For this purpose, the contending parties are strictly\nenjoined to comply with such orders, prohibitions and/or injunctions as are issued by the\nSecretary of Labor and Employment or the Commission, under pain of immediate disciplinary\naction, including dismissal or loss of employment status or payment by the locking-out\nemployer of backwages, damages and other affirmative relief, even criminal prosecution\nagainst either or both of them.\n\nThe foregoing notwithstanding, the President of the Philippines shall not be precluded\nfrom determining the industries that, in his opinion, are indispensable to the national interest,\n\nand from intervening at any time and assuming jurisdiction over any such labor dispute in\norder to settle or terminate the same.\n\n(h) Before or at any stage of the compulsory arbitration process, the parties may opt to\nsubmit their dispute to voluntary arbitration.\n\n(i) The Secretary of Labor and Employment, the Commission or the voluntary arbitrator\nor panel of voluntary arbitrators shall decide or resolve the dispute within thirty (30) calendar\ndays from the date of the assumption of jurisdiction or the certification or submission of the\ndispute, as the case may be. The decision of the President, the Secretary of Labor and\nEmployment, the Commission or the voluntary arbitrator shall be final and executory ten (10)\ncalendar days after receipt thereof by the parties.",
    "chunks": [
      "(a) It is the policy of the State to\nencourage free trade unionism and free collective bargaining.",
      "(b) Workers shall have the right to engage in concerted activities for purposes of collective\nbargaining or for their mutual benefit and protection. The right of legitimate labor\norganizations to strike and picket and of employers to lockout, consistent with the national\ninterest, shall continue to be recognized and respected. However, no labor union may strike\nand no employer may declare a lockout on grounds involving inter-union and intra-union\ndisputes.",
      "(c) In cases of bargaining deadlocks, the duly certified or recognized bargaining agent may\nfile a notice of strike or the employer may file a notice of lockout with the Ministry at least 30\ndays before the intended date thereof. In cases of unfair labor practice, the period of notice\nshall be 15 days and in the absence of a duly certified or recognized bargaining agent, the\nnotice of strike may be filed by any legitimate labor organization in behalf of its members.\nHowever, in case of dismissal from employment of union officers duly elected in accordance\nwith the union constitution and by-laws, which may constitute union busting where the\nexistence of the union is threatened, the 15-day cooling-off period shall not apply and the\nunion may take action immediately.",
      "(d) The notice must be in accordance with such implementing rules and regulations as the\nMinister of Labor and Employment may promulgate.",
      "(e) During the cooling-off period, it shall be the duty of the Ministry to exert all efforts at\nmediation and conciliation to effect a voluntary settlement. Should the dispute remain\nunsettled until the lapse of the requisite number of days from the mandatory filing of the\nnotice, the labor union may strike or the employer may declare a lockout.",
      "(f) A decision to declare a strike must be approved by a majority of the total union\nmembership in the bargaining unit concerned, obtained by secret ballot in meetings or\nreferenda called for that purpose. A decision to declare a lockout must be approved by a",
      "majority of the board of directors of the corporation or association or of the partners in a\npartnership, obtained by secret ballot in a meeting called for that purpose. The decision shall\nbe valid for the duration of the dispute based on substantially the same grounds considered\nwhen the strike or lockout vote was taken. The Ministry may, at its own initiative or upon the\nrequest of any affected party, supervise the conduct of the secret balloting. In every case, the\nunion or the employer shall furnish the Ministry the results of the voting at least seven days\nbefore the intended strike or lockout, subject to the cooling-off period herein provided.",
      "(g) When, in his opinion, there exists a labor dispute causing or likely to cause a strike or\nlockout in an industry indispensable to the national interest, the Secretary of Labor and\nEmployment may assume jurisdiction over the dispute and decide it or certify the same to the\nCommission for compulsory arbitration. Such assumption or certification shall have the effect\nof automatically enjoining the intended or impending strike or lockout as specified in the\nassumption or certification order. If one has already taken place at the time of assumption or\ncertification, all striking or locked out employees shall immediately return to work and the\nemployer shall immediately resume operations and readmit all workers under the same terms\nand conditions prevailing before the strike or lockout. The Secretary of Labor and Employment\nor the Commission may seek the assistance of law enforcement agencies to ensure compliance\nwith this provision as well as with such orders as he may issue to enforce the same.",
      "In line with the national concern for and the highest respect accorded to the right of\npatients to life and health, strikes and lockouts in hospitals, clinics and similar medical\ninstitutions shall, to every extent possible, be avoided, and all serious efforts, not only by labor\nand management but government as well, be exhausted to substantially minimize, if not\nprevent, their adverse effects on such life and health, through the exercise, however\nlegitimate, by labor of its right to strike and by management to lockout. In labor disputes\nadversely affecting the continued operation of such hospitals, clinics or medical institutions, it\nshall be the duty of the striking union or locking-out employer to provide and maintain an\neffective skeletal workforce of medical and other health personnel, whose movement and\nservices shall be unhampered and unrestricted, as are necessary to insure the proper and\nadequate protection of the life and health of its patients, most especially emergency cases, for\nthe duration of the strike or lockout. In such cases, therefore, the Secretary of Labor and\nEmployment may immediately assume, within twenty four (24) hours from knowledge of the\noccurrence of such a strike or lockout, jurisdiction over the same or certify it to the\nCommission for compulsory arbitration. For this purpose, the contending parties are strictly\nenjoined to comply with such orders, prohibitions and/or injunctions as are issued by the\nSecretary of Labor and Employment or the Commission, under pain of immediate disciplinary\naction, including dismissal or loss of employment status or payment by the locking-out\nemployer of backwages, damages and other affirmative relief, even criminal prosecution\nagainst either or both of them.",
      "The foregoing notwithstanding, the President of the Philippines shall not be precluded\nfrom determining the industries that, in his opinion, are indispensable to the national interest,",
      "and from intervening at any time and assuming jurisdiction over any such labor dispute in\norder to settle or terminate the same.",
      "(h) Before or at any stage of the compulsory arbitration process, the parties may opt to\nsubmit their dispute to voluntary arbitration.",
      "(i) The Secretary of Labor and Employment, the Commission or the voluntary arbitrator\nor panel of voluntary arbitrators shall decide or resolve the dispute within thirty (30) calendar\ndays from the date of the assumption of jurisdiction or the certification or submission of the\ndispute, as the case may be. The decision of the President, the Secretary of Labor and\nEmployment, the Commission or the voluntary arbitrator shall be final and executory ten (10)\ncalendar days after receipt thereof by the parties."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter I - STRIKES AND LOCKOUTS"
    ],
    "language": "en",
    "old_article_number": "263"
  },
  {
    "article": "Art. 279",
    "title": "Prohibited activities",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) No labor organization or employer shall\ndeclare a strike or lockout without first having bargained collectively in accordance with Title\nVII of this Book or without first having filed the notice required in the preceding Article or\nwithout the necessary strike or lockout vote first having been obtained and reported to the\nMinistry.\n\nNo strike or lockout shall be declared after assumption of jurisdiction by the President or\nthe Minister or after certification or submission of the dispute to compulsory or voluntary\narbitration or during the pendency of cases involving the same grounds for the strike or\nlockout.\n\nAny worker whose employment has been terminated as a consequence of any unlawful\nlockout shall be entitled to reinstatement with full backwages. Any union officer who\nknowingly participates in an illegal strike and any worker or union officer who knowingly\nparticipates in the commission of illegal acts during a strike may be declared to have lost his\nemployment status: Provided, That mere participation of a worker in a lawful strike shall not\nconstitute sufficient ground for termination of his employment, even if a replacement had\nbeen hired by the employer during such lawful strike.\n\n(b) No person shall obstruct, impede, or interfere with by force, violence, coercion,\nthreats or intimidation, any peaceful picketing by employees during any labor controversy or\nin the exercise of the right to self-organization or collective bargaining, or shall aid or abet such\nobstruction or interference.\n\n(c) No employer shall use or employ any strike-breaker, nor shall any person be employed\nas a strike-breaker.\n\n(d) No public official or employee, including officers and personnel of the New Armed\nForces of the Philippines or the Integrated National Police, or armed person, shall bring in,\nintroduce or escort in any manner, any individual who seeks to replace strikers in entering or\nleaving the premises of a strike area, or work in place of the strikers. The police force shall\nkeep out of the picket lines unless actual violence or other criminal acts occur therein:\nProvided, That nothing herein shall be interpreted to prevent any public officer from taking\nany measure necessary to maintain peace and order, protect life and property, and/or enforce\nthe law and legal orders.\n\n(e) No person engaged in picketing shall commit any act of violence, coercion or\nintimidation or obstruct the free ingress to or egress from the employer’s premises for lawful\npurposes, or obstruct public thoroughfares.",
    "chunks": [
      "(a) No labor organization or employer shall\ndeclare a strike or lockout without first having bargained collectively in accordance with Title\nVII of this Book or without first having filed the notice required in the preceding Article or\nwithout the necessary strike or lockout vote first having been obtained and reported to the\nMinistry.",
      "No strike or lockout shall be declared after assumption of jurisdiction by the President or\nthe Minister or after certification or submission of the dispute to compulsory or voluntary\narbitration or during the pendency of cases involving the same grounds for the strike or\nlockout.",
      "Any worker whose employment has been terminated as a consequence of any unlawful\nlockout shall be entitled to reinstatement with full backwages. Any union officer who\nknowingly participates in an illegal strike and any worker or union officer who knowingly\nparticipates in the commission of illegal acts during a strike may be declared to have lost his\nemployment status: Provided, That mere participation of a worker in a lawful strike shall not\nconstitute sufficient ground for termination of his employment, even if a replacement had\nbeen hired by the employer during such lawful strike.",
      "(b) No person shall obstruct, impede, or interfere with by force, violence, coercion,\nthreats or intimidation, any peaceful picketing by employees during any labor controversy or\nin the exercise of the right to self-organization or collective bargaining, or shall aid or abet such\nobstruction or interference.",
      "(c) No employer shall use or employ any strike-breaker, nor shall any person be employed\nas a strike-breaker.",
      "(d) No public official or employee, including officers and personnel of the New Armed\nForces of the Philippines or the Integrated National Police, or armed person, shall bring in,\nintroduce or escort in any manner, any individual who seeks to replace strikers in entering or\nleaving the premises of a strike area, or work in place of the strikers. The police force shall\nkeep out of the picket lines unless actual violence or other criminal acts occur therein:\nProvided, That nothing herein shall be interpreted to prevent any public officer from taking\nany measure necessary to maintain peace and order, protect life and property, and/or enforce\nthe law and legal orders.",
      "(e) No person engaged in picketing shall commit any act of violence, coercion or\nintimidation or obstruct the free ingress to or egress from the employer’s premises for lawful\npurposes, or obstruct public thoroughfares."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter I - STRIKES AND LOCKOUTS"
    ],
    "language": "en",
    "old_article_number": "264"
  },
  {
    "article": "Art. 280",
    "title": "Improved Offer Balloting",
    "category": "Labor Law - Book 5",
    "simplified_text": "In an effort to settle a strike, the\nDepartment of Labor and Employment shall conduct a referendum by secret balloting on the\nimproved offer of the employer on or before the 30th day of the strike. When at least a\nmajority of the union members vote to accept the improved offer the striking workers shall\nimmediately return to work and the employer shall thereupon readmit them upon the signing\nof the agreement.\n\nIn case of a lockout, the Department of Labor and Employment shall also conduct a\nreferendum by secret balloting on the reduced offer of the union on or before the 30th day of\nthe lockout. When at least a majority of the board of directors or trustees or the partners\nholding the controlling interest in the case of a partnership vote to accept the reduced offer,\nthe workers shall immediately return to work and the employer shall thereupon readmit them\nupon the signing of the agreement.",
    "chunks": [
      "In an effort to settle a strike, the\nDepartment of Labor and Employment shall conduct a referendum by secret balloting on the\nimproved offer of the employer on or before the 30th day of the strike. When at least a\nmajority of the union members vote to accept the improved offer the striking workers shall\nimmediately return to work and the employer shall thereupon readmit them upon the signing\nof the agreement.",
      "In case of a lockout, the Department of Labor and Employment shall also conduct a\nreferendum by secret balloting on the reduced offer of the union on or before the 30th day of\nthe lockout. When at least a majority of the board of directors or trustees or the partners\nholding the controlling interest in the case of a partnership vote to accept the reduced offer,\nthe workers shall immediately return to work and the employer shall thereupon readmit them\nupon the signing of the agreement."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter I - STRIKES AND LOCKOUTS"
    ],
    "language": "en",
    "old_article_number": "265"
  },
  {
    "article": "Art. 281",
    "title": "Requirement for Arrest and Detention",
    "category": "Labor Law - Book 5",
    "simplified_text": "Except on grounds of national\nsecurity and public peace or in case of commission of a crime, no union members or union\norganizers may be arrested or detained for union activities without previous consultations\nwith the Secretary of Labor.",
    "chunks": [
      "Except on grounds of national\nsecurity and public peace or in case of commission of a crime, no union members or union\norganizers may be arrested or detained for union activities without previous consultations\nwith the Secretary of Labor."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter I - STRIKES AND LOCKOUTS"
    ],
    "language": "en",
    "old_article_number": "266"
  },
  {
    "article": "Art. 282",
    "title": "Assistance by the Department of Labor",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Department of Labor, at\nthe initiative of the Secretary of Labor, shall extend special assistance to the organization, for\npurposes of collective bargaining, of the most underprivileged workers who, for reasons of\noccupation, organizational structure or insufficient incomes, are not normally covered by\nmajor labor organizations or federations.",
    "chunks": [
      "The Department of Labor, at\nthe initiative of the Secretary of Labor, shall extend special assistance to the organization, for\npurposes of collective bargaining, of the most underprivileged workers who, for reasons of\noccupation, organizational structure or insufficient incomes, are not normally covered by\nmajor labor organizations or federations."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter II - ASSISTANCE TO LABOR ORGANIZATIONS"
    ],
    "language": "en",
    "old_article_number": "267"
  },
  {
    "article": "Art. 283",
    "title": "Assistance by the Institute of Labor and Manpower Studies",
    "category": "Labor Law - Book 5",
    "simplified_text": "The\nInstitute of Labor and Manpower Studies shall render technical and other forms of assistance\nto labor organizations and employer organizations in the field of labor education, especially\npertaining to collective bargaining, arbitration, labor standards and the Labor Code of the\nPhilippines in general.",
    "chunks": [
      "The\nInstitute of Labor and Manpower Studies shall render technical and other forms of assistance\nto labor organizations and employer organizations in the field of labor education, especially\npertaining to collective bargaining, arbitration, labor standards and the Labor Code of the\nPhilippines in general."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter II - ASSISTANCE TO LABOR ORGANIZATIONS"
    ],
    "language": "en",
    "old_article_number": "268"
  },
  {
    "article": "Art. 284",
    "title": "Prohibition Against Aliens; Exceptions",
    "category": "Labor Law - Book 5",
    "simplified_text": "All aliens, natural or juridical,\nas well as foreign organizations are strictly prohibited from engaging directly or indirectly in\nall forms of trade union activities without prejudice to normal contacts between Philippine\nlabor unions and recognized international labor centers: Provided, however, That aliens\nworking in the country with valid permits issued by the Department of Labor and Employment,\nmay exercise the right to self-organization and join or assist labor organizations of their own\nchoosing for purposes of collective bargaining: Provided, further, That said aliens are nationals\nof a country which grants the same or similar rights to Filipino workers.",
    "chunks": [
      "All aliens, natural or juridical,\nas well as foreign organizations are strictly prohibited from engaging directly or indirectly in\nall forms of trade union activities without prejudice to normal contacts between Philippine\nlabor unions and recognized international labor centers: Provided, however, That aliens\nworking in the country with valid permits issued by the Department of Labor and Employment,\nmay exercise the right to self-organization and join or assist labor organizations of their own\nchoosing for purposes of collective bargaining: Provided, further, That said aliens are nationals\nof a country which grants the same or similar rights to Filipino workers."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter III - FOREIGN ACTIVITIES"
    ],
    "language": "en",
    "old_article_number": "269"
  },
  {
    "article": "Art. 285",
    "title": "Regulations of Foreign Assistance",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) No foreign individual,\norganization or entity may give any donations, grants or other forms of assistance, in cash or\nin kind, directly or indirectly, to any labor organization, group of workers or any auxiliary\nthereof, such as cooperatives, credit unions and institutions engaged in research, education\nor communication, in relation to trade union activities, without prior permission by the\nSecretary of Labor.\n\n“Trade union activities\" shall mean:\n\n(1) organization, formation and administration of labor organization;\n\n(2) negotiation and administration of collective bargaining agreements;\n\n(3) all forms of concerted union action;\n\n(4) organizing, managing, or assisting union conventions, meetings, rallies, referenda,\nteach-ins, seminars, conferences and institutes;\n\n(5) any form of participation or involvement in representation proceedings,\nrepresentation elections, consent elections, union elections; and\n\n(6) other activities or actions analogous to the foregoing.\n\n(b) This prohibition shall equally apply to foreign donations, grants or other forms of\nassistance, in cash or in kind, given directly or indirectly to any employer or employer’s\norganization to support any activity or activities affecting trade unions.\n\n(c) The Secretary of Labor shall promulgate rules and regulations to regulate and control\nthe giving and receiving of such donations, grants, or other forms of assistance, including the\nmandatory reporting of the amounts of the donations or grants, the specific recipients thereof,\nthe projects or activities proposed to be supported, and their duration.",
    "chunks": [
      "(a) No foreign individual,\norganization or entity may give any donations, grants or other forms of assistance, in cash or\nin kind, directly or indirectly, to any labor organization, group of workers or any auxiliary\nthereof, such as cooperatives, credit unions and institutions engaged in research, education\nor communication, in relation to trade union activities, without prior permission by the\nSecretary of Labor.",
      "“Trade union activities\" shall mean:",
      "(1) organization, formation and administration of labor organization;",
      "(2) negotiation and administration of collective bargaining agreements;",
      "(3) all forms of concerted union action;",
      "(4) organizing, managing, or assisting union conventions, meetings, rallies, referenda,\nteach-ins, seminars, conferences and institutes;",
      "(5) any form of participation or involvement in representation proceedings,\nrepresentation elections, consent elections, union elections; and",
      "(6) other activities or actions analogous to the foregoing.",
      "(b) This prohibition shall equally apply to foreign donations, grants or other forms of\nassistance, in cash or in kind, given directly or indirectly to any employer or employer’s\norganization to support any activity or activities affecting trade unions.",
      "(c) The Secretary of Labor shall promulgate rules and regulations to regulate and control\nthe giving and receiving of such donations, grants, or other forms of assistance, including the\nmandatory reporting of the amounts of the donations or grants, the specific recipients thereof,\nthe projects or activities proposed to be supported, and their duration."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter III - FOREIGN ACTIVITIES"
    ],
    "language": "en",
    "old_article_number": "270"
  },
  {
    "article": "Art. 286",
    "title": "Applicability to Farm Tenants and Rural Workers",
    "category": "Labor Law - Book 5",
    "simplified_text": "The provisions of this\nTitle pertaining to foreign organizations and activities shall be deemed applicable likewise to\nall organizations of farm tenants, rural workers and the like: Provided, That in appropriate\ncases, the Secretary of Agrarian Reform shall exercise the powers and responsibilities vested\nby this Title in the Secretary of Labor.",
    "chunks": [
      "The provisions of this\nTitle pertaining to foreign organizations and activities shall be deemed applicable likewise to\nall organizations of farm tenants, rural workers and the like: Provided, That in appropriate\ncases, the Secretary of Agrarian Reform shall exercise the powers and responsibilities vested\nby this Title in the Secretary of Labor."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter III - FOREIGN ACTIVITIES"
    ],
    "language": "en",
    "old_article_number": "271"
  },
  {
    "article": "Art. 287",
    "title": "Penalties",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) Any person violating any of the provisions of Article 264\nof this Code shall be punished by a fine of not less than one thousand pesos (P1,000.00) nor\nmore than ten thousand pesos (P10,000.00) and/or imprisonment for not less than three\nmonths nor more than three (3) years, or both such fine and imprisonment, at the discretion\nof the court. Prosecution under this provision shall preclude prosecution for the same act\nunder the Revised Penal Code, and vice versa.\n\n(b) Upon the recommendation of the Minister of Labor and Employment and the Minister\nof National Defense, foreigners who violate the provisions of this Title shall be subject to\nimmediate and summary deportation by the Commission on Immigration and Deportation and\nshall be permanently barred from re-entering the country without the special permission of\nthe President of the Philippines.",
    "chunks": [
      "(a) Any person violating any of the provisions of Article 264\nof this Code shall be punished by a fine of not less than one thousand pesos (P1,000.00) nor\nmore than ten thousand pesos (P10,000.00) and/or imprisonment for not less than three\nmonths nor more than three (3) years, or both such fine and imprisonment, at the discretion\nof the court. Prosecution under this provision shall preclude prosecution for the same act\nunder the Revised Penal Code, and vice versa.",
      "(b) Upon the recommendation of the Minister of Labor and Employment and the Minister\nof National Defense, foreigners who violate the provisions of this Title shall be subject to\nimmediate and summary deportation by the Commission on Immigration and Deportation and\nshall be permanently barred from re-entering the country without the special permission of\nthe President of the Philippines."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title VIII - STRIKES AND LOCKOUTS AND FOREIGN INVOLVEMENT IN TRADE UNION ACTIVITIES",
      "Chapter IV - PENALTIES FOR VIOLATION"
    ],
    "language": "en",
    "old_article_number": "272"
  },
  {
    "article": "Art. 288",
    "title": "Study of Labor-Management Relations",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Secretary of Labor shall\nhave the power and it shall be his duty to inquire into:\n\n(a) the existing relations between employers and employees in the Philippines;\n\n(b) the growth of associations of employees and the effect of such associations upon\nemployer-employee relations;\n\n(c) the extent and results of the methods of collective bargaining in the determination of\nterms and conditions of employment;\n\n(d) the methods which have been tried by employers and associations of employees for\nmaintaining mutually satisfactory relations;\n\n(e) desirable industrial practices which have been developed through collective\nbargaining and other voluntary arrangements;\n\n(f) the possible ways of increasing the usefulness and efficiency of collective bargaining\nfor settling differences;\n\n(g) the possibilities for the adoption of practical and effective methods of labor-\nmanagement cooperation;\n\n(h) any other aspects of employer-employee relations concerning the promotion of\nharmony and understanding between the parties; and\n\n(i) the relevance of labor laws and labor relations to national development.\n\nThe Secretary of Labor shall also inquire into the causes of industrial unrest and take all\nthe necessary steps within his power as may be prescribed by law to alleviate the same, and\nshall from time to time recommend the enactment of such remedial legislation as in his\njudgment may be desirable for the maintenance and promotion of industrial peace.",
    "chunks": [
      "The Secretary of Labor shall\nhave the power and it shall be his duty to inquire into:",
      "(a) the existing relations between employers and employees in the Philippines;",
      "(b) the growth of associations of employees and the effect of such associations upon\nemployer-employee relations;",
      "(c) the extent and results of the methods of collective bargaining in the determination of\nterms and conditions of employment;",
      "(d) the methods which have been tried by employers and associations of employees for\nmaintaining mutually satisfactory relations;",
      "(e) desirable industrial practices which have been developed through collective\nbargaining and other voluntary arrangements;",
      "(f) the possible ways of increasing the usefulness and efficiency of collective bargaining\nfor settling differences;",
      "(g) the possibilities for the adoption of practical and effective methods of labor-\nmanagement cooperation;",
      "(h) any other aspects of employer-employee relations concerning the promotion of\nharmony and understanding between the parties; and",
      "(i) the relevance of labor laws and labor relations to national development.",
      "The Secretary of Labor shall also inquire into the causes of industrial unrest and take all\nthe necessary steps within his power as may be prescribed by law to alleviate the same, and\nshall from time to time recommend the enactment of such remedial legislation as in his\njudgment may be desirable for the maintenance and promotion of industrial peace."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IX - SPECIAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "273"
  },
  {
    "article": "Art. 289",
    "title": "Visitorial Power",
    "category": "Labor Law - Book 5",
    "simplified_text": "The Secretary of Labor and Employment or his duly\nauthorized representative is hereby empowered to inquire into financial activities of\nlegitimate labor organizations upon the filing of a complaint under oath and duly supported\nby the written consent of at least twenty percent (20%) of the total membership of the labor\norganization concerned and to examine their books of accounts and other records to\ndetermine compliance or non-compliance with the law and to prosecute any violations of the\nlaw and the union constitution and by-laws: Provided, That such inquiry or examination shall\nnot be conducted during the sixty (60) days freedom period nor within the thirty (30) days\nimmediately preceding the date of election of union officials.",
    "chunks": [
      "The Secretary of Labor and Employment or his duly\nauthorized representative is hereby empowered to inquire into financial activities of\nlegitimate labor organizations upon the filing of a complaint under oath and duly supported\nby the written consent of at least twenty percent (20%) of the total membership of the labor\norganization concerned and to examine their books of accounts and other records to\ndetermine compliance or non-compliance with the law and to prosecute any violations of the\nlaw and the union constitution and by-laws: Provided, That such inquiry or examination shall\nnot be conducted during the sixty (60) days freedom period nor within the thirty (30) days\nimmediately preceding the date of election of union officials."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IX - SPECIAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "274"
  },
  {
    "article": "Art. 290",
    "title": "Tripartism, Tripartite Conferences, and Tripartite Industrial Peace Councils",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) Tripartism in labor relations is hereby declared a State policy. Towards this\nend, workers and employers shall, as far as practicable, be represented in decision and policy-\nmaking bodies of the government.\n\n(b) The Secretary of Labor and Employment or his duly authorized representatives may\nfrom time to time call a national, regional, or industrial tripartite conference of representatives\nof government, workers and employers, and other interest groups as the case may be, for the\nconsideration and adoption of voluntary codes of principles designed to promote industrial\npeace based on social justice or to align labor movement relations with established priorities\nin economic and social development. In calling such conference, the Secretary of Labor and\nEmployment may consult with accredited representatives of workers and employers.\n\n(c) A National Tripartite Industrial Peace Council (NTIPC) shall be established, headed by\nthe Secretary of Labor and Employment, with twenty (20) representatives each from the labor\nand employers’ sectors to be designated by the President at regular intervals. For this purpose,\na sectoral nomination, selection, and recall process shall be established by the DOLE in\nconsultation with the sectors observing the ‘most representative’ organization criteria of ILO\nConvention No. 144.\n\nTripartite Industrial Peace Councils (TIPCs) at the regional or industry level shall also be\nestablished with representatives from government, workers and employers to serve as a\ncontinuing forum for tripartite advisement and consultation in aid of streamlining the role of\ngovernment, empowering workers’ and employers’ organizations, enhancing their respective\nrights, attaining industrial peace, and improving productivity.\n\nThe TIPCs shall have the following functions:\n\n(1) Monitor the full implementation and compliance of concerned sectors with the\nprovisions of all tripartite instruments, including international conventions and declarations,\ncodes of conduct, and social accords;\n\n(2) Participate in national, regional or industry-specific tripartite conferences which the\nPresident or the Secretary of Labor and Employment may call from time to time;\n\n(3) Review existing labor, economic and social policies and evaluate local and\ninternational developments affecting them;\n\n(4) Formulate, for submission to the President or to Congress, tripartite views,\nrecommendations and proposals on labor, economic, and social concerns, including the\npresentation of tripartite positions on relevant bills pending in Congress;\n\n(5) Advise the Secretary of Labor and Employment in the formulation or implementation\nof policies and legislation affecting labor and employment;\n\n(6) Serve as a communication channel and a mechanism for undertaking joint programs\namong government, workers, employers and their organizations toward enhancing labor-\nmanagement relations; and\n\n(7) Adopt its own program of activities and rules, consistent with development objectives.\n\nAll TIPCs shall be an integral part of the organizational structure of the NTIPC.\n\nThe operations of all TIPCs shall be funded from the regular budget of the DOLE.",
    "chunks": [
      "(a) Tripartism in labor relations is hereby declared a State policy. Towards this\nend, workers and employers shall, as far as practicable, be represented in decision and policy-\nmaking bodies of the government.",
      "(b) The Secretary of Labor and Employment or his duly authorized representatives may\nfrom time to time call a national, regional, or industrial tripartite conference of representatives\nof government, workers and employers, and other interest groups as the case may be, for the\nconsideration and adoption of voluntary codes of principles designed to promote industrial\npeace based on social justice or to align labor movement relations with established priorities\nin economic and social development. In calling such conference, the Secretary of Labor and\nEmployment may consult with accredited representatives of workers and employers.",
      "(c) A National Tripartite Industrial Peace Council (NTIPC) shall be established, headed by\nthe Secretary of Labor and Employment, with twenty (20) representatives each from the labor\nand employers’ sectors to be designated by the President at regular intervals. For this purpose,\na sectoral nomination, selection, and recall process shall be established by the DOLE in\nconsultation with the sectors observing the ‘most representative’ organization criteria of ILO\nConvention No. 144.",
      "Tripartite Industrial Peace Councils (TIPCs) at the regional or industry level shall also be\nestablished with representatives from government, workers and employers to serve as a\ncontinuing forum for tripartite advisement and consultation in aid of streamlining the role of\ngovernment, empowering workers’ and employers’ organizations, enhancing their respective\nrights, attaining industrial peace, and improving productivity.",
      "The TIPCs shall have the following functions:",
      "(1) Monitor the full implementation and compliance of concerned sectors with the\nprovisions of all tripartite instruments, including international conventions and declarations,\ncodes of conduct, and social accords;",
      "(2) Participate in national, regional or industry-specific tripartite conferences which the\nPresident or the Secretary of Labor and Employment may call from time to time;",
      "(3) Review existing labor, economic and social policies and evaluate local and\ninternational developments affecting them;",
      "(4) Formulate, for submission to the President or to Congress, tripartite views,\nrecommendations and proposals on labor, economic, and social concerns, including the\npresentation of tripartite positions on relevant bills pending in Congress;",
      "(5) Advise the Secretary of Labor and Employment in the formulation or implementation\nof policies and legislation affecting labor and employment;",
      "(6) Serve as a communication channel and a mechanism for undertaking joint programs\namong government, workers, employers and their organizations toward enhancing labor-\nmanagement relations; and",
      "(7) Adopt its own program of activities and rules, consistent with development objectives.",
      "All TIPCs shall be an integral part of the organizational structure of the NTIPC.",
      "The operations of all TIPCs shall be funded from the regular budget of the DOLE."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IX - SPECIAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "275"
  },
  {
    "article": "Art. 291",
    "title": "Government Employees",
    "category": "Labor Law - Book 5",
    "simplified_text": "The terms and conditions of employment of\nall government employees, including employees of government-owned and controlled\ncorporations, shall be governed by the Civil Service Law, rules and regulations. Their salaries\nshall be standardized by the National Assembly as provided for in the New Constitution.\nHowever, there shall be no reduction of existing wages, benefits and other terms and\nconditions of employment being enjoyed by them at the time of the adoption of this Code.",
    "chunks": [
      "The terms and conditions of employment of\nall government employees, including employees of government-owned and controlled\ncorporations, shall be governed by the Civil Service Law, rules and regulations. Their salaries\nshall be standardized by the National Assembly as provided for in the New Constitution.\nHowever, there shall be no reduction of existing wages, benefits and other terms and\nconditions of employment being enjoyed by them at the time of the adoption of this Code."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IX - SPECIAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "276"
  },
  {
    "article": "Art. 292",
    "title": "Miscellaneous Provisions",
    "category": "Labor Law - Book 5",
    "simplified_text": "(a) All unions are authorized to collect\nreasonable membership fees, union dues, assessments and fines and other contributions for\nlabor education and research, mutual death and hospitalization benefits, welfare fund, strike\nfund and credit and cooperative undertakings.\n\n(b) Subject to the constitutional right of workers to security of tenure and their right to\nbe protected against dismissal except for a just and authorized cause and without prejudice to\nthe requirement of notice under Article 283 of this Code, the employer shall furnish the\nworker whose employment is sought to be terminated a written notice containing a statement\nof the causes for termination and shall afford the latter ample opportunity to be heard and to\ndefend himself with the assistance of his representative if he so desires in accordance with\ncompany rules and regulations promulgated pursuant to guidelines set by the Department of\nLabor and Employment. Any decision taken by the employer shall be without prejudice to the\nright of the worker to contest the validity or legality of his dismissal by filing a complaint with\nthe regional branch of the National Labor Relations Commission. The burden of proving that\nthe termination was for a valid or authorized cause shall rest on the employer. The Secretary\nof the Department of Labor and Employment may suspend the effects of the termination\npending resolution of the dispute in the event of a prima facie finding by the appropriate\nofficial of the Department of Labor and Employment before whom such dispute is pending\nthat the termination may cause a serious labor dispute or is in implementation of a mass lay-\noff.\n\n(c) Any employee, whether employed for a definite period or not, shall, beginning on his\nfirst day of service, be considered as an employee for purposes of membership in any labor\nunion.\n\n(d) No docket fee shall be assessed in labor standards disputes. In all other disputes,\ndocket fees may be assessed against the filing party, provided that in bargaining deadlock,\nsuch fees shall be shared equally by the negotiating parties.\n\n(e) The Minister of Labor and Employment and the Minister of the Budget shall cause to\nbe created or reclassified in accordance with law such positions as may be necessary to carry\nout the objectives of this Code and cause the upgrading of the salaries of the personnel\ninvolved in the Labor Relations System of the Ministry. Funds needed for this purpose shall be\nprovided out of the Special Activities Fund appropriated by Batas Pambansa Blg. 80 and from\nannual appropriations thereafter.\n\n(f) A special Voluntary Arbitration Fund is hereby established in the Board to subsidize the\ncost of voluntary arbitration in cases involving the interpretation and implementation of the\nCollective Bargaining Agreement, including the Arbitrator’s fees, and for such other related\npurposes to promote and develop voluntary arbitration. The Board shall administer the Special\nVoluntary Arbitration Fund in accordance with the guidelines it may adopt upon the\nrecommendation of the Council, which guidelines shall be subject to the approval of the\nSecretary of Labor and Employment. Continuing funds needed for this purpose in the initial\nyearly amount of fifteen million pesos (P15,000,000.00) shall be provided in the 1989 annual\ngeneral appropriations acts.\n\nThe amount of subsidy in appropriate cases shall be determined by the Board in\naccordance with established guidelines issued by it upon the recommendation of the Council.\n\nThe Fund shall also be utilized for the operation of the Council, the training and education\nof Voluntary Arbitrators, and the promotion and development of a comprehensive Voluntary\nArbitration Program.\n\n(g) The Ministry shall help promote and gradually develop, with the agreement of labor\norganizations and employers, labor-management cooperation programs at appropriate levels\nof the enterprise based on shared responsibility and mutual respect in order to ensure\nindustrial peace and improvement in productivity, working conditions and the quality of\nworking life.\n\n(h) In establishments where no legitimate labor organization exists, labor-management\ncommittees may be formed voluntarily by workers and employers for the purpose of\npromoting industrial peace. The Department of Labor and Employment shall endeavor to\nenlighten and educate the workers and employers on their rights and responsibilities through\nlabor education with emphasis on the policy thrusts of this Code.\n\n(i) To ensure speedy labor justice, the periods provided in this Code within which decisions\nor resolutions of labor relations cases or matters should be rendered shall be mandatory. For\nthis purpose, a case or matter shall be deemed submitted for decision or resolution upon the\nfiling of the last pleading or memorandum required by the rules of the Commission or by the\nCommission itself, or the Labor Arbiter, or the Director of the Bureau of Labor Relations or\nMed-Arbiter, or the Regional Director.\n\nUpon expiration of the corresponding period, a certification stating why a decision or\nresolution has not been rendered within the said period shall be issued forthwith by the\n\nChairman of the Commission, the Executive Labor Arbiter, or the Director of the Bureau of\nLabor Relations or Med-Arbiter, or the Regional Director, as the case may be, and a copy\nthereof served upon the parties.\n\nDespite the expiration of the applicable mandatory period, the aforesaid officials shall,\nwithout prejudice to any liability which may have been incurred as a consequence thereof, see\nto it that the case or matter shall be decided or resolved without any further delay.",
    "chunks": [
      "(a) All unions are authorized to collect\nreasonable membership fees, union dues, assessments and fines and other contributions for\nlabor education and research, mutual death and hospitalization benefits, welfare fund, strike\nfund and credit and cooperative undertakings.",
      "(b) Subject to the constitutional right of workers to security of tenure and their right to\nbe protected against dismissal except for a just and authorized cause and without prejudice to\nthe requirement of notice under Article 283 of this Code, the employer shall furnish the\nworker whose employment is sought to be terminated a written notice containing a statement\nof the causes for termination and shall afford the latter ample opportunity to be heard and to\ndefend himself with the assistance of his representative if he so desires in accordance with\ncompany rules and regulations promulgated pursuant to guidelines set by the Department of\nLabor and Employment. Any decision taken by the employer shall be without prejudice to the\nright of the worker to contest the validity or legality of his dismissal by filing a complaint with\nthe regional branch of the National Labor Relations Commission. The burden of proving that\nthe termination was for a valid or authorized cause shall rest on the employer. The Secretary\nof the Department of Labor and Employment may suspend the effects of the termination\npending resolution of the dispute in the event of a prima facie finding by the appropriate\nofficial of the Department of Labor and Employment before whom such dispute is pending\nthat the termination may cause a serious labor dispute or is in implementation of a mass lay-\noff.",
      "(c) Any employee, whether employed for a definite period or not, shall, beginning on his\nfirst day of service, be considered as an employee for purposes of membership in any labor\nunion.",
      "(d) No docket fee shall be assessed in labor standards disputes. In all other disputes,\ndocket fees may be assessed against the filing party, provided that in bargaining deadlock,\nsuch fees shall be shared equally by the negotiating parties.",
      "(e) The Minister of Labor and Employment and the Minister of the Budget shall cause to\nbe created or reclassified in accordance with law such positions as may be necessary to carry\nout the objectives of this Code and cause the upgrading of the salaries of the personnel\ninvolved in the Labor Relations System of the Ministry. Funds needed for this purpose shall be\nprovided out of the Special Activities Fund appropriated by Batas Pambansa Blg. 80 and from\nannual appropriations thereafter.",
      "(f) A special Voluntary Arbitration Fund is hereby established in the Board to subsidize the\ncost of voluntary arbitration in cases involving the interpretation and implementation of the\nCollective Bargaining Agreement, including the Arbitrator’s fees, and for such other related\npurposes to promote and develop voluntary arbitration. The Board shall administer the Special\nVoluntary Arbitration Fund in accordance with the guidelines it may adopt upon the\nrecommendation of the Council, which guidelines shall be subject to the approval of the\nSecretary of Labor and Employment. Continuing funds needed for this purpose in the initial\nyearly amount of fifteen million pesos (P15,000,000.00) shall be provided in the 1989 annual\ngeneral appropriations acts.",
      "The amount of subsidy in appropriate cases shall be determined by the Board in\naccordance with established guidelines issued by it upon the recommendation of the Council.",
      "The Fund shall also be utilized for the operation of the Council, the training and education\nof Voluntary Arbitrators, and the promotion and development of a comprehensive Voluntary\nArbitration Program.",
      "(g) The Ministry shall help promote and gradually develop, with the agreement of labor\norganizations and employers, labor-management cooperation programs at appropriate levels\nof the enterprise based on shared responsibility and mutual respect in order to ensure\nindustrial peace and improvement in productivity, working conditions and the quality of\nworking life.",
      "(h) In establishments where no legitimate labor organization exists, labor-management\ncommittees may be formed voluntarily by workers and employers for the purpose of\npromoting industrial peace. The Department of Labor and Employment shall endeavor to\nenlighten and educate the workers and employers on their rights and responsibilities through\nlabor education with emphasis on the policy thrusts of this Code.",
      "(i) To ensure speedy labor justice, the periods provided in this Code within which decisions\nor resolutions of labor relations cases or matters should be rendered shall be mandatory. For\nthis purpose, a case or matter shall be deemed submitted for decision or resolution upon the\nfiling of the last pleading or memorandum required by the rules of the Commission or by the\nCommission itself, or the Labor Arbiter, or the Director of the Bureau of Labor Relations or\nMed-Arbiter, or the Regional Director.",
      "Upon expiration of the corresponding period, a certification stating why a decision or\nresolution has not been rendered within the said period shall be issued forthwith by the",
      "Chairman of the Commission, the Executive Labor Arbiter, or the Director of the Bureau of\nLabor Relations or Med-Arbiter, or the Regional Director, as the case may be, and a copy\nthereof served upon the parties.",
      "Despite the expiration of the applicable mandatory period, the aforesaid officials shall,\nwithout prejudice to any liability which may have been incurred as a consequence thereof, see\nto it that the case or matter shall be decided or resolved without any further delay."
    ],
    "tags": [
      "Book Five - LABOR RELATIONS",
      "Title IX - SPECIAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "277"
  },
  {
    "article": "Art. 293",
    "title": "Coverage",
    "category": "Labor Law - Book 6",
    "simplified_text": "The provisions of this Title shall apply to all establishments\nor undertakings, whether for profit or not.",
    "chunks": [
      "The provisions of this Title shall apply to all establishments\nor undertakings, whether for profit or not."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "278"
  },
  {
    "article": "Art. 294",
    "title": "Security of Tenure",
    "category": "Labor Law - Book 6",
    "simplified_text": "In cases of regular employment, the employer\nshall not terminate the services of an employee except for a just cause or when authorized by\nthis Title. An employee who is unjustly dismissed from work shall be entitled to reinstatement\nwithout loss of seniority rights and other privileges and to his full backwages, inclusive of\nallowances, and to his other benefits or their monetary equivalent computed from the time\nhis compensation was withheld from him up to the time of his actual reinstatement.",
    "chunks": [
      "In cases of regular employment, the employer\nshall not terminate the services of an employee except for a just cause or when authorized by\nthis Title. An employee who is unjustly dismissed from work shall be entitled to reinstatement\nwithout loss of seniority rights and other privileges and to his full backwages, inclusive of\nallowances, and to his other benefits or their monetary equivalent computed from the time\nhis compensation was withheld from him up to the time of his actual reinstatement."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "279"
  },
  {
    "article": "Art. 295",
    "title": "Regular and Casual Employment",
    "category": "Labor Law - Book 6",
    "simplified_text": "The provisions of written agreement\nto the contrary notwithstanding and regardless of the oral agreement of the parties, an\nemployment shall be deemed to be regular where the employee has been engaged to perform\nactivities which are usually necessary or desirable in the usual business or trade of the\nemployer, except where the employment has been fixed for a specific project or undertaking\nthe completion or termination of which has been determined at the time of the engagement\nof the employee or where the work or service to be performed is seasonal in nature and the\nemployment is for the duration of the season.\n\nAn employment shall be deemed to be casual if it is not covered by the preceding\nparagraph: Provided, That any employee who has rendered at least one year of service,\nwhether such service is continuous or broken, shall be considered a regular employee with\nrespect to the activity in which he is employed and his employment shall continue while such\nactivity exists.",
    "chunks": [
      "The provisions of written agreement\nto the contrary notwithstanding and regardless of the oral agreement of the parties, an\nemployment shall be deemed to be regular where the employee has been engaged to perform\nactivities which are usually necessary or desirable in the usual business or trade of the\nemployer, except where the employment has been fixed for a specific project or undertaking\nthe completion or termination of which has been determined at the time of the engagement\nof the employee or where the work or service to be performed is seasonal in nature and the\nemployment is for the duration of the season.",
      "An employment shall be deemed to be casual if it is not covered by the preceding\nparagraph: Provided, That any employee who has rendered at least one year of service,\nwhether such service is continuous or broken, shall be considered a regular employee with\nrespect to the activity in which he is employed and his employment shall continue while such\nactivity exists."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "280"
  },
  {
    "article": "Art. 296",
    "title": "Probationary Employment",
    "category": "Labor Law - Book 6",
    "simplified_text": "Probationary employment shall not exceed\nsix (6) months from the date the employee started working, unless it is covered by an\napprenticeship agreement stipulating a longer period. The services of an employee who has\nbeen engaged on a probationary basis may be terminated for a just cause or when he fails to\nqualify as a regular employee in accordance with reasonable standards made known by the\nemployer to the employee at the time of his engagement. An employee who is allowed to\nwork after a probationary period shall be considered a regular employee.",
    "chunks": [
      "Probationary employment shall not exceed\nsix (6) months from the date the employee started working, unless it is covered by an\napprenticeship agreement stipulating a longer period. The services of an employee who has\nbeen engaged on a probationary basis may be terminated for a just cause or when he fails to\nqualify as a regular employee in accordance with reasonable standards made known by the\nemployer to the employee at the time of his engagement. An employee who is allowed to\nwork after a probationary period shall be considered a regular employee."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "281"
  },
  {
    "article": "Art. 297",
    "title": "Termination by Employer",
    "category": "Labor Law - Book 6",
    "simplified_text": "An employer may terminate an\nemployment for any of the following causes:\n\n(a) Serious misconduct or willful disobedience by the employee of the lawful orders of his\nemployer or representative in connection with his work;\n\n(b) Gross and habitual neglect by the employee of his duties;\n\n(c) Fraud or willful breach by the employee of the trust reposed in him by his employer or\nduly authorized representative;\n\n(d) Commission of a crime or offense by the employee against the person of his employer\nor any immediate member of his family or his duly authorized representatives; and\n\n(e) Other causes analogous to the foregoing.",
    "chunks": [
      "An employer may terminate an\nemployment for any of the following causes:",
      "(a) Serious misconduct or willful disobedience by the employee of the lawful orders of his\nemployer or representative in connection with his work;",
      "(b) Gross and habitual neglect by the employee of his duties;",
      "(c) Fraud or willful breach by the employee of the trust reposed in him by his employer or\nduly authorized representative;",
      "(d) Commission of a crime or offense by the employee against the person of his employer\nor any immediate member of his family or his duly authorized representatives; and",
      "(e) Other causes analogous to the foregoing."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "282"
  },
  {
    "article": "Art. 298",
    "title": "Closure of Establishment and Reduction of Personnel",
    "category": "Labor Law - Book 6",
    "simplified_text": "The employer\nmay also terminate the employment of any employee due to the installation of labor-saving\ndevices, redundancy, retrenchment to prevent losses or the closing or cessation of operation\nof the establishment or undertaking unless the closing is for the purpose of circumventing the\nprovisions of this Title, by serving a written notice on the workers and the Ministry of Labor\nand Employment at least one (1) month before the intended date thereof. In case of\ntermination due to the installation of labor-saving devices or redundancy, the worker affected\nthereby shall be entitled to a separation pay equivalent to at least his one (1) month pay or to\nat least one (1) month pay for every year of service, whichever is higher. In case of\nretrenchment to prevent losses and in cases of closures or cessation of operations of\nestablishment or undertaking not due to serious business losses or financial reverses, the\nseparation pay shall be equivalent to one (1) month pay or at least one-half (1/2) month pay\nfor every year of service, whichever is higher. A fraction of at least six (6) months shall be\nconsidered one (1) whole year.",
    "chunks": [
      "The employer\nmay also terminate the employment of any employee due to the installation of labor-saving\ndevices, redundancy, retrenchment to prevent losses or the closing or cessation of operation\nof the establishment or undertaking unless the closing is for the purpose of circumventing the\nprovisions of this Title, by serving a written notice on the workers and the Ministry of Labor\nand Employment at least one (1) month before the intended date thereof. In case of\ntermination due to the installation of labor-saving devices or redundancy, the worker affected\nthereby shall be entitled to a separation pay equivalent to at least his one (1) month pay or to\nat least one (1) month pay for every year of service, whichever is higher. In case of\nretrenchment to prevent losses and in cases of closures or cessation of operations of\nestablishment or undertaking not due to serious business losses or financial reverses, the\nseparation pay shall be equivalent to one (1) month pay or at least one-half (1/2) month pay\nfor every year of service, whichever is higher. A fraction of at least six (6) months shall be\nconsidered one (1) whole year."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "283"
  },
  {
    "article": "Art. 299",
    "title": "Disease as Ground for Termination",
    "category": "Labor Law - Book 6",
    "simplified_text": "An employer may terminate the\nservices of an employee who has been found to be suffering from any disease and whose\ncontinued employment is prohibited by law or is prejudicial to his health as well as to the\nhealth of his co-employees: Provided, That he is paid separation pay equivalent to at least one\n(1) month salary or to one-half (1/2) month salary for every year of service, whichever is\ngreater, a fraction of at least six (6) months being considered as one (1) whole year.",
    "chunks": [
      "An employer may terminate the\nservices of an employee who has been found to be suffering from any disease and whose\ncontinued employment is prohibited by law or is prejudicial to his health as well as to the\nhealth of his co-employees: Provided, That he is paid separation pay equivalent to at least one\n(1) month salary or to one-half (1/2) month salary for every year of service, whichever is\ngreater, a fraction of at least six (6) months being considered as one (1) whole year."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "284"
  },
  {
    "article": "Art. 300",
    "title": "Termination by Employee",
    "category": "Labor Law - Book 6",
    "simplified_text": "(a) An employee may terminate without just\ncause the employee-employer relationship by serving a written notice on the employer at least\none (1) month in advance. The employer upon whom no such notice was served may hold the\nemployee liable for damages.\n\n(b) An employee may put an end to the relationship without serving any notice on the\nemployer for any of the following just causes:\n\n1. Serious insult by the employer or his representative on the honor and person of the\nemployee;\n\n2. Inhuman and unbearable treatment accorded the employee by the employer or his\nrepresentative;\n\n3. Commission of a crime or offense by the employer or his representative against the\nperson of the employee or any of the immediate members of his family; and\n\n4. Other causes analogous to any of the foregoing.",
    "chunks": [
      "(a) An employee may terminate without just\ncause the employee-employer relationship by serving a written notice on the employer at least\none (1) month in advance. The employer upon whom no such notice was served may hold the\nemployee liable for damages.",
      "(b) An employee may put an end to the relationship without serving any notice on the\nemployer for any of the following just causes:",
      "1. Serious insult by the employer or his representative on the honor and person of the\nemployee;",
      "2. Inhuman and unbearable treatment accorded the employee by the employer or his\nrepresentative;",
      "3. Commission of a crime or offense by the employer or his representative against the\nperson of the employee or any of the immediate members of his family; and",
      "4. Other causes analogous to any of the foregoing."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "285"
  },
  {
    "article": "Art. 301",
    "title": "When Employment not Deemed Terminated",
    "category": "Labor Law - Book 6",
    "simplified_text": "The bona fide suspension\nof the operation of a business or undertaking for a period not exceeding six (6) months, or the\nfulfillment by the employee of a military or civic duty shall not terminate employment. In all\nsuch cases, the employer shall reinstate the employee to his former position without loss of\nseniority rights if he indicates his desire to resume his work not later than one (1) month from\nthe resumption of operations of his employer or from his relief from the military or civic\nduty.",
    "chunks": [
      "The bona fide suspension\nof the operation of a business or undertaking for a period not exceeding six (6) months, or the\nfulfillment by the employee of a military or civic duty shall not terminate employment. In all\nsuch cases, the employer shall reinstate the employee to his former position without loss of\nseniority rights if he indicates his desire to resume his work not later than one (1) month from\nthe resumption of operations of his employer or from his relief from the military or civic\nduty."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title I - TERMINATION OF EMPLOYMENT"
    ],
    "language": "en",
    "old_article_number": "286"
  },
  {
    "article": "Art. 302",
    "title": "Retirement",
    "category": "Labor Law - Book 6",
    "simplified_text": "Any employee may be retired upon reaching the\nretirement age established in the collective bargaining agreement or other applicable\nemployment contract.\n\nIn case of retirement, the employee shall be entitled to receive such retirement benefits\nas he may have earned under existing laws and any collective bargaining agreement and other\nagreements: Provided, however, That an employee’s retirement benefits under any collective\nbargaining and other agreements shall not be less than those provided therein.\n\nIn the absence of a retirement plan or agreement providing for retirement benefits of\nemployees in the establishment, an employee upon reaching the age of sixty (60) years or\nmore, but not beyond sixty-five (65) years which is hereby declared the compulsory retirement\nage, who has served at least five (5) years in the said establishment, may retire and shall be\nentitled to retirement pay equivalent to at least one-half (1/2) month salary for every year of\nservice, a fraction of at least six (6) months being considered as one whole year.\n\nUnless the parties provide for broader inclusions, the term one-half (1/2) month salary\nshall mean fifteen (15) days plus one-twelfth (1/12) of the 13th month pay and the cash\nequivalent of not more than five (5) days of service incentive leaves.\n\nAn underground mining employee upon reaching the age of fifty (50) years or more, but\nnot beyond sixty (60) years which is hereby declared the compulsory retirement age for\nunderground mine workers, who has served at least five (5) years as underground mine\nworker, may retire and shall be entitled to all the retirement benefits provided for in this\nArticle.\n\nRetail, service and agricultural establishments or operations employing not more than ten\n(10) employees or workers are exempted from the coverage of this provision.\n\nViolation of this provision is hereby declared unlawful and subject to the penal\nprovisions under Article 288 of this Code.\n\nNothing in this Article shall deprive any employee of benefits to which he may be\nentitled under existing laws or company policies or practices.",
    "chunks": [
      "Any employee may be retired upon reaching the\nretirement age established in the collective bargaining agreement or other applicable\nemployment contract.",
      "In case of retirement, the employee shall be entitled to receive such retirement benefits\nas he may have earned under existing laws and any collective bargaining agreement and other\nagreements: Provided, however, That an employee’s retirement benefits under any collective\nbargaining and other agreements shall not be less than those provided therein.",
      "In the absence of a retirement plan or agreement providing for retirement benefits of\nemployees in the establishment, an employee upon reaching the age of sixty (60) years or\nmore, but not beyond sixty-five (65) years which is hereby declared the compulsory retirement\nage, who has served at least five (5) years in the said establishment, may retire and shall be\nentitled to retirement pay equivalent to at least one-half (1/2) month salary for every year of\nservice, a fraction of at least six (6) months being considered as one whole year.",
      "Unless the parties provide for broader inclusions, the term one-half (1/2) month salary\nshall mean fifteen (15) days plus one-twelfth (1/12) of the 13th month pay and the cash\nequivalent of not more than five (5) days of service incentive leaves.",
      "An underground mining employee upon reaching the age of fifty (50) years or more, but\nnot beyond sixty (60) years which is hereby declared the compulsory retirement age for\nunderground mine workers, who has served at least five (5) years as underground mine\nworker, may retire and shall be entitled to all the retirement benefits provided for in this\nArticle.",
      "Retail, service and agricultural establishments or operations employing not more than ten\n(10) employees or workers are exempted from the coverage of this provision.",
      "Violation of this provision is hereby declared unlawful and subject to the penal\nprovisions under Article 288 of this Code.",
      "Nothing in this Article shall deprive any employee of benefits to which he may be\nentitled under existing laws or company policies or practices."
    ],
    "tags": [
      "Book Six - POST-EMPLOYMENT",
      "Title II - RETIREMENT FROM THE SERVICE"
    ],
    "language": "en",
    "old_article_number": "287"
  },
  {
    "article": "Art. 303",
    "title": "Penalties",
    "category": "Labor Law - Book 7",
    "simplified_text": "Except as otherwise provided in this Code, or unless the\nacts complained of hinge on a question of interpretation or implementation of ambiguous\nprovisions of an existing collective bargaining agreement, any violation of the provisions of\nthis Code declared to be unlawful or penal in nature shall be punished with a fine of not less\nthan One Thousand Pesos (P1,000.00) nor more than Ten Thousand Pesos (P10,000.00), or\nimprisonment of not less than three months nor more than three years, or both such fine and\nimprisonment at the discretion of the court.\n\nIn addition to such penalty, any alien found guilty shall be summarily deported upon\ncompletion of service of sentence.\n\nAny provision of law to the contrary notwithstanding, any criminal offense punished in\nthis Code shall be under the concurrent jurisdiction of the Municipal or City Courts and the\nCourts of First Instance.",
    "chunks": [
      "Except as otherwise provided in this Code, or unless the\nacts complained of hinge on a question of interpretation or implementation of ambiguous\nprovisions of an existing collective bargaining agreement, any violation of the provisions of\nthis Code declared to be unlawful or penal in nature shall be punished with a fine of not less\nthan One Thousand Pesos (P1,000.00) nor more than Ten Thousand Pesos (P10,000.00), or\nimprisonment of not less than three months nor more than three years, or both such fine and\nimprisonment at the discretion of the court.",
      "In addition to such penalty, any alien found guilty shall be summarily deported upon\ncompletion of service of sentence.",
      "Any provision of law to the contrary notwithstanding, any criminal offense punished in\nthis Code shall be under the concurrent jurisdiction of the Municipal or City Courts and the\nCourts of First Instance."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title I - PENAL PROVISIONS AND LIABILITIES"
    ],
    "language": "en",
    "old_article_number": "288"
  },
  {
    "article": "Art. 304",
    "title": "Who are Liable When Committed by Other Than Natural Person",
    "category": "Labor Law - Book 7",
    "simplified_text": "If the\noffense is committed by a corporation, trust, firm, partnership, association or any other entity,\nthe penalty shall be imposed upon the guilty officer or officers of such corporation, trust, firm,\npartnership, association or entity.",
    "chunks": [
      "If the\noffense is committed by a corporation, trust, firm, partnership, association or any other entity,\nthe penalty shall be imposed upon the guilty officer or officers of such corporation, trust, firm,\npartnership, association or entity."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title I - PENAL PROVISIONS AND LIABILITIES"
    ],
    "language": "en",
    "old_article_number": "289"
  },
  {
    "article": "Art. 305",
    "title": "Offenses",
    "category": "Labor Law - Book 7",
    "simplified_text": "Offenses penalized under this Code and the rules and\nregulations issued pursuant thereto shall prescribe in three (3) years.\n\nAll unfair labor practice arising from Book V shall be filed with the appropriate agency\nwithin one (1) year from accrual of such unfair labor practice; otherwise, they shall be forever\nbarred.",
    "chunks": [
      "Offenses penalized under this Code and the rules and\nregulations issued pursuant thereto shall prescribe in three (3) years.",
      "All unfair labor practice arising from Book V shall be filed with the appropriate agency\nwithin one (1) year from accrual of such unfair labor practice; otherwise, they shall be forever\nbarred."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title II - PRESCRIPTION OF OFFENSES AND CLAIMS"
    ],
    "language": "en",
    "old_article_number": "290"
  },
  {
    "article": "Art. 306",
    "title": "Money Claims",
    "category": "Labor Law - Book 7",
    "simplified_text": "All money claims arising from employer-employee\nrelations accruing during the effectivity of this Code shall be filed within three (3) years from\nthe time the cause of action accrued; otherwise they shall be forever barred.\n\nAll money claims accruing prior to the effectivity of this Code shall be filed with the\nappropriate entities established under this Code within one (1) year from the date of\neffectivity, and shall be processed or determined in accordance with the implementing rules\nand regulations of the Code; otherwise, they shall be forever barred.\n\nWorkmen’s compensation claims accruing prior to the effectivity of this Code and during\nthe period from November 1, 1974 up to December 31, 1974, shall be filed with the\nappropriate regional offices of the Department of Labor not later than March 31, 1975;\notherwise, they shall forever be barred. The claims shall be processed and adjudicated in\naccordance with the law and rules at the time their causes of action accrued.",
    "chunks": [
      "All money claims arising from employer-employee\nrelations accruing during the effectivity of this Code shall be filed within three (3) years from\nthe time the cause of action accrued; otherwise they shall be forever barred.",
      "All money claims accruing prior to the effectivity of this Code shall be filed with the\nappropriate entities established under this Code within one (1) year from the date of\neffectivity, and shall be processed or determined in accordance with the implementing rules\nand regulations of the Code; otherwise, they shall be forever barred.",
      "Workmen’s compensation claims accruing prior to the effectivity of this Code and during\nthe period from November 1, 1974 up to December 31, 1974, shall be filed with the\nappropriate regional offices of the Department of Labor not later than March 31, 1975;\notherwise, they shall forever be barred. The claims shall be processed and adjudicated in\naccordance with the law and rules at the time their causes of action accrued."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title II - PRESCRIPTION OF OFFENSES AND CLAIMS"
    ],
    "language": "en",
    "old_article_number": "291"
  },
  {
    "article": "Art. 307",
    "title": "Institution of Money Claims",
    "category": "Labor Law - Book 7",
    "simplified_text": "Money claims specified in the immediately\npreceding Article shall be filed before the appropriate entity independently of the criminal\naction that may be instituted in the proper courts.\n\nPending the final determination of the merits of money claims filed with the appropriate\nentity, no civil action arising from the same cause of action shall be filed with any court. This\nprovision shall not apply to employees compensation cases which shall be processed and\ndetermined strictly in accordance with the pertinent provisions of this Code.",
    "chunks": [
      "Money claims specified in the immediately\npreceding Article shall be filed before the appropriate entity independently of the criminal\naction that may be instituted in the proper courts.",
      "Pending the final determination of the merits of money claims filed with the appropriate\nentity, no civil action arising from the same cause of action shall be filed with any court. This\nprovision shall not apply to employees compensation cases which shall be processed and\ndetermined strictly in accordance with the pertinent provisions of this Code."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title II - PRESCRIPTION OF OFFENSES AND CLAIMS"
    ],
    "language": "en",
    "old_article_number": "292"
  },
  {
    "article": "Art. 308",
    "title": "Application of Law Enacted Prior to this Code",
    "category": "Labor Law - Book 7",
    "simplified_text": "All actions or claims\naccruing prior to the effectivity of this Code shall be determined in accordance with the laws\nin force at the time of their accrual.",
    "chunks": [
      "All actions or claims\naccruing prior to the effectivity of this Code shall be determined in accordance with the laws\nin force at the time of their accrual."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "293"
  },
  {
    "article": "Art. 309",
    "title": "Secretary of Labor to Initiate Integration of Maternity Leave Benefits",
    "category": "Labor Law - Book 7",
    "simplified_text": "Within six (6) months after this Code takes effect, the Secretary of Labor shall initiate such\nmeasures as may be necessary for the integration of maternity leave benefits into the Social\nSecurity System, in the case of private employment, and the Government Service Insurance\nSystem, in the case of public employment.",
    "chunks": [
      "Within six (6) months after this Code takes effect, the Secretary of Labor shall initiate such\nmeasures as may be necessary for the integration of maternity leave benefits into the Social\nSecurity System, in the case of private employment, and the Government Service Insurance\nSystem, in the case of public employment."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "294"
  },
  {
    "article": "Art. 310",
    "title": "Untitled (see content)",
    "category": "Labor Law - Book 7",
    "simplified_text": "Funding of the Overseas Employment Development Board and National\nSeamen's Board referred to in Articles 17 and 20, respectively, of this Code shall initially be\nfunded out of the unprogrammed fund of the Department of Labor and the National\nManpower and Youth Council.",
    "chunks": [
      "Funding of the Overseas Employment Development Board and National\nSeamen's Board referred to in Articles 17 and 20, respectively, of this Code shall initially be\nfunded out of the unprogrammed fund of the Department of Labor and the National\nManpower and Youth Council."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "295"
  },
  {
    "article": "Art. 311",
    "title": "Termination of the Workmen's Compensation Program",
    "category": "Labor Law - Book 7",
    "simplified_text": "The Bureau of\nWorkmen’s Compensation, Workmen’s Compensation Commission, and Workmen’s\nCompensation Units in the regional offices of the Department of Labor shall continue to\nexercise the functions and the respective jurisdictions over workmen’s compensation cases\nvested upon them by Act No. 3428, as amended, otherwise known as the Workmen’s\nCompensation Act until March 31, 1976. Likewise, the term of office of incumbent members\nof the Workmen’s Compensation Commission, including its Chairman and any commissioner\ndeemed retired as of December 31, 1975, as well as the present employees and officials of the\n\nBureau of Workmen’s Compensation, Workmen’s Compensation Commission and the\nWorkmen’s Compensation Units shall continue up to that date. Thereafter, said offices shall\nbe considered abolished and all officials and personnel thereof shall be transferred to and\nmandatorily absorbed by the Department of Labor, subject to Presidential Decree No. 6,\nLetters of Instructions Nos. 14 and 14-A and the Civil Service Law and rules.\n\nSuch amount as may be necessary to cover the operational expenses of the Bureau of\nWorkmen’s Compensation and the Workmen’s Compensation Units, including the salaries of\nincumbent personnel for the period up to March 31, 1976 shall be appropriated from the\nunprogrammed funds of the Department of Labor.",
    "chunks": [
      "The Bureau of\nWorkmen’s Compensation, Workmen’s Compensation Commission, and Workmen’s\nCompensation Units in the regional offices of the Department of Labor shall continue to\nexercise the functions and the respective jurisdictions over workmen’s compensation cases\nvested upon them by Act No. 3428, as amended, otherwise known as the Workmen’s\nCompensation Act until March 31, 1976. Likewise, the term of office of incumbent members\nof the Workmen’s Compensation Commission, including its Chairman and any commissioner\ndeemed retired as of December 31, 1975, as well as the present employees and officials of the",
      "Bureau of Workmen’s Compensation, Workmen’s Compensation Commission and the\nWorkmen’s Compensation Units shall continue up to that date. Thereafter, said offices shall\nbe considered abolished and all officials and personnel thereof shall be transferred to and\nmandatorily absorbed by the Department of Labor, subject to Presidential Decree No. 6,\nLetters of Instructions Nos. 14 and 14-A and the Civil Service Law and rules.",
      "Such amount as may be necessary to cover the operational expenses of the Bureau of\nWorkmen’s Compensation and the Workmen’s Compensation Units, including the salaries of\nincumbent personnel for the period up to March 31, 1976 shall be appropriated from the\nunprogrammed funds of the Department of Labor."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "296"
  },
  {
    "article": "Art. 312",
    "title": "Continuation of Insurance Policies and Indemnity Bonds",
    "category": "Labor Law - Book 7",
    "simplified_text": "All workmen’s\ncompensation insurance policies and indemnity bonds for self-insured employers existing\nupon the effectivity of this Code shall remain in force and effect until the expiration dates of\nsuch policies or the lapse of the period of such bonds, as the case may be, but in no case\nbeyond December 31, 1974. Claims may be filed against the insurance carriers and/or self-\ninsured employers for causes of action which accrued during the existence of said policies or\nauthority to self-insure.",
    "chunks": [
      "All workmen’s\ncompensation insurance policies and indemnity bonds for self-insured employers existing\nupon the effectivity of this Code shall remain in force and effect until the expiration dates of\nsuch policies or the lapse of the period of such bonds, as the case may be, but in no case\nbeyond December 31, 1974. Claims may be filed against the insurance carriers and/or self-\ninsured employers for causes of action which accrued during the existence of said policies or\nauthority to self-insure."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "297"
  },
  {
    "article": "Art. 313",
    "title": "Abolition of the Court of Industrial Relations and the National Labor Relations Commission",
    "category": "Labor Law - Book 7",
    "simplified_text": "The Court of Industrial Relations and the National Labor Relations\nCommission established under Presidential Decree No. 21 are hereby abolished. All\nunexpended funds, properties, equipment and records of the Court of Industrial Relations, and\nsuch of its personnel as may be necessary, are hereby transferred to the Commission and to\nits regional branches. All unexpended funds, properties and equipment of the National Labor\nRelations Commission established under Presidential Decree No. 21 are transferred to the\nBureau of Labor Relations. Personnel not absorbed by or transferred to the Commission shall\nenjoy benefits granted under existing laws.",
    "chunks": [
      "The Court of Industrial Relations and the National Labor Relations\nCommission established under Presidential Decree No. 21 are hereby abolished. All\nunexpended funds, properties, equipment and records of the Court of Industrial Relations, and\nsuch of its personnel as may be necessary, are hereby transferred to the Commission and to\nits regional branches. All unexpended funds, properties and equipment of the National Labor\nRelations Commission established under Presidential Decree No. 21 are transferred to the\nBureau of Labor Relations. Personnel not absorbed by or transferred to the Commission shall\nenjoy benefits granted under existing laws."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "298"
  },
  {
    "article": "Art. 314",
    "title": "Disposition of Pending Cases",
    "category": "Labor Law - Book 7",
    "simplified_text": "All cases pending before the Court of\nIndustrial Relations and the National Labor Relations Commission established under\nPresidential Decree No. 21 on the date of effectivity of this Code shall be transferred to and\nprocessed by the corresponding labor relations divisions or the National Labor Relations\nCommission created under this Code having cognizance of the same in accordance with the\nprocedure laid down herein and its implementing rules and regulations. Cases on labor\nrelations on appeal with the Secretary of Labor or the Office of the President of the Philippines\nas of the date of effectivity of this Code shall remain under their respective jurisdictions and\nshall be decided in accordance with the rules and regulations in force at the time of appeal.\n\nAll workmen’s compensation cases pending before the Workmen’s Compensation Units\nin the regional offices of the Department of Labor and those pending before the Workmen’s\nCompensation Commission as of March 31, 1975, shall be processed and adjudicated in\naccordance with the law, rules and procedure existing prior to the effectivity of the Employees\nCompensation and State Insurance Fund.",
    "chunks": [
      "All cases pending before the Court of\nIndustrial Relations and the National Labor Relations Commission established under\nPresidential Decree No. 21 on the date of effectivity of this Code shall be transferred to and\nprocessed by the corresponding labor relations divisions or the National Labor Relations\nCommission created under this Code having cognizance of the same in accordance with the\nprocedure laid down herein and its implementing rules and regulations. Cases on labor\nrelations on appeal with the Secretary of Labor or the Office of the President of the Philippines\nas of the date of effectivity of this Code shall remain under their respective jurisdictions and\nshall be decided in accordance with the rules and regulations in force at the time of appeal.",
      "All workmen’s compensation cases pending before the Workmen’s Compensation Units\nin the regional offices of the Department of Labor and those pending before the Workmen’s\nCompensation Commission as of March 31, 1975, shall be processed and adjudicated in\naccordance with the law, rules and procedure existing prior to the effectivity of the Employees\nCompensation and State Insurance Fund."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "299"
  },
  {
    "article": "Art. 315",
    "title": "Personnel Whose Services are Terminated",
    "category": "Labor Law - Book 7",
    "simplified_text": "Personnel of agencies or\nany of their subordinate units whose services are terminated as a result of the implementation\nof this Code shall enjoy the rights and protection provided in Sections 5 and 6 of Republic Act\nnumbered fifty-four hundred and thirty five and such other pertinent laws, rules and\nregulations. In any case, no lay-off shall be effected until funds to cover the gratuity and/or\nretirement benefits of those laid off are duly certified as available.",
    "chunks": [
      "Personnel of agencies or\nany of their subordinate units whose services are terminated as a result of the implementation\nof this Code shall enjoy the rights and protection provided in Sections 5 and 6 of Republic Act\nnumbered fifty-four hundred and thirty five and such other pertinent laws, rules and\nregulations. In any case, no lay-off shall be effected until funds to cover the gratuity and/or\nretirement benefits of those laid off are duly certified as available."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "300"
  },
  {
    "article": "Art. 316",
    "title": "Separability Provisions",
    "category": "Labor Law - Book 7",
    "simplified_text": "If any provision or part of this Code, or the\napplication thereof to any person or circumstance, is held invalid, the remainder of this code,\nor the application of such provision or part to other persons or circumstances, shall not be\naffected thereby.",
    "chunks": [
      "If any provision or part of this Code, or the\napplication thereof to any person or circumstance, is held invalid, the remainder of this code,\nor the application of such provision or part to other persons or circumstances, shall not be\naffected thereby."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "301"
  },
  {
    "article": "Art. 317",
    "title": "Repealing Clause",
    "category": "Labor Law - Book 7",
    "simplified_text": "All labor laws not adopted as part of this Code either\ndirectly or by reference are hereby repealed. All provisions of existing laws, orders, decrees,\nrules and regulations inconsistent herewith are likewise repealed.\n\nDone in the City of Manila, this 1st day of May in the year of our Lord, nineteen hundred\nand seventy-four.",
    "chunks": [
      "All labor laws not adopted as part of this Code either\ndirectly or by reference are hereby repealed. All provisions of existing laws, orders, decrees,\nrules and regulations inconsistent herewith are likewise repealed.",
      "Done in the City of Manila, this 1st day of May in the year of our Lord, nineteen hundred\nand seventy-four."
    ],
    "tags": [
      "Book Seven - TRANSITORY AND FINAL PROVISIONS",
      "Title III - TRANSITORY AND FINAL PROVISIONS"
    ],
    "language": "en",
    "old_article_number": "302"
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
