import streamlit as st
from streamlit_option_menu import option_menu

# ── Page Config ──────────────────────────────────────────────────────────────
# Sets the browser tab title, uses the full screen width, and keeps the
# sidebar open by default when the app loads.
st.set_page_config(
    page_title="Coffee Insight",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global Styles ─────────────────────────────────────────────────────────────
# All visual customisation lives here in a single CSS block injected via
# st.markdown. Using CSS custom properties (--variables) means the entire
# colour palette can be changed in one place without hunting through the file.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Design tokens ───────────────────────────────────────────────────────────
   Every colour used in the app is defined here.
   --bg        : main content background (warm beige)
   --surface   : card / widget background (white)
   --sidebar   : sidebar panel background (dark espresso brown)
   --accent    : left border on KPI cards and selected menu item (burnt orange)
   --gold      : horizontal divider and icon highlight colour
   --text      : primary readable text (near-black brown)
   --text-soft : secondary / label text (medium brown)
   --border    : subtle card borders
   ──────────────────────────────────────────────────────────────────────── */
:root {
    --bg:        #F5EEDC;
    --surface:   #FFFFFF;
    --sidebar:   #412314;
    --accent:    #B65431;
    --gold:      #B8860B;
    --text:      #1A0A04;
    --text-soft: #5C3D28;
    --border:    #D4C4B0;
}

/* ── Base typography & background ───────────────────────────────────────────
   Apply DM Sans globally and set the warm beige app background.
   The broad [class*="css"] selector catches Streamlit's generated classnames. */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }
.block-container { padding-top: 1.5rem !important; }

/* ── Main content text contrast ─────────────────────────────────────────────
   Streamlit sometimes overrides heading and paragraph colours to a light grey.
   We re-assert dark text here, scoped to .stApp to avoid touching the sidebar. */
.stApp h1, .stApp h2, .stApp h3,
.stApp p, .stApp span {
    color: var(--text) !important;
}

/* ── Top chrome (Streamlit header bar) ──────────────────────────────────────
   The thin header bar Streamlit renders at the very top is made transparent
   so it blends into our beige background. */
header { background: transparent !important; }

/* ── Sidebar panel ───────────────────────────────────────────────────────────
   Sets the dark espresso brown background for the whole sidebar area. */
[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
}

/* ── Sidebar collapse arrow button ───────────────────────────────────────────
   The arrow/chevron that collapses the sidebar sits on the dark background.
   We use multiple overlapping selectors because Streamlit changes the exact
   data-testid across versions — this ensures at least one always matches. */
[data-testid="stSidebar"] button svg,
[data-testid="stSidebar"] button[kind="header"] svg,
[data-testid="stSidebar"] .stButton button svg {
    color: #F4A460 !important;
    fill: #F4A460 !important;
    stroke: #F4A460 !important;
}
[data-testid="stSidebar"] button:hover {
    background-color: rgba(244, 164, 96, 0.12) !important;
}

/* ── Hamburger icon (sidebar collapsed, on light beige background) ───────────
   When the sidebar is collapsed the toggle button sits on the beige main
   background, so the icon needs to be dark to contrast against it. */
[data-testid="collapsedControl"] svg {
    fill: var(--text) !important;
}

/* ── KPI metric cards ────────────────────────────────────────────────────────
   Each st.metric() renders inside [data-testid="stMetric"]. We give each card
   a white background, a coloured left border as a visual anchor, and a subtle
   border on the other three sides to lift it off the beige background. */
[data-testid="stMetric"] {
    background-color: var(--surface) !important;
    border-radius: 6px;
    padding: 18px 22px;
    border-left: 5px solid var(--accent);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}

/* Label (e.g. "FATURAMENTO TOTAL") — uppercased and softened */
[data-testid="stMetricLabel"] {
    color: var(--text-soft) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Value (e.g. "R$ —") — large serif for visual weight */
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 30px !important;
}

/* ── Section divider ─────────────────────────────────────────────────────────
   The <hr> below the page title uses a gold colour to add warmth and echo
   the coffee-shop aesthetic. */
