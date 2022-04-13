class GfycatClientError(Exception):
    def __init__(self, error_message, status_code=None, response_data=None):
        self.status_code = status_code
        self.error_message = error_message
        self.response_data = response_data
    
    def __str__(self):
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message