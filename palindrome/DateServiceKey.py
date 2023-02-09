import hmac

class DateServiceKey:
    value=None

    def __init__(self, dateKey, service):
        self.value = hmac.new(dateKey.value, service.encode('utf-8'), 'sha256').digest()

    def hexValue():
        return binascii.hexlify(self.value)