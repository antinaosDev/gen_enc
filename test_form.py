import streamlit as st
import pandas as pd

st.title("Test")

with st.form("test_form"):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    edited = st.data_editor(df)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(edited)
