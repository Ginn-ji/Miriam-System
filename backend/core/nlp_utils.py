import re
import io
import PyPDF2
from fastapi import HTTPException
from langdetect import detect

CONVERSATIONAL_FILLERS = [
    r"\bano po ba ang\b", r"\bano po ba\b", r"\bano po\b", r"\bano ba ang\b", r"\bano ba\b",
    r"\bpwede po ba akong\b", r"\bpwede po bang\b", r"\bpwede po ba\b", r"\bpwede bang\b", r"\bpwede ba akong\b", r"\bpwede ba\b",
    r"\btanong ko lang po\b", r"\btanong ko lang\b", r"\bgusto ko lang itanong\b", r"\bgusto ko lang malaman\b",
    r"\blegal po ba na\b", r"\blegal po ba\b", r"\blegal ba na\b", r"\blegal ba\b",
    r"\bmeron po ba akong\b", r"\bmayroon po ba akong\b", r"\bmeron ba akong\b",
    r"\bano ang dapat kong gawin kapag\b", r"\bano dapat gawin kapag\b", r"\bano gagawin kapag\b",
    r"\bkasi naman\b", r"\bbigla na lang\b", r"\bbasta na lang\b", r"\blang po\b", r"\bpo ba\b"
]

TAGALOG_MARKERS = {
    "ang", "ng", "sa", "na", "mga", "ko", "mo", "ako", "ka", "siya", "kami", "tayo", "kayo", "sila",
    "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung",
    "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
    "may", "wala", "walang", "hindi", "ayaw", "trabaho", "sahod", "sweldo", "suweldo", "kaltas", "tanggal",
    "tinanggal", "tinanggalan", "sinibak", "pinaalis", "nagresign", "overtime", "buntis", "amo", "boss"
}

def clean_conversational_noise(text: str) -> str:
    cleaned = text.lower().replace('"', ' ').replace("'", " ")
    for pattern in CONVERSATIONAL_FILLERS:
        cleaned = re.sub(pattern, " ", cleaned)
    cleaned = cleaned.replace("-", " ")
    cleaned = re.sub(r'\b(\w{4,})ng\b', r'\1', cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()

def strip_filipino_affixes(word: str) -> str:
    w = word.lower()
    if len(w) <= 4: return w
    if len(w) > 4 and w[1:3] == 'in' and w[0] not in 'aeiou': w = w[0] + w[3:]
    if len(w) > 4 and w[1:3] == 'um' and w[0] not in 'aeiou': w = w[0] + w[3:]
    for pre in ['pinag', 'ipag', 'pina', 'nag', 'mag', 'pag']:
        if w.startswith(pre) and len(w) > len(pre) + 2:
            w = w[len(pre):]
            break
    if len(w) >= 6 and w[:2] == w[2:4]: w = w[2:]
    for suf in ['han', 'hin', 'an', 'in']:
        if w.endswith(suf) and len(w) > len(suf) + 3:
            w = w[:-len(suf)]
            break
    return w

def detect_language_simple(text: str) -> str:
    try: return detect(text[:1000])
    except: return "unknown"

def is_tagalog_or_taglish(text: str) -> bool:
    tokens = set(re.sub(r'[^\w\s]', '', text.lower()).split())
    if tokens & TAGALOG_MARKERS: return True
    return detect_language_simple(text) in ['tl', 'unknown', 'id', 'ms', 'sk', 'cy', 'hr']

async def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return "".join(page.extract_text() or "" for page in pdf_reader.pages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting PDF: {str(e)}")

def is_valid_password(pwd: str) -> bool:
    return len(pwd) >= 8 and bool(re.search(r'[^a-zA-Z]', pwd))

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))