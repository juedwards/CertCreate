# Minecraft Education AI Foundations Certificate Generator

A Flask web application for generating participation certificates for the Minecraft Education 'AI Foundations' program.

## Features

- **Teacher Registration**: Simple form to register school and teacher information
- **School Certificates**: Generate A4 PDF certificates of participation for schools
- **Student Certificates**: Generate individual achievement certificates for students
- **Configurable Branding**: Easy-to-update logo paths and certificate settings
- **Minecraft Education Theme**: Styled with official branding colors and design patterns

## Project Structure

```
/app
  /static
    /css          # Stylesheets
    /images       # General images
    /logos        # Logo files (editable)
  /templates      # Jinja2 HTML templates
  /config         # Configuration settings
  /certificates   # Generated PDF storage
  app.py          # Main Flask application
  pdf_generator.py # PDF generation module
```

## Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   cd app
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Configuration

### Updating Logos

1. Navigate to `app/static/logos/`
2. Replace the placeholder files with your actual logos:
   - `minecraft_education_logo.png` (recommended: 400x160px)
   - `ai_foundations_logo.png` (recommended: 200x80px)
   - `certificate_seal.png` (recommended: 100x100px)
   - `institution_logo.png` (optional)

3. If using different filenames, update paths in `app/config/settings.py`

### Certificate Settings

Edit `app/config/settings.py` to customize:
- Program name and tagline
- Certificate titles and messages
- Colors and fonts
- PDF dimensions and margins

```python
CERTIFICATE_SETTINGS = {
    'program_name': 'AI Foundations',
    'program_tagline': 'Building Digital Skills and AI Literacy with Minecraft',
    'school_certificate_title': 'Certificate of Participation',
    'student_certificate_title': 'Certificate of Achievement',
    # ... more settings
}
```

### Color Theme

The application uses Minecraft Education branding colors defined in `settings.py`:

```python
COLORS = {
    'primary_green': '#3CB043',    # Minecraft grass green
    'minecraft_blue': '#1E88E5',   # Minecraft Education blue
    'gold': '#FFD700',             # Achievement gold
    # ... more colors
}
```

## Usage Flow

1. **Step 1**: Teacher enters their name and school name
2. **Step 2**: School certificate is generated and can be downloaded
3. **Step 3**: Option to create individual student certificates
4. **Step 4**: Enter student's first name and download their certificate

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with registration form |
| `/register` | POST | Process registration and generate school certificate |
| `/school-certificate` | GET | Display school certificate |
| `/download/school-certificate` | GET | Download school certificate PDF |
| `/student-certificates` | GET | Student certificate form |
| `/generate-student-certificate` | POST | Generate student certificate |
| `/download/student-certificate` | GET | Download student certificate PDF |
| `/new-session` | GET | Clear session and start over |

## Production Deployment

For production deployment, consider:

1. **Change the secret key** in `settings.py`:
   ```python
   FLASK_SETTINGS = {
       'SECRET_KEY': 'your-secure-random-key-here',
       'DEBUG': False,
   }
   ```

2. **Use a production WSGI server**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up proper file storage** for generated certificates (cloud storage recommended)

4. **Add HTTPS** through a reverse proxy (nginx/Apache)

## Technologies Used

- **Backend**: Flask (Python)
- **PDF Generation**: ReportLab
- **Frontend**: HTML5, CSS3 (custom styling)
- **Fonts**: Nunito (Google Fonts)

## License

This project is for educational purposes with Minecraft Education.

© Minecraft Education - Mojang AB / Microsoft Corporation
