class TargetResource:
    host=None
    resource=None
    def __init__(self, host, resource):
        self.host = host
        self.resource = resource
    
    def serialize(self):
        if len(self.host) == 0 or len(self.resource) == 0:
            return ''
        return 'Host=' + self.host + ', Resource=' + self.resource