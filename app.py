import streamlit as st
import os
import threading
import http.server
import socketserver
from PIL import Image

# ── HTTP server (serves index.html + first-pullup-peakform.html) ──────────────
_PORT = 8502
_ROOT = os.path.dirname(os.path.abspath(__file__))

class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=_ROOT, **kwargs)
    def log_message(self, *_):
        pass

def _start_server():
    with socketserver.TCPServer(("", _PORT), _Handler) as httpd:
        httpd.serve_forever()

if "http_server_started" not in st.session_state:
    threading.Thread(target=_start_server, daemon=True).start()
    st.session_state["http_server_started"] = True

# ── Page config ───────────────────────────────────────────────────────────────
_icon = Image.open(os.path.join(_ROOT, "input", "PeakForm Icon.png"))
st.set_page_config(
    page_title="PeakForm",
    page_icon=_icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
for _k, _v in [("authenticated", False), ("page", "landing"), ("login_error", False)]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── URL nav router ─────────────────────────────────────────────────────────────
# Landing iframe buttons use window.parent.location.href='/?nav=X' to trigger
# a Streamlit rerun. Session state persists across reruns (not full reloads).
_nav = st.query_params.get("nav", None)
if _nav:
    if _nav == "login":
        st.session_state.page = "login"
    elif _nav == "area_atleta":
        st.session_state.page = "area_atleta" if st.session_state.authenticated else "login"
    elif _nav == "landing":
        st.session_state.page = "landing"
    elif _nav == "logout":
        st.session_state.authenticated = False
        st.session_state.login_error = False
        st.session_state.page = "landing"
    st.query_params.clear()
    st.rerun()

# ── Shared base CSS ───────────────────────────────────────────────────────────
_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Barlow:wght@300;400;500;600&display=swap');
:root{--black:#111111;--black2:#0d0d0d;--white:#F5F2EE;--gray:#9E9890;--gray2:#6a6560;--orange:#C84B11;--orange-light:#E05515;}
#MainMenu,header,footer{display:none!important;}
[data-testid="stToolbar"]{display:none!important;}
.stApp{background:var(--black)!important;}
.block-container{padding:0!important;max-width:100%!important;margin:0!important;}
section[data-testid="stMain"]>div{padding:0!important;}
iframe{border:none!important;}
div[data-testid="stVerticalBlock"]>div{gap:0!important;}
.element-container{margin-bottom:0!important;padding:0!important;}
[data-testid="column"]{padding:0.25rem 0.5rem 0 0!important;}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# LANDING
# ─────────────────────────────────────────────────────────────────────────────
def show_landing():
    st.markdown(_BASE_CSS, unsafe_allow_html=True)
    st.components.v1.iframe(
        f"http://localhost:{_PORT}/index.html",
        height=900,
        scrolling=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown(_BASE_CSS + """
<style>
.pf-login-wrap{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2rem;font-family:'Barlow',sans-serif;}
.pf-login-logo{font-family:'Barlow Condensed',sans-serif;font-size:2rem;font-weight:800;color:var(--white);letter-spacing:.02em;text-align:center;margin-bottom:.3rem;}
.pf-login-logo span{color:var(--orange);}
.pf-login-sub{font-size:.68rem;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--gray);text-align:center;margin-bottom:2.5rem;}
.pf-login-card{background:#0d0d0d;border:1px solid rgba(245,242,238,.07);padding:2.5rem;width:100%;max-width:380px;}
.pf-login-card h2{font-family:'Barlow Condensed',sans-serif;font-size:1.4rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:var(--white);margin-bottom:.3rem;}
.pf-login-card p{font-size:.82rem;color:var(--gray);margin-bottom:1.5rem;line-height:1.5;}
.pf-error{background:rgba(200,75,17,.1);border:1px solid rgba(200,75,17,.3);color:var(--orange);font-size:.8rem;padding:.7rem 1rem;margin-bottom:1rem;line-height:1.4;}
.pf-back{font-size:.72rem;color:var(--gray2);text-align:center;margin-top:1.5rem;}
.pf-back a{color:var(--gray2);text-decoration:none;letter-spacing:.05em;}
.pf-back a:hover{color:var(--gray);}

[data-testid="stTextInput"] input{background:rgba(245,242,238,.04)!important;border:1px solid rgba(245,242,238,.12)!important;border-radius:0!important;color:var(--white)!important;font-family:'Barlow',sans-serif!important;font-size:.9rem!important;}
[data-testid="stTextInput"] input:focus{border-color:var(--orange)!important;box-shadow:none!important;}
[data-testid="stTextInput"] label p{font-size:.68rem!important;font-weight:600!important;letter-spacing:.15em!important;text-transform:uppercase!important;color:var(--gray)!important;}
[data-testid="stForm"]{border:none!important;background:transparent!important;padding:0!important;}
[data-testid="stFormSubmitButton"]>button{background:var(--orange)!important;color:var(--white)!important;border:none!important;border-radius:0!important;font-family:'Barlow',sans-serif!important;font-size:.82rem!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important;width:100%!important;padding:.85rem!important;margin-top:.3rem!important;}
[data-testid="stFormSubmitButton"]>button:hover{background:var(--orange-light)!important;}
</style>
""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div class="pf-login-wrap">
          <div class="pf-login-logo">Peak<span>Form</span></div>
          <div class="pf-login-sub">Área reservada</div>
          <div class="pf-login-card">
            <h2>Entrar</h2>
            <p>Acede à tua área de atleta e aos teus programas.</p>
        """, unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown('<div class="pf-error">Dados inválidos. Confirma o utilizador e a palavra-passe.</div>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            user = st.text_input("Utilizador")
            pwd  = st.text_input("Palavra-passe", type="password")
            submitted = st.form_submit_button("Entrar →")

        st.markdown("""
          </div>
          <div class="pf-back"><a href="/?nav=landing">← Voltar à landing</a></div>
        </div>
        """, unsafe_allow_html=True)

    if submitted:
        if user == "PeakFormTeste" and pwd == "teste123":
            st.session_state.authenticated = True
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
.pf-anav{display:flex;align-items:center;justify-content:space-between;padding:1.15rem 3rem;background:rgba(13,13,13,.98);border-bottom:1px solid rgba(200,75,17,.15);}
.pf-anav-logo{font-family:'Barlow Condensed',sans-serif;font-size:1.5rem;font-weight:800;color:var(--white);letter-spacing:.02em;}
.pf-anav-logo span{color:var(--orange);}
.pf-anav-tag{font-size:.67rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gray);}
.pf-amain{padding:3.5rem 3rem 1.5rem;}
.pf-atag{font-size:.67rem;font-weight:600;letter-spacing:.25em;text-transform:uppercase;color:var(--orange);display:flex;align-items:center;gap:.7rem;margin-bottom:1rem;}
.pf-atag::before{content:'';display:block;width:20px;height:1px;background:var(--orange);}
.pf-atitle{font-family:'Barlow Condensed',sans-serif;font-size:2.8rem;font-weight:900;text-transform:uppercase;color:var(--white);line-height:1;margin-bottom:.6rem;}
.pf-asub{font-size:.9rem;color:var(--gray);font-weight:300;line-height:1.7;max-width:520px;margin-bottom:2.5rem;}
.pf-plabel{font-size:.67rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gray2);padding-bottom:.7rem;border-bottom:1px solid rgba(245,242,238,.06);margin-bottom:1.5rem;}
.pf-pcard{background:#0d0d0d;border:1px solid rgba(245,242,238,.07);display:grid;grid-template-columns:1fr 155px;max-width:700px;}
.pf-pcard-body{padding:2rem 2.2rem 1.8rem;}
.pf-pbadge{display:inline-flex;align-items:center;gap:.5rem;font-size:.6rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--orange);margin-bottom:.9rem;}
.pf-pbadge-dot{width:5px;height:5px;border-radius:50%;background:var(--orange);}
.pf-pname{font-family:'Barlow Condensed',sans-serif;font-size:2rem;font-weight:900;text-transform:uppercase;color:var(--white);line-height:1;margin-bottom:.65rem;}
.pf-pname em{color:var(--orange);font-style:normal;}
.pf-pdesc{font-size:.83rem;color:var(--gray);line-height:1.7;margin-bottom:1.3rem;max-width:380px;}
.pf-pmeta{display:flex;gap:1.8rem;padding-top:1.1rem;border-top:1px solid rgba(245,242,238,.07);}
.pf-mitem{display:flex;flex-direction:column;gap:.12rem;}
.pf-mval{font-family:'Barlow Condensed',sans-serif;font-size:1.25rem;font-weight:800;color:var(--white);}
.pf-mkey{font-size:.58rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--gray2);}
.pf-pvisual{background:linear-gradient(135deg,#1a0800 0%,#2d0e00 50%,#1a0800 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;border-left:1px solid rgba(245,242,238,.06);position:relative;overflow:hidden;}
.pf-pvisual::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 50% 50%,rgba(200,75,17,.2) 0%,transparent 70%);}
.pf-pvnum{font-family:'Barlow Condensed',sans-serif;font-size:5rem;font-weight:900;color:rgba(200,75,17,.15);line-height:1;position:relative;z-index:1;letter-spacing:-.04em;}
.pf-pvlbl{font-size:.58rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);position:relative;z-index:1;margin-top:.3rem;}
.pf-btn-zone{padding:1.5rem 3rem 3rem;}

/* st.button overrides */
.stButton>button{font-family:'Barlow',sans-serif!important;border-radius:0!important;font-size:.8rem!important;font-weight:700!important;letter-spacing:.1em!important;text-transform:uppercase!important;padding:.75rem 1.8rem!important;transition:all .2s!important;border:1px solid rgba(245,242,238,.18)!important;background:transparent!important;color:var(--gray)!important;}
.stButton>button:hover{background:rgba(245,242,238,.06)!important;color:var(--white)!important;border-color:rgba(245,242,238,.3)!important;}
.stButton>button[kind="primary"]{background:var(--orange)!important;color:var(--white)!important;border-color:var(--orange)!important;}
.stButton>button[kind="primary"]:hover{background:var(--orange-light)!important;border-color:var(--orange-light)!important;}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="pf-anav">
  <div class="pf-anav-logo">Peak<span>Form</span></div>
  <div class="pf-anav-tag">Área do Atleta</div>
</div>
<div class="pf-amain">
  <div class="pf-atag">Os teus programas</div>
  <div class="pf-atitle">Área do Atleta</div>
  <p class="pf-asub">Os teus programas PeakForm, organizados para treinares com progressão, clareza e método.</p>
  <div class="pf-plabel">Programas disponíveis</div>
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
</div>
<div class="pf-btn-zone">
""", unsafe_allow_html=True)

    c1, c2, _ = st.columns([1.6, 1, 5])
    with c1:
        if st.button("Abrir programa →", key="open_prog", type="primary"):
            st.session_state.page = "first_pullup"
            st.rerun()
    with c2:
        if st.button("Sair", key="logout"):
            st.session_state.authenticated = False
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
.pf-ptopbar{display:flex;align-items:center;gap:1.4rem;padding:.95rem 2rem;background:rgba(13,13,13,.98);border-bottom:1px solid rgba(200,75,17,.15);}
.pf-ptopbar-logo{font-family:'Barlow Condensed',sans-serif;font-size:1.35rem;font-weight:800;color:var(--white);}
.pf-ptopbar-logo span{color:var(--orange);}
.pf-ptopbar-sep{width:1px;height:1.1rem;background:rgba(245,242,238,.14);}
.pf-ptopbar-title{font-size:.66rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--gray);}
.pf-pback-bar{padding:.6rem 2rem;background:var(--black);border-bottom:1px solid rgba(245,242,238,.05);}
.stButton>button{font-family:'Barlow',sans-serif!important;border-radius:0!important;font-size:.76rem!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase!important;padding:.55rem 1.4rem!important;background:transparent!important;color:var(--gray)!important;border:1px solid rgba(245,242,238,.14)!important;}
.stButton>button:hover{background:rgba(245,242,238,.06)!important;color:var(--white)!important;border-color:rgba(245,242,238,.28)!important;}
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
<div style="padding:4rem 2rem;text-align:center;font-family:'Barlow',sans-serif;">
  <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.5rem;font-weight:800;text-transform:uppercase;color:#F5F2EE;margin-bottom:1rem;">Ficheiro não encontrado</div>
  <p style="font-size:.88rem;color:#9E9890;line-height:1.8;">
    Coloca o ficheiro <code style="color:#C84B11;background:rgba(200,75,17,.08);padding:.15rem .45rem;">first-pullup-peakform.html</code><br>
    na raiz do repositório e reinicia a app.
  </p>
</div>""", unsafe_allow_html=True)
        return

    st.components.v1.iframe(
        f"http://localhost:{_PORT}/input/first-pullup-peakform.html",
        height=870,
        scrolling=True,
    )


# ── Router ────────────────────────────────────────────────────────────────────
_page = st.session_state.page

if _page == "landing":
    show_landing()
elif _page == "login":
    show_login()
elif _page == "area_atleta":
    show_area_atleta() if st.session_state.authenticated else show_login()
elif _page == "first_pullup":
    show_first_pullup() if st.session_state.authenticated else show_login()
else:
    st.session_state.page = "landing"
    st.rerun()
