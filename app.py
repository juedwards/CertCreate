"""
Minecraft Education Training Certificate Generator
==================================================
Flask web application for generating educator certificates of completion.
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash, send_from_directory, abort
import os
import uuid
from datetime import datetime

# Import configuration
from config.settings import (
    FLASK_SETTINGS, 
    CERTIFICATE_SETTINGS, 
    COLORS,
    get_certificates_dir
)

# Import PDF generator
from pdf_generator import generate_certificate

# Import data store for tracking certificates
from data_store import record_certificate, get_stats

# Import profanity filter
from profanity_filter import check_all_fields, get_polite_rejection_message

# Import claim code helpers
from claim_code import (
    get_claim_code,
    verify_claim_code,
    is_valid_admin_token,
    seconds_until_rotation,
)

app = Flask(__name__)
app.secret_key = FLASK_SETTINGS['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = FLASK_SETTINGS['MAX_CONTENT_LENGTH']

# Get the directory where app.py is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from the app/images folder."""
    return send_from_directory(os.path.join(APP_DIR, 'images'), filename)


@app.route('/')
def index():
    """Home page - Teacher registration form."""
    return render_template('index.html', 
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


@app.route('/register', methods=['POST'])
def register():
    """Process educator registration and generate their certificate."""
    first_name = request.form.get('first_name', '').strip()
    surname = request.form.get('surname', '').strip()
    school_name = request.form.get('school_name', '').strip()
    region = request.form.get('region', '').strip()
    claim_code = request.form.get('claim_code', '').strip()
    
    if not first_name or not surname or not school_name or not region or not claim_code:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('index'))
    
    # Verify the daily claim code (only attendees have today's code)
    if not verify_claim_code(claim_code):
        flash('Invalid or expired claim code. Please use the code provided during the training session.', 'error')
        return redirect(url_for('index'))
    
    # Check for inappropriate content
    is_clean, field_name, _ = check_all_fields(
        first_name=first_name,
        surname=surname,
        school_name=school_name
    )
    if not is_clean:
        flash(get_polite_rejection_message(), 'error')
        return redirect(url_for('index'))
    
    # Store in session for later use
    session['first_name'] = first_name
    session['surname'] = surname
    session['teacher_name'] = f"{first_name} {surname}"
    session['school_name'] = school_name
    session['region'] = region
    session['completion_date'] = datetime.now().strftime('%B %d, %Y')
    
    # Generate unique certificate ID
    cert_id = str(uuid.uuid4())[:8].upper()
    session['cert_id'] = cert_id
    
    # Generate certificate PDF
    try:
        pdf_filename = f"certificate_{cert_id}.pdf"
        pdf_path = os.path.join(get_certificates_dir(), pdf_filename)
        
        generate_certificate(
            first_name=first_name,
            surname=surname,
            school_name=school_name,
            completion_date=session['completion_date'],
            output_path=pdf_path,
            cert_id=cert_id
        )
        
        session['pdf_path'] = pdf_path
        session['pdf_filename'] = pdf_filename
        
        # Record certificate in data store (school name, region, and cert ID - no personal data)
        record_certificate(cert_id, school_name, region)
        
    except Exception as e:
        flash(f'Error generating certificate: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    return redirect(url_for('certificate'))


@app.route('/certificate')
def certificate():
    """Display the certificate page with download option."""
    if 'teacher_name' not in session:
        flash('Please complete the registration first.', 'error')
        return redirect(url_for('index'))
    
    return render_template('certificate.html',
                         teacher_name=session.get('teacher_name'),
                         school_name=session.get('school_name'),
                         completion_date=session.get('completion_date'),
                         cert_id=session.get('cert_id'),
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


@app.route('/download/certificate')
def download_certificate():
    """Download the certificate PDF."""
    pdf_path = session.get('pdf_path')
    pdf_filename = session.get('pdf_filename')
    
    if not pdf_path or not os.path.exists(pdf_path):
        flash('Certificate not found. Please generate a new one.', 'error')
        return redirect(url_for('index'))
    
    return send_file(
        pdf_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=pdf_filename
    )


@app.route('/new-session')
def new_session():
    """Start a new session (clear all data)."""
    session.clear()
    return redirect(url_for('index'))


@app.route('/stats')
def stats():
    """Display certificate statistics."""
    certificate_stats = get_stats()
    return render_template('stats.html',
                         stats=certificate_stats,
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


@app.route('/claim-code/<token>', strict_slashes=False)
def claim_code_admin(token):
    """Hidden page showing today's claim code (guarded by a secret token)."""
    if not is_valid_admin_token(token):
        abort(404)
    
    return render_template('claim_code_admin.html',
                         claim_code=get_claim_code(),
                         today=datetime.now().strftime('%B %d, %Y %H:%M'),
                         seconds_until_rotation=seconds_until_rotation(),
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', 
                         error_code=404,
                         error_message='Page not found',
                         colors=COLORS), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',
                         error_code=500,
                         error_message='Internal server error',
                         colors=COLORS), 500


if __name__ == '__main__':
    # Ensure certificates directory exists
    get_certificates_dir()
    
    # Run the application
    app.run(
        debug=FLASK_SETTINGS['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
