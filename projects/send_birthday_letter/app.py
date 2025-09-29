import streamlit as st
import pandas as pd
from email_template import templates
from email_sender import send_email
import datetime

st.title("📧 Email Sender App")

uploaded_file = st.file_uploader("Tải lên file Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.sidebar.header("Bộ lọc")
    selected_ids = st.sidebar.multiselect(
        "Chọn theo mã nhân viên:",
        options=df["Mã nhân viên"].unique()
    )

    selected_depts = st.sidebar.multiselect(
        "Chọn theo phòng ban:",
        options=df["Phòng ban"].unique()
    )

    filtered_df = df.copy()
    if selected_ids:
        filtered_df = filtered_df[filtered_df["Mã nhân viên"].isin(selected_ids)]
    if selected_depts:
        filtered_df = filtered_df[filtered_df["Phòng ban"].isin(selected_depts)]

    st.subheader("📃 Danh sách nhân viên")
    st.dataframe(filtered_df)

    receiver_list = filtered_df[["Tên nhân viên", "Email"]]

    mode = st.radio("Chọn cách soạn email:", ["Dùng template có sẵn", "Tự soạn email"])

    email_subject = ''
    email_content = ''

    if mode == "Dùng template có sẵn":
        template_choice = st.selectbox("Chọn mẫu email:", list(templates.keys()))
        selected_template = templates[template_choice]

        if template_choice == "Chúc mừng sinh nhật":
            today = datetime.date.today().strftime("%m-%d")
            filtered_df["Ngày sinh"] = pd.to_datetime(filtered_df["Ngày sinh"], errors="coerce")
            filtered_df["Tháng-Ngày sinh"] = filtered_df["Ngày sinh"].dt.strftime("%m-%d")

            birthday_today = filtered_df[filtered_df["Tháng-Ngày sinh"] == today]
            receiver_list = birthday_today[["Tên nhân viên", "Email"]]

            st.info("Chỉ những nhân viên có sinh nhật hôm nay sẽ nhận email này")
            st.dataframe(receiver_list)

        raw_html = selected_template  

        sample_data = {"name": "Nguyễn Văn A"}
        preview_html = raw_html.format(**sample_data)

        st.subheader("📄 Preview Email")
        st.components.v1.html(preview_html, height=300, scrolling=True)

        edited_html = st.text_area("Chỉnh sửa nội dung HTML:", raw_html, height=250)

        email_content = edited_html
        email_subject = template_choice

    else:
        subject = st.text_input("Tiêu đề email")
        edited_html = st.text_area("Soạn nội dung email (có thể dùng HTML):", height=250)

        st.subheader("📄 Email Preview")
        st.components.v1.html(edited_html, height=300, scrolling=True)

        email_content = edited_html
        email_subject = subject

    st.write("📧 Những người sẽ nhận email:")
    st.write(receiver_list)

    if st.button("📤 Gửi email"):
        for _, row in receiver_list.iterrows():
            name = row["Tên nhân viên"]
            email = row["Email"]

            try:
                personalized_content = email_content.format(name=name)
                send_email(email, email_subject, personalized_content)
                st.success(f"Đã gửi email cho {name} ({email})")
            except Exception as e:
                st.error(f"Lỗi khi gửi email cho {name} ({email}): {e}")


st.write("📁 Tải file quản lý nhân viên mẫu")
with open("workforce_information.xlsx", "rb") as f:
    st.download_button(
        label="Excel nhân viên mẫu",
        data=f,
        file_name="workforce_information.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
