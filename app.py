# -*- coding: utf-8 -*-
"""
울산과학고등학교 앱 + 카카오톡 챗봇 서버 (Vercel 용 · 라즈베리파이 필요 없음)

하는 일
  급식(조식·중식·석식), 학사일정 → 나이스(NEIS)에서 자동으로 가져옴
  행사, 동아리, 홍보, 링크(기상곡 신청, 실험실 신청, 학습실 위치알리미) → 아래 설정에 적은 내용으로 안내

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
import os
import re
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import requests
from flask import Flask, request, jsonify

from page import PAGE, ICON_B64

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
        "title": "기상곡 신청",
        "desc": "기상곡을 신청할 수 있어요.",
        "url": "https://onair-three-beta.vercel.app/",
        "button": "신청하러 가기",
        "keywords": ["기상곡", "기상송", "기상음악", "노래신청", "노래 신청"],
    },
    {
        "title": "화학실·생물실 신청",
        "desc": "화학실과 생물실 사용을 예약해요. 학교 계정으로 로그인해야 해요.",
        "url": "https://ushs-lab.vercel.app/?next=/book",
        "button": "예약하러 가기",
        "keywords": ["화학실", "생물실", "실험실", "실험실 신청", "실험실 예약"],
    },
    {
        "title": "학교 위치알리미",
        "desc": "학교 구글 계정(@ushs.hs.kr)으로 로그인해야 열려요. 카톡에서 안 열리면 오른쪽 위 메뉴에서 '다른 브라우저로 열기'를 눌러 보세요.",
        "url": "https://script.google.com/a/macros/ushs.hs.kr/s/AKfycbwBclQ5njll0mmySd74avm2zbHOMqZ4dqKfgveHE897OXVTXLfr7MhkPxKNPkxLkRJSbw/exec",
        "button": "열기",
        "keywords": ["학교 위치알리미", "학교 위치"],
    },
    {
        "title": "현장체험학습 신청서",
        "desc": "현장체험학습 신청서를 작성하러 가요.",
        "url": "",   # ← 신청서 주소를 여기에 넣으면 앱과 챗봇에 바로 나타남 (비어 있으면 숨겨짐)
        "button": "작성하러 가기",
        "keywords": ["현장체험", "체험학습", "신청서"],
    },
    {
        "title": "학습실 위치알리미",
        "desc": "학교 구글 계정(@ushs.hs.kr)으로 로그인해야 열려요. 카톡에서 안 열리면 오른쪽 위 메뉴에서 '다른 브라우저로 열기'를 눌러 보세요.",
        "url": "https://script.google.com/a/macros/ushs.hs.kr/s/AKfycbwgOU6e7XZhSiszoH6_xPvyHH-W0opNGVKG5msiECVHAJP8NaMhMbYMaYXTdLocGoMrxQ/exec",
        "button": "열기",
        "keywords": ["위치알리미", "위치 알리미", "학습실", "위치"],
    },
]

# 3-1. 링크 모음 (앱 맨 아래 "링크 모음"과 챗봇 "링크 모음"에 나옴)
#    group 이 같은 것끼리 묶여 나옴. 한 줄 추가하면 바로 늘어남. "학교 홈페이지"는 나이스에서 자동으로 찾아 넣음
MORE_LINKS = [
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
    {"group": "탐구·연구", "title": "RISS 학술연구정보", "url": "https://www.riss.kr"},
    {"group": "탐구·연구", "title": "구글 학술검색", "url": "https://scholar.google.com"},
    {"group": "탐구·연구", "title": "ScienceON", "url": "https://scienceon.kisti.re.kr"},
    {"group": "탐구·연구", "title": "NCBI", "url": "https://www.ncbi.nlm.nih.gov"},
    {"group": "탐구·연구", "title": "arXiv", "url": "https://arxiv.org"},
    {"group": "탐구·연구", "title": "KOSIS 국가통계", "url": "https://kosis.kr"},
    {"group": "탐구·연구", "title": "공공데이터포털", "url": "https://www.data.go.kr"},
    {"group": "도구", "title": "Desmos 그래프", "url": "https://www.desmos.com/calculator"},
    {"group": "도구", "title": "GeoGebra", "url": "https://www.geogebra.org"},
    {"group": "도구", "title": "WolframAlpha", "url": "https://www.wolframalpha.com"},
    {"group": "도구", "title": "PhET 시뮬레이션", "url": "https://phet.colorado.edu/ko/"},
    {"group": "도구", "title": "백준", "url": "https://www.acmicpc.net"},
    {"group": "도구", "title": "기상청 날씨누리", "url": "https://www.weather.go.kr"},
]

# 3-2. 학교 기사 (구글 뉴스에서 아래 낱말로 검색해 제목에 그 낱말이 들어간 기사만 보여 줌)
NEWS_WORDS = ["울산과학고", "울산과고"]
NEWS_COUNT = 8             # 보여 줄 기사 수

# 4. 동아리
#    category 로 분야를 나누면 "학술 동아리"처럼 분야별로 볼 수 있음
#    url 은 없으면 "" 로 두기
CLUBS = [
    {"name": "동아리 이름 1", "category": "학술", "desc": "어떤 활동을 하는지 한두 문장", "url": ""},
    {"name": "동아리 이름 2", "category": "공학", "desc": "어떤 활동을 하는지 한두 문장", "url": ""},
    {"name": "동아리 이름 3", "category": "예체능", "desc": "어떤 활동을 하는지 한두 문장", "url": ""},
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
SCHEDULE_DAYS = 30         # 학사일정 기본 조회 기간(일)
NEIS_TIMEOUT = 3           # 나이스 응답 대기(초). 카카오는 5초 안에 답해야 함

# ======================================================================
# 여기부터는 수정하지 않아도 됨
# ======================================================================

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
    base = [quick(t) for t in ["오늘 급식", "내일 급식", "학사일정", "학교 기사", "행사", "동아리", "홍보"]]
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
    "학교 기사": "news",
    "학교 위치알리미": "link:학교 위치알리미",
    "현장체험학습 신청서": "link:현장체험학습 신청서",
    "기상곡 신청": "link:기상곡 신청",
    "실험실 신청": "link:화학실·생물실 신청",
    "위치알리미": "link:학습실 위치알리미",
}


def by_words(utter):
    u = squash(utter)
    for l in live_links():
        words = [l["title"]] + l.get("keywords", [])
        if any(squash(w) in u for w in words):
            return "link:" + l["title"]
    if re.search(r"기사|뉴스|신문|보도", u):
        return "news"
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
    if re.search(r"메뉴|처음|도움|시작|안녕|하이", u):
        return "home"
    return ""


def handle(utter, block=""):
    what = by_words(utter) or BLOCKS.get((block or "").strip(), "")
    if what.startswith("link:"):
        for l in live_links():
            if l["title"] == what[5:]:
                return one_link(l)
    if what == "news":
        return news()
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
    up = sorted([e for e in EVENTS if e.get("date", "") >= t], key=lambda e: e["date"])
    if not up:
        return schedule(utter, "따로 등록된 행사가 없어서 학사일정을 보여 드릴게요.")
    items = []
    for e in up[:10]:
        btn = [link_button(e.get("button") or "자세히 보기", e["url"])] if e.get("url") else None
        items.append(card(short_label(e["date"].replace("-", "")) + " " + e["title"], e.get("desc"), btn))
    return reply([simple_text("🎉 다가오는 행사예요."), carousel("textCard", items)], [quick("학사일정"), quick("처음으로")])


# ---------- 동아리 ----------

def clubs(utter):
    q_word = re.sub(r"동아리|소개|알려줘|목록|보여줘|전체|뭐있어|뭐가있어|\?", "", squash(utter))
    cats = []
    for c in CLUBS:
        if c.get("category") and c["category"] not in cats:
            cats.append(c["category"])
    q = [quick(c, c + " 동아리") for c in cats[:8]] + [quick("전체 동아리"), quick("처음으로")]
    found = CLUBS
    if q_word:
        hit = [c for c in CLUBS if q_word in squash(c["name"] + c.get("category", ""))]
        if hit:
            found = hit  # 이름이나 분야가 맞으면 그것만, 아니면 전체
    outs = []
    if len(found) > 10:
        outs.append(simple_text(f"동아리가 {len(found)}개라 10개까지만 보여 드려요. 아래에서 분야를 골라 보세요."))
    items = []
    for c in found[:10]:
        btn = [link_button("자세히 보기", c["url"])] if c.get("url") else None
        cat = "[" + c["category"] + "] " if c.get("category") else ""
        items.append(card(c["name"], cat + c.get("desc", ""), btn))
    outs.append(carousel("textCard", items))
    return reply(outs, q)


# ---------- 홍보 ----------

def promo():
    if not PROMO:
        return reply([simple_text("지금 올라온 홍보가 없어요.")])
    with_photo = all(p.get("image") for p in PROMO)
    items = []
    for p in PROMO[:10]:
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


def all_links():
    items = [card(l["title"], l["desc"], [link_button(l.get("button") or "열기", l["url"])]) for l in live_links()]
    more = [card(m["title"], "[" + m["group"] + "]", [link_button("열기", m["url"])]) for m in more_links()]
    outs = [carousel("textCard", items)]
    for i in (0, 10):
        if more[i:i + 10]:
            outs.append(carousel("textCard", more[i:i + 10]))
    return reply(outs)


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
    return reply([{"textCard": card(l["title"], l["desc"], [link_button(l.get("button") or "열기", l["url"])])}])


# ---------- 첫 화면 ----------

def home(unknown):
    outs = []
    if unknown:
        outs.append(simple_text("무슨 말인지 잘 모르겠어요 😅 아래 버튼을 눌러 보세요."))
    outs.append({"textCard": card(
        SCHOOL_NAME + " 챗봇",
        "급식, 학사일정, 학교 기사, 행사, 동아리, 홍보, 각종 신청 링크를 안내해요.\n'내일 점심', '금요일 급식', '12월 일정'처럼 물어봐도 돼요.",
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
        "links": [{"title": l["title"], "desc": l["desc"], "url": l["url"]} for l in live_links()],
        "more": more_links(),
    })


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
        "background_color": "#f4f1ea", "theme_color": "#0b5d4b",
        "icons": [{"src": "/icon.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}],
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False, threaded=True)
