import streamlit as st

st.set_page_config(
    page_title="Coffee Insight",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "sb_open" not in st.session_state:
    st.session_state.sb_open = True
if "page" not in st.session_state:
    st.session_state.page = "Visão Geral"

PAGES = ["Visão Geral", "Clientes", "Produtos", "Vendas"]

ICONS = {
    "Visão Geral": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23E8D8C4' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E",
    "Clientes":    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23E8D8C4' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E",
    "Produtos":    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23E8D8C4' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M18 8h1a4 4 0 0 1 0 8h-1'/%3E%3Cpath d='M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z'/%3E%3Cline x1='6' y1='1' x2='6' y2='4'/%3E%3Cline x1='10' y1='1' x2='10' y2='4'/%3E%3Cline x1='14' y1='1' x2='14' y2='4'/%3E%3C/svg%3E",
    "Vendas":      "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23E8D8C4' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'/%3E%3Cline x1='12' y1='20' x2='12' y2='4'/%3E%3Cline x1='6' y1='20' x2='6' y2='14'/%3E%3Cline x1='2' y1='20' x2='22' y2='20'/%3E%3C/svg%3E",
}
# Icon colour variants via URL-encoded stroke colour
ICONS_ACT  = {k: v.replace("%23E8D8C4", "%23F4A460") for k, v in ICONS.items()}  # orange active
ICONS_DARK = {k: v.replace("%23E8D8C4", "%232E1710") for k, v in ICONS.items()}  # dark for rail
ICONS_WHITE= {k: v.replace("%23E8D8C4", "%23FFFFFF") for k, v in ICONS.items()}  # white for active rail

is_open = st.session_state.sb_open
page    = st.session_state.page

# JS helper: clicks the hidden Streamlit button matching a given key label.
# This bridges the gap between our custom HTML nav and Streamlit's event loop.
def js_click(label: str) -> str:
    safe = label.replace("'", "\\'")
    return (
        "var btns = window.parent.document.querySelectorAll('.stButton button');"
        f"for(var i=0;i<btns.length;i++){{if(btns[i].innerText.trim()==='{safe}'){{btns[i].click();break;}}}}"
    )

def icon_img(name: str, size: int = 18, variant: str = "default") -> str:
    src = {"active": ICONS_ACT, "dark": ICONS_DARK, "white": ICONS_WHITE}.get(variant, ICONS)[name]
    return f'<img src="{src}" width="{size}" height="{size}" style="flex-shrink:0">'

HAMBURGER_SVG = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
  <line x1="3" y1="6"  x2="21" y2="6"/>
  <line x1="3" y1="12" x2="21" y2="12"/>
  <line x1="3" y1="18" x2="21" y2="18"/>
</svg>"""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&family=Saira+Condensed:wght@400;600;700&display=swap');

:root {
    --bg:         #F5EEDC;
    --surface:    #FFFFFF;
    --sidebar:    #412314;
    --sidebar-dk: #2E1710;
    --accent:     #B65431;
    --gold:       #DDA853;
    --orange-lt:  #F4A460;
    --text:       #1A0A04;
    --text-soft:  #5C3D28;
    --border:     #D4C4B0;
    --nav-text:   #E8D8C4;
    --nav-muted:  #9C7A65;
}

html, body, [class*="css"] {
    font-family: 'Roboto Condensed', sans-serif !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
header,
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

/* Remove gap between sidebar and content columns */
div[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: stretch !important;
}

/* ── Hamburger button (shared) ── */
.hbg {
    cursor: pointer;
    color: var(--orange-lt);
    display: flex; align-items: center; justify-content: center;
    width: 36px; height: 36px;
    border-radius: 6px;
    transition: background 0.15s;
}
.hbg:hover { background: rgba(244,164,96,0.18); }

/* ════════════════════════
   COLLAPSED RAIL
   ════════════════════════ */
.rail {
    width: 64px;
    min-height: 100vh;
    background: var(--orange-lt);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 14px;
}
.rail-sep {
    width: 32px; height: 1px;
    background: rgba(65,35,20,0.28);
    margin: 10px 0 12px;
}
.rail-item {
    width: 44px; height: 44px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    margin-bottom: 4px;
    transition: background 0.15s;
}
.rail-item:hover   { background: rgba(65,35,20,0.15); }
.rail-item.active  { background: var(--accent); }

/* ════════════════════════
   EXPANDED PANEL
   ════════════════════════ */
.panel {
    width: 256px;
    min-height: 100vh;
    background: var(--sidebar);
    display: flex;
    flex-direction: column;
}

/* Header block */
.panel-hdr {
    background: var(--sidebar-dk);
    padding: 18px 18px 16px;
    border-bottom: 1px solid rgba(244,164,96,0.2);
    position: relative;
}
.panel-hdr::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: var(--orange-lt);
}
.panel-brand {
    display: flex; align-items: center;
    justify-content: space-between;
}
.panel-brand-left {
    display: flex; align-items: center; gap: 11px;
}
.panel-icon {
    width: 38px; height: 38px;
    background: var(--accent); border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; flex-shrink: 0;
}
.panel-name {
    font-family: 'Saira Condensed', sans-serif;
    font-size: 20px; font-weight: 700;
    color: var(--orange-lt);
    line-height: 1; display: block;
}
.panel-tagline {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 10px; color: var(--nav-muted);
    margin-top: 2px; letter-spacing: 0.07em;
    text-transform: uppercase; display: block;
}

/* Section label */
.panel-section {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 10px; font-weight: 700;
    color: var(--nav-muted);
    letter-spacing: 0.14em; text-transform: uppercase;
    padding: 18px 20px 6px;
}

/* Nav items */
.panel-nav { padding: 0 10px; flex: 1; }
.nav-item {
    display: flex; align-items: center; gap: 11px;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 2px;
    border-left: 3px solid transparent;
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 15px;
    color: var(--nav-text);
    transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.nav-item:hover {
    background: rgba(244,164,96,0.1);
    color: var(--gold);
    border-color: rgba(221,168,83,0.3);
}
.nav-item.active {
    background: rgba(182,84,49,0.28);
    color: var(--orange-lt);
    font-weight: 700;
    border-color: var(--accent);
}

/* Footer */
.panel-footer {
    padding: 12px 20px 16px;
    border-top: 1px solid rgba(244,164,96,0.12);
}
.panel-footer span {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 11px; color: var(--nav-muted);
    display: flex; align-items: center; gap: 7px;
}
.dot {
    width: 6px; height: 6px;
    background: var(--accent); border-radius: 50%;
    display: inline-block;
}

/* ════════════════════
   HIDDEN STREAMLIT BUTTONS
   Rendered off-screen so JS can click them,
   but they never appear visually.
   ════════════════════ */
.hidden-btns {
    position: absolute;
    width: 1px; height: 1px;
    opacity: 0; overflow: hidden;
    pointer-events: none;
}

/* ════════════════════
   MAIN CONTENT
   ════════════════════ */
.main {
    padding: 30px 38px;
    background: var(--bg);
    flex: 1;
}
.page-title {
    font-family: 'Saira Condensed', sans-serif;
    font-size: 32px; font-weight: 700;
    color: #1A0A04; margin: 0 0 4px;
}
.page-bar {
    width: 48px; height: 4px;
    background: var(--accent);
    border-radius: 2px; margin-bottom: 22px;
}
.subtitle {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 15px; color: var(--text-soft); margin-bottom: 22px;
}

/* KPI cards */
[data-testid="stMetric"] {
    background-color: var(--surface) !important;
    border-radius: 6px !important;
    padding: 18px 22px !important;
    border-left: 5px solid var(--accent) !important;
    border-top: 1px solid var(--border) !important;
    border-right: 1px solid var(--border) !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Roboto Condensed', sans-serif !important;
    font-size: 12px !important; font-weight: 700 !important;
    color: var(--text-soft) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Saira Condensed', sans-serif !important;
    font-size: 34px !important; font-weight: 700 !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Build sidebar HTML ────────────────────────────────────────────────────────
if is_open:
    nav_html = ""
    for p in PAGES:
        cls     = "nav-item active" if p == page else "nav-item"
        ico     = icon_img(p, 18, "active" if p == page else "default")
        nav_html += f'<div class="{cls}" onclick="{js_click(p)}">{ico}<span>{p}</span></div>'

    sidebar_html = f"""
    <div class="panel">
        <div class="panel-hdr">
            <div class="panel-brand">
                <div class="panel-brand-left">
                    <div class="panel-icon">☕</div>
                    <div>
                        <span class="panel-name">Coffee Insight</span>
                        <span class="panel-tagline">Painel Gerencial</span>
                    </div>
                </div>
                <div class="hbg" onclick="{js_click('__TOGGLE__')}">{HAMBURGER_SVG}</div>
            </div>
        </div>
        <div class="panel-section">Navegação</div>
        <div class="panel-nav">{nav_html}</div>
        <div class="panel-footer">
            <span><i class="dot"></i>Março 2024</span>
        </div>
    </div>"""
else:
    rail_html = ""
    for p in PAGES:
        cls  = "rail-item active" if p == page else "rail-item"
        ico  = icon_img(p, 22, "white" if p == page else "dark")
        rail_html += f'<div class="{cls}" title="{p}" onclick="{js_click(p)}">{ico}</div>'

    sidebar_html = f"""
    <div class="rail">
        <div class="hbg" onclick="{js_click('__TOGGLE__')}" style="color:#2E1710">{HAMBURGER_SVG}</div>
        <div class="rail-sep"></div>
        {rail_html}
    </div>"""

# ── Layout ────────────────────────────────────────────────────────────────────
col_sb, col_main = st.columns([256, 900] if is_open else [64, 900], gap="small")

with col_sb:
    st.markdown(sidebar_html, unsafe_allow_html=True)

    # Hidden buttons — rendered in a 1×1px invisible div.
    # The JS in the HTML onclick attributes finds and clicks these.
    st.markdown('<div class="hidden-btns">', unsafe_allow_html=True)

    if st.button("__TOGGLE__", key="toggle"):
        st.session_state.sb_open = not st.session_state.sb_open
        st.rerun()

    for p in PAGES:
        if st.button(p, key=f"nav_{p}"):
            st.session_state.page = p
            if not st.session_state.sb_open:
                st.session_state.sb_open = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────────────────────────
with col_main:
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>Painel Gerencial — Março 2024</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-bar'></div>", unsafe_allow_html=True)

    if page == "Visão Geral":
        st.markdown("<p class='subtitle'>Acompanhamento macro do desempenho da cafeteria.</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Total", "R$ —")
        c2.metric("Total de Pedidos",  "—")
        c3.metric("Ticket Médio",      "R$ —")
        st.container(height=350, border=False)

    elif page == "Clientes":
        st.markdown("<p class='subtitle'>Análise de métodos de pagamento e fidelidade.</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Transações em Cartão",   "— %")
        c2.metric("Transações em Dinheiro", "— %")
        st.container(height=350, border=False)

    elif page == "Produtos":
        st.markdown("<p class='subtitle'>Quais cafés estão gerando mais receita.</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Produto Mais Vendido",  "—")
        c2.metric("Produto Menos Vendido", "—")
        c3.metric("Receita do Top 1",      "R$ —")
        st.container(height=350, border=False)

    elif page == "Vendas":
        st.markdown("<p class='subtitle'>Análise de horários de pico e dias da semana.</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Horário de Pico",      "—")
        c2.metric("Melhor Dia da Semana", "—")
        st.container(height=350, border=False)

    st.markdown("</div>", unsafe_allow_html=True)