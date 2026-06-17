# Minecraft Education Training Certificate Generator

A Flask web application for generating personalised certificates of completion for
educators who have completed Minecraft Education training (e.g. at ISTE).

## Features

- **Educator Registration**: Simple form for first name, surname, school and country
- **Hourly Claim Code**: Attendees must enter a rotating hourly code; organisers view it via a hidden link
- **Certificate of Completion**: Generate a personalised A4 PDF certificate
- **Statistics**: View certificate counts and a global country breakdown at `/stats`
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
    'program_name': 'Minecraft Education',
    'program_tagline': 'Claim your credential for completing Minecraft Education training',
    'certificate_title': 'Certificate of Completion',
    'certificate_message': 'This credential certifies that {name} from {school_name} has successfully completed Minecraft Education training.',
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

1. **Step 1**: Educator completes Minecraft Education training
2. **Step 2**: Organiser shares the current hour's claim code (from the hidden admin link) with attendees
3. **Step 3**: Educator enters their first name, surname, school, country and the claim code
4. **Step 4**: Personalised certificate of completion is generated and can be downloaded

## Claim Code

Attendees must enter an **hourly-rotating claim code** to generate a certificate, so only
people present at the session can claim one. The code is derived from a server secret and
the current hour (no state is stored) and changes automatically at the top of each hour
(server time).

- **View the current code**: visit the hidden link `/claim-code/<admin_token>`, where
  `<admin_token>` is the secret token configured below. An invalid token returns 404.
- **Configure** via environment variables (recommended for production):
  - `CLAIM_CODE_SECRET` — seeds code generation; keep private.
  - `CLAIM_CODE_ADMIN_TOKEN` — the unguessable token used in the hidden URL.

  These default to placeholder values in `config/settings.py` (`CLAIM_CODE_SETTINGS`)
  and **must be changed in production**.

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with registration form |
| `/register` | POST | Process registration (validates claim code) and generate the certificate |
| `/certificate` | GET | Display the generated certificate |
| `/download/certificate` | GET | Download the certificate PDF |
| `/claim-code/<admin_token>` | GET | Hidden page showing the current hour's claim code |
| `/stats` | GET | Certificate statistics and country breakdown |
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
