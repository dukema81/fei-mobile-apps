# -*- coding: utf-8 -*-
"""「飞」系系统 · 手机APP(PWA) 批量生成器
用法: python gen_all.py [proj ...]   缺省生成全部（跳过 feiyang-otms 专属版）
"""
import io
import json
import os
import sys

CLAW = r"C:/Users/maxl/WorkBuddy/Claw"

# name=APP名(=项目名) prefix=线上前缀 color=主题色 dash=工作台端点(None则用品牌卡) tabs=[(图标,标签,端点,说明)]
CONFIGS = {
    "feirong-fms":    dict(name="飞融金融管理系统", short="飞融FMS", prefix="finan", color="#1d4ed8",
        dash="/api/dashboard", tabs=[("📒","凭证","/api/vouchers","会计凭证"),("💰","账单","/api/bills","应收应付"),("🤝","往来","/api/partners","往来单位")]),
    "feishou-rms":    dict(name="飞售零售管理系统", short="飞售RMS", prefix="retail", color="#b45309",
        dash="/api/dashboard", tabs=[("🧾","销售","/api/sales","销售单"),("🛒","商品","/api/commodities","商品档案"),("🏬","门店","/api/stores","门店")]),
    "feican-rms":     dict(name="飞餐餐饮管理系统", short="飞餐RMS", prefix="rms", color="#dc2626",
        dash="/api/dashboard", tabs=[("🍽️","订单","/api/orders","餐饮订单"),("🥘","菜品","/api/dishes","菜品"),("📦","库存","/api/inventory","食材库存")]),
    "feiyi-his":      dict(name="飞医医疗管理系统", short="飞医HIS", prefix="his", color="#0d9488",
        dash="/api/dashboard", tabs=[("🏥","挂号","/api/registrations","门诊挂号"),("🧑‍🤝‍🧑","患者","/api/patients","患者档案"),("💊","处方","/api/prescriptions","处方")]),
    "feishui-tax":    dict(name="飞税税务管理系统", short="飞税", prefix="tax", color="#7c3aed",
        dash="/api/dashboard", tabs=[("📋","申报","/api/declarations","纳税申报"),("🧾","发票","/api/invoices","发票"),("⚠️","风险","/api/risks","税务风险")]),
    "feixiao-oa":     dict(name="飞效OA管理系统", short="飞效OA", prefix="oa", color="#2563eb",
        dash="/api/dashboard", tabs=[("🏖️","请假","/api/leaves","请假申请"),("📅","会议","/api/meetings","会议"),("💸","报销","/api/expenses","费用报销")]),
    "feiyu-edu":      dict(name="飞育教育管理系统", short="飞育", prefix="edu", color="#059669",
        dash="/api/dashboard", tabs=[("🎓","学生","/api/students","学籍"),("📝","成绩","/api/scores","成绩"),("💳","缴费","/api/fees","学费缴费")]),
    "feiyun-tms":     dict(name="飞运运输管理系统", short="飞运TMS", prefix="tms", color="#ea580c",
        dash="/api/dashboard", tabs=[("🚚","运单","/api/waybills","运单"),("🛣️","调度","/api/dispatches","车辆调度"),("🚛","车辆","/api/vehicles","车辆")]),
    "feihua-aps":     dict(name="飞划APS系统", short="飞划APS", prefix="aps", color="#c2410c",
        dash=None, tabs=[("🏭","工单","/api/work-orders","生产工单"),("📥","订单","/api/sales-orders","销售订单"),("🧱","物料","/api/materials","物料")]),
    "feipu-energy":   dict(name="飞瀑能源管理系统", short="飞瀑", prefix="pu", color="#0891b2",
        dash=None, tabs=[("⚡","抄表","/api/readings","能耗抄表"),("🔋","计量","/api/meters","计量设备"),("🚨","告警","/api/alarms","能耗告警")]),
    "feiben-cost":    dict(name="飞奔成本管理系统", short="飞奔", prefix="cost", color="#4f46e5",
        dash="/api/board", tabs=[("💸","费用","/api/expenses","费用归集"),("🎯","预算","/api/budgets","成本预算"),("📊","差异","/api/variances","成本差异")]),
    "feihua-hrm":     dict(name="飞花HRM系统", short="飞花HRM", prefix="hr", color="#be185d",
        dash="/api/board", tabs=[("👥","员工","/api/employees","员工档案"),("🏖️","假勤","/api/leaves","请假"),("💵","薪酬","/api/payroll","薪酬")]),
    "feikong-qms":    dict(name="飞控QMS系统", short="飞控QMS", prefix="qms", color="#0f766e",
        dash="/api/board", tabs=[("🔍","检验","/api/inspections","质量检验"),("🐞","缺陷","/api/defects","缺陷"),("⛔","NCR","/api/ncrs","不合格品")]),
    "feichuan-wms":   dict(name="飞传WMS系统", short="飞传WMS", prefix="wms", color="#9333ea",
        dash="/api/board", tabs=[("📥","订单","/api/orders","出入库单"),("📦","库存","/api/stock","库存"),("🗺️","库位","/api/locations","库位")]),
    "feichi-mes":     dict(name="飞驰MES系统", short="飞驰MES", prefix="mes", color="#b91c1c",
        dash="/api/board", tabs=[("🏭","工单","/api/orders","生产工单"),("📝","报工","/api/prod-reports","生产报工"),("🩹","缺陷","/api/defects","质量缺陷")]),
    "feiquan-scm":    dict(name="飞泉SCM系统", short="飞泉SCM", prefix="scm", color="#1d7fd8",
        dash=None, tabs=[("📥","订单","/api/orders","采购订单"),("📝","请购","/api/requisitions","请购单"),("🤝","供应商","/api/suppliers","供应商")]),
    "feiyuan-erp":    dict(name="飞鸢ERP系统", short="飞鸢ERP", prefix="erp", color="#334155",
        dash=None, tabs=[("🛒","销售","/api/sales-orders","销售订单"),("📦","采购","/api/purchase-orders","采购订单"),("🗃️","库存","/api/inventory","库存")]),
    "feiying-crm":    dict(name="飞鹰CRM系统", short="飞鹰CRM", prefix="crm", color="#d97706",
        dash=None, tabs=[("🏢","客户","/api/customers","客户"),("🎣","线索","/api/leads","销售线索"),("💼","商机","/api/opportunities","商机")]),
    "feiliu-flow":    dict(name="飞流流程管理系统", short="飞流BPM", prefix="flow", color="#0369a1",
        dash="/api/stats", tabs=[("📬","待办","/api/tasks","待办任务"),("🔄","实例","/api/instances","流程实例"),("🧩","流程","/api/flows","流程模型")]),
    "feihong-stock":  dict(name="飞虹股票交易系统", short="飞虹", prefix="fh", color="#b91c1c",
        dash=None, tabs=[("📈","持仓","/api/positions","持仓"),("🧾","委托","/api/orders","委托单"),("📡","信号","/api/signals","交易信号")]),
    "feiyang-customs":dict(name="飞扬关务系统", short="飞扬", prefix="cus", color="#7e22ce",
        dash=None, tabs=[("🛃","报关","/api/declarations","报关单"),("📖","税则","/api/hs","HS税则"),("🤝","往来","/api/partners","关务往来")]),
    "feiyun-finance": dict(name="飞云财务核算系统", short="飞云", prefix="fin", color="#475569",
        dash=None, tabs=[("📒","凭证","/api/vouchers","会计凭证"),("📄","事件","/api/events","业务事件")]),
    "feiwu-data":     dict(name="飞物数据管理系统", short="飞物", prefix="data", color="#0e7490",
        dash=None, tabs=[("🗄️","数据集","/api/datasets","数据集"),("📏","指标","/api/metrics","指标"),("🚨","告警","/api/alerts","质量告警")]),
}


