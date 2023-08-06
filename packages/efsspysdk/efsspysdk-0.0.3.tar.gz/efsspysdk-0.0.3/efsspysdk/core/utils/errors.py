class SDKException(Exception):
    """Base exception class for the SDK"""
    pass

class APIError(SDKException):
    """Exception raised for API errors"""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

class AuthenticationError(SDKException):
    """Exception raised for authentication errors"""
    pass

class InvalidResourceError(SDKException):
    """Exception raised when a resource is not found"""
    def __init__(self, message):
        super().__init__(message)
