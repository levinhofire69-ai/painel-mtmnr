import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import unicodedata
import re
import html

# 1. Configuração da Página para Telão / Projetor
st.set_page_config(
    page_title="Central MTMNR - Ao Vivo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização CSS Cyberpunk / Holográfica com Rolagem Customizada
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

    /* Grid de Escolas Otimizado para 50+ Instituições */
    .school-container-scroll {
        max-height: 380px;
        overflow-y: auto;
        padding-right: 8px;
    }

    .school-container-scroll::-webkit-scrollbar {
        width: 6px;
    }
    .school-container-scroll::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 4px;
    }
    .school-container-scroll::-webkit-scrollbar-thumb {
        background: #00e5ff;
        border-radius: 4px;
    }

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

    /* Nuvem de palavras com alinhamento flexível */
    .wordcloud-box {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 0, 127, 0.4);
        border-radius: 12px;
        padding: 15px;
        min-height: 240px;
        display: flex;
        flex-wrap: wrap;
        align-content: center;
        justify-content: center;
        gap: 12px;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.2);
    }

    .tag-item {
        font-family: 'Orbitron', sans-serif;
        padding: 8px 14px;
        border-radius: 16px;
        animation: floatTag 3s ease-in-out infinite alternate;
        transition: all 0.3s ease;
    }

    .offline-badge {
        display: block;
        text-align: center;
        margin-bottom: 12px;
    }
    .offline-badge span {
        background: #ff007f;
        color: white;
        padding: 5px 14px;
        border-radius: 12px;
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 2px;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
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
        100% { transform: translateY(-4px) scale(1.02); }
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
# HELPERS: DETECÇÃO ROBUSTA DE COLUNA, SANITIZAÇÃO E PADRONIZAÇÃO
# =====================================================================
def _norm_col(s):
    return str(s).strip().lower().replace("\ufeff", "")

def achar_coluna(df, nome_exato, termos_contem=None):
    alvo = _norm_col(nome_exato)
    for c in df.columns:
        if _norm_col(c) == alvo:
            return c
    if termos_contem:
        for c in df.columns:
            cc = _norm_col(c)
            if any(t in cc for t in termos_contem):
                return c
    return None

def padronizar_escola(nome):
    if pd.isna(nome):
        return "Não Informado"

    t = unicodedata.normalize('NFKD', str(nome)).encode('ascii', errors='ignore').decode().upper()
    t = " ".join(t.split())

    if (t == "UFR" or t.startswith("UFR ") or "UNIVERSIDADE FEDERAL" in t or 
        "FACULDADE FEDERAL" in t or "UNIDADE FEDERAL" in t or "FEDERAL DE RONDON" in t or "FEDERAL DE RONONOP" in t):
        return "Universidade Federal de Rondonópolis (UFR)"

    if "IFMT" in t or "INSTITUTO FEDERAL" in t:
        return "Instituto Federal de Mato Grosso (IFMT)"

    if "FRAGEL" in t or "DONA" in t:
        return "EE Cívico-Militar Dona Maria de Lourdes R. Fragelli"

    if "EDITH PEREIRA" in t:
        return "EE Cívico-Militar Prof.ª Edith Pereira Barbosa"

    if "HUGUENEY" in t or "HUGUINEY" in t:
        return "EE Cívico-Militar Carlos Hugueney"

    if "RIBEIRO FARIAS" in t:
        return "Ribeiro Farias Consultoria"

    if t in ("", "N/A", "NA", "-", "IF", "NAN", "NONE", "ESCOLA ESTADUAL"):
        return "Não Informado"

    return str(nome).strip()

def padronizar_cidade(nome):
    if pd.isna(nome) or str(nome).strip() == "":
        return "NÃO INFORMADO"
    s = str(nome).strip()
    s = re.sub(r'\s*[-/]\s*MT\s*$', '', s, flags=re.IGNORECASE).strip()
    if s.upper() in ("N/A", "NA", "-", "IF", "NAN", "NONE"):
        return "NÃO INFORMADO"
    return s

def limpar_nome_projeto(txt):
    if pd.isna(txt):
        return None
    s = str(txt).strip()
    if s == "" or s.lower() == "nan":
        return None
    s = re.sub(r'^\[.*?\]\s*', '', s).strip()
    return s if s else None


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
            return df, False
        else:
            return pd.read_csv(fonte), False
    except Exception:
        try:
            return pd.read_csv(arquivo_backup), True
        except Exception:
            return pd.DataFrame(), False


# =====================================================================
# BLOCO INTELIGENTE COM ATUALIZAÇÃO AUTOMÁTICA EM SEGUNDO PLANO
# =====================================================================
@st.fragment(run_every=4)
def painel_ao_vivo():
    df_cred, cred_offline = carregar_dados_seguro(fonte_cred_input, "dados_credenciamento.csv")
    df_vote, vote_offline = carregar_dados_seguro(fonte_votos_input, "dados_votacao.csv")
    is_offline = cred_offline or vote_offline

    col_cidade = achar_coluna(df_cred, "Polo / Cidade da Instituição", ["polo / cidade", "polo"])
    col_escola = achar_coluna(df_cred, "Nome da Escola ou Instituição", ["nome da escola"])
    col_nome   = achar_coluna(df_cred, "Nome Completo:", ["nome completo"])

    if not df_cred.empty and col_cidade:
        df_cred['Cidade_Clean'] = df_cred[col_cidade].apply(padronizar_cidade)
        total_participantes = len(df_cred)
        total_municipios = df_cred.loc[df_cred['Cidade_Clean'] != 'NÃO INFORMADO', 'Cidade_Clean'].nunique()
    else:
        total_participantes = 0
        total_municipios = 0

    if not df_cred.empty and col_escola:
        df_cred['Escola_Clean'] = df_cred[col_escola].apply(padronizar_escola)
        df_escolas_validas = df_cred[~df_cred['Escola_Clean'].isin(['Não Informado', '', 'NAN', 'NONE', '-'])]
        total_escolas = df_escolas_validas['Escola_Clean'].nunique()
    else:
        total_escolas = 0
        df_escolas_validas = pd.DataFrame()

    col_nota = achar_coluna(df_vote, "Que nota você dá para a 1ª MTMNR na UFR?", ["nota"])
    media_nota = None
    if not df_vote.empty and col_nota:
        serie_notas = pd.to_numeric(
            df_vote[col_nota].astype(str).str.extract(r'(\d+[\.,]?\d*)')[0].str.replace(',', '.'),
            errors='coerce'
        )
        serie_notas = serie_notas.where((serie_notas >= 0) & (serie_notas <= 10))
        if not serie_notas.dropna().empty:
            media_nota = serie_notas.mean()

    banner_html = (
        '<div class="welcome-banner">'
        '<div class="welcome-subtitle">✨ SEJA BEM-VINDO(A) À ✨</div>'
        '<div style="display: flex; align-items: center; justify-content: center; gap: 18px;">'
        '<span class="bot-head">🤖</span>'
        '<div class="welcome-main-title">1ª Regional Mato Grosso da Mostra Nacional de Robótica (MTMNR)</div>'
        '<span class="bot-head">⚡</span>'
        '</div>'
        '<div class="welcome-badge-line">'
        '<span>📍 UNIVERSIDADE FEDERAL DE RONDONÓPOLIS (UFR)</span>'
        '<span>•</span>'
        '<span style="color: #00ff66;">● MONITORAMENTO AO VIVO</span>'
        '</div>'
        '</div>'
    )
    st.markdown(banner_html, unsafe_allow_html=True)

    if is_offline:
        st.markdown('<div class="offline-badge"><span>⚠️ MODO OFFLINE — EXIBINDO CACHE LOCAL</span></div>', unsafe_allow_html=True)

    media_display = f"{media_nota:.1f} ★" if media_nota is not None and not pd.isna(media_nota) else "—"

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_participantes}</div><div class="kpi-label">Público Conectado</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_escolas}</div><div class="kpi-label">Escolas / Instituições</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_municipios}</div><div class="kpi-label">Polos Regionais</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{media_display}</div><div class="kpi-label">Avaliação Geral</div></div>', unsafe_allow_html=True)

    st.write("")

    if not df_cred.empty and col_nome:
        df_feed = df_cred.dropna(subset=[col_nome]).copy()
        df_feed = df_feed[df_feed[col_nome].astype(str).str.strip().ne('')]
        ultimos = df_feed.tail(8)

        feed_msgs = []
        for _, row in ultimos.iterrows():
            nome = html.escape(str(row[col_nome]).strip())
            cidade = html.escape(str(row.get(col_cidade, '')).strip()) if col_cidade else "UFR"
            if not cidade or cidade.upper() == 'NÃO INFORMADO':
                cidade = "UFR"
            feed_msgs.append(f"⚡ [CHECK-IN] {nome} ➔ {cidade}")

        if feed_msgs:
            feed_msg = " /// ".join(feed_msgs)
            ticker_html = (
                f'<div class="terminal-ticker">'
                f'<span style="color:#00e5ff; font-weight:bold;">LIVE FEED:</span>'
                f'<div class="ticker-content">'
                f'<span class="ticker-text">{feed_msg} /// BEM-VINDOS À 1ª REGIONAL MATO GROSSO DA MOSTRA NACIONAL DE ROBÓTICA!</span>'
                f'</div>'
                f'</div>'
            )
            st.markdown(ticker_html, unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([1.1, 1, 1.1])

    with col_left:
        st.markdown("##### 🏆 TOP ROBÔS & PROJETOS")
        col_projeto = achar_coluna(df_vote, "Qual estande ou projeto de robótica você mais gostou?", ["estande", "projeto"])

        if not df_vote.empty and col_projeto:
            serie_projetos = df_vote[col_projeto].apply(limpar_nome_projeto).dropna()
            if not serie_projetos.empty:
                contagem = serie_projetos.value_counts().head(5)
                top_estandes = pd.DataFrame({'Projeto': contagem.index, 'Votos': contagem.values})

                fig_rank = px.bar(
                    top_estandes, x='Votos', y='Projeto', orientation='h',
                    text='Votos', color='Votos',
                    color_continuous_scale=['#00e5ff', '#7928ca', '#ff007f']
                )
                fig_rank.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Orbitron", color="#ffffff", size=11),
                    yaxis=dict(autorange="reversed", title=None),
                    xaxis=dict(title=None),
                    coloraxis_showscale=False,
                    height=260, margin=dict(l=5, r=5, t=5, b=5)
                )
                fig_rank.update_traces(textposition='outside', cliponaxis=False)
                fig_rank.update_xaxes(range=[0, top_estandes['Votos'].max() * 1.2])
                st.plotly_chart(fig_rank, use_container_width=True)
            else:
                st.info("Aguardando votação de projetos...")
        else:
            st.info("Aguardando votação de projetos...")

    with col_mid:
        st.markdown("##### 🎯 META DE IMPACTO (UFR)")
        meta_visitantes = 300
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_participantes,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'font': {'family': 'Orbitron', 'color': '#00ff66', 'size': 34}},
            gauge={
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
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        st.markdown("##### 💬 RADAR DE FEEDBACK (NUVEM DINÂMICA)")
        cores = ["#00e5ff", "#ff007f", "#00ff66", "#f5a623", "#7928ca", "#3b82f6", "#a855f7"]
        tags_list = []

        col_feedback = achar_coluna(df_vote, "O que você mais gostou?", ["gostou"])

        if not df_vote.empty and col_feedback:
            serie_feedback = df_vote[col_feedback].dropna().astype(str).str.strip()
            serie_feedback = serie_feedback[~serie_feedback.isin(['', 'NAN', 'NONE', '-', '.'])]
            serie_feedback = serie_feedback.str.replace(r'^\d+[\s\-\(\)]*', '', regex=True).str.strip()
            serie_feedback = serie_feedback[serie_feedback.ne('')]

            if not serie_feedback.empty:
                # As 3 opções oficiais do formulário
                oficiais = [
                    "Criatividade dos Projetos",
                    "Demonstração prática dos robôs",
                    "Organização / Espaço"
                ]
                
                # Substitui qualquer resposta livre (campo "Outro") por uma categoria genérica
                def categorizar_feedback(txt):
                    for of in oficiais:
                        if txt.lower() == of.lower():
                            return of
                    return "Outros (respostas livres)"

                serie_categorizada = serie_feedback.apply(categorizar_feedback)
                contagem = serie_categorizada.value_counts()

                max_qtd = contagem.max()

                for idx, (resposta, qtd) in enumerate(contagem.items()):
                    cor = cores[idx % len(cores)]
                    
                    # Escala proporcional de tamanho (mínimo 14px, máximo 28px)
                    tam = int(14 + (qtd / max_qtd) * 14) if max_qtd > 0 else 14
                    resposta_safe = html.escape(resposta)

                    tag_html = (
                        f'<span class="tag-item" style="'
                        f'font-size: {tam}px; '
                        f'color: {cor}; '
                        f'border: 1px solid {cor}88; '
                        f'background: {cor}15; '
                        f'box-shadow: 0 0 {10 + (qtd * 2)}px {cor}44; '
                        f'margin: 5px; '
                        f'display: inline-block;'
                        f'">{resposta_safe} ({qtd})</span>'
                    )
                    tags_list.append(tag_html)
            else:
                tags_list.append('<span class="tag-item" style="font-size: 14px; color: #00e5ff; border: 1px solid #00e5ff66;">⏳ AGUARDANDO RESPOSTAS...</span>')
        else:
            tags_list.append('<span class="tag-item" style="font-size: 16px; color: #00e5ff; border: 1px solid #00e5ff66; background: #00e5ff15;">AGUARDANDO FEEDBACKS...</span>')

        wordcloud_html = f'<div class="wordcloud-box">{"".join(tags_list)}</div>'
        st.markdown(wordcloud_html, unsafe_allow_html=True)

    st.write("")

    st.markdown("##### 🏫 ESCOLAS & INSTITUIÇÕES CONECTADAS NO EVENTO")
    if not df_escolas_validas.empty and col_cidade:
        escolas_resumo = df_escolas_validas.groupby('Escola_Clean').agg(
            Total_Alunos=('Escola_Clean', 'size'),
            Cidade=('Cidade_Clean', lambda x: x.mode().iloc[0] if not x.mode().empty else "NÃO INFORMADO")
        ).reset_index().sort_values('Total_Alunos', ascending=False)

        cards_list = []
        for _, row in escolas_resumo.iterrows():
            escola_nome = html.escape(str(row['Escola_Clean']))
            cidade_nome = html.escape(str(row['Cidade']))
            total_part = int(row['Total_Alunos'])

            card_html = (
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
            cards_list.append(card_html)

        grid_html = f'<div class="school-container-scroll"><div class="school-grid">{"".join(cards_list)}</div></div>'
        st.markdown(grid_html, unsafe_allow_html=True)
    else:
        st.info("Aguardando credenciamento das escolas e delegações...")

painel_ao_vivo()
