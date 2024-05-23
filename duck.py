import duckdb
import streamlit as st

if "db" not in st.session_state:
    st.session_state["db"] = ":memory:"

@st.cache_resource
def get_cursor():
    conn = duckdb.connect(st.session_state["db"])
    cursor = conn.cursor()
    return cursor

cursor = get_cursor()
with st.form(key="query_form"):
    query = st.text_area(label="query")
    submitted = st.form_submit_button("Enter")
    if submitted:
        if query[-1] != ';':
            query += ';'
        try:
            st.write(query)
            cursor.sql(query)
            df = cursor.df()
            st.write(df)
        except Exception as e:
            st.write(e)
