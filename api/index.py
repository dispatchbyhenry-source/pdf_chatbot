import sys
import os
from io import BytesIO

# Add parent directory to path to import pdfreader
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from pdfreader import app

# Vercel expects a handler function
def handler(request):
    """
    Vercel serverless function handler for Flask app
    """
    # Get request data
    method = request.method
    path = request.path
    headers = dict(request.headers) if hasattr(request, 'headers') else {}
    body = request.body if hasattr(request, 'body') else b''
    query_string = request.query_string if hasattr(request, 'query_string') else ''
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('Content-Type', ''),
        'CONTENT_LENGTH': headers.get('Content-Length', str(len(body))),
        'SERVER_NAME': headers.get('Host', 'localhost'),
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Response storage
    response_data = {'status': None, 'headers': []}
    
    def start_response(status, response_headers):
        response_data['status'] = status
        response_data['headers'] = response_headers
    
    # Call Flask app
    result = app(environ, start_response)
    
    # Collect response body
    body_parts = []
    for part in result:
        if isinstance(part, bytes):
            body_parts.append(part)
        else:
            body_parts.append(part.encode('utf-8'))
    
    response_body = b''.join(body_parts)
    
    # Return response
    status_code = int(response_data['status'].split()[0])
    response_headers = dict(response_data['headers'])
    
    return {
        'statusCode': status_code,
        'headers': response_headers,
        'body': response_body.decode('utf-8')
    }

