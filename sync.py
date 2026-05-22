import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup

HANDLE = os.environ.get("CF_HANDLE")
TOKEN = os.environ.get("GH_TOKEN")

if not HANDLE:
    print("Error: CF_HANDLE env variable is missing.")
    sys.exit(1)

print(f"Fetching accepted submissions for: {HANDLE}...")

# 1. Fetch metadata from Codeforces API
url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=100"
response = requests.get(url)

if response.status_code != 200 or response.json().get("status") != "OK":
    print("Failed to contact Codeforces API.")
    sys.exit(1)

submissions = response.json().get("result", [])
os.makedirs("submissions", exist_ok=True)
history_file = "submission_history.json"

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        try:
            history = set(json.load(f))
        except:
            history = set()
else:
    history = set()

# C++ specific extension check
def get_ext(lang_string):
    if "c++" in lang_string.lower() or "g++" in lang_string.lower():
        return ".cpp"
    return ".txt"

new_commits = 0
updated_history = list(history)

# 2. Extract code block from HTML page
for sub in submissions:
    sub_id = str(sub.get("id"))
    verdict = sub.get("verdict")
    
    if verdict == "OK" and sub_id not in history:
        problem = sub.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        prog_lang = sub.get("programmingLanguage", "txt")
        
        if not contest_id or not index:
            continue
            
        prob_name = f"{contest_id}_{index}"
        ext = get_ext(prog_lang)
        file_path = f"submissions/{prob_name}{ext}"
        
        # Build the actual submission page web link
        submission_url = f"https://codeforces.com/contest/{contest_id}/submission/{sub_id}"
        print(f"Scraping code for problem {prob_name} (ID: {sub_id})...")
        
        try:
            # Codeforces pages require a standard User-Agent header or they block requests
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            page_res = requests.get(submission_url, headers=headers)
            
            if page_res.status_code == 200:
                soup = BeautifulSoup(page_res.text, 'html.parser')
                # Find the specific source code element block on Codeforces
                code_element = soup.find('pre', id='program-source-text')
                
                if code_element:
                    source_code = code_element.text
                    
                    with open(file_path, "w", encoding="utf-8") as sf:
                        sf.write(source_code)
                        
                    updated_history.append(sub_id)
                    new_commits += 1
                    # Polite delay so Codeforces doesn't flag the script for rate limits
                    time.sleep(2)
                else:
                    print(f"Could not find code element for submission {sub_id}. Private block?")
            else:
                print(f"Failed to fetch submission page {sub_id}. Code: {page_res.status_code}")
        except Exception as e:
            print(f"Error scraping submission {sub_id}: {e}")

# 3. Save progress
with open(history_file, "w") as f:
    json.dump(updated_history, f)

print(f"Finished! Successfully archived {new_commits} actual C++ source code files.")
