import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. CẤU HÌNH TRANG CHUẨN ĐỒ ÁN ---
st.set_page_config(
    page_title="VNExpress AI Portal - Mock Design System",
    page_icon="📄",
    layout="wide",
)

# --- 2. KHO DỮ LIỆU GIẢ LẬP LỚN (MOCK DATABASE TRÊN RAM) ---
# Đảm bảo cấu trúc khớp 100% với file sample_dataset.csv thực tế
if 'mock_db' not in st.session_state:
    st.session_state.mock_db = [
        {"id": 1, "title": "AI đang thay đổi toàn diện phương thức học tập của sinh viên kỹ thuật", "updatetime": "2026-05-20", "wordcount": 450, "publication": "VNExpress", "tags": "Công nghệ, AI", "content": "Trí tuệ nhân tạo đóng vai trò quan trọng trong việc cá nhân hóa lộ trình học tập. Hệ thống AI có khả năng tự động phân tích lỗ hổng kiến thức, đề xuất bài tập tối ưu và trợ giúp sinh viên công nghệ lập trình hiệu quả hơn nhờ các mô hình ngôn ngữ lớn.", "score": 0.92},
        {"id": 2, "title": "Bùng nổ làn sóng tích hợp Agentic AI vào quản trị doanh nghiệp nội địa", "updatetime": "2026-05-22", "wordcount": 580, "publication": "VNExpress", "tags": "Công nghệ, AI Agent", "content": "Thay vì các chatbot phản hồi thụ động, các hệ thống Multi-Agent System (MAS) tự chủ đang được triển khai mạnh mẽ. Các tác tử AI có khả năng tự phân rã mục tiêu lớn, phối hợp liên phòng ban để tự động hóa quy trình vận hành phức tạp.", "score": 0.88},
        {"id": 3, "title": "Hạ tầng đám mây dịch chuyển mạnh mẽ sang kiến trúc phi tập trung", "updatetime": "2026-05-18", "wordcount": 410, "publication": "TechInsight", "tags": "Công nghệ, Hạ tầng mạng", "content": "Sự trỗi dậy của điện toán biên (Edge Computing) đang làm giảm sự phụ thuộc vào các trung tâm dữ liệu tập trung lớn. Giải pháp này giúp tối ưu hóa băng thông, giảm thiểu độ trễ phản hồi và tăng cường bảo mật thông tin lớp đầu cuối.", "score": 0.74},
        {"id": 4, "title": "Thị trường vàng biến động mạnh trước áp lực lạm phát toàn cầu", "updatetime": "2026-05-21", "wordcount": 380, "publication": "VNExpress", "tags": "Kinh tế, Vàng", "content": "Giá vàng miếng liên tục lập đỉnh mới trước áp lực lạm phát toàn cầu và biến động địa chính trị. Các nhà đầu tư trong nước có xu hướng dịch chuyển dòng vốn sang các kênh trú ẩn an toàn, khiến khối lượng giao dịch tăng đột biến.", "score": 0.85},
        {"id": 5, "title": "Xuất khẩu nông sản Việt Nam lập kỷ lục mới trong quý II năm 2026", "updatetime": "2026-05-25", "wordcount": 520, "publication": "VnEconomy", "tags": "Kinh tế, Xuất nhập khẩu", "content": "Nhờ ứng dụng quy trình trồng trọt đạt chuẩn kỹ thuật số và chuyển đổi chuỗi cung ứng xanh, các mặt hàng nông sản chủ lực như sầu riêng, gạo và cà phê liên tục mở rộng thị phần tại các thị trường khó tính như EU, Mỹ và Nhật Bản.", "score": 0.79},
        {"id": 6, "title": "Lãi suất ngân hàng có xu hướng hạ nhiệt nhằm kích cầu tiêu dùng nội địa", "updatetime": "2026-05-24", "wordcount": 340, "publication": "Thời báo Tài chính", "tags": "Kinh tế, Ngân hàng", "content": "Ngân hàng Nhà nước vừa ban hành văn bản điều chỉnh giảm lãi suất điều hành. Động thái này được kỳ vọng sẽ hỗ trợ đắc lực cho các doanh nghiệp vừa và nhỏ tiếp cận nguồn vốn giá rẻ để phục hồi và mở rộng sản xuất kinh doanh.", "score": 0.71},
        {"id": 7, "title": "Đội tuyển Việt Nam thử nghiệm sơ đồ chiến thuật mới cho vòng loại châu Á", "updatetime": "2026-05-22", "wordcount": 490, "publication": "VNExpress", "tags": "Thể thao, Bóng đá", "content": "Ban huấn luyện đã áp dụng thử nghiệm sơ đồ linh hoạt 3-5-2 nhằm gia tăng mật độ kiểm soát bóng tại khu vực trung lộ. Lối chơi này đòi hỏi các tiền vệ biên phải có thể lực cực kỳ dồi dào để sẵn sàng chuyển trạng thái từ thủ sang công.", "score": 0.82}
    ]

