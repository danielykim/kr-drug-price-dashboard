## Intro
This repository contains the following modules:
- South Korea drug price data manipulation
- [Dashboard](http://kr-drug-price-dashboard.eba-p9n9y8af.ap-northeast-2.elasticbeanstalk.com/). Feel free to try it.


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
Data Source: [건강보험심사평가원 약제급여목록표](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000)

Data Period
- Start: 2016-07-01
  - Produce code was massively revised back then
  - For your information, data is monthly updated even though it looks a date
- End: the latest posting in the source
  - This code automatically detect the latest posting, and download it.


## Contact
[Daniel Y Kim, PhD](https://www.linkedin.com/in/danielyounghokim/)
