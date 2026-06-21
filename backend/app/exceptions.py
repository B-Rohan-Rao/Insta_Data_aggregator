class InstagramServiceError(Exception):
    """Base exception for Instagram service errors."""
    pass

class InstagramProfileNotFoundError(InstagramServiceError):
    """Raised when an Instagram profile does not exist."""
    pass

class InstagramProfilePrivateError(InstagramServiceError):
    """Raised when an Instagram profile is private."""
    pass

class InstagramRateLimitError(InstagramServiceError):
    """Raised when Instagram rate limit is reached."""
    pass
