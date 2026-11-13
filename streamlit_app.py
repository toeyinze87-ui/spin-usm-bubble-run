from pathlib import Path
import streamlit as st
from site_content import load_content, render
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title="SPIN USM Bubble Run 2027",page_icon="🫧",layout="wide")
st.html("<style>"+(ROOT/"style.css").read_text()+"</style>")

@st.fragment(run_every="30s")
def website():
    try:
        content=load_content()
        markup=render(content)
        st.session_state["last_valid_page"]=markup
    except (OSError,ValueError,KeyError,TypeError) as exc:
        if "last_valid_page" in st.session_state:
            st.warning("An update is being prepared. Showing the last available version.")
            markup=st.session_state["last_valid_page"]
        else:
            st.error("The site is temporarily unavailable. Please check back shortly.")
            # Details go to the server logs, not the public page.
            print("Content validation error:",str(exc))
            return
    st.html(markup)
website()
