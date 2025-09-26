# 📊 Naukri Job Trends Analysis  

This project focuses on analyzing job postings from **Naukri.com**. The idea is to understand the current market trends, most in-demand skills, salary ranges, and job roles through data collected directly from the portal.  

The workflow starts with scraping jobs, then cleaning and processing the dataset, and finally creating meaningful visualizations to extract insights.  

---

## 🚀 Features  

- Web scraping of job postings for multiple roles (Data Analyst, Data Scientist, Python Developer, etc.)  
- Data cleaning and preprocessing (handling missing values, parsing salaries and experience)  
- Exploratory Data Analysis (EDA) using **Matplotlib** and **Seaborn**  
- WordCloud visualization of most frequent skills  
- End-to-end pipeline from raw scraped data → cleaned → processed → final insights  

---

## 📂 Project Structure  

```
Naukri_Job_Trends/
│
├── data/
│   ├── raw/                 # Scraped raw data
│   ├── cleaned/             # Cleaned dataset
│   └── processed/           # Final processed dataset 
│
├── outputs/                 # Generated plots & visualizations
│
├── scripts/                 
│   ├── naukri_scraped.py     # Web scraping
│   ├── naukri_cleaned.py     # Data cleaning & preprocessing
│   └── naukri_processed.py   # Data analysis & visualization
│
├── requirements.txt          # Required Python packages
└── README.md                 # Project documentation
```

## 📑 Usage  

1. **Scraping**  
   - Run `scripts/naukri_scraped.ipynb` to scrape jobs from Naukri.com.  
   - The results will be saved in `data/raw/`.  

2. **Cleaning & Preprocessing**  
   - Run `scripts/naukri_cleaned.ipynb` to clean the scraped data.  
   - Outputs will be stored in `data/cleaned/`.  

3. **Analysis & Visualization**  
   - Run `scripts/naukri_processed.ipynb` to generate plots and insights.  
   - Visuals will be saved under `outputs/`.  

---

## 📊 Example Visuals  

- Salary distribution across roles  
- Average salary per job role  
- Salary vs. required experience  
- Top hiring locations  
- WordCloud of most common skills  

---

## 📦 Requirements  

- pandas==2.3.2  
- numpy==2.3.3  
- selenium==4.35.0  
- webdriver-manager==4.0.2  
- matplotlib==3.10.6  
- seaborn==0.13.2  
- wordcloud==1.9.4  

---

## 🔮 Future Scope  

- Automating the scraping to track weekly/monthly changes  
- Expanding job roles and categories  
- Adding predictive analysis for salary trends  

---

## 👩‍💻 Author  

Developed by **Sashithra**  

---
