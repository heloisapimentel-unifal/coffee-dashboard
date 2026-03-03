import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Coffee Insight",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Carregamento de Dados ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data', 'Coffe_sales.xlsx')
        return pd.read_excel(file_path)
    except Exception:
        return pd.DataFrame({'money': [0], 'coffee_name': ['-'], 'Weekday': ['-'], 'card': [None]})

df = load_data()

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Visão Geral"
if "prev_page" not in st.session_state:
    st.session_state.prev_page = st.session_state.page
# --- Lógica de Scroll Persistente ---
if "prev_page" not in st.session_state:
    st.session_state.prev_page = st.session_state.page

if st.session_state.prev_page != st.session_state.page:
    st.components.v1.html(
        """
        <script>
            function performScroll() {
                const parentDoc = window.parent.document;
                const anchor = parentDoc.getElementById('top-anchor');
                const mainContainer = parentDoc.querySelector('.main');
                
                if (anchor) {
                    anchor.scrollIntoView({block: 'start', behavior: 'instant'});
                } else if (mainContainer) {
                    mainContainer.scrollTo(0, 0);
                }
            }

            // Executa o scroll em rajada para vencer o carregamento dos gráficos
            performScroll(); 
            let intervals = [100, 300, 600, 1000, 2000];
            intervals.forEach(t => setTimeout(performScroll, t));
        </script>
        """,
        height=0,
    )
    st.session_state.prev_page = st.session_state.page
PAGES = ["Visão Geral", "Clientes", "Produtos", "Vendas"]

# Ícones SVG outline — estilo Lucide (mesmo da imagem de referência)
SVG_ICONS = {
    "Visão Geral": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "Clientes":    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "Produtos":    '<path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><line x1="6" x2="6" y1="2" y2="4"/><line x1="10" x2="10" y1="2" y2="4"/><line x1="14" x2="14" y1="2" y2="4"/>',
    "Vendas":      '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
}

# ── CSS Global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&family=Saira+Condensed:wght@400;600;700&display=swap');

