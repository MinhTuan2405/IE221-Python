from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Image
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from num2words import num2words
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm
import datetime
from company_infor import COMPANY_INFOR

pdfmetrics.registerFont(TTFont('TimesNewRoman', 'TIMES.TTF'))

def number_to_words(n):
    return num2words(n, lang="vi") + " đồng chẵn"

def create_invoice_pdf(invoice_data):
    """
    invoice_data: dataframe
    Includes fields:
    Mã Khách hàng, Tên khách hàng, Số điện thoại, Địa chỉ, Email, Ngày mua,
    Tên sản phẩm, Số lượng, Đơn vị tính, Giá, VAT, Giảm giá, Thành tiền, Đã Trả, Còn Nợ
    """
    logo_path = 'logo.png'
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    row0 = invoice_data.iloc[0] 

    def format_money(val):
        try:
            return f"{int(val):,} VND"
        except:
            return str(val)

    # ---- HEADER ----
    def draw_header(logo_path, company_infor):
        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        normal_style.fontName = "TimesNewRoman"
        normal_style.fontSize = 10
        normal_style.leading = 14
        normal_style.alignment = TA_LEFT

        bold_style = styles["Heading2"]
        bold_style.fontName = "TimesNewRoman"
        bold_style.fontSize = 18    
        bold_style.leading = 20
        bold_style.alignment = TA_LEFT

        logo = ""
        if logo_path:
            logo = Image(logo_path, width=45*mm, height=30*mm)

        right_content = [
            Paragraph(f"{company_infor['name'].upper()}", bold_style),
            Paragraph(f"Địa chỉ: {company_infor['address']}", normal_style),
            Paragraph(f"Email: {company_infor['email']}", normal_style),
            Paragraph(f"Số điện thoại: {company_infor['phone']}", normal_style),
            Paragraph(f"Mã số thuế: {company_infor['tax']}", normal_style),
        ]

        data = [[logo, right_content]]

        table = Table(data, colWidths=[50*mm, 130*mm])
        table.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (1,0), (1,0), 15),  
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("TOPPADDING", (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ]))
        table.wrapOn(c, width, height)
        table.drawOn(c, 40, height - 150)

    def draw_products_table(invoice_data, c, width, start_y):
        """
        draw the product table, then make the total bill the the signing area
        start_y: current y position for drawing the table
        """
        wrap_style = ParagraphStyle(
            name="wrap",
            fontName="TimesNewRoman",
            fontSize=9,
            alignment=TA_LEFT,
            leading=12
        )

        # Table header
        data = [[
            "STT", "Tên sản phẩm", "Số lượng", "ĐVT", "Giá", "VAT", "Giảm giá", "Thành tiền", "Đã Trả", "Còn Nợ"
        ]]

        for i, (_, row) in enumerate(invoice_data.iterrows(), start=1):
            data.append([
                Paragraph(str(i), wrap_style),
                Paragraph(row.get("Tên sản phẩm", ""), wrap_style),
                Paragraph(str(row.get("Số lượng", "")), wrap_style),
                Paragraph(row.get("Đơn vị tính", ""), wrap_style),
                Paragraph(format_money(row.get("Giá", 0)), wrap_style),
                Paragraph(f"{row.get('VAT', 0)*100:.0f}%", wrap_style),
                Paragraph(format_money(row.get("Giảm giá", 0)), wrap_style),
                Paragraph(format_money(row.get("Thành tiền", 0)), wrap_style),
                Paragraph(format_money(row.get("Đã Trả", 0)), wrap_style),
                Paragraph(format_money(row.get("Còn Nợ", 0)), wrap_style),
            ])

        # Summary
        total_billing  = invoice_data['Thành tiền'].sum()
        total_payment  = invoice_data['Đã Trả'].sum()
        total_debt     = invoice_data['Còn Nợ'].sum()
        total_discount = invoice_data['Giảm giá'].sum()

        data.append([
            "", Paragraph("<b>TỔNG CỘNG</b>", wrap_style), "", "", "", "",
            Paragraph(format_money(total_discount), wrap_style),
            Paragraph(format_money(total_billing), wrap_style),
            Paragraph(format_money(total_payment), wrap_style),
            Paragraph(format_money(total_debt), wrap_style),
        ])

        col_widths = [25, 90, 45, 50, 60, 35, 50, 70, 60, 60]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
            ("FONTNAME", (0,0), (-1,-1), "TimesNewRoman"),
            ("FONTSIZE", (0,0), (-1,0), 10),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#004080")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("ALIGN", (0,0), (0,-2), "CENTER"),
            ("ALIGN", (1,1), (1,-2), "LEFT"),
            ("ALIGN", (2,1), (3,-2), "CENTER"),
            ("ALIGN", (4,1), (-1,-2), "LEFT"),
            ("ALIGN", (1,-1), (-1,-1), "RIGHT"),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BACKGROUND", (0,-1), (-1,-1), colors.lightgrey),
            ("FONTSIZE", (0,-1), (-1,-1), 10),
        ]))

        table.wrapOn(c, width, start_y)
        table_height = table._height 
        table.drawOn(c, 20, start_y - table_height)

        current_y = start_y - table_height - 20  

        # ---- TOTAL IN WORDS ----
        c.setFont("TimesNewRoman", 12)
        c.drawRightString(width - 60, current_y, f"Bằng chữ: {number_to_words(total_billing)}")

        # ---- SIGNATURE AREA ----
        signature_y = current_y - 40
        c.drawString(60, signature_y, "Người lập hóa đơn")
        c.drawString(width - 200, signature_y, "Khách hàng")
        c.line(60, signature_y-5, 180, signature_y-5)  # line for signature
        c.line(width - 200, signature_y-5, width - 60, signature_y-5)

        return total_billing


    # ---- DRAW HEADER ----
    draw_header(logo_path, COMPANY_INFOR)

    c.setFont("TimesNewRoman", 16)
    c.drawCentredString(width/2, height - 200, "Hóa đơn bán hàng".upper())

    # ---- CUSTOMER INFO ----
    c.setFont("TimesNewRoman", 12)
    y = height - 220
    c.drawString(60, y,     f"Mã KH: {row0['Mã Khách hàng']}")
    c.drawString(330, y,    f"Tên KH: {row0['Tên khách hàng']}")
    c.drawString(60, y-20,  f"SĐT: {row0['Số điện thoại']}")
    c.drawString(330, y-20, f"Email: {row0['Email']}")
    c.drawString(60, y-40,  f"Địa chỉ: {row0['Địa chỉ']}")
    c.drawString(60, y-60,  f"Ngày mua: {row0['Ngày mua']}")

    # ---- PRODUCT DETAILS ----
    c.setFont("TimesNewRoman", 14)
    c.drawCentredString(width/2, height - 320, "Thông tin mua hàng chi tiết".upper())
    draw_products_table(invoice_data, c, width, start_y=height - 350)

    c.save()
    buffer.seek(0)
    return buffer
