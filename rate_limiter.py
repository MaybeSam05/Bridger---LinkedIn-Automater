from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import time

class RateLimiter:
    def __init__(self):
        # Store requests as: {ip: [(timestamp, endpoint), ...]}
        self._requests: Dict[str, List[Tuple[float, str]]] = {}
        
        # Configure limits as: {endpoint: (requests, seconds)}
        self._limits = {
            # Authentication endpoints - more restrictive
            "/authenticate_gmail": (5, 300),  # 5 requests per 5 minutes
            "/setup": (5, 300),              # 5 requests per 5 minutes
            
            # Profile analysis endpoints - moderate restriction
            "/find_connection": (10, 300),    # 10 requests per 5 minutes
            
            # Email endpoints - moderate restriction
            "/send_email": (10, 300),         # 10 requests per 5 minutes
            
            # Read-only endpoints - more lenient
            "/email_history": (30, 60),       # 30 requests per minute
            "/check_linkedin_status": (30, 60) # 30 requests per minute
        }
        
        # Default limit for unlisted endpoints
        self._default_limit = (20, 60)  # 20 requests per minute
    
    def _clean_old_requests(self, ip: str, endpoint: str) -> None:
        """Remove requests older than the window for the given endpoint."""
        if ip not in self._requests:
            return
            
        now = time.time()
        window = self._limits.get(endpoint, self._default_limit)[1]
        
        self._requests[ip] = [
            req for req in self._requests[ip]
            if now - req[0] < window and req[1] == endpoint
        ]
    
    def is_rate_limited(self, request: Request) -> bool:
        """Check if the request should be rate limited."""
        ip = request.client.host
        endpoint = request.url.path
        now = time.time()
        
        # Clean old requests first
        self._clean_old_requests(ip, endpoint)
        
        # Get limits for this endpoint
        max_requests, window = self._limits.get(endpoint, self._default_limit)
        
        # Initialize request list for this IP if it doesn't exist
        if ip not in self._requests:
            self._requests[ip] = []
        
        # Count recent requests for this endpoint
        recent_requests = sum(
            1 for req in self._requests[ip]
            if req[1] == endpoint
        )
        
        # Check if limit is exceeded
        if recent_requests >= max_requests:
            return True
        
        # Add new request to the list
        self._requests[ip].append((now, endpoint))
        return False

# Create a global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_dependency(request: Request):
    """FastAPI dependency for rate limiting."""
    if rate_limiter.is_rate_limited(request):
        endpoint = request.url.path
        max_requests, window = rate_limiter._limits.get(endpoint, rate_limiter._default_limit)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. Maximum {max_requests} requests per {window} seconds.",
                "retry_after": window
            }
        )
    return True 