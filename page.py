# -*- coding: utf-8 -*-
# 앱 화면(HTML)과 아이콘. 내용을 바꿀 때는 이 파일이 아니라 app.py 의 "설정"을 고치면 됨.

PAGE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__SCHOOL__</title>
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/icon.png?v=2">
<link rel="icon" href="/icon.png?v=2">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="__SHORT__">
<meta name="theme-color" content="#e9963c">
<style>
*{box-sizing:border-box; -webkit-tap-highlight-color:transparent}
[hidden]{display:none !important}
html,body{margin:0; background:#fff; color:#222}
body{font-family:"Noto Sans KR","Malgun Gothic","Apple SD Gothic Neo",-apple-system,sans-serif; font-size:16px; line-height:1.5; word-break:keep-all}
a{color:inherit; text-decoration:none}
button{font:inherit; cursor:pointer}
.wrap{max-width:1000px; margin:0 auto}

.top{background:#e9963c; text-align:center; padding:calc(env(safe-area-inset-top) + 18px) 16px 16px}
.top img{width:46px; height:46px; border-radius:50%; vertical-align:middle; margin-right:10px}
.top .nm{display:inline-block; vertical-align:middle; text-align:left}
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
.row .d{white-space:pre-line}
.noti{margin-top:12px; font-size:14px; color:#e6dfd6; display:flex; flex-wrap:wrap; gap:6px 10px; align-items:center}
.noti button{background:#fff; color:#333; border:1px solid #4a4138; padding:6px 12px; font-size:14px; font-weight:700}
.noti ol{margin:4px 0 0; padding-left:20px; flex-basis:100%; line-height:1.7}
.noti ol li{font-size:14px; padding:0}
.noti ol li:before{display:none}
.noti b{color:#fff}
.noti button.on{background:#2b2520; color:#fff; border-color:#2b2520}
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
.row .d{display:block; font-size:13.5px; color:#777; white-space:pre-line}
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
.cbtn{background:#fff; color:#333; border:1px solid #4a4138; padding:8px 16px; font-size:15.5px; font-weight:700}
.chips{display:flex; flex-wrap:wrap; gap:6px; margin:12px 0 6px}
.chips button{background:#fff; color:#333; border:1px solid #4a4138; padding:6px 12px; font-size:14.5px; font-weight:700}
.chips button[aria-pressed="true"]{background:#2b2520; color:#fff; border-color:#2b2520}
.chips.sub{margin-top:0}
.chips.sub button{font-size:13.5px; padding:4px 10px; border-color:#8a8076; font-weight:400}
.chips.sub button[aria-pressed="true"]{background:#6a5f53; border-color:#6a5f53; font-weight:700}
.sub{font-size:13.5px; font-weight:700; color:#b9772a; margin:10px 0 0}
.sgrp .sub:first-child{margin-top:4px}
.sgrp:not(.open) .x2{display:none}
.morebtn{margin-top:10px; background:#fff; color:#333; border:1px solid #4a4138; padding:7px 14px; font-size:14.5px; font-weight:700}
.fav{width:18px; height:18px; flex:none; align-self:center; object-fit:contain}
.row.hasfav{padding-left:0}
.row.hasfav:before{display:none}
.links a.hasfav{padding-left:0; display:flex; align-items:center; gap:8px}
.links a.hasfav:before{display:none}
.links a.hasfav span{overflow:hidden; text-overflow:ellipsis}
.find{background:#f3f1ee; border-bottom:1px solid #d9d9d9}
.find .wrap{padding:10px 16px}
.find input{width:100%; border:1px solid #8a8076; padding:9px 11px; font:inherit; font-size:16px; background:#fff; color:#222; border-radius:0; -webkit-appearance:none}
#hits{margin-top:6px; background:#fff; border:1px solid #c9c4be; max-height:60vh; overflow:auto}
#hits .row{padding:8px 10px 8px 26px; border-bottom:1px solid #eee; cursor:pointer}
#hits .row:before{left:11px; top:19px}
#hits .row:last-child{border-bottom:0}
#hits .muted{padding:8px 10px}
.ftabs{display:flex; gap:6px; margin-bottom:10px}
.ftabs button{flex:1; max-width:90px; background:#fff; color:#333; border:1px solid #4a4138; padding:7px 0; font-size:15px; font-weight:800}
.ftabs button[aria-selected="true"]{background:#2b2520; color:#fff}
#mapbox{border:1px solid #d9d9d9; background:#fff; max-width:760px}
#mapbox svg{display:block; width:100%; height:auto}
#mapbox text{font-family:inherit; font-weight:700; fill:#222; text-anchor:middle}
#mapbox text.hit{fill:#d6007f}
.legend{display:flex; flex-wrap:wrap; gap:6px 16px; font-size:13.5px; color:#444; margin-top:8px; align-items:center}
.legend span{display:inline-flex; align-items:center; gap:5px}
.legend svg{width:18px; height:18px}
.conn b{display:block; font-size:18px}
.conn p{margin:2px 0 8px; font-size:14.5px; color:#555}
.copy{display:flex; gap:6px; margin-bottom:10px}
.copy input{flex:1; min-width:0; border:1px solid #999; padding:7px 9px; font:14px/1.3 Consolas,Menlo,monospace; color:#222; background:#f6f6f6}
.copy button{background:#6a5f53; color:#fff; border:0; padding:0 14px; font-size:14.5px; font-weight:700; white-space:nowrap}
.conn .how{font-size:14.5px; color:#333; padding-left:18px; position:relative; margin:3px 0}
.conn .how:before{content:""; position:absolute; left:2px; top:10px; width:5px; height:5px; background:#333}
.conn .ex{font-size:14px; color:#555; margin:8px 0 0}
.conn .note{font-size:14px; color:#b3261e; margin:8px 0 0}
footer{padding:18px 16px 0; font-size:12.5px; color:#777; line-height:1.7}
footer a{text-decoration:underline}

@media (max-width: 520px){ .bar span{display:none} }
@media (min-width: 900px){
  .top b{font-size:30px}
  .meal .wrap{padding:24px 16px 22px}
  .meal ul{columns:2; column-gap:40px}
  .mbar{max-width:460px}
  .cols{columns:2; column-gap:36px}
  .cols section{padding-left:0; padding-right:0; break-inside:avoid}
  .cols{padding:0 16px}
  .links{grid-template-columns:1fr 1fr 1fr 1fr}
  .sgrp:not(.open) .links a.x2{display:flex}
  .sgrp:not(.open) .links a.x4{display:none}
  section.wide{padding-left:16px; padding-right:16px}
}
</style>
</head>
<body>
<div class="top"><div class="wrap"><img src="/icon.png?v=2" alt=""><span class="nm"><b>__SCHOOL__</b><small>ULSAN SCIENCE HIGH SCHOOL</small></span></div></div>
<div class="bar"><div class="wrap">
  <nav><a href="#meal">급식</a><a href="https://script.google.com/a/macros/ushs.hs.kr/s/AKfycby2gOXvtxIrsN8IEo8oOp2D0up47iO7iImfhoiqHPYY-iCouFVPZY330BDXmFn_7t0A/exec" target="_blank" rel="noopener">게시판</a><a href="https://pf.kakao.com/_VGtxeX/chat" target="_blank" rel="noopener">챗봇</a><a href="#s-clubs" id="navclub">동아리</a><a href="#s-links">바로가기</a><a href="#s-sched">일정</a><a href="#s-news">기사</a><a href="#s-map">지도</a><a href="#s-conn">AI</a><a href="#s-more">링크</a></nav>
  <span id="clock"></span>
</div></div>

<div class="find"><div class="wrap">
  <input id="q" type="search" placeholder="검색: 교실 이름, 링크, 일정, 기사" autocomplete="off" aria-label="검색">
  <div id="hits" hidden></div>
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
  <div class="noti" id="noti" hidden><button id="nbtn"></button><button id="ntest" hidden>알림 시험해 보기</button><button id="nopen" hidden></button><button id="ninst" hidden>홈 화면에 앱 설치</button><span id="nmsg"></span></div>
</div></div>

<div class="wrap body">
  <div class="cols">
    <section id="s-links" hidden><div class="shead"><h3>바로가기</h3></div><div id="links"></div></section>
    <section id="s-clubs" hidden><div class="shead"><h3>동아리</h3></div><button id="cbtn" class="cbtn">동아리 살펴보기</button><div id="cpanel" hidden><div class="chips" id="ccat"></div><div class="chips sub" id="csub" hidden></div><div id="clubs"></div></div></section>
    <section id="s-sched"><div class="shead"><h3><i>학사</i>일정</h3><a id="homelink" hidden target="_blank" rel="noopener">학교 홈페이지 ⟩</a></div><div id="sched"><div class="muted">불러오는 중…</div></div></section>
    <section id="s-news" hidden><div class="shead"><h3><i>학교</i> 기사</h3><a href="https://news.google.com/search?q=%EC%9A%B8%EC%82%B0%EA%B3%BC%ED%95%99%EA%B3%A0&hl=ko&gl=KR&ceid=KR:ko" target="_blank" rel="noopener">더보기 ⟩</a></div><div id="news"></div></section>
    <section id="s-events" hidden><div class="shead"><h3>행사</h3></div><div id="events"></div></section>
    <section id="s-promo" hidden><div class="shead"><h3>소식</h3></div><div id="promo"></div></section>
  </div>
  <section id="s-map" class="wide" hidden><div class="shead"><h3><i>학교</i> 지도</h3></div>
    <div class="ftabs" id="ftabs" role="tablist"></div>
    <div id="mapbox"></div>
    <div class="legend">
      <span><svg viewBox="0 0 18 18"><rect x="3" y="1" width="12" height="16" fill="#2f6fe4"/></svg>남자화장실</span>
      <span><svg viewBox="0 0 18 18"><rect x="3" y="1" width="12" height="16" fill="#e0443c"/></svg>여자화장실</span>
      <span><svg viewBox="0 0 18 18"><circle cx="9" cy="9" r="7" fill="#fff" stroke="#222" stroke-width="2"/><circle cx="9" cy="9" r="2.5" fill="#222"/></svg>승강기</span>
      <span><svg viewBox="0 0 18 18"><path d="M2 15h4v-4h4V7h4V3h2" fill="none" stroke="#222" stroke-width="2"/></svg>계단</span>
      <span id="mapby"></span>
    </div>
  </section>
  <section id="s-conn" class="wide" hidden><div class="shead"><h3><i>AI</i> 커넥터</h3></div><div id="conn"></div></section>
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
  function fav(url){
    var i = el("img", "fav"), host = "";
    try { host = new URL(url).hostname; } catch (e) {}
    i.alt = ""; i.loading = "lazy"; i.referrerPolicy = "no-referrer";
    i.onerror = function(){ i.style.visibility = "hidden"; };
    i.src = "https://www.google.com/s2/favicons?sz=64&domain=" + encodeURIComponent(host);
    return i;
  }
  function row(o){
    var r = el(o.url ? "a" : "div", "row");
    if (o.url){ r.href = o.url; r.target = "_blank"; r.rel = "noopener"; }
    if (o.fav && o.url){ r.classList.add("hasfav"); r.appendChild(fav(o.url)); }
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
      fill("s-links", "links", d.links, function(x){ return {title:x.title, desc:[x.desc, x.by].filter(Boolean).join("\n"), url:x.url}; });
      INFO = d; $("mapby").textContent = d.mapBy || ""; 
      fill("s-events", "events", d.events, function(x){ return {title:x.title, desc:x.desc, url:x.url, side:x.day}; });
      fill("s-promo", "promo", d.promo, function(x){ return {title:x.title, desc:x.desc, url:x.url, image:x.image}; });
      CLUBS = d.clubs || []; $("s-clubs").hidden = !CLUBS.length; if (!$("cpanel").hidden) drawClubs();
      var mo = $("more"), groups = {}, order = [];
      mo.textContent = "";
      (d.more || []).forEach(function(x){
        if (!groups[x.group]){ groups[x.group] = []; order.push(x.group); }
        groups[x.group].push(x);
        if (x.title === "학교 홈페이지"){ $("homelink").href = x.url; $("homelink").hidden = false; }
      });
      var linkA = function(x){ var a = el("a", "hasfav"); a.href = x.url; a.target = "_blank"; a.rel = "noopener"; a.appendChild(fav(x.url)); a.appendChild(el("span", "", x.title)); return a; };
      order.forEach(function(g){
        mo.appendChild(el("div", "grp", g));
        var subs = {}, sorder = [];
        groups[g].forEach(function(x){ var s = x.sub || ""; if (!subs[s]){ subs[s] = []; sorder.push(s); } subs[s].push(x); });
        if (sorder.length === 1 && !sorder[0]){
          var c = el("div", "links");
          groups[g].forEach(function(x){ c.appendChild(linkA(x)); });
          mo.appendChild(c);
          return;
        }
        // 갈래(과목·기능)마다 앞쪽 몇 개만 먼저 보여 주고, "더 알아보기"를 누르면 나머지가 펼쳐진다
        var wrap = el("div", "sgrp" + (OPENG[g] ? " open" : "")), hidden = 0;
        sorder.forEach(function(s){
          if (s) wrap.appendChild(el("div", "sub", s));
          var c = el("div", "links");
          subs[s].forEach(function(x, k){ var a = linkA(x); if (k >= 2){ a.classList.add("x2"); hidden++; } if (k >= 4) a.classList.add("x4"); c.appendChild(a); });
          wrap.appendChild(c);
        });
        mo.appendChild(wrap);
        if (!hidden) return;
        var mb = el("button", "morebtn");
        var label = function(){ mb.textContent = OPENG[g] ? g + " 접기" : g + " 더 알아보기 (" + groups[g].length + "개)"; mb.setAttribute("aria-expanded", OPENG[g] ? "true" : "false"); };
        mb.onclick = function(){ OPENG[g] = !OPENG[g]; wrap.classList.toggle("open", !!OPENG[g]); label(); };
        label(); mo.appendChild(mb);
      });
      $("s-more").hidden = !order.length;
      var cn = $("conn"); cn.textContent = "";
      (d.connectors || []).forEach(function(c){
        var box = el("div", "conn");
        box.appendChild(el("b", "", c.title));
        box.appendChild(el("p", "", c.desc + " 아래 주소는 사이트가 아니라 AI 설정에 붙여 넣는 주소예요." + (c.by ? " (" + c.by + ")" : "")));
        var cp = el("div", "copy"), inp = el("input"), bt = el("button", "", "주소 복사");
        inp.readOnly = true; inp.value = c.url; inp.setAttribute("aria-label", c.title + " 커넥터 주소");
        inp.onfocus = function(){ inp.select(); };
        bt.onclick = function(){
          var done = function(){ bt.textContent = "복사됨"; setTimeout(function(){ bt.textContent = "주소 복사"; }, 1500); };
          if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(c.url).then(done, function(){ inp.select(); });
          else { inp.select(); try { document.execCommand("copy"); done(); } catch (e) {} }
        };
        cp.appendChild(inp); cp.appendChild(bt); box.appendChild(cp);
        (c.how || []).forEach(function(h){ box.appendChild(el("div", "how", h)); });
        if (c.examples && c.examples.length) box.appendChild(el("div", "ex", "이렇게 물어보세요: " + c.examples.join(" / ")));
        if (c.note) box.appendChild(el("div", "note", c.note));
        cn.appendChild(box);
      });
      $("s-conn").hidden = !(d.connectors || []).length;
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
      NEWS = d.items || [];
      fill("s-news", "news", d.items, function(x){ return {title:x.title, desc:x.source, url:x.url, side:(x.day || "").slice(2)}; });
    }).catch(function(){ $("s-news").hidden = true; });
  }

  // ----- 동아리 살펴보기 -----
  // 위쪽 버튼(전체·창체·학술·자율·유네스코)을 누르면 그 분류만 걸러서 보여 줌. 자율은 한 줄 더 나와서 예체능·학술·취미 등으로 다시 거름
  var CLUBS = [], ccat = "", csub = "";
  function uniq(list){ var o = []; list.forEach(function(x){ if (x && o.indexOf(x) < 0) o.push(x); }); return o; }
  function chip(box, label, on, fn){ var b = el("button", "", label); b.setAttribute("aria-pressed", on ? "true" : "false"); b.onclick = fn; box.appendChild(b); }
  function drawClubs(){
    var count = function(list, key, v){ return list.filter(function(c){ return c[key] === v; }).length; };
    var cb = $("ccat"); cb.textContent = "";
    chip(cb, "전체 " + CLUBS.length, !ccat, function(){ ccat = ""; csub = ""; drawClubs(); });
    uniq(CLUBS.map(function(c){ return c.category; })).forEach(function(k){
      chip(cb, k + " " + count(CLUBS, "category", k), ccat === k, function(){ ccat = k; csub = ""; drawClubs(); });
    });
    var inCat = CLUBS.filter(function(c){ return !ccat || c.category === ccat; });
    var subs = ccat ? uniq(inCat.map(function(c){ return c.sub; })) : [];
    var sb = $("csub"); sb.textContent = ""; sb.hidden = !subs.length;
    if (subs.length){
      chip(sb, "전체", !csub, function(){ csub = ""; drawClubs(); });
      subs.forEach(function(k){ chip(sb, k + " " + count(inCat, "sub", k), csub === k, function(){ csub = k; drawClubs(); }); });
    }
    var box = $("clubs"); box.textContent = "";
    inCat.filter(function(c){ return !csub || c.sub === csub; }).forEach(function(x){
      box.appendChild(row({tag: x.sub ? x.category + "·" + x.sub : x.category, title: x.name, desc: x.desc, url: x.url}));
    });
  }
  function openClubs(){ if ($("cpanel").hidden){ $("cpanel").hidden = false; $("cbtn").textContent = "동아리 접기"; drawClubs(); } }
  $("cbtn").onclick = function(){
    if ($("cpanel").hidden) return openClubs();
    $("cpanel").hidden = true; $("cbtn").textContent = "동아리 살펴보기";
  };
  $("navclub").onclick = function(e){ e.preventDefault(); go("s-clubs"); };

  // ----- 학교 지도 -----
  var NS = "http://www.w3.org/2000/svg", MAP = [], INFO = {}, NEWS = [], OPENG = {}, floorNow = 0, hitRoom = "";
  function sv(tag, at){ var e = document.createElementNS(NS, tag); for (var k in at) e.setAttribute(k, at[k]); return e; }
  function norm(s){ return (s || "").toLowerCase().replace(/\s+/g, ""); }
  function drawMap(){
    var f = MAP[floorNow], box = $("mapbox"); if (!f) return;
    box.textContent = "";
    var s = sv("svg", {viewBox: "0 0 " + f.w + " " + f.h, role: "img", "aria-label": f.n + " 지도"});
    f.p.forEach(function(p){ s.appendChild(sv("polygon", {points: p.join(" "), fill: "#fdf3f8", stroke: "#6a5f53", "stroke-width": 2.5, "stroke-linejoin": "round"})); });
    f.s.forEach(function(g){ s.appendChild(sv("line", {x1: g[0], y1: g[1], x2: g[2], y2: g[3], stroke: "#bfb3ba", "stroke-width": 2})); });
    f.i.forEach(function(i){
      var x = i[1], y = i[2];
      if (i[0] === "m" || i[0] === "f") s.appendChild(sv("rect", {x: x - 9, y: y - 13, width: 18, height: 26, fill: i[0] === "m" ? "#2f6fe4" : "#e0443c"}));
      else if (i[0] === "e"){ s.appendChild(sv("circle", {cx: x, cy: y, r: 9, fill: "#fff", stroke: "#222", "stroke-width": 2.5})); s.appendChild(sv("circle", {cx: x, cy: y, r: 3, fill: "#222"})); }
      else s.appendChild(sv("path", {d: "M" + (x - 11) + " " + (y + 9) + "h6v-6h6v-6h6v-6h4", fill: "none", stroke: "#222", "stroke-width": 2.5}));
    });
    f.t.forEach(function(t){
      var lines = t[3].split("|"), big = t[2] > 25, fs = big ? 30 : 15, lh = fs * 1.15;
      var hit = hitRoom && norm(t[3].replace(/\|/g, "")) === hitRoom;
      if (hit) s.appendChild(sv("circle", {cx: t[0], cy: t[1], r: big ? 70 : 46, fill: "#ffe3f3", stroke: "#d6007f", "stroke-width": 3}));
      var tx = sv("text", {x: t[0], y: t[1] - (lines.length - 1) * lh / 2 + fs * 0.36, "font-size": fs});
      if (hit) tx.setAttribute("class", "hit");
      lines.forEach(function(l, k){ var sp = sv("tspan", {x: t[0]}); if (k) sp.setAttribute("dy", lh); sp.textContent = l; tx.appendChild(sp); });
      s.appendChild(tx);
    });
    box.appendChild(s);
    var tabs = $("ftabs"); tabs.textContent = "";
    MAP.forEach(function(m, k){
      var b = el("button", "", m.n); b.setAttribute("role", "tab"); b.setAttribute("aria-selected", k === floorNow ? "true" : "false");
      b.onclick = function(){ floorNow = k; hitRoom = ""; drawMap(); };
      tabs.appendChild(b);
    });
  }
  function loadMap(){
    return getJSON("/api/map").then(function(d){ MAP = d || []; $("s-map").hidden = !MAP.length; drawMap(); }).catch(function(){ $("s-map").hidden = true; });
  }

  // ----- 급식 알림 -----
  var pushKey = "", swReg = null;
  function b64u(s){ var p = (s + "===".slice((s.length + 3) % 4)).replace(/-/g, "+").replace(/_/g, "/"), r = atob(p), a = new Uint8Array(r.length); for (var i = 0; i < r.length; i++) a[i] = r.charCodeAt(i); return a; }
  function post(url, body){ return fetch(url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)}).then(function(r){ return r.json(); }); }
  function notiUI(sub, msg){
    $("noti").hidden = false;
    $("nbtn").textContent = sub ? "급식 알림 끄기" : "급식 알림 받기";
    $("nbtn").className = sub ? "on" : "";
    $("ntest").hidden = !sub;
    $("nmsg").textContent = msg != null ? msg : (sub ? "매일 7시 · 12시 · 18시에 알려 드려요." : "아침 7시 · 점심 12시 · 저녁 6시");
  }
  function initPush(){
    var ua = navigator.userAgent, ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    var inapp = /KAKAOTALK|NAVER\(|Instagram|FBAN|FBAV|Line\/|DaumApps|everytimeApp|; wv\)/i.test(ua);
    function cant(msg){ $("noti").hidden = false; $("nbtn").hidden = true; $("ntest").hidden = true; $("nmsg").textContent = msg; }
    function steps(title, list){
      cant(title);
      var ol = el("ol");
      list.forEach(function(t){ var li = el("li"); li.innerHTML = t; ol.appendChild(li); });
      $("noti").appendChild(ol);
    }
    var standalone = navigator.standalone === true || (window.matchMedia && matchMedia("(display-mode: standalone)").matches);
    var here = location.host + location.pathname;
    if (inapp){
      // 카톡·네이버 같은 앱 안의 브라우저는 알림을 못 켜므로, 한 번 눌러서 진짜 브라우저로 넘어가게 함
      var ext = /KAKAOTALK/i.test(ua) ? "kakaotalk://web/openExternal?url=" + encodeURIComponent("https://" + here)
              : ios ? "x-safari-https://" + here
              : "intent://" + here + "#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url=" + encodeURIComponent("https://" + here) + ";end";
      cant("급식 알림은 " + (ios ? "사파리" : "크롬") + "에서 켤 수 있어요.");
      $("nopen").hidden = false;
      $("nopen").textContent = ios ? "사파리로 열기" : "크롬으로 열기";
      $("nopen").setAttribute("data-href", ext);
      $("nopen").onclick = function(){ location.href = ext; };
      return;
    }
    if (ios && !standalone){
      steps("아이폰은 홈 화면에 추가해야 급식 알림을 받을 수 있어요. 한 번만 하면 돼요.", [
        "화면 아래(또는 위)의 <b>공유 버튼</b>(네모에서 화살표가 나오는 모양)을 눌러요.",
        "<b>홈 화면에 추가</b>를 누르고 <b>추가</b>를 눌러요.",
        "홈 화면에 생긴 <b>__SHORT__</b> 앱을 열고 <b>급식 알림 받기</b>를 눌러요."]);
      return;
    }
    if (!("serviceWorker" in navigator) || !("PushManager" in window) || !("Notification" in window)){
      cant(ios ? "급식 알림: 아이폰 소프트웨어를 16.4 이상으로 업데이트하면 켤 수 있어요." : "급식 알림: 이 브라우저에서는 켤 수 없어요. 크롬이나 삼성 인터넷으로 열어 주세요.");
      return;
    }
    getJSON("/api/push/key").then(function(k){
      if (!k.on) return;
      pushKey = k.key;
      return navigator.serviceWorker.register("/sw.js").then(function(reg){
        swReg = reg;
        return reg.pushManager.getSubscription();
      }).then(function(sub){
        if (sub) post("/api/push/subscribe", sub.toJSON()).catch(function(){});   // 서버가 다시 켜졌어도 구독이 살아 있도록 다시 알려 줌
        notiUI(sub);
      });
    }).catch(function(){ cant("급식 알림을 준비하지 못했어요. 새로 고침한 뒤 다시 확인해 주세요."); });
  }
  $("nbtn").onclick = function(){
    if (!swReg) return;
    swReg.pushManager.getSubscription().then(function(sub){
      if (sub){
        var ep = sub.endpoint;
        return sub.unsubscribe().then(function(){ post("/api/push/unsubscribe", {endpoint: ep}).catch(function(){}); notiUI(null, "알림을 껐어요."); });
      }
      return Notification.requestPermission().then(function(p){
        if (p !== "granted"){ notiUI(null, "브라우저에서 알림이 차단되어 있어요. 주소창 왼쪽 자물쇠 → 알림을 '허용'으로 바꿔 주세요."); return; }
        return swReg.pushManager.subscribe({userVisibleOnly: true, applicationServerKey: b64u(pushKey)}).then(function(s){
          var body = s.toJSON(); body.hello = true;
          return post("/api/push/subscribe", body).then(function(r){ notiUI(r.ok ? s : null, r.ok ? "알림을 켰어요. 확인 알림이 곧 도착해요." : "알림 등록에 실패했어요. 잠시 뒤 다시 눌러 주세요."); });
        });
      });
    }).catch(function(){ notiUI(null, "알림을 켜지 못했어요. 잠시 뒤 다시 눌러 주세요."); });
  };
  // 안드로이드 크롬: 한 번 눌러 홈 화면에 앱으로 설치
  var instEvt = null;
  window.addEventListener("beforeinstallprompt", function(e){ e.preventDefault(); instEvt = e; $("noti").hidden = false; $("ninst").hidden = false; });
  window.addEventListener("appinstalled", function(){ $("ninst").hidden = true; });
  $("ninst").onclick = function(){ if (instEvt){ instEvt.prompt(); instEvt = null; $("ninst").hidden = true; } };
  $("ntest").onclick = function(){
    swReg.pushManager.getSubscription().then(function(sub){
      if (!sub) return;
      $("nmsg").textContent = "시험 알림을 보내는 중…";
      return post("/api/push/subscribe", sub.toJSON()).then(function(){ return post("/api/push/test", {endpoint: sub.endpoint}); })
        .then(function(r){ $("nmsg").textContent = r.ok ? "시험 알림을 보냈어요. 몇 초 안에 도착해요." : "시험 알림을 보내지 못했어요."; });
    }).catch(function(){ $("nmsg").textContent = "시험 알림을 보내지 못했어요."; });
  };

  // ----- 검색 -----
  function go(id){ if (id === "s-clubs") openClubs(); var e = $(id); if (e && !e.hidden) e.scrollIntoView({behavior: "smooth", block: "start"}); }
  function search(q){
    var n = norm(q), out = [], seen = {};
    if (!n) return out;
    function add(kind, title, sub, act){ var k = kind + title; if (!seen[k] && norm(title + sub).indexOf(n) >= 0){ seen[k] = 1; out.push({kind: kind, title: title, sub: sub, act: act}); } }
    MAP.forEach(function(f, k){ f.t.forEach(function(t){ var name = t[3].replace(/\|/g, " "); add("교실", name, f.n[0] + "층", {floor: k, room: norm(name)}); }); });
    (INFO.links || []).forEach(function(x){ add("바로가기", x.title, x.desc, {url: x.url}); });
    (INFO.more || []).forEach(function(x){ add("링크", x.title, x.group + (x.sub ? " · " + x.sub : ""), {url: x.url}); });
    (INFO.connectors || []).forEach(function(x){ add("AI 커넥터", x.title, x.desc, {sec: "s-conn"}); });
    (INFO.schedule || []).forEach(function(x){ add("일정", x.name, x.day + " · " + x.dday, {sec: "s-sched"}); });
    (INFO.events || []).forEach(function(x){ add("행사", x.title, x.day, {sec: "s-events"}); });
    (INFO.clubs || []).forEach(function(x){ add("동아리", x.name, x.desc, {sec: "s-clubs"}); });
    (INFO.promo || []).forEach(function(x){ add("소식", x.title, x.desc, {sec: "s-promo"}); });
    NEWS.forEach(function(x){ add("기사", x.title, x.source + " · " + x.day, {url: x.url}); });
    if ("급식아침점심저녁조식중식석식".indexOf(n) >= 0) out.push({kind: "급식", title: "급식 보기", sub: "", act: {sec: "meal"}});
    return out.slice(0, 30);
  }
  function showHits(){
    var q = $("q").value, box = $("hits"); box.textContent = "";
    if (!norm(q)){ box.hidden = true; return; }
    var res = search(q); box.hidden = false;
    if (!res.length){ box.appendChild(el("div", "muted", "'" + q + "' 검색 결과가 없어요.")); return; }
    res.forEach(function(h){
      var r = row({tag: h.kind, title: h.title, desc: h.sub, url: h.act.url});
      if (!h.act.url){ r.setAttribute("role", "button"); r.tabIndex = 0;
        r.onclick = function(){
          if (h.act.room){ floorNow = h.act.floor; hitRoom = h.act.room; drawMap(); go("s-map"); } else go(h.act.sec);
          box.hidden = true;
        };
        r.onkeydown = function(e){ if (e.key === "Enter") r.onclick(); };
      }
      box.appendChild(r);
    });
  }
  $("q").addEventListener("input", showHits);
  $("q").addEventListener("focus", showHits);

  function clock(){
    var n = new Date();
    $("clock").textContent = (n.getMonth() + 1) + "월 " + n.getDate() + "일 " + "일월화수목금토"[n.getDay()] + "요일";
  }

  clock(); loadMeal(""); loadInfo(); loadNews(); loadMap(); initPush();
  // 앱을 다시 열면(다른 앱 갔다 오면) 지금 시간에 맞는 급식으로 새로 고침
  document.addEventListener("visibilitychange", function(){
    if (!document.hidden){ clock(); if (!state.manual) loadMeal(""); loadInfo(); }
  });
})();
</script>
</body>
</html>
"""

SW = r"""self.addEventListener("install", function(e){ self.skipWaiting(); });
self.addEventListener("activate", function(e){ e.waitUntil(self.clients.claim()); });
self.addEventListener("push", function(e){
  var d = {};
  try { d = e.data.json(); } catch (x) {}
  e.waitUntil(self.registration.showNotification(d.title || "급식 알림", {body: d.body || "", icon: "/icon.png?v=2", badge: "/icon.png?v=2", tag: d.tag || "meal", data: {url: d.url || "/"}}));
});
self.addEventListener("notificationclick", function(e){
  e.notification.close();
  e.waitUntil(self.clients.matchAll({type: "window", includeUncontrolled: true}).then(function(list){
    for (var i = 0; i < list.length; i++){ if ("focus" in list[i]) return list[i].focus(); }
    return self.clients.openWindow(e.notification.data.url);
  }));
});
"""

ICON_B64 = "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"
