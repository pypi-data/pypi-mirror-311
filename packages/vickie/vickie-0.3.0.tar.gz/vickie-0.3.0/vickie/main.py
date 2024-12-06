from vickie.validators import *

class Vickie(ABValidator,
        FValidator,
        NetValidator,
        URIValidator,
        ProductValidator,
        EmailValidator,
        CryptoValidator,
        PhoneValidator):

    def __init__(self):
        pass
