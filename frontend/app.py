import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px

# --- CẤU HÌNH HỆ THỐNG ---
API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Text Document Management System - VNExpress AI Search",
    page_icon="📄",
    layout="wide",
)

# --- CUSTOM CSS (Giao diện tone sáng, tối ưu hiển thị Metadata không bị dính chữ) ---
st.markdown(
    """
    <style>
    .main { background-color: #f4f6f9; }
    .stButton>button { width: 100%; border-radius: 20px; }
    
    /* Giao diện thẻ bài viết Semantic Match */
    .news-card {
        padding: 20px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 6px solid #008080;
    }
    
    /* Giao diện thẻ bài viết Keyword Match */
    .news-card-kw {
        padding: 20px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 6px solid #ff9800;
    }
    
    .category-tag {
        background-color: #e0f2f1;
        color: #004d40;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .category-tag-kw {
        background-color: #fff3e0;
        color: #e65100;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* Khung cấu trúc Metadata bóc tách riêng biệt chuyên nghiệp */
    .meta-line {
        font-size: 13px;
        color: #555555;
        margin-top: 12px;
        margin-bottom: 0px;
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
    }
    .meta-item {
        display: inline-flex;
        align-items: center;
    }
    
    .latency-text { color: #004d40; font-style: italic; font-size: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: THÔNG TIN HỆ THỐNG CHUẨN ENTERPRISE ---
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/2965/2965333.png" width="70">
            <h2 style="color: #008080; margin-top: 10px; font-size: 22px; font-weight: bold;">VNExpress AI Portal</h2>
            <p style="font-size: 12px; color: #666; font-style: italic;">Hệ thống Quản trị & Biên tập Tin tức</p>
        </div>
        <hr style="margin: 10px 0;">
    """,
        unsafe_allow_html=True,
    )

    st.info(
        "🧠 **AI Powered System**\n\nHệ quản trị dữ liệu văn bản phi cấu trúc và tìm kiếm ngữ nghĩa nâng cao trên nền tảng không gian Vector."
    )

    st.markdown(
        "<p style='font-weight: bold; color: #333; margin-top: 15px; margin-bottom: 5px; font-size: 13px;'>🌐 PHÂN QUYỀN HỆ THỐNG (ROLES)</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .role-box {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            background-color: #ffffff;
            border-radius: 6px;
            margin-bottom: 8px;
            border: 1px solid #eef2f5;
        }
        .role-dot { width: 8px; height: 8px; border-radius: 50%; background-color: #008080; margin-right: 10px; }
        .role-title { font-size: 12px; font-weight: 500; color: #444; }
        .infra-tag { font-size: 11px; color: #555; background-color: #eaeded; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    roles = [
        "System Administrator (Root)",
        "Data Engineer / NLP Specialist",
        "Frontend Developer (UI/UX)",
    ]
    for r in roles:
        st.markdown(
            f'<div class="role-box"><div class="role-dot"></div><div class="role-title">{r}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        "<br><p style='font-weight: bold; color: #333; margin-bottom: 5px; font-size: 13px;'>🛠️ THÔNG SỐ HẠ TẦNG (INFRA)</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "• Embedding: <span class='infra-tag'>all-MiniLM-L6-v2</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "• NoSQL CSDL: <span class='infra-tag'>MongoDB Atlas</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "• Vector DB: <span class='infra-tag'>FAISS CPU Index</span>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.success("Cổng truyền dữ liệu: **Online**")

# --- APP HEADER ---
st.title("📄 Text Document Management System")
st.write(
    "Hệ quản trị dữ liệu văn bản phi cấu trúc kết hợp Tìm kiếm ngữ nghĩa (Semantic Search)"
)

tab1, tab2, tab3 = st.tabs(
    ["🔍 Intelligent Search", "📊 Document Analytics", "➕ Add Document"]
)

# ==========================================
# TAB 1: INTELLIGENT SEARCH (KẾT NỐI API THẬT)
# ==========================================
with tab1:
    st.subheader("Trải nghiệm Sức mạnh Tìm kiếm Ngữ nghĩa AI")

    st.write("💡 **Gợi ý kịch bản Demo nhanh:**")
    cols = st.columns(4)
    suggestions = [
        "Ứng dụng trí tuệ nhân tạo trong học tập",
        "Biến động kinh tế thị trường và giá vàng",
        "Chiến thuật của đội tuyển bóng đá quốc gia",
        "Khám phá loài sinh vật mới dưới biển sâu",
    ]

    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion):
            st.session_state.query_input = suggestion

    query = st.text_input(
        "Nhập ý tưởng hoặc nhu cầu tìm kiếm tin tức của bạn:",
        value=st.session_state.query_input,
        placeholder="Ví dụ: Xu hướng phát triển công nghệ giáo dục thông minh hiện nay...",
    )

    col_search, col_k = st.columns([3, 1])
    with col_k:
        top_k = st.select_slider(
            "Số lượng kết quả hiển thị", options=[1, 2, 3, 5], value=3
        )

    if st.button("Tìm kiếm 🔍", type="primary"):
        if query:
            start_time = time.time()
            try:
                # GỌI API BACKEND: Thực hiện tìm kiếm kết hợp (Hybrid/Semantic)
                resp = requests.post(
                    f"{API_BASE}/search", params={"query": query, "top_k": top_k}
                )
                if resp.status_code == 200:
                    results = resp.json()
                    latency = round(time.time() - start_time, 3)

                    st.markdown(
                        f"⏱️ <span class='latency-text'>AI hoàn thành quét không gian vector trong {latency} giây</span>",
                        unsafe_allow_html=True,
                    )
                    col_left, col_right = st.columns(2)

                    # --- CỘT TRÁI: KEYWORD MATCH (TF-IDF) ---
                    with col_left:
                        st.markdown("### 🔍 Keyword Match (TF-IDF)")
                        st.caption("Tìm kiếm dựa trên từ khóa trùng khớp chính xác")
                        st.warning(
                            "Hạn chế: Tìm kiếm truyền thống dễ bỏ sót tài liệu nếu không gõ trúng chuẩn xác từng ký tự từ khóa gốc."
                        )
                        
                        for r in results:
                            with st.container():
                                raw_tags = r.get("tags", "General")
                                first_tag = raw_tags.split(",")[0] if isinstance(raw_tags, str) else "General"
                                
                                author = r.get('author') if r.get('author') else "Ký giả"
                                updatetime = r.get('updatetime') if r.get('updatetime') else "N/A"
                                publication = r.get('publication') if r.get('publication') else "VNExpress"
                                
                                st.markdown(
                                    f"""
                                    <div class="news-card-kw">
                                        <span class="category-tag-kw">{first_tag}</span>
                                        <h4 style="margin: 10px 0 4px 0; color:#e65100; font-size:16px; font-weight:bold;">{r['title']}</h4>
                                        <div class="meta-line">
                                            <span class="meta-item">✍️ <b>Tác giả:</b> {author}</span>
                                            <span class="meta-item">📅 <b>Cập nhật:</b> {updatetime}</span>
                                            <span class="meta-item">📰 <b>Nguồn:</b> {publication}</span>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                    # --- CỘT PHẢI: SEMANTIC MATCH (SBERT + FAISS) ---
                    with col_right:
                        st.markdown("### 🧠 Semantic Match (SBERT + FAISS)")
                        st.caption("Tìm kiếm dựa trên hiểu biết ngữ nghĩa cốt truyện")
                        
                        for r in results:
                            with st.container():
                                raw_tags = r.get("tags", "General")
                                first_tag = raw_tags.split(",")[0] if isinstance(raw_tags, str) else "General"
                                
                                author = r.get('author') if r.get('author') else "Ký giả"
                                updatetime = r.get('updatetime') if r.get('updatetime') else "N/A"
                                publication = r.get('publication') if r.get('publication') else "VNExpress"

                                st.markdown(
                                    f"""
                                    <div class="news-card">
                                        <span class="category-tag">{first_tag}</span>
                                        <h4 style="margin: 10px 0 4px 0; color:#008080; font-size:16px; font-weight:bold;">{r['title']}</h4>
                                        <div class="meta-line">
                                            <span class="meta-item">✍️ <b>Tác giả:</b> {author}</span>
                                            <span class="meta-item">📅 <b>Cập nhật:</b> {updatetime}</span>
                                            <span class="meta-item">📰 <b>Nguồn:</b> {publication}</span>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                with st.expander("Đọc toàn bộ nội dung & Kiểm tra Score"):
                                    st.write(r["content"])
                                    if r.get("wordcount"):
                                        st.caption(f"📝 Độ dài văn bản: {r['wordcount']} từ")
                                    
                                    score = r.get("score", 0.0)
                                    st.progress(
                                        max(0.0, min(float(score), 1.0)),
                                        text=f"Cosine Similarity Score: {score}",
                                    )
                else:
                    st.error("Lỗi phản hồi dữ liệu từ API Backend.")
            except:
                st.error(
                    "Không thể kết nối với Backend Server. Vui lòng đảm bảo server uvicorn FastAPI đang chạy."
                )
        else:
            st.warning("Vui lòng nhập nội dung cần tìm kiếm!")

# ==========================================
# TAB 2: DOCUMENT ANALYTICS (GỌI API GET TOÀN BỘ DATA)
# ==========================================
with tab2:
    st.subheader("Hệ thống Quản trị & Phân tích kho dữ liệu MongoDB")

    try:
        # GỌI API BACKEND: Kéo toàn bộ danh sách tài liệu từ MongoDB lên để thống kê
        resp = requests.get(f"{API_BASE}/documents")
        if resp.status_code == 200:
            data = resp.json()
            
            if data:
                df = pd.DataFrame(data)

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Tổng văn bản (Documents)", len(df))
                m2.metric(
                    "Nhãn độc lập (Tags Unique)",
                    df["tags"].nunique() if "tags" in df.columns else 0,
                )
                m3.metric("Nguồn Dataset", "VNExpress (Kaggle)")
                m4.metric("Dữ liệu Vector Space", "Đồng bộ", delta="FAISS Ready")

                st.write("---")
                col_chart, col_table = st.columns([1, 1])

                with col_chart:
                    st.write("**Tỷ lệ phân bổ tài liệu theo Nhãn chính (Tags)**")
                    if "tags" in df.columns:
                        df["main_tag"] = df["tags"].apply(
                            lambda x: (
                                x.split(",")[0].strip() if isinstance(x, str) else "General"
                            )
                        )
                        fig = px.pie(
                            df,
                            names="main_tag",
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Safe,
                        )
                        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
                        st.plotly_chart(fig, use_container_width=True)

                with col_table:
                    st.write("**Danh sách văn bản mới cập nhật**")
                    display_cols = [
                        c
                        for c in ["title", "tags", "author", "updatetime"]
                        if c in df.columns
                    ]
                    st.dataframe(df[display_cols].tail(5), use_container_width=True, hide_index=True)
                    if st.button("Xem cấu trúc JSON thô (MongoDB BSON)"):
                        st.json(data)
            else:
                st.info("Cơ sở dữ liệu MongoDB hiện đang trống. Pipeline đang chờ nạp dataset hoặc thêm thủ công.")
        else:
            st.error(f"Backend phản hồi mã lỗi: {resp.status_code}")
    except:
        st.error(
            "Backend offline. Vui lòng kích hoạt API Server để hiển thị biểu đồ phân tích thực tế."
        )

# ==========================================
# TAB 3: ADD DOCUMENT (GỌI API POST ĐỒNG BỘ)
# ==========================================
with tab3:
    st.subheader("Thêm Tài liệu Văn bản & Kích hoạt Vector Embedding")

    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Tiêu đề bài báo *")
            author = st.text_input("Tác giả")
            publication = st.text_input(
                "Nguồn xuất bản (Publication)", value="VNExpress"
            )
        with c2:
            tags = st.text_input(
                "Từ khóa / Nhãn (Tags) *", placeholder="Ví dụ: Công nghệ, AI, Giáo dục"
            )
            updatetime = st.date_input("Ngày cập nhật")

        summary = st.text_area(
            "Nội dung chi tiết bài viết (Dữ liệu văn bản phi cấu trúc) *", height=180
        )
        submitted = st.form_submit_button(
            "Lưu Tài Liệu & Đồng Bộ AI Index", type="primary"
        )

        if submitted:
            if title and summary and tags:
                word_count = len(summary.split())
                payload = {
                    "title": title,
                    "author": author if author else "Ký giả VNExpress",
                    "publication": publication,
                    "tags": tags,
                    "updatetime": str(updatetime),
                    "wordcount": word_count,
                    "content": summary,
                }
                try:
                    # GỌI API BACKEND: Đẩy bài viết mới lên MongoDB và tự động sinh Vector đưa vào FAISS
                    res = requests.post(f"{API_BASE}/documents", json=payload)
                    if res.status_code in [200, 201]:
                        st.balloons()
                        st.success(
                            f"Đã lưu thành công bài báo: '{title}'. Pipeline đã hoàn thành trích xuất Vector Embedding!"
                        )
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(
                            f"Backend từ chối nạp dữ liệu (Mã lỗi: {res.status_code})"
                        )
                except:
                    st.error(
                        "Không thể kết nối đến API Endpoint. Vui lòng kiểm tra cổng mạng của Backend Server."
                    )
            else:
                st.warning("Vui lòng nhập đầy đủ các trường dữ liệu bắt buộc (*)")