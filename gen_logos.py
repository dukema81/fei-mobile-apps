# -*- coding: utf-8 -*-
"""飞系24系统 · 专属Logo生成器 V2
每个项目一枚领域化矢量徽标：主题色渐变圆角底 + 白色业务图形 + 领域点缀。
产出: <proj>/mobile/icon.svg、fei-mobile-repo/apps/<proj>/mobile/icon.svg、mobile-apps/logo/ 预览页
"""
import io, json, os, shutil, sys

CLAW = r"C:/Users/maxl/WorkBuddy/Claw"
sys.path.insert(0, os.path.join(CLAW, "mobile-apps"))
import gen_all  # noqa: E402

def _darken(hex_color, f=0.62):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r*f), int(g*f), int(b*f))

# 领域图形（512 画布中央区域，白色描边/填充，均为可独立成立的简约矢量）
G = {
    "feirong-fms":   '<ellipse cx="256" cy="330" rx="120" ry="34"/><rect x="136" y="248" width="240" height="40" rx="18"/><rect x="136" y="178" width="240" height="40" rx="18"/><ellipse cx="256" cy="180" rx="120" ry="32"/><text x="256" y="128" font-size="86" font-weight="700" text-anchor="middle" fill="#fff" font-family="Arial">¥</text>',
    "feishou-rms":   '<path d="M136 226l24-92h192l24 92z"/><rect x="150" y="240" width="212" height="122" rx="16"/><rect x="212" y="286" width="88" height="76" rx="8" opacity=".85"/><path d="M136 226c26 0 26-26 52-26s26 26 52 26 26-26 52-26 26 26 52 26" fill="none" stroke="#fff" stroke-width="16"/>',
    "feican-rms":    '<path d="M132 268a124 96 0 0 0 248 0z"/><rect x="244" y="120" width="16" height="120" rx="8" transform="rotate(14 252 180)"/><rect x="268" y="120" width="16" height="120" rx="8" transform="rotate(-10 276 180)"/><path d="M300 148c30 10 52 26 60 44" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/>',
    "feiyi-his":     '<rect x="216" y="128" width="80" height="256" rx="14"/><rect x="128" y="216" width="256" height="80" rx="14"/><path d="M148 386h216" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".6"/>',
    "feishui-tax":   '<path d="M256 118l132 44v96c0 78-56 122-132 140-76-18-132-62-132-140v-96z"/><text x="256" y="300" font-size="120" font-weight="700" text-anchor="middle" fill="{}" font-family="Arial">%</text>'.format(None),
    "feixiao-oa":    '<rect x="140" y="128" width="232" height="256" rx="22"/><rect x="176" y="180" width="120" height="22" rx="11" opacity=".85"/><rect x="176" y="234" width="160" height="22" rx="11" opacity=".85"/><path d="M176 306l30 32 58-70" fill="none" stroke="{}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>',
    "feiyu-edu":     '<path d="M256 138L118 206l138 68 138-68z"/><path d="M178 238v76c0 30 42 48 78 48s78-18 78-48v-76" fill="none" stroke="#fff" stroke-width="20"/><path d="M370 214v96" stroke="#fff" stroke-width="18" stroke-linecap="round"/>',
    "feiyun-tms":    '<rect x="112" y="200" width="180" height="120" rx="14"/><path d="M292 232h74l46 52v36h-120z"/><circle cx="182" cy="346" r="30"/><circle cx="330" cy="346" r="30"/><path d="M132 168h100" stroke="#fff" stroke-width="16" stroke-linecap="round"/>',
    "feihua-aps":    '<circle cx="200" cy="210" r="74" fill="none" stroke="#fff" stroke-width="34"/><circle cx="200" cy="210" r="14"/><rect x="300" y="146" width="88" height="30" rx="10"/><rect x="300" y="196" width="88" height="30" rx="10" opacity=".8"/><rect x="300" y="246" width="60" height="30" rx="10" opacity=".6"/>',
    "feipu-energy":  '<path d="M282 118L172 288h72l-26 106 110-170h-72z"/>',
    "feiben-cost":   '<path d="M256 132a124 124 0 1 0 124 124H256z"/><path d="M286 118a124 124 0 0 1 108 108H286z" opacity=".8"/>',
    "feihua-hrm":    '<circle cx="256" cy="184" r="52"/><path d="M156 372c0-58 44-92 100-92s100 34 100 92z"/><circle cx="150" cy="222" r="38" opacity=".75"/><circle cx="362" cy="222" r="38" opacity=".75"/>',
    "feikong-qms":   '<circle cx="232" cy="228" r="98" fill="none" stroke="#fff" stroke-width="34"/><path d="M306 306l96 96" stroke="#fff" stroke-width="40" stroke-linecap="round"/><path d="M196 228l28 30 52-58" fill="none" stroke="{}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>',
    "feichuan-wms":  '<path d="M120 240L256 150l136 90v122H120z" fill="none" stroke="#fff" stroke-width="30" stroke-linejoin="round"/><rect x="196" y="270" width="120" height="92" rx="8"/><path d="M256 270v92" stroke="{}" stroke-width="14"/>',
    "feichi-mes":    '<path d="M136 362V228l70 44v-44l70 44v-44l100 60v74z"/><rect x="336" y="150" width="52" height="52" rx="10"/><path d="M362 202v26" stroke="#fff" stroke-width="14"/>',
    "feiquan-scm":   '<circle cx="196" cy="256" r="76" fill="none" stroke="#fff" stroke-width="40"/><circle cx="316" cy="256" r="76" fill="none" stroke="#fff" stroke-width="40" opacity=".8"/>',
    "feiyuan-erp":   '<circle cx="256" cy="256" r="124" fill="none" stroke="#fff" stroke-width="26"/><ellipse cx="256" cy="256" rx="52" ry="124" fill="none" stroke="#fff" stroke-width="18"/><path d="M140 256h232M150 196h212M150 316h212" stroke="#fff" stroke-width="16"/>',
    "feiying-crm":   '<circle cx="256" cy="256" r="118" fill="none" stroke="#fff" stroke-width="30"/><circle cx="256" cy="256" r="62" fill="none" stroke="#fff" stroke-width="26"/><circle cx="256" cy="256" r="18"/>',
    "feiliu-flow":   '<rect x="128" y="140" width="110" height="76" rx="16"/><rect x="274" y="296" width="110" height="76" rx="16"/><path d="M238 178h74a24 24 0 0 1 24 24v70" fill="none" stroke="#fff" stroke-width="22"/><path d="M312 260l24 36 24-36z"/><path d="M274 334h-74a24 24 0 0 1-24-24v-70" fill="none" stroke="#fff" stroke-width="22" opacity=".85"/><path d="M200 272l-24-36-24 36z" opacity=".85"/>',
    "feihong-stock": '<rect x="148" y="238" width="34" height="112" rx="8"/><rect x="238" y="188" width="34" height="162" rx="8"/><rect x="328" y="262" width="34" height="88" rx="8"/><path d="M140 220l90-64 70 44 76-84" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round"/><path d="M348 116h34v34z"/>',
    "feiyang-customs":'<path d="M256 118l128 46v98c0 80-54 124-128 142-74-18-128-62-128-142v-98z"/><path d="M196 256h120M256 196v120" stroke="{}" stroke-width="26" stroke-linecap="round"/>',
    "feiyun-finance":'<path d="M256 140v230M180 180h152" stroke="#fff" stroke-width="20" stroke-linecap="round"/><path d="M120 330a60 60 0 0 1 120 0z"/><path d="M272 330a60 60 0 0 1 120 0z"/><path d="M170 384h172" stroke="#fff" stroke-width="22" stroke-linecap="round"/>',
    "feiwu-data":    '<rect x="140" y="280" width="52" height="92" rx="10"/><rect x="230" y="222" width="52" height="150" rx="10" opacity=".85"/><rect x="320" y="160" width="52" height="212" rx="10" opacity=".7"/><circle cx="166" cy="196" r="26" fill="none" stroke="#fff" stroke-width="14"/><path d="M166 222v58M256 176v46" stroke="#fff" stroke-width="12"/>',
    "feiyang-otms":  '<circle cx="256" cy="196" r="34" fill="none" stroke="#fff" stroke-width="22"/><path d="M256 230v130M180 282h152" stroke="#fff" stroke-width="24" stroke-linecap="round"/><path d="M150 330c30 0 30 26 60 26" fill="none" stroke="#fff" stroke-width="0"/><path d="M148 386c26-24 62-36 108-36s82 12 108 36" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round"/>',
}
# 填充占位符替换为底色深部（挖空效果）
HOLE = "#0f172a"

