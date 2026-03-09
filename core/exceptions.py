class BakaError(Exception):
    """Baka class for exceptions in this module"""
    pass

class LoginError(BakaError):
    """Raised when login to Bakalari fails"""
    pass

class FetchError(BakaError):
    """Raised when fetching data from Bakalari fails"""
    pass

class DataExtractionError(BakaError):
    """Raised when data extraction from HTML fails"""
