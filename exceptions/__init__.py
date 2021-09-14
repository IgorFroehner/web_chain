
class BlockchainException(BaseException):

    def __init__(self, message='Blockchain exception'):
        self.message = message
        super().__init__(self.message)
