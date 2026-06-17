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

# Auto-detect Azure environment (Azure sets WEBSITE_SITE_NAME)
IS_AZURE = os.environ.get('WEBSITE_SITE_NAME') is not None

# Use writable directories - Azure needs /tmp, local dev uses project folders
if IS_AZURE:
    # Azure App Service - use /tmp for writable storage
    DATA_DIR = os.environ.get('DATA_DIR', '/tmp/certcreate/data')
    CERTIFICATES_DIR = os.environ.get('CERTIFICATES_DIR', '/tmp/certcreate/certificates')
else:
    # Local development
    DATA_DIR = os.environ.get('DATA_DIR', os.path.join(BASE_DIR, 'data'))
    CERTIFICATES_DIR = os.environ.get('CERTIFICATES_DIR', os.path.join(BASE_DIR, 'certificates'))

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CERTIFICATES_DIR, exist_ok=True)

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
    
    # RGB Elevate logo
    'microsoft': 'images/RGB-Elevate.png',
}

# =============================================================================
# CERTIFICATE SETTINGS
# =============================================================================

CERTIFICATE_SETTINGS = {
    # Program information
    'program_name': 'Minecraft Education',
    'program_tagline': 'Claim your credential for completing Minecraft Education training',
    'organization': 'Minecraft Education',
    
    # Certificate title
    'certificate_title': 'Certificate of Completion',
    
    # Certificate message ({name} and {school_name} are substituted)
    'certificate_message': 'This credential certifies that {name} from {school_name} has successfully completed Minecraft Education training.',
    
    # Footer text
    'footer_text': '© Minecraft Education',
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
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production'),
    'DEBUG': os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max upload
}

# =============================================================================
# CLAIM CODE SETTINGS
# =============================================================================
# Attendees must enter a daily-rotating claim code to generate a certificate.
# - 'secret' seeds the code generation (keep this private; change in production).
# - 'admin_token' is the unguessable token in the hidden URL used to view today's
#   code, e.g. /claim-code/<admin_token>. Change it in production.

CLAIM_CODE_SETTINGS = {
    'secret': os.environ.get('CLAIM_CODE_SECRET', 'change-me-claim-code-secret'),
    'admin_token': os.environ.get('CLAIM_CODE_ADMIN_TOKEN', 'change-me-admin-link-token'),
    'code_length': 5,
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
