import html
import time

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Textno - Quản lý tài liệu",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Libre+Caslon+Text:wght@400;700&display=swap');

    :root {
        --ink: #18211d;
        --muted: #66716b;
        --line: #dce3df;
        --canvas: #f3f5f2;
        --panel: #ffffff;
        --brand: #174f3f;
        --brand-dark: #0e3c2e;
        --brand-soft: #e7f0eb;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: "DM Sans", sans-serif;
        color: var(--ink);
    }
    [data-testid="stAppViewContainer"] { background: var(--canvas); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainBlockContainer"] {
        max-width: 1280px;
        padding: 2.8rem 3rem 4rem;
    }
    [data-testid="stSidebar"] {
        background: #12382e;
        border-right: 0;
    }
    [data-testid="stSidebar"] > div:first-child { padding: 1.2rem 1rem; }
    [data-testid="stSidebar"] * { color: #eaf0ed; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #aac1b7; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.13); }

    .brand-wrap {
        padding: .4rem .55rem 1.35rem;
        border-bottom: 1px solid rgba(255,255,255,.13);
        margin-bottom: 1rem;
    }
    .brand-name {
        font-family: "Libre Caslon Text", serif;
        font-size: 1.65rem;
        letter-spacing: -.04em;
        color: #fff;
    }
    .brand-subtitle { margin-top: .3rem; font-size: .72rem; color: #aac1b7; }
    .system-card {
        margin-top: 2rem;
        padding: .9rem;
        border: 1px solid rgba(255,255,255,.14);
        border-radius: .75rem;
        background: rgba(255,255,255,.05);
        font-size: .72rem;
        line-height: 1.7;
        color: #c9d8d1;
    }
    .system-online { color: #8ad0ad; font-weight: 700; }

    [data-testid="stSidebar"] [role="radiogroup"] { gap: .35rem; }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: .68rem .75rem;
        border-radius: .65rem;
        transition: background .2s ease;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: rgba(255,255,255,.12);
    }

    .eyebrow {
        color: var(--brand);
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    .page-title {
        max-width: 850px;
        margin: .45rem 0 .65rem;
        font-family: "Libre Caslon Text", serif;
        font-size: clamp(2.35rem, 5vw, 3.65rem);
        font-weight: 400;
        line-height: 1.12;
        letter-spacing: -.055em;
        color: var(--ink);
    }
    .page-lead {
        max-width: 720px;
        margin-bottom: 1.6rem;
        color: var(--muted);
        font-size: .92rem;
        line-height: 1.7;
    }
    .section-title {
        margin: 1.7rem 0 .75rem;
        font-family: "Libre Caslon Text", serif;
        font-size: 1.45rem;
        font-weight: 400;
        letter-spacing: -.035em;
    }
    .results-meta {
        margin: -.4rem 0 .8rem;
        color: var(--muted);
        font-size: .72rem;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stDateInput"] input {
        border-color: var(--line);
        border-radius: .65rem;
        background: #fbfcfb;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--brand);
        box-shadow: 0 0 0 1px var(--brand);
    }
    div[data-testid="stForm"] {
        padding: 1.4rem;
        border: 1px solid var(--line);
        border-radius: .95rem;
        background: var(--panel);
        box-shadow: 0 8px 22px rgba(28,49,40,.04);
    }
    div[data-testid="stForm"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectSlider"] label {
        color: #3a4740 !important;
        font-size: .75rem;
        font-weight: 700;
    }
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        min-height: 2.65rem;
        border: 1px solid var(--line);
        border-radius: .65rem;
        color: var(--ink);
        background: #fff;
        font-weight: 700;
        transition: all .18s ease;
    }
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        border-color: var(--brand);
        color: var(--brand);
    }
    .stButton > button[kind="primary"],
    [data-testid="stFormSubmitButton"] > button[kind="primary"] {
        border-color: var(--brand);
        color: #fff;
        background: var(--brand);
    }
    .stButton > button[kind="primary"]:hover,
    [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
        border-color: var(--brand-dark);
        color: #fff;
        background: var(--brand-dark);
    }
    div[data-testid="stMetric"] {
        padding: 1.1rem;
        border: 1px solid var(--line);
        border-radius: .85rem;
        background: var(--panel);
        box-shadow: 0 8px 22px rgba(28,49,40,.04);
    }
    div[data-testid="stMetric"] label { color: var(--muted); font-size: .72rem; }
    div[data-testid="stMetricValue"] {
        font-family: "Libre Caslon Text", serif;
        font-size: 1.7rem;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: .75rem;
        overflow: hidden;
    }
    .result-card {
        min-height: 238px;
        padding: 1.15rem;
        border: 1px solid var(--line);
        border-radius: .9rem;
        background: var(--panel);
        box-shadow: 0 8px 22px rgba(28,49,40,.04);
    }
    .result-tag {
        color: var(--brand);
        font-size: .62rem;
        font-weight: 800;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    .result-card h3 {
        margin: .65rem 0 .55rem;
        font-family: "Libre Caslon Text", serif;
        font-size: 1.05rem;
        line-height: 1.35;
        letter-spacing: -.025em;
    }
    .result-card p {
        margin: 0;
        color: var(--muted);
        font-size: .72rem;
        line-height: 1.6;
    }
    .result-meta {
        margin-top: 1rem;
        padding-top: .7rem;
        border-top: 1px solid var(--line);
        color: var(--muted);
        font-size: .65rem;
    }
    .score { color: var(--brand); font-weight: 800; }
    .pipeline-note {
        margin: 1rem 0;
        padding: .75rem .9rem;
        border-left: 3px solid #d89a45;
        color: #66502f;
        background: #fff8e9;
        font-size: .72rem;
    }
    [data-testid="stExpander"] {
        border-color: var(--line);
        border-radius: .7rem;
        background: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def page_header(eyebrow: str, title: str, lead: str) -> None:
    st.markdown(
        f"""
        <div class="eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-lead">{lead}</div>
        """,
        unsafe_allow_html=True,
    )


def safe(value, fallback: str = "") -> str:
    return html.escape(str(value if value not in (None, "") else fallback))


with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-name">textno</div>
            <div class="brand-subtitle">Document Intelligence Workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Điều hướng",
        ["Tìm kiếm tài liệu", "Phân tích dữ liệu", "Thêm tài liệu"],
        label_visibility="collapsed",
    )
    st.markdown(
        """
        <div class="system-card">
            <b>Trạng thái hệ thống</b><br>
            <span class="system-online">● Hoạt động ổn định</span><br>
            MongoDB · FAISS Index<br>
            Cổng dữ liệu: Online
        </div>
        """,
        unsafe_allow_html=True,
    )


if page == "Tìm kiếm tài liệu":
    page_header(
        "Tìm kiếm tài liệu",
        "Tìm đúng nội dung,<br>không chỉ đúng từ khóa.",
        "Khám phá bài viết trong kho dữ liệu dựa trên chủ đề và ngữ cảnh. "
        "Kết quả được xếp hạng theo mức độ liên quan.",
    )

    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

    query_col, count_col = st.columns([4, 1])
    with query_col:
        query = st.text_input(
            "Nội dung tìm kiếm",
            value=st.session_state.query_input,
            placeholder="Ví dụ: Ứng dụng công nghệ trong giáo dục",
        )
    with count_col:
        top_k = st.select_slider(
            "Số kết quả",
            options=[1, 2, 3, 5],
            value=3,
        )

    search_clicked = st.button("Tìm kiếm", type="primary", width="stretch")

    st.markdown('<div class="section-title">Gợi ý chủ đề</div>', unsafe_allow_html=True)
    suggestions = [
        "Ứng dụng công nghệ trong giáo dục",
        "Biến động kinh tế và giá vàng",
        "Đội tuyển bóng đá quốc gia",
        "Khám phá sinh vật dưới biển sâu",
    ]
    suggestion_cols = st.columns(4)
    for index, suggestion in enumerate(suggestions):
        if suggestion_cols[index].button(suggestion, width="stretch"):
            st.session_state.query_input = suggestion
            st.rerun()

    if search_clicked:
        if not query:
            st.warning("Vui lòng nhập nội dung cần tìm kiếm.")
        else:
            start_time = time.time()
            try:
                response = requests.post(
                    f"{API_BASE}/search",
                    params={"query": query, "top_k": top_k},
                )
                if response.status_code == 200:
                    results = response.json()
                    latency = round(time.time() - start_time, 3)
                    st.markdown(
                        '<div class="section-title">Kết quả nổi bật</div>'
                        f'<div class="results-meta">{len(results)} tài liệu · {latency} giây</div>',
                        unsafe_allow_html=True,
                    )

                    result_cols = st.columns(min(len(results), 3) or 1)
                    for index, result in enumerate(results):
                        raw_tags = result.get("tags") or result.get("category") or "Chưa phân loại"
                        first_tag = (
                            raw_tags.split(",")[0]
                            if isinstance(raw_tags, str)
                            else "Chưa phân loại"
                        )
                        score = max(0.0, min(float(result.get("score", 0.0)), 1.0))
                        with result_cols[index % len(result_cols)]:
                            st.markdown(
                                f"""
                                <article class="result-card">
                                    <span class="result-tag">{safe(first_tag, "Chưa phân loại")}</span>
                                    <h3>{safe(result.get("title"), "Tài liệu chưa có tiêu đề")}</h3>
                                    <p>{safe(result.get("publication"), "VNExpress")} ·
                                    {safe(result.get("author"), "Ký giả")}</p>
                                    <div class="result-meta">
                                        {safe(result.get("created_at"), "Chưa rõ ngày")}
                                        · <span class="score">{round(score * 100)}% liên quan</span>
                                    </div>
                                </article>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.expander("Xem nội dung và điểm liên quan"):
                                st.write(result.get("content", ""))
                                if result.get("wordcount"):
                                    st.caption(f"Độ dài: {result['wordcount']} từ")
                                st.progress(score, text=f"Cosine similarity: {score:.3f}")
                else:
                    st.error("Không nhận được dữ liệu hợp lệ từ máy chủ.")
            except requests.RequestException:
                st.error("Không thể kết nối với máy chủ. Vui lòng kiểm tra Backend API.")


elif page == "Phân tích dữ liệu":
    page_header(
        "Phân tích dữ liệu",
        "Tổng quan kho tài liệu",
        "Theo dõi quy mô, chủ đề và trạng thái đồng bộ của nguồn dữ liệu.",
    )

    try:
        response = requests.get(f"{API_BASE}/documents")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            metric_cols = st.columns(4)
            metric_cols[0].metric("Tổng tài liệu", len(df))
            topic_column = "tags" if "tags" in df.columns else "category"
            metric_cols[1].metric(
                "Chủ đề độc lập",
                df[topic_column].nunique() if topic_column in df.columns else 0,
            )
            metric_cols[2].metric("Nguồn dữ liệu", "VNExpress")
            metric_cols[3].metric("Trạng thái chỉ mục", "Đồng bộ", delta="FAISS Ready")

            chart_col, table_col = st.columns([1, 1.35])
            with chart_col:
                st.markdown(
                    '<div class="section-title">Phân bổ theo chủ đề</div>',
                    unsafe_allow_html=True,
                )
                if topic_column in df.columns and not df.empty:
                    df["main_tag"] = df[topic_column].apply(
                        lambda value: (
                            value.split(",")[0].strip()
                            if isinstance(value, str)
                            else "Chưa phân loại"
                        )
                    )
                    figure = px.pie(
                        df,
                        names="main_tag",
                        hole=0.62,
                        color_discrete_sequence=[
                            "#174f3f",
                            "#5d8173",
                            "#9db5aa",
                            "#d89a45",
                            "#b8a890",
                            "#7d8c84",
                        ],
                    )
                    figure.update_layout(
                        margin=dict(l=10, r=10, t=10, b=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        legend=dict(orientation="h", y=-0.15),
                    )
                    st.plotly_chart(figure, width="stretch")
                else:
                    st.info("Chưa có dữ liệu chủ đề để hiển thị.")

            with table_col:
                st.markdown(
                    '<div class="section-title">Tài liệu cập nhật gần đây</div>',
                    unsafe_allow_html=True,
                )
                display_cols = [
                    column
                    for column in ["title", topic_column, "author", "created_at"]
                    if column in df.columns
                ]
                if display_cols:
                    st.dataframe(
                        df[display_cols].tail(8),
                        width="stretch",
                        hide_index=True,
                    )
                if st.button("Xem dữ liệu JSON", width="stretch"):
                    st.json(data)
        else:
            st.info("Cơ sở dữ liệu hiện đang trống.")
    except requests.RequestException:
        st.error("Không thể kết nối với máy chủ để tải dữ liệu phân tích.")


else:
    page_header(
        "Thêm tài liệu",
        "Tạo tài liệu mới",
        "Nhập nội dung và metadata. Sau khi lưu, tài liệu sẽ được đồng bộ vào "
        "chỉ mục tìm kiếm hiện tại.",
    )

    with st.form("entry_form", clear_on_submit=True):
        left_col, right_col = st.columns(2)
        with left_col:
            title = st.text_input("Tiêu đề *")
            author = st.text_input("Tác giả")
            publication = st.text_input("Nguồn xuất bản", value="VNExpress")
        with right_col:
            tags = st.text_input(
                "Chủ đề / Nhãn *",
                placeholder="Ví dụ: Công nghệ, Giáo dục",
            )
            updatetime = st.date_input("Ngày cập nhật")

        summary = st.text_area(
            "Nội dung chi tiết *",
            height=210,
            placeholder="Nhập nội dung tài liệu...",
        )
        st.markdown(
            '<div class="pipeline-note">Tài liệu mới sẽ được lưu vào MongoDB '
            "và đồng bộ với chỉ mục tìm kiếm FAISS.</div>",
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button(
            "Lưu tài liệu",
            type="primary",
            width="stretch",
        )

        if submitted:
            if title and summary and tags:
                payload = {
                    "title": title,
                    "author": author if author else "Ký giả VNExpress",
                    "publication": publication,
                    "tags": tags,
                    "updatetime": str(updatetime),
                    "wordcount": len(summary.split()),
                    "content": summary,
                }
                try:
                    response = requests.post(f"{API_BASE}/documents", json=payload)
                    if response.status_code in [200, 201]:
                        st.success(f"Đã lưu thành công tài liệu: “{title}”.")
                    else:
                        st.error(
                            "Máy chủ từ chối lưu dữ liệu "
                            f"(mã lỗi: {response.status_code})."
                        )
                except requests.RequestException:
                    st.error("Không thể kết nối đến máy chủ để lưu tài liệu.")
            else:
                st.warning("Vui lòng nhập đầy đủ các trường bắt buộc (*).")
