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
        st.error(f"⚠️ Arquivo 'Coffe_sales.xlsx' não encontrado no caminho: {file_path}")
        return pd.DataFrame({'money': [0], 'coffee_name': ['-'], 'Weekday': ['-'], 'card': [None]})

df = load_data()

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Visão Geral"

PAGES = ["Visão Geral", "Clientes", "Produtos", "Vendas"]

# ── CSS Base ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&family=Saira+Condensed:wght@400;600;700&display=swap');

:root {
    --bg:         #F5EEDC;
    --surface:    #FFFFFF;
    --sidebar:    #412314;
    --sidebar-dk: #2E1710;
    --accent:     #BA5934; /* Terracota da Paleta */
    --gold:       #CD9B26; /* Mostarda da Paleta */
    --orange-lt:  #DB6A19; /* Laranja da Paleta */
    --text:       #1A0A04;
    --text-soft:  #42210B; /* Marrom Escuro da Paleta */
    --border:     #D4C4B0;
    --nav-text:   #E8D8C4;
    --nav-muted:  #9C7A65;
}

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

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] svg { fill: var(--orange-lt) !important; stroke: var(--orange-lt) !important; }
[data-testid="collapsedControl"] svg { fill: var(--text) !important; stroke: none !important; }

.sb-header {
    background: var(--sidebar-dk); padding: 20px 18px 16px;
    border-bottom: 1px solid rgba(244,164,96,0.2); position: relative; margin-bottom: 4px;
}
.sb-header::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--orange-lt);
}
.sb-brand { display: flex; align-items: center; gap: 12px; }
.sb-icon-box {
    width: 38px; height: 38px; background: var(--accent); border-radius: 9px;
    display: flex; align-items: center; justify-content: center; font-size: 19px; flex-shrink: 0;
}
.sb-name { font-family: 'Saira Condensed', sans-serif; font-size: 20px; font-weight: 700; color: var(--orange-lt); display: block; line-height: 1; }
.sb-tagline { font-family: 'Roboto Condensed', sans-serif; font-size: 10px; color: var(--nav-muted); margin-top: 2px; letter-spacing: 0.07em; text-transform: uppercase; display: block; }
.sb-nav-label { font-family: 'Roboto Condensed', sans-serif; font-size: 10px; font-weight: 700; color: var(--nav-muted); letter-spacing: 0.14em; text-transform: uppercase; padding: 18px 20px 6px; }
.sb-footer { padding: 14px 20px 18px; border-top: 1px solid rgba(244,164,96,0.12); }
.sb-footer-row { font-family: 'Roboto Condensed', sans-serif; font-size: 11px; color: var(--nav-muted); display: flex; align-items: center; gap: 7px; }
.sb-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; display: inline-block; }

/* Radio Nav */
[data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] { display: none !important; }
[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] { display: flex !important; flex-direction: column !important; gap: 0 !important; padding: 0 10px !important; }
[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center !important; width: 100% !important; padding: 11px 14px !important;
    margin: 2px 0 !important; border-radius: 8px !important; cursor: pointer !important;
    font-family: 'Roboto Condensed', sans-serif !important; font-size: 15px !important; font-weight: 400 !important;
    color: var(--nav-text) !important; background: transparent !important; border-left: 3px solid transparent !important;
    box-sizing: border-box !important; transition: background 0.15s, color 0.15s, border-color 0.15s !important;
}
[data-testid="stSidebar"] .stRadio label > div:first-child { display: none !important; }
[data-testid="stSidebar"] .stRadio label:hover { background: rgba(244,164,96,0.1) !important; color: var(--gold) !important; border-color: rgba(221,168,83,0.3) !important; }
[data-testid="stSidebar"] .stRadio label[aria-checked="true"] { background: rgba(182,84,49,0.28) !important; color: var(--orange-lt) !important; font-weight: 700 !important; border-color: var(--accent) !important; }

