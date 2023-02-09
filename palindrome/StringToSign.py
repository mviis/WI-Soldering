import datetime

class StringToSign:
    algorithm=None
    tsTxt=None
    scope=None
    hashedRequest=None

    def __init__(self, credentials, canonicalRequest, utcTs):
        self.algorithm = 'MES1-HMAC-SHA256'
        self.tsTxt = utcTs
        self.scope = credentials.scope()
        self.hashedRequest = canonicalRequest.hash()
    
    def sign(self, signingKey):
        str = self.algorithm + '\n' + self.tsTxt + '\n' + self.scope + '\n' + self.hashedRequest
        return signingKey.sign(str)