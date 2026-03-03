import streamlit as st
from streamlit_option_menu import option_menu

# 1. Configuração Inicial 
st.set_page_config(page_title="Coffee Insight", layout="wide", initial_sidebar_state="expanded")

# 2. Injeção de CSS (Contraste dos Botões Corrigido com Laranja Claro)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&display=swap');

    html, body, [class*="css"], .stMarkdown p {
        font-family: 'Roboto Condensed', sans-serif !important;
        color: #412314 !important; 
    }

    /* FUNDO PRINCIPAL: Bege */
    .stApp {
        background-color: #F5EEDC !important;
    }

    h1, h2, h3 {
        color: #412314 !important;
        font-weight: 700 !important;
    }

    /* SIDEBAR: Marrom Café */
    [data-testid="stSidebar"] {
        background-color: #412314 !important;
        border-right: none;
    }
    
    header {
        background: transparent !important;
    }
    
    /* ---------------------------------------------------
       CORES DOS BOTÕES DO MENU
       --------------------------------------------------- */
    /* 1. Botão Sanduíche/Setinha (Fundo Claro) -> Laranja Mais Claro (#DDA853) */
    [data-testid="collapsedControl"] svg {
        color: ##000000 !important;
        fill: ##000000 !important;
    }
        

    /* 2. Botão 'X' para fechar (Fundo Escuro da Sidebar) -> Cor Clara (Bege) */
    [data-testid="stSidebar"] button svg {
        color: #F5EEDC !important;
        fill: #F5EEDC !important;
    }
    
    /* Efeito ao passar o mouse no botão X */
    [data-testid="stSidebar"] button:hover {
        background-color: rgba(245, 238, 220, 0.1) !important;
    }
    /* --------------------------------------------------- */

    .block-container {padding-top: 1rem;}

    /* CARDS DE KPI */
    [data-testid="stMetric"] {
        background-color: #FFFFFF; 
        border-radius: 4px;
        padding: 15px 20px;
        box-shadow: none; 
        border-left: 6px solid #B65431; 
        border-top: 1px solid #e0d9c8;
        border-right: 1px solid #e0d9c8;
        border-bottom: 1px solid #e0d9c8;
    }

    [data-testid="stMetricLabel"] {
        color: #8c5b42 !important; 
        font-size: 15px !important;
        text-transform: uppercase;
        font-weight: 400 !important;
    }

    [data-testid="stMetricValue"] {
        color: #412314 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }

    hr {
        border-bottom: 2px solid #DDA853 !important;
        margin-top: 5px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar com Option Menu
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #DDA853 !important; padding-top: 20px; font-size: 26px;'>☕ Coffee Insight</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    pagina = option_menu(
        menu_title=None,
        options=["Visão Geral", "Clientes", "Produtos", "Vendas"],
        icons=["house-door", "person", "cup", "bar-chart-line"], 
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#412314", "border": "none"},
            "icon": {"color": "#DDA853", "font-size": "20px"}, 
            "nav-link": {
                "font-family": "'Roboto Condensed', sans-serif",
                "font-size": "17px",
                "text-align": "left",
                "margin": "8px 10px",
                "color": "#F5EEDC", 
                "border-radius": "4px",
            },
            "nav-link:hover": {
                "background-color": "rgba(221,168,83,0.15)", 
                "color": "#DDA853"
            },
            "nav-link-selected": {
                "background-color": "#B65431", 
                "color": "#F5EEDC",            
                "font-weight": "700"
            },
        }
    )

# 4. Título Principal da Tela Central
st.markdown("<h1>Painel Gerencial - Março 2024</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# 5. Estrutura das Páginas (Esqueleto)
if pagina == "Visão Geral":
    st.write("Acompanhamento macro do desempenho da cafeteria.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Faturamento Total", "R$ ---")
    with col2: st.metric("Total de Pedidos", "---")
    with col3: st.metric("Ticket Médio", "R$ ---")
    
    st.container(height=350, border=False)

elif pagina == "Clientes":
    st.write("Análise de métodos de pagamento e fidelidade.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: st.metric("Transações em Cartão", "--- %")
    with col2: st.metric("Transações em Dinheiro", "--- %")
    
    st.container(height=350, border=False)

elif pagina == "Produtos":
    st.write("Quais cafés estão gerando mais receita.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Produto Mais Vendido", "---")
    with col2: st.metric("Produto Menos Vendido", "---")
    with col3: st.metric("Receita do Top 1", "R$ ---")
    
    st.container(height=350, border=False)

elif pagina == "Vendas":
    st.write("Análise de horários de pico e dias da semana.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: st.metric("Horário de Pico", "---")
    with col2: st.metric("Melhor Dia da Semana", "---")
    
    st.container(height=350, border=False)