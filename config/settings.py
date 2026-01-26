"""
Certificate Generator Configuration Settings
============================================
Edit this file to customize logos, colors, and certificate settings.
All paths are relative to the app/static folder.
"""

import os

# Base directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
CERTIFICATES_DIR = os.path.join(BASE_DIR, 'certificates')

# =============================================================================
# LOGO CONFIGURATION
# =============================================================================
# Update these paths to change the logos displayed on certificates
# Paths are relative to app/static/

LOGOS = {
    # Main Minecraft Education logo (displayed on certificates)
    'minecraft_education': 'images/minecraft_logo.png',
    
    # AI Foundations program logo
    'ai_foundations': 'static/logos/ai_foundations_logo.png',
    
    # School/institution logo placeholder (optional)
    'institution': 'logos/institution_logo.png',
    
    # Certificate badge/seal
    'certificate_seal': 'logos/certificate_seal.png',
    
    # Background pattern for certificates (optional)
    'certificate_background': 'images/certificate_background.png',
    
    # BBC Bitesize logo
    'bbc_bitesize': 'images/bbc_bitesize.png',
    
    # Microsoft logo
    'microsoft': 'images/Microsoft-Logo.png',
}

# =============================================================================
# CERTIFICATE SETTINGS
# =============================================================================

CERTIFICATE_SETTINGS = {
    # Program information
    'program_name': 'AI Foundations',
    'program_tagline': 'Building Digital Skills and AI Literacy with Minecraft',
    'organization': 'Minecraft Education',
    
    # Certificate titles
    'school_certificate_title': 'Certificate of Participation',
    'student_certificate_title': 'Certificate of Achievement',
    
    # Certificate messages
    'school_certificate_message': 'This certifies that {school_name} has successfully participated in the AI Foundations program, demonstrating commitment to building AI literacy and digital skills.',
    'student_certificate_message': 'This certifies that {student_name} from {school_name} has successfully completed the AI Foundations program.',
    
    # Footer text
    'footer_text': '© Minecraft Education - Building Digital Skills and AI Literacy',
}

# =============================================================================
# BRANDING COLORS (Minecraft Education Theme)
# =============================================================================
# Colors based on official Minecraft Education branding

COLORS = {
    # Brand Palette - Only 4 colors
    'primary_green': '#3C8517',      # Dark green - primary brand color
    'dark_green': '#3C8517',         # Same as primary
    'light_green': '#D9F3CD',        # Light green - backgrounds/accents
    
    # Background colours
    'bg_dark': '#262626',            # Dark grey backgrounds
    'bg_darker': '#262626',          # Dark grey
    'bg_light': '#FFFFFF',           # White
    'bg_off_white': '#D9F3CD',       # Light green for alternating sections
    
    # Accent colours (mapped to brand palette)
    'accent_purple': '#3C8517',      # Use primary green
    'accent_blue': '#3C8517',        # Use primary green
    'accent_orange': '#3C8517',      # Use primary green
    
    # Certificate-specific
    'cert_gold': '#3C8517',          # Use primary green for accents
    'cert_border': '#3C8517',        # Certificate border
    'cert_background': '#FFFFFF',    # White background
    
    # Text colours
    'text_dark': '#262626',          # Dark grey text
    'text_muted': '#262626',         # Dark grey for secondary text
    'text_light': '#FFFFFF',         # White text
}

# =============================================================================
# PDF SETTINGS
# =============================================================================

PDF_SETTINGS = {
    # Page size (A4)
    'page_width': 595.27,   # A4 width in points
    'page_height': 841.89,  # A4 height in points
    
    # Margins
    'margin_top': 50,
    'margin_bottom': 50,
    'margin_left': 50,
    'margin_right': 50,
    
    # Font sizes
    'title_font_size': 36,
    'subtitle_font_size': 24,
    'body_font_size': 14,
    'small_font_size': 10,
    
    # Logo sizes (width in points)
    'main_logo_width': 200,
    'secondary_logo_width': 100,
    'seal_size': 80,
}

# =============================================================================
# FLASK APP SETTINGS
# =============================================================================

FLASK_SETTINGS = {
    'SECRET_KEY': 'your-secret-key-change-in-production',
    'DEBUG': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max upload
}


def get_logo_path(logo_key):
    """Get the full path to a logo file."""
    if logo_key in LOGOS:
        return os.path.join(BASE_DIR, LOGOS[logo_key])
    return None


def get_certificates_dir():
    """Get the certificates directory, creating it if needed."""
    if not os.path.exists(CERTIFICATES_DIR):
        os.makedirs(CERTIFICATES_DIR)
    return CERTIFICATES_DIR
