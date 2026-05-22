import os
import sys
import json
import requests

# Load Environment Variables
HANDLE = os.environ.get("CF_HANDLE")
TOKEN = os.environ.get("GH_TOKEN")

if not HANDLE:
    print("Error: CF_HANDLE env variable is missing.")
    sys.exit(1)

print(f"Fetching accepted submissions for Codeforces user: {HANDLE}...")

# 1. Fetch data from official Codeforces API
url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=1000"
response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to query Codeforces API. Status Code: {response.status_code}")
    sys.exit(1)

data = response.json()
if data.get("status") != "OK":
    print("Codeforces API returned an error status.")
    sys.exit(1)

submissions = data.get("result", [])
print(f"Found {len(submissions)} recent submissions total.")

# 2. Setup folders and mapping for file extensions
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

# Language extension mapping
ext_map = {
    "cpp": ".cpp", "c++": ".cpp", "g++": ".cpp", "clang": ".cpp",
    "python": ".py", "pypy": ".py",
    "java": ".java",
    "kotlin": ".kt",
    "rust": ".rs",
    "go": ".go"
}

def get_ext(lang_string):
    lang_lower = lang_string.lower()
    for key, ext in ext_map.items():
        if key in lang_lower:
            return ext
    return ".txt"

# 3. Filter and parse new Accepted (AC) solutions
new_commits = 0
updated_history = list(history)

for sub in submissions:
    sub_id = str(sub.get("id"))
    verdict = sub.get("verdict")
    
    # Only grab unique Accepted solutions
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
        
        # Note: Codeforces API does NOT return full code contents for privacy reasons. 
        # This writes a metadata placeholder tracking file for the problem.
        if not os.path.exists(file_path):
            with open(file_path, "w") as sf:
                sf.write(f"// Codeforces Problem: {contest_id}{index}\n")
                sf.write(f"// Language: {prog_lang}\n")
                sf.write(f"// Submission ID: {sub_id}\n\n")
                sf.write("// Paste your solution source code here if backup required.\n")
            
            updated_history.append(sub_id)
            new_commits += 1

# 4. Save progress
with open(history_file, "w") as f:
    json.dump(updated_history, f)

print(f"Success! Found and logged {new_commits} new solved problems.")
