class ClientCredentials:
    clientId=None
    utcDate=None
    service=None
    def __init__(self, clientId, utcDate, service):
        self.clientId = clientId
        self.utcDate = utcDate
        self.service = service
    
    def scope(self):
        return self.utcDate + '/' + self.service + '/' + 'mes1_request'
    
    def serialize(self):
        return self.clientId + '/' + self.scope()