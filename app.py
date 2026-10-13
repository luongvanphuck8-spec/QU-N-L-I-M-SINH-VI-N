import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(page_title="QUẢN LÝ ĐIỂM SINH VIÊN", layout="wide")

# 1. Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Khởi tạo Dataframe
data = {
    "Họ tên": [
        "Nguyễn Văn A", "Trần Thị B", "Lê Hoàng C", "Phạm Minh D", "Vũ Thị E",
        "Đặng Văn F", "Bùi Thị G", "Đỗ Hoàng H", "Ngô Thị I", "Dương Văn K"
    ],
    'Chuyên cần': [9.0, 8.5, 7.0, 10.0, 6.5, 8.0, 9.5, 5.0, 8.5, 9.0],
    'Giữa kỳ':    [8.0, 7.5, 6.0,  9.5, 5.5, 7.0, 8.5, 6.0, 7.5, 8.0],
    'Cuối kỳ':    [8.5, 8.0, 6.5,  9.0, 6.0, 7.5, 9.0, 5.5, 8.0, 8.5]
}
df = pd.DataFrame(data)

# Tính điểm tổng kết
df["Tổng kết"] = (df["Chuyên cần"] * 0.2 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.5).round(2)

# Phân loại xếp loại
def phan_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df['Xếp loại'] = df['Tổng kết'].apply(phan_loai)

# 3. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 4. Thống kê thông tin tổng quan
st.subheader("📊 Thống kê chung")

diem_tb_lop = df['Tổng kết'].mean()
sv_cao_nhat = df.loc[df['Tổng kết'].idxmax()]
sv_thap_nhat = df.loc[df['Tổng kết'].idxmin()]
so_sv_dat = (df["Tổng kết"] >= 5.0).sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Điểm TB cả lớp", value=f"{diem_tb_lop:.2f}")
with col2:
    st.metric(label="Điểm cao nhất", value=f"{sv_cao_nhat['Tổng kết']} ({sv_cao_nhat['Họ tên']})")
with col3:
    st.metric(label="Điểm thấp nhất", value=f"{sv_thap_nhat['Tổng kết']} ({sv_thap_nhat['Họ tên']})")
with col4:
    st.metric(label="Số SV đạt (>=5.0)", value=f"{so_sv_dat} / {len(df)}")

st.markdown("---")

# 5. Xem chi tiết sinh viên (Selectbox)
st.subheader("🔍 Tra cứu sinh viên")
selected_student = st.selectbox("Chọn sinh viên để xem chi tiết:", df["Họ tên"].unique())

if selected_student:
    sv_info = df[df["Họ tên"] == selected_student].iloc[0]
    
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    col_a.metric("Điểm Chuyên cần", sv_info["Chuyên cần"])
    col_b.metric("Điểm Giữa kỳ", sv_info["Giữa kỳ"])
    col_c.metric("Điểm Cuối kỳ", sv_info["Cuối kỳ"])
    col_d.metric("Điểm Tổng kết", sv_info["Tổng kết"])
    col_e.metric("Xếp loại", sv_info["Xếp loại"])

st.markdown("---")

# 6. Biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(df['Họ tên'], df['Tổng kết'], color='skyblue', edgecolor='navy')

ax.set_title('Biểu đồ điểm tổng kết của 10 sinh viên', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Họ tên sinh viên', fontsize=11)
ax.set_ylabel('Điểm tổng kết', fontsize=11)
ax.set_ylim(0, 10)
plt.xticks(rotation=45, ha='right')

# Hiển thị số điểm trên mỗi cột
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval:.1f}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
st.pyplot(fig)

# 7. Thông tin người tạo ở cuối trang
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 13px;'>
        <b>Người thực hiện:</b> Nguyễn Văn A | <b>MSSV:</b> 12345678
    </div>
    """, 
    unsafe_allow_html=True
)