hr {
    border: none !important;
    border-bottom: 2px solid var(--gold) !important;
    margin: 4px 0 24px !important;
}

/* ── Page subtitle ───────────────────────────────────────────────────────────
   The short descriptive line below the divider uses the softer brown so it
   reads as secondary information without vanishing into the background. */
.subtitle {
    color: var(--text-soft) !important;
    font-size: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation styles ─────────────────────────────────────────────────
# Extracted into a constant so the option_menu() call below stays readable.
# All colours are hardcoded strings here because streamlit_option_menu doesn't
# accept CSS variables — it inlines the styles directly into the component.
MENU_STYLES = {
    # The nav container itself should be invisible (same colour as sidebar).
    "container": {"padding": "0", "background-color": "#412314", "border": "none"},
    # Icons use the warm gold to stand out against the dark sidebar.
    "icon": {"color": "#DDA853", "font-size": "18px"},
    # Inactive nav links: light beige text on dark background.
    "nav-link": {
        "font-family": "'DM Sans', sans-serif",
        "font-size": "16px",
        "color": "#F5EEDC",
        "margin": "4px 10px",
        "border-radius": "4px",
    },
    # Active / selected link: filled with burnt orange so the current page is
    # immediately obvious, with white text for maximum contrast.
    "nav-link-selected": {
        "background-color": "#B65431",
        "color": "#FFFFFF",
        "font-weight": "500",
    },
}

# ── Sidebar content ───────────────────────────────────────────────────────────
# Everything inside this block renders in the sidebar panel.
with st.sidebar:
    # App logo / title — Playfair Display gives it a refined, editorial feel.
    # Colour #DDA853 (warm gold) contrasts well against the dark sidebar.
    st.markdown(
        "<h2 style='text-align:center; color:#F4A460; padding:24px 0 8px; "
        "font-family:Playfair Display,serif; font-size:24px; letter-spacing:0.02em;'>"
        "☕ Coffee Insight</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # option_menu renders a styled navigation list.
    # The selected page name is returned as a plain string (e.g. "Visão Geral").
    page = option_menu(
        menu_title=None,
        options=["Visão Geral", "Clientes", "Produtos", "Vendas"],
        icons=["house-door", "person", "cup", "bar-chart-line"],
        default_index=0,
        styles=MENU_STYLES,
    )

# ── Page header ───────────────────────────────────────────────────────────────
# Rendered outside the sidebar block so it always appears in the main area.
# Inline colour is hardcoded to guarantee Streamlit doesn't override it.
st.markdown(
    "<h1 style='font-family:Playfair Display,serif; font-size:32px; color:#1A0A04;'>"
    "Painel Gerencial — Março 2024</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────────────────
# Each branch renders the content for the selected sidebar page.
# st.columns() splits the row into equal-width sections for the KPI cards.

if page == "Visão Geral":
    st.markdown("<p class='subtitle'>Acompanhamento macro do desempenho da cafeteria.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", "R$ —")
    col2.metric("Total de Pedidos", "—")
    col3.metric("Ticket Médio", "R$ —")

    st.container(height=350, border=False)  # placeholder for future chart

elif page == "Clientes":
    st.markdown("<p class='subtitle'>Análise de métodos de pagamento e fidelidade.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Transações em Cartão", "— %")
    col2.metric("Transações em Dinheiro", "— %")

    st.container(height=350, border=False)  # placeholder for future chart

elif page == "Produtos":
    st.markdown("<p class='subtitle'>Quais cafés estão gerando mais receita.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Produto Mais Vendido", "—")
    col2.metric("Produto Menos Vendido", "—")
    col3.metric("Receita do Top 1", "R$ —")

    st.container(height=350, border=False)  # placeholder for future chart

elif page == "Vendas":
    st.markdown("<p class='subtitle'>Análise de horários de pico e dias da semana.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Horário de Pico", "—")
    col2.metric("Melhor Dia da Semana", "—")

    st.container(height=350, border=False)  # placeholder for future chart