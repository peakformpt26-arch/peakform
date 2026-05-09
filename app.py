import streamlit as st
import os
import threading
import http.server
import socketserver

# ── Background HTTP server for index.html ──────────────────────────────────
# Streamlit renders components inside iframes. Serving the landing page via
# a real HTTP server on a side port lets the iframe behave exactly like a
# browser tab: position:fixed nav works, scripts run, fonts/Hotmart load.
_PORT = 8502
_ROOT = os.path.dirname(os.path.abspath(__file__))

class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=_ROOT, **kwargs)
    def log_message(self, *_):
        pass  # silence request logs

def _start_server():
    with socketserver.TCPServer(("", _PORT), _Handler) as httpd:
        httpd.serve_forever()

# Start once per process; subsequent Streamlit re-runs skip this block.
if "http_server_started" not in st.session_state:
    t = threading.Thread(target=_start_server, daemon=True)
    t.start()
    st.session_state["http_server_started"] = True

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PeakForm – Treina. Evolui. Chega ao topo.",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome so only the landing page is visible
st.markdown(
    """
    <style>
    #MainMenu, header, footer { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    .stApp { background: #111111; }
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    section[data-testid="stMain"] > div { padding: 0 !important; }
    iframe { border: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Embed the landing page ─────────────────────────────────────────────────
# scrolling=True + tall height → iframe has its own scroll, position:fixed
# navbar stays at the top of the iframe as the user scrolls. UX is identical
# to opening index.html directly in the browser.
st.components.v1.iframe(
    f"http://localhost:{_PORT}/index.html",
    height=900,
    scrolling=True,
)