# --- 3. CUSTOM CSS HIỆN ĐẠI (BO GÓC, ĐỔ BÓNG, HIGHLIGHT KHUNG) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* Giao diện thẻ bài viết tinh tế */
    .custom-card {
        padding: 16px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        border-left: 5px solid #008080;
    }
    .custom-card-kw {
        padding: 14px;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 10px;
        border-left: 5px solid #ff9800;
    }
    
    /* Nhãn danh mục nhỏ xinh */
    .category-badge {
        background-color: #e0f2f1;
        color: #004d40;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
    }
    
    /* Khung hiển thị chi tiết bên phải */
    .detail-container {
        padding: 24px;
        border-radius: 12px;
        background-color: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        min-height: 480px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR CHỨA TRẠNG THÁI HỆ THỐNG ĐỘNG ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 15px;">
            <h2 style="color: #008080; margin-top: 10px; font-size: 24px; font-weight: bold;">VNExpress AI</h2>
            <p style="font-size: 12px; color: #666; font-style: italic;">Hệ quản trị & Tìm kiếm ngữ nghĩa văn bản</p>
        </div>
        <hr style="margin: 10px 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-weight: bold; font-size: 13px; color: #333;'>⚙️ TRẠNG THÁI HẠ TẦNG (INFRA)</p>", unsafe_allow_html=True)
    st.success("🟢 Connected to MongoDB Atlas")
    st.success("🟢 FAISS Vector Index: Ready")
    
    st.markdown("<br><p style='font-weight: bold; font-size: 13px; color: #333;'>📊 LƯU TRỮ HỆ THỐNG</p>", unsafe_allow_html=True)
    # Giả lập thanh dung lượng bộ nhớ lưu trữ giống các app lớn
    current_docs = len(st.session_state.mock_db)
    st.progress(current_docs / 50, text=f"{current_docs} / 50 Tài liệu mẫu đã nạp")
    st.caption("Model nhúng: `all-MiniLM-L6-v2` (384 Dimensions)")
    st.markdown("---")
    st.warning("Chế độ: **Thiết kế giả lập (Mock UI)**")

# --- 5. TIÊU ĐỀ CHÍNH ---
st.title("📄 Text Document Management System")
st.write("Hệ thống quản trị tài liệu phi cấu trúc kết hợp đối sánh Thuật toán Tìm kiếm")

tab1, tab2, tab3 = st.tabs(["🔍 Intelligent Search", "📊 Document Analytics", "➕ Add Document"])

