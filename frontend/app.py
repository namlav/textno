import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Text Document Management System",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Text Document Management System")
st.markdown("Hệ thống quản lý và tìm kiếm tài liệu văn bản phi cấu trúc")

tab1, tab2, tab3 = st.tabs(["🔍 Search", "📋 Documents", "➕ Add Document"])

with tab1:
    st.header("Semantic Search")
    query = st.text_input("Enter your search query:", placeholder="e.g. machine learning")
    top_k = st.slider("Number of results", 1, 20, 5)

    if st.button("Search") and query:
        with st.spinner("Searching..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/search",
                    params={"query": query, "top_k": top_k},
                    timeout=30,
                )
                if resp.status_code == 200:
                    results = resp.json()
                    if results:
                        st.subheader(f"Found {len(results)} results")
                        for i, r in enumerate(results, 1):
                            with st.container(border=True):
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    st.markdown(f"**{i}. {r['title']}**")
                                    content = r.get("content", "")
                                    preview = content[:300] + "..." if len(content) > 300 else content
                                    st.markdown(f"_{preview}_")
                                    if r.get("category"):
                                        st.caption(f"Category: {r['category']}")
                                with col2:
                                    score_pct = round(r["score"] * 100, 1)
                                    st.metric("Score", f"{score_pct}%")
                    else:
                        st.info("No results found.")
                else:
                    st.error(f"API error: {resp.text}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Make sure the API server is running.")

with tab2:
    st.header("All Documents")
    try:
        resp = requests.get(f"{API_BASE}/documents", timeout=30)
        if resp.status_code == 200:
            docs = resp.json()
            if docs:
                df = pd.DataFrame(docs)
                display_cols = ["title", "category", "created_at"]
                available = [c for c in display_cols if c in df.columns]
                st.dataframe(df[available], use_container_width=True)
            else:
                st.info("No documents in the database.")
        else:
            st.error(f"API error: {resp.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend.")

with tab3:
    st.header("Add New Document")
    with st.form("add_doc_form"):
        title = st.text_input("Title")
        content = st.text_area("Content", height=200)
        category = st.text_input("Category (optional)")
        author = st.text_input("Author (optional)")
        submitted = st.form_submit_button("Add Document")

        if submitted:
            if not title or not content:
                st.error("Title and content are required.")
            else:
                payload = {
                    "title": title,
                    "content": content,
                    "category": category or None,
                    "author": author or None,
                }
                try:
                    resp = requests.post(f"{API_BASE}/documents", json=payload, timeout=30)
                    if resp.status_code == 200:
                        st.success("Document added successfully!")
                    else:
                        st.error(f"Error: {resp.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend.")
