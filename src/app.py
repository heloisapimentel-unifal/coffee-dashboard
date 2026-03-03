import streamlit as st

st.set_page_config(
    page_title="Coffee Insight",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Visão Geral"

PAGES = ["Visão Geral", "Clientes", "Produtos", "Vendas"]

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

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Roboto Condensed', sans-serif !important;
    color: var(--text) !important;
}
.stApp           { background-color: var(--bg) !important; }
.block-container { padding-top: 1.5rem !important; }
header           { background: transparent !important; }

.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Saira Condensed', sans-serif !important;
    color: var(--text) !important;
}

/* ── Sidebar shell ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

/* ── Collapse/expand arrows: orange-lt on dark bg ── */
[data-testid="stSidebar"] svg {
    fill:   var(--orange-lt) !important;
    stroke: var(--orange-lt) !important;
}
/* Hamburger on beige bg when collapsed: dark */
[data-testid="collapsedControl"] svg {
    fill:   var(--text) !important;
    stroke: none !important;
}

/* ── Sidebar header block ── */
.sb-header {
    background:    var(--sidebar-dk);
    padding:       20px 18px 16px;
    border-bottom: 1px solid rgba(244,164,96,0.2);
    position:      relative;
    margin-bottom: 4px;
}
.sb-header::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: var(--orange-lt);
}
.sb-brand { display: flex; align-items: center; gap: 12px; }
.sb-icon-box {
    width: 38px; height: 38px;
    background: var(--accent); border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; flex-shrink: 0;
}
.sb-name {
    font-family: 'Saira Condensed', sans-serif;
    font-size: 20px; font-weight: 700;
    color: var(--orange-lt); display: block; line-height: 1;
}
.sb-tagline {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 10px; color: var(--nav-muted);
    margin-top: 2px; letter-spacing: 0.07em;
    text-transform: uppercase; display: block;
}

/* ── Section label ── */
.sb-nav-label {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 10px; font-weight: 700;
    color: var(--nav-muted);
    letter-spacing: 0.14em; text-transform: uppercase;
    padding: 18px 20px 6px;
}

/* ── Footer ── */
.sb-footer {
    padding: 14px 20px 18px;
    border-top: 1px solid rgba(244,164,96,0.12);
}
.sb-footer-row {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 11px; color: var(--nav-muted);
    display: flex; align-items: center; gap: 7px;
}
.sb-dot {
    width: 6px; height: 6px;
    background: var(--accent); border-radius: 50%;
    display: inline-block;
}

/* ══════════════════════════════════════════════
   RADIO NAV
   st.radio is the only reliable Streamlit widget
   for navigation. We style it to look exactly
   like a modern sidebar menu.
   ══════════════════════════════════════════════ */

/* Hide the widget label ("nav") */
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] {
    display: none !important;
}

/* Radio group container */
[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {
    display:        flex !important;
    flex-direction: column !important;
    gap:            0 !important;
    padding:        0 10px !important;
}

/* Each label = one nav row */
[data-testid="stSidebar"] .stRadio label {
    display:        flex !important;
    align-items:    center !important;
    width:          100% !important;
    padding:        11px 14px !important;
    margin:         2px 0 !important;
    border-radius:  8px !important;
    cursor:         pointer !important;
    font-family:    'Roboto Condensed', sans-serif !important;
    font-size:      15px !important;
    font-weight:    400 !important;
    color:          var(--nav-text) !important;
    background:     transparent !important;
    border-left:    3px solid transparent !important;
    box-sizing:     border-box !important;
    transition:     background 0.15s, color 0.15s, border-color 0.15s !important;
}

/* Hide the radio circle completely */
[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}

/* Hover */
[data-testid="stSidebar"] .stRadio label:hover {
    background:   rgba(244,164,96,0.1) !important;
    color:        var(--gold) !important;
    border-color: rgba(221,168,83,0.3) !important;
}

/* Selected — uses aria-checked which Streamlit always sets correctly */
[data-testid="stSidebar"] .stRadio label[aria-checked="true"] {
    background:  rgba(182,84,49,0.28) !important;
    color:       var(--orange-lt) !important;
    font-weight: 700 !important;
    border-color: var(--accent) !important;
}
[data-testid="stSidebar"] .stRadio label[aria-checked="true"]:hover {
    background: rgba(182,84,49,0.38) !important;
}

/* ── KPI cards ── */
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
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Saira Condensed', sans-serif !important;
    font-size: 34px !important; font-weight: 700 !important;
    color: var(--text) !important;
}

/* ── Page header ── */
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
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-brand">
            <div class="sb-icon-box">☕</div>
            <div>
                <span class="sb-name">Coffee Insight</span>
                <span class="sb-tagline">Painel Gerencial</span>
            </div>
        </div>
    </div>
    <div class="sb-nav-label">Navegação</div>
    """, unsafe_allow_html=True)

    # st.radio returns the selected label string directly.
    # aria-checked="true" is set by Streamlit on the active label — our CSS
    # uses this to highlight the active item reliably.
    page = st.radio(
        label="nav",
        options=PAGES,
        index=PAGES.index(st.session_state.page),
    )
    # Keep session state in sync (needed if other widgets also change the page)
    st.session_state.page = page

    st.markdown("""
    <div class="sb-footer">
        <div class="sb-footer-row">
            <span class="sb-dot"></span>Março 2024
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────────────────────────
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