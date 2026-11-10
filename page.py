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
<meta name="theme-color" content="#e9963c">
<style>
*{box-sizing:border-box; -webkit-tap-highlight-color:transparent}
html,body{margin:0; background:#fff; color:#222}
body{font-family:"Noto Sans KR","Malgun Gothic","Apple SD Gothic Neo",-apple-system,sans-serif; font-size:16px; line-height:1.5; word-break:keep-all}
a{color:inherit; text-decoration:none}
button{font:inherit; cursor:pointer}
.wrap{max-width:1000px; margin:0 auto}

.top{background:#e9963c; text-align:center; padding:calc(env(safe-area-inset-top) + 18px) 16px 16px}
.top b{display:block; font-size:25px; font-weight:800; letter-spacing:-.03em; color:#2a221b}
.top small{display:block; font-size:10.5px; letter-spacing:.06em; color:#7a5a36; font-weight:700; margin-top:-2px}
.bar{background:#6a5f53; color:#fff}
.bar .wrap{display:flex; align-items:stretch; justify-content:space-between}
.bar nav{display:flex; overflow-x:auto}
.bar nav a{padding:12px 13px; font-size:15px; font-weight:700; white-space:nowrap}
.bar nav a:first-child{background:#2b2520}
.bar span{padding:12px 13px; font-size:14px; color:#e6dfd6; white-space:nowrap}

.meal{background:#6a5f53; color:#fff; border-top:1px solid #7b7064}
.meal .wrap{padding:18px 16px 16px}
.mhead{display:flex; justify-content:space-between; align-items:baseline; gap:10px}
.mhead h2{font-size:22px; font-weight:800; margin:0; letter-spacing:-.02em}
.mhead span{font-size:14.5px; color:#e6dfd6}
.meal ul{list-style:none; margin:12px 0 0; padding:0}
.meal li{font-size:18px; padding:3px 0 3px 18px; position:relative}
.meal li:before{content:""; position:absolute; left:2px; top:14px; width:5px; height:5px; background:#3a332c}
.meal .cal{font-size:13px; color:#d8cfc4; margin:8px 0 0}
.meal .empty{font-size:15.5px; color:#e6dfd6; margin:12px 0 0}
.meal .retry{margin-top:8px; background:#fff; border:1px solid #333; padding:5px 12px; font-size:14px}
.mbar{display:flex; gap:6px; margin-top:14px}
.mbar button{background:#fff; color:#333; border:1px solid #4a4138; padding:7px 0; font-size:14.5px; font-weight:700}
.mbar .nav{width:42px}
.tabs{flex:1; display:flex; gap:6px}
.tabs button{flex:1}
.tabs button[aria-selected="true"]{background:#2b2520; color:#fff; border-color:#2b2520}
.tabs button:disabled{opacity:.45; cursor:default}
.today{display:none; margin-top:10px; background:none; border:0; color:#fff; font-size:14px; text-decoration:underline; padding:0}
.today.on{display:inline-block}

.body{padding-bottom:calc(env(safe-area-inset-bottom) + 30px)}
section{padding:22px 16px 18px; border-bottom:1px solid #d9d9d9}
.shead{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px}
.shead h3{font-size:22px; font-weight:800; letter-spacing:-.03em; margin:0}
.shead h3 i{font-style:normal; color:#e0a04a}
.shead a{font-size:14.5px; color:#333}
.row{display:flex; gap:12px; align-items:baseline; padding:5px 0 5px 18px; position:relative; font-size:17px}
.row:before{content:""; position:absolute; left:2px; top:16px; width:5px; height:5px; background:#333}
.row .body2{flex:1; min-width:0}
.row .t{display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.row .d{display:block; font-size:13.5px; color:#777; white-space:normal}
.row .side{font-size:16px; color:#444; white-space:nowrap; font-variant-numeric:tabular-nums}
.row .tag{color:#b9772a; font-weight:700; margin-right:6px}
.row img{width:54px; height:54px; object-fit:cover; flex:none; align-self:center}
a.row:hover .t, .links a:hover{text-decoration:underline}
.muted{color:#777; font-size:15px; padding:4px 0}
.grp{font-size:15px; font-weight:800; color:#6a5f53; margin:14px 0 2px}
.grp:first-child{margin-top:0}
.links{display:grid; grid-template-columns:1fr 1fr; column-gap:14px}
.links a{position:relative; padding:4px 0 4px 18px; font-size:16px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.links a:before{content:""; position:absolute; left:2px; top:15px; width:5px; height:5px; background:#333}
footer{padding:18px 16px 0; font-size:12.5px; color:#777; line-height:1.7}
footer a{text-decoration:underline}

@media (min-width: 900px){
  .top b{font-size:30px}
  .meal .wrap{padding:24px 16px 22px}
  .meal ul{columns:2; column-gap:40px}
  .mbar{max-width:460px}
  .cols{columns:2; column-gap:36px}
  .cols section{padding-left:0; padding-right:0; break-inside:avoid}
  .cols{padding:0 16px}
  .links{grid-template-columns:1fr 1fr 1fr 1fr}
  section.wide{padding-left:16px; padding-right:16px}
}
</style>
</head>
<body>
<div class="top"><div class="wrap"><b>__SCHOOL__</b><small>ULSAN SCIENCE HIGH SCHOOL</small></div></div>
<div class="bar"><div class="wrap">
  <nav><a href="#meal">급식</a><a href="#s-links">바로가기</a><a href="#s-sched">일정</a><a href="#s-news">기사</a><a href="#s-more">링크</a></nav>
  <span id="clock"></span>
</div></div>

<div class="meal" id="meal"><div class="wrap" aria-live="polite">
  <div class="mhead"><h2 id="title">급식</h2><span id="when"></span></div>
  <div id="menu"><p class="empty">불러오는 중…</p></div>
  <div class="mbar">
    <button class="nav" id="prev" aria-label="전날">◀</button>
    <div class="tabs" role="tablist" id="tabs"></div>
    <button class="nav" id="next" aria-label="다음 날">▶</button>
  </div>
  <button class="today" id="today">지금 급식으로 돌아가기</button>
</div></div>

<div class="wrap body">
  <div class="cols">
    <section id="s-links" hidden><div class="shead"><h3>바로가기</h3></div><div id="links"></div></section>
    <section id="s-sched"><div class="shead"><h3><i>학사</i>일정</h3><a id="homelink" hidden target="_blank" rel="noopener">학교 홈페이지 ⟩</a></div><div id="sched"><div class="muted">불러오는 중…</div></div></section>
    <section id="s-news" hidden><div class="shead"><h3><i>학교</i> 기사</h3><a href="https://news.google.com/search?q=%EC%9A%B8%EC%82%B0%EA%B3%BC%ED%95%99%EA%B3%A0&hl=ko&gl=KR&ceid=KR:ko" target="_blank" rel="noopener">더보기 ⟩</a></div><div id="news"></div></section>
    <section id="s-events" hidden><div class="shead"><h3>행사</h3></div><div id="events"></div></section>
    <section id="s-promo" hidden><div class="shead"><h3>소식</h3></div><div id="promo"></div></section>
    <section id="s-clubs" hidden><div class="shead"><h3>동아리</h3></div><div id="clubs"></div></section>
  </div>
  <section id="s-more" class="wide" hidden><div class="shead"><h3>링크 모음</h3></div><div id="more"></div></section>
  <footer>학생들이 편하게 쓰도록 만든 안내 페이지이며, 학교 공식 홈페이지가 아닙니다.<br>급식·학사일정: 나이스 교육정보 개방 포털 · 기사: 구글 뉴스</footer>
</div>

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
    $("when").textContent = d.label || "";

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
    if (o.image){ var i = el("img"); i.src = o.image; i.alt = ""; i.loading = "lazy"; r.appendChild(i); }
    var b = el("span", "body2");
    var t = el("span", "t");
    if (o.tag) t.appendChild(el("span", "tag", o.tag));
    t.appendChild(document.createTextNode(o.title || ""));
    b.appendChild(t);
    if (o.desc) b.appendChild(el("span", "d", o.desc));
    r.appendChild(b);
    if (o.side) r.appendChild(el("span", "side", o.side));
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
      fill("s-events", "events", d.events, function(x){ return {title:x.title, desc:x.desc, url:x.url, side:x.day}; });
      fill("s-promo", "promo", d.promo, function(x){ return {title:x.title, desc:x.desc, url:x.url, image:x.image}; });
      fill("s-clubs", "clubs", d.clubs, function(x){ return {tag:x.category, title:x.name, desc:x.desc, url:x.url}; });
      var mo = $("more"), groups = {}, order = [];
      mo.textContent = "";
      (d.more || []).forEach(function(x){
        if (!groups[x.group]){ groups[x.group] = []; order.push(x.group); }
        groups[x.group].push(x);
        if (x.title === "학교 홈페이지"){ $("homelink").href = x.url; $("homelink").hidden = false; }
      });
      order.forEach(function(g){
        mo.appendChild(el("div", "grp", g));
        var c = el("div", "links");
        groups[g].forEach(function(x){ var a = el("a", "", x.title); a.href = x.url; a.target = "_blank"; a.rel = "noopener"; c.appendChild(a); });
        mo.appendChild(c);
      });
      $("s-more").hidden = !order.length;
      var sc = $("sched"); sc.textContent = "";
      if (d.schedule === null) sc.appendChild(el("div", "muted", "학사일정을 불러오지 못했어요."));
      else if (!d.schedule.length) sc.appendChild(el("div", "muted", "앞으로 " + d.days + "일 동안 등록된 일정이 없어요."));
      else d.schedule.forEach(function(x){ sc.appendChild(row({title:x.name, side:x.day + " · " + x.dday})); });
    }).catch(function(){
      $("sched").textContent = "";
      $("sched").appendChild(el("div", "muted", "학사일정을 불러오지 못했어요."));
    });
  }
  function loadNews(){
    return getJSON("/api/news").then(function(d){
      fill("s-news", "news", d.items, function(x){ return {title:x.title, desc:x.source, url:x.url, side:(x.day || "").slice(2)}; });
    }).catch(function(){ $("s-news").hidden = true; });
  }

  function clock(){
    var n = new Date();
    $("clock").textContent = (n.getMonth() + 1) + "월 " + n.getDate() + "일 " + "일월화수목금토"[n.getDay()] + "요일";
  }

  clock(); loadMeal(""); loadInfo(); loadNews();
  // 앱을 다시 열면(다른 앱 갔다 오면) 지금 시간에 맞는 급식으로 새로 고침
  document.addEventListener("visibilitychange", function(){
    if (!document.hidden){ clock(); if (!state.manual) loadMeal(""); loadInfo(); }
  });
})();
</script>
</body>
</html>
"""

ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIAAQMAAADOtka5AAAABlBMVEX////pljz7hWlKAAADTElEQVR42u3cQW7bMBAF0E+acLQIEC2zKBAdITeojpKbREdze5L2Bu7OBdywi7RAGHGsP44pGMHXJqBLvYjkkKKsaULGx44IAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgYH58f/3xZyiKlSMbB55zzjnvb4pipZ7x+REPOeecd6Eozg+rCUfsAQC7XBQbdKLVhD1eG4/Xxv8v8k348DDucQSADOzeFDUXBAgQIECAAAECBAgQIECAAAECBAgQIECAAAENgR4JAAIwvimu+ZLmgLucc84TiuKKL2kSegDAGIoiD2zwBAB43BZFx8u6b//euT0UxfkR9N9UBQgQIECAAAECBAhY4YnlhTvlq5lad+CAO/ORhwQOZh/sOeBoAj844MUEdmS/txtG9pznNR48BZw7jNMZ51y2CSN3TjCB4YxfGsuvbqgjmUDHAZ0JbDngseiQcgr+Wm7FzUFz4TTQOQdRnSigCqTlM3p1YmuA8AZ14gIQls8YP/ceidomrfWO5WxgdO2wPudcGLwnXF8Tetc29SqbsLjL6lpfQXLenK+wE6Pzznb5KwjO20KDN9+Ts/7lh3H0ranXuKgOzvqXv4Let6LNgc63njRoQvKtJw2uIPqWgwZXEHzLQSWJY/LlvTSYTKNrNreYzoOveoRrNqU1mtC5JmMFSK65RPXKyR5u0AfBNxUqCU2TKwUswhPLYZ3d+uCqHeGJ5UQBnScQa0DyBGKTToyeSK7VDq5ArKXWTZ5cxAhHKAZyizN49kMRjkhKJNA54qgKJEcc0c0yOyfCEQgjm2I5OdIxI/hACPRWd3BsiyP4QEg0cFsH7j92WUbLIvhxHPlM2YmvWs+U/Vm72s2Rb25PD4IBdPSHBrBdfMW2AARHgGd6GFz5ypVhqA+CFXQ9vU4ZwC05E0xgM//oyZf0PbEVraTvWS8afWiuwPfkGmECWy4ObSDQd1wrI373DnRnzv8uJ9+d+69UbbkusJvwLhKyP/m/iAQrCk5tyb6YBRLYMBPhFJC5PKGGX0S9cKlOetcmQMD1A2SyVcMrCOS3Gpm6Mdi1IvWgHM4ahYGqdeKf7pd3F/OsMIWyAAECBAgQIECAAAECBAgQIODywF+u1bkJ3NIsggAAAABJRU5ErkJggg=="
