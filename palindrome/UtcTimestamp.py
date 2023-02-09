class UtcTimestamp:
    ts=None
    def __init__(self, ts):
        self.ts = ts
    
    def serialize(self):
        return '{:%Y%m%dT%H:%M:%S}'.format(self.ts)