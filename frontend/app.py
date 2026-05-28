# app.py — AI Semantic Search Dashboard (Enhanced UI)

import streamlit as st
import pandas as pd
import time

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SemanticAI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0F172A;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1E293B;
}

.block-container {
    padding-top: 2rem;
}

.hero-box {
    background: linear-gradient(
        135deg,
        #1E293B,
        #0F172A
    );
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid #334155;
    margin-bottom: 2rem;
}

.metric-card {
    background-color: #111827;
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid #1E293B;
    text-align: center;
}

.result-card {
    background-color: #111827;
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid #1E293B;
    margin-bottom: 1rem;
}

.tag {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    background-color: #1E293B;
    margin-right: 0.5rem;
    margin-top: 0.5rem;
    font-size: 0.8rem;
}

.score-box {
    background: linear-gradient(
        90deg,
        #06B6D4,
        #8B5CF6
    );
    padding: 0.4rem 1rem;
    border-radius: 999px;
    color: white;
    font-weight: bold;
    display: inline-block;
}

.search-box {
    background-color: #111827;
    border-radius: 20px;
    padding: 1rem;
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🧠 SemanticAI")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Semantic Search",
        "Documents",
        "Analytics",
        "Architecture"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
Current Model:
Sentence-BERT
""")

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.markdown("""
    <div class="hero-box">
        <h1>🚀 AI Semantic Search Dashboard</h1>
        <p>
        Search documents using semantic understanding
        instead of keyword matching.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>5,204</h2>
            <p>Total Documents</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>5,204</h2>
            <p>Embeddings</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>0.12s</h2>
            <p>Search Latency</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>91%</h2>
            <p>Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📌 System Stack")

    st.success("""
    FastAPI + MongoDB + FAISS + Sentence-BERT + Streamlit
    """)

# =====================================================
# SEMANTIC SEARCH
# =====================================================

elif menu == "Semantic Search":

    st.markdown("""
    <div class="hero-box">
        <h1>🔍 Semantic Search</h1>
        <p>
        Find documents by meaning, not exact keywords.
        </p>
    </div>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Search documents by meaning..."
    )

    col1, col2 = st.columns(2)

    with col1:
        method = st.radio(
            "Search Method",
            [
                "Sentence-BERT",
                "TF-IDF"
            ]
        )

    with col2:
        top_k = st.slider(
            "Top-K Results",
            1,
            10,
            5
        )

    if st.button("🚀 Run Semantic Search"):

        with st.spinner("Searching semantic space..."):
            time.sleep(1)

        results = [
            {
                "title": "Doraemon",
                "score": 0.91,
                "content": "Mèo máy đến từ tương lai.",
                "tags": ["robot", "manga", "kids"]
            },
            {
                "title": "Naruto",
                "score": 0.84,
                "content": "Ninja trẻ tuổi với ước mơ trở thành Hokage.",
                "tags": ["ninja", "anime"]
            },
            {
                "title": "Sherlock Holmes",
                "score": 0.78,
                "content": "Tiểu thuyết trinh thám nổi tiếng.",
                "tags": ["detective", "novel"]
            }
        ]

        st.markdown("---")

        st.subheader("📚 Search Results")

        for item in results[:top_k]:

            tags_html = ""

            for tag in item["tags"]:
                tags_html += f'''
                <span class="tag">
                    #{tag}
                </span>
                '''

            st.markdown(f"""
            <div class="result-card">

                <h2>📘 {item["title"]}</h2>

                <div class="score-box">
                    Similarity Score: {item["score"]}
                </div>

                <br><br>

                <p>{item["content"]}</p>

                {tags_html}

            </div>
            """, unsafe_allow_html=True)

# =====================================================
# DOCUMENTS PAGE
# =====================================================

elif menu == "Documents":

    st.markdown("""
    <div class="hero-box">
        <h1>📚 Document Management</h1>
        <p>
        Manage unstructured documents and datasets.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_document"):

        title = st.text_input("Document Title")

        content = st.text_area(
            "Document Content"
        )

        tags = st.text_input(
            "Tags (comma separated)"
        )

        submit = st.form_submit_button(
            "➕ Add Document"
        )

        if submit:

            st.success(
                "Document added successfully!"
            )

    st.markdown("---")

    st.subheader("📄 Existing Documents")

    docs = pd.DataFrame({
        "Title": [
            "Doraemon",
            "Naruto",
            "Sherlock Holmes"
        ],
        "Category": [
            "Manga",
            "Anime",
            "Novel"
        ]
    })

    st.dataframe(
        docs,
        use_container_width=True
    )

# =====================================================
# ANALYTICS
# =====================================================

elif menu == "Analytics":

    st.markdown("""
    <div class="hero-box">
        <h1>📊 Search Analytics</h1>
        <p>
        Monitor semantic search performance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    chart_data = pd.DataFrame({
        "Searches": [10, 20, 15, 35, 50]
    })

    st.line_chart(chart_data)

    st.markdown("---")

    st.subheader("🔥 Top Search Keywords")

    st.write("""
    - robot
    - ninja
    - AI
    - detective
    """)

# =====================================================
# ARCHITECTURE
# =====================================================

elif menu == "Architecture":

    st.markdown("""
    <div class="hero-box">
        <h1>🏗️ System Architecture</h1>
        <p>
        End-to-end semantic retrieval pipeline.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""
User Query
    ↓
Preprocessing
    ↓
Sentence-BERT Embedding
    ↓
FAISS Vector Search
    ↓
MongoDB Retrieval
    ↓
Top-K Results
    """)
