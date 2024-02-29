import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

page = st.sidebar.selectbox("Explorer ou Prédire", ("Prédire", "Explorer"))

if page == "Prédire":
    show_predict_page()
else:
    show_explore_page()