/* KPI Cards */
[data-testid="stMetric"] {
    background-color: var(--surface) !important; border-radius: 6px !important; padding: 18px 22px !important;
    border-left: 5px solid var(--accent) !important; border-top: 1px solid var(--border) !important;
    border-right: 1px solid var(--border) !important; border-bottom: 1px solid var(--border) !important;
}
[data-testid="stMetricLabel"] { font-family: 'Roboto Condensed', sans-serif !important; font-size: 12px !important; font-weight: 700 !important; color: var(--text-soft) !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { font-family: 'Saira Condensed', sans-serif !important; font-size: 34px !important; font-weight: 700 !important; color: var(--text) !important; }

/* Page Header */
.page-title { font-family: 'Saira Condensed', sans-serif; font-size: 32px; font-weight: 700; color: #1A0A04; margin: 0 0 4px; }
.page-bar { width: 48px; height: 4px; background: var(--accent); border-radius: 2px; margin-bottom: 22px; }
.subtitle { font-family: 'Roboto Condensed', sans-serif; font-size: 15px; color: var(--text-soft); margin-bottom: 22px; }

/* Top 5 Table CSS (Ajustado para Valores em R$) */
.t5-box { background: #FFFFFF; border: 1px solid #D4C4B0; border-radius: 6px; padding: 20px; }
.t5-row { display: flex; align-items: center; margin-bottom: 15px; }
.t5-row:last-child { margin-bottom: 0; }
.t5-name { width: 32%; font-weight: 700; font-size: 14px; color: #1A0A04; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.t5-track { flex: 1; height: 8px; background: #F5EEDC; border-radius: 4px; margin: 0 12px; overflow: hidden; }
.t5-fill { height: 100%; background: #BA5934; border-radius: 4px; }
.t5-val { width: 30%; text-align: right; font-weight: 700; font-size: 14px; color: #42210B; white-space: nowrap; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar UI ────────────────────────────────────────────────────────────────
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

    page = st.radio("nav", options=PAGES, index=PAGES.index(st.session_state.page))
    st.session_state.page = page

    st.markdown("""
    <div class="sb-footer">
        <div class="sb-footer-row"><span class="sb-dot"></span>Março 2024</div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown("<div class='page-title'>Painel Gerencial — Março 2024</div>", unsafe_allow_html=True)
st.markdown("<div class='page-bar'></div>", unsafe_allow_html=True)

if page == "Visão Geral":
    st.markdown("<p class='subtitle'>Acompanhamento macro do desempenho da cafeteria.</p>", unsafe_allow_html=True)
    
    # 1. KPIs
    fat_total = df['money'].sum()
    tm = df['money'].mean()
    mv = df['coffee_name'].value_counts().idxmax() if 'coffee_name' in df.columns and not df.empty else "-"
    dmf = df['Weekday'].value_counts().idxmin() if 'Weekday' in df.columns and not df.empty else "-"
    dias_pt = {'Sun': 'Domingo', 'Mon': 'Segunda', 'Tue': 'Terça', 'Wed': 'Quarta', 'Thu': 'Quinta', 'Fri': 'Sexta', 'Sat': 'Sábado'}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faturamento Total", f"R$ {fat_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    c2.metric("Ticket Médio", f"R$ {tm:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    c3.metric("Mais Vendido", mv)
    c4.metric("Dia Mais Fraco", dias_pt.get(dmf, dmf))
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Gráficos Superiores
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("### Perfil de Clientes (Fidelidade)")
        if 'card' in df.columns:
            fid = df['card'].dropna().value_counts().reset_index()
            fid.columns = ['card', 'visitas']
            
            def cat_fid(v):
                if v >= 10: return 'VIP (10+)'
                if v >= 5: return 'Fiel (5-9)'
                if v >= 2: return 'Recorrente (2-4)'
                return 'Único (1)'
                
            fid['categoria'] = fid['visitas'].apply(cat_fid)
            ccat = fid['categoria'].value_counts().reset_index()
            ccat.columns = ['Categoria', 'Quantidade']
            
            fig = px.bar(ccat, x='Categoria', y='Quantidade', text='Quantidade', color='Categoria',
                         color_discrete_sequence=['#BA5934', '#CD9B26', '#597B55', '#DB6A19'])
            
            fig.update_traces(textposition='outside', textfont=dict(color='#42210B', size=14, weight='bold'))
            fig.update_layout(
                showlegend=False, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="<b>Classificação</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B', weight='bold')),
                yaxis=dict(title="<b>Quantidade</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B', weight='bold'), gridcolor='rgba(66, 33, 11, 0.15)')
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("### Top 5 Produtos (Receita)")
        if 'coffee_name' in df.columns and 'money' in df.columns:
            
            # SOMA O FATURAMENTO EM VEZ DE CONTAR UNIDADES
            t5 = df.groupby('coffee_name')['money'].sum().reset_index()
            t5.columns = ['Produto', 'Faturamento']
            
            # Ordena do maior para o menor e pega os 5 primeiros
            t5 = t5.sort_values('Faturamento', ascending=False).head(5)
            m_faturamento = t5['Faturamento'].max()
            
            # Montagem segura do HTML
            html_content = '<div class="t5-box">'
            for _, r in t5.iterrows():
                p = (r['Faturamento'] / m_faturamento) * 100
                
                # Formata o valor para o padrão moeda brasileiro (ex: R$ 1.234,56)
                val_formatado = f"R$ {r['Faturamento']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                
                html_content += f'<div class="t5-row"><div class="t5-name" title="{r["Produto"]}">{r["Produto"]}</div><div class="t5-track"><div class="t5-fill" style="width:{p}%;"></div></div><div class="t5-val">{val_formatado}</div></div>'
            html_content += '</div>'
            
            st.markdown(html_content, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Gráfico Inferior
    st.markdown("### Faturamento por Produto")
    if 'coffee_name' in df.columns and 'money' in df.columns:
        fp = df.groupby('coffee_name')['money'].sum().reset_index()
        fp.columns = ['Produto', 'Faturamento']
        fp = fp.sort_values('Faturamento', ascending=False)
        
        fig2 = px.bar(fp, x='Produto', y='Faturamento', text_auto='.2s', color='Faturamento',
                      color_continuous_scale=['#CD9B26', '#DB6A19', '#BA5934', '#42210B'])
        
        fig2.update_traces(textposition='outside', textfont=dict(color='#42210B', size=14, weight='bold'))
        fig2.update_layout(
            margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="<b>Produto</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B', weight='bold')),
            yaxis=dict(title="<b>Receita Acumulada (R$)</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B', weight='bold'), gridcolor='rgba(66, 33, 11, 0.15)')
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

elif page == "Clientes":
    st.markdown("<p class='subtitle'>Análise de fidelidade, métodos de pagamento e perfil de consumo.</p>", unsafe_allow_html=True)
    
    # ── 1. Preparação de Dados de Clientes ──
    df_clientes = df.dropna(subset=['card']).copy()
    
    if not df_clientes.empty:
        # Frequência (visitas) e Gasto por cliente
        fidelidade = df_clientes['card'].value_counts().reset_index()
        fidelidade.columns = ['card', 'visitas']
        
        gasto = df_clientes.groupby('card')['money'].sum().reset_index()
        perfil_clientes = pd.merge(fidelidade, gasto, on='card')
        
        def categorizar_fidelidade(visitas):
            if visitas >= 10: return 'VIP (10+)'
            if visitas >= 5: return 'Fiel (5-9)'
            if visitas >= 2: return 'Recorrente (2-4)'
            return 'Único (1)'
            
        perfil_clientes['categoria'] = perfil_clientes['visitas'].apply(categorizar_fidelidade)
        
        # ── 2. Cálculos dos KPIs ──
        total_clientes = perfil_clientes['card'].nunique()
        total_vips = perfil_clientes[perfil_clientes['categoria'] == 'VIP (10+)'].shape[0]
        
        ticket_vip = df_clientes[df_clientes['card'].isin(perfil_clientes[perfil_clientes['categoria'] == 'VIP (10+)']['card'])]['money'].mean()
        ticket_vip = ticket_vip if pd.notna(ticket_vip) else 0
        
        pct_cartao = (df[df['cash_type'] == 'card'].shape[0] / len(df)) * 100 if 'cash_type' in df.columns else 0
        
        # ── 3. Renderizando os KPIs ──
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Clientes Únicos (Cartão)", f"{total_clientes}")
        c2.metric("Pagamentos no Cartão", f"{pct_cartao:.1f}%".replace('.', ','))
        c3.metric("Total de Clientes VIP", f"{total_vips}")
        c4.metric("Ticket Médio VIP", f"R$ {ticket_vip:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 4. Gráficos da Primeira Linha ──
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### Receita por Categoria de Cliente")
            receita_cat = perfil_clientes.groupby('categoria')['money'].sum().reset_index()
            receita_cat.columns = ['Categoria', 'Receita Total']
            
            fig_rec = px.pie(
                receita_cat, 
                values='Receita Total', 
                names='Categoria',
                hole=0.4, # Gráfico de rosca (Donut)
                color='Categoria',
                color_discrete_sequence=['#BA5934', '#CD9B26', '#597B55', '#DB6A19']
            )
            fig_rec.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                insidetextfont=dict(color='#FFFFFF', size=14, weight='bold')
            )
            fig_rec.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_rec, use_container_width=True, config={'displayModeBar': False})
            
        with col2:
            st.markdown("### Top 5 Maiores Clientes")
            top_clientes = perfil_clientes.sort_values('money', ascending=False).head(5).reset_index(drop=True)
            
            html_clientes = '<div class="t5-box">'
            max_gasto = top_clientes['money'].max()
            
            for i, r in top_clientes.iterrows():
                pos = i + 1
                
                # Traduzindo os IDs estranhos para um ranking executivo (com emojis)
                if pos == 1:
                    nome_cliente = "🏆 1º Maior Comprador"
                elif pos == 2:
                    nome_cliente = "🥈 2º Maior Comprador"
                elif pos == 3:
                    nome_cliente = "🥉 3º Maior Comprador"
                else:
                    nome_cliente = f"🏅 {pos}º Maior Comprador"
                    
                p = (r['money'] / max_gasto) * 100
                val_formatado = f"R$ {r['money']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                
                # Dica: o "title" adiciona um tooltip. Se o usuário passar o mouse por cima de "1º Maior Comprador", aparece o ID real da pessoa.
                html_clientes += f'<div class="t5-row"><div class="t5-name" title="ID: {r["card"]}">{nome_cliente}</div><div class="t5-track"><div class="t5-fill" style="width:{p}%; background-color:#CD9B26;"></div></div><div class="t5-val">{val_formatado}</div></div>'
            html_clientes += '</div>'
            
            st.markdown(html_clientes, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 5. Café Favorito por Categoria (Com Visual Premium) ──
        st.markdown("### Café Favorito por Categoria de Fidelidade")
        
        # Junta os dados de perfil com a tabela original
        df_completo = pd.merge(df_clientes, perfil_clientes[['card', 'categoria']], on='card', how='left')
        preferencias = df_completo.groupby(['categoria', 'coffee_name']).size().reset_index(name='quantidade')
        
        # Pega o máximo de vendas dentro de cada categoria
        idx = preferencias.groupby(['categoria'])['quantidade'].transform(max) == preferencias['quantidade']
        top_cafes = preferencias[idx].sort_values(by='quantidade', ascending=False).drop_duplicates(subset=['categoria'])
        
        html_cafes = '<div class="t5-box">'
        max_unid = top_cafes['quantidade'].max()
        
        for _, r in top_cafes.iterrows():
            p = (r['quantidade'] / max_unid) * 100
            
            # Usamos o estilo t5-row flexível para caber: (Categoria) + (Nome do Café) + (Barra) + (Valor)
            html_cafes += f'<div class="t5-row"><div class="t5-name" style="width: 20%; color: #DB6A19;">{r["categoria"]}</div><div class="t5-name" style="width: 30%; font-weight: bold;">{r["coffee_name"]}</div><div class="t5-track"><div class="t5-fill" style="width:{p}%; background-color:#597B55;"></div></div><div class="t5-val" style="width: 15%;">{r["quantidade"]} un.</div></div>'
        html_cafes += '</div>'
        
        st.markdown(html_cafes, unsafe_allow_html=True)

    else:
        st.warning("Não há dados de cartão (clientes) suficientes para análise.")
elif page == "Produtos":
    st.markdown("<p class='subtitle'>Desempenho do cardápio: quais cafés estão gerando mais receita e volume.</p>", unsafe_allow_html=True)
    
    # ── 1. Preparação de Dados ──
    if 'coffee_name' in df.columns and 'money' in df.columns:
        # Agrupar por produto: quantidade de vendas e faturamento total
        performance = df.groupby('coffee_name').agg(
            quantidade=('money', 'count'),
            faturamento=('money', 'sum')
        ).reset_index()
        
        # ── 2. Cálculos dos KPIs ──
        total_produtos = performance['coffee_name'].nunique()
        
        # Ordenar por quantidade para achar o mais e menos vendido
        perf_qtd = performance.sort_values('quantidade', ascending=False)
        mais_vendido = perf_qtd.iloc[0]['coffee_name'] if not perf_qtd.empty else "-"
        menos_vendido = perf_qtd.iloc[-1]['coffee_name'] if not perf_qtd.empty else "-"
        
        # Preço médio do cardápio (Ticket Médio por Produto, não por cliente)
        preco_medio_menu = df.drop_duplicates('coffee_name')['money'].mean()
        
        # ── 3. Renderizando KPIs ──
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Itens no Cardápio", f"{total_produtos}")
        c2.metric("Mais Vendido", mais_vendido)
        c3.metric("Menos Vendido", menos_vendido)
        c4.metric("Preço Médio do Menu", f"R$ {preco_medio_menu:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 4. Matriz de Performance (Scatter Plot) ──
        st.markdown("### Matriz de Performance de Produtos")
        st.markdown("<span style='color: #9C7A65; font-size: 14px;'>Produtos no quadrante superior direito são os campeões (alto volume e alta receita).</span>", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            performance, 
            x='quantidade', 
            y='faturamento',
            size='faturamento', # Bolhas maiores para quem dá mais dinheiro
            color='faturamento', # Cor muda conforme o faturamento
            text='coffee_name',
            hover_name='coffee_name',
            color_continuous_scale=['#CD9B26', '#DB6A19', '#BA5934', '#42210B'],
            labels={'quantidade': 'Unidades Vendidas', 'faturamento': 'Receita Total (R$)'}
        )
        
        # Formatação do texto para ficar fora da bolha e fácil de ler
        fig_scatter.update_traces(
            textposition='top center',
            textfont=dict(color='#42210B', size=12, weight='bold'),
            marker=dict(line=dict(width=1, color='#42210B'))
        )
        
        fig_scatter.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=450, # Deixei o gráfico um pouco mais alto para as bolhas espalharem bem
            coloraxis_showscale=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title="<b>Volume de Vendas (Unidades)</b>",
                title_font=dict(color='#42210B', size=14),
                tickfont=dict(color='#42210B', weight='bold'),
                showgrid=True, gridcolor='rgba(66, 33, 11, 0.1)', zerolinecolor='rgba(66, 33, 11, 0.3)'
            ),
            yaxis=dict(
                title="<b>Faturamento Total (R$)</b>",
                title_font=dict(color='#42210B', size=14),
                tickfont=dict(color='#42210B', weight='bold'),
                showgrid=True, gridcolor='rgba(66, 33, 11, 0.1)', zerolinecolor='rgba(66, 33, 11, 0.3)'
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 5. Top 5 e Bottom 5 (O que manter e o que remover do cardápio) ──
        col_top, col_bot = st.columns(2, gap="large")
        
        # Reutilizamos a lógica de renderizar o HTML da tabela
        def gerar_tabela_produtos(df_produtos, max_val, cor_barra):
            html = '<div class="t5-box">'
            for _, r in df_produtos.iterrows():
                p = (r['quantidade'] / max_val) * 100
                html += f'<div class="t5-row"><div class="t5-name" style="width: 35%;">{r["coffee_name"]}</div><div class="t5-track"><div class="t5-fill" style="width:{p}%; background-color:{cor_barra};"></div></div><div class="t5-val" style="width: 25%;">{r["quantidade"]} un.</div></div>'
            html += '</div>'
            return html

        with col_top:
            st.markdown("### 🏆 Top 5 (Mais Vendidos)")
            top5 = perf_qtd.head(5)
            # Mostarda/Terracota para os melhores
            st.markdown(gerar_tabela_produtos(top5, top5['quantidade'].max(), '#BA5934'), unsafe_allow_html=True)

        with col_bot:
            st.markdown("### ⚠️ Bottom 5 (Menos Vendidos)")
            bot5 = perf_qtd.tail(5).sort_values('quantidade', ascending=True)
            # Marrom Claro / Muted para os piores (pra não chamar tanta atenção)
            st.markdown(gerar_tabela_produtos(bot5, top5['quantidade'].max(), '#A47754'), unsafe_allow_html=True)

    else:
        st.warning("Dados de produtos ou valores não encontrados no dataset.")
elif page == "Vendas":
    st.markdown("<p class='subtitle'>Análise de horários de pico, fluxo de caixa e métodos de pagamento.</p>", unsafe_allow_html=True)
    
    # ── 1. Preparação de Dados ──
    # Extrair a data pura para calcular médias diárias
    if 'date' in df.columns:
        df['data_dia'] = pd.to_datetime(df['date']).dt.date
        vendas_por_dia = df.groupby('data_dia')['money'].sum().mean()
        pedidos_por_dia = df.groupby('data_dia')['money'].count().mean()
    else:
        vendas_por_dia, pedidos_por_dia = 0, 0
        
    melhor_dia = df['Weekday'].value_counts().idxmax() if 'Weekday' in df.columns and not df.empty else "-"
    pico = df['Time_of_Day'].value_counts().idxmax() if 'Time_of_Day' in df.columns and not df.empty else "-"
    
    dias_pt = {'Sun': 'Domingo', 'Mon': 'Segunda', 'Tue': 'Terça', 'Wed': 'Quarta', 'Thu': 'Quinta', 'Fri': 'Sexta', 'Sat': 'Sábado'}
    turnos_pt = {'Morning': 'Manhã', 'Afternoon': 'Tarde', 'Evening': 'Noite'}

    # ── 2. Renderizando KPIs Operacionais ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Média de Receita/Dia", f"R$ {vendas_por_dia:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    c2.metric("Média de Pedidos/Dia", f"{pedidos_por_dia:.0f}")
    c3.metric("Melhor Dia da Semana", dias_pt.get(melhor_dia, melhor_dia))
    c4.metric("Turno de Pico", turnos_pt.get(pico, pico))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 3. Heatmap e Volume por Dia ──
    col_heat, col_vol = st.columns([2, 1], gap="large")
    
    dias_ordem = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dias_labels = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    
    with col_heat:
        st.markdown("### Mapa de Calor: Ocupação (Dia x Hora)")
        if 'Weekday' in df.columns and 'hour_of_day' in df.columns:
            # Matriz cruzada (Crosstab)
            mapa_vendas = pd.crosstab(df['Weekday'], df['hour_of_day']).reindex(dias_ordem)
            
            # Gráfico Heatmap Plotly
            fig_heat = px.imshow(
                mapa_vendas, 
                labels=dict(x="Hora do Dia", y="Dia da Semana", color="Volume de Pedidos"),
                x=mapa_vendas.columns,
                y=dias_labels,
                color_continuous_scale=['#F5EEDC', '#CD9B26', '#BA5934', '#42210B'], # Paleta Bege -> Mostarda -> Terracota -> Marrom
                aspect="auto",
                text_auto=True
            )
            fig_heat.update_xaxes(side="bottom", tickfont=dict(color='#42210B', weight='bold'), title_font=dict(color='#42210B', weight='bold'))
            fig_heat.update_yaxes(tickfont=dict(color='#42210B', weight='bold'), title_font=dict(color='#42210B', weight='bold'))
            fig_heat.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})

    with col_vol:
        st.markdown("### Pedidos por Dia")
        if 'Weekday' in df.columns:
            vol_dia = df['Weekday'].value_counts().reindex(dias_ordem).reset_index()
            vol_dia.columns = ['Dia', 'Pedidos']
            vol_dia['Dia_PT'] = dias_labels
            
            fig_vol = px.bar(
                vol_dia, x='Dia_PT', y='Pedidos', text='Pedidos',
                labels={'Dia_PT': 'Dia da Semana'},
                color_discrete_sequence=['#BA5934'] # Terracota
            )
            fig_vol.update_traces(textposition='outside', textfont=dict(color='#42210B', size=13, weight='bold'))
            fig_vol.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="<b>Dia da Semana</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B', weight='bold'), showgrid=False),
                yaxis=dict(title="<b>Qtd Pedidos</b>", title_font=dict(color='#42210B'), tickfont=dict(color='#42210B', weight='bold'), gridcolor='rgba(66, 33, 11, 0.15)')
            )
            st.plotly_chart(fig_vol, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── 4. Análise de Pagamentos (Dinheiro vs Cartão) ──
    col_pie, col_ticket = st.columns([1.5, 2], gap="large")
    
    if 'cash_type' in df.columns and 'money' in df.columns:
        with col_pie:
            st.markdown("### Proporção de Receita por Método")
            receita_metodo = df.groupby('cash_type')['money'].sum().reset_index()
            # Renomeando para ficar bonito no gráfico
            receita_metodo['cash_type'] = receita_metodo['cash_type'].map({'card': 'Cartão', 'cash': 'Dinheiro'})
            
            fig_pay = px.pie(
                receita_metodo, 
                values='money', 
                names='cash_type',
                hole=0.45,
                color='cash_type',
                # Cartão = Mostarda, Dinheiro = Verde Floresta
                color_discrete_map={'Cartão': '#CD9B26', 'Dinheiro': '#597B55'} 
            )
            fig_pay.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                insidetextfont=dict(color='#FFFFFF', size=14, weight='bold')
            )
            fig_pay.update_layout(
                showlegend=False, margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pay, use_container_width=True, config={'displayModeBar': False})

        with col_ticket:
            st.markdown("### Análise de Ticket Médio")
            
            tm_cartao = df[df['cash_type'] == 'card']['money'].mean()
            tm_dinheiro = df[df['cash_type'] == 'cash']['money'].mean()
            
            # Lógica volátil da sua EDA
            if pd.notna(tm_cartao) and pd.notna(tm_dinheiro) and tm_dinheiro > 0:
                diff = tm_cartao - tm_dinheiro
                perc = (abs(diff) / tm_dinheiro) * 100
                status = "inferior" if diff < 0 else "superior"
                insight_text = f"O gasto no cartão é em média <b>{perc:.1f}% {status}</b> ao gasto em dinheiro."
            else:
                insight_text = "Dados insuficientes para comparação."

            # Desenhando duas caixas grandes de Ticket Médio lado a lado usando CSS do Top 5 adaptado
            val_c = f"R$ {tm_cartao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notna(tm_cartao) else "R$ 0,00"
            val_d = f"R$ {tm_dinheiro:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notna(tm_dinheiro) else "R$ 0,00"
            
            html_tickets = f"""
            <div style="display: flex; gap: 20px; margin-top: 10px;">
                <div class="t5-box" style="flex: 1; border-left: 5px solid #CD9B26; text-align: center; padding: 30px 20px;">
                    <span style="color: #42210B; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">💳 Ticket Cartão</span><br>
                    <span style="font-family: 'Saira Condensed', sans-serif; font-size: 38px; font-weight: 700; color: #1A0A04;">{val_c}</span>
                </div>
                <div class="t5-box" style="flex: 1; border-left: 5px solid #597B55; text-align: center; padding: 30px 20px;">
                    <span style="color: #42210B; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">💵 Ticket Dinheiro</span><br>
                    <span style="font-family: 'Saira Condensed', sans-serif; font-size: 38px; font-weight: 700; color: #1A0A04;">{val_d}</span>
                </div>
            </div>
            <div style="background-color: #F5EEDC; border: 1px dashed #D4C4B0; border-radius: 6px; padding: 15px 20px; margin-top: 20px; color: #42210B; font-size: 15px;">
                💡 <b>Insight:</b> {insight_text}
            </div>
            """
            st.markdown(html_tickets, unsafe_allow_html=True)