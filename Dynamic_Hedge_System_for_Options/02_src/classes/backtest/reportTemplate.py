"""
@Author: Carl
@Time: 2022/2/1 10:43
@SoftWare: PyCharm
@File: reportTemplate.py
"""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, ListItem, ListFlowable, Frame
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

class ReportTemplate:
    def __init__(self):
        self.txt_template()
        self.table_template()

    def txt_template(self):
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        self.txt_style = getSampleStyleSheet()
        self.txt_style.add(ParagraphStyle(name='正文', alignment=TA_JUSTIFY, fontName='STSong-Light', fontSize=12,
                                          textColor=colors.black))
        self.txt_style.add(ParagraphStyle(name='标题1', alignment=TA_CENTER, fontName='STSong-Light', fontSize=20,
                                          textColor=colors.black, leading=20, wordWrap='CJK'))
        self.txt_style.add(ParagraphStyle(name='标题2', alignment=TA_LEFT, fontName='STSong-Light', fontSize=14,
                                          textColor=colors.black, wordWrap='CJK'))

    def table_template(self):
        self.table_style = [
            ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # 第一行的字体大小
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 第一行左右中间对齐
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有表格上下居中对齐
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # 设置表格框线
            ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ]

    def gen_img(self, filepath):
        img = Image(filepath)
        img.drawHeight = 256
        img.drawWidth = 440
        return img
