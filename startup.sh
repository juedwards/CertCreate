#!/bin/bash

# Create writable directories for Azure
mkdir -p /tmp/certcreate/data
mkdir -p /tmp/certcreate/certificates

# Export environment variables for writable paths
export DATA_DIR=/tmp/certcreate/data
export CERTIFICATES_DIR=/tmp/certcreate/certificates

# Start gunicorn
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
