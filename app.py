"""
Minecraft Education AI Foundations Certificate Generator
========================================================
Flask web application for generating participation certificates.
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash, send_from_directory
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
from pdf_generator import generate_school_certificate, generate_student_certificate

# Import data store for tracking certificates
from data_store import record_school_certificate, record_student_certificate, get_stats

# Import profanity filter
from profanity_filter import check_all_fields, get_polite_rejection_message

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
    """Process teacher registration and generate school certificate."""
    teacher_name = request.form.get('teacher_name', '').strip()
    school_name = request.form.get('school_name', '').strip()
    region = request.form.get('region', '').strip()
    
    if not teacher_name or not school_name or not region:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('index'))
    
    # Check for inappropriate content
    is_clean, field_name, _ = check_all_fields(
        teacher_name=teacher_name,
        school_name=school_name
    )
    if not is_clean:
        flash(get_polite_rejection_message(), 'error')
        return redirect(url_for('index'))
    
    # Store in session for later use
    session['teacher_name'] = teacher_name
    session['school_name'] = school_name
    session['region'] = region
    session['completion_date'] = datetime.now().strftime('%B %d, %Y')
    
    # Generate unique certificate ID
    cert_id = str(uuid.uuid4())[:8].upper()
    session['school_cert_id'] = cert_id
    
    # Generate school certificate PDF
    try:
        pdf_filename = f"school_certificate_{cert_id}.pdf"
        pdf_path = os.path.join(get_certificates_dir(), pdf_filename)
        
        generate_school_certificate(
            school_name=school_name,
            teacher_name=teacher_name,
            completion_date=session['completion_date'],
            output_path=pdf_path,
            cert_id=cert_id
        )
        
        session['school_pdf_path'] = pdf_path
        session['school_pdf_filename'] = pdf_filename
        
        # Record certificate in data store (school name, region, and cert ID - no personal data)
        record_school_certificate(cert_id, school_name, region)
        
    except Exception as e:
        flash(f'Error generating certificate: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    return redirect(url_for('school_certificate'))


@app.route('/school-certificate')
def school_certificate():
    """Display school certificate page with download option."""
    if 'school_name' not in session:
        flash('Please complete the registration first.', 'error')
        return redirect(url_for('index'))
    
    return render_template('school_certificate.html',
                         teacher_name=session.get('teacher_name'),
                         school_name=session.get('school_name'),
                         completion_date=session.get('completion_date'),
                         cert_id=session.get('school_cert_id'),
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


@app.route('/download/school-certificate')
def download_school_certificate():
    """Download the school certificate PDF."""
    pdf_path = session.get('school_pdf_path')
    pdf_filename = session.get('school_pdf_filename')
    
    if not pdf_path or not os.path.exists(pdf_path):
        flash('Certificate not found. Please generate a new one.', 'error')
        return redirect(url_for('index'))
    
    return send_file(
        pdf_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=pdf_filename
    )


@app.route('/student-certificates')
def student_certificates():
    """Student certificate generation page."""
    if 'school_name' not in session:
        flash('Please complete the school registration first.', 'error')
        return redirect(url_for('index'))
    
    return render_template('student_certificates.html',
                         school_name=session.get('school_name'),
                         teacher_name=session.get('teacher_name'),
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


@app.route('/generate-student-certificate', methods=['POST'])
def generate_student_cert():
    """Generate a student certificate."""
    if 'school_name' not in session:
        flash('Please complete the school registration first.', 'error')
        return redirect(url_for('index'))
    
    student_name = request.form.get('student_name', '').strip()
    
    if not student_name:
        flash('Please enter the student\'s first name.', 'error')
        return redirect(url_for('student_certificates'))
    
    # Check for inappropriate content
    is_clean, _, _ = check_all_fields(student_name=student_name)
    if not is_clean:
        flash(get_polite_rejection_message(), 'error')
        return redirect(url_for('student_certificates'))
    
    # Generate unique certificate ID
    cert_id = str(uuid.uuid4())[:8].upper()
    
    # Generate student certificate PDF
    try:
        pdf_filename = f"student_certificate_{student_name.replace(' ', '_')}_{cert_id}.pdf"
        pdf_path = os.path.join(get_certificates_dir(), pdf_filename)
        
        generate_student_certificate(
            student_name=student_name,
            school_name=session.get('school_name'),
            output_path=pdf_path,
            cert_id=cert_id
        )
        
        # Store for download
        session['last_student_pdf_path'] = pdf_path
        session['last_student_pdf_filename'] = pdf_filename
        session['last_student_name'] = student_name
        
        # Record certificate in data store (only school name and cert ID, NOT student name)
        record_student_certificate(cert_id, session.get('school_name'))
        
    except Exception as e:
        flash(f'Error generating certificate: {str(e)}', 'error')
        return redirect(url_for('student_certificates'))
    
    return redirect(url_for('student_certificate_ready'))


@app.route('/student-certificate-ready')
def student_certificate_ready():
    """Display student certificate ready page."""
    if 'last_student_name' not in session:
        flash('No student certificate generated.', 'error')
        return redirect(url_for('student_certificates'))
    
    return render_template('student_certificate_ready.html',
                         student_name=session.get('last_student_name'),
                         school_name=session.get('school_name'),
                         colors=COLORS,
                         settings=CERTIFICATE_SETTINGS)


@app.route('/download/student-certificate')
def download_student_certificate():
    """Download the student certificate PDF."""
    pdf_path = session.get('last_student_pdf_path')
    pdf_filename = session.get('last_student_pdf_filename')
    
    if not pdf_path or not os.path.exists(pdf_path):
        flash('Certificate not found. Please generate a new one.', 'error')
        return redirect(url_for('student_certificates'))
    
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
