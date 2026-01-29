"""
Simple Data Storage Module
==========================
Stores certificate tracking data in a JSON file.
Only stores: certificate ID, school name, and type.
No personal data (teacher names, student names) is stored.
"""

import json
import os
from datetime import datetime
from threading import Lock

# File path for the data store
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'certificates.json')

# Thread lock for safe file access
_lock = Lock()


def _ensure_data_dir():
    """Ensure the data directory exists."""
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def _load_data():
    """Load data from JSON file."""
    _ensure_data_dir()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # Return default structure
    return {
        'school_certificates': {},
        'student_certificates': {},
        'stats': {
            'total_school_certificates': 0,
            'total_student_certificates': 0
        }
    }


def _save_data(data):
    """Save data to JSON file."""
    _ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def record_school_certificate(cert_id, school_name, region=None):
    """
    Record a school certificate.
    
    Args:
        cert_id: Unique certificate ID
        school_name: Name of the school
        region: UK region (England, Wales, Northern Ireland, Scotland)
    """
    with _lock:
        data = _load_data()
        
        data['school_certificates'][cert_id] = {
            'school_name': school_name,
            'region': region,
            'date': datetime.now().isoformat()
        }
        data['stats']['total_school_certificates'] = len(data['school_certificates'])
        
        _save_data(data)


def record_student_certificate(cert_id, school_name):
    """
    Record a student certificate.
    
    Args:
        cert_id: Unique certificate ID
        school_name: Name of the school (not student name)
    """
    with _lock:
        data = _load_data()
        
        data['student_certificates'][cert_id] = {
            'school_name': school_name,
            'date': datetime.now().isoformat()
        }
        data['stats']['total_student_certificates'] = len(data['student_certificates'])
        
        _save_data(data)


def get_stats():
    """
    Get certificate statistics.
    
    Returns:
        dict with total_school_certificates, total_student_certificates, and country breakdown
    """
    with _lock:
        data = _load_data()
        stats = data['stats'].copy()
        
        # Calculate country breakdown for school certificates
        country_counts = {}
        
        for cert_id, cert_data in data['school_certificates'].items():
            country = cert_data.get('region', 'Unknown')
            if country:
                country_counts[country] = country_counts.get(country, 0) + 1
        
        stats['countries'] = country_counts
        
        # Calculate percentages
        total = stats['total_school_certificates']
        if total > 0:
            stats['country_percentages'] = {
                country: round((count / total) * 100, 1)
                for country, count in country_counts.items()
            }
        else:
            stats['country_percentages'] = {}
        
        # Legacy region support (map old UK regions to United Kingdom)
        region_counts = {
            'England': 0,
            'Wales': 0,
            'Northern Ireland': 0,
            'Scotland': 0
        }
        for cert_id, cert_data in data['school_certificates'].items():
            region = cert_data.get('region')
            if region in region_counts:
                region_counts[region] += 1
        
        stats['regions'] = region_counts
        if total > 0:
            stats['region_percentages'] = {
                region: round((count / total) * 100, 1)
                for region, count in region_counts.items()
            }
        else:
            stats['region_percentages'] = {region: 0 for region in region_counts}
        
        return stats


def get_all_data():
    """
    Get all stored data (for admin purposes).
    
    Returns:
        Complete data dictionary
    """
    with _lock:
        return _load_data()


def get_certificate_info(cert_id):
    """
    Look up a certificate by ID.
    
    Args:
        cert_id: Certificate ID to look up
        
    Returns:
        dict with certificate info or None if not found
    """
    with _lock:
        data = _load_data()
        
        if cert_id in data['school_certificates']:
            return {
                'type': 'school',
                **data['school_certificates'][cert_id]
            }
        
        if cert_id in data['student_certificates']:
            return {
                'type': 'student',
                **data['student_certificates'][cert_id]
            }
        
        return None
