# -*- coding: utf-8 -*-
"""
울산과학고등학교 앱 + 카카오톡 챗봇 서버 (Vercel 용 · 라즈베리파이 필요 없음)

하는 일
  급식(조식·중식·석식), 학사일정 → 나이스(NEIS)에서 자동으로 가져옴
  행사, 동아리, 홍보, 링크(기상곡 신청, 실험실 신청, 학교 위치알리미, 나이스 학부모서비스), 학교 기사 → 아래 설정에 적은 내용으로 안내

올리는 곳:  GitHub 저장소에 app.py, page.py, requirements.txt 를 올리고 Render 또는 Vercel 에 연결
           Render: Build Command = pip install -r requirements.txt / Start Command = python app.py
           Vercel: vercel.json 도 같이 올리고 Import 만 하면 됨
앱·사이트:  https://(서버 주소)   ← 들어가면 지금 시간에 맞는 급식, 학사일정, 바로가기가 나옴
챗봇 확인:  https://(서버 주소)/test?q=내일 급식
카카오 스킬 URL:  https://(서버 주소)/skill

질문을 알아듣는 순서
  1. 학생이 보낸 말에 들어 있는 낱말(급식, 동아리, 기상곡 …)
  2. 낱말로 모르면, 카카오 챗봇 관리자센터에서 그 말이 걸린 블록 이름(BLOCKS 참고)
  3. 둘 다 모르면 첫 화면

바꿔야 할 곳은 "설정" 부분(1~6번)뿐. 그 아래는 손대지 않아도 됨.
GitHub 에서 이 파일을 고치고 저장(Commit)하면 1분쯤 뒤 챗봇에 자동으로 반영됨.
"""

import base64
import hashlib
import json
import os
import sys
import threading
import re
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import requests
from flask import Flask, request, jsonify

try:  # 급식 알림(웹 푸시)에 쓰는 도구. 설치가 안 돼 있으면 알림 기능만 꺼짐
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from pywebpush import webpush, WebPushException
    PUSH_LIB = True
except Exception:
    PUSH_LIB = False

from page import PAGE, ICON_B64, SW
from mapdata import MAP

# ======================================================================
# 설정
# ======================================================================

# 1. 학교 정보
SCHOOL_NAME = "울산과학고등학교"
ATPT_CODE = "H10"          # 울산광역시교육청 코드
SCHOOL_CODE = "7480110"    # 나이스 행정표준코드. 비워 두면 학교 이름으로 자동으로 찾음

# 2. 나이스 인증키 (open.neis.go.kr 에서 무료 발급)
#    이 파일은 GitHub 에 올라가므로 인증키를 여기에 직접 적지 말 것.
#    Render 나 Vercel 의 Environment Variables 에 이름 NEIS_KEY 로 넣으면 자동으로 읽음.
#    인증키가 없어도 챗봇은 작동함.
NEIS_KEY = os.environ.get("NEIS_KEY", "").strip()

# 3. 링크 모음
#    keywords 중 하나가 학생 말에 들어 있으면 그 링크 카드가 바로 나감
#    앞에서 3개는 첫 화면 바로가기 버튼에도 나옴
LINKS = [
    {
        "title": "게시판",
        "desc": "동아리 홍보 게시판(포스터 올리기), 자유 게시판, 익명 게시판이에요. 학교 구글 계정(@ushs.hs.kr)으로 로그인해야 열려요. 카톡에서 안 열리면 오른쪽 위 메뉴에서 '다른 브라우저로 열기'를 눌러 보세요.",
        "url": "https://script.google.com/a/macros/ushs.hs.kr/s/AKfycby2gOXvtxIrsN8IEo8oOp2D0up47iO7iImfhoiqHPYY-iCouFVPZY330BDXmFn_7t0A/exec",
        "button": "게시판 열기",
        "keywords": ["게시판", "자유게시판", "자유 게시판", "홍보 게시판", "포스터", "글쓰기", "익명", "고민"],
    },
    {
        "title": "기상곡 신청",
        "desc": "기상곡을 신청할 수 있어요.",
        "url": "https://onair-three-beta.vercel.app/",
        "by": "제작: On-Air 시관 관리부 1학년 김무성, 김예영",
        "button": "신청하러 가기",
        "keywords": ["기상곡", "기상송", "기상음악", "노래신청", "노래 신청"],
    },
    {
        "title": "화학실·생물실 신청",
        "desc": "화학실과 생물실 사용을 예약해요. 학교 계정으로 로그인해야 해요.",
        "url": "https://ushs-lab.vercel.app/?next=/book",
        "by": "제작 동아리: ACE, LICHEM, AiBE, LAYOUT",
        "button": "예약하러 가기",
        "keywords": ["화학실", "생물실", "실험실", "실험실 신청", "실험실 예약"],
    },
    {
        "title": "교직원 위치 찾기",
        "desc": "선생님 이름을 넣으면 계신 곳의 위치와 실 번호를 캠퍼스 조감도에서 보여 줘요.",
        "url": "https://bejewelled-lokum-e67e6a.netlify.app/",
        "button": "찾으러 가기",
        "keywords": ["교직원 찾기", "교직원 위치", "선생님 위치", "선생님 찾기", "쌤 위치", "쌤 찾기", "교사 위치"],
    },
    {
        "title": "교무실별 교직원 검색",
        "desc": "실 번호(예: A104)를 넣으면 그 교무실의 위치와 계신 선생님을 보여 줘요.",
        "url": "https://incomparable-nougat-d0f748.netlify.app/",
        "button": "검색하러 가기",
        "keywords": ["교무실별", "교무실 검색", "교무실 선생님", "호실 검색", "실번호", "실 번호", "공간 검색"],
    },
    {
        "title": "학교 위치알리미",
        "desc": "학교 구글 계정(@ushs.hs.kr)으로 로그인해야 열려요. 카톡에서 안 열리면 오른쪽 위 메뉴에서 '다른 브라우저로 열기'를 눌러 보세요.",
        "url": "https://script.google.com/a/macros/ushs.hs.kr/s/AKfycbwBclQ5njll0mmySd74avm2zbHOMqZ4dqKfgveHE897OXVTXLfr7MhkPxKNPkxLkRJSbw/exec",
        "button": "열기",
        "by": "제작: 이병석 선생님",
        "keywords": ["위치알리미", "위치 알리미", "학교 위치", "위치"],
    },
    {
        "title": "나이스 학부모서비스",
        "desc": "현장체험학습 신청서 등 각종 신청과 조회를 할 수 있어요.",
        "url": "https://parents.neis.go.kr",
        "button": "열기",
        "keywords": ["학부모서비스", "학부모 서비스", "현장체험", "체험학습", "신청서", "나이스"],
    },
]

