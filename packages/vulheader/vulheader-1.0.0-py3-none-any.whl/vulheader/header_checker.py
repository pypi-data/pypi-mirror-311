import requests

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]

def check(url, header=None):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        if header:
            return "present" if header in headers else "missing"
        else:
            return {header: ("present" if header in headers else "missing") for header in SECURITY_HEADERS}
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to {url}. Details: {e}")
        return "error"
