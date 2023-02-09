import hmac
import datetime
import hashlib
import binascii

class DateKey:
    value=None
    def __init__(self, secret, utcDate):
        key = b'mes1' + secret.encode('utf-8')
        self.value = hmac.new(key, DateKey.utcDate().encode('utf-8'), 'sha256').digest()
    
    @staticmethod
    def utcDate():
        return '{:%Y%m%d}'.format(datetime.datetime.now())
    
    def hexValue():
        return binascii.hexlify(self.value)