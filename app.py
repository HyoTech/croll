import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

url_list = {
    'fantasy': 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=203&page=',
    'romance': 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=207&page=',
    'thriller': 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=202&page=',
    'sf': 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=208&page=',
    'mystery': 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=206&page=',
    'historical': 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=205&page='
}

def write_novel_file(genre_name, base_url):
    page = 1
    total_count = 0
    seen_urls = set()  # 중복 제거를 위한 집합

    # 파일 열기
    with open(f'{genre_name}.txt', 'w', encoding='utf-8') as f:
        while True:
            now_url = f"{base_url}{page}"
            response = requests.get(now_url)
            time.sleep(1)  # 요청 간격
            
            if response.status_code != 200:
                print(f"Error fetching {now_url}: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')

            # 소설 목록 선택
            novel_list = soup.select('#content > div > ul > li')

            # 페이지에 소설이 없으면 종료
            if not novel_list:
                print(f"No more novels on page {page}.")
                break

            for novel in novel_list:
                # 소설의 링크 추출 (상대 경로를 절대 경로로 변환)
                href = novel.find('a')['href']
                full_url = urljoin(base_url, href)

                # 중복 확인
                if full_url not in seen_urls:
                    seen_urls.add(full_url)  # 새로운 데이터 저장
                    print(full_url, file=f)  # 파일에 저장
                    total_count += 1
            
            print(f"Page {page} completed. Total collected: {total_count}")
            page += 1

            # 중복된 데이터를 가져왔을 경우 종료
            if len(novel_list) > 0 and all(urljoin(base_url, novel.find('a')['href']) in seen_urls for novel in novel_list):
                print("All novels are duplicates. Stopping the crawl.")
                break
        
    print(f"{genre_name} 완료, 총 {total_count} 개의 소설 저장 완료.")

# 각 장르에 대해 파일 작성 실행
for genre, url in url_list.items():
    write_novel_file(genre, url)