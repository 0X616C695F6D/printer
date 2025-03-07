from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Image as RLImage, Spacer, FrameBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pyphen
from io import BytesIO
from PIL import Image as PILImage

pdfmetrics.registerFont(TTFont('D-DIN', '/home/ash/.fonts/D-DIN.ttf'))

def create_newspaper_pdf(content: dict, output_path: str):
    """
    Generates a U.S. Letter-sized PDF with a two-column layout.
    
    Parameters:
        content (dict): A dictionary where keys represent article sections 
            (e.g., 'stock', 'astronomy', 'tech') and values are dictionaries containing:
                - 'headline': Article headline
                - 'summary': Summarized text
                - 'image': Processed image object (PIL Image) or image file path/URL.
        output_path (str): Path where the generated PDF will be saved.
    """
    # Page settings
    page_width, page_height = letter  # 612 x 792 points
    margin = 0.5 * inch
    gutter = 0.25 * inch
    column_width = (page_width - 2 * margin - gutter) / 2
    column_height = page_height - 2 * margin

    # Define two frames (columns)
    frame1 = Frame(margin, margin, column_width, column_height, id='col1')
    frame2 = Frame(margin + column_width + gutter, margin, column_width, column_height, id='col2')
    
    # Create a page template with two frames.
    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    
    # Create the document.
    doc = BaseDocTemplate(output_path, pagesize=letter, pageTemplates=[template])
    
    # Define text styles.
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
    
    # Build the list of flowables.
    flowables = []
    
    from datetime import datetime

    # Newspaper Title and Date
    newspaper_title = "Morning Times"
    current_date = datetime.now().strftime("%B %d, %Y")
    title_paragraph = Paragraph(
        f"<para align='center'><b>{newspaper_title}</b><br/><font size=10>{current_date}</font></para>",
        ParagraphStyle(
            'NewspaperTitle',
            parent=styles['Heading1'],
            fontName='D-DIN',
            fontSize=26,
            leading=22,
            spaceAfter=20
        )
    )
    flowables.insert(0, title_paragraph)

    
    divider = Paragraph("<hr width='100%'/>", styles['BodyText'])
    flowables.append(divider)

    for section, articles in content.items():
        # Add a section label.
        section_title = f"<b>{section.upper()}</b>"
        flowables.append(Paragraph(section_title, headline_style))
        
        # article
        for article in articles:
            if 'summary' in article:
                flowables.append(Paragraph(article['summary'], summary_style))
            if 'image' in article and article['image']:
                article_image = article['image']
                if isinstance(article_image, PILImage.Image):
                    # Convert the PIL image to a byte stream.
                    img_buffer = BytesIO()
                    article_image.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    rl_img = RLImage(img_buffer, width=column_width/2)
                else:
                    rl_img = RLImage(article_image, width=column_width/2)
                flowables.append(rl_img)
            
            flowables.append(Spacer(1, 12))
            

    divider = Paragraph("<hr width='100%'/>", styles['BodyText'])
    flowables.append(divider)
    
    try:
        doc.build(flowables)
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")