def logo_svg(color, glyph):
    g = glyph.replace("{}", HOLE)
    d = _darken(color)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="512" height="512" rx="112" fill="url(#g)"/>'
            '<circle cx="256" cy="256" r="212" fill="none" stroke="#ffffff" stroke-opacity=".16" stroke-width="10"/>'
            '<g fill="#ffffff">%s</g></svg>' % (color, d, g))

def main():
    gen = os.path.join(CLAW, "mobile-apps", "gen_logos.py")
    projs = list(gen_all.CONFIGS.keys()) + ["feiyang-otms"]
    colors = {p: ("#0e7490" if p == "feiyang-otms" else gen_all.CONFIGS[p]["color"]) for p in projs}
    names = {p: ("飞洋海洋运输管理系统" if p == "feiyang-otms" else gen_all.CONFIGS[p]["name"]) for p in projs}
    outs = []
    for p in projs:
        svg = logo_svg(colors[p], G[p])
        for root in (os.path.join(CLAW, p, "mobile"),
                     os.path.join(CLAW, "fei-mobile-repo", "apps", p, "mobile")):
            os.makedirs(root, exist_ok=True)
            io.open(os.path.join(root, "icon.svg"), "w", encoding="utf-8").write(svg)
        outs.append((p, names[p], colors[p]))
    # 预览页
    os.makedirs(os.path.join(CLAW, "mobile-apps", "logo"), exist_ok=True)
    cards = "".join(
        '<div class="c"><img src="%s_icon.svg"><b>%s</b><span>%s</span></div>'
        % (p, n, c) for p, n, c in outs)
    for p, _, _ in outs:
        io.open(os.path.join(CLAW, "mobile-apps", "logo", p + "_icon.svg"), "w", encoding="utf-8").write(
            logo_svg(colors[p], G[p]))
    io.open(os.path.join(CLAW, "mobile-apps", "logo", "index.html"), "w", encoding="utf-8").write(
        '<!doctype html><meta charset="utf-8"><title>飞系24系统专属Logo V2</title>'
        '<style>body{font-family:system-ui;background:#0f172a;color:#e2e8f0;padding:32px}'
        'h1{font-size:22px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:18px}'
        '.c{background:#1e293b;border-radius:14px;padding:14px;text-align:center}'
        '.c img{width:96px;height:96px;border-radius:22px}.c b{display:block;margin-top:8px;font-size:13px}'
        '.c span{font-size:11px;color:#94a3b8}</style>'
        '<h1>飞系24系统 · 专属Logo V2（领域图形 + 主题渐变）</h1><div class="g">%s</div>' % cards)
    print("LOGOS OK", len(outs))
    json.dump([{"proj": p, "name": n, "color": c} for p, n, c in outs],
              io.open(os.path.join(CLAW, "mobile-apps", "logo", "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
