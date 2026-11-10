# -*- coding: utf-8 -*-
# 앱 화면(HTML)과 아이콘. 내용을 바꿀 때는 이 파일이 아니라 app.py 의 "설정"을 고치면 됨.

PAGE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__SCHOOL__</title>
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/icon.png">
<link rel="icon" href="/icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="__SHORT__">
<meta name="theme-color" content="#f4f1ea" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14171b" media="(prefers-color-scheme: dark)">
<style>
:root{
  --bg:#f4f1ea; --card:#fffdf8; --ink:#1c2330; --sub:#6b7280; --line:#e2ddd0;
  --accent:#0b5d4b; --hero:#0b5d4b; --hero-ink:#f4f1ea; --hero-sub:#b9d6cd; --chip:#ebe6d9;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#14171b; --card:#1c2126; --ink:#eceae4; --sub:#9aa1ab; --line:#2a3037;
    --accent:#6fcfb6; --hero:#0e4d3f; --hero-ink:#f4f1ea; --hero-sub:#a5cdc1; --chip:#252b32;
  }
}
*{box-sizing:border-box; -webkit-tap-highlight-color:transparent}
html,body{margin:0; background:var(--bg); color:var(--ink)}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Pretendard","Noto Sans KR","Malgun Gothic",sans-serif;
  font-size:16px; line-height:1.5; word-break:keep-all;
  padding:calc(env(safe-area-inset-top) + 18px) 16px calc(env(safe-area-inset-bottom) + 40px);
}
main{max-width:560px; margin:0 auto}
header{display:flex; justify-content:space-between; align-items:baseline; margin:0 4px 14px}
header h1{font-size:17px; font-weight:700; margin:0; letter-spacing:-.01em}
header span{font-size:14px; color:var(--sub)}

.hero{background:var(--hero); color:var(--hero-ink); border-radius:22px; padding:22px 22px 18px}
.hero .when{font-size:14px; color:var(--hero-sub); margin:0 0 2px}
.hero h2{font-size:30px; font-weight:800; letter-spacing:-.02em; margin:0 0 14px}
.hero ul{list-style:none; margin:0; padding:0}
.hero li{font-size:19px; font-weight:500; padding:5px 0; border-bottom:1px solid rgba(255,255,255,.13)}
.hero li:last-child{border-bottom:0}
.hero .cal{font-size:13px; color:var(--hero-sub); margin:12px 0 0}
.hero .empty{font-size:16px; color:var(--hero-sub); margin:0; padding:6px 0 10px}
.hero button.retry{margin-top:6px; background:rgba(255,255,255,.16); color:var(--hero-ink); border:0; border-radius:10px; padding:8px 14px; font:inherit; font-size:14px}

.bar{display:flex; gap:8px; align-items:center; margin:12px 0 0}
.tabs{flex:1; display:flex; background:var(--chip); border-radius:12px; padding:3px}
.tabs button{flex:1; border:0; background:none; color:var(--sub); font:inherit; font-size:14px; font-weight:600; padding:8px 0; border-radius:9px}
.tabs button[aria-selected="true"]{background:var(--card); color:var(--ink); box-shadow:0 1px 2px rgba(0,0,0,.08)}
.tabs button:disabled{opacity:.35}
.nav{border:0; background:var(--chip); color:var(--ink); width:40px; height:40px; border-radius:12px; font-size:16px}
.today{display:none; margin:10px auto 0; border:0; background:none; color:var(--accent); font:inherit; font-size:14px; font-weight:600; padding:6px 10px}
.today.on{display:block}

