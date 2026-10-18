#!/usr/bin/env python3
"""Generate README cover SVGs into assets/covers/."""
from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1280, 640
OUT = Path(__file__).resolve().parent.parent / "assets" / "covers"
FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC',system-ui,sans-serif"


def chips(items, x, y, accent):
    out, cx = [], x
    for t in items:
        w = 26 + sum(26 if ord(c) > 255 else 14.5 for c in t)
        out.append(
            f'<rect x="{cx}" y="{y}" rx="22" width="{w:.0f}" height="44" fill="#ffffff" fill-opacity="0.10" stroke="{accent}" stroke-opacity="0.55"/>'
            f'<text x="{cx + w / 2:.0f}" y="{y + 29}" text-anchor="middle" font-size="22" font-weight="600" fill="#fff">{escape(t)}</text>'
        )
        cx += w + 14
    return "".join(out)


def window(x, y, w, h, body, accent):
    return (
        f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#0b1020" fill-opacity="0.72" stroke="#fff" stroke-opacity="0.14"/>'
        f'<circle cx="{x + 26}" cy="{y + 24}" r="6" fill="#ff5f57"/><circle cx="{x + 46}" cy="{y + 24}" r="6" fill="#febc2e"/><circle cx="{x + 66}" cy="{y + 24}" r="6" fill="#28c840"/>'
        f'<rect x="{x}" y="{y + 46}" width="{w}" height="1" fill="#fff" fill-opacity="0.10"/>{body}</g>'
    )


# ---------- motifs (drawn inside a window at 740,110 size 480x420) ----------
X0, Y0, WW, WH = 740, 110, 480, 420


def m_dashboard(a, b):
    s = ""
    for i, (lab, val) in enumerate([("MTD", "1577"), ("S1–S7", "680"), ("预警", "106")]):
        x = X0 + 24 + i * 148
        s += f'<rect x="{x}" y="{Y0 + 70}" width="136" height="84" rx="12" fill="#fff" fill-opacity="0.06"/>'
        s += f'<text x="{x + 16}" y="{Y0 + 100}" font-size="16" fill="#cbd5e1">{lab}</text>'
        s += f'<text x="{x + 16}" y="{Y0 + 138}" font-size="30" font-weight="700" fill="{a if i < 2 else "#f87171"}">{val}</text>'
    hs = [120, 160, 95, 190, 140, 210, 170, 230]
    for i, h in enumerate(hs):
        x = X0 + 34 + i * 54
        s += f'<rect x="{x}" y="{Y0 + 390 - h}" width="30" height="{h}" rx="6" fill="url(#g2)"/>'
    pts = " ".join(f"{X0 + 49 + i * 54},{Y0 + 370 - h * 0.9}" for i, h in enumerate(hs))
    s += f'<polyline points="{pts}" fill="none" stroke="{b}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    return s


def m_console(a, b):
    s = f'<rect x="{X0 + 16}" y="{Y0 + 62}" width="110" height="342" rx="12" fill="#fff" fill-opacity="0.05"/>'
    for i, lab in enumerate(["总览", "知识库", "项目", "区域工具", "系统"]):
        y = Y0 + 82 + i * 52
        s += f'<rect x="{X0 + 26}" y="{y}" width="90" height="36" rx="8" fill="{a if i == 1 else "#fff"}" fill-opacity="{0.9 if i == 1 else 0.06}"/>'
        s += f'<text x="{X0 + 71}" y="{y + 24}" text-anchor="middle" font-size="16" fill="#fff">{lab}</text>'
    for r in range(3):
        for c in range(3):
            x, y = X0 + 142 + c * 108, Y0 + 62 + r * 116
            s += f'<rect x="{x}" y="{y}" width="96" height="104" rx="12" fill="#fff" fill-opacity="0.06" stroke="{a}" stroke-opacity="{0.6 if (r + c) % 3 == 0 else 0.15}"/>'
            s += f'<rect x="{x + 12}" y="{y + 14}" width="28" height="36" rx="4" fill="{b if (r * 3 + c) % 2 else a}" fill-opacity="0.85"/>'
            s += f'<rect x="{x + 12}" y="{y + 62}" width="70" height="8" rx="4" fill="#fff" fill-opacity="0.35"/>'
            s += f'<rect x="{x + 12}" y="{y + 78}" width="46" height="8" rx="4" fill="#fff" fill-opacity="0.18"/>'
    return s


