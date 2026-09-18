"""
Job Portal Analytics — Data Pull Script (JSearch API via RapidAPI)
Aggregates jobs from LinkedIn, Indeed, Glassdoor, ZipRecruiter etc.

pip install requests pandas
"""

import requests
import pandas as pd
import time

# -------- CONFIG --------
RAPIDAPI_KEY = "509f0af1b3msha5ab422ac239df8p14e0a6jsn9f6adadaf6b8"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

SEARCH_TERMS = [
    "data analyst",
    "data scientist",
    "data engineer",
    "software engineer",
    "software developer",
    "full stack developer",
    "backend developer",
    "frontend developer",
    "devops engineer",
    "cloud engineer",
    "cybersecurity analyst",
    "business analyst",
    "product manager",
    "project manager IT",
    "QA engineer",
    "machine learning engineer",
    "AI engineer",
    "system administrator",
    "network engineer",
    "UI UX designer",
]
COUNTRY = "in"          # "in" = India, "us" = USA, etc.
PAGES_PER_TERM = 1       # keep 1 to save your 200 req/month quota (20 roles x 1 page = 20 requests)
# -------------------------

BASE_URL = "https://jsearch.p.rapidapi.com/search-v2"
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
}


def fetch_jobs(search_term, pages=PAGES_PER_TERM):
    all_jobs = []
    for page in range(1, pages + 1):
        params = {
            "query": f"{search_term} in India",
            "page": str(page),
            "num_pages": "1",
            "country": COUNTRY,
            "date_posted": "all",
        }
        resp = requests.get(BASE_URL, headers=HEADERS, params=params)

        if resp.status_code != 200:
            print(f"  [!] page {page} failed: {resp.status_code} - {resp.text[:200]}")
            break

        data = resp.json()
        results = data.get("data", {}).get("jobs", [])
        if not results:
            break

        for job in results:
            all_jobs.append({
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "location": job.get("job_city") or job.get("job_country"),
                "country": job.get("job_country"),
                "employment_type": job.get("job_employment_type"),
                "is_remote": job.get("job_is_remote"),
                "salary_min": job.get("job_min_salary"),
                "salary_max": job.get("job_max_salary"),
                "salary_currency": job.get("job_salary_currency"),
                "posted_date": job.get("job_posted_at_datetime_utc"),
                "source": job.get("job_publisher"),   # LinkedIn / Indeed / Glassdoor etc
                "description": job.get("job_description"),
                "apply_link": job.get("job_apply_link"),
                "search_term": search_term,
            })

        print(f"  page {page}: {len(results)} jobs pulled")
        time.sleep(1)

    return all_jobs


def main():
    everything = []
    for term in SEARCH_TERMS:
        print(f"Fetching: {term}")
        jobs = fetch_jobs(term)
        everything.extend(jobs)
        print(f"  -> total so far: {len(everything)}\n")

    df = pd.DataFrame(everything)
    df.drop_duplicates(subset=["title", "company", "posted_date"], inplace=True)
    df.to_csv("job_data_raw.csv", index=False)
    print(f"Saved {len(df)} rows to job_data_raw.csv")

    if "source" in df.columns:
        print("\nJobs by source portal:")
        print(df["source"].value_counts())


if __name__ == "__main__":
    main()