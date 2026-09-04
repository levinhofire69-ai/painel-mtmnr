import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# 1. Configuração da Página para Telão / Projetor
st.set_page_config(
    page_title="Central MTMNR - Ao Vivo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização CSS Cyberpunk / Holográfica com Boas-Vindas em Destaque
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap');

    .stApp {
        background: radial-gradient(ellipse at bottom, #0d1b2a 0%, #050811 100%);
        color: #e0e6ed;
        font-family: 'Share Tech Mono', monospace;
    }
    
    footer { visibility: hidden; }

    /* Banner Gigante de Boas-Vindas */
    .welcome-banner {
        background: linear-gradient(135deg, rgba(0,229,255,0.1) 0%, rgba(121,40,202,0.25) 50%, rgba(255,0,127,0.1) 100%);
        border: 2px solid rgba(0, 229, 255, 0.5);
        border-radius: 18px;
        padding: 16px 24px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 0 35px rgba(0, 229, 255, 0.25), inset 0 0 20px rgba(121, 40, 202, 0.2);
        animation: bannerGlow 4s infinite alternate;
    }

    .welcome-subtitle {
        font-family: 'Orbitron', sans-serif;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 6px;
        color: #00ff66;
        text-transform: uppercase;
        margin-bottom: 6px;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.6);
    }

    .welcome-main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #ffffff 0%, #00e5ff 40%, #ff007f 80%, #ffffff 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 229, 255, 0.6);
        animation: textShimmer 5s linear infinite;
        margin-bottom: 6px;
    }

    .welcome-badge-line {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        font-size: 13px;
        color: #8da4c4;
        letter-spacing: 3px;
    }

    .bot-head {
        font-size: 36px;
        display: inline-block;
        animation: botPulse 2s infinite alternate, botBounce 3s ease-in-out infinite;
    }

    /* Cartões KPI */
    .kpi-card {
        background: rgba(13, 27, 42, 0.7);
        border: 1px solid #00e5ff;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.25), inset 0 0 10px rgba(0, 229, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .kpi-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 38px;
        font-weight: 900;
        color: #00e5ff;
        text-shadow: 0 0 10px #00e5ff;
    }

    .kpi-label {
        font-size: 11px;
        color: #8da4c4;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
    }

    /* Ticker Terminal */
    .terminal-ticker {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid #00ff66;
        border-radius: 8px;
        padding: 8px 15px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.2);
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 13px;
        color: #00ff66;
    }

    .ticker-content {
        white-space: nowrap;
        overflow: hidden;
        width: 100%;
    }

    .ticker-text {
        display: inline-block;
        animation: marquee 25s linear infinite;
    }

    /* Grid de Escolas */
    .school-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 14px;
        background: rgba(0,0,0,0.4);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(0, 229, 255, 0.3);
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.1);
    }

    .school-card {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(121, 40, 202, 0.18) 100%);
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 10px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.1);
    }

    .school-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .school-city {
        font-size: 11px;
        color: #00e5ff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .school-status {
        font-size: 10px;
        color: #00ff66;
        display: flex;
        align-items: center;
        gap: 5px;
        font-weight: bold;
    }

    .wordcloud-box {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 0, 127, 0.4);
        border-radius: 12px;
        padding: 15px;
        min-height: 240px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.2);
    }

    .tag-item {
        font-family: 'Orbitron', sans-serif;
        padding: 6px 12px;
        border-radius: 16px;
        animation: floatTag 3s ease-in-out infinite alternate;
    }

    @keyframes bannerGlow {
        from { border-color: rgba(0, 229, 255, 0.4); box-shadow: 0 0 25px rgba(0, 229, 255, 0.2); }
        to { border-color: rgba(255, 0, 127, 0.6); box-shadow: 0 0 35px rgba(255, 0, 127, 0.35); }
    }

    @keyframes textShimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    @keyframes botPulse {
        from { filter: drop-shadow(0 0 5px #00e5ff); }
        to { filter: drop-shadow(0 0 20px #ff007f); }
    }

    @keyframes botBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }

    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    @keyframes floatTag {
        0% { transform: translateY(0px) scale(0.98); }
        100% { transform: translateY(-5px) scale(1.02); }
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# MENU LATERAL - CONTROLE DE CONTINGÊNCIA & TELA CHEIA
# =====================================================================
with st.sidebar:
    st.header("⚙️ Controle do Painel")
    if st.button("🖥️ Maximizar Tela Cheia"):
        components.html("""
            <script>
                var elem = window.parent.document.documentElement;
                if (elem.requestFullscreen) { elem.requestFullscreen(); }
                else if (elem.webkitRequestFullscreen) { elem.webkitRequestFullscreen(); }
                else if (elem.msRequestFullscreen) { elem.msRequestFullscreen(); }
            </script>
        """, height=0)
        
    st.markdown("---")
    st.write("**Modo Offline (Contingência):**")
    fonte_cred_input = st.text_input("Fonte - Credenciamento:", value="1fG5etsR3P1sGbwoyLHIch0R1Pz_zXH0lhgeU4kVv7xk")
    fonte_votos_input = st.text_input("Fonte - Votação:", value="1xUGYchBCpcOMLMcZvOXPLIKj1PDjwdBF03XJ4uQ5_wM")

# =====================================================================
# CARREGAMENTO INTELIGENTE COM BACKUP AUTOMÁTICO
# =====================================================================
@st.cache_data(ttl=4)
def carregar_dados_seguro(fonte, arquivo_backup):
    try:
        if len(fonte) == 44 and " " not in fonte and "." not in fonte:
            url = f"https://docs.google.com/spreadsheets/d/{fonte}/export?format=csv"
            df = pd.read_csv(url)
            df.to_csv(arquivo_backup, index=False)
            return df
        else:
            return pd.read_csv(fonte)
    except Exception:
        return pd.read_csv(arquivo_backup)

# =====================================================================
# BLOCO INTELIGENTE COM ATUALIZAÇÃO AUTOMÁTICA EM SEGUNDO PLANO (SEM PISCAR)
# =====================================================================
@st.fragment(run_every=4)
def painel_ao_vivo():
    df_cred = carregar_dados_seguro(fonte_cred_input, "dados_credenciamento.csv")
    df_vote = carregar_dados_seguro(fonte_votos_input, "dados_votacao.csv")

    # Higienização de Dados (Pandas)
    col_cidade = [c for c in df_cred.columns if "cidade" in c.lower() or "municipio" in c.lower()]
    col_escola = [c for c in df_cred.columns if "escola" in c.lower() or "institui" in c.lower()]

    if not df_cred.empty and col_cidade:
        df_cred['Cidade_Clean'] = df_cred[col_cidade[0]].astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip().str.upper()
        total_participantes = len(df_cred)
        total_municipios = df_cred['Cidade_Clean'].nunique()
    else:
        total_participantes = 0
        total_municipios = 0

    if not df_cred.empty and col_escola:
        df_cred['Escola_Clean'] = df_cred[col_escola[0]].astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip().str.upper()
        df_escolas_validas = df_cred[~df_cred['Escola_Clean'].isin(['', 'NAN', 'NAO INFORMADO', 'NONE', '-'])]
        total_escolas = df_escolas_validas['Escola_Clean'].nunique()
    else:
        total_escolas = 0
        df_escolas_validas = pd.DataFrame()

    if not df_vote.empty and "Nota_Geral" in df_vote.columns:
        total_votos = len(df_vote)
        media_nota = pd.to_numeric(df_vote['Nota_Geral'], errors='coerce').mean()
        if pd.isna(media_nota):
            media_nota = 5.0
    else:
        total_votos = 0
        media_nota = 5.0

    # Interface do Telão
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-subtitle">✨ SEJA BEM-VINDO(A) À ✨</div>
        <div style="display: flex; align-items: center; justify-content: center; gap: 18px;">
            <span class="bot-head">🤖</span>
            <div class="welcome-main-title">1ª Regional Mato Grosso da Mostra Nacional de Robótica (MTMNR)</div>
            <span class="bot-head">⚡</span>
        </div>
        <div class="welcome-badge-line">
            <span>📍 UNIVERSIDADE FEDERAL DE RONDONÓPOLIS (UFR)</span>
            <span>•</span>
            <span style="color: #00ff66;">● MONITORAMENTO AO VIVO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_participantes}</div><div class="kpi-label">Público Conectado</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_escolas}</div><div class="kpi-label">Escolas / Instituições</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_municipios}</div><div class="kpi-label">Polos Regionais (MT)</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{media_nota:.1f} ★</div><div class="kpi-label">Avaliação Geral</div></div>', unsafe_allow_html=True)

    st.write("")

    if not df_cred.empty and "Nome Completo" in df_cred.columns:
        ultimos = df_cred.tail(8)
        feed_msg = " /// ".join([f"⚡ [CHECK-IN] {row['Nome Completo']} ➔ {row.get(col_escola[0] if col_escola else 'Cidade de Origem', 'UFR')}" for _, row in ultimos.iterrows()])
        st.markdown(f'''
        <div class="terminal-ticker">
            <span style="color:#00e5ff; font-weight:bold;">LIVE FEED:</span>
            <div class="ticker-content">
                <span class="ticker-text">{feed_msg} /// BEM-VINDOS À 1ª REGIONAL MATO GROSSO DA MOSTRA NACIONAL DE ROBÓTICA!</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([1.1, 1, 1.1])

    with col_left:
        st.markdown("##### 🏆 TOP ROBÔS & PROJETOS")
        if not df_vote.empty and "Estande Favorito" in df_vote.columns and len(df_vote) > 0:
            top_estandes = df_vote['Estande Favorito'].value_counts().head(5).reset_index()
            top_estandes.columns = ['Estande', 'Votos']
            
            fig_rank = px.bar(
                top_estandes, x='Votos', y='Estande', orientation='h',
                text='Votos', color='Votos',
                color_continuous_scale=['#00e5ff', '#7928ca', '#ff007f']
            )
            fig_rank.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Orbitron", color="#ffffff", size=12),
                yaxis=dict(autorange="reversed"), coloraxis_showscale=False,
                height=260, margin=dict(l=5, r=5, t=5, b=5)
            )
            fig_rank.update_traces(textposition='outside')
            st.plotly_chart(fig_rank, use_container_width=True)
        else:
            st.info("Aguardando votação popular...")

    with col_mid:
        st.markdown("##### 🎯 META DE IMPACTO (UFR)")
        meta_visitantes = 300
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_participantes,
            domain = {'x': [0, 1], 'y': [0, 1]},
            number = {'font': {'family': 'Orbitron', 'color': '#00ff66', 'size': 34}},
            gauge = {
                'axis': {'range': [None, meta_visitantes], 'tickcolor': "#00e5ff"},
                'bar': {'color': "#00e5ff"},
                'bgcolor': "rgba(0,0,0,0.5)",
                'borderwidth': 2,
                'bordercolor': "#7928ca",
                'steps': [
                    {'range': [0, meta_visitantes * 0.5], 'color': 'rgba(0, 229, 255, 0.1)'},
                    {'range': [meta_visitantes * 0.5, meta_visitantes], 'color': 'rgba(121, 40, 202, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "#ff007f", 'width': 4},
                    'thickness': 0.75,
                    'value': meta_visitantes
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=260,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        st.markdown("##### 💬 RADAR DE FEEDBACK")
        cores = ["#00e5ff", "#ff007f", "#00ff66", "#f5a623", "#7928ca"]
        tags_list = []
        
        if not df_vote.empty and "O que você mais gostou?" in df_vote.columns:
            contagem = df_vote['O que você mais gostou?'].value_counts()
            for idx, (palavra, qtd) in enumerate(contagem.items()):
                cor = cores[idx % len(cores)]
                tam = min(13 + (qtd * 3), 24)
                tags_list.append(f'<span class="tag-item" style="font-size: {tam}px; color: {cor}; border: 1px solid {cor}66; box-shadow: 0 0 10px {cor}33;">{palavra} ({qtd})</span>')
        else:
            tags_list.append('<span class="tag-item" style="font-size: 15px; color: #00e5ff; border: 1px solid #00e5ff66;">🤖 ROBÔS EM AÇÃO</span>')
            tags_list.append('<span class="tag-item" style="font-size: 14px; color: #ff007f; border: 1px solid #ff007f66;">💡 CRIATIVIDADE</span>')
            tags_list.append('<span class="tag-item" style="font-size: 16px; color: #00ff66; border: 1px solid #00ff6666;">🔥 INOVAÇÃO UFR</span>')
            
        tags_html = f'<div class="wordcloud-box">{"".join(tags_list)}</div>'
        st.markdown(tags_html, unsafe_allow_html=True)

    st.write("")

    st.markdown("##### 🏫 ESCOLAS & INSTITUIÇÕES CONECTADAS NO EVENTO")
    if not df_escolas_validas.empty:
        escolas_resumo = df_escolas_validas.groupby(['Escola_Clean', 'Cidade_Clean']).size().reset_index(name='Total_Alunos')
        
        cards_list = []
        for _, row in escolas_resumo.iterrows():
            escola_nome = row['Escola_Clean']
            cidade_nome = row['Cidade_Clean']
            total_part = row['Total_Alunos']
            
            card = (
                f'<div class="school-card">'
                f'<div>'
                f'<div class="school-name">🏛️ {escola_nome}</div>'
                f'<div class="school-city">📍 POLO: {cidade_nome}</div>'
                f'</div>'
                f'<div class="school-status">'
                f'<span>● PRESENTE NA UFR</span> • <span style="color:#ffffff;">{total_part} participante(s)</span>'
                f'</div>'
                f'</div>'
            )
            cards_list.append(card)
        
        html_final = f'<div class="school-grid">{"".join(cards_list)}</div>'
        st.markdown(html_final, unsafe_allow_html=True)
    else:
        st.info("Aguardando credenciamento das escolas e delegações...")

# Chama a função fragmento para iniciar o painel dinâmico
painel_ao_vivo()
