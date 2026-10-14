"""
Custom exception hierarchy for granular error handling.
"""

class SMSException(Exception):
    """Base class for all system exceptions."""
    pass

class ValidationError(SMSException):
    """Raised when user input fails structural or logical validation."""
    pass

class StudentNotFoundError(SMSException):
    """Raised when an operation targets a non-existent student."""
    pass

class DuplicateStudentError(SMSException):
    """Raised when attempting to add a student with an existing ID."""
    pass

class AuthenticationError(SMSException):
    """Raised on invalid login credentials."""
    pass

class AccountLockedError(SMSException):
    """Raised when maximum login attempts are exceeded."""
    pass

class StorageError(SMSException):
    """Raised on file I/O, parsing, or serialization failures."""
    pass

class SubjectError(SMSException):
    """Raised when invalid subjects or marks operations are attempted."""
    pass