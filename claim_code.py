"""
Claim Code Module
=================
Generates an hourly-rotating claim code that attendees must enter to generate a
certificate. The code is derived deterministically from a server-side secret and
the current hour, so it changes every hour without any stored state.

The current code can be viewed via a hidden URL guarded by an admin token, so the
organiser can share it live with attendees during the training session.
"""

import hmac
import hashlib
from datetime import datetime, timedelta

from config.settings import CLAIM_CODE_SETTINGS

# Unambiguous alphabet (no 0/O/1/I) so the code is easy to read and type.
_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def _period_key(for_time=None):
    """Return the rotation-period identifier (date + hour) for a given time."""
    t = for_time or datetime.now()
    return t.strftime('%Y-%m-%dT%H')


def get_claim_code(for_time=None):
    """
    Get the claim code for a given time (defaults to the current hour, server
    local time).

    The code is an HMAC of the period (date + hour) keyed by the configured
    secret, mapped onto an unambiguous alphabet. It is stable for the whole hour
    and changes at the top of each hour.
    """
    secret = CLAIM_CODE_SETTINGS['secret']
    length = CLAIM_CODE_SETTINGS['code_length']
    digest = hmac.new(
        secret.encode('utf-8'),
        _period_key(for_time).encode('utf-8'),
        hashlib.sha256,
    ).digest()
    return ''.join(_ALPHABET[b % len(_ALPHABET)] for b in digest[:length])


def _normalise(code):
    """Normalise a submitted code for comparison (strip spaces, uppercase)."""
    return (code or '').strip().upper().replace(' ', '').replace('-', '')


def verify_claim_code(submitted):
    """Return True if the submitted code matches today's claim code."""
    expected = get_claim_code()
    return hmac.compare_digest(_normalise(submitted), expected)


def is_valid_admin_token(token):
    """Return True if the supplied token matches the configured admin link token."""
    return hmac.compare_digest(str(token), str(CLAIM_CODE_SETTINGS['admin_token']))


def seconds_until_rotation():
    """Seconds remaining until the code rotates (top of the next hour)."""
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return int((next_hour - now).total_seconds())
