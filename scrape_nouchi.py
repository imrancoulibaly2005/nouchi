import urllib.request
import re
import json
import time

BASE = "http://www.nouchi.com/dico/liste-des-derniers-mots/alphaindex/dictionnaire/{}.html"
LETTERS = "abcdefghijklmnopqrstuvwxyz"

def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def fetch(letter):
    url = BASE.format(letter)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  Erreur {letter}: {e}")
        return ""

def parse(html):
    results = []
    # Split on <h2 to get each word block
    parts = re.split(r'(?=<h2)', html)
    for part in parts:
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', part, re.DOTALL)
        if not h2:
            continue
        mot = clean(h2.group(1))
        if not mot or len(mot) > 80 or mot.lower() in ('dictionnaire', 'nouchi'):
            continue
        # Type
        typ_m = re.search(r'Type\s*:\s*([^,\n<]{2,40})', part)
        typ = clean(typ_m.group(1)).rstrip(',').strip() if typ_m else "nom"
        # Signification
        sig_m = re.search(r'Signification\s*:\s*<[^>]*>(.*?)</[a-z]>', part, re.DOTALL)
        if not sig_m:
            sig_m = re.search(r'Signification\s*:\s*(.*?)(?:Synonyme|Type|<hr|$)', part, re.DOTALL)
        sig = clean(sig_m.group(1)) if sig_m else ""
        # Synonyme as fallback
        if not sig:
            syn_m = re.search(r'Synonyme\(s\)\s*:\s*(.*?)(?:\n|<hr|Type|$)', part, re.DOTALL)
            sig = clean(syn_m.group(1)) if syn_m else ""
        if mot and sig:
            results.append({"mot": mot, "type": typ, "sig": sig})
    return results

all_words = []
seen = set()

for letter in LETTERS:
    print(f"Fetching {letter.upper()}...", end=" ", flush=True)
    html = fetch(letter)
    words = parse(html)
    new = 0
    for w in words:
        key = w["mot"].lower()
        if key not in seen:
            seen.add(key)
            all_words.append(w)
            new += 1
    print(f"{new} mots")
    time.sleep(0.3)

print(f"\nTotal: {len(all_words)} mots extraits")
with open("scraped_nouchi.json", "w", encoding="utf-8") as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)
print("Sauvegardé dans scraped_nouchi.json")
