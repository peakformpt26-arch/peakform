import streamlit as st
import os
from PIL import Image

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ICON = os.path.join(_ROOT, "input", "PeakForm Icon.png")

st.set_page_config(
    page_title="PeakForm — Train. Evolve. Perform Better.",
    page_icon=Image.open(_ICON),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide all Streamlit chrome — full-screen SPA
st.markdown("""
<style>
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.stApp {
  background: #111111 !important;
  margin: 0; padding: 0;
  overflow: hidden;
}
.block-container {
  padding: 0 !important;
  max-width: 100% !important;
  margin: 0 !important;
}
section[data-testid="stMain"] { padding: 0 !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="stVerticalBlock"] > div {
  margin: 0 !important;
  padding: 0 !important;
}
.element-container { margin: 0 !important; padding: 0 !important; }

/* Force iframe to fill full viewport */
iframe {
  border: none !important;
  height: 100vh !important;
  width: 100vw !important;
  display: block !important;
}
</style>
""", unsafe_allow_html=True)

_html_path = os.path.join(_ROOT, "peakform_premium.html")

if not os.path.exists(_html_path):
    st.error("Ficheiro peakform_premium.html não encontrado. Corre o build script primeiro.")
    st.stop()

with open(_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=900, scrolling=True)
