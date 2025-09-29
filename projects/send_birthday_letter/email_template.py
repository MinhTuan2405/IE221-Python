# Email HTML Templates
templates = {
    "Chúc mừng sinh nhật": """
    <html>
      <body style="font-family:Arial, sans-serif; color:#333; background:#f9f9f9; padding:20px;">
        <h2 style="color:#D35400;">🎉 Chúc mừng sinh nhật {name}!</h2>
        <p>Chúc bạn một ngày sinh nhật thật nhiều niềm vui, hạnh phúc và thành công.</p>
        <p>Hãy tận hưởng ngày đặc biệt này cùng gia đình và bạn bè nhé! 🥳</p>
        <p style="margin-top:20px;">Trân trọng,<br><b>Đội ngũ công ty</b></p>
      </body>
    </html>
    """,

    #######################################################################################################################
    "Mời tham gia sự kiện": """
    <html>
      <body style="font-family:Arial, sans-serif; color:#333; padding:20px;">
        <h2 style="color:#27AE60;">🌟 Kính gửi {name},</h2>
        <p>Chúng tôi trân trọng mời bạn tham dự sự kiện đặc biệt: Python Summit Day</p>
        <p><b>Thời gian:</b> 31/12/2025, 12:00<br>
           <b>Địa điểm:</b> Hội Trường Lớn, 1000 An Dương Vương, Phường Chợ Quán, Thành phố Hồ Chí Minh</p>
        <p>Rất mong sự có mặt của bạn để sự kiện thêm phần ý nghĩa.</p>
        <p style="margin-top:20px;">Thân ái,<br><b>Ban tổ chức</b></p>
      </body>
    </html>
    """,

    #######################################################################################################################
    "Nhắc nhở họp": """
    <html>
      <body style="font-family:Arial, sans-serif; color:#333; padding:20px;">
        <h2 style="color:#2980B9;">⏰ Lời nhắc họp</h2>
        <p>Xin chào {name},</p>
        <p>Cuộc họp <b>Họp hàng tháng</b> sẽ diễn ra vào:</p>
        <p><b>Thời gian:</b> 31/12/2025, 12:00<br>
           <b>Địa điểm:</b> Phòng E1</p>
        <p>Vui lòng sắp xếp tham dự đầy đủ và đúng giờ.</p>
        <p style="margin-top:20px;">Trân trọng,<br><b>Phòng Hành chính</b></p>
      </body>
    </html>
    """,

    #######################################################################################################################
    "Thông báo nghỉ làm": """
    <html>
      <body style="font-family:Arial, sans-serif; color:#333; padding:20px;">
        <h2 style="color:#8E44AD;">📢 Thông báo nghỉ làm</h2>
        <p>Kính gửi {name},</p>
        <p>Xin thông báo công ty sẽ nghỉ làm vào ngày <b>31/12/2025</b> nhân dịp <b> nghỉ chủ nhật</b>.</p>
        <p>Rất mong mọi người sắp xếp công việc phù hợp.</p>
        <p style="margin-top:20px;">Trân trọng,<br><b>Ban giám đốc</b></p>
      </body>
    </html>
    """,
    
    #######################################################################################################################
    "Thông báo khẩn từ cấp trên": """
    <html>
      <body style="font-family:Arial, sans-serif; color:#333; background:#fff4e6; padding:20px; border:1px solid #e67e22;">
        <h2 style="color:#C0392B;">⚠️ Thông báo khẩn</h2>
        <p>Kính gửi {name},</p>
        <p>Đây là thông báo khẩn từ <b>Bộ phận giám đốc</b>:</p>
        <blockquote style="border-left:3px solid #e67e22; padding-left:10px; margin:10px 0;">
          Thông báo này là thông báo rất khẩn, cảm ơn đã chú ý
        </blockquote>
        <p>Vui lòng thực hiện ngay và báo cáo kết quả trước <b>31/12/2025, 12:00</b>.</p>
        <p style="margin-top:20px;">Trân trọng,<br><b>Văn phòng Giám đốc</b></p>
      </body>
    </html>
    """
}
