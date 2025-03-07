from reportlab.platypus import Paragraph, Image as RLImage, Spacer
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, FrameBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime
import io

pdfmetrics.registerFont(TTFont('D-DIN', '/home/ash/.fonts/D-DIN.ttf'))
pdfmetrics.registerFont(TTFont('D-DIN-Bold', '/home/ash/.fonts/D-DIN-Bold.ttf'))

def create_newspaper_pdf(content: dict, output_path: str):
    """
    Generates a 2-column PDF. If there's a black & white NASA image, it is placed at the top
    of the first column at the correct single-column width.
    """
    page_width, page_height = letter
    margin = 0.5 * inch
    gutter = 0.15 * inch
    column_width = (page_width - 2 * margin - gutter) / 2
    column_height = page_height - 2 * margin

    # Two-column frames
    frame1 = Frame(margin, margin, column_width, column_height, id='col1')
    frame2 = Frame(margin + column_width + gutter, margin, column_width, column_height, id='col2')
    
    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc = BaseDocTemplate(output_path, pagesize=letter, pageTemplates=[template])
    
    styles = getSampleStyleSheet()
    headline_style = ParagraphStyle(
        'Headline',
        parent=styles['Heading1'],
        fontName='D-DIN',
        fontSize=18,
        leading=18,
        spaceAfter=10,
    )
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['BodyText'],
        fontName='D-DIN',
        fontSize=10,
        leading=12,
        spaceAfter=12,
    )
    
    flowables = []
    
    # 1) Newspaper Title & Date
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    newspaper_title = "Morning Times"
    title_para = Paragraph(
        f"<para align='center'><b>{newspaper_title}</b><br/><font size=10>{current_date}</font></para>",
        ParagraphStyle(
            'NewspaperTitle',
            parent=styles['Heading1'],
            fontName='D-DIN-Bold',
            fontSize=26,
            leading=22,
            spaceAfter=20
        )
    )
    flowables.append(title_para)
    
    divider = Paragraph("<hr width='100%'/>", styles['BodyText'])
    flowables.append(divider)
    
    # 2) If we have a NASA image in content['front_image'], place it as single-column wide
    front_image_articles = content.get('front_image', [])
    if front_image_articles:
        first_img_data = front_image_articles[0]
        pil_img = first_img_data.get('image')
        if pil_img:
            # Scale to single-column width
            img_w, img_h = pil_img.size
            scale = column_width / float(img_w)
            new_w = column_width
            new_h = img_h * scale
            
            # Convert PIL to a bytes buffer
            img_buffer = io.BytesIO()
            pil_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Create the ReportLab image with single-column width
            rl_img = RLImage(img_buffer, width=new_w, height=new_h)
            
            flowables.append(rl_img)
            flowables.append(Spacer(1, 12))  # a bit of space after the image
            # We do NOT add FrameBreak(), so text flows underneath in the same column
    
    # 3) Put the rest of the articles in the columns
    for section, articles in content.items():
        if section == 'front_image':
            continue  # already placed the NASA image
        
        section_title = f"<b>{section.upper()}</b>"
        flowables.append(Paragraph(section_title, headline_style))
        
        for article in articles:
            if 'summary' in article:
                flowables.append(Paragraph(article['summary'], summary_style))
            # If article has an image, handle similarly
            flowables.append(Spacer(1, 12))
    
    # Final divider
    flowables.append(Paragraph("<hr width='100%'/>", styles['BodyText']))
    
    doc.build(flowables)
