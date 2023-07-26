from typing import Literal

import requests
from bs4 import BeautifulSoup


# google_translate()함수를 작성
# 3개의 인자 필요 & 형식 지정
def google_translate(
    text: str,  # 우리가 번역할 대상 문자열
    source: Literal["auto", "en", "ko"],  # 입력할 source
    target: Literal["en", "ko"],  # 바꿔줄 target
):
    # 문자열 입력 이후 좌우 공백을 제거하고 빈 문자열인지 확인
    text = text.strip()
    if not text:
        return ""

    # 크롤링할 주소로 구글 번역 모바일 사이트를 지정
    endpoint_url = "https://translate.google.com/m"

    # 파라미터를 딕셔너리로 지정하고 해당 주소로 GET요청을 할 것
    params = {
        "hl": source,
        "sl": source,
        "tl": target,
        "q": text,
        "ie": "UTF-8",
        "prev": "_m",
    }

    # 헤더도 모바일 디바이스처럼 흉내내기
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
        ),
    }

    # GET 요청 전송하기
    res = requests.get(
        endpoint_url,
        params=params,
        headers=headers,
        timeout=5,
    )
    # 응답의 상태코드가 200_ok가 아니면 예외 발생
    res.raise_for_status()

    # 응답받은 HTML문자열은 beutifulsoup의 html.parser를 통해 파싱한다.
    # 문자열 안, class=result-container안에 번역된 문자열이 존재.
    # 문자열 좌우공백제거
    soup = BeautifulSoup(res.text, "html.parser")
    translated_text = soup.select_one(".result-container").text.strip()

    return translated_text
