

"""
Job Portal Analytics — Data Cleaning Script
Cleans the raw job data pulled from JSearch API and produces a clean CSV file.

Usage:
    python data_cleaning.py

Input:  job_data_raw.csv    (raw file from the API pull script)
Output: job_data_clean.csv  (cleaned data)

pip install pandas
"""

import re
import pandas as pd

# -------- CONFIG --------
INPUT_CSV = "job_data_raw.csv"
OUTPUT_CLEAN_CSV = "job_data_clean.csv"

# Known job-board portals we want to call out separately in a "platform" column.
# Everything else (company career pages) gets bucketed as "Company Site".
KNOWN_PORTALS = ["LinkedIn", "Indeed", "Glassdoor", "Shine", "BeBee"]
# -------------------------


def clean_description(text):
    """Collapse literal \\n escapes and repeated whitespace into single spaces."""
    if pd.isna(text):
        return text
    text = text.replace("\\n", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def bucket_platform(source, known_portals=KNOWN_PORTALS):
    """Map the messy 'source' (job_publisher) field to a clean platform bucket."""
    source_str = str(source).lower()
    for portal in known_portals:
        if portal.lower() in source_str:
            return portal
    return "Company Site"


def load_data(path):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns from {path}")
    return df


def clean_data(df):
    df = df.copy()

    # 1. Drop columns that are 100% empty (salary fields — API never returned them)
    empty_cols = [c for c in df.columns if df[c].isnull().all()]
    if empty_cols:
        print(f"Dropping fully-empty columns: {empty_cols}")
        df = df.drop(columns=empty_cols)

    # 2. Fix stray unicode characters (e.g. en-dash instead of hyphen) in employment_type
    if "employment_type" in df.columns:
        df["employment_type"] = (
            df["employment_type"].astype(str).str.replace("–", "-", regex=False).str.strip()
        )

    # 3. Fill missing location / country
    for col in ["location", "country"]:
        if col in df.columns:
            df[col] = df[col].fillna("Not specified")

    # 4. Normalize posted_date to a plain date (invalid/missing -> blank)
    if "posted_date" in df.columns:
        df["posted_date"] = pd.to_datetime(
            df["posted_date"], errors="coerce", utc=True
        ).dt.date

    # 5. Clean up description text
    if "description" in df.columns:
        df["description"] = df["description"].apply(clean_description)

    # 6. Strip whitespace on key text columns
    for col in ["title", "company", "location", "source", "search_term"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 7. Add a clean 'platform' column (LinkedIn/Indeed/Glassdoor/Shine/BeBee vs Company Site)
    if "source" in df.columns:
        df["platform"] = df["source"].apply(bucket_platform)

    # 8. Make is_remote human-readable
    if "is_remote" in df.columns:
        df["is_remote"] = df["is_remote"].map({True: "Yes", False: "No"}).fillna(df["is_remote"])

    # 9. Drop duplicate postings (same title + company + apply link)
    before = len(df)
    dedup_subset = [c for c in ["title", "company", "apply_link"] if c in df.columns]
    df = df.drop_duplicates(subset=dedup_subset)
    print(f"Dropped {before - len(df)} duplicate postings")

    # 10. Reorder columns for readability
    preferred_order = [
        "title", "company", "location", "country", "employment_type",
        "is_remote", "platform", "source", "posted_date", "search_term",
        "description", "apply_link",
    ]
    ordered_cols = [c for c in preferred_order if c in df.columns]
    remaining_cols = [c for c in df.columns if c not in ordered_cols]
    df = df[ordered_cols + remaining_cols]

    return df


def main():
    raw_df = load_data(INPUT_CSV)

    clean_df = clean_data(raw_df)
    clean_df.to_csv(OUTPUT_CLEAN_CSV, index=False)
    print(f"Saved cleaned data -> {OUTPUT_CLEAN_CSV}  ({clean_df.shape[0]} rows, {clean_df.shape[1]} cols)")

    print("\nNull counts after cleaning:")
    print(clean_df.isnull().sum())

    if "platform" in clean_df.columns:
        print("\nJobs by platform:")
        print(clean_df["platform"].value_counts())


if __name__ == "__main__":
    main()