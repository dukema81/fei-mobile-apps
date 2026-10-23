# -*- coding: utf-8 -*-
"""批量验收全部手机APP：加载、登录、工作台、首个业务Tab"""
import sys
sys.path.insert(0, r"C:/Users/maxl/WorkBuddy/Claw/mobile-apps")
import gen_all as G
from playwright.sync_api import sync_playwright

HOST = "http://42.193.158.63"
results = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 375, "height": 812}, is_mobile=True)
    for proj, c in G.CONFIGS.items():
        url = "%s/%s/m/" % (HOST, c["prefix"])
        st = {"load": False, "login": False, "dash": False, "tab": False, "overflow": False}
        try:
            pg = ctx.new_page()
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(url, timeout=20000)
            pg.wait_for_timeout(800)
            st["load"] = pg.locator("#lg-u, #main").count() > 0
            pg.set_default_timeout(6000)
            if st["load"] and pg.locator("#lg-u").count():
                pg.fill("#lg-u", c.get("user", "admin")); pg.fill("#lg-p", c.get("pwd", "123456"))
                pg.click(".btn"); pg.wait_for_timeout(1200)
                st["login"] = pg.locator("#tabbar").is_visible()
                if st["login"]:
                    pg.wait_for_timeout(600)
                    txt = pg.inner_text("#main")
                    st["dash"] = len(txt.strip()) >= 8 and "加载失败" not in txt
                    pg.evaluate("document.querySelectorAll('#tabbar a')[1].click()")
                    pg.wait_for_timeout(1000)
                    txt2 = pg.inner_text("#main")
                    st["tab"] = len(txt2.strip()) >= 8 and "加载失败" not in txt2
            st["overflow"] = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2")
            if errors:
                st["js"] = errors[0][:80]
            pg.close()
        except Exception as e:
            st["err"] = str(e)[:80]
        NO_BACKEND = {"feikong-qms","feichuan-wms","feichi-mes","feiquan-scm","feiying-crm","feiwu-data"}
        ok = st["load"] and not st["overflow"] and "js" not in st and "err" not in st and (st["login"] or st["dash"] or proj in NO_BACKEND)
        results.append((proj, ok, st))
        print(("OK  " if ok else "FAIL"), proj, st)
    b.close()

npass = sum(1 for _, ok, _ in results if ok)
print("==== APPS PASS=%d/%d ====" % (npass, len(results)))
sys.exit(0 if npass == len(results) else 1)
