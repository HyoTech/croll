import requests
from bs4 import BeautifulSoup
import csv
import time

# 장르별 텍스트 파일 매핑
text_list = {
    #'fantasy': 'fantasy.txt',
    'romance': 'romance.txt',
    'thriller': 'thriller.txt',
    'sf': 'sf.txt',
    'mystery': 'mystery.txt',
    'historical': 'historical.txt'
}

# 텍스트 파일에서 링크 읽기
def read_links_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        links = [line.strip() for line in file.readlines()]
    return links

# 소설 정보 크롤링
def scrape_novel_details(url):
    response = requests.get(url)
    time.sleep(1)  # 요청 간격 조정
    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # 소설 이름
        novel_name_tag = soup.select_one('.end_head > h2')
        if not novel_name_tag:
            print(f"novel_name_tag not found in {url}")
        novel_name = novel_name_tag.text.strip() if novel_name_tag else "N/A"

        # 작가 이름
        author_tag = soup.select_one('.info_lst > ul > li:has(span:-soup-contains("글")) > a')
        if not author_tag:
            print(f"author_tag not found in {url}")
        author = author_tag.text.strip() if author_tag else "N/A"

        # 장르
        genre_tag = soup.select_one('.info_lst > ul > li:nth-of-type(2) > span > a')
        if not genre_tag:
            print(f"genre_tag not found in {url}")
        genre = genre_tag.text.strip() if genre_tag else "N/A"

        # 인트로 내용
        intro_tag = soup.select_one('._synopsis')
        if not intro_tag:
            print(f"intro_tag not found in {url}")
        intro = intro_tag.text.strip() if intro_tag else "N/A"

        return {
            'novel_name': novel_name,
            'author': author,
            'genre': genre,
            'intro': intro,
            'url': url
        }

    except AttributeError as e:
        print(f"Error parsing {url}: {e}")
        return None

# 결과를 CSV로 저장
def save_to_csv(filename, data):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['novel_name', 'author', 'genre', 'intro', 'url'])
        writer.writeheader()
        writer.writerows(data)

# 메인 실행 로직
def main():
    for genre, input_file in text_list.items():
        print(f"Processing {genre} ({input_file})...")
        links = read_links_from_file(input_file)
        print(f"총 {len(links)}개의 링크를 읽었습니다.")

        novel_details = []

        for idx, link in enumerate(links, start=1):
            print(f"[{idx}/{len(links)}] {link} 처리 중...")
            details = scrape_novel_details(link)
            if details:
                novel_details.append(details)

        # 장르별 CSV 파일로 저장
        output_file = f'{genre}_novel_details.csv'
        save_to_csv(output_file, novel_details)
        print(f"{genre} 장르 크롤링 완료. 결과가 {output_file}에 저장되었습니다.\n")

if __name__ == '__main__':
    main()