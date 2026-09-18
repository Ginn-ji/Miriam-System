"""
backup_db.py
------------
Exports all MongoDB collections from thesis_db to JSON files
stored in a timestamped backup folder.

Collections backed up:
  - legal_knowledge
  - users  (passwords are kept as hashed strings - never plaintext)
  - chat_history
  - settings
  - translation_cache
  - test_cases

Usage:
    python backup_db.py
"""

import sys
# Force UTF-8 output to avoid Windows charmap codec errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# ── Config ────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME   = os.environ["DB_NAME"]

COLLECTIONS = [
    "legal_knowledge",
    "users",
    "chat_history",
    "settings",
    "translation_cache",
    "test_cases",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def make_serializable(doc: dict) -> dict:
    """Convert MongoDB ObjectId and datetime objects to JSON-safe strings."""
    clean = {}
    for k, v in doc.items():
        if k == "_id":
            clean[k] = str(v)          # ObjectId → string
        elif hasattr(v, "isoformat"):
            clean[k] = v.isoformat()   # datetime → ISO string
        elif isinstance(v, dict):
            clean[k] = make_serializable(v)
        elif isinstance(v, list):
            clean[k] = [
                make_serializable(i) if isinstance(i, dict) else
                str(i) if hasattr(i, "isoformat") else i
                for i in v
            ]
        else:
            clean[k] = v
    return clean


# ── Main ──────────────────────────────────────────────────────────────────────
async def backup():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = ROOT_DIR / "backups" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    print(f"Connecting to MongoDB Atlas ({DB_NAME})...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    summary = {}

    for col_name in COLLECTIONS:
        print(f"  Exporting '{col_name}'...", end=" ", flush=True)
        try:
            docs = await db[col_name].find({}).to_list(None)
            clean_docs = [make_serializable(d) for d in docs]

            out_file = backup_dir / f"{col_name}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(clean_docs, f, ensure_ascii=False, indent=2)

            count = len(clean_docs)
            summary[col_name] = count
            print(f"{count} documents -> {out_file.name}")

        except Exception as e:
            summary[col_name] = f"ERROR: {e}"
            print(f"FAILED -- {e}")

    client.close()

    # Write a summary manifest
    manifest = {
        "backup_timestamp_utc": timestamp,
        "database": DB_NAME,
        "collections": summary,
    }
    with open(backup_dir / "_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    total = sum(v for v in summary.values() if isinstance(v, int))
    print(f"\nBackup complete! Saved to: {backup_dir}")
    print(f"Total documents backed up: {total}")
    for col, count in summary.items():
        print(f"  {col}: {count}")


if __name__ == "__main__":
    asyncio.run(backup())
