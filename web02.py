import pandas as pd
import streamlit as st
import random

# Đọc dữ liệu từ file Excel
file = st.file_uploader("Chọn file Excel", type=["xlsx", "xls"])

# Thêm CSS tùy chỉnh để định vị văn bản theo tọa độ
st.markdown("""
    <style>
        .positioned-text {
            position: absolute;
            font-size: 80px;  /* Cỡ chữ */
            color: #4CAF50;   /* Màu xanh lá */
        }
        .details-text {
            position: absolute;
            font-size: 30px;  /* Cỡ chữ */
            color: #FF5733;   /* Màu cam */
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 100px; /* Khoảng cách trên */
        }
    </style>
""", unsafe_allow_html=True)

if file is not None:
    # Đọc dữ liệu từ sheet đầu tiên chỉ một lần khi file được tải lên
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_excel(file)

    # Thay thế giá trị NaN bằng chuỗi rỗng trong DataFrame
    st.session_state.df = st.session_state.df.fillna("")

    # Kiểm tra xem các cột "Từ vựng", "Âm hán việt", "Hiragana", "Nghĩa" có tồn tại không
    required_columns = ['Từ vựng', 'Âm hán việt', 'Hiragana', 'Nghĩa']
    if all(col in st.session_state.df.columns for col in required_columns):
        # Khởi tạo index mặc định nếu chưa có trong session_state
        if 'index' not in st.session_state:
            st.session_state.index = 0

        # Hiển thị từ vựng tại vị trí x, y được chỉ định
        vocab_x, vocab_y = 100, 50  # Tọa độ (x, y) cho từ vựng
        details_x, details_y = 100, 150  # Tọa độ (x, y) cho thông tin chi tiết
        st.markdown(
            f"""
            <div class='details-text' 
                style='position: absolute; 
                    left: 50%; 
                    top: {details_y - 100}px; 
                    transform: translateX(-50%); 
                    text-align: center; 
                    font-size: 45px; 
                    color: #4CAF50; 
                    font-weight: bold;
                    white-space: nowrap;   /* Ngăn chữ xuống dòng */
                    overflow: hidden;      /* Ẩn văn bản bị tràn */
                    text-overflow: ellipsis; /* Hiển thị "..." nếu văn bản bị tràn */
                    width: auto;  /* Đảm bảo chiều rộng của phần tử đủ lớn */
                    max-width: 100%; /* Đảm bảo không vượt quá chiều rộng của container */
            '>
                {st.session_state.df['Từ vựng'][st.session_state.index]}
            </div>
            """,
            unsafe_allow_html=True
        )
        for _ in range(8):
            st.write("")
        col, col1, col2, col3,  = st.columns([0.8, 0.5, 0.7, 1])
        with col1:
            if st.button("←", key="prev_btn"):
                if st.session_state.index > 0:
                    st.session_state.index -= 1
                st.experimental_rerun()
        with col2:
            if st.button("Random", key="random_btn"):
                st.session_state.index = random.randint(0, len(st.session_state.df['Từ vựng']) - 1)
                st.experimental_rerun()
        with col3:
            if st.button("→", key="next_btn"):
                if st.session_state.index < len(st.session_state.df['Từ vựng']) - 1:
                    st.session_state.index += 1
                st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        col, col1, col2, col3,  = st.columns([0.8, 0.5, 0.7, 1])
        with col2:
            # Hiển thị thông tin chi tiết tại vị trí cụ thể khi lật card
            button = st.button("Lật card", key="flip_btn")
                
        if button:
            selected_row = st.session_state.df.iloc[st.session_state.index]
            st.markdown(
                f"""
                <div class='details-text' 
                    style='position: absolute; 
                        left: {details_x + 260}px; 
                        top: {details_y - 120}px; 
                        transform: translate(-50%, -50%);
                        text-align: center;'>
                    {selected_row['Âm hán việt']}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div class='details-text' 
                    style='position: absolute; 
                            left: {details_x + 260}px; 
                            top: {details_y - 100}px; 
                            transform: translateX(-50%); 
                            text-align: center;'>
                    {selected_row['Hiragana']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class='details-text' 
                    style='position: absolute; 
                            left: {details_x + 260}px; 
                            top: {details_y - 50}px; 
                            transform: translateX(-50%); 
                            text-align: center;'>
                    {selected_row['Nghĩa']}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.error("Các cột 'Từ vựng', 'Âm hán việt', 'Hiragana', 'Nghĩa' phải tồn tại trong dữ liệu.")
