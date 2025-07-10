import streamlit as st
import streamlit as st

st.set_page_config(layout="wide")
st.title("Points needed to win matches at Wimbledon 2025")

st.info("Select page:")
st.page_link("pages/01_matches.py", label="Matches - Points from victory by match", icon="🎾")
st.page_link("pages/02_players.py", label="Players - Points from victory by player", icon="🧍")
