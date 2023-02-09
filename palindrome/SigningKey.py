import hmac
from palindrome.DateKey import *
from palindrome.DateServiceKey import *

class SigningKey:
    value=None
    dateServiceKey=None
    def __init__(self, dateServiceKey=None):
        self.dateServiceKey = dateServiceKey
        if dateServiceKey is not None:
            self.value = hmac.new(self.dateServiceKey.value, 'mes1_request'.encode('utf-8'), 'sha256').digest()

    def sign(self, stringToSign):
        return hmac.new(self.value, stringToSign.encode('utf-8'), 'sha256').hexdigest()
    
    @staticmethod
    def from_(secret, utcDate, service):
        dk = DateKey(secret, utcDate)
        dsk = DateServiceKey(dk, service)
        return SigningKey(dsk)