LOGINS = {
    "feishui-tax":    ("/api/auth/login", "admin", "tax@2026"),
    "feixiao-oa":     ("/api/auth/login", "admin", "oa@2026"),
    "feiyu-edu":      ("/api/auth/login", "admin", "123456"),
    "feihua-aps":     ("/api/auth/login", "admin", "aps@2026"),
    "feipu-energy":   ("/api/auth/login", "admin", "energy@2026"),
    "feiben-cost":    ("/api/auth/login", "admin", "cost@2026"),
    "feihua-hrm":     ("/api/auth/login", "admin", "hr@2026"),
    "feiliu-flow":    ("/api/auth/login", "admin", "admin123"),
    "feiyuan-erp":    ("/api/auth/login", "admin", "admin123"),
    "feihong-stock":  ("/api/auth/login", "admin", "admin123"),
    "feiyang-customs":("/api/auth/login", "admin", "admin123"),
    "feiyun-finance": ("/api/auth/login", "admin", "admin123"),
}
for _p, (_ep, _u, _pw) in LOGINS.items():
    CONFIGS[_p]["login"] = _ep
    CONFIGS[_p]["user"] = _u
    CONFIGS[_p]["pwd"] = _pw

INDEX_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<meta name="theme-color" content="__COLOR__">
<title>__NAME__</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg">
<link rel="apple-touch-icon" href="icon.svg">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div id="app">
  <header id="hd"><span id="hd-title">__SHORT__</span><span id="hd-user" onclick="logout()">退出</span></header>
  <main id="main"></main>
  <nav id="tabbar">
    <a data-tab="dash" class="on"><i>📋</i><b>工作台</b></a>
    __TABS__
    <a data-tab="me"><i>👤</i><b>我的</b></a>
  </nav>
