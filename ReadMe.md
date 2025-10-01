# 📘 Course Scraper  

_Automated course data scraper built with Python & Selenium 🕵️‍♂️_  

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)  
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium)  
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)  
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-lightblue?logo=numpy)  
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-teal?logo=pandas)  

---

## 📖 Overview  

Course Scraper is a Python-based automation tool that scrapes **Coursera** courses using **Selenium**.  
As of today `(1-Oct-2025)`, it works smoothly and extracts structured course data into a clean format for analysis.

🔎 **Why it exists?**  
I built this to collect educational data for experiments, ML projects, and analytics.  

⚡ **Flexibility:**  
- If Coursera changes its site paths, you can easily update them inside `_config.py`.  
- Anyone can reuse and modify this project for their own data collection needs.  

🛠️ **Maintenance Note:**  
I don’t plan on adding new features 🚫, but I’ll fix bugs if something breaks.

💬 **Support:**  
If you run into issues or bugs, just hit me up

---

## ⚡ Installation    

You can either **download the ZIP** or **clone via Git**:  

**Download ZIP:** [Download Here](https://github.com/cmd-HMN/Course_Scraper/archive/refs/heads/main.zip)  

or 

**Clone via Git:**  

```bash
git clone https://github.com/cmd-HMN/Course_Scraper.git
cd Course_Scraper
```

---
## 🖥️ Running  

You can run the scraper in two ways: *via shell script* or *directly with Python*.  

### 1. Run using Shell Script 

```bash
# For Linux, first make the script executable
chmod +x ./run_pipeline.sh  

# Then run the pipeline
./run_pipeline.sh

```

###  2. Run using python

```
# Move into source directory
cd scraper/src  

# Install dependencies
pip install -r requirements.txt  

# Run pipeline
python pipeline.py
```

---

### ⚙️ Arguments  

Both methods (shell script or Python) accept arguments to control scraping:  

#### General
- `_config.py` → This general setting is in this file.

#### Crawler Specific
- `-co`, `-overwrite` → Overwrite the `crawler.txt` file (default: False)  
- `-cinterval`, `-crawl_interval` → Time interval in which the crawler works before taking a rest (default: 5 seconds)  
- `-crest`, `-crawl_rest` → Rest time of the crawler after interval (default: 1.5 seconds)  

#### Scraper Specific
- `-sinterval`, `-scraper_interval` → Time interval in which the scraper works before taking a rest (default: 5 seconds)  
- `-srest`, `-scraper_rest` → Rest time of the scraper after interval (default: 1.5 seconds)  
- `-scount`, `-scraper_link_count` → Number of links to scrape (default: all / None)  

#### Example  

```bash
python pipeline.py -co True -cinterval 6 -crest 2 -sinterval 4 -srest 1 -scount 50
```

---

## 📜 License  

This project is licensed under the **MIT License**.  
See the [`LICENSE`](LICENSE) file for more details.

---

## 🌟 Acknowledgements  

- Built with ❤️ using Python, Selenium, NumPy, and Pandas  
- Inspired by educational data scraping projects  
- If you find a bug or issue, just hit me up ✌️  

---

Thank you for checking out **Course Scraper**!
