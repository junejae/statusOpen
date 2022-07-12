# 기본 패키지
import time
import string
import argparse
import pandas as pd
from bs4 import BeautifulSoup

# 크롤링 패키지
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# NLP 패키지
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline


def crawling(args):
    # 감정분석 모델 준비
    model_name = args.model_name
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    pipe = TextClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            device=0, # gpu number, -1 if cpu used
            return_all_scores=True,
            function_to_apply='sigmoid'
        )

    # chromedriver가 저장된 위치
    driver_dir = args.driver_dir

    # 결과물을 저장할 위치
    data_dir = args.data_dir

    # 데이터를 수집 할 작품 제목 리스트
    novel_list = args.novel_list

    driver = webdriver.Chrome(driver_dir) # 크롬드라이버 경로 설정

    for novel in novel_list:
        print(f"Crawling: {novel}")
        # url입력
        url = "https://pagestage.kakao.com/search" # 사이트 입력
        driver.get(url) # 사이트 오픈
        time.sleep(5) # 5초 지연

        # 검색창 선택
        xpath = '''//*[@id="__next"]/div[1]/div/main/div/div/div[1]/div/form/div/input'''
        element = driver.find_element(by=By.XPATH, value=xpath)
        element.clear()
        time.sleep(2)

        # 검색창 입력
        element.send_keys(novel)
        time.sleep(2)

        element.send_keys(Keys.ENTER)
        time.sleep(2)

        # 처음 보이는 검색결과 클릭(19금 작품은 로그인 되어있지 않아 열람 불가능)
        search_xpath = '''//*[@id="__next"]/div[1]/div/main/div/div/div[3]/div/div[2]/div[1]/div'''
        driver.find_element(by=By.XPATH, value=search_xpath).click()
        time.sleep(2)

        # 더보기 버튼이 없어지기 전까지 무한클릭 -> 모든 댓글 확보
        while True:
            try:
                more_xpath = '''//*[@id="__next"]/div[1]/div/main/section/div/div[3]/section/button'''
                driver.find_element(by=By.XPATH, value=more_xpath).click()
                time.sleep(3)
            except:
                break

        # 스포일러 방지 버튼이 없어지기 전까지 무한클릭 -> 모든 내용 온전히 확보
        while True:
            try:
                spoil_xpath = '''//*[@id="__next"]/div[1]/div/main/section/div/div[3]/section/div/div/div/p/button'''
                driver.find_element(by=By.XPATH, value=spoil_xpath).click()
                time.sleep(2)
            except:
                break

        # 페이지 소스 출력
        html = driver.page_source
        html_source = BeautifulSoup(html, 'html.parser')
        full_comments = html_source.find_all("div", attrs={"class":"flex-[0_1_100%] relative"})  # 전체 댓글 스크립트

        # 데이터 추출
        nicknames = []
        dates = []
        story_nums = []
        sentences = []
        likes = []

        for comment in full_comments:
            nickname = comment.find("p", attrs={"class":"break-words font-bold mr-6"}).string
            date = comment.find("div", attrs={"class":"flex-[0_0_auto]"}).string
            story_num = comment.find("a").string
            sentence = comment.find("p", attrs={"class":"leading-[21px] break-all"}).string
            like = comment.find("span", attrs={"class":"font-gmarket font-medium leading-[normal] pt-[0.2em] text-12 text-13"}).string
            
            # 댓글 전처리 작업
            sentence = sentence.replace("#스테이지스테플러_대가성활동", "").strip()

            nicknames.append(nickname)
            dates.append(date)
            story_nums.append(story_num)
            sentences.append(sentence)
            likes.append(like)

        print(f"Sentimental Analysis: {novel}")
        # 댓글 감정분석
        emotions = []

        for outputs in pipe(sentences):
            temp = set()

            for output in outputs:
                if output["score"]>0.4:
                    temp.add(output["label"])

            emotions.append(temp)

        # csv 파일로 저장하기
        total_comments = pd.DataFrame({'nickname':nicknames, 'date':dates,'story_num':story_nums,
                                    'comment':sentences,'like':likes, 'emotion':emotions})
        
        print(f"Saving: {novel}")

        # 파일 이름에서 특수문자 제거
        for c in string.punctuation:
            novel = novel.replace(c, '')

        total_comments.to_csv(f"{data_dir}{novel}_comment_data.csv", index=False, encoding="utf-8")

    driver.close()  # 크롬드라이버 종료

def main(args):
    print('Start crawling...')
    crawling(args)
    print('Crawling finished!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--novel_list', default=[], nargs='+')
    parser.add_argument('--driver_dir', type=str, default="chromedriver.exe" )
    parser.add_argument('--data_dir', type=str, default="" )
    parser.add_argument('--model_name', type=str, default="searle-j/kote_for_easygoing_people" )

    args = parser.parse_args()
    print(args)

    main(args)