import hashlib
import binascii

class CanonicalRequest:
    target=None
    hashedPayload=None

    def __init__(self, target, payload):
        self.target = target
        hashed = hashlib.sha256(payload.encode('utf-8'))
        self.hashedPayload = binascii.hexlify(hashed.digest()).decode('utf-8')
    
    def hash(self):
        req = self.target.host + '\n'  + self.target.resource + '\n' + self.hashedPayload
        return binascii.hexlify(hashlib.sha256(req.encode('utf-8')).digest()).decode('utf-8')