def m_network(a, b):
    import math
    cx, cy = X0 + 240, Y0 + 240
    nodes = [(cx, cy, 34, a)]
    labels = ["采集", "质检", "评分", "画像", "AB", "监控"]
    s = ""
    for i, lab in enumerate(labels):
        ang = -math.pi / 2 + i * 2 * math.pi / len(labels)
        x, y = cx + 150 * math.cos(ang), cy + 140 * math.sin(ang)
        s += f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{a}" stroke-opacity="0.55" stroke-width="3" stroke-dasharray="8 8"/>'
        nodes.append((x, y, 30, b if i % 2 else a))
        nodes.append((x, y, 0, lab))
    for n in nodes:
        x, y, r, c = n
        if r == 0:
            s += f'<text x="{x:.0f}" y="{y + 7:.0f}" text-anchor="middle" font-size="18" font-weight="600" fill="#fff">{c}</text>'
        else:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}" fill-opacity="0.28" stroke="{c}" stroke-width="2.5"/>'
    s += f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" font-size="20" font-weight="700" fill="#fff">Agent</text>'
    return s


def m_flow(a, b):
    s = ""
    steps = ["入职", "转正", "调岗", "离职"]
    for i, lab in enumerate(steps):
        x = X0 + 30 + i * 112
        s += f'<rect x="{x}" y="{Y0 + 90}" width="92" height="56" rx="12" fill="{a}" fill-opacity="{0.9 - i * 0.15}"/>'
        s += f'<text x="{x + 46}" y="{Y0 + 125}" text-anchor="middle" font-size="20" font-weight="700" fill="#fff">{lab}</text>'
        if i < 3:
            s += f'<path d="M{x + 96} {Y0 + 118} h14" stroke="#fff" stroke-opacity="0.6" stroke-width="3" marker-end="url(#arr)"/>'
    for i, lab in enumerate(["HRIS", "SAP", "OA"]):
        x = X0 + 50 + i * 140
        s += f'<rect x="{x}" y="{Y0 + 230}" width="110" height="70" rx="14" fill="#fff" fill-opacity="0.07" stroke="{b}" stroke-opacity="0.7"/>'
        s += f'<text x="{x + 55}" y="{Y0 + 273}" text-anchor="middle" font-size="22" font-weight="700" fill="#fff">{lab}</text>'
        s += f'<path d="M{x + 55} {Y0 + 150} V{Y0 + 226}" stroke="{b}" stroke-opacity="0.5" stroke-width="2.5" stroke-dasharray="6 6"/>'
    for i in range(3):
        s += f'<rect x="{X0 + 50}" y="{Y0 + 330 + i * 24}" width="{380 - i * 90}" height="12" rx="6" fill="#fff" fill-opacity="{0.25 - i * 0.06}"/>'
    return s


def m_leaderboard(a, b):
    rows = [("1", "Team ··", "··", 0.35), ("2", "Ours · Top 2", "84.77", 1.0), ("3", "Team ··", "··", 0.35), ("4", "Team ··", "··", 0.25), ("5", "Team ··", "··", 0.2)]
    s = f'<text x="{X0 + 28}" y="{Y0 + 86}" font-size="18" fill="#cbd5e1">LEADERBOARD · OpenSeek</text>'
    for i, (rk, name, sc, op) in enumerate(rows):
        y = Y0 + 106 + i * 60
        hi = i == 1
        s += f'<rect x="{X0 + 20}" y="{y}" width="440" height="48" rx="12" fill="{a if hi else "#fff"}" fill-opacity="{0.9 if hi else 0.05}"/>'
        s += f'<text x="{X0 + 44}" y="{y + 32}" font-size="22" font-weight="700" fill="#fff" fill-opacity="{1 if hi else 0.6}">#{rk}</text>'
        s += f'<text x="{X0 + 100}" y="{y + 32}" font-size="21" font-weight="{700 if hi else 400}" fill="#fff" fill-opacity="{1 if hi else 0.55}">{name}</text>'
        s += f'<text x="{X0 + 440}" y="{y + 32}" text-anchor="end" font-size="22" font-weight="700" fill="#fff" fill-opacity="{1 if hi else 0.55}">{sc}</text>'
    return s


def m_solar(a, b):
    s = f'<circle cx="{X0 + 370}" cy="{Y0 + 120}" r="46" fill="{b}"/><circle cx="{X0 + 370}" cy="{Y0 + 120}" r="70" fill="{b}" fill-opacity="0.18"/>'
    for i in range(4):
        x = X0 + 40 + i * 70
        y = Y0 + 230 - i * 22
        s += f'<g transform="skewX(-18)"><rect x="{x + 70}" y="{y}" width="60" height="100" rx="6" fill="{a}" fill-opacity="0.85" stroke="#fff" stroke-opacity="0.35"/>'
        s += f'<path d="M{x + 70} {y + 33} h60 M{x + 70} {y + 66} h60 M{x + 100} {y} v100" stroke="#fff" stroke-opacity="0.35" stroke-width="2"/></g>'
    for k in range(3):
        y = Y0 + 360 + k * 16
        s += f'<path d="M{X0 + 20} {y} q60 -18 120 0 t120 0 t120 0 t110 0" fill="none" stroke="{a}" stroke-opacity="{0.8 - k * 0.22}" stroke-width="3"/>'
    return s


def m_radar(a, b):
    import math
    cx, cy, R = X0 + 240, Y0 + 245, 150
    labs = ["供应商", "买方", "新进入者", "替代品", "竞争"]
    def pt(i, r):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        return cx + r * math.cos(ang), cy + r * math.sin(ang)
    s = ""
    for k in (1, 0.66, 0.33):
        p = " ".join(f"{x:.0f},{y:.0f}" for x, y in (pt(i, R * k) for i in range(5)))
        s += f'<polygon points="{p}" fill="none" stroke="#fff" stroke-opacity="0.18" stroke-width="2"/>'
    vals = [0.7, 0.85, 0.45, 0.6, 0.9]
    p = " ".join(f"{x:.0f},{y:.0f}" for x, y in (pt(i, R * v) for i, v in enumerate(vals)))
    s += f'<polygon points="{p}" fill="{a}" fill-opacity="0.45" stroke="{b}" stroke-width="3"/>'
    for i, l in enumerate(labs):
        x, y = pt(i, R + 34)
        s += f'<text x="{x:.0f}" y="{y + 7:.0f}" text-anchor="middle" font-size="18" fill="#fff">{l}</text>'
    return s


def m_book(a, b):
    s = ""
    tabs = [("理想", a), ("字节", b), ("腾讯", a), ("TCL", b), ("附录", "#94a3b8")]
    for i, (lab, c) in enumerate(tabs):
        y = Y0 + 72 + i * 66
        s += f'<rect x="{X0 + 24}" y="{y}" width="432" height="54" rx="12" fill="#fff" fill-opacity="0.05"/>'
        s += f'<rect x="{X0 + 24}" y="{y}" width="10" height="54" rx="4" fill="{c}"/>'
        s += f'<text x="{X0 + 54}" y="{y + 35}" font-size="22" font-weight="700" fill="#fff">{lab}</text>'
        for k in range(3):
            s += f'<rect x="{X0 + 150 + k * 96}" y="{y + 20}" width="80" height="14" rx="7" fill="{c}" fill-opacity="{0.55 - k * 0.15}"/>'
    return s


