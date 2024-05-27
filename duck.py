import duckdb
import streamlit as st

st.title("Duck DB with streamlit :duck:")

if "db" not in st.session_state:
    st.session_state["db"] = "./warehouse/dbt.duckdb"

st.header(f"duckdb path : `{st.session_state['db']}`")


@st.cache_resource
def get_cursor():
    conn = duckdb.connect(st.session_state["db"])
    cursor = conn.cursor()
    return cursor


@st.cache_data
def get_df(cursor, query):
    cursor.execute(query)
    df = cursor.fetch_df()
    return df


with st.form(key="query_form"):
    query = st.text_area(label="query")
    submitted = st.form_submit_button("Enter")
    if submitted:
        if query[-1] != ";":
            query += ";"
        try:
            st.write(query)
            cursor = get_cursor()
            cursor.execute(query)
            df = cursor.fetch_df()
            st.write(df)
        except Exception as e:
            st.write(e)
