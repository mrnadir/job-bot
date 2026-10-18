import os, json, requests
from bs4 import BeautifulSoup

URL = "https://bdgovtjob.net/category/government-jobs-circular/"
SEEN_FILE = "seen.json"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_jobs():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    jobs = {}
    for a in soup.select("h2 a[href]"):
        link = a["href"]
        if link.startswith("https://bdgovtjob.net/") and "/category/" not in link:
            jobs[link] = a.get_text(strip=True)
    return jobs

def send_whatsapp(text):
    requests.get(
        "https://api.callmebot.com/whatsapp.php",
        params={
            "phone": os.environ["WA_PHONE"],    # country code soho, jemon 8801XXXXXXXXX
            "apikey": os.environ["WA_APIKEY"],
            "text": text,
        },
        timeout=30,
    )

def main():
    seen = set(json.load(open(SEEN_FILE))) if os.path.exists(SEEN_FILE) else set()
    jobs = get_jobs()
    new = {l: t for l, t in jobs.items() if l not in seen}

    if not jobs:
        print("Kono job pawa jayni, selector check korun")
        return

    for link, title in new.items():   # ekta ekta kore pathai, jate message boro na hoy
        send_whatsapp(f"🆕 {title}\n{link}")

    json.dump(sorted(seen | set(jobs)), open(SEEN_FILE, "w"), ensure_ascii=False)
    print(f"{len(new)} ta notun job pathano hoyeche")

main()