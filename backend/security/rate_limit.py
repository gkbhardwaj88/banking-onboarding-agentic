from time import time
BUCKET = {}

def rate_limit(ip: str, limit=10, interval=60):
    now = time()
    if ip not in BUCKET:
        BUCKET[ip] = []
    BUCKET[ip] = [t for t in BUCKET[ip] if now - t < interval]
    if len(BUCKET[ip]) >= limit:
        return False
    BUCKET[ip].append(now)
    return True