:root {
    --bg:         #F5EEDC;
    --surface:    #FFFFFF;
    --sidebar:    #412314;
    --sidebar-dk: #2E1710;
    --accent:     #BA5934;
    --gold:       #CD9B26;
    --orange-lt:  #DB6A19;
    --text:       #1A0A04;
    --text-soft:  #42210B;
    --border:     #D4C4B0;
}
/* Alvo: O fundo do container na segunda coluna (Mais Vendido) */
/* Alvo ultra-específico para o fundo do segundo card */
    [data-testid="column"]:nth-of-type(2) [data-testid="metric-container"] {
        background-color: #95A75F !important;
        border: 1px solid #95A75F !important;
        padding: 10px 15px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
html, body, [class*="css"] {
    font-family: 'Roboto Condensed', sans-serif !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }
.block-container { padding-top: 1.5rem !important; }
header { background: transparent !important; }
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Saira Condensed', sans-serif !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── Botão laranja de abrir/fechar ── */
[data-testid="collapsedControl"] {
    background-color: var(--orange-lt) !important;
    border-radius: 0 8px 8px 0 !important;
}
[data-testid="collapsedControl"]:hover { background-color: var(--accent) !important; }
[data-testid="collapsedControl"] svg { fill: #FFFFFF !important; stroke: none !important; }
[data-testid="stSidebarCollapseButton"] > button {
    background-color: var(--orange-lt) !important;
    border-radius: 50% !important;
    border: none !important;
}
[data-testid="stSidebarCollapseButton"] > button:hover { background-color: var(--accent) !important; }
[data-testid="stSidebarCollapseButton"] svg { fill: #FFFFFF !important; stroke: none !important; }

/* ── Esconde os botões nativos do Streamlit na Sidebar ── */
[data-testid="stSidebar"] .nav-hidden {
    display: none !important;
}

/* Caso queira manter a acessibilidade para o JS clicar neles, use este: */
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:has(button[kind="secondary"]) {
    display: none;
}

/* ── iframe sem borda/fundo branco ── */
[data-testid="stSidebar"] iframe { background: transparent !important; }

/* ── KPI Cards ── */
[data-testid="stMetric"] {
    background-color: var(--surface) !important; border-radius: 6px !important;
    padding: 18px 22px !important; border-left: 5px solid var(--accent) !important;
    border-top: 1px solid var(--border) !important; border-right: 1px solid var(--border) !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Roboto Condensed', sans-serif !important; font-size: 12px !important;
    font-weight: 700 !important; color: var(--text-soft) !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Saira Condensed', sans-serif !important; font-size: 24px !important;
    font-weight: 700 !important; color: var(--text) !important;
}

/* ── Page Header ── */
.page-title { font-family: 'Saira Condensed', sans-serif; font-size: 32px; font-weight: 700; color: #1A0A04; margin: 0 0 4px; }
.page-bar { width: 48px; height: 4px; background: #BA5934; border-radius: 2px; margin-bottom: 22px; }
.subtitle { font-family: 'Roboto Condensed', sans-serif; font-size: 15px; color: #42210B; margin-bottom: 22px; }

/* ── Top 5 Table ── */
.t5-box { background: #FFFFFF; border: 1px solid #D4C4B0; border-radius: 6px; padding: 20px; }
.t5-row { display: flex; align-items: center; margin-bottom: 15px; }
.t5-row:last-child { margin-bottom: 0; }
.t5-name { width: 32%; font-weight: 700; font-size: 14px; color: #1A0A04; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.t5-track { flex: 1; height: 8px; background: #F5EEDC; border-radius: 4px; margin: 0 12px; overflow: hidden; }
.t5-fill { height: 100%; background: #BA5934; border-radius: 4px; }
.t5-val { width: 30%; text-align: right; font-weight: 700; font-size: 14px; color: #42210B; white-space: nowrap; }

/* ── Sidebar branding ── */
.sb-header {
    background: #2E1710; padding: 20px 18px 16px;
    border-bottom: 1px solid rgba(244,164,96,0.2); position: relative;
}
.sb-header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #DB6A19; }
.sb-brand { display: flex; align-items: center; gap: 12px; }
.sb-icon-box { width: 38px; height: 38px; background: #BA5934; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 19px; flex-shrink: 0; }
.sb-name { font-family: 'Saira Condensed', sans-serif; font-size: 20px; font-weight: 700; color: #DB6A19; display: block; line-height: 1; }
.sb-tagline { font-family: 'Roboto Condensed', sans-serif; font-size: 10px; color: #9C7A65; margin-top: 2px; letter-spacing: 0.07em; text-transform: uppercase; display: block; }
.sb-footer { padding: 14px 20px 18px; border-top: 1px solid rgba(244,164,96,0.12); }
.sb-footer-row { font-family: 'Roboto Condensed', sans-serif; font-size: 11px; color: #9C7A65; display: flex; align-items: center; gap: 7px; }
.sb-dot { width: 6px; height: 6px; background: #BA5934; border-radius: 50%; display: inline-block; }
</style>
""", unsafe_allow_html=True)


# ── Scroll pro topo ao mudar de página ───────────────────────────────────────
if st.session_state.prev_page != st.session_state.page:
    st.session_state.prev_page = st.session_state.page
    st.components.v1.html("""
        <script>
            window.parent.document.querySelector('.main')
                ?.scrollTo({ top: 0, behavior: 'instant' });
            window.parent.document.querySelector('[data-testid="stAppViewContainer"]')
                ?.scrollTo({ top: 0, behavior: 'instant' });
        </script>
    """, height=0)


# ── Nav HTML com ícones SVG (fiel à imagem de referência) ────────────────────
def build_nav_html(current_page: str) -> str:
    items = ""
    for p in PAGES:
        active  = p == current_page
        icon    = SVG_ICONS[p]
        bg      = "background:rgba(186,89,52,0.32); border-radius:8px;" if active else "border-radius:8px;"
        border  = "border-left:3px solid #DB6A19;" if active else "border-left:3px solid transparent;"
        t_col   = "#DB6A19" if active else "#C8B5A0"
        i_col   = "#DB6A19" if active else "#8A6A55"
        weight  = "700"     if active else "400"
        cls     = "item active" if active else "item"

        items += f"""
        <div class="{cls}" data-page="{p}" style="{bg}{border}">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                 viewBox="0 0 24 24" fill="none"
                 stroke="{i_col}" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">
                {icon}
            </svg>
            <span style="color:{t_col};font-weight:{weight};">{p}</span>
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
<style>
    
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; padding:0 10px; font-family:'Roboto Condensed',sans-serif; }}
  .nav-label {{
      font-size:10px; font-weight:700; color:#7A5A48;
      letter-spacing:.14em; text-transform:uppercase;
      padding:16px 6px 8px;
  }}
  .item {{
      display:flex; align-items:center; gap:13px;
      padding:12px 12px; margin:3px 0; cursor:pointer;
      transition:background .15s, border-color .15s;
  }}
  .item:hover:not(.active) {{
      background:rgba(244,164,96,.1);
      border-left-color:rgba(219,106,25,.4) !important;
  }}
  .item span {{ font-size:15px; letter-spacing:.01em; }}
</style>
</head>
<body>
  <div class="nav-label">Navegação</div>
  {items}
  <script>
    document.querySelectorAll('.item').forEach(function(el) {{
                el.addEventListener('click', function() {{
                    var pageName = this.getAttribute('data-page');
                var parent = window.parent.document;    
                var mainContent = parent.querySelector('.main');
                var appContainer = parent.querySelector('[data-testid="stAppViewContainer"]');
    
                if (mainContent) mainContent.scrollTo({{ top: 0, behavior: 'instant' }});
                if (appContainer) appContainer.scrollTo({{ top: 0, behavior: 'instant' }});

                // Clica no botão invisível do Streamlit para mudar a página
                parent.querySelectorAll('[data-testid="stSidebar"] button').forEach(function(btn) {{
                 if (btn.innerText.trim() === pageName) btn.click();
                }});
            }});
    }});

  </script>
</body>
</html>"""

# ── Sidebar ──────────────────────────────────────────────────────────────────
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
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-hidden">', unsafe_allow_html=True)
    for p in PAGES:
        if st.button(p, key=f"nav_{p}"):
            if st.session_state.page != p:
                st.session_state.page = p
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.components.v1.html(
        build_nav_html(st.session_state.page),
        height=260,
        scrolling=False,
    )

    # 4. Rodapé
    st.markdown("""
    <div class="sb-footer">
        <div class="sb-footer-row"><span class="sb-dot"></span>Março 2024</div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
page = st.session_state.page

st.markdown("<div class='page-title'>Painel Gerencial — Março 2024</div>", unsafe_allow_html=True)
st.markdown("<div class='page-bar'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
if page == "Visão Geral":
    st.markdown("<p class='subtitle'>Acompanhamento macro do desempenho da cafeteria.</p>", unsafe_allow_html=True)

    fat_total = df['money'].sum()
    tm = df['money'].mean()
    mv  = df['coffee_name'].value_counts().idxmax() if 'coffee_name' in df.columns and not df.empty else "-"
    dmf = df['Weekday'].value_counts().idxmin()     if 'Weekday'      in df.columns and not df.empty else "-"
    dias_pt = {'Sun':'Domingo','Mon':'Segunda','Tue':'Terça','Wed':'Quarta','Thu':'Quinta','Fri':'Sexta','Sat':'Sábado'}

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Faturamento Total", f"$ {fat_total:,.2f}".replace(',','X').replace('.',',').replace('X','.'))
    c2.metric("MAIS VENDIDO", mv, help=f"O item mais vendido é: {mv}")
    c3.metric("MENOS VENDIDO", "Espresso", help="O item menos vendido é: Espresso")
    c4.metric("DIA MAIS FRACO", dias_pt.get(dmf, dmf), help=f"O dia com menor movimento é: {dias_pt.get(dmf, dmf)}")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1], gap="large")
    with col1:
        st.markdown("### Perfil de Clientes (Fidelidade)")
        if 'card' in df.columns:
            fid = df['card'].dropna().value_counts().reset_index()
            fid.columns = ['card','visitas']
            def cat_fid(v):
                if v >= 10: return 'VIP (10+)'
                if v >= 5:  return 'Fiel (5-9)'
                if v >= 2:  return 'Recorrente (2-4)'
                return 'Único (1)'
            fid['categoria'] = fid['visitas'].apply(cat_fid)
            ccat = fid['categoria'].value_counts().reset_index()
            ccat.columns = ['Categoria','Quantidade']
            fig = px.bar(ccat, x='Categoria', y='Quantidade', text='Quantidade', color='Categoria',
                         color_discrete_sequence=['#BA5934','#CD9B26','#597B55','#DB6A19'])
            fig.update_traces(textposition='outside', textfont=dict(color='#42210B',size=14,weight='bold'))
            fig.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              xaxis=dict(title="<b>Classificação</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B',weight='bold')),
                              yaxis=dict(title="<b>Quantidade</b>",    title_font=dict(color='#42210B'), tickfont=dict(color='#42210B',weight='bold'), gridcolor='rgba(66,33,11,0.15)'))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    with col2:
        st.markdown("### Top 5 Produtos (Receita)")
        if 'coffee_name' in df.columns and 'money' in df.columns:
            t5 = df.groupby('coffee_name')['money'].sum().reset_index()
            t5.columns = ['Produto','Faturamento']
            t5 = t5.sort_values('Faturamento', ascending=False).head(5)
            mx = t5['Faturamento'].max()
            html = '<div class="t5-box">'
            for _, r in t5.iterrows():
                pct = (r['Faturamento']/mx)*100
                val = f"$ {r['Faturamento']:,.2f}".replace(',','X').replace('.',',').replace('X','.')
                html += f'<div class="t5-row"><div class="t5-name" title="{r["Produto"]}">{r["Produto"]}</div><div class="t5-track"><div class="t5-fill" style="width:{pct}%;"></div></div><div class="t5-val">{val}</div></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Faturamento por Produto")
    if 'coffee_name' in df.columns and 'money' in df.columns:
        fp = df.groupby('coffee_name')['money'].sum().reset_index()
        fp.columns = ['Produto','Faturamento']
        fp = fp.sort_values('Faturamento', ascending=False)
        fig2 = px.bar(fp, x='Produto', y='Faturamento', text_auto='.2s', color='Faturamento',
                      color_continuous_scale=['#CD9B26','#DB6A19','#BA5934','#42210B'])
        fig2.update_traces(textposition='outside', textfont=dict(color='#42210B',size=14,weight='bold'))
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), coloraxis_showscale=False,
                           plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           xaxis=dict(title="<b>Produto</b>",              title_font=dict(color='#42210B'), tickfont=dict(color='#42210B',weight='bold')),
                           yaxis=dict(title="<b>Receita Acumulada ($)</b>",title_font=dict(color='#42210B'), tickfont=dict(color='#42210B',weight='bold'), gridcolor='rgba(66,33,11,0.15)'))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

# ═══════════════════════════════════════════════════════════
elif page == "Clientes":
    st.markdown("<p class='subtitle'>Análise de fidelidade, métodos de pagamento e perfil de consumo.</p>", unsafe_allow_html=True)
    df_clientes = df.dropna(subset=['card']).copy()

    if not df_clientes.empty:
        fid2 = df_clientes['card'].value_counts().reset_index()
        fid2.columns = ['card','visitas']
        gasto = df_clientes.groupby('card')['money'].sum().reset_index()
        pc    = pd.merge(fid2, gasto, on='card')

        def cat2(v):
            if v >= 10: return 'VIP (10+)'
            if v >= 5:  return 'Fiel (5-9)'
            if v >= 2:  return 'Recorrente (2-4)'
            return 'Único (1)'
        pc['categoria'] = pc['visitas'].apply(cat2)

        total_c   = pc['card'].nunique()
        total_vip = pc[pc['categoria']=='VIP (10+)'].shape[0]
        tvip      = df_clientes[df_clientes['card'].isin(pc[pc['categoria']=='VIP (10+)']['card'])]['money'].mean()
        tvip      = tvip if pd.notna(tvip) else 0
        pct_c     = (df[df['cash_type']=='card'].shape[0]/len(df))*100 if 'cash_type' in df.columns else 0

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Clientes Únicos (Cartão)", f"{total_c}")
        c2.metric("Pagamentos no Cartão",     f"{pct_c:.1f}%".replace('.',','))
        c3.metric("Total de Clientes VIP",    f"{total_vip}")
        c4.metric("Ticket Médio VIP",         f"$ {tvip:,.2f}".replace(',','X').replace('.',',').replace('X','.'))
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("### Receita por Categoria de Cliente")
            rc = pc.groupby('categoria')['money'].sum().reset_index()
            rc.columns = ['Categoria','Receita Total']
            fig_r = px.pie(rc, values='Receita Total', names='Categoria', hole=0.4,
                           color='Categoria', color_discrete_sequence=['#BA5934','#CD9B26','#597B55','#DB6A19'])
            fig_r.update_traces(textposition='inside', textinfo='percent+label',
                                insidetextfont=dict(color='#FFFFFF',size=14,weight='bold'))
            fig_r.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_r, use_container_width=True, config={'displayModeBar':False})

        with col2:
            st.markdown("### Top 5 Maiores Clientes")
            tc = pc.sort_values('money', ascending=False).head(5).reset_index(drop=True)
            medals = ["🏆 1º","🥈 2º","🥉 3º","🏅 4º","🏅 5º"]
            hc = '<div class="t5-box">'
            mx2 = tc['money'].max()
            for i, r in tc.iterrows():
                pct = (r['money']/mx2)*100
                val = f"$ {r['money']:,.2f}".replace(',','X').replace('.',',').replace('X','.')
                hc += f'<div class="t5-row"><div class="t5-name" title="ID:{r["card"]}">{medals[i]} Maior Comprador</div><div class="t5-track"><div class="t5-fill" style="width:{pct}%;background:#CD9B26;"></div></div><div class="t5-val">{val}</div></div>'
            hc += '</div>'
            st.markdown(hc, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Café Favorito por Categoria de Fidelidade")
        dfc = pd.merge(df_clientes, pc[['card','categoria']], on='card', how='left')
        pref = dfc.groupby(['categoria','coffee_name']).size().reset_index(name='quantidade')
        idx  = pref.groupby(['categoria'])['quantidade'].transform(max) == pref['quantidade']
        tcaf = pref[idx].sort_values('quantidade', ascending=False).drop_duplicates(subset=['categoria'])
        hcaf = '<div class="t5-box">'
        mx3  = tcaf['quantidade'].max()
        for _, r in tcaf.iterrows():
            pct = (r['quantidade']/mx3)*100
            hcaf += f'<div class="t5-row"><div class="t5-name" style="width:20%;color:#DB6A19;">{r["categoria"]}</div><div class="t5-name" style="width:30%;font-weight:700;">{r["coffee_name"]}</div><div class="t5-track"><div class="t5-fill" style="width:{pct}%;background:#597B55;"></div></div><div class="t5-val" style="width:15%;">{r["quantidade"]} un.</div></div>'
        hcaf += '</div>'
        st.markdown(hcaf, unsafe_allow_html=True)
    else:
        st.warning("Não há dados de cartão suficientes para análise.")

# ═══════════════════════════════════════════════════════════
elif page == "Produtos":
    st.markdown("<p class='subtitle'>Desempenho do cardápio: quais cafés estão gerando mais receita e volume.</p>", unsafe_allow_html=True)

    if 'coffee_name' in df.columns and 'money' in df.columns:
        perf = df.groupby('coffee_name').agg(quantidade=('money','count'), faturamento=('money','sum')).reset_index()
        pq   = perf.sort_values('quantidade', ascending=False)
        mais = pq.iloc[0]['coffee_name']  if not pq.empty else "-"
        menos= pq.iloc[-1]['coffee_name'] if not pq.empty else "-"
        pm   = df.drop_duplicates('coffee_name')['money'].mean()

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Itens no Cardápio",   f"{perf['coffee_name'].nunique()}")
        c2.metric("Mais Vendido",        mais)
        c3.metric("Menos Vendido",       menos)
        c4.metric("Preço Médio do Menu", f"$ {pm:,.2f}".replace(',','X').replace('.',',').replace('X','.'))
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### Matriz de Performance de Produtos")
        st.markdown("<span style='color:#9C7A65;font-size:14px;'>Produtos no quadrante superior direito são os campeões (alto volume e alta receita).</span>", unsafe_allow_html=True)
        fig_s = px.scatter(perf, x='quantidade', y='faturamento', size='faturamento',
                           color='faturamento', text='coffee_name', hover_name='coffee_name',
                           color_continuous_scale=['#CD9B26','#DB6A19','#BA5934','#42210B'],
                           labels={'quantidade':'Unidades Vendidas','faturamento':'Receita Total ($)'})
        fig_s.update_traces(textposition='top center', textfont=dict(color='#42210B',size=12,weight='bold'),
                            marker=dict(line=dict(width=1,color='#42210B')))
        fig_s.update_layout(margin=dict(l=0,r=0,t=20,b=0), height=450, coloraxis_showscale=False,
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(title="<b>Volume de Vendas (Unidades)</b>", title_font=dict(color='#42210B',size=14),
                                       tickfont=dict(color='#42210B',weight='bold'), showgrid=True,
                                       gridcolor='rgba(66,33,11,0.1)', zerolinecolor='rgba(66,33,11,0.3)'),
                            yaxis=dict(title="<b>Faturamento Total ($)</b>", title_font=dict(color='#42210B',size=14),
                                       tickfont=dict(color='#42210B',weight='bold'), showgrid=True,
                                       gridcolor='rgba(66,33,11,0.1)', zerolinecolor='rgba(66,33,11,0.3)'))
        st.plotly_chart(fig_s, use_container_width=True, config={'displayModeBar':False})
        st.markdown("<br>", unsafe_allow_html=True)

        def tabela_p(d, mx, cor):
            h = '<div class="t5-box">'
            for _, r in d.iterrows():
                pct = (r['quantidade']/mx)*100
                h += f'<div class="t5-row"><div class="t5-name" style="width:35%;">{r["coffee_name"]}</div><div class="t5-track"><div class="t5-fill" style="width:{pct}%;background:{cor};"></div></div><div class="t5-val" style="width:25%;">{r["quantidade"]} un.</div></div>'
            return h + '</div>'

        t5p = pq.head(5)
        col_top, col_bot = st.columns(2, gap="large")
        with col_top:
            st.markdown("### 🏆 Top 5 (Mais Vendidos)")
            st.markdown(tabela_p(t5p, t5p['quantidade'].max(), '#BA5934'), unsafe_allow_html=True)
        with col_bot:
            st.markdown("### ⚠️ Bottom 5 (Menos Vendidos)")
            b5 = pq.tail(5).sort_values('quantidade', ascending=True)
            st.markdown(tabela_p(b5, t5p['quantidade'].max(), '#A47754'), unsafe_allow_html=True)
    else:
        st.warning("Dados de produtos ou valores não encontrados.")

# ═══════════════════════════════════════════════════════════
elif page == "Vendas":
    st.markdown("<p class='subtitle'>Análise de horários de pico, fluxo de caixa e métodos de pagamento.</p>", unsafe_allow_html=True)

    if 'date' in df.columns:
        df['data_dia']  = pd.to_datetime(df['date']).dt.date
        vpd = df.groupby('data_dia')['money'].sum().mean()
        ppd = df.groupby('data_dia')['money'].count().mean()
    else:
        vpd, ppd = 0, 0

    md  = df['Weekday'].value_counts().idxmax()     if 'Weekday'      in df.columns and not df.empty else "-"
    pic = df['Time_of_Day'].value_counts().idxmax() if 'Time_of_Day'  in df.columns and not df.empty else "-"
    dias_pt   = {'Sun':'Domingo','Mon':'Segunda','Tue':'Terça','Wed':'Quarta','Thu':'Quinta','Fri':'Sexta','Sat':'Sábado'}
    turnos_pt = {'Morning':'Manhã','Afternoon':'Tarde','Evening':'Noite'}

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Média de Receita/Dia",   f"$ {vpd:,.2f}".replace(',','X').replace('.',',').replace('X','.'))
    c2.metric("Média de Pedidos/Dia",   f"{ppd:.0f}")
    c3.metric("Melhor Dia da Semana",   dias_pt.get(md, md))
    c4.metric("Turno de Pico",          turnos_pt.get(pic, pic))
    st.markdown("<br>", unsafe_allow_html=True)

    do = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    dl = ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom']
    col_heat, col_vol = st.columns([2,1], gap="large")

    with col_heat:
        st.markdown("### Mapa de Calor: Ocupação (Dia x Hora)")
        if 'Weekday' in df.columns and 'hour_of_day' in df.columns:
            mapa = pd.crosstab(df['Weekday'], df['hour_of_day']).reindex(do)
            fh   = px.imshow(mapa, labels=dict(x="Hora do Dia",y="Dia da Semana",color="Volume de Pedidos"),
                             x=mapa.columns, y=dl,
                             color_continuous_scale=['#F5EEDC','#CD9B26','#BA5934','#42210B'],
                             aspect="auto", text_auto=True)
            fh.update_xaxes(side="bottom", tickfont=dict(color='#42210B',weight='bold'), title_font=dict(color='#42210B',weight='bold'))
            fh.update_yaxes(tickfont=dict(color='#42210B',weight='bold'), title_font=dict(color='#42210B',weight='bold'))
            fh.update_layout(margin=dict(l=0,r=0,t=10,b=0), plot_bgcolor='rgba(0,0,0,0)',
                             paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
            st.plotly_chart(fh, use_container_width=True, config={'displayModeBar':False})

    with col_vol:
        st.markdown("### Pedidos por Dia")
        if 'Weekday' in df.columns:
            vol = df['Weekday'].value_counts().reindex(do).reset_index()
            vol.columns = ['Dia','Pedidos']
            vol['Dia_PT'] = dl
            fv = px.bar(vol, x='Dia_PT', y='Pedidos', text='Pedidos',
                        labels={'Dia_PT':'Dia da Semana'}, color_discrete_sequence=['#BA5934'])
            fv.update_traces(textposition='outside', textfont=dict(color='#42210B',size=13,weight='bold'))
            fv.update_layout(margin=dict(l=0,r=0,t=10,b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(title="<b>Dia da Semana</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B',weight='bold'), showgrid=False),
                             yaxis=dict(title="<b>Qtd Pedidos</b>",   title_font=dict(color='#42210B'), tickfont=dict(color='#42210B',weight='bold'), gridcolor='rgba(66,33,11,0.15)'))
            st.plotly_chart(fv, use_container_width=True, config={'displayModeBar':False})

    st.markdown("<br><br>", unsafe_allow_html=True)
    col_pie, col_ticket = st.columns([1.5,2], gap="large")

    if 'cash_type' in df.columns and 'money' in df.columns:
        with col_pie:
            st.markdown("### Proporção de Receita por Método de Pagamento")
            rm = df.groupby('cash_type')['money'].sum().reset_index()
            rm['cash_type'] = rm['cash_type'].map({'card':'Cartão','cash':'Dinheiro'})
            fp2 = px.pie(rm, values='money', names='cash_type', hole=0.45,
                         color='cash_type', color_discrete_map={'Cartão':'#CD9B26','Dinheiro':'#597B55'})
            fp2.update_traces(textposition='inside', textinfo='percent+label',
                              insidetextfont=dict(color='#FFFFFF',size=14,weight='bold'))
            fp2.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fp2, use_container_width=True, config={'displayModeBar':False})

        with col_ticket:
            st.markdown("### Análise de Ticket Médio")
            tmc = df[df['cash_type']=='card']['money'].mean()
            tmd = df[df['cash_type']=='cash']['money'].mean()
            if pd.notna(tmc) and pd.notna(tmd) and tmd > 0:
                diff   = tmc - tmd
                perc   = (abs(diff)/tmd)*100
                status = "inferior" if diff < 0 else "superior"
                ins    = f"O gasto no cartão é em média <b>{perc:.1f}% {status}</b> ao gasto em dinheiro."
            else:
                ins = "Dados insuficientes para comparação."

            vc = f"$ {tmc:,.2f}".replace(',','X').replace('.',',').replace('X','.') if pd.notna(tmc) else "$ 0,00"
            vd = f"$ {tmd:,.2f}".replace(',','X').replace('.',',').replace('X','.') if pd.notna(tmd) else "$ 0,00"

            st.markdown(f"""
            <div style="display:flex;gap:20px;margin-top:10px;">
                <div class="t5-box" style="flex:1;border-left:5px solid #CD9B26;text-align:center;padding:30px 20px;">
                    <span style="color:#42210B;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:1px;">💳 Ticket Cartão</span><br>
                    <span style="font-family:'Saira Condensed',sans-serif;font-size:38px;font-weight:700;color:#1A0A04;">{vc}</span>
                </div>
                <div class="t5-box" style="flex:1;border-left:5px solid #597B55;text-align:center;padding:30px 20px;">
                    <span style="color:#42210B;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:1px;">💵 Ticket Dinheiro</span><br>
                    <span style="font-family:'Saira Condensed',sans-serif;font-size:38px;font-weight:700;color:#1A0A04;">{vd}</span>
                </div>
            </div>
            <div style="background:#F5EEDC;border:1px dashed #D4C4B0;border-radius:6px;padding:15px 20px;margin-top:20px;color:#42210B;font-size:15px;">
                💡 <b>Insight:</b> {ins}
            </div>
            """, unsafe_allow_html=True)