
class ConfigFail(Exception):

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, "[config error] "+msg)

    def get_message(self):
        return self.msg