</div>
<div id="toast"></div>
<script src="config.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

ICON_TPL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192">
  <rect width="192" height="192" rx="36" fill="__COLOR__"/>
  <path d="M96 30 L140 52 V96 C140 128 120 148 96 158 C72 148 52 128 52 96 V52 Z" fill="#ffffff" opacity=".92"/>
  <circle cx="96" cy="88" r="22" fill="__COLOR__"/>
  <text x="96" y="97" font-size="26" font-weight="bold" text-anchor="middle" fill="#fff" font-family="sans-serif">__CHAR__</text>
</svg>
"""

APP_JS = r"""/* __NAME__ · 手机APP(PWA) · 通用外壳 */
'use strict';
var CFG = window.APP_CONFIG;
var TOKEN = localStorage.getItem(CFG.tokenKey) || '';
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function toast(m){var t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},2200);}
function tag(s){return '<span class="tag">'+esc(s)+'</span>';}
function fmt(v){
  if (v == null) return '-';
  if (typeof v === 'number') return v.toLocaleString('zh-CN');
  if (typeof v === 'object') return '';
  var s = String(v);
  return s.length > 60 ? s.slice(0, 60) + '…' : s;
}
function api(path, opt){
  opt = opt || {};
  opt.headers = Object.assign({'Content-Type':'application/json'}, opt.headers||{},
    TOKEN?{'Authorization':'Bearer '+TOKEN}:{});
  if (opt.body && typeof opt.body !== 'string') opt.body = JSON.stringify(opt.body);
  return fetch(CFG.base + path, opt).then(function(r){
    return r.json().then(function(j){
      if (j && j.code === 200) return j.data;
      if (j && j.ok === true) return (j.data !== undefined) ? j.data : j;
      if (j && j.token) return j;
      var m = (j && j.message) || (j && j.error && (j.error.message || j.error)) || ('HTTP ' + r.status);
      throw new Error(m);
    });
  });
}

function dictRows(d){
  var keys = Object.keys(d).filter(function(k){return typeof d[k] !== 'object'||d[k]==null;}).slice(0,9);
  return '<div class="kpis">' + keys.map(function(k){
    return '<div class="kpi"><b>'+esc(fmt(d[k]))+'</b><span>'+esc(k)+'</span></div>';
  }).join('') + '</div>';
}
function listCards(items){
  if (!items || !items.length) return '<div class="empty">暂无数据</div>';
  return items.slice(0, 50).map(function(it){
    if (typeof it !== 'object' || !it) return '<div class="card"><h4>'+esc(fmt(it))+'</h4></div>';
    var ks = Object.keys(it).filter(function(k){return it[k]!=null && typeof it[k] !== 'object';});
    var title = ks[0], rest = ks.slice(1, 5);
    return '<div class="card"><h4>'+esc(fmt(it[title]))+'</h4>'
      + rest.map(function(k){return '<div class="row"><span class="lb">'+esc(k)+'</span><span>'+esc(fmt(it[k]))+'</span></div>';}).join('')
      + '</div>';
  }).join('');
}
function errHtml(e){
  var m = String(e && e.message || e);
  if (m.indexOf('401')>=0 || m.indexOf('token')>=0) { showLogin(); return '<div class="empty">请先登录</div>'; }
  return '<div class="empty">加载失败：'+esc(m)+'</div>';
}

var TABS = {};
TABS.dash = function(){
  if (!CFG.dash) {
    return Promise.resolve('<div class="me-card" style="background:linear-gradient(135deg,'+CFG.color+',#0f172a)">'
      + '<b>'+esc(CFG.name)+'</b><p>移动工作台 · V1.0</p></div>'
      + '<div class="me-item">核心功能<span>'+CFG.tabs.map(function(t){return t[1];}).join(' / ')+'</span></div>'
      + '<div class="me-item">请登录后使用<span>点底部「我的」</span></div>');
  }
  return api(CFG.dash).then(function(d){
    var html = '';
    if (d && typeof d === 'object' && !Array.isArray(d)) html = dictRows(d);
    else if (Array.isArray(d)) html = listCards(d);
    else html = '<div class="empty">暂无概览数据</div>';
    return html;
  });
};
CFG.tabs.forEach(function(t, i){
  TABS['t'+i] = function(){
    return api(t[2]).then(function(d){
      var items = d && d.items ? d.items : (Array.isArray(d) ? d : null);
      if (items === null) {
        if (d && typeof d === 'object') return dictRows(d);
        return '<div class="empty">暂无数据</div>';
      }
      return '<div class="card" style="padding:8px 12px"><h4>'+t[3]+' · 共 '+items.length+' 条</h4></div>' + listCards(items);
    });
  };
});
TABS.me = function(){
  return api(CFG.me || '/api/me').then(function(d){
    var u = (d && d.user) || d || {};
    return '<div class="me-card" style="background:linear-gradient(135deg,'+CFG.color+',#0f172a)">'
      + '<b>'+esc(u.name||u.username||CFG.short)+'</b><p>'+esc(u.role||'')+'</p></div>'
      + '<div class="me-item">'+esc(CFG.name)+'<span>V1.0</span></div>'
      + '<div class="me-item">服务地址<span style="max-width:55%;overflow:hidden;text-overflow:ellipsis">'+esc(CFG.base)+'</span></div>'
      + '<button class="btn gray" onclick="logout()">退出登录</button>';
  }).catch(function(){
    return '<div class="me-card" style="background:linear-gradient(135deg,'+CFG.color+',#0f172a)">'
      + '<b>'+esc(CFG.name)+'</b><p>移动工作台</p></div>'
      + '<button class="btn gray" onclick="logout()">退出登录</button>';
  });
};

var cur = 'dash';
function render(tab){
  cur = tab;
  var names = {dash:'工作台', me:'我的'};
  CFG.tabs.forEach(function(t,i){ names['t'+i] = t[1]; });
  document.getElementById('hd-title').textContent = (names[tab] || CFG.short);
  document.querySelectorAll('#tabbar a').forEach(function(a){
    a.classList.toggle('on', a.getAttribute('data-tab') === tab);
  });
  var main = document.getElementById('main');
  main.innerHTML = '<div class="empty">加载中…</div>';
  (TABS[tab] || TABS.dash)().then(function(html){
    if (cur === tab) main.innerHTML = html || '<div class="empty">暂无数据</div>';
  }).catch(function(e){ if (cur===tab) main.innerHTML = errHtml(e); });
}
document.getElementById('tabbar').addEventListener('click', function(ev){
  var a = ev.target.closest('a'); if (!a) return;
  render(a.getAttribute('data-tab'));
});

function showLogin(){
  document.getElementById('tabbar').style.display = 'none';
  document.getElementById('main').innerHTML =
    '<div class="card"><h4>登录'+esc(CFG.name)+'</h4>'
    + '<input id="lg-u" value="'+esc(CFG.user||'')+'" style="width:100%;margin:8px 0" placeholder="用户名">'
    + '<input id="lg-p" value="'+esc(CFG.pwd||'')+'" type="password" style="width:100%;margin:8px 0" placeholder="密码">'
    + '<button class="btn" onclick="doLogin()">登 录</button></div>';
  document.getElementById('hd-title').textContent = CFG.short + ' · 登录';
}
function doLogin(){
  var u = document.getElementById('lg-u').value.trim();
  var p = document.getElementById('lg-p').value;
  if (!u || !p) { toast('请输入账号密码'); return; }
  api(CFG.login || '/api/login', {method:'POST', body:{username:u, password:p}}).then(function(d){
    TOKEN = d.token; localStorage.setItem(CFG.tokenKey, TOKEN);
    document.getElementById('tabbar').style.display = '';
    toast('登录成功'); render('dash');
  }).catch(function(e){ toast('登录失败：'+(e.message||e)); });
}
function logout(){
  TOKEN=''; localStorage.removeItem(CFG.tokenKey); showLogin();
}

if ('serviceWorker' in navigator) { navigator.serviceWorker.register('sw.js').catch(function(){}); }
if (!TOKEN) showLogin(); else render('dash');
"""

SW_JS = r"""var CACHE = '__KEY__-m-v1';
var ASSETS = ['index.html','style.css','app.js','config.js','icon.svg','manifest.webmanifest'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.pathname.indexOf('/api/') >= 0) return;
  e.respondWith(caches.match(e.request).then(function (hit) {
    return hit || fetch(e.request).then(function (r) {
      var cp = r.clone();
      caches.open(CACHE).then(function (c) { c.put(e.request, cp); });
      return r;
    });
  }).catch(function () { return caches.match('index.html'); }));
});
"""

STYLE = open(os.path.join(CLAW, "feiyang-otms", "mobile", "style.css"), encoding="utf-8").read()


def gen(proj):
    c = CONFIGS[proj]
    root = os.path.join(CLAW, proj, "mobile")
    os.makedirs(root, exist_ok=True)
    cfg = {
        "name": c["name"], "short": c["short"], "base": "/" + c["prefix"] + "/",
        "color": c["color"], "dash": c["dash"], "tabs": c["tabs"],
        "tokenKey": proj.replace("-", "_") + "_m_token", "key": proj.replace("-", ""), "login": c.get("login"), "user": c.get("user", "admin"), "pwd": c.get("pwd", "123456"),
    }
    tabs_html = "".join('<a data-tab="t%d"><i>%s</i><b>%s</b></a>' % (i, t[0], t[1])
                        for i, t in enumerate(c["tabs"]))
    io.open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(
        INDEX_TPL.replace("__COLOR__", c["color"]).replace("__NAME__", c["name"])
        .replace("__SHORT__", c["short"]).replace("__TABS__", tabs_html))
    io.open(os.path.join(root, "config.js"), "w", encoding="utf-8").write(
        "window.APP_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";")
    io.open(os.path.join(root, "app.js"), "w", encoding="utf-8").write(
        APP_JS.replace("__NAME__", c["name"]))
    io.open(os.path.join(root, "style.css"), "w", encoding="utf-8").write(
        STYLE.replace("#0e7490", c["color"]).replace("#083344", "#0f172a"))
    io.open(os.path.join(root, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps({
        "name": c["name"], "short_name": c["short"], "lang": "zh-CN",
        "start_url": "./index.html", "scope": "./", "display": "standalone",
        "orientation": "portrait", "theme_color": c["color"], "background_color": "#0f172a",
        "icons": [{"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
    }, ensure_ascii=False, indent=2))
    io.open(os.path.join(root, "icon.svg"), "w", encoding="utf-8").write(
        ICON_TPL.replace("__COLOR__", c["color"]).replace("__CHAR__", c["short"][:1]))
    io.open(os.path.join(root, "sw.js"), "w", encoding="utf-8").write(
        SW_JS.replace("__KEY__", proj.replace("-", "")))
    return root


if __name__ == "__main__":
    want = sys.argv[1:] or [p for p in CONFIGS if p != "feiyang-otms"]
    for p in want:
        print("OK", p, "->", gen(p))
