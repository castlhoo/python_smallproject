# 🔍 Audit News Web Scraper

## 📌 Project Overview
This project was initiated as a way to study advanced Python and web scraping while integrating my interest in auditing.  
The goal is to **scrape the latest news related to audit and use it for data analysis**.  
By collecting news articles from multiple websites based on the keyword **"audit"**, the program utilizes **asynchronous processing for efficient requests** and saves the results in an **Excel file**.

## 🎯 Project Motivation
Auditing plays a crucial role in assessing the financial health of businesses.  
However, gathering information on **current trends, regulatory changes, and key events** related to auditing can be time-consuming.  

This project was developed to address the following challenges:
1. **Efficient web scraping**: Implementing a system to **simultaneously** collect data from multiple news sites.
2. **Real-time audit news collection**: Automatically organizing the latest audit trends.
3. **Utilizing asynchronous processing**: Optimizing request speed using `asyncio` and `ThreadPoolExecutor`.
4. **Data storage for analysis**: Saving scraped data in Excel (`.xlsx`) format for further processing.

---

## 🏗️ Project Structure
```plaintext
├── python_smallproject/
│   ├── concrawling.py             # Web scraping execution code
```

---

## 🛠️ Technologies Used
- **Python 3.9+**
- **Selenium**: Scraping dynamically loaded websites
- **BeautifulSoup**: HTML data parsing
- **asyncio**: Asynchronous web requests handling
- **ThreadPoolExecutor**: Optimizing multi-threaded requests
- **openpyxl**: Storing scraped data in an Excel (`.xlsx`) file

---

## 🚀 Execution Guide

### 1️⃣ **Install Required Libraries**
```bash
pip install -r requirements.txt
```
(Alternatively, manually install the required packages)
```bash
pip install selenium beautifulsoup4 openpyxl requests asyncio webdriver_manager
```

---

## 📊 Target Websites for Scraping
| No  | News Website       | Scraping URL |
|----|------------------|------------------------------------------------------|
| 1️⃣ | Reuters         | [🔗 Reuters Audit News](https://www.reuters.com/site-search/?query=audit) |
| 2️⃣ | CNBC            | [🔗 CNBC Audit News](https://www.cnbc.com/search/?query=audit&qsearchterm=audit) |
| 3️⃣ | Accounting Today | [🔗 Accounting Today Audit](https://www.accountingtoday.com/tag/audit) |

---

## 🛠 Code Explanation

### **1️⃣ Defining URLs for Scraping & Sending Web Requests**
```python
# List of websites to scrape audit-related news from
crawl_urls = [
    "https://www.reuters.com/site-search/?query=audit",
    "https://www.cnbc.com/search/?query=audit&qsearchterm=audit",
    "https://www.accountingtoday.com/tag/audit"
]
```

### **2️⃣ Asynchronously Fetching Web Data**
```python
import asyncio
import requests

async def fetch(url, executor):
    """
    Fetch data asynchronously using ThreadPoolExecutor.
    """
    loop = asyncio.get_running_loop()
    print("Thread Name:", threading.current_thread().getName(), url)
    
    # Running the synchronous requests.get() function asynchronously
    res_fetch = await loop.run_in_executor(executor, requests.get, url)
    
    # Returning the raw HTML content
    return res_fetch.text
```

### **3️⃣ Storing Scraped Data in Excel**
```python
import openpyxl
from bs4 import BeautifulSoup

# Initializing Excel file
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.title = "Audit News"

# Extracting article lists
res1 = requests.get(crawl_urls[0])
soup1 = BeautifulSoup(res1.content, 'html.parser')
items1 = soup1.select('li.story-card__tpl-common__1Q7br.story-card__tpl-feed-media-on-right__383El')  # Corrected class name
for index, item1 in enumerate(items1[:10], start=1):
    # Extracting article titles (using the correct selector)
    title1 = item1.select_one('span.TitleHeading')
    excel_sheet.append([index, "Reuters", title1.text.strip() if title1 else "No Title"])

res2 = requests.get(crawl_urls[1])
soup2 = BeautifulSoup(res2.content, 'html.parser')
items2 = soup2.select('#searchcontainer.Card-title')
for index, item2 in enumerate(items2[:10], start=1):
    title2 = item2.text.strip() if item2 else "No Title"
    excel_sheet.append([index, "CNBC", title2])

res3 = requests.get(crawl_urls[2])
soup3 = BeautifulSoup(res3.content, 'html.parser')
items3 = soup3.select('.MediumImageRightStackedList.PromoMediumlmageRight-title')
for index, item3 in enumerate(items3[:10], start=1):
    title3 = item3.text.strip() if item3 else "No Title"
    excel_sheet.append([index, "Accounting Today", title3])

    # Adding extracted titles to Excel
    excel_sheet.append([index, "Reuters", title1])
```

### **4️⃣ Asynchronous `main()` Function for Multiple URL Requests**
```python
from concurrent.futures import ThreadPoolExecutor

async def main():
    """
    Execute multiple fetch requests asynchronously.
    """
    executor = ThreadPoolExecutor(max_workers=5)
    
    # Creating a list of tasks for each URL
    futures = [fetch(url, executor) for url in crawl_urls]
    
    # Awaiting all requests to complete
    results = await asyncio.gather(*futures)
    
    # Printing response length for verification
    for i, content in enumerate(results):
        print(f"URL {i+1} Response Length:", len(content))
```

### **5️⃣ Saving Scraped Data in Excel File**
```python
# Saving the final Excel file with scraped data
excel_file.save('HotAuditIssue.xlsx')
excel_file.close()
```

---

## 📌 Key Features
✅ **Asynchronous Web Scraping**: Using `asyncio` to fetch data from multiple websites simultaneously  
✅ **Dynamic Page Scraping with Selenium**: Extracting JavaScript-loaded news articles  
✅ **Real-time News Storage**: Saving data in Excel (`.xlsx`) for further analysis  
✅ **Audit-Related Keyword Collection**: Automatically monitoring the latest trends and regulations  

---

## 🔥 Future Enhancements
- **Automation**: Periodic scraping to update with new audit news
- **Data Analysis**: Visualizing trends in audit-related news
- **Cloud Storage**: Integrating with AWS S3 or Google Sheets

---

## Lessons Learned
1. **Limitations of HTML-based Scraping**: Realized the need to expand knowledge to scrape dynamic content effectively.
2. **Power of Asynchronous Scraping**: By collecting data in one place, preprocessing and analysis become feasible, even for AI applications.

✅ **Now run this project to efficiently collect the latest Audit-related news! 🚀**

