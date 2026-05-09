import streamlit as st
import os
from PIL import Image

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ICON = os.path.join(_ROOT, "input", "PeakForm Icon.png")


def _html(path: str) -> str:
    with open(os.path.join(_ROOT, path), "r", encoding="utf-8") as f:
        return f.read()


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PeakForm",
    page_icon=Image.open(_ICON),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
for _k, _v in [
    ("authenticated", False),
    ("page", "landing"),
    ("login_error", False),
    ("has_first_pullup_access", False),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── URL nav router ─────────────────────────────────────────────────────────────
_nav = st.query_params.get("nav", None)
if _nav:
    if _nav == "login":
        st.session_state.page = "login"
    elif _nav == "area_atleta":
        st.session_state.page = "area_atleta" if st.session_state.authenticated else "login"
    elif _nav == "landing":
        st.session_state.page = "landing"
    elif _nav == "first_pullup":
        if st.session_state.authenticated and st.session_state.has_first_pullup_access:
            st.session_state.page = "first_pullup"
        else:
            st.session_state.page = "login"
    elif _nav == "em_breve":
        st.session_state.page = "em_breve"
    elif _nav == "logout":
        st.session_state.authenticated = False
        st.session_state.login_error = False
        st.session_state.has_first_pullup_access = False
        st.session_state.page = "landing"
    st.query_params.clear()
    st.rerun()

# ── Shared CSS ────────────────────────────────────────────────────────────────
_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Barlow:wght@300;400;500;600&display=swap');
:root {
  --black: #111111; --black2: #0d0d0d; --white: #F5F2EE;
  --warm-gray: #9E9890; --gray2: #6a6560;
  --orange: #C84B11; --orange-light: #E05515;
}
#MainMenu, header, footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.stApp { background: var(--black) !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }
iframe { border: none !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
.element-container { margin-bottom: 0 !important; padding: 0 !important; }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# LANDING
# ─────────────────────────────────────────────────────────────────────────────
def show_landing():
    st.markdown(_BASE_CSS + """
<style>
.pf-sl-logo {
  font-family: 'Barlow Condensed', sans-serif; font-size: 1.9rem;
  font-weight: 800; color: #F5F2EE; letter-spacing: .02em;
  padding: .72rem 0 .72rem 2rem; display: block;
}
.pf-sl-logo span { color: #C84B11; }
.pf-sl-links {
  display: flex; gap: 2rem; list-style: none;
  padding: .85rem 0; margin: 0; align-items: center;
}
.pf-sl-links a {
  font-size: .78rem; font-weight: 500; letter-spacing: .12em;
  text-transform: uppercase; color: #9E9890; text-decoration: none;
}
/* Nav strip */
[data-testid="stHorizontalBlock"] {
  background: rgba(17,17,17,.97) !important;
  border-bottom: 1px solid rgba(200,75,17,.15) !important;
  gap: 0 !important; align-items: stretch !important;
}
[data-testid="stHorizontalBlock"] [data-testid="column"] { padding: 0 !important; }
[data-testid="stHorizontalBlock"] .stButton > button {
  font-family: 'Barlow', sans-serif !important; border-radius: 0 !important;
  font-size: .74rem !important; font-weight: 600 !important;
  letter-spacing: .1em !important; text-transform: uppercase !important;
  padding: .74rem 1rem !important; width: 100% !important;
  transition: all .2s !important;
}
/* Login (3rd col) — outline */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-last-child(2) .stButton > button {
  background: transparent !important; color: rgba(245,242,238,.75) !important;
  border: 1px solid rgba(245,242,238,.18) !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-last-child(2) .stButton > button:hover {
  border-color: rgba(245,242,238,.45) !important; color: #F5F2EE !important;
}
/* Área do Atleta (last col) — orange */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button {
  background: #C84B11 !important; color: #F5F2EE !important; border: none !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button:hover {
  background: #E05515 !important;
}
</style>
""", unsafe_allow_html=True)

    c_logo, c_links, c_login, c_area = st.columns([2.2, 5.1, 1.1, 1.8])
    with c_logo:
        st.markdown('<div class="pf-sl-logo">Peak<span>Form</span></div>', unsafe_allow_html=True)
    with c_links:
        st.markdown(
            '<ul class="pf-sl-links">'
            '<li><a href="#">Sobre</a></li><li><a href="#">Método</a></li>'
            '<li><a href="#">Programas</a></li><li><a href="#">Planos</a></li>'
            '<li><a href="#">Coaches</a></li></ul>',
            unsafe_allow_html=True,
        )
    with c_login:
        if st.button("Login", key="lnd_login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    with c_area:
        if st.button("Área do Atleta", key="lnd_area", use_container_width=True):
            st.session_state.page = "area_atleta" if st.session_state.authenticated else "login"
            st.rerun()

    landing_html = _html("index.html")
    landing_html = landing_html.replace(
        "</head>",
        "<style>nav{display:none!important}.hero{padding-top:4rem!important}</style></head>",
        1,
    )
    st.components.v1.html(landing_html, height=900, scrolling=True)


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown(_BASE_CSS + """
<style>
.stApp,[data-testid="stAppViewContainer"],section[data-testid="stMain"] {
  background: #0a0a0a !important;
}
[data-testid="stHorizontalBlock"] { background: transparent !important; border-bottom: none !important; }
[data-testid="column"] { padding: 0 !important; }

.pf-login-brand {
  min-height: 100vh; display: flex; flex-direction: column;
  justify-content: center; padding: 4rem 3.5rem;
  background: #0d0d0d; border-right: 1px solid rgba(245,242,238,.05);
  font-family: 'Barlow', sans-serif; position: relative; overflow: hidden;
}
.pf-login-brand::after {
  content: 'PF'; position: absolute; bottom: -3rem; right: -2rem;
  font-family: 'Barlow Condensed', sans-serif; font-size: 18rem; font-weight: 900;
  color: rgba(200,75,17,.035); line-height: 1; pointer-events: none; user-select: none;
}
.pf-lb-logo { font-family: 'Barlow Condensed', sans-serif; font-size: 2rem; font-weight: 800; color: #F5F2EE; }
.pf-lb-logo span { color: #C84B11; }
.pf-lb-tag { font-size: .63rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: #9E9890; margin-top: .3rem; margin-bottom: 3.5rem; }
.pf-lb-eyebrow { font-size: .63rem; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: #C84B11; display: flex; align-items: center; gap: .7rem; margin-bottom: 1rem; }
.pf-lb-eyebrow::before { content: ''; width: 20px; height: 1px; background: #C84B11; flex-shrink: 0; }
.pf-lb-title { font-family: 'Barlow Condensed', sans-serif; font-size: 3rem; font-weight: 900; text-transform: uppercase; line-height: 1; color: #F5F2EE; margin-bottom: 1.2rem; }
.pf-lb-text { font-size: .87rem; color: #9E9890; line-height: 1.8; margin-bottom: 2rem; max-width: 380px; font-weight: 300; }
.pf-lb-list { list-style: none; display: flex; flex-direction: column; gap: .7rem; }
.pf-lb-list li { font-size: .82rem; color: #9E9890; display: flex; gap: .7rem; align-items: flex-start; line-height: 1.5; font-weight: 300; }
.pf-lb-list li::before { content: '→'; color: #C84B11; font-weight: 700; flex-shrink: 0; }

.pf-login-form-wrap {
  min-height: 100vh; display: flex; flex-direction: column;
  align-items: center; justify-content: center; padding: 2rem; background: #0a0a0a;
}
.pf-lf-logo { font-family: 'Barlow Condensed', sans-serif; font-size: 2rem; font-weight: 800; color: #F5F2EE; text-align: center; }
.pf-lf-logo span { color: #C84B11; }
.pf-lf-tag { font-size: .63rem; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: #9E9890; text-align: center; margin-top: .3rem; margin-bottom: 2.5rem; }
.pf-lf-card { background: #111111; border: 1px solid rgba(245,242,238,.06); padding: 2.5rem; width: 100%; max-width: 380px; }
.pf-lf-title { font-family: 'Barlow Condensed', sans-serif; font-size: 1.5rem; font-weight: 800; text-transform: uppercase; letter-spacing: .05em; color: #F5F2EE; margin-bottom: .4rem; }
.pf-lf-sub { font-size: .82rem; color: #9E9890; margin-bottom: 1.5rem; line-height: 1.6; font-weight: 300; }
.pf-error { background: rgba(200,75,17,.08); border-left: 2px solid #C84B11; color: #C84B11; font-size: .8rem; padding: .7rem 1rem; margin-bottom: 1rem; line-height: 1.5; }
.pf-test-block { margin-top: 1.2rem; padding: .85rem 1.1rem; background: rgba(245,242,238,.02); border: 1px solid rgba(245,242,238,.05); }
.pf-test-label { font-size: .58rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: rgba(158,152,144,.5); margin-bottom: .45rem; }
.pf-test-data { font-size: .76rem; color: #6a6560; line-height: 1.75; }
.pf-test-data code { color: #9E9890; background: rgba(245,242,238,.04); padding: .08rem .35rem; font-size: .74rem; font-family: monospace; }

[data-testid="stTextInput"] input {
  background: #141414 !important; color: #F5F2EE !important;
  border: 1px solid rgba(245,242,238,.13) !important; border-radius: 0 !important;
  font-family: 'Barlow', sans-serif !important; font-size: .9rem !important;
  caret-color: #C84B11 !important; -webkit-text-fill-color: #F5F2EE !important;
}
[data-testid="stTextInput"] input::placeholder {
  color: rgba(245,242,238,.28) !important; -webkit-text-fill-color: rgba(245,242,238,.28) !important;
}
[data-testid="stTextInput"] input:focus { border-color: #C84B11 !important; box-shadow: none !important; }
[data-testid="stTextInput"] input:-webkit-autofill,
[data-testid="stTextInput"] input:-webkit-autofill:focus {
  -webkit-box-shadow: 0 0 0 1000px #141414 inset !important;
  -webkit-text-fill-color: #F5F2EE !important;
}
[data-testid="stTextInput"] label p {
  font-size: .63rem !important; font-weight: 600 !important;
  letter-spacing: .15em !important; text-transform: uppercase !important; color: #9E9890 !important;
}
[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important; }
[data-testid="stFormSubmitButton"] > button {
  background: #C84B11 !important; color: #F5F2EE !important; border: none !important;
  border-radius: 0 !important; font-family: 'Barlow', sans-serif !important;
  font-size: .82rem !important; font-weight: 700 !important; letter-spacing: .12em !important;
  text-transform: uppercase !important; width: 100% !important;
  padding: .9rem !important; margin-top: .5rem !important; cursor: pointer !important;
}
[data-testid="stFormSubmitButton"] > button:hover { background: #E05515 !important; }
small { display: none !important; }
.stButton > button {
  background: transparent !important; color: #6a6560 !important;
  border: 1px solid rgba(245,242,238,.08) !important; border-radius: 0 !important;
  font-family: 'Barlow', sans-serif !important; font-size: .72rem !important;
  font-weight: 500 !important; letter-spacing: .08em !important;
  text-transform: uppercase !important; width: 100% !important;
  padding: .65rem !important; margin-top: .6rem !important;
}
.stButton > button:hover { border-color: rgba(245,242,238,.2) !important; color: #9E9890 !important; }
</style>
""", unsafe_allow_html=True)

    col_brand, col_form = st.columns([1, 1])
    with col_brand:
        st.markdown("""
<div class="pf-login-brand">
  <div class="pf-lb-logo">Peak<span>Form</span></div>
  <div class="pf-lb-tag">Treino funcional &amp; performance</div>
  <div class="pf-lb-eyebrow">Área do Atleta</div>
  <div class="pf-lb-title">CONTINUA A TUA<br>PROGRESSÃO.</div>
  <p class="pf-lb-text">Acede aos teus programas, sessões, vídeos técnicos e notas de treino num só lugar.</p>
  <ul class="pf-lb-list">
    <li>Programas comprados</li>
    <li>Sessões organizadas por semana</li>
    <li>Progresso e notas de treino</li>
    <li>Acesso ao First Pull-Up</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    with col_form:
        st.markdown("""
<div class="pf-login-form-wrap">
  <div class="pf-lf-logo">Peak<span>Form</span></div>
  <div class="pf-lf-tag">Área Reservada</div>
  <div class="pf-lf-card">
    <div class="pf-lf-title">Entrar</div>
    <p class="pf-lf-sub">Entra na tua Área do Atleta para aceder aos programas, sessões e progresso.</p>
""", unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown(
                '<div class="pf-error">Dados inválidos. Confirma o utilizador e a palavra-passe.</div>',
                unsafe_allow_html=True,
            )

        with st.form("login_form", clear_on_submit=False):
            user = st.text_input("Utilizador", placeholder="O teu utilizador")
            pwd  = st.text_input("Palavra-passe", type="password", placeholder="A tua palavra-passe")
            submitted = st.form_submit_button("Entrar →")

        st.markdown("""
    <div class="pf-test-block">
      <div class="pf-test-label">Conta de teste</div>
      <div class="pf-test-data">
        Utilizador: <code>PeakFormTeste</code><br>
        Palavra-passe: <code>teste123</code>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        if st.button("← Voltar à página inicial", key="login_back"):
            st.session_state.page = "landing"
            st.rerun()

    if submitted:
        if user == "PeakFormTeste" and pwd == "teste123":
            st.session_state.authenticated = True
            st.session_state.has_first_pullup_access = True
            st.session_state.page = "area_atleta"
            st.session_state.login_error = False
        else:
            st.session_state.login_error = True
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ÁREA DO ATLETA
# ─────────────────────────────────────────────────────────────────────────────
def show_area_atleta():
    st.markdown(_BASE_CSS + """
<style>
.stApp { background: #F7F5F2 !important; }
[data-testid="stAppViewContainer"] { background: #F7F5F2 !important; }
section[data-testid="stMain"] { background: #F7F5F2 !important; }
[data-testid="stHorizontalBlock"] { background: transparent !important; border-bottom: none !important; }

.pf-anav { display: flex; align-items: center; justify-content: space-between; padding: 1rem 2.5rem; background: #111111; }
.pf-anav-logo { font-family: 'Barlow Condensed', sans-serif; font-size: 1.4rem; font-weight: 800; color: #F5F2EE; }
.pf-anav-logo span { color: #C84B11; }
.pf-anav-tag { font-size: .67rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: #9E9890; }

.pf-amain { background: #F7F5F2; padding: 3rem 3rem 1.5rem; }
.pf-atag { font-size: .67rem; font-weight: 600; letter-spacing: .25em; text-transform: uppercase; color: #C84B11; display: flex; align-items: center; gap: .7rem; margin-bottom: 1rem; }
.pf-atag::before { content: ''; display: block; width: 20px; height: 1px; background: #C84B11; }
.pf-atitle { font-family: 'Barlow Condensed', sans-serif; font-size: 2.8rem; font-weight: 900; text-transform: uppercase; color: #111111; line-height: 1; margin-bottom: .6rem; }
.pf-asub { font-size: .9rem; color: #6a6560; font-weight: 300; line-height: 1.7; max-width: 520px; margin-bottom: 2.5rem; }
.pf-plabel { font-size: .67rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: #9E9890; padding-bottom: .7rem; border-bottom: 1px solid rgba(17,17,17,.1); margin-bottom: 1.5rem; }
.pf-pcard { background: #111111; border: 1px solid rgba(17,17,17,.15); display: grid; grid-template-columns: 1fr 155px; max-width: 700px; }
.pf-pcard-body { padding: 2rem 2.2rem 1.8rem; }
.pf-pbadge { display: inline-flex; align-items: center; gap: .5rem; font-size: .6rem; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: #C84B11; margin-bottom: .9rem; }
.pf-pbadge-dot { width: 5px; height: 5px; border-radius: 50%; background: #C84B11; }
.pf-pname { font-family: 'Barlow Condensed', sans-serif; font-size: 2rem; font-weight: 900; text-transform: uppercase; color: #F5F2EE; line-height: 1; margin-bottom: .65rem; }
.pf-pname em { color: #C84B11; font-style: normal; }
.pf-pdesc { font-size: .83rem; color: #9E9890; line-height: 1.7; margin-bottom: 1.3rem; max-width: 380px; }
.pf-pmeta { display: flex; gap: 1.8rem; padding-top: 1.1rem; border-top: 1px solid rgba(245,242,238,.07); }
.pf-mitem { display: flex; flex-direction: column; gap: .12rem; }
.pf-mval { font-family: 'Barlow Condensed', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F5F2EE; }
.pf-mkey { font-size: .58rem; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; color: #6a6560; }
.pf-pvisual { background: linear-gradient(135deg,#1a0800 0%,#2d0e00 50%,#1a0800 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; border-left: 1px solid rgba(245,242,238,.06); position: relative; overflow: hidden; }
.pf-pvisual::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse 80% 70% at 50% 50%,rgba(200,75,17,.2) 0%,transparent 70%); }
.pf-pvnum { font-family: 'Barlow Condensed', sans-serif; font-size: 5rem; font-weight: 900; color: rgba(200,75,17,.15); line-height: 1; position: relative; z-index: 1; letter-spacing: -.04em; }
.pf-pvlbl { font-size: .58rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: #C84B11; position: relative; z-index: 1; margin-top: .3rem; }
.pf-coming-card { background: #F0EDE8; border: 1px solid rgba(17,17,17,.1); max-width: 700px; margin-top: 1rem; padding: 1.5rem 2.2rem; display: flex; align-items: center; gap: 1.5rem; opacity: .7; }
.pf-coming-badge { font-size: .58rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; color: #9E9890; border: 1px solid rgba(17,17,17,.15); padding: .25rem .7rem; white-space: nowrap; }
.pf-coming-name { font-family: 'Barlow Condensed', sans-serif; font-size: 1.1rem; font-weight: 800; text-transform: uppercase; color: #6a6560; }
.pf-cat-label { font-size: .65rem; font-weight: 700; letter-spacing: .3em; text-transform: uppercase; color: #9E9890; margin-top: 2.5rem; margin-bottom: 1rem; padding-bottom: .5rem; border-bottom: 1px solid rgba(17,17,17,.1); }
.pf-coming-section { background: #F0EDE8; border: 1px solid rgba(17,17,17,.08); max-width: 700px; padding: 1.2rem 2rem; font-size: .82rem; color: #9E9890; font-style: italic; }

.pf-btn-zone { background: #F7F5F2; padding: 1.5rem 3rem 3rem; }
.stButton > button {
  font-family: 'Barlow', sans-serif !important; border-radius: 0 !important;
  font-size: .8rem !important; font-weight: 700 !important; letter-spacing: .1em !important;
  text-transform: uppercase !important; padding: .75rem 1.8rem !important;
  transition: all .2s !important; border: 1px solid rgba(17,17,17,.2) !important;
  background: transparent !important; color: #6a6560 !important;
}
.stButton > button:hover { background: rgba(17,17,17,.05) !important; color: #111111 !important; border-color: rgba(17,17,17,.4) !important; }
[data-testid="stBaseButton-primary"] > button, button[kind="primary"] {
  background: #C84B11 !important; color: #F5F2EE !important; border-color: #C84B11 !important;
}
[data-testid="stBaseButton-primary"] > button:hover, button[kind="primary"]:hover {
  background: #E05515 !important; border-color: #E05515 !important;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="pf-anav">
  <div class="pf-anav-logo">Peak<span>Form</span></div>
  <div class="pf-anav-tag">Área do Atleta</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="pf-amain">
  <div class="pf-atag">Os teus programas</div>
  <div class="pf-atitle">Área do Atleta</div>
  <p class="pf-asub">Os teus programas PeakForm, organizados para treinares com progressão, clareza e método.</p>
  <div class="pf-plabel">Programas disponíveis</div>
  <div class="pf-cat-label">Skills</div>
  <div class="pf-pcard">
    <div class="pf-pcard-body">
      <div class="pf-pbadge"><span class="pf-pbadge-dot"></span>Disponível</div>
      <div class="pf-pname">First <em>Pull-Up</em></div>
      <p class="pf-pdesc">Programa de 6 semanas para conquistares a tua primeira strict pull-up com progressão estruturada, vídeos técnicos e critérios claros de evolução.</p>
      <div class="pf-pmeta">
        <div class="pf-mitem"><div class="pf-mval">6</div><div class="pf-mkey">Semanas</div></div>
        <div class="pf-mitem"><div class="pf-mval">3×</div><div class="pf-mkey">Por semana</div></div>
        <div class="pf-mitem"><div class="pf-mval">~25'</div><div class="pf-mkey">Por sessão</div></div>
        <div class="pf-mitem"><div class="pf-mval">3</div><div class="pf-mkey">Fases</div></div>
      </div>
    </div>
    <div class="pf-pvisual">
      <div class="pf-pvnum">01</div>
      <div class="pf-pvlbl">Skills</div>
    </div>
  </div>
  <div class="pf-coming-card"><div class="pf-coming-badge">Em breve</div><div class="pf-coming-name">Bar Muscle-Up</div></div>
  <div class="pf-coming-card"><div class="pf-coming-badge">Em breve</div><div class="pf-coming-name">HSPU — Handstand Push-Up</div></div>
  <div class="pf-cat-label">Strength</div>
  <div class="pf-coming-section">Em desenvolvimento — programas de força e ciclos estruturados em breve.</div>
  <div class="pf-cat-label">Engine</div>
  <div class="pf-coming-section">Em desenvolvimento — programas de condicionamento e capacidade aeróbia em breve.</div>
  <div class="pf-cat-label">Competition</div>
  <div class="pf-coming-section">Em desenvolvimento — preparação competitiva para Open, ATHX e HYROX em breve.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="pf-btn-zone">', unsafe_allow_html=True)
    c1, c2, _ = st.columns([1.6, 1, 5])
    with c1:
        if st.button("Abrir programa →", key="open_prog", type="primary"):
            st.session_state.page = "first_pullup"
            st.rerun()
    with c2:
        if st.button("Sair", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.has_first_pullup_access = False
            st.session_state.login_error = False
            st.session_state.page = "landing"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FIRST PULL-UP
# ─────────────────────────────────────────────────────────────────────────────
def show_first_pullup():
    prog_path = os.path.join(_ROOT, "input", "first-pullup-peakform.html")

    st.markdown(_BASE_CSS + """
<style>
.pf-ptopbar { display: flex; align-items: center; gap: 1.4rem; padding: .95rem 2rem; background: rgba(13,13,13,.98); border-bottom: 1px solid rgba(200,75,17,.15); }
.pf-ptopbar-logo { font-family: 'Barlow Condensed', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F5F2EE; }
.pf-ptopbar-logo span { color: #C84B11; }
.pf-ptopbar-sep { width: 1px; height: 1.1rem; background: rgba(245,242,238,.14); }
.pf-ptopbar-title { font-size: .66rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: #9E9890; }
.pf-pback-bar { padding: .6rem 2rem; background: #111111; border-bottom: 1px solid rgba(245,242,238,.05); }
.stButton > button {
  font-family: 'Barlow', sans-serif !important; border-radius: 0 !important;
  font-size: .76rem !important; font-weight: 600 !important; letter-spacing: .1em !important;
  text-transform: uppercase !important; padding: .55rem 1.4rem !important;
  background: transparent !important; color: #9E9890 !important;
  border: 1px solid rgba(245,242,238,.14) !important;
}
.stButton > button:hover { background: rgba(245,242,238,.06) !important; color: #F5F2EE !important; border-color: rgba(245,242,238,.28) !important; }
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="pf-ptopbar">
  <div class="pf-ptopbar-logo">Peak<span>Form</span></div>
  <div class="pf-ptopbar-sep"></div>
  <div class="pf-ptopbar-title">First Pull-Up — Programa completo</div>
</div>
<div class="pf-pback-bar">
""", unsafe_allow_html=True)

    if st.button("← Voltar à Área do Atleta", key="back_area"):
        st.session_state.page = "area_atleta"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if not os.path.exists(prog_path):
        st.markdown("""
<div style="padding:4rem 2rem;text-align:center;font-family:'Barlow',sans-serif;background:#111111;">
  <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.5rem;font-weight:800;text-transform:uppercase;color:#F5F2EE;margin-bottom:1rem;">Ficheiro não encontrado</div>
  <p style="font-size:.88rem;color:#9E9890;line-height:1.8;">
    Coloca o ficheiro <code style="color:#C84B11;">first-pullup-peakform.html</code> na pasta <code style="color:#C84B11;">input/</code> e reinicia a app.
  </p>
</div>""", unsafe_allow_html=True)
        return

    st.components.v1.html(_html("input/first-pullup-peakform.html"), height=870, scrolling=True)


# ─────────────────────────────────────────────────────────────────────────────
# EM BREVE (Coaching 1:1)
# ─────────────────────────────────────────────────────────────────────────────
def show_em_breve():
    st.markdown(_BASE_CSS + """
<style>
.pf-eb-wrap { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; font-family: 'Barlow', sans-serif; }
.pf-eb-logo { font-family: 'Barlow Condensed', sans-serif; font-size: 1.8rem; font-weight: 800; color: #F5F2EE; margin-bottom: 4rem; }
.pf-eb-logo span { color: #C84B11; }
.pf-eb-eyebrow { font-size: .63rem; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: #C84B11; display: flex; align-items: center; gap: .7rem; margin-bottom: 1rem; }
.pf-eb-eyebrow::before { content: ''; width: 20px; height: 1px; background: #C84B11; flex-shrink: 0; }
.pf-eb-title { font-family: 'Barlow Condensed', sans-serif; font-size: 3.5rem; font-weight: 900; text-transform: uppercase; color: #F5F2EE; line-height: 1; margin-bottom: 1.5rem; }
.pf-eb-text { font-size: .9rem; color: #9E9890; line-height: 1.85; max-width: 500px; font-weight: 300; text-align: center; }
.stButton > button {
  background: transparent !important; color: #6a6560 !important;
  border: 1px solid rgba(245,242,238,.1) !important; border-radius: 0 !important;
  font-family: 'Barlow', sans-serif !important; font-size: .74rem !important;
  font-weight: 500 !important; letter-spacing: .1em !important; text-transform: uppercase !important;
  padding: .7rem 2rem !important; margin-top: 2.5rem !important;
}
.stButton > button:hover { border-color: rgba(245,242,238,.28) !important; color: #9E9890 !important; }
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="pf-eb-wrap">
  <div class="pf-eb-logo">Peak<span>Form</span></div>
  <div class="pf-eb-eyebrow">Coaching 1:1</div>
  <div class="pf-eb-title">EM BREVE.</div>
  <p class="pf-eb-text">Estamos a preparar uma experiência de acompanhamento mais próxima, estruturada e ajustada ao teu objectivo e nível.</p>
</div>
""", unsafe_allow_html=True)

    _, c, _ = st.columns([3, 2, 3])
    with c:
        if st.button("← Voltar à página inicial", key="eb_back", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
_page = st.session_state.page

if   _page == "landing":      show_landing()
elif _page == "login":        show_login()
elif _page == "area_atleta":  show_area_atleta()  if st.session_state.authenticated else show_login()
elif _page == "first_pullup": show_first_pullup() if (st.session_state.authenticated and st.session_state.has_first_pullup_access) else show_login()
elif _page == "em_breve":     show_em_breve()
else:
    st.session_state.page = "landing"
    st.rerun()
