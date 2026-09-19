import urllib.request
import urllib.parse
import json

test_set = [
    "sahod para sa mga government employees",
    "pwede ba akong tanggalin kung may sakit ako",
    "sinibak ako nang walang dahilan",
    "tinanggal dahil buntis",
    "minimum wage ng kasambahay",
    "saan ako pwedeng magsampa ng reklamo laban sa employer ko",
    "pwede ba mag-inspect ang DOLE dito sa company namin"
]

print("=" * 70)
print("LIVE CHATBOT RETRIEVAL TESTS ACROSS GENERAL USER QUERIES")
print("=" * 70)

for q in test_set:
    data = urllib.parse.urlencode({"message": q}).encode()
    req = urllib.request.Request("http://127.0.0.1:8000/api/chat", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            top_laws = [(l.get("article"), l.get("title"), l.get("accuracy")) for l in (res.get("laws") or [])]
            print(f"QUERY:    {q}")
            print(f"RESPONSE: {res.get('response', '')[:100]}...")
            print(f"TOP LAWS: {top_laws}")
            print("-" * 70)
    except Exception as e:
        print(f"ERROR on '{q}': {e}")