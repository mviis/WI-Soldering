import datetime
from palindrome.SigningKey import *
from palindrome.CanonicalRequest import *
from palindrome.UtcTimestamp import *
from palindrome.StringToSign import *

class AuthorizationHeader:
    algorithm="MES1-HMAC-SHA256"
    credentials=None
    signature=None
    target=None
    utcTs=None
    
    def __init__(self, utcTs, credentials, signature, target):
        self.utcTs = utcTs
        self.credentials = credentials
        self.signature = signature
        self.target = target
    
    @staticmethod
    def from_(secret, credentials, target, payload):
        return AuthorizationHeader.fromTs(secret, credentials, target, payload, UtcTimestamp(datetime.datetime.utcnow()).serialize())
    
    @staticmethod
    def fromTs(secret, credentials, target, payload, ts):
        signingKey = SigningKey.from_(secret, credentials.utcDate, credentials.service)
        cr = CanonicalRequest(target, payload)
        sts = StringToSign(credentials, cr, ts)
        return AuthorizationHeader(sts.tsTxt, credentials, sts.sign(signingKey), target)

    def serialize(self):
        return self.algorithm + ' Credential=' + self.credentials.serialize() + ', Signature=' + self.signature + ', ' + self.target.serialize() + ', Utc=' + self.utcTs