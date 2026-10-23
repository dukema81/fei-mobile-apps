/* 飞扬关务系统 · 手机APP(PWA) · 通用外壳 */
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
