#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pandas numpy matplotlib seaborn scikit-learn')


# In[3]:


#imports
import pandas as pd
import numpy as np
import re

# Define your input/output paths
raw_csv_path = r"D:\PROJECTS\Naukri_Job_Trends\data\raw\naukri_jobs_raw.csv"           # input raw file
cleaned_csv_path = r"D:\PROJECTS\Naukri_Job_Trends\data\cleaned\naukri_cleaned.csv"
exploded_skills_path = "naukri_skills_exploded.csv"
top_skills_out = "naukri_top_skills.csv"


# In[4]:


#load the scraped datset
df = pd.read_csv(raw_csv_path)


# In[5]:


#Standardize Column Names & Setup Lookup
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Map friendly column names for later use
col_lookup = {
    "job_title": "job_title",
    "role": "role" if "role" in df.columns else "job_title",
    "company_name": "company",
    "location": "location",
    "experience_required": "experience",
    "salary": "salary",
    "skills_required": "skills",
    "job_posted_date": "job_posted_date"
}


# In[6]:


#Clean String Columns & Standardize Missing Values
for c in df.columns:
    df[c] = df[c].astype(str).str.strip()
    df[c] = df[c].replace({"nan": np.nan, "none": np.nan, "n/a": np.nan, "na": np.nan, "": np.nan})

# Quick check of missing values
print("\nMissing values per column:")
display(df.isna().sum().sort_values(ascending=False))


# In[7]:


#Remove Duplicates and Rows with Missing Job Titles
before = len(df)
df.drop_duplicates(inplace=True)
df = df[~df['job_title'].isna()].copy()  # keep only rows with job_title
after = len(df)
print(f"Dropped {before - after} duplicates/invalid rows. Remaining: {after}")


# In[8]:


#Parse Experience Column into Min, Max, and Average
exp_col = col_lookup.get("experience_required")

def parse_experience(exp):
    if pd.isna(exp): return (np.nan, np.nan)
    s = str(exp).lower()
    if "fresher" in s: return (0.0, 0.0)
    nums = re.findall(r'(\d+(?:\.\d+)?)', s)
    if len(nums) >= 2: return (float(nums[0]), float(nums[1]))
    if len(nums) == 1: return (float(nums[0]), float(nums[0]))
    return (np.nan, np.nan)

if exp_col in df.columns:
    df["exp_min"], df["exp_max"] = zip(*df[exp_col].apply(parse_experience))
    df["exp_avg"] = df[["exp_min", "exp_max"]].mean(axis=1)
else:
    df["exp_min"] = df["exp_max"] = df["exp_avg"] = np.nan

display(df[[exp_col, "exp_min", "exp_max", "exp_avg"]].head(8))


# In[9]:


#Parse Salary Column into Min, Max, and Average (LPA)
salary_col = col_lookup.get("salary")

def parse_salary(s):
    if pd.isna(s):
        return (np.nan, np.nan, np.nan)

    s = str(s).lower().replace("lpa", "").replace("lac", "").replace("pa", "").replace(",", "").strip()
    match = re.findall(r'(\d+\.?\d*)', s)

    if len(match) == 2:
        min_sal = float(match[0])
        max_sal = float(match[1])
    elif len(match) == 1:
        min_sal = max_sal = float(match[0])
    else:
        return (np.nan, np.nan, np.nan)

    avg_sal = (min_sal + max_sal) / 2

    # Ensure all values are in LPA
    if min_sal > 100 or max_sal > 100 or avg_sal > 100:
        min_sal /= 100000
        max_sal /= 100000
        avg_sal /= 100000

    return (round(min_sal, 2), round(max_sal, 2), round(avg_sal, 2))

df["min_sal"], df["max_sal"], df["sal_avg_lpa"] = zip(*df[salary_col].apply(parse_salary))

display(df[[salary_col, "min_sal", "max_sal", "sal_avg_lpa"]].head(20))


# In[10]:


#Normalize Skills Column into List and Cleaned Text
skills_col = col_lookup.get("skills_required")

def normalize_skill_text(s):
    if pd.isna(s): return []
    parts = re.split(r',|\||;|/|\n|\t|-', str(s))
    cleaned = []
    for p in parts:
        p0 = p.strip().lower()
        if not p0: continue
        p0 = p0.replace("ms ", "").replace("microsoft ", "")
        p0 = p0.replace("powerbi", "power bi").replace("sql server", "sql")
        p0 = re.sub(r'\s+', ' ', p0)
        cleaned.append(p0)
    # unique preserve order
    seen = set(); out = []
    for item in cleaned:
        if item not in seen:
            seen.add(item); out.append(item)
    return out

df["skills_list"] = df[skills_col].apply(normalize_skill_text) if skills_col in df.columns else [[] for _ in range(len(df))]
df["skills_normalized"] = df["skills_list"].apply(lambda lst: ", ".join(lst) if lst else np.nan)

display(df[[skills_col, "skills_normalized"]].head(6))


# In[11]:


#Explode Skills List and Compute Top Skills
df_skills = df[[col_lookup["job_title"], col_lookup["company_name"], col_lookup["location"], "skills_list"]].copy()
df_skills = df_skills[df_skills["skills_list"].apply(lambda x: isinstance(x, list) and len(x) > 0)].reset_index(drop=True)
df_skills_exploded = df_skills.explode("skills_list").rename(columns={"skills_list":"skill"})
df_skills_exploded["skill"] = df_skills_exploded["skill"].str.strip().str.lower()

# Top skills
top_skills = (
    df_skills_exploded["skill"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "skill", "skill": "count"})
)


# In[12]:


#Save Cleaned Data and Skills Outputs
df.to_csv(cleaned_csv_path, index=False, encoding="utf-8-sig")
df_skills_exploded.to_csv(exploded_skills_path, index=False, encoding="utf-8-sig")
top_skills.to_csv(top_skills_out, index=False, encoding="utf-8-sig")

print("Saved cleaned CSV to:", cleaned_csv_path)
print("Saved exploded skills CSV to:", exploded_skills_path)
print("Saved top skills CSV to:", top_skills_out)

