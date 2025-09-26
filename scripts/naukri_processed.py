#!/usr/bin/env python
# coding: utf-8

# ***Processing the Dataset***

# In[1]:


get_ipython().system('pip install wordcloud')


# In[2]:


#Imports & paths
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Paths
cleaned_csv_path = r"D:\PROJECTS\Naukri_Job_Trends\data\cleaned\naukri_cleaned.csv"
processed_csv_path = r"D:\PROJECTS\Naukri_Job_Trends\data\processed\naukri_processed.csv"


# In[3]:


#Load cleaned CSV & overview
df = pd.read_csv(cleaned_csv_path)

print("Rows, Columns:", df.shape)
print("\nMissing values per column:")
display(df.isna().sum())


# In[4]:


# Fill missing categorical columns
df['location'] = df['location'].fillna("Unknown")
df['company'] = df['company'].fillna("Unknown")
df['skills_normalized'] = df['skills_normalized'].fillna("None")


# In[5]:


#Fill missing numeric/experience columns (role-wise)
exp_cols = ['exp_min', 'exp_max', 'exp_avg']
for col in exp_cols:
    df[col] = df.groupby('role')[col].transform(lambda x: x.fillna(x.mean()))


# In[6]:


#Impute missing salaries (role-wise)
job_col = "role"

# Compute role-wise averages for min & max salary
role_salary_stats = df.groupby(job_col).agg(
    avg_min_sal=("min_sal", "mean"),
    avg_max_sal=("max_sal", "mean")
).round(1)

# Impute missing values using role-wise averages
def fill_salary(row):
    if pd.isna(row["min_sal"]):
        row["min_sal"] = role_salary_stats.loc[row[job_col], "avg_min_sal"]
    if pd.isna(row["max_sal"]):
        row["max_sal"] = role_salary_stats.loc[row[job_col], "avg_max_sal"]
    return row

df = df.apply(fill_salary, axis=1)

# Recompute average salary after imputation
df["sal_avg_lpa"] = df[["min_sal", "max_sal"]].mean(axis=1).round(1)


# In[7]:


# Drop unnecessary / redundant columns
cols_to_drop = ["experience", "salary", "skills", "posted_date"]
df = df.drop(columns=cols_to_drop)

print("Dropped columns:", cols_to_drop)
print("Remaining columns:", df.columns.tolist())


# In[8]:


#Save processed CSV
output_csv_path = "D:/PROJECTS/Naukri_Job_Trends/data/processed/final_naukri_processed.csv"

df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

print("Saved final processed CSV to:", output_csv_path)


# ***Visualizations: top roles, salaries, experience vs salary***

# In[9]:


#Load processed dataset
df = pd.read_csv(output_csv_path)


# In[10]:


#Visualize Distribution of Average Salaries (LPA)
plt.figure(figsize=(8,5))
sns.histplot(df["sal_avg_lpa"], bins=30, kde=True)
plt.title("Distribution of Average Salaries (LPA)")
plt.xlabel("Average Salary (LPA)")
plt.ylabel("Frequency")

plt.savefig(r"D:\PROJECTS\Naukri_Job_Trends\outputs\Distribution of Average Salaries.png", dpi=300, bbox_inches="tight")

plt.show()


# In[11]:


#Average Salary per Role (Bar Plot)
salary_role = df.groupby("role")["sal_avg_lpa"].mean().sort_values(ascending=False)

plt.figure(figsize=(10,6))
sns.barplot(x=salary_role.values, y=salary_role.index, palette="viridis")
plt.title("Average Salary per Role (LPA)")
plt.xlabel("Average Salary (LPA)")
plt.ylabel("Role")

# Add labels
for index, value in enumerate(salary_role.values):
    plt.text(value + 0.2, index, f"{value:.1f}", va='center')

plt.tight_layout()

plt.savefig(r"D:\PROJECTS\Naukri_Job_Trends\outputs\Average Salary per Role.png", dpi=300, bbox_inches="tight")

plt.show()




# In[12]:


#Scatter Plot: Average Salary vs Experience by Role
role_exp_salary = df.groupby("role")[["exp_avg", "sal_avg_lpa"]].mean().reset_index()

plt.figure(figsize=(10,6))
sns.scatterplot(
    data=role_exp_salary, 
    x="exp_avg", 
    y="sal_avg_lpa", 
    hue="role", 
    s=150,  # bigger points
    palette="tab10"
)

for i, row in role_exp_salary.iterrows():
    plt.text(row["exp_avg"]+0.1, row["sal_avg_lpa"]+0.1, row["role"], fontsize=9)

plt.title("Average Salary vs Experience by Role")
plt.xlabel("Average Experience (Years)")
plt.ylabel("Average Salary (LPA)")

plt.savefig(r"D:\PROJECTS\Naukri_Job_Trends\outputs\Average Salary vs Experience by Role.png", dpi=300, bbox_inches="tight")

plt.show()



# In[13]:


# Box Plot: Salary Distribution by Role
plt.figure(figsize=(12,6))
sns.boxplot(data=df, x="role", y="sal_avg_lpa", palette="Set2")
plt.title("Salary Distribution by Role")
plt.xticks(rotation=90)
plt.ylabel("Average Salary (LPA)")

plt.savefig(r"D:\PROJECTS\Naukri_Job_Trends\outputs\Salary Distribution by Role.png", dpi=300, bbox_inches="tight")

plt.show()



# In[14]:


#Top 10 Hiring Locations
location_counts = df["location"].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=location_counts.values, y=location_counts.index, palette="magma")
plt.title("Top 10 Hiring Locations")
plt.xlabel("Number of Job Postings")
plt.ylabel("Location")

plt.savefig(r"D:\PROJECTS\Naukri_Job_Trends\outputs\Top 10 hiring Locations.png", dpi=300, bbox_inches="tight")

plt.show()




# In[15]:


#Word Cloud of Most Common Skills

skills_text = " ".join(df["skills_normalized"].dropna().astype(str))
wordcloud = WordCloud(width=1000, height=500, background_color="white").generate(skills_text)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most Common Skills")

plt.savefig(r"D:\PROJECTS\Naukri_Job_Trends\outputs\Most Common Skills.png", dpi=300, bbox_inches="tight")

plt.show()