# ==========================================
# TAB 1: INTELLIGENT SEARCH (BỐ CỤC ĐỐI SÁNH SỬA LỖI STATE)
# ==========================================
with tab1:
    st.subheader("Trải nghiệm Sức mạnh Tìm kiếm Ngữ nghĩa AI")
    
    st.write("💡 **Gợi ý kịch bản Demo nhanh (Click để tìm kiếm ngay lập tức):**")
    cols = st.columns(3)
    suggestions = [
        "Ứng dụng trí tuệ nhân tạo trong học tập", 
        "Biến động kinh tế thị trường và giá vàng", 
        "Chiến thuật của đội tuyển bóng đá quốc gia"
    ]
    
    if 'current_query' not in st.session_state:
        st.session_state.current_query = ""
    auto_search = False

    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state.current_query = suggestion
            auto_search = True

    query = st.text_input("Nhập ý tưởng hoặc nhu cầu tìm kiếm tin tức của bạn:", 
                          value=st.session_state.current_query,
                          placeholder="Ví dụ: Xu hướng phát triển công nghệ trí tuệ nhân tạo hiện nay...")
    
    if query != st.session_state.current_query:
        st.session_state.current_query = query

    col_search, col_k = st.columns([3, 1])
    with col_k:
        top_k = st.select_slider("Số lượng kết quả hiển thị tối đa", options=[1, 2, 3, 5], value=3)

    if col_search.button("Kích hoạt AI Search", type="primary", use_container_width=True) or auto_search:
        if st.session_state.current_query:
            start_time = time.time()
            time.sleep(0.3)  # Giả lập độ trễ xử lý vector của AI
            latency = round(time.time() - start_time, 3)
            
            st.markdown(f"⏱️ <span style='color:#004d40; font-style:italic; font-size:13px;'>AI hoàn thành quét không gian vector trong {latency} giây (Simulated)</span>", unsafe_allow_html=True)
            
            # --- CHIA KHUNG LƯỚI ĐỐI SÁNH: TRÁI (KEYWORD) VS PHẢI (SEMANTIC) ---
            col_left, col_right = st.columns(2)
            
            # Phân tách từ khóa phục vụ cột Keyword
            keywords = [w.lower().strip() for w in st.session_state.current_query.split() if len(w) >= 2]
            
            # --- CỘT TRÁI: KEYWORD MATCH (LỌC CHÍNH XÁC KÝ TỰ CÓ TRONG BÀI) ---
            with col_left:
                st.markdown("### 🔍 Keyword Match (TF-IDF)")
                st.caption("Tìm kiếm dựa trên từ khóa trùng khớp chính xác")
                st.warning("Hạn chế: Dễ bỏ sót hoặc hiển thị sai lệch nếu từ khóa không khớp hoàn toàn ngữ cảnh.")
                
                kw_matches = []
                for r in st.session_state.mock_db:
                    text_to_search = (r['title'] + " " + r['content'] + " " + r['tags']).lower()
                    if any(kw in text_to_search for kw in keywords):
                        kw_matches.append(r)
                
                if not kw_matches:
                    st.info("ℹ️ Không tìm thấy bài viết nào chứa từ khóa trùng khớp chính xác.")
                else:
                    for r in kw_matches[:top_k]:
                        st.markdown(f"""
                        <div class="custom-card-kw">
                            <h5 style="margin:0 0 5px 0; color:#333; font-size:15px;">{r['title']}</h5>
                            <small style="color:#666;">📰 Nguồn: {r['publication']} | Ngày: {r['updatetime']}</small>
                        </div>
                        """, unsafe_allow_html=True)

            # --- CỘT PHẢI: SEMANTIC MATCH (TÍNH TOÁN KHOẢNG CÁCH VECTOR) ---
            with col_right:
                st.markdown("### 🧠 Semantic Match (SBERT + FAISS)")
                st.caption("Tìm kiếm dựa trên hiểu biết ngữ nghĩa cốt truyện")
                
                semantic_scored_list = []
                for r in st.session_state.mock_db:
                    base_score = r['score']
                    current_q_lower = st.session_state.current_query.lower()
                    
                    # Mô phỏng tính khoảng cách ngữ nghĩa theo chủ đề gõ câu lệnh
                    if any(k in current_q_lower for k in ['vàng', 'giá', 'kinh tế', 'lãi suất', 'xuất khẩu']):
                        if any(t in r['tags'].lower() for t in ['kinh tế', 'vàng', 'xuất khẩu']):
                            base_score = max(0.85, base_score + 0.04)
                        else:
                            base_score = min(0.24, base_score - 0.4)
                            
                    elif any(k in current_q_lower for k in ['ai', 'công nghệ', 'agent', 'tác tử', 'mạng']):
                        if any(t in r['tags'].lower() for t in ['công nghệ', 'ai']):
                            base_score = max(0.88, base_score + 0.05)
                        else:
                            base_score = min(0.22, base_score - 0.4)
                            
                    elif any(k in current_q_lower for k in ['bóng đá', 'thể thao', 'chiến thuật']):
                        if 'thể thao' in r['tags'].lower():
                            base_score = max(0.84, base_score + 0.04)
                        else:
                            base_score = min(0.18, base_score - 0.4)
                    
                    r['dynamic_score'] = round(base_score, 3)
                    semantic_scored_list.append(r)
                
                # Sắp xếp theo score giảm dần
                semantic_scored_list = sorted(semantic_scored_list, key=lambda x: x['dynamic_score'], reverse=True)
                
                # Ngưỡng lọc điểm số (Score Thresholding) bảo vệ chất lượng hiển thị
                SCORE_THRESHOLD = 0.40
                valid_semantic_results = [r for r in semantic_scored_list if r['dynamic_score'] >= SCORE_THRESHOLD][:top_k]
                
                if not valid_semantic_results:
                    st.info("⚠️ Không tìm thấy kết quả nào có độ trùng khớp ngữ nghĩa đủ cao.")
                else:
                    for r in valid_semantic_results:
                        with st.container():
                            st.markdown(f"""
                            <div class="custom-card">
                                <span class="category-badge">{r['tags']}</span>
                                <h4 style="margin: 8px 0 6px 0; color:#008080; font-size:16px;">{r['title']}</h4>
                                <p style="color:#666; font-size:12px; margin:0;">📅 Cập nhật: {r['updatetime']} | 📰 Nguồn: {r['publication']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            with st.expander("Đọc toàn bộ văn bản & Kiểm tra Cosine Score"):
                                st.write(r['content'])
                                st.caption(f"📝 Độ dài văn bản: {r['wordcount']} từ")
                                st.progress(max(0.0, min(float(r['dynamic_score']), 1.0)), text=f"Cosine Similarity Score: {r['dynamic_score']}")
                                
                    # Báo cáo kết quả bị ẩn
                    total_matched = len([r for r in semantic_scored_list if r['dynamic_score'] >= SCORE_THRESHOLD])
                    if total_matched < top_k:
                        st.caption(f"💡 *Hệ thống tự động ẩn {top_k - total_matched} kết quả nhiễu có độ tương đồng thấp dưới {SCORE_THRESHOLD*100}% để đảm bảo độ chính xác.*")
        else:
            st.warning("Vui lòng nhập nội dung cần tìm kiếm!")

# ==========================================
# TAB 2: DOCUMENT ANALYTICS (NÂNG CẤP ĐA BIỂU ĐỒ TRỰC QUAN)
# ==========================================
with tab2:
    st.subheader("Hệ thống Phân tích & Thống kê Kho dữ liệu Tri thức")
    
    # Chuyển đổi toàn bộ mock_db sang DataFrame để xử lý dữ liệu biểu đồ
    df = pd.DataFrame(st.session_state.mock_db)
    
    # 1. Hàng Metrics báo cáo thông số nhanh trên cùng
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tổng số tài liệu hiện hành", len(df), delta="+1 bài báo mới")
    m2.metric("Không gian mẫu văn bản", f"{len(df)} BSON Docs", delta="MongoDB Atlas Synced")
    m3.metric("Tổng số từ vựng (Word Count)", f"{df['wordcount'].sum()} từ", delta="Đã số hóa")
    m4.metric("Thời gian phản hồi AI", "0.32 giây", delta="-0.05 giây (Nhanh)")
    
    st.write("---")
    
    # 2. HÀNG BIỂU ĐỒ 1: Chia đôi màn hình (Tròn & Cột)
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.write("**📊 Cơ cấu tỷ lệ tài liệu theo Nhãn (Tags)**")
        # Biểu đồ tròn phân tích cơ cấu danh mục
        fig_pie = px.pie(
            df, 
            names='tags', 
            hole=0.4, 
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with row1_col2:
        st.write("**📈 Tần suất bài báo theo Nguồn phát hành (Publication)**")
        # Biểu đồ cột đếm số lượng tài liệu theo từng nguồn báo
        df_pub_count = df['publication'].value_counts().reset_index()
        df_pub_count.columns = ['publication', 'count']
        
        fig_bar = px.bar(
            df_pub_count, 
            x='publication', 
            y='count', 
            color='publication',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.write("---")
    
    # 3. HÀNG BIỂU ĐỒ 2 & BẢNG DỮ LIỆU: Chia đôi màn hình (Đường xu hướng & Bảng Metadata)
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.write("**📅 Xu hướng cập nhật tài liệu theo thời gian**")
        # Gom nhóm dữ liệu theo ngày để vẽ biểu đồ đường (Line Chart) tiến độ tích hợp hệ thống
        df_time = df.groupby('updatetime').size().reset_index(name='Số lượng')
        df_time = df_time.sort_values('updatetime')
        
        fig_line = px.line(
            df_time, 
            x='updatetime', 
            y='Số lượng', 
            markers=True,
            color_discrete_sequence=['#008080']
        )
        fig_line.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=260)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with row2_col2:
        st.write("**📋 Danh sách các tài liệu mới đồng bộ**")
        # Hiển thị bảng danh mục dữ liệu thô rút gọn bên cạnh biểu đồ xu hướng
        st.dataframe(
            df[['id', 'title', 'tags', 'publication', 'wordcount']], 
            use_container_width=True, 
            hide_index=True,
            height=260
        )

# ==========================================
# TAB 3: ADD DOCUMENT (MOCK STORAGE IN RAM)
# ==========================================
with tab3:
    st.subheader("Thêm Tài liệu Văn bản & Kích hoạt Pipeline Vector")
    
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Tiêu đề bài viết *")
            publication = st.text_input("Nguồn xuất bản", value="VNExpress")
        with c2:
            tags = st.selectbox("Chọn nhãn phân loại chính *", ["Công nghệ, AI", "Kinh tế, Vàng", "Thể thao, Bóng đá"])
            updatetime = st.date_input("Ngày cập nhật hệ thống")
            
        summary = st.text_area("Toàn văn nội dung tài liệu phi cấu trúc *", height=150)
        
        submitted = st.form_submit_button("Lưu Tài Liệu & Đồng Bộ AI Index", type="primary")
        
        if submitted:
            if title and summary:
                word_count = len(summary.split())
                
                new_doc = {
                    "id": len(st.session_state.mock_db) + 1,
                    "title": title, 
                    "publication": publication,
                    "tags": tags, 
                    "updatetime": str(updatetime), 
                    "wordcount": word_count,
                    "content": summary,
                    "score": 0.82
                }
                
                st.session_state.mock_db.append(new_doc)
                st.balloons()
                st.success(f"🎉 Đã lưu thành công! Hệ thống giả lập đã nhúng Vector Embedding và đồng bộ vào bộ chỉ mục RAM Space!")
            else:
                st.warning("Vui lòng điền đầy đủ các thông tin bắt buộc (*)")