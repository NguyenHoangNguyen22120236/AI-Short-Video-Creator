from urllib.parse import urlparse

def is_url(path):
    parsed = urlparse(path)
    return parsed.scheme in ('http', 'https')