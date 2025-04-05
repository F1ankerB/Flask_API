from flask import g, request, abort
from flask_wtf.csrf import generate_csrf

def get_csrf_token():
    return generate_csrf()

def add_csrf_header(response):
    response.headers['X-CSRF-Token'] = get_csrf_token()
    return response