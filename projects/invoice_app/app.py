import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

from invoices import create_invoice_pdf

def normalize_columns(df):
    df.columns = df.columns.str.strip()                    
    df.columns = df.columns.str.replace("\n", " ", regex=True)  
    df.columns = df.columns.str.replace("\r", " ", regex=True)

    column_map = {
        "Ma Khach hang": "Mã Khách hàng",
        "Ten khach hang": "Tên khách hàng",
        "So dien thoai": "Số điện thoại",
        "Dia chi": "Địa chỉ",
        "Ngay mua": "Ngày mua",
        "Ten san pham": "Tên sản phẩm",
        "So luong": "Số lượng",
        "Don vi tinh": "Đơn vị tính",
        "Gia": "Giá",
        "VAT": "VAT",
        "Giam gia": "Giảm giá",
        "Thanh tien": "Thành tiền",
        "Da Tra": "Đã Trả",
        "Con No": "Còn Nợ",
    }

    df.rename(columns=column_map, inplace=True)
    return df

# ----------------- STREAMLIT APP -----------------

st.title("📑 Ứng dụng tạo hóa đơn từ Excel")

uploaded_file = st.file_uploader("📤 Tải file Excel chứa thông tin hóa đơn", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = normalize_columns(df)
    st.write("📊 Dữ liệu đã tải:")
    st.dataframe(df)

    if st.button("🛠️ Tạo hóa đơn PDF"):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for sales_infor, invoice_data in df.groupby(["Mã Khách hàng", "Ngày mua"]):   # group by Customer ID and Selling Date
                pdf_buffer = create_invoice_pdf(invoice_data)
                zipf.writestr(f"hoadon_{sales_infor[0]}.pdf", pdf_buffer.getvalue())

        zip_buffer.seek(0)
        st.success("✅ Đã tạo xong các hóa đơn!")
        st.download_button(
            label="Tải tất cả hóa đơn (.zip)",
            data=zip_buffer,
            file_name="invoices.zip",
            mime="application/zip"
        )

st.write("📁 Tải file hóa đơn mẫu")

with open("invoices_sample.xlsx", "rb") as f:
    st.download_button(
        label="Excel hóa đơn mẫu",
        data=f,
        file_name="invoices_sample.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )