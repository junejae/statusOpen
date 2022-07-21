# StatusOpen: 독자의 댓글을 케이크처럼 쉽게 분석하는 법

## 1. Introduction

웹소설의 묘미 중 하나는 매 화마다 독자들의 댓글을 통해 작가들이 빠르게 피드백을 받을 수 있다는 점이라고 생각합니다.

하지만, 모든 댓글이 작가에게 따뜻한 것은 아닙니다.

가끔씩 출몰하는 악플은 작가들의 여린 마음에 상처를 내기 충분합니다.

이런 아픈 경험을 겪기 싫은 일부 작가들은 댓글을 보는 것을 완전히 포기하고 에이전시를 통해 댓글창의 상태를 파악하는 경우도 있습니다만, 역시 직접 보는 것보단 작가의 입장에서 받아들일 만한 정보가 적을 수 밖에 없죠.

그렇다면, 댓글 전체가 아닌 댓글에서 나오는 감정만을 종합해서 볼 수 있다면 어떨까요?

독자들이 느낀 감정을 통계적으로 관측하면서, 작가가 의도했던 감정인지 파악할 수 있지 않을까요?

StatusOpen은 상기한 아이디어를 구현하기 위해 매 화별 댓글의 종합적인 감정상태를 분석하여 보여주는 대시보드형 어플리케이션입니다.

댓글의 감정상태 분석을 위해 서울대의 KOTE 데이터셋으로 finetuning 된 KcELECTRA 모델을 활용하였습니다.

현재 카카오 페이지 스테이지 플렛폼 내의 전연령 소설 작품에 한하여 크롤링, 분석을 진행 할 수 있습니다.

## 2. How to Run

### a) 댓글 데이터 크롤링

Bash: `sh crawling.sh`

`crawling.sh` 스크립트의 argument로 크롤링을 원하는 웹소설 제목을 입력

### b) 대시보드 실행

Bash: `streamlit run dashboard.py`

이후 자동으로 브라우저를 통해 열리는 창으로 이동

또는 http://localhost:8501 로 접속

`crawling.sh` 코드 내의 NOVEL_NAME 변수로 크롤링이 완료 된 웹소설 제목을 입력

## 3. Reference

- KcELECTRA: Korean comments ELECTRA (https://github.com/Beomi/KcELECTRA)
- KOTE (Korean Online That-gul Emotions) Dataset (https://github.com/searle-j/kote)