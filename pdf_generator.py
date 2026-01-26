"""
PDF Certificate Generator Module
================================
Generates A4 PDF certificates using ReportLab.
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config.settings import (
    COLORS, 
    PDF_SETTINGS, 
    CERTIFICATE_SETTINGS,
    LOGOS,
    STATIC_DIR,
    get_logo_path
)


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


def get_reportlab_color(hex_color):
    """Convert hex color to ReportLab color."""
    r, g, b = hex_to_rgb(hex_color)
    return colors.Color(r, g, b)


class CertificateGenerator:
    """Base class for generating PDF certificates."""
    
    def __init__(self, output_path):
        self.output_path = output_path
        self.page_width, self.page_height = A4
        self.margin = 50
        
        # Colors - using official Minecraft Education branding
        self.primary_green = get_reportlab_color(COLORS['primary_green'])
        self.dark_green = get_reportlab_color(COLORS['dark_green'])
        self.light_green = get_reportlab_color(COLORS['light_green'])
        self.cert_gold = get_reportlab_color(COLORS['cert_gold'])
        self.accent_blue = get_reportlab_color(COLORS['accent_blue'])
        self.text_dark = get_reportlab_color(COLORS['text_dark'])
        self.text_muted = get_reportlab_color(COLORS['text_muted'])
        self.cert_background = get_reportlab_color(COLORS['cert_background'])
        
    def draw_border(self, c):
        """Draw decorative border around the certificate."""
        # Outer border - certificate gold
        c.setStrokeColor(self.cert_gold)
        c.setLineWidth(8)
        c.rect(20, 20, self.page_width - 40, self.page_height - 40)
        
        # Inner border - primary green (Minecraft Education signature)
        c.setStrokeColor(self.primary_green)
        c.setLineWidth(2)
        c.rect(32, 32, self.page_width - 64, self.page_height - 64)
        
        # Corner decorations
        self._draw_corner_decoration(c, 40, 40)
        self._draw_corner_decoration(c, self.page_width - 40, 40)
        self._draw_corner_decoration(c, 40, self.page_height - 40)
        self._draw_corner_decoration(c, self.page_width - 40, self.page_height - 40)
    
    def _draw_corner_decoration(self, c, x, y):
        """Draw a simple corner decoration."""
        c.setFillColor(self.cert_gold)
        c.circle(x, y, 5, fill=1, stroke=0)
    
    def draw_logo(self, c, y_position):
        """Draw the Minecraft Education, BBC Bitesize, and Microsoft logos."""
        logo_path = get_logo_path('minecraft_education')
        bbc_logo_path = get_logo_path('bbc_bitesize')
        microsoft_logo_path = get_logo_path('microsoft')
        
        logo_width = PDF_SETTINGS['main_logo_width'] * 0.7  # Slightly smaller for 3 logos
        logo_height = logo_width * 0.4  # Approximate aspect ratio
        spacing = 20  # Space between logos
        
        # Calculate positions for three logos side by side
        total_width = (logo_width * 3) + (spacing * 2)
        start_x = (self.page_width - total_width) / 2
        
        logos_drawn = False
        
        # Draw Minecraft Education logo on the left
        if logo_path and os.path.exists(logo_path):
            try:
                c.drawImage(logo_path, start_x, y_position, 
                           width=logo_width, height=logo_height,
                           preserveAspectRatio=True, mask='auto')
                logos_drawn = True
            except Exception as e:
                print(f"Error loading Minecraft logo: {e}")
        
        # Draw BBC Bitesize logo in the middle
        if bbc_logo_path and os.path.exists(bbc_logo_path):
            try:
                c.drawImage(bbc_logo_path, start_x + logo_width + spacing, y_position, 
                           width=logo_width, height=logo_height,
                           preserveAspectRatio=True, mask='auto')
                logos_drawn = True
            except Exception as e:
                print(f"Error loading BBC Bitesize logo: {e}")
        
        # Draw Microsoft logo on the right
        if microsoft_logo_path and os.path.exists(microsoft_logo_path):
            try:
                c.drawImage(microsoft_logo_path, start_x + (logo_width * 2) + (spacing * 2), y_position, 
                           width=logo_width, height=logo_height,
                           preserveAspectRatio=True, mask='auto')
                logos_drawn = True
            except Exception as e:
                print(f"Error loading Microsoft logo: {e}")
        
        if logos_drawn:
            return y_position - 20
        
        # Fallback: Draw text if logos not available
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(self.primary_green)
        c.drawCentredString(self.page_width / 2, y_position + 20, "MINECRAFT EDUCATION")
        return y_position
    
    def draw_program_badge(self, c, y_position):
        """Draw the AI Foundations program badge."""
        badge_text = CERTIFICATE_SETTINGS['program_name'].upper()
        
        # Badge background
        badge_width = 180
        badge_height = 30
        x_position = (self.page_width - badge_width) / 2
        
        c.setFillColor(self.primary_green)
        c.roundRect(x_position, y_position - badge_height + 5, 
                   badge_width, badge_height, 5, fill=1, stroke=0)
        
        # Badge text
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(self.page_width / 2, y_position - 15, badge_text)
        
        return y_position - badge_height - 20
    
    def draw_seal(self, c, y_position):
        """Draw the certificate seal."""
        seal_path = get_logo_path('certificate_seal')
        if seal_path and os.path.exists(seal_path):
            try:
                seal_size = PDF_SETTINGS['seal_size']
                x_position = (self.page_width - seal_size) / 2
                c.drawImage(seal_path, x_position, y_position - seal_size,
                           width=seal_size, height=seal_size,
                           preserveAspectRatio=True, mask='auto')
                return y_position - seal_size - 10
            except Exception:
                pass
        
        # Fallback: Draw a simple seal
        c.setFillColor(self.cert_gold)
        c.circle(self.page_width / 2, y_position - 30, 30, fill=1, stroke=0)
        c.setFillColor(self.dark_green)
        c.circle(self.page_width / 2, y_position - 30, 20, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.page_width / 2, y_position - 35, "★")
        
        return y_position - 70


def generate_school_certificate(school_name, teacher_name, completion_date, output_path, cert_id):
    """Generate a school certificate of participation."""
    
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4
    
    generator = CertificateGenerator(output_path)
    
    # Background - white
    c.setFillColor(colors.white)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    
    # Draw border
    generator.draw_border(c)
    
    # Starting Y position (below border)
    y = page_height - 120
    
    # Logo
    y = generator.draw_logo(c, y)
    y -= 30
    
    # Program badge
    y = generator.draw_program_badge(c, y)
    y -= 20
    
    # Certificate title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(generator.primary_green)
    c.drawCentredString(page_width / 2, y, CERTIFICATE_SETTINGS['school_certificate_title'].upper())
    y -= 50
    
    # "This certifies that"
    c.setFont("Helvetica", 14)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 2, y, "This certifies that")
    y -= 40
    
    # School name
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(generator.text_dark)
    
    # Handle long school names
    if len(school_name) > 30:
        c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_width / 2, y, school_name)
    y -= 35
    
    # "represented by"
    c.setFont("Helvetica", 14)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 2, y, "represented by")
    y -= 35
    
    # Teacher name
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(generator.accent_blue)
    c.drawCentredString(page_width / 2, y, teacher_name)
    y -= 50
    
    # Completion message
    c.setFont("Helvetica", 12)
    c.setFillColor(generator.text_muted)
    message_lines = [
        "has successfully participated in the",
        "AI Foundations program,",
        "demonstrating commitment to building",
        "AI literacy and digital skills with Minecraft Education."
    ]
    for line in message_lines:
        c.drawCentredString(page_width / 2, y, line)
        y -= 18
    
    y -= 20
    
    # Seal
    y = generator.draw_seal(c, y)
    y -= 10
    
    # Footer info
    footer_y = 80
    
    # Date
    c.setFont("Helvetica", 10)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 4, footer_y + 20, "DATE OF COMPLETION")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(generator.text_dark)
    c.drawCentredString(page_width / 4, footer_y, completion_date)
    
    # Certificate ID
    c.setFont("Helvetica", 10)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(3 * page_width / 4, footer_y + 20, "CERTIFICATE ID")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(generator.text_dark)
    c.drawCentredString(3 * page_width / 4, footer_y, cert_id)
    
    # Footer text
    c.setFont("Helvetica", 8)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 2, 45, CERTIFICATE_SETTINGS['footer_text'])
    
    c.save()
    return output_path


def generate_student_certificate(student_name, school_name, output_path, cert_id):
    """Generate a student certificate of achievement."""
    
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4
    
    generator = CertificateGenerator(output_path)
    
    # Background - white
    c.setFillColor(colors.white)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    
    # Draw border
    generator.draw_border(c)
    
    # Starting Y position (below border)
    y = page_height - 120
    
    # Logo
    y = generator.draw_logo(c, y)
    y -= 30
    
    # Program badge
    y = generator.draw_program_badge(c, y)
    y -= 20
    
    # Certificate title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(generator.primary_green)
    c.drawCentredString(page_width / 2, y, CERTIFICATE_SETTINGS['student_certificate_title'].upper())
    y -= 50
    
    # "This certifies that"
    c.setFont("Helvetica", 14)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 2, y, "This certifies that")
    y -= 50
    
    # Student name (prominent) - using certificate gold
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(generator.cert_gold)
    
    # Add shadow effect for student name
    c.setFillColor(colors.Color(0.3, 0.3, 0.3, 0.3))
    c.drawCentredString(page_width / 2 + 2, y - 2, student_name)
    c.setFillColor(generator.cert_gold)
    c.drawCentredString(page_width / 2, y, student_name)
    y -= 40
    
    # "from"
    c.setFont("Helvetica", 14)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 2, y, "from")
    y -= 35
    
    # School name
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(generator.primary_green)
    if len(school_name) > 35:
        c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_width / 2, y, school_name)
    y -= 50
    
    # Completion message
    c.setFont("Helvetica", 12)
    c.setFillColor(generator.text_muted)
    message_lines = [
        "has successfully completed the",
        "AI Foundations program,",
        "building AI literacy and digital skills",
        "with Minecraft Education."
    ]
    for line in message_lines:
        c.drawCentredString(page_width / 2, y, line)
        y -= 18
    
    y -= 20
    
    # Seal
    y = generator.draw_seal(c, y)
    
    # Footer info
    footer_y = 80
    
    # Date
    completion_date = datetime.now().strftime('%B %d, %Y')
    c.setFont("Helvetica", 10)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 4, footer_y + 20, "DATE")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(generator.text_dark)
    c.drawCentredString(page_width / 4, footer_y, completion_date)
    
    # Certificate ID
    c.setFont("Helvetica", 10)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(3 * page_width / 4, footer_y + 20, "CERTIFICATE ID")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(generator.text_dark)
    c.drawCentredString(3 * page_width / 4, footer_y, cert_id)
    
    # Footer text
    c.setFont("Helvetica", 8)
    c.setFillColor(generator.text_muted)
    c.drawCentredString(page_width / 2, 45, CERTIFICATE_SETTINGS['footer_text'])
    
    c.save()
    return output_path