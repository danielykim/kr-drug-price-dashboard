## Intro
This repository contains the following modules:
- South Korea drug price data manipulation
- [Dashboard](http://kr-drug-price-dashboard.eba-p9n9y8af.ap-northeast-2.elasticbeanstalk.com/). Feel free to try it.
  - Drug price's time series in South Korea (60 months at most)
  - Drug information


## How to run it?
```
$ git clone https://github.com/danielykim/kr-drug-price-dashboard
$ pip install virtualenv
$ virtualenv venv
```

For Windows,
```
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ python application.py
```

This code was originally written for Python 3.6+.


## Data Manipulation
Data Source: [건강보험심사평가원 (HIRA) 약제급여목록표](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000)

Data Period
- Start: 2016-07-01
  - Product codes were massively revised back then
  - For your information, data is monthly updated even though it looks a date
- End: the latest posting in the source
  - This code automatically detect the latest posting, and download it.


## Contact
Daniel Y Kim, PhD
- [LinkedIn](https://www.linkedin.com/in/danielyounghokim/)
- [Homepage](http://danielykim.me/)


----


## 소개
이 저장소에서 관리하는 코드는 크게 2가지 역할을 합니다:
- `건강보험심사평가원 (HIRA)`에서 매월 제공하는 대한민국 약 가격 데이터 자동 수집 및 처리
- [대쉬보드](http://kr-drug-price-dashboard.eba-p9n9y8af.ap-northeast-2.elasticbeanstalk.com/)를 이용한 데이터 시각화
  - 대한민국 약 가격 변동 시계열(최대 60개월)
  - 제품 정보


## 데이터 처리
데이터 출처: [건강보험심사평가원 (HIRA) 약제급여목록표](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000)

데이터 수집 기간
- 시작: 2016-07-01
  - [`데이터 출처`](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000)에 이전 데이터도 있습니다만, 제품코드 처리가 더 필요하여 향후에 적용할 예정입니다.
  - 데이터는 매월 [`데이터 출처`](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000)에 올라옵니다.
- 끝: [`데이터 출처`](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000)에 있는 현재 가장 최신 데이터

이 코드를 이용하면 `시작` 기간부터 현재 가장 최신 데이터를 자동으로 가져와서 처리합니다.

`application.py` 또는 `updater.py`를 실행하면 가격 데이터를 60개월만 가지고 있도록 가장 최신 데이터를 가져와서 표를 갱신합니다.


## 문의
김영호 박사
- [링크드인](https://www.linkedin.com/in/danielyounghokim/)
- [홈페이지](http://danielykim.me/)