# 3-1. 링크 모음 (앱 맨 아래 "링크 모음"과 챗봇 "링크 모음"에 나옴)
#    group 이 같은 것끼리 묶여 나옴. 한 줄 추가하면 바로 늘어남. "학교 홈페이지"는 나이스에서 자동으로 찾아 넣음
#    sub 를 적으면 그 묶음 안에서 다시 작은 갈래(과목, 기능)로 나뉨. 갈래마다 앞쪽 몇 개만 먼저 보이고
#    나머지는 "더 알아보기"를 눌러야 나오므로, 많이 쓰는 것을 앞에 둘 것
MORE_LINKS = [
    {"group": "AI", "sub": "대화·질문", "title": "베이즈 AI (BAZE)", "url": "https://baze.co/"},
    {"group": "AI", "sub": "대화·질문", "title": "ChatGPT", "url": "https://chatgpt.com"},
    {"group": "AI", "sub": "대화·질문", "title": "Claude", "url": "https://claude.ai"},
    {"group": "AI", "sub": "대화·질문", "title": "Gemini", "url": "https://gemini.google.com"},
    {"group": "AI", "sub": "대화·질문", "title": "Copilot", "url": "https://copilot.microsoft.com"},
    {"group": "AI", "sub": "대화·질문", "title": "뤼튼", "url": "https://wrtn.ai"},
    {"group": "AI", "sub": "대화·질문", "title": "Grok", "url": "https://grok.com"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "Perplexity", "url": "https://www.perplexity.ai"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "Consensus", "url": "https://consensus.app"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "Elicit", "url": "https://elicit.com"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "SciSpace", "url": "https://scispace.com"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "라이너", "url": "https://getliner.com"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "Connected Papers", "url": "https://www.connectedpapers.com"},
    {"group": "AI", "sub": "검색·논문 조사", "title": "Research Rabbit", "url": "https://www.researchrabbit.ai"},
    {"group": "AI", "sub": "자료 정리·요약", "title": "NotebookLM", "url": "https://notebooklm.google.com"},
    {"group": "AI", "sub": "자료 정리·요약", "title": "릴리스 AI", "url": "https://lilys.ai"},
    {"group": "AI", "sub": "자료 정리·요약", "title": "ChatPDF", "url": "https://www.chatpdf.com"},
    {"group": "AI", "sub": "자료 정리·요약", "title": "클로바노트", "url": "https://clovanote.naver.com"},
    {"group": "AI", "sub": "번역·영어 글쓰기", "title": "DeepL 번역", "url": "https://www.deepl.com"},
    {"group": "AI", "sub": "번역·영어 글쓰기", "title": "파파고", "url": "https://papago.naver.com"},
    {"group": "AI", "sub": "번역·영어 글쓰기", "title": "DeepL Write", "url": "https://www.deepl.com/write"},
    {"group": "AI", "sub": "번역·영어 글쓰기", "title": "Grammarly", "url": "https://www.grammarly.com"},
    {"group": "AI", "sub": "번역·영어 글쓰기", "title": "QuillBot", "url": "https://quillbot.com"},
    {"group": "AI", "sub": "코딩", "title": "GitHub Copilot", "url": "https://github.com/features/copilot"},
    {"group": "AI", "sub": "코딩", "title": "Google AI Studio", "url": "https://aistudio.google.com"},
    {"group": "AI", "sub": "코딩", "title": "Cursor", "url": "https://cursor.com"},
    {"group": "AI", "sub": "코딩", "title": "Replit", "url": "https://replit.com"},
    {"group": "AI", "sub": "수학·공부", "title": "콴다", "url": "https://qanda.ai"},
    {"group": "AI", "sub": "수학·공부", "title": "Symbolab", "url": "https://www.symbolab.com"},
    {"group": "AI", "sub": "수학·공부", "title": "Khanmigo", "url": "https://www.khanmigo.ai"},
    {"group": "AI", "sub": "발표·디자인", "title": "Gamma", "url": "https://gamma.app"},
    {"group": "AI", "sub": "발표·디자인", "title": "Canva", "url": "https://www.canva.com"},
    {"group": "AI", "sub": "발표·디자인", "title": "미리캔버스", "url": "https://www.miricanvas.com"},
    {"group": "AI", "sub": "발표·디자인", "title": "Napkin AI", "url": "https://www.napkin.ai"},
    {"group": "AI", "sub": "이미지·영상·음성", "title": "Adobe Firefly", "url": "https://firefly.adobe.com"},
    {"group": "AI", "sub": "이미지·영상·음성", "title": "Midjourney", "url": "https://www.midjourney.com"},
    {"group": "AI", "sub": "이미지·영상·음성", "title": "Runway", "url": "https://runwayml.com"},
    {"group": "AI", "sub": "이미지·영상·음성", "title": "Vrew", "url": "https://vrew.ai"},
    {"group": "AI", "sub": "이미지·영상·음성", "title": "Suno", "url": "https://suno.com"},
    {"group": "AI", "sub": "이미지·영상·음성", "title": "ElevenLabs", "url": "https://elevenlabs.io"},
    {"group": "학교·행정", "title": "나이스플러스", "url": "https://www.neisplus.kr"},
    {"group": "학교·행정", "title": "나이스 대국민서비스", "url": "https://www.neis.go.kr"},
    {"group": "학교·행정", "title": "울산광역시교육청", "url": "https://www.use.go.kr"},
    {"group": "학교·행정", "title": "학교알리미", "url": "https://www.schoolinfo.go.kr"},
    {"group": "학교·행정", "title": "정부24", "url": "https://www.gov.kr"},
    {"group": "입시·학습", "title": "대입정보포털 어디가", "url": "https://www.adiga.kr"},
    {"group": "입시·학습", "title": "KAIST 입학", "url": "https://admission.kaist.ac.kr"},
    {"group": "입시·학습", "title": "UNIST", "url": "https://www.unist.ac.kr"},
    {"group": "입시·학습", "title": "POSTECH", "url": "https://www.postech.ac.kr"},
    {"group": "입시·학습", "title": "서울대 입학", "url": "https://admission.snu.ac.kr"},
    {"group": "입시·학습", "title": "EBSi", "url": "https://www.ebsi.co.kr"},
    {"group": "탐구·연구", "sub": "물리", "title": "arXiv", "url": "https://arxiv.org"},
    {"group": "탐구·연구", "sub": "물리", "title": "HyperPhysics", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/hframe.html"},
    {"group": "탐구·연구", "sub": "물리", "title": "NIST 물리 상수", "url": "https://physics.nist.gov/cuu/Constants/"},
    {"group": "탐구·연구", "sub": "물리", "title": "파인만 물리학 강의", "url": "https://www.feynmanlectures.caltech.edu"},
    {"group": "탐구·연구", "sub": "물리", "title": "Falstad 회로 시뮬레이터", "url": "https://www.falstad.com/circuit/"},
    {"group": "탐구·연구", "sub": "물리", "title": "NASA ADS 논문 검색", "url": "https://ui.adsabs.harvard.edu"},
    {"group": "탐구·연구", "sub": "물리", "title": "APS Physics", "url": "https://physics.aps.org"},
    {"group": "탐구·연구", "sub": "물리", "title": "한국물리학회", "url": "https://www.kps.or.kr"},
    {"group": "탐구·연구", "sub": "화학", "title": "PubChem", "url": "https://pubchem.ncbi.nlm.nih.gov"},
    {"group": "탐구·연구", "sub": "화학", "title": "Ptable 주기율표", "url": "https://ptable.com"},
    {"group": "탐구·연구", "sub": "화학", "title": "NIST 화학 WebBook", "url": "https://webbook.nist.gov/chemistry/"},
    {"group": "탐구·연구", "sub": "화학", "title": "MSDS 검색 (안전보건공단)", "url": "https://msds.kosha.or.kr"},
    {"group": "탐구·연구", "sub": "화학", "title": "ChemSpider", "url": "https://www.chemspider.com"},
    {"group": "탐구·연구", "sub": "화학", "title": "MolView 분자 모형", "url": "https://molview.org"},
    {"group": "탐구·연구", "sub": "화학", "title": "대한화학회", "url": "https://www.kcsnet.or.kr"},
    {"group": "탐구·연구", "sub": "생물", "title": "NCBI", "url": "https://www.ncbi.nlm.nih.gov"},
    {"group": "탐구·연구", "sub": "생물", "title": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov"},
    {"group": "탐구·연구", "sub": "생물", "title": "BLAST", "url": "https://blast.ncbi.nlm.nih.gov/Blast.cgi"},
    {"group": "탐구·연구", "sub": "생물", "title": "UniProt", "url": "https://www.uniprot.org"},
    {"group": "탐구·연구", "sub": "생물", "title": "RCSB PDB 단백질 구조", "url": "https://www.rcsb.org"},
    {"group": "탐구·연구", "sub": "생물", "title": "Ensembl", "url": "https://www.ensembl.org"},
    {"group": "탐구·연구", "sub": "생물", "title": "bioRxiv", "url": "https://www.biorxiv.org"},
    {"group": "탐구·연구", "sub": "생물", "title": "국가생물종지식정보시스템", "url": "https://www.nature.go.kr"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "기상자료개방포털", "url": "https://data.kma.go.kr"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "천문우주지식정보", "url": "https://astro.kasi.re.kr"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "USGS 지진 정보", "url": "https://earthquake.usgs.gov"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "NASA Worldview 위성 영상", "url": "https://worldview.earthdata.nasa.gov"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "earth 바람·해류 지도", "url": "https://earth.nullschool.net"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "Stellarium 웹 별자리", "url": "https://stellarium-web.org"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "바다누리 해양정보", "url": "https://www.khoa.go.kr/oceangrid/"},
    {"group": "탐구·연구", "sub": "지구과학", "title": "SDSS SkyServer", "url": "https://skyserver.sdss.org"},
    {"group": "탐구·연구", "sub": "수학", "title": "OEIS 수열 사전", "url": "https://oeis.org"},
    {"group": "탐구·연구", "sub": "수학", "title": "MathWorld 수학 사전", "url": "https://mathworld.wolfram.com"},
    {"group": "탐구·연구", "sub": "수학", "title": "arXiv 수학", "url": "https://arxiv.org/archive/math"},
    {"group": "탐구·연구", "sub": "수학", "title": "3Blue1Brown", "url": "https://www.3blue1brown.com"},
    {"group": "탐구·연구", "sub": "수학", "title": "Art of Problem Solving", "url": "https://artofproblemsolving.com"},
    {"group": "탐구·연구", "sub": "수학", "title": "Project Euler", "url": "https://projecteuler.net"},
    {"group": "탐구·연구", "sub": "수학", "title": "대한수학회", "url": "https://www.kms.or.kr"},
    {"group": "탐구·연구", "sub": "정보", "title": "GitHub", "url": "https://github.com"},
    {"group": "탐구·연구", "sub": "정보", "title": "Google Colab", "url": "https://colab.research.google.com"},
    {"group": "탐구·연구", "sub": "정보", "title": "Kaggle", "url": "https://www.kaggle.com"},
    {"group": "탐구·연구", "sub": "정보", "title": "Hugging Face", "url": "https://huggingface.co"},
    {"group": "탐구·연구", "sub": "정보", "title": "solved.ac", "url": "https://solved.ac"},
    {"group": "탐구·연구", "sub": "정보", "title": "Codeforces", "url": "https://codeforces.com"},
    {"group": "탐구·연구", "sub": "정보", "title": "프로그래머스", "url": "https://programmers.co.kr"},
    {"group": "탐구·연구", "sub": "정보", "title": "파이썬 문서", "url": "https://docs.python.org/ko/3/"},
    {"group": "탐구·연구", "sub": "정보", "title": "MDN 웹 문서", "url": "https://developer.mozilla.org/ko/"},
    {"group": "탐구·연구", "sub": "정보", "title": "한국정보올림피아드", "url": "https://koi.or.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "RISS 학술연구정보", "url": "https://www.riss.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "구글 학술검색", "url": "https://scholar.google.com"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "ScienceON", "url": "https://scienceon.kisti.re.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "DBpia", "url": "https://www.dbpia.co.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "KCI 한국학술지인용색인", "url": "https://www.kci.go.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "Semantic Scholar", "url": "https://www.semanticscholar.org"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "KOSIS 국가통계", "url": "https://kosis.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "공공데이터포털", "url": "https://www.data.go.kr"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "Our World in Data", "url": "https://ourworldindata.org"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "Overleaf (LaTeX)", "url": "https://www.overleaf.com"},
    {"group": "탐구·연구", "sub": "기타 (논문·통계·글쓰기)", "title": "Zotero 참고문헌 관리", "url": "https://www.zotero.org"},
    {"group": "영어", "title": "북크리에이터", "url": "https://app.bookcreator.com"},
    {"group": "영어", "title": "Question Lab", "url": "https://script.google.com/a/macros/ushs.hs.kr/s/AKfycbyfR2ayRgzAj9_mDfPeIbhlGeFllizeezZZsnaeSOsPo68M9MHXRQ9UdCloOwjqksMm/exec"},
    {"group": "도구", "title": "Desmos 그래프", "url": "https://www.desmos.com/calculator"},
    {"group": "도구", "title": "GeoGebra", "url": "https://www.geogebra.org"},
    {"group": "도구", "title": "WolframAlpha", "url": "https://www.wolframalpha.com"},
    {"group": "도구", "title": "PhET 시뮬레이션", "url": "https://phet.colorado.edu/ko/"},
    {"group": "도구", "title": "백준", "url": "https://www.acmicpc.net"},
    {"group": "도구", "title": "기상청 날씨누리", "url": "https://www.weather.go.kr"},
]

# 3-3. AI 커넥터 (Claude·ChatGPT 같은 AI에 연결해서 쓰는 도구. 주소를 눌러 들어가는 사이트가 아니라, AI 설정에 붙여 넣는 주소)
CONNECTORS = [
    {
        "title": "울곽 시약 검색",
        "desc": "학교에 있는 시약의 위치, 시약장별 목록, MSDS를 AI에게 물어볼 수 있어요.",
        "url": "https://ushs-lab-mcp.vercel.app/mcp",
        "by": "MCP 배포: 하성준, 박승준",
        "how": [
            "Claude: 왼쪽 아래 프로필 → 설정 → 커넥터 → + 버튼 → 사용자 지정 커넥터 추가 → 이름을 적고 주소 칸에 위 주소를 붙여 넣기",
            "ChatGPT(유료 계정): 설정 → 앱 및 커넥터 → 고급 설정에서 개발자 모드 켜기 → 만들기 → 위 주소 붙여 넣고 인증은 '없음'",
        ],
        "examples": ["질산은, 아세트산 어디 있어?", "자료실-8에 뭐가 들어 있어?", "벤젠 MSDS 보여줘. 보호구 뭐 써야 해?"],
        "note": "MSDS는 참고 자료예요. 용기 라벨의 CAS번호가 화면의 번호와 같은지 꼭 대조하세요. AI 답변은 틀릴 수 있고 목록에 빠진 시약이 있을 수 있어요.",
    },
]

# 3-4. 학교 지도 제작자, 급식 알림 시각
MAP_BY = "학교 층별 안내판을 따라 그린 지도"
PUSH_SLOTS = [  # (급식 코드, 이름, 알림 보내기 시작 시각, 이 시각이 지나면 그 끼니 알림은 안 보냄)
    ("1", "아침", 7.0, 7.75),
    ("2", "점심", 12.0, 12.75),
    ("3", "저녁", 18.0, 18.75),
]
# 알림 구독 묶음(암호화됨)이 보관되는 곳. 서버가 켜질 때 여기서 스스로 복구함 (저장소 이름이 바뀌면 같이 바꿀 것)
PUSH_BACKUP_URL = "https://raw.githubusercontent.com/jaehuk091029-dot/ushs-student/push-data/subs.txt"

# 3-2. 학교 기사 (구글 뉴스에서 아래 낱말로 검색해 제목에 그 낱말이 들어간 기사만 보여 줌)
NEWS_WORDS = ["울산과학고", "울산과고"]
NEWS_COUNT = 8             # 보여 줄 기사 수

# 4. 동아리
#    category 는 창체 / 학술 / 자율 / 유네스코. 자율 동아리는 sub 로 한 번 더 나눔(예체능 / 학술 / 취미 / 봉사·교류). 10개가 넘으면 챗봇에서는 이름 목록으로 보여 주고, 이름을 보내면 자세히 알려 줌
#    url 은 없으면 "" 로 두기
CLUBS = [
    {"name": "수학탐구(FORMAT)", "category": "창체", "desc": "지도교사: 이영희, 전상균 · 21명", "url": ""},
    {"name": "수학체험(MAGIC)", "category": "창체", "desc": "지도교사: 김다은, 김지혜 · 19명", "url": ""},
    {"name": "물리실험반(EMP)", "category": "창체", "desc": "지도교사: 이승주, 김해일, 김혜경 · 19명", "url": ""},
    {"name": "화학실험(ACE)", "category": "창체", "desc": "지도교사: 김현아, 박성대, 정혜영 · 20명", "url": ""},
    {"name": "생물실험반(AIBE)", "category": "창체", "desc": "지도교사: 송정기, 최선, 이희성 · 21명", "url": ""},
    {"name": "물리탐구반(E.T.F)", "category": "창체", "desc": "지도교사: 염성식 · 9명", "url": ""},
    {"name": "화학생명융합반(CBC)", "category": "창체", "desc": "지도교사: 오덕기, 박미숙 · 14명", "url": ""},
    {"name": "정보과학(lay-out)반", "category": "창체", "desc": "지도교사: 이병석, 박정호 · 14명", "url": ""},
    {"name": "인공지능연구반(ADEUS)", "category": "창체", "desc": "지도교사: 김재원, 황대호 · 15명", "url": ""},
    {"name": "인문독서연구반(PHILOBIBLIO)", "category": "창체", "desc": "지도교사: 진현화 · 9명", "url": ""},
    {"name": "융합탐구반(SIC)", "category": "창체", "desc": "지도교사: 하지현 · 10명", "url": ""},
    {"name": "융합공학탐구반(AERO)", "category": "창체", "desc": "지도교사: 임윤성, 천세은 · 15명", "url": ""},
    {"name": "화학실험(LICHEM)", "category": "창체", "desc": "지도교사: 구선희, 전수미 · 20명", "url": ""},
    {"name": "수학학술(EXPONENTIAL)", "category": "학술", "desc": "지도교사: 오덕기 · 15명", "url": ""},
    {"name": "물리학술(INFINITY)", "category": "학술", "desc": "지도교사: 김해일 · 11명", "url": ""},
    {"name": "화학학술(CHEMICORE)", "category": "학술", "desc": "지도교사: 구선희 · 20명", "url": ""},
    {"name": "생명학술(BSTAR)", "category": "학술", "desc": "지도교사: 최선 · 11명", "url": ""},
    {"name": "정보학술(STUDIO)", "category": "학술", "desc": "지도교사: 이병석 · 16명", "url": ""},
    {"name": "천문학술동아리(LuceVista)", "category": "학술", "desc": "지도교사: 황대호 · 13명", "url": ""},
    {"name": "Ensemble(오케스트라)", "category": "자율", "sub": "예체능", "desc": "지도교사: 권오준 · 21명", "url": ""},
    {"name": "USb(밴드부)", "category": "자율", "sub": "예체능", "desc": "지도교사: 이지선 · 22명", "url": ""},
    {"name": "C-mile(댄스부)", "category": "자율", "sub": "예체능", "desc": "지도교사: 임윤성 · 16명", "url": ""},
    {"name": "P.A.C.(흑인힙합동아리)", "category": "자율", "sub": "예체능", "desc": "지도교사: 이지선 · 26명", "url": ""},
    {"name": "team WOD(헬스부)", "category": "자율", "sub": "예체능", "desc": "지도교사: 박성대 · 6명", "url": ""},
    {"name": "Gradient(수학물리융합반)", "category": "자율", "sub": "학술", "desc": "지도교사: 오덕기 · 21명", "url": ""},
    {"name": "MRC(해부)", "category": "자율", "sub": "학술", "desc": "지도교사: 최선 · 16명", "url": ""},
    {"name": "Packet(해킹)", "category": "자율", "sub": "학술", "desc": "지도교사: 이병석 · 10명", "url": ""},
    {"name": "CORAL(수생학)", "category": "자율", "sub": "학술", "desc": "지도교사: 최선 · 30명", "url": ""},
    {"name": "공학반(The Gear)", "category": "자율", "sub": "학술", "desc": "지도교사: 이승주 · 9명", "url": ""},
    {"name": "창업활동(ADAGIO)", "category": "자율", "sub": "취미", "desc": "지도교사: 전상균 · 24명", "url": ""},
    {"name": "C.O.T.B(체스)", "category": "자율", "sub": "취미", "desc": "지도교사: 최선 · 18명", "url": ""},
    {"name": "아름다운 카페(카페활동)", "category": "자율", "sub": "취미", "desc": "지도교사: 하지현 · 11명", "url": ""},
    {"name": "On-Air(방송반)", "category": "자율", "sub": "취미", "desc": "지도교사: 이병석 · 17명", "url": ""},
    {"name": "더불어 사는 세상(고양이 돌봄)", "category": "자율", "sub": "봉사·교류", "desc": "지도교사: 하지현 · 30명", "url": ""},
    {"name": "국제교류코랩", "category": "자율", "sub": "봉사·교류", "desc": "일본과 국제교류를 하는 동아리 · 지도교사: 이영희 · 27명", "url": ""},
    {"name": "온정나눔동아리", "category": "유네스코", "desc": "도서관에서 초등학생들에게 수업 봉사를 하는 동아리 · 지도교사: 전상균 · 18명", "url": ""},
]

# 5. 홍보 (학생회 공지, 대회 안내, 모집 공고 등)
#    image 는 https 로 시작하는 사진 주소. 모든 항목에 사진이 있으면 사진 카드로 나감
PROMO = [
    {"title": "홍보 제목 예시", "desc": "내용을 짧게", "image": "", "url": "", "button": "자세히 보기"},
]

# 6. 행사 (나이스 학사일정에 없는 학교 자체 행사)
#    date 는 "2026-12-01" 처럼 적기. 지난 행사는 자동으로 빠짐
EVENTS = [
    {"date": "2026-12-01", "title": "행사 이름 예시", "desc": "장소, 시간, 준비물", "url": "", "button": "자세히 보기"},
]

# 기타
NEXT_DAY_AFTER = 19.5      # 이 시각(19시 30분) 이후에 그냥 "급식"이라고 하면 내일 급식을 보여 줌
BREAKFAST_UNTIL = 8.5      # 앱: 이 시각(8시 30분)까지는 아침 급식을 먼저 보여 줌
LUNCH_UNTIL = 13.5         # 앱: 이 시각(13시 30분)까지는 점심, 그 뒤 NEXT_DAY_AFTER 까지는 저녁, 그 뒤는 내일 아침
APP_SHORT_NAME = "울산과학고"  # 휴대폰 홈 화면에 추가했을 때 아이콘 아래 나오는 이름
APP_URL = "https://ushs-student.onrender.com"   # 앱(사이트) 주소. 챗봇 첫 화면의 '앱 열기' 버튼이 여기로 감
SCHEDULE_DAYS = 30         # 학사일정 기본 조회 기간(일)
NEIS_TIMEOUT = 3           # 나이스 응답 대기(초). 카카오는 5초 안에 답해야 함

# ======================================================================
# 여기부터는 수정하지 않아도 됨
# ======================================================================

try:
    sys.stdout.reconfigure(line_buffering=True)   # print 한 내용이 서버 기록에 바로 보이게 함
except Exception:
    pass

app = Flask(__name__)
app.json.ensure_ascii = False
KST = ZoneInfo("Asia/Seoul")
WEEK = "월화수목금토일"
cache = {}  # 같은 질문은 30분 동안 나이스에 다시 묻지 않음


# ---------- 기본 도구 ----------

def squash(s):
    return re.sub(r"\s+", "", s or "")


def today():
    return datetime.now(KST).date()


def neis(service, params, with_school=True):
    q = {"Type": "json", "pIndex": 1, "pSize": 100}
    q.update(params)
    if with_school:
        q["ATPT_OFCDC_SC_CODE"] = ATPT_CODE
        q["SD_SCHUL_CODE"] = school_code()
    if NEIS_KEY:
        q["KEY"] = NEIS_KEY
    key = service + str(sorted(q.items()))
    hit = cache.get(key)
    if hit and time.time() - hit[0] < 1800:
        return hit[1]
    try:
        r = requests.get("https://open.neis.go.kr/hub/" + service, params=q, timeout=NEIS_TIMEOUT)
        data = r.json()
    except Exception:
        if hit:
            return hit[1]  # 나이스가 느리거나 멈췄으면 전에 받아 둔 내용이라도 보여 줌
        raise
    rows = []
    if service in data and len(data[service]) > 1:
        rows = data[service][1].get("row", [])
    cache[key] = (time.time(), rows)
    return rows


def school_code():
    global SCHOOL_CODE
    if not SCHOOL_CODE:
        rows = neis("schoolInfo", {"ATPT_OFCDC_SC_CODE": ATPT_CODE, "SCHUL_NM": SCHOOL_NAME}, with_school=False)
        for r in rows:
            if r.get("SCHUL_NM") == SCHOOL_NAME:
                SCHOOL_CODE = r["SD_SCHUL_CODE"]
                print("[나이스] " + SCHOOL_NAME + " 학교코드 = " + SCHOOL_CODE)
    return SCHOOL_CODE


def md_label(d):
    return f"{d.month}월 {d.day}일({WEEK[d.weekday()]})"


def short_label(ymd):
    d = datetime.strptime(str(ymd)[:8], "%Y%m%d").date()
    return f"{d.month}/{d.day}({WEEK[d.weekday()]})"


# ---------- 카카오 응답 모양 만들기 ----------

def reply(outputs, quick=None):
    return {
        "version": "2.0",
        "template": {"outputs": outputs[:3], "quickReplies": quick if quick is not None else main_quick()},
    }


def simple_text(text):
    return {"simpleText": {"text": str(text)[:1000]}}


def card(title, desc, buttons=None):
    c = {"title": str(title)[:50], "description": str(desc or "")[:230]}
    if buttons:
        c["buttons"] = buttons[:3]
    return c


def link_button(label, url):
    return {"action": "webLink", "label": str(label)[:14], "webLinkUrl": url}


def carousel(kind, items):
    return {"carousel": {"type": kind, "items": items[:10]}}


def quick(label, text=None):
    return {"label": str(label)[:14], "action": "message", "messageText": text or label}


def live_links():
    return [l for l in LINKS if l.get("url")]   # 주소가 비어 있는 링크는 숨김


def main_quick():
    labels = ["오늘 급식", "내일 급식", "급식 알림", "학사일정", "학교 기사", "동아리"]
    if any(not is_sample(e.get("title", "")) for e in EVENTS):
        labels.append("행사")
    if any(not is_sample(p.get("title", "")) for p in PROMO):
        labels.append("홍보")
    base = [quick(t) for t in labels]
    links = [quick(l["title"]) for l in live_links()[:2]]
    return (base + links + [quick("링크 모음")])[:10]


def split_text(text, size=990):
    parts, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > size:
            parts.append(cur)
            cur = line
        else:
            cur = cur + "\n" + line if cur else line
    if cur:
        parts.append(cur)
    return [simple_text(p) for p in parts[:3]]


# ---------- 무슨 질문인지 알아내기 ----------

# 카카오 챗봇 관리자센터의 블록 이름 → 할 일
# 블록 이름을 바꿨다면 여기 왼쪽 이름도 똑같이 바꿔 줘야 함
BLOCKS = {
    "웰컴 블록": "home",
    "처음으로": "home",
    "급식": "meal",
    "학사일정": "schedule",
    "행사": "events",
    "동아리": "clubs",
    "홍보": "promo",
    "링크 모음": "links",
    "급식 알림": "noti",
    "학교 기사": "news",
    "AI 사이트": "ai",
    "시약 검색": "conn",
    "학교 지도": "map",
    "학교 위치알리미": "link:학교 위치알리미",
    "현장체험학습 신청서": "link:나이스 학부모서비스",
    "나이스 학부모서비스": "link:나이스 학부모서비스",
    "기상곡 신청": "link:기상곡 신청",
    "실험실 신청": "link:화학실·생물실 신청",
    "위치알리미": "link:학교 위치알리미",
}


def by_words(utter):
    u = squash(utter)
    low = u.lower()
    if ("동아리" in u and "게시판" not in u) or any(low in club_keys(c) for c in CLUBS):
        return "clubs"
    for l in live_links():
        words = [l["title"]] + l.get("keywords", [])
        if any(squash(w) in u for w in words):
            return "link:" + l["title"]
    if re.search(r"알림|알람", u):
        return "noti"
    if re.search(r"기사|뉴스|신문|보도", u):
        return "news"
    if re.search(r"시약|커넥터|mcp|msds", u, re.I):
        return "conn"
    if re.search(r"(?<![a-z])ai(?![a-z])|인공지능|gpt|지피티|제미나이|클로드|베이즈", u, re.I):
        return "ai"
    if re.search(r"급식|식단|밥|조식|중식|석식|아침|점심|저녁", u):
        return "meal"
    if "동아리" in u:
        return "clubs"
    if re.search(r"홍보|소식|공지|모집", u):
        return "promo"
    if re.search(r"행사|이벤트", u):
        return "events"
    if re.search(r"학사|일정|시험|고사|방학|휴업", u):
        return "schedule"
    if re.search(r"링크|바로가기", u):
        return "links"
    for name in sorted(ROOMS, key=len, reverse=True):
        if name in u.lower():
            return "room:" + name
    if any(k in low for c in CLUBS for k in club_keys(c)):
        return "clubs"
    if re.search(r"지도|약도|몇층|어디", u):
        return "map"
    if re.search(r"메뉴|처음|도움|시작|안녕|하이", u):
        return "home"
    return ""


def handle(utter, block=""):
    what = by_words(utter) or BLOCKS.get((block or "").strip(), "")
    if what.startswith("link:"):
        for l in live_links():
            if l["title"] == what[5:]:
                return one_link(l)
    if what == "noti":
        return noti()
    if what == "news":
        return news()
    if what == "conn":
        return connectors()
    if what.startswith("room:"):
        return room(what[5:])
    if what == "map":
        return school_map()
    if what == "ai":
        return ai_links()
    if what == "meal":
        return meal(utter)
    if what == "schedule":
        return schedule(utter)
    if what == "events":
        return events(utter)
    if what == "clubs":
        return clubs(utter)
    if what == "promo":
        return promo()
    if what == "links":
        return all_links()
    return home(unknown=(what != "home"))


# ---------- 급식 ----------

def meal_kind(u):
    if re.search(r"조식|아침", u):
        return "1"
    if re.search(r"중식|점심", u):
        return "2"
    if re.search(r"석식|저녁", u):
        return "3"
    return ""


def parse_day(utter, rollover):
    u = squash(utter)
    t = today()
    if "모레" in u:
        return t + timedelta(days=2), "모레"
    if "내일" in u:
        return t + timedelta(days=1), "내일"
    if "어제" in u:
        return t - timedelta(days=1), "어제"
    if "오늘" in u:
        return t, "오늘"
    m = re.search(r"(\d{1,2})[/.월](\d{1,2})", u)
    if m:
        mon, day = int(m.group(1)), int(m.group(2))
        try:
            d = t.replace(month=mon, day=day)
            if d < t - timedelta(days=180):
                d = d.replace(year=t.year + 1)
            elif d > t + timedelta(days=180):
                d = d.replace(year=t.year - 1)
            return d, None
        except ValueError:
            pass
    m = re.search(r"(다음주|담주|이번주)?([월화수목금토일])요일", u)
    if m:
        diff = WEEK.index(m.group(2)) - t.weekday()
        if m.group(1) in ("다음주", "담주"):
            diff += 7
        elif not m.group(1) and diff < 0:
            diff += 7
        return t + timedelta(days=diff), None
    if rollover:
        now = datetime.now(KST)
        if now.hour + now.minute / 60 >= NEXT_DAY_AFTER:
            return t + timedelta(days=1), "내일"
    return t, "오늘"


def menu_items(dish):
    items = []
    for x in re.split(r"<br\s*/?>", dish or ""):
        x = re.sub(r"\s*\([\d.\s]+\)", "", x).replace("*", "").strip()
        if x:
            items.append(x)
    return items


def clean_menu(dish):
    return "\n".join("· " + x for x in menu_items(dish))


def meal(utter):
    kind = meal_kind(squash(utter))
    day, label = parse_day(utter, rollover=not kind)
    params = {"MLSV_YMD": day.strftime("%Y%m%d")}
    if kind:
        params["MMEAL_SC_CODE"] = kind
    rows = neis("mealServiceDietInfo", params)
    head = (label + " · " if label else "") + md_label(day)
    prev, nxt = day - timedelta(days=1), day + timedelta(days=1)
    q = [
        quick(f"◀ {prev.month}/{prev.day}", f"{prev.month}/{prev.day} 급식"),
        quick(f"{nxt.month}/{nxt.day} ▶", f"{nxt.month}/{nxt.day} 급식"),
        quick("오늘 급식"), quick("내일 급식"), quick("처음으로"),
    ]
    if not rows:
        return reply([simple_text(head + " 급식 정보가 없어요.\n주말·공휴일이거나 아직 식단이 올라오지 않았을 수 있어요.")], q)
    rows = sorted(rows, key=lambda r: r.get("MMEAL_SC_CODE", ""))
    outs = []
    for r in rows[:3]:
        cal = "\n\n(" + r["CAL_INFO"] + ")" if r.get("CAL_INFO") else ""
        outs.append(simple_text(f"🍚 {head} {r.get('MMEAL_SC_NM', '')}\n\n{clean_menu(r.get('DDISH_NM'))}{cal}"))
    return reply(outs, q)


# ---------- 학사일정 ----------

def schedule(utter, intro=""):
    t = today()
    start, end = t, t + timedelta(days=SCHEDULE_DAYS)
    title = f"앞으로 {SCHEDULE_DAYS}일 학사일정"
    u = squash(utter)
    mon = 0
    m = re.search(r"(\d{1,2})월", u)
    if m and 1 <= int(m.group(1)) <= 12:
        mon = int(m.group(1))
    elif "다음달" in u or "담달" in u:
        mon = t.month % 12 + 1
    elif "이번달" in u:
        mon = t.month
    if mon:
        # 학년도(3월~다음 해 2월) 기준으로 연도를 정함
        if t.month >= 3:
            year = t.year + 1 if mon <= 2 else t.year
        else:
            year = t.year - 1 if mon >= 3 else t.year
        start = datetime(year, mon, 1).date()
        end = (datetime(year + (mon == 12), mon % 12 + 1, 1) - timedelta(days=1)).date()
        title = f"{year}년 {mon}월 학사일정"
    rows = neis("SchoolSchedule", {"AA_FROM_YMD": start.strftime("%Y%m%d"), "AA_TO_YMD": end.strftime("%Y%m%d")})
    lines, seen = [], set()
    for r in sorted(rows, key=lambda r: r.get("AA_YMD", "")):
        name = (r.get("EVENT_NM") or "").strip()
        if not name or "토요휴업일" in name:
            continue
        line = short_label(r["AA_YMD"]) + "  " + name
        if line not in seen:
            seen.add(line)
            lines.append(line)
    nm = t.month % 12 + 1
    q = [quick("이번 달 일정", f"{t.month}월 일정"), quick("다음 달 일정", f"{nm}월 일정"), quick("행사"), quick("처음으로")]
    pre = intro + "\n\n" if intro else ""
    if not lines:
        return reply([simple_text(pre + "📅 " + title + "\n\n등록된 일정이 없어요.")], q)
    return reply(split_text(pre + "📅 " + title + "\n\n" + "\n".join(lines)), q)


# ---------- 행사 ----------

def events(utter):
    t = today().strftime("%Y-%m-%d")
    up = sorted([e for e in EVENTS if e.get("date", "") >= t and not is_sample(e.get("title", ""))], key=lambda e: e["date"])
    if not up:
        return schedule(utter, "따로 등록된 행사가 없어서 학사일정을 보여 드릴게요.")
    items = []
    for e in up[:10]:
        btn = [link_button(e.get("button") or "자세히 보기", e["url"])] if e.get("url") else None
        items.append(card(short_label(e["date"].replace("-", "")) + " " + e["title"], e.get("desc"), btn))
    return reply([simple_text("🎉 다가오는 행사예요."), carousel("textCard", items)], [quick("학사일정"), quick("처음으로")])


# ---------- 동아리 ----------

def club_keys(c):
    # 동아리를 찾을 때 쓰는 낱말: 전체 이름과 괄호로 나뉜 각 부분 (예: "화학실험(ACE)" → 화학실험(ace), 화학실험, ace)
    n = squash(c["name"]).lower()
    keys = set([n] + [p for p in re.split(r"[()]", n) if len(p) >= 2])
    for k in list(keys):   # "온정나눔동아리" → "온정나눔", "방송반" → "방송" 으로도 찾을 수 있게
        short = re.sub(r"(동아리|반|부)$", "", k)
        if len(short) >= 2:
            keys.add(short)
    return keys


def clubs(utter):
    u = squash(utter).lower()
    q_word = re.sub(r"동아리|소개|알려줘|목록|보여줘|전체|뭐있어|뭐가있어|\?", "", u)
    cats, subs = [], []
    for c in CLUBS:
        if c.get("category") and c["category"] not in cats:
            cats.append(c["category"])
        if c.get("sub") and c["sub"] not in subs:
            subs.append(c["sub"])
    found, pick = CLUBS, ""
    if q_word:
        # "자율 학술"처럼 자율 안의 세부 분류 → 분류(창체·학술·자율·유네스코) → 동아리 이름 순서로 찾음
        cat = "자율" if "자율" in q_word else next((x for x in cats if x in q_word), "")
        sub = next((x for x in subs if any(w in q_word for w in squash(x).split("·"))), "")
        if sub and (cat == "자율" or sub not in cats):
            hit, pick = [c for c in CLUBS if c.get("sub") == sub], "자율"
        elif cat:
            hit, pick = [c for c in CLUBS if c.get("category") == cat], cat
        else:
            hit = [c for c in CLUBS if any(k in u for k in club_keys(c)) or q_word in squash(c["name"]).lower()]
        if hit:
            found = hit  # 맞는 것이 있으면 그것만, 없으면 전체
    if pick == "자율":
        # 자율 동아리를 보고 있을 때는 세부 분류 버튼을 보여 줌
        q = [quick(x if x not in cats else "자율 " + x, "자율 " + x + " 동아리") for x in subs[:6]] + [quick("자율 전체", "자율 동아리"), quick("전체 동아리"), quick("처음으로")]
    else:
        q = [quick(c, c + " 동아리") for c in cats[:8]] + [quick("전체 동아리"), quick("처음으로")]
    if len(found) > 10:
        # 카드는 10장까지만 보낼 수 있어서, 많을 때는 이름 목록으로 보여 줌
        by_sub = pick == "자율"
        lines = []
        for g in (subs if by_sub else cats) or [""]:
            names = [c["name"] for c in found if c.get("sub" if by_sub else "category", "") == g]
            if names:
                lines.append(("[" + ("자율·" if by_sub else "") + g + "] " if g else "") + str(len(names)) + "개")
                lines += ["· " + n for n in names]
                lines.append("")
        text = "📚 " + (pick + " " if pick else "") + "동아리 " + str(len(found)) + "개\n\n" + "\n".join(lines).strip() + "\n\n동아리 이름을 보내면 자세히 알려 드려요. (예: ACE)"
        return reply(split_text(text), q)
    items = []
    for c in found[:10]:
        btn = [link_button("자세히 보기", c["url"])] if c.get("url") else None
        cat = "[" + c["category"] + ("·" + c["sub"] if c.get("sub") else "") + "] " if c.get("category") else ""
        items.append(card(c["name"], cat + c.get("desc", ""), btn))
    return reply([carousel("textCard", items)], q)


# ---------- 홍보 ----------

def promo():
    real = [p for p in PROMO if not is_sample(p.get("title", ""))]
    if not real:
        return reply([simple_text("지금 올라온 홍보가 없어요.")])
    with_photo = all(p.get("image") for p in real)
    items = []
    for p in real[:10]:
        btn = [link_button(p.get("button") or "자세히 보기", p["url"])] if p.get("url") else None
        c = card(p["title"], p.get("desc"), btn)
        if with_photo:
            c["thumbnail"] = {"imageUrl": p["image"]}
        items.append(c)
    return reply([simple_text("📢 학교 소식이에요."), carousel("basicCard" if with_photo else "textCard", items)])


# ---------- 링크 ----------

def more_links():
    out = []
    try:
        rows = neis("schoolInfo", {"ATPT_OFCDC_SC_CODE": ATPT_CODE, "SD_SCHUL_CODE": SCHOOL_CODE or school_code()}, with_school=False)
        home = (rows[0].get("HMPG_ADRES") or "").strip() if rows else ""
        if home:
            out.append({"group": "학교·행정", "title": "학교 홈페이지", "url": home if home.startswith("http") else "http://" + home})
    except Exception as e:
        print("[오류] 학교 홈페이지", repr(e))
    return out + [m for m in MORE_LINKS if m.get("url")]


def top_links(items, n):
    # 갈래(sub)가 있는 묶음은 갈래마다 앞에서 n개만 고름 (챗봇 카드는 개수 제한이 있어서)
    seen, out = {}, []
    for m in items:
        if m.get("sub"):
            k = (m["group"], m["sub"])
            seen[k] = seen.get(k, 0) + 1
            if seen[k] > n:
                continue
        out.append(m)
    return out


def all_links():
    items = [card(l["title"], l["desc"], [link_button(l.get("button") or "열기", l["url"])]) for l in live_links()]
    more = [card(m["title"], "[" + m["group"] + (" · " + m["sub"] if m.get("sub") else "") + "]", [link_button("열기", m["url"])]) for m in top_links(more_links(), 1)]
    outs = [carousel("textCard", items)]
    for i in (0, 10):
        if more[i:i + 10]:
            outs.append(carousel("textCard", more[i:i + 10]))
    return reply(outs)


# ---------- 학교 지도 ----------

def room_names():
    rooms = {}
    for f in MAP:
        for t in f["t"]:
            if t[4]:
                rooms.setdefault(squash(t[4]).lower(), [t[4], []])[1].append(f["b"] + " " + f["n"][0] + "층")
    return rooms


ROOMS = room_names()


def map_button():
    return [link_button("지도 보기", request.host_url.replace("http://", "https://") + "#s-map")]


def room(key):
    name, fl = ROOMS[key]
    where = ", ".join(sorted(set(fl)))
    return reply([{"textCard": card("📍 " + name, name + "은(는) " + where + "에 있어요.", map_button())}])


def school_map():
    lines = []
    for f in MAP:
        names = []
        for t in f["t"]:
            if t[4] and t[4] not in names and not re.fullmatch(r"(외부인숙소 )?[ABC]\d{3}", t[4]):
                names.append(t[4])   # 기숙사 호실은 너무 많아서 목록에서는 뺌
        lines.append(f["b"] + " " + f["n"][0] + "층: " + (", ".join(names) or f.get("note", "")))
    outs = split_text("🗺 학교 지도\n\n" + "\n\n".join(lines))[:2]
    return reply(outs + [{"textCard": card("층별 지도", "앱에서 본관동·실험동 층별 지도를 볼 수 있어요.", map_button())}])


def ai_links():
    ai = [m for m in MORE_LINKS if m.get("group") == "AI" and m.get("url")]
    first = top_links(ai, 1)
    picks = (first + [m for m in ai if m not in first])[:10]   # 기능마다 하나씩 먼저, 남는 자리는 순서대로
    items = [card(m["title"], m.get("sub") or "AI 사이트", [link_button("열기", m["url"])]) for m in picks]
    return reply([simple_text("🤖 기능별로 많이 쓰는 AI 사이트예요. 더 많은 목록은 앱의 링크 모음에 있어요."), carousel("textCard", items)])


def connectors():
    outs = []
    for c in CONNECTORS[:3]:
        text = "🧪 " + c["title"] + " (AI 커넥터)\n" + c["desc"] + ("\n" + c["by"] if c.get("by") else "") + "\n\n주소: " + c["url"] + "\n\n" + "\n".join("· " + h for h in c.get("how", []))
        if c.get("note"):
            text += "\n\n⚠ " + c["note"]
        outs.append(simple_text(text))
    return reply(outs or [simple_text("등록된 커넥터가 없어요.")])


# ---------- 학교 기사 ----------

def news_items():
    hit = cache.get("news")
    if hit and time.time() - hit[0] < 1800:
        return hit[1]
    try:
        r = requests.get("https://news.google.com/rss/search",
                         params={"q": " OR ".join(NEWS_WORDS), "hl": "ko", "gl": "KR", "ceid": "KR:ko"},
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=4)
        found, seen = [], set()
        for it in ET.fromstring(r.content).iter("item"):
            title = (it.findtext("title") or "").strip()
            src = (it.findtext("source") or "").strip()
            if src and title.endswith(" - " + src):
                title = title[:-len(" - " + src)].strip()
            url = (it.findtext("link") or "").strip()
            key = squash(title)
            if not url or key in seen or not any(squash(w) in key for w in NEWS_WORDS):
                continue
            seen.add(key)
            try:
                when = parsedate_to_datetime(it.findtext("pubDate")).astimezone(KST)
            except Exception:
                when = None
            found.append({"title": title, "source": src, "url": url, "ts": when.timestamp() if when else 0,
                          "day": f"{when.year}.{when.month}.{when.day}" if when else ""})
        found.sort(key=lambda x: -x["ts"])
        items = [{k: v for k, v in x.items() if k != "ts"} for x in found[:NEWS_COUNT]]
    except Exception:
        if hit:
            return hit[1]
        raise
    cache["news"] = (time.time(), items)
    return items


def news():
    try:
        items = news_items()
    except Exception as e:
        print("[오류] 기사", repr(e))
        return reply([simple_text("기사를 불러오지 못했어요. 잠시 뒤 다시 물어봐 주세요.")])
    if not items:
        return reply([simple_text("최근 학교 기사를 찾지 못했어요.")])
    cards = [card(n["title"], " · ".join(x for x in (n["source"], n["day"]) if x), [link_button("기사 보기", n["url"])]) for n in items]
    return reply([simple_text("📰 " + SCHOOL_NAME + " 관련 기사예요."), carousel("textCard", cards)])


def one_link(l):
    desc = l["desc"] + ("\n" + l["by"] if l.get("by") else "")
    return reply([{"textCard": card(l["title"], desc, [link_button(l.get("button") or "열기", l["url"])])}])


# ---------- 급식 알림 안내 ----------

def noti():
    times = " · ".join(s[1] + " " + str(int(s[2])) + "시" for s in PUSH_SLOTS)
    desc = ("매일 " + times + "에 그 끼니 급식을 휴대폰 알림으로 보내 드려요.\n"
            "아래 버튼으로 앱을 열고 '급식 알림 받기'를 한 번만 누르면 돼요.\n"
            "아이폰은 먼저 '홈 화면에 추가'를 한 뒤 그 앱에서 눌러 주세요.")
    return reply([{"textCard": card("🔔 급식 알림 받기", desc, [link_button("알림 켜러 가기", APP_URL + "/#meal")])}])


# ---------- 첫 화면 ----------

def home(unknown):
    outs = []
    if unknown:
        outs.append(simple_text("무슨 말인지 잘 모르겠어요 😅 아래 버튼을 눌러 보세요."))
    outs.append({"textCard": card(
        SCHOOL_NAME + " 챗봇",
        "급식, 급식 알림, 학사일정, 학교 기사, 동아리, 각종 신청 링크를 안내해요.\n'내일 점심', '금요일 급식', '12월 일정'처럼 물어봐도 돼요.",
        [link_button("앱 열기", APP_URL)],
    )})
    return reply(outs)


# ---------- 앱 화면 ----------

def is_sample(text):
    # 설정에 아직 예시로 남아 있는 항목은 앱에 보여 주지 않음
    return "예시" in text or re.fullmatch(r"동아리 이름 \d+", text.strip()) is not None


def dday(d):
    n = (d - today()).days
    return "오늘" if n == 0 else ("내일" if n == 1 else f"D-{n}")


def app_focus():
    # 지금 시각에 먼저 보여 줄 급식: (날짜, 조식1·중식2·석식3)
    now = datetime.now(KST)
    h = now.hour + now.minute / 60
    if h < BREAKFAST_UNTIL:
        return now.date(), "1"
    if h < LUNCH_UNTIL:
        return now.date(), "2"
    if h < NEXT_DAY_AFTER:
        return now.date(), "3"
    return now.date() + timedelta(days=1), "1"


@app.route("/", methods=["GET"])
def app_page():
    html = PAGE.replace("__SCHOOL__", SCHOOL_NAME).replace("__SHORT__", APP_SHORT_NAME)
    return html, 200, {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-cache"}


@app.route("/api/meal", methods=["GET"])
def api_meal():
    day, focus = app_focus()
    d = request.args.get("d", "")
    if re.fullmatch(r"\d{8}", d):
        try:
            day = datetime.strptime(d, "%Y%m%d").date()
        except ValueError:
            pass
    diff = (day - today()).days
    out = {
        "date": day.strftime("%Y%m%d"),
        "label": md_label(day),
        "rel": {-1: "어제", 0: "오늘", 1: "내일", 2: "모레"}.get(diff, ""),
        "focus": focus,
        "prev": (day - timedelta(days=1)).strftime("%Y%m%d"),
        "next": (day + timedelta(days=1)).strftime("%Y%m%d"),
        "meals": [],
    }
    try:
        rows = neis("mealServiceDietInfo", {"MLSV_YMD": out["date"]})
        for r in sorted(rows, key=lambda r: r.get("MMEAL_SC_CODE", "")):
            out["meals"].append({
                "code": str(r.get("MMEAL_SC_CODE", "")),
                "name": r.get("MMEAL_SC_NM", ""),
                "menu": menu_items(r.get("DDISH_NM")),
                "cal": r.get("CAL_INFO", ""),
            })
    except Exception as e:
        print("[오류] 급식", repr(e))
        out["error"] = True
    return jsonify(out)


@app.route("/api/info", methods=["GET"])
def api_info():
    t = today()
    sched = []
    try:
        rows = neis("SchoolSchedule", {"AA_FROM_YMD": t.strftime("%Y%m%d"),
                                       "AA_TO_YMD": (t + timedelta(days=SCHEDULE_DAYS)).strftime("%Y%m%d")})
        seen = set()
        for r in sorted(rows, key=lambda r: r.get("AA_YMD", "")):
            name = (r.get("EVENT_NM") or "").strip()
            key = str(r.get("AA_YMD", "")) + name
            if not name or "토요휴업일" in name or key in seen:
                continue
            seen.add(key)
            d = datetime.strptime(str(r["AA_YMD"])[:8], "%Y%m%d").date()
            sched.append({"day": short_label(r["AA_YMD"]), "name": name, "dday": dday(d)})
    except Exception as e:
        print("[오류] 학사일정", repr(e))
        sched = None
    ev = []
    for e in sorted(EVENTS, key=lambda e: e.get("date", "")):
        if e.get("date", "") < t.strftime("%Y-%m-%d") or is_sample(e.get("title", "")):
            continue
        d = datetime.strptime(e["date"], "%Y-%m-%d").date()
        ev.append({"day": short_label(e["date"].replace("-", "")), "title": e["title"],
                   "desc": e.get("desc", ""), "url": e.get("url", ""), "dday": dday(d)})
    return jsonify({
        "days": SCHEDULE_DAYS,
        "schedule": sched,
        "events": ev,
        "promo": [p for p in PROMO if not is_sample(p.get("title", ""))],
        "clubs": [c for c in CLUBS if not is_sample(c.get("name", ""))],
        "links": [{"title": l["title"], "desc": l["desc"], "url": l["url"], "by": l.get("by", "")} for l in live_links()],
        "mapBy": MAP_BY,
        "more": more_links(),
        "connectors": CONNECTORS,
    })


# ---------- 급식 알림 (웹 푸시) ----------
# 구독 정보는 서버 메모리에 두고, GitHub Actions 가 틈틈이 암호화된 묶음으로 받아 저장소(push-data 가지)에 보관함.
# 서버는 켜질 때 그 묶음을 스스로 읽어 복구하고, 잠들지 않도록 10분마다 자기 주소를 한 번씩 부르며,
# 1분마다 시계를 보고 7시·12시·18시가 되면 직접 알림을 보냄. 알림 열쇠는 NEIS_KEY 에서 만들어 따로 넣을 것이 없음.

SUBS = {}        # endpoint -> 구독 정보
SENT = {}        # "날짜-끼니" -> True (같은 알림을 두 번 보내지 않기 위함)
LAST_BLOB = {"hash": "", "text": ""}
PUSH_LOCK = threading.Lock()
SELF_URL = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")
PUSH_HOST = SELF_URL.replace("https://", "") or "ushs-student.onrender.com"
PUSH_HOSTS = ("fcm.googleapis.com", ".push.services.mozilla.com", ".notify.windows.com", ".push.apple.com")


def push_on():
    return PUSH_LIB and bool(NEIS_KEY)


def push_secret(tag):
    return hashlib.sha256((tag + ":" + NEIS_KEY).encode()).digest()


def vapid_keys():
    n = int.from_bytes(push_secret("vapid"), "big") % (2 ** 255) + 1
    key = ec.derive_private_key(n, ec.SECP256R1())
    raw = base64.urlsafe_b64encode(n.to_bytes(32, "big")).decode().rstrip("=")
    pub = key.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return raw, base64.urlsafe_b64encode(pub).decode().rstrip("=")


def fernet():
    return Fernet(base64.urlsafe_b64encode(push_secret("blob")))


def valid_sub(s):
    try:
        ep = s["endpoint"]
        host = ep.split("/")[2]
        ok_host = any(host == h or host.endswith(h) for h in PUSH_HOSTS)
        return ep.startswith("https://") and ok_host and len(ep) < 1000 and len(s["keys"]["p256dh"]) < 200 and len(s["keys"]["auth"]) < 100
    except Exception:
        return False


def clean_sub(s):
    return {"endpoint": s["endpoint"], "keys": {"p256dh": s["keys"]["p256dh"], "auth": s["keys"]["auth"]}}


def push_state():
    day = today().strftime("%Y%m%d")
    for k in [k for k in SENT if not k.startswith(day)]:
        del SENT[k]
    return json.dumps({"subs": [SUBS[k] for k in sorted(SUBS)], "sent": sorted(SENT)}, sort_keys=True, separators=(",", ":"))


PUSH_LOG = []    # 최근 전송 결과 (어디로 보냈는지는 적지 않고 성공·실패 이유만 적음). /api/push/status 에서 확인


def push_note(title, result):
    PUSH_LOG.append({"time": datetime.now(KST).strftime("%m-%d %H:%M:%S"), "title": title, "result": result})
    del PUSH_LOG[:-30]
    print("[알림]", title, result)


def send_push(sub, payload):
    priv, _ = vapid_keys()
    service = sub["endpoint"].split("/")[2]
    try:
        webpush(clean_sub(sub), json.dumps(payload, ensure_ascii=False).encode("utf-8"), vapid_private_key=priv,
                vapid_claims={"sub": "https://" + PUSH_HOST}, ttl=3600, timeout=8, headers={"Urgency": "high"})
        push_note(payload.get("title", ""), "성공 (" + service + ")")
        return True
    except WebPushException as e:
        resp = getattr(e, "response", None)
        code = getattr(resp, "status_code", 0)
        if code in (404, 410):
            SUBS.pop(sub["endpoint"], None)   # 브라우저에서 알림을 끈 구독은 지움
        push_note(payload.get("title", ""), "실패 " + str(code) + " (" + service + ") " + str(getattr(resp, "text", "") or e)[:120])
    except Exception as e:
        push_note(payload.get("title", ""), "실패 (" + service + ") " + repr(e)[:120])
    return False


def send_all(payload):
    total, n = len(SUBS), 0
    for sub in list(SUBS.values()):
        n += send_push(sub, payload)
    print("[알림] 보냄", n, "/", total, payload.get("title"))


def merge_blob(text):
    lines = text.strip().split("\n")
    data = json.loads(fernet().decrypt(lines[-1].encode()).decode())
    with PUSH_LOCK:
        for s in data.get("subs", []):
            if valid_sub(s) and len(SUBS) < 3000:
                SUBS.setdefault(s["endpoint"], clean_sub(s))
        for k in data.get("sent", []):
            SENT[str(k)] = True
    return len(SUBS)


def meal_push_tick():
    # 지금이 알림 시간이면 그 끼니 급식을 한 번만 보냄. 구독자가 없거나 급식 조회에 실패하면 다음에 다시 시도함
    now = datetime.now(KST)
    h = now.hour + now.minute / 60
    slot = next((s for s in PUSH_SLOTS if s[2] <= h < s[3]), None)
    if not slot:
        return {"ok": True, "sent": 0, "why": "알림 시간이 아님"}
    key = now.strftime("%Y%m%d") + "-" + slot[0]
    with PUSH_LOCK:
        if SENT.get(key):
            return {"ok": True, "sent": 0, "why": "이미 보냄"}
        if not SUBS:
            return {"ok": True, "sent": 0, "why": "구독자 없음"}
        try:
            rows = neis("mealServiceDietInfo", {"MLSV_YMD": now.strftime("%Y%m%d"), "MMEAL_SC_CODE": slot[0]})
        except Exception as e:
            print("[알림] 급식 조회 실패", repr(e))
            return {"ok": False, "why": "급식 조회 실패"}
        SENT[key] = True
    if not rows:
        return {"ok": True, "sent": 0, "why": "급식 없음"}
    payload = {"title": "오늘 " + slot[1] + " 급식", "body": ", ".join(menu_items(rows[0].get("DDISH_NM"))), "tag": "meal-" + key, "url": "/"}
    threading.Thread(target=send_all, args=(payload,), daemon=True).start()
    return {"ok": True, "sent": len(SUBS)}


def push_keeper():
    # 서버가 켜져 있는 동안 계속 도는 일꾼
    try:
        r = requests.get(PUSH_BACKUP_URL, timeout=10)
        if r.status_code == 200 and r.text.strip():
            print("[알림] 보관된 구독 복구:", merge_blob(r.text), "명")
    except Exception as e:
        print("[알림] 구독 복구 실패", repr(e))
    n = 0
    while True:
        try:
            meal_push_tick()
            if SELF_URL and n % 10 == 0:
                requests.get(SELF_URL + "/status", timeout=20)   # 15분 동안 아무도 안 쓰면 잠드는 것을 막음
        except Exception as e:
            print("[알림] 일꾼 오류", repr(e))
        n += 1
        time.sleep(60)


@app.route("/sw.js", methods=["GET"])
def sw():
    return SW, 200, {"Content-Type": "application/javascript; charset=utf-8", "Cache-Control": "no-cache"}


@app.route("/api/push/key", methods=["GET"])
def push_key():
    if not push_on():
        return jsonify({"on": False})
    return jsonify({"on": True, "key": vapid_keys()[1], "slots": [[s[1], s[2]] for s in PUSH_SLOTS]})


@app.route("/api/push/subscribe", methods=["POST"])
def push_subscribe():
    s = request.get_json(silent=True) or {}
    if not push_on() or not valid_sub(s) or (len(SUBS) >= 3000 and s["endpoint"] not in SUBS):
        return jsonify({"ok": False}), 400
    new = s["endpoint"] not in SUBS
    SUBS[s["endpoint"]] = clean_sub(s)
    if new and s.get("hello"):   # 방금 알림을 켠 사람에게는 잘 켜졌는지 바로 알 수 있게 한 번 보내 줌
        hello = {"title": "급식 알림이 켜졌어요", "body": "매일 아침 7시, 점심 12시, 저녁 6시에 급식을 알려 드릴게요.", "tag": "hello", "url": "/"}
        threading.Thread(target=send_push, args=(clean_sub(s), hello), daemon=True).start()
    return jsonify({"ok": True})


@app.route("/api/push/unsubscribe", methods=["POST"])
def push_unsubscribe():
    s = request.get_json(silent=True) or {}
    SUBS.pop(s.get("endpoint", ""), None)
    return jsonify({"ok": True})


@app.route("/api/push/test", methods=["POST"])
def push_test():
    s = request.get_json(silent=True) or {}
    sub = SUBS.get(s.get("endpoint", ""))
    if not push_on() or not sub:
        return jsonify({"ok": False}), 400
    ok = send_push(sub, {"title": "급식 알림이 켜졌어요", "body": "매일 아침 7시, 점심 12시, 저녁 6시에 급식을 알려 드릴게요.", "tag": "test", "url": "/"})
    return jsonify({"ok": ok})


@app.route("/api/push/status", methods=["GET"])
def push_status():
    return jsonify({"on": push_on(), "subs": len(SUBS), "sent": sorted(SENT), "now": datetime.now(KST).strftime("%m-%d %H:%M:%S"), "log": PUSH_LOG[-30:]})


@app.route("/api/push/blob", methods=["GET"])
def push_blob():
    if not push_on():
        return "", 200, {"Content-Type": "text/plain"}
    with PUSH_LOCK:
        state = push_state()
        if not SUBS and not SENT:
            return "", 200, {"Content-Type": "text/plain"}
        h = hashlib.sha256(state.encode()).hexdigest()[:16]
        if LAST_BLOB["hash"] != h:
            LAST_BLOB["hash"] = h
            LAST_BLOB["text"] = h + "\n" + fernet().encrypt(state.encode()).decode() + "\n"
        return LAST_BLOB["text"], 200, {"Content-Type": "text/plain", "Cache-Control": "no-store"}


@app.route("/api/push/restore", methods=["POST"])
def push_restore():
    if not push_on():
        return jsonify({"ok": False}), 400
    try:
        n = merge_blob(request.get_data(as_text=True))
    except (InvalidToken, ValueError, IndexError):
        return jsonify({"ok": False}), 400
    return jsonify({"ok": True, "subs": n})


@app.route("/cron/meal-push", methods=["GET"])
def cron_meal_push():
    if not push_on():
        return jsonify({"ok": False})
    return jsonify(meal_push_tick())


@app.route("/api/map", methods=["GET"])
def api_map():
    return jsonify(MAP), 200, {"Cache-Control": "public, max-age=3600"}


@app.route("/api/news", methods=["GET"])
def api_news():
    try:
        return jsonify({"items": news_items()})
    except Exception as e:
        print("[오류] 기사", repr(e))
        return jsonify({"items": None})


@app.route("/manifest.json", methods=["GET"])
def manifest():
    return jsonify({
        "name": SCHOOL_NAME, "short_name": APP_SHORT_NAME, "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#e9963c",
        "icons": [{"src": "/icon.png?v=2", "sizes": "192x192", "type": "image/png", "purpose": "any"}],
    })


@app.route("/icon.png", methods=["GET"])
def icon():
    return base64.b64decode(ICON_B64), 200, {"Content-Type": "image/png", "Cache-Control": "public, max-age=604800"}


# ---------- 챗봇 주소(라우트) ----------

@app.route("/status", methods=["GET"])
def status():
    code = SCHOOL_CODE or "아직 못 찾음"
    key = "등록됨" if NEIS_KEY else "없음(조회 개수 제한)"
    return (f"{SCHOOL_NAME} 서버 작동 중\n학교코드: {code}\n나이스 인증키: {key}\n"
            "앱: /\n챗봇 미리보기: /test?q=내일 급식\n카카오 스킬 URL 끝: /skill"), 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/skill", methods=["POST"])
def skill():
    data = request.get_json(silent=True) or {}
    utter = (data.get("userRequest", {}).get("utterance") or "").strip()
    block = (data.get("intent") or {}).get("name", "")
    try:
        return jsonify(handle(utter, block))
    except requests.Timeout:
        return jsonify(reply([simple_text("나이스 서버 응답이 늦어요. 잠시 뒤 다시 물어봐 주세요.")]))
    except Exception as e:
        print("[오류]", repr(e))
        return jsonify(reply([simple_text("잠시 문제가 생겼어요. 조금 뒤에 다시 시도해 주세요.")]))


@app.route("/test", methods=["GET"])
def test():
    q = request.args.get("q", "")
    b = request.args.get("block", "")
    try:
        return jsonify(handle(q, b))
    except Exception as e:
        return jsonify({"오류": repr(e)})


# Render 처럼 "python app.py" 로 켜는 서버와 내 컴퓨터에서 쓰임. Vercel 에서는 이 부분이 실행되지 않음
# Render 는 PORT 라는 이름으로 문 번호를 정해 주므로 그 번호를 받아 씀 (없으면 5000)
if __name__ == "__main__":
    if push_on():
        threading.Thread(target=push_keeper, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False, threaded=True)
