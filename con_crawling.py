import asyncio
import requests, openpyxl
import threading
import timeit
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# 실행 시작시간 측정
start_time = timeit.default_timer()

# 크롤링할 URL 리스트
crawl_urls = [
    "https://www.reuters.com/site-search/?query=audit",
    "https://www.cnbc.com/search/?query=audit&qsearchterm=audit",
    "https://www.accountingtoday.com/tag/audit"
]

# 비동기 fetch 함수 정의
async def fetch(url, executor):
    loop = asyncio.get_running_loop()
    print("Thread Name:", threading.current_thread().getName(), url)

    # 비동기적으로 HTTP 요청 실행
    res_fetch = await loop.run_in_executor(executor, requests.get, url)
    
    # 응답 HTML 반환
    return res_fetch.text

# 액셀 파일 생성 및 설정
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.title = "Audit Trend"

# 액셀 헤더 추가
header = ['No', 'Publications', 'Head']
excel_sheet.append(header)

# 열 너비 조정
excel_sheet.column_dimensions['A'].width = 5
excel_sheet.column_dimensions['B'].width = 20
excel_sheet.column_dimensions['C'].width = 100

# 크롤링하여 Excel에 데이터 저장
res1 = requests.get(crawl_urls[0])
soup1 = BeautifulSoup(res1.content, 'html.parser')

# 기사 리스트 가져오기
items1 = soup1.select('ul.search-results__list__2SxSK')  # 정확한 클래스명 적용
for index, item1 in enumerate(items1[:10], start=1):
    # 기사 제목 가져오기 (올바른 선택자 사용)
    title1_tag = item1.select_one("span.TitleHeading")
    title1 = title1_tag.text.strip() if title1_tag else "No Title"

    # 엑셀에 데이터 추가
    excel_sheet.append([index, "Reuters", title1])

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

# 액셀 파일 저장
excel_file.save('HotAuditIssue.xlsx')
excel_file.close()

# 비동기 main 함수
async def main():
    executor = ThreadPoolExecutor(max_workers=5)

    # 비동기 요청 실행
    futures = [fetch(url, executor) for url in crawl_urls]
    results = await asyncio.gather(*futures)

    for i, content in enumerate(results):
        print(f"URL {i+1} 응답 길이:", len(content))  # 응답 데이터 길이 출력

# 메인 함수 실행
if __name__ == '__main__':
    asyncio.run(main())

    execution_time = timeit.default_timer() - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