def m_grid(a, b):
    s = ""
    labs = ["理想", "腾讯", "字节", "TCL"]
    for i, lab in enumerate(labs):
        x = X0 + 24 + (i % 2) * 222
        y = Y0 + 66 + (i // 2) * 172
        c = a if i % 3 == 0 else b
        s += f'<rect x="{x}" y="{y}" width="210" height="158" rx="14" fill="#fff" fill-opacity="0.06" stroke="{c}" stroke-opacity="0.6"/>'
        s += f'<rect x="{x + 14}" y="{y + 14}" width="182" height="74" rx="8" fill="{c}" fill-opacity="0.35"/>'
        s += f'<text x="{x + 16}" y="{y + 120}" font-size="22" font-weight="700" fill="#fff">{lab}</text>'
        s += f'<rect x="{x + 16}" y="{y + 134}" width="120" height="8" rx="4" fill="#fff" fill-opacity="0.25"/>'
    return s


def m_gauge(a, b):
    s = f'<path d="M{X0 + 90} {Y0 + 250} A150 150 0 0 1 {X0 + 390} {Y0 + 250}" fill="none" stroke="#fff" stroke-opacity="0.12" stroke-width="28" stroke-linecap="round"/>'
    s += f'<path d="M{X0 + 90} {Y0 + 250} A150 150 0 0 1 {X0 + 340} {Y0 + 140}" fill="none" stroke="url(#g2)" stroke-width="28" stroke-linecap="round"/>'
    s += f'<text x="{X0 + 240}" y="{Y0 + 236}" text-anchor="middle" font-size="56" font-weight="800" fill="#fff">82</text>'
    s += f'<text x="{X0 + 240}" y="{Y0 + 268}" text-anchor="middle" font-size="18" fill="#cbd5e1">门店健康分</text>'
    for i, (lab, c) in enumerate([("P1 · 线索流失", "#f87171"), ("P2 · 试驾转化", "#fbbf24"), ("P3 · 交付卡点", b)]):
        y = Y0 + 300 + i * 38
        s += f'<circle cx="{X0 + 60}" cy="{y + 12}" r="8" fill="{c}"/><text x="{X0 + 80}" y="{y + 19}" font-size="19" fill="#fff">{lab}</text>'
        s += f'<rect x="{X0 + 250}" y="{y + 6}" width="{180 - i * 40}" height="12" rx="6" fill="{c}" fill-opacity="0.7"/>'
    return s


def m_scatter(a, b):
    s = ""
    tiers = [("S+", 0.95), ("S", 0.8), ("A", 0.62), ("B", 0.42), ("C", 0.25)]
    for i, (t, v) in enumerate(tiers):
        y = Y0 + 80 + i * 64
        s += f'<text x="{X0 + 34}" y="{y + 30}" font-size="22" font-weight="800" fill="#fff">{t}</text>'
        s += f'<rect x="{X0 + 90}" y="{y + 10}" width="350" height="28" rx="14" fill="#fff" fill-opacity="0.07"/>'
        s += f'<rect x="{X0 + 90}" y="{y + 10}" width="{350 * v:.0f}" height="28" rx="14" fill="{a if i < 2 else b}" fill-opacity="{1 - i * 0.12}"/>'
    return s


def m_agent(a, b):
    s = ""
    bubbles = [("候选人 A 推进到终面", False), ("调用 scorecard_engine ✓", True), ("跳过评估直接发 Offer", False), ("规则拒绝：缺少评分 ✗", True)]
    for i, (t, bot) in enumerate(bubbles):
        y = Y0 + 70 + i * 84
        w = 26 + sum(22 if ord(c) > 255 else 12 for c in t)
        x = X0 + 450 - w - 10 if not bot else X0 + 24
        fill = (b if "✗" in t else a) if bot else "#fff"
        op = 0.85 if bot else 0.12
        s += f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="18" fill="{fill}" fill-opacity="{op}"/>'
        s += f'<text x="{x + 16}" y="{y + 37}" font-size="20" font-weight="600" fill="#fff">{escape(t)}</text>'
    return s


MOTIFS = dict(dashboard=m_dashboard, console=m_console, network=m_network, flow=m_flow, leaderboard=m_leaderboard,
              solar=m_solar, radar=m_radar, book=m_book, grid=m_grid, gauge=m_gauge, scatter=m_scatter, agent=m_agent)


def cover(name, tag, title, sub, chip_list, c1, c2, accent, accent2, motif, period=""):
    title_lines = title.split("\n")
    ty = 250 if len(title_lines) == 1 else 220
    title_svg = "".join(
        f'<text x="80" y="{ty + i * 70}" font-size="60" font-weight="800" fill="#fff" letter-spacing="1">{escape(t)}</text>'
        for i, t in enumerate(title_lines)
    )
    sub_y = ty + (len(title_lines) - 1) * 70 + 56
    tag_w = 40 + sum(22 if ord(c) > 255 else 12.5 for c in tag)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="g2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{accent}" stop-opacity="0.55"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{accent}" stop-opacity="0.55"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity="0.05"/></pattern>
<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000" flood-opacity="0.45"/></filter>
<marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#fff" fill-opacity="0.7"/></marker>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<circle cx="1040" cy="120" r="320" fill="url(#glow)"/>
<circle cx="120" cy="620" r="260" fill="url(#glow)" opacity="0.6"/>
<rect x="80" y="96" rx="20" width="{tag_w:.0f}" height="40" fill="{accent}" fill-opacity="0.22" stroke="{accent}" stroke-opacity="0.8"/>
<text x="100" y="123" font-size="20" font-weight="700" fill="#fff" letter-spacing="1">{escape(tag)}</text>
{f'<text x="{100 + tag_w:.0f}" y="123" font-size="20" fill="#fff" fill-opacity="0.7">{escape(period)}</text>' if period else ''}
{title_svg}
<text x="80" y="{sub_y}" font-size="28" fill="#fff" fill-opacity="0.82">{escape(sub)}</text>
<rect x="80" y="{sub_y + 30}" width="72" height="5" rx="2.5" fill="{accent2}"/>
{chips(chip_list, 80, 500, accent2)}
{window(X0, Y0, WW, WH, MOTIFS[motif](accent, accent2), accent)}
<text x="{W - 40}" y="{H - 28}" text-anchor="end" font-size="16" fill="#fff" fill-opacity="0.45">github.com/annawzhang</text>
</svg>
'''
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


COVERS = [
    # internships
    ("intern-lixiang", "实习 · 理想汽车", "AI 策略产品", "经营驾驶舱 · 销售 SOP 智能体 · VOC Agent",
     ["680 单元宽表", "5 类预警", "邀约 +1.8pp"], "#052e2b", "#0f766e", "#14b8a6", "#5eead4", "dashboard", "2026.07 – 至今"),
    ("intern-tencent", "实习 · 腾讯", "海外 HR 工作台 0→1", "AI 技术产品经理 · 海外薪酬福利",
     ["12 个 HR Agent", "未命中率 6%", "40min→3min"], "#071a3a", "#1d4ed8", "#3b82f6", "#93c5fd", "console", "2026.05 – 2026.07"),
    ("intern-byte", "实习 · 字节跳动 Seed", "招聘数据产品", "多 Agent 编排 · 八维可解释评估 · 漏斗 AB",
     ["20,121 人评分", "准确率 90.5%+", "招聘效率 +40%"], "#1e1046", "#4338ca", "#6366f1", "#c4b5fd", "network", "2026.02 – 2026.05"),
    ("intern-tcl", "实习 · TCL", "HRIS Demo\n与 OA 对接", "人力产品 · 入转调离流程 · 数据治理",
     ["20+ 交互 Demo", "HRIS/SAP/OA", "SQL 调优"], "#3b0a0a", "#b91c1c", "#ef4444", "#fca5a5", "flow", "2025.12 – 2026.02"),
    # competitions
    ("comp-flagos", "FlagOS 全球 AI 挑战赛", "全球 Top 2", "LongContext-ICL-Annotation · AI 产品负责人",
     ["Leaderboard 84.77", "Task8 满分", "PR #223"], "#2a1703", "#b45309", "#f59e0b", "#fde68a", "leaderboard", "Runner-up"),
    ("comp-waterna", "中国国际大学生创新大赛", "省金 / 国铜", "WaterNa 硅基光伏耦合发电机",
     ["多源能源数据", "特征工程", "商业化测算"], "#04263a", "#0369a1", "#0ea5e9", "#fde047", "solar", "核心成员"),
    ("comp-bizcase", "全国商业精英挑战赛", "全国三等奖", "宋锦品牌高端化策略",
     ["PEST", "波特五力", "LDA-SEM"], "#3a0718", "#9f1239", "#e11d48", "#fda4af", "radar", "核心成员"),
    # featured projects
    ("proj-portfolio", "作品集", "四段实习作品集", "背景 → 方案 → 架构 → 结果",
     ["理想", "腾讯", "字节", "TCL"], "#0b1324", "#334155", "#14b8a6", "#a5b4fc", "grid"),
    ("proj-handbook", "手册 · 开源", "People Product\nHandbook", "按四段实习归类 · 附录收录商赛与 Skills",
     ["人力产品", "Agent", "方法论"], "#1a0b3b", "#6d28d9", "#8b5cf6", "#f0abfc", "book"),
    ("proj-console", "Demo · 腾讯向", "Enterprise\nAI Console", "权限知识库 · 机器人看板 · 系统自检",
     ["工作台 0→1", "权限书架", "自检"], "#06182e", "#0e7490", "#06b6d4", "#93c5fd", "console"),
    ("proj-hiring-agent", "Demo · Agent", "Hiring Agent", "白名单调用评分卡 · 违规推进被规则拒绝",
     ["工具白名单", "规则护栏", "留痕"], "#2a0a2e", "#a21caf", "#d946ef", "#f472b6", "agent"),
    ("proj-talent", "Demo · 字节向", "Explainable\nTalent Scoring", "八维加权 · S+/S/A/B/C · 排他 AB",
     ["可解释", "分层", "AB 实验"], "#111536", "#3730a3", "#818cf8", "#22d3ee", "scatter"),
    ("proj-retail-kpi", "Demo · 理想向", "Retail KPI Cockpit", "同层健康分 · 预警归因 · 今天先管谁",
     ["健康分", "预警归因", "责任分派"], "#062a1f", "#047857", "#10b981", "#a3e635", "gauge"),
]

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for c in COVERS:
        cover(*c)
    print(f"wrote {len(COVERS)} covers to {OUT}")