section{margin-top:30px}
section h3{font-size:14px; font-weight:700; color:var(--sub); margin:0 4px 8px; letter-spacing:.02em}
.list{background:var(--card); border:1px solid var(--line); border-radius:16px; overflow:hidden}
.row{display:flex; align-items:center; gap:12px; padding:14px 16px; border-bottom:1px solid var(--line); color:inherit; text-decoration:none}
.row:last-child{border-bottom:0}
.row .body{flex:1; min-width:0}
.row .t{font-weight:600}
.row .d{font-size:13.5px; color:var(--sub); margin-top:1px}
.row .side{font-size:13px; color:var(--accent); font-weight:700; white-space:nowrap}
.row .date{font-size:13.5px; color:var(--sub); width:74px; flex:none; font-variant-numeric:tabular-nums}
.row .go{color:var(--sub); font-size:18px}
.row img{width:56px; height:56px; border-radius:10px; object-fit:cover; flex:none}
.tag{display:inline-block; font-size:12px; color:var(--accent); font-weight:700; margin-right:6px}
.muted{padding:14px 16px; color:var(--sub); font-size:14px}
footer{margin:34px 4px 0; font-size:12.5px; color:var(--sub); text-align:center}
a.row:active, button:active{opacity:.7}
button, a.row{cursor:pointer}
/* 컴퓨터처럼 넓은 화면: 왼쪽에 급식, 오른쪽에 바로가기·일정 */
@media (min-width: 900px){
  body{padding:36px 32px 56px}
  main{max-width:1040px}
  header{margin-bottom:20px}
  header h1{font-size:22px}
  header span{font-size:15px}
  .cols{display:grid; grid-template-columns:minmax(0,5fr) minmax(0,6fr); gap:36px; align-items:start}
  .left{position:sticky; top:28px}
  .right section:first-of-type{margin-top:0}
  .hero{padding:30px 30px 24px}
  .hero h2{font-size:36px}
  .hero li{font-size:20px}
  a.row:hover{background:var(--chip)}
  .tabs button:hover:not(:disabled), .nav:hover{color:var(--ink); filter:brightness(.97)}
}
</style>
</head>
<body>
<main>
  <header><h1>__SCHOOL__</h1><span id="clock"></span></header>

  <div class="cols">
  <div class="left">
  <div class="hero" id="hero" aria-live="polite">
    <p class="when" id="when">&nbsp;</p>
    <h2 id="title">급식</h2>
    <div id="menu"><p class="empty">불러오는 중…</p></div>
  </div>
  <div class="bar">
    <button class="nav" id="prev" aria-label="전날">◀</button>
    <div class="tabs" role="tablist" id="tabs"></div>
    <button class="nav" id="next" aria-label="다음 날">▶</button>
  </div>
  <button class="today" id="today">지금 급식으로 돌아가기</button>
  </div>
  <div class="right">

  <section id="s-links" hidden><h3>바로가기</h3><div class="list" id="links"></div></section>
  <section id="s-sched"><h3>학사일정</h3><div class="list" id="sched"><div class="muted">불러오는 중…</div></div></section>
  <section id="s-events" hidden><h3>행사</h3><div class="list" id="events"></div></section>
  <section id="s-promo" hidden><h3>소식</h3><div class="list" id="promo"></div></section>
  <section id="s-clubs" hidden><h3>동아리</h3><div class="list" id="clubs"></div></section>
  </div>
  </div>

  <footer>급식·학사일정 출처: 나이스 교육정보 개방 포털</footer>
</main>

<script>
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var NICK = {"1":"아침", "2":"점심", "3":"저녁"};
  var KINDS = ["1","2","3"];
  var state = {data:null, kind:"", manual:false};

  function el(tag, cls, text){
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function getJSON(url){
    return fetch(url, {cache:"no-store"}).then(function(r){ return r.json(); });
  }

  // ----- 급식 -----
  function drawMeal(){
    var d = state.data, menu = $("menu");
    menu.textContent = "";
    var by = {};
    (d.meals || []).forEach(function(m){ by[m.code] = m; });
    if (!by[state.kind]) state.kind = KINDS.filter(function(k){ return by[k]; })[0] || state.kind;
    var m = by[state.kind];

    $("title").textContent = (d.rel ? d.rel + " " : "") + (NICK[state.kind] || "급식");
    $("when").textContent = d.label + (d.rel ? "" : " 급식");

    var tabs = $("tabs"); tabs.textContent = "";
    KINDS.forEach(function(k){
      var b = el("button", "", NICK[k]);
      b.setAttribute("role", "tab");
      b.setAttribute("aria-selected", k === state.kind ? "true" : "false");
      b.disabled = !by[k];
      b.onclick = function(){ state.kind = k; state.manual = true; drawMeal(); };
      tabs.appendChild(b);
    });
    $("today").classList.toggle("on", state.manual);

    if (!m){
      menu.appendChild(el("p", "empty", d.error ? "급식을 불러오지 못했어요." : "급식 정보가 없어요. 주말·공휴일이거나 아직 식단이 올라오지 않았을 수 있어요."));
      if (d.error){
        var r = el("button", "retry", "다시 시도");
        r.onclick = function(){ loadMeal(d.date === "" ? "" : d.date); };
        menu.appendChild(r);
      }
      return;
    }
    var ul = el("ul");
    m.menu.forEach(function(x){ ul.appendChild(el("li", "", x)); });
    menu.appendChild(ul);
    if (m.cal) menu.appendChild(el("p", "cal", m.cal));
  }

  function loadMeal(ymd){
    return getJSON("/api/meal" + (ymd ? "?d=" + ymd : "")).then(function(d){
      state.data = d;
      if (!ymd){ state.kind = d.focus; state.manual = false; }
      drawMeal();
    }).catch(function(){
      state.data = {date: ymd || "", label: "", rel: "", meals: [], error: true, prev: "", next: ""};
      drawMeal();
    });
  }
  $("prev").onclick = function(){ if (state.data && state.data.prev){ state.manual = true; loadMeal(state.data.prev); } };
  $("next").onclick = function(){ if (state.data && state.data.next){ state.manual = true; loadMeal(state.data.next); } };
  $("today").onclick = function(){ loadMeal(""); };

  // ----- 아래 목록들 -----
  function row(o){
    var r = el(o.url ? "a" : "div", "row");
    if (o.url){ r.href = o.url; r.target = "_blank"; r.rel = "noopener"; }
    if (o.date) r.appendChild(el("span", "date", o.date));
    if (o.image){ var i = el("img"); i.src = o.image; i.alt = ""; i.loading = "lazy"; r.appendChild(i); }
    var b = el("div", "body");
    var t = el("div", "t");
    if (o.tag) t.appendChild(el("span", "tag", o.tag));
    t.appendChild(document.createTextNode(o.title || ""));
    b.appendChild(t);
    if (o.desc) b.appendChild(el("div", "d", o.desc));
    r.appendChild(b);
    if (o.side) r.appendChild(el("span", "side", o.side));
    if (o.url) r.appendChild(el("span", "go", "›"));
    return r;
  }
  function fill(sec, box, items, map){
    var s = $(sec), b = $(box);
    b.textContent = "";
    if (!items || !items.length){ s.hidden = true; return; }
    items.forEach(function(x){ b.appendChild(row(map(x))); });
    s.hidden = false;
  }
  function loadInfo(){
    return getJSON("/api/info").then(function(d){
      fill("s-links", "links", d.links, function(x){ return {title:x.title, desc:x.desc, url:x.url}; });
      fill("s-events", "events", d.events, function(x){ return {date:x.day, title:x.title, desc:x.desc, url:x.url, side:x.dday}; });
      fill("s-promo", "promo", d.promo, function(x){ return {title:x.title, desc:x.desc, url:x.url, image:x.image}; });
      fill("s-clubs", "clubs", d.clubs, function(x){ return {tag:x.category, title:x.name, desc:x.desc, url:x.url}; });
      var sc = $("sched"); sc.textContent = "";
      if (d.schedule === null) sc.appendChild(el("div", "muted", "학사일정을 불러오지 못했어요."));
      else if (!d.schedule.length) sc.appendChild(el("div", "muted", "앞으로 " + d.days + "일 동안 등록된 일정이 없어요."));
      else d.schedule.forEach(function(x){ sc.appendChild(row({date:x.day, title:x.name, side:x.dday})); });
    }).catch(function(){
      $("sched").textContent = "";
      $("sched").appendChild(el("div", "muted", "학사일정을 불러오지 못했어요."));
    });
  }

  function clock(){
    var n = new Date();
    $("clock").textContent = (n.getMonth() + 1) + "월 " + n.getDate() + "일 " + "일월화수목금토"[n.getDay()] + "요일";
  }

  clock(); loadMeal(""); loadInfo();
  // 앱을 다시 열면(다른 앱 갔다 오면) 지금 시간에 맞는 급식으로 새로 고침
  document.addEventListener("visibilitychange", function(){
    if (!document.hidden){ clock(); if (!state.manual) loadMeal(""); loadInfo(); }
  });
})();
</script>
</body>
</html>
"""

ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIAAQMAAADOtka5AAAABlBMVEX08eoLXUsFvG6RAAADTElEQVR42u3cQW7bMBAF0E+acLQIEC2zKBAdITeojpKbREdze5L2Bu7OBdywi7RAGHGsP44pGMHXJqBLvYjkkKKsaULGx44IAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgYH58f/3xZyiKlSMbB55zzjnvb4pipZ7x+REPOeecd6Eozg+rCUfsAQC7XBQbdKLVhD1eG4/Xxv8v8k348DDucQSADOzeFDUXBAgQIECAAAECBAgQIECAAAECBAgQIECAAAENgR4JAAIwvimu+ZLmgLucc84TiuKKL2kSegDAGIoiD2zwBAB43BZFx8u6b//euT0UxfkR9N9UBQgQIECAAAECBAhY4YnlhTvlq5lad+CAO/ORhwQOZh/sOeBoAj844MUEdmS/txtG9pznNR48BZw7jNMZ51y2CSN3TjCB4YxfGsuvbqgjmUDHAZ0JbDngseiQcgr+Wm7FzUFz4TTQOQdRnSigCqTlM3p1YmuA8AZ14gIQls8YP/ceidomrfWO5WxgdO2wPudcGLwnXF8Tetc29SqbsLjL6lpfQXLenK+wE6Pzznb5KwjO20KDN9+Ts/7lh3H0ranXuKgOzvqXv4Let6LNgc63njRoQvKtJw2uIPqWgwZXEHzLQSWJY/LlvTSYTKNrNreYzoOveoRrNqU1mtC5JmMFSK65RPXKyR5u0AfBNxUqCU2TKwUswhPLYZ3d+uCqHeGJ5UQBnScQa0DyBGKTToyeSK7VDq5ArKXWTZ5cxAhHKAZyizN49kMRjkhKJNA54qgKJEcc0c0yOyfCEQgjm2I5OdIxI/hACPRWd3BsiyP4QEg0cFsH7j92WUbLIvhxHPlM2YmvWs+U/Vm72s2Rb25PD4IBdPSHBrBdfMW2AARHgGd6GFz5ypVhqA+CFXQ9vU4ZwC05E0xgM//oyZf0PbEVraTvWS8afWiuwPfkGmECWy4ObSDQd1wrI373DnRnzv8uJ9+d+69UbbkusJvwLhKyP/m/iAQrCk5tyb6YBRLYMBPhFJC5PKGGX0S9cKlOetcmQMD1A2SyVcMrCOS3Gpm6Mdi1IvWgHM4ahYGqdeKf7pd3F/OsMIWyAAECBAgQIECAAAECBAgQIODywF+u1bkJ3NIsggAAAABJRU5ErkJggg=="
