# -*- coding: utf-8 -*-
import six


class BaseError(Exception):
    """ Erro Base """
    def __init__(self, message=None, codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if six.PY2:
            super(Exception, self).__init__(message)
        else:
            super().__init__(message)


class InvalidParam(BaseError):
    """ MitteProError - Parâmetro {0} é inválido. Razão: {1} """
    def __init__(self, message="MitteProError - Parâmetro {0} é inválido. Razão: {1}", codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(InvalidParam, self).__init__(message)
        else:
            super().__init__(message)


class APIError(BaseError):
    """ MitteProError. Razão: {0} """
    def __init__(self, message="MitteProError. Razão: {0}", codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(APIError, self).__init__(message)
        else:
            super().__init__(message)


class TimeOutError(BaseError):
    """
        MitteProError. Razão: O servidor não respondeu dentro do tempo que você estipulou. "
        O tempo foi de {0} segundo(s)
    """
    def __init__(self, message="MitteProError. Razão: O servidor não respondeu dentro do tempo que você estipulou. "
                               "O tempo foi de {0} segundo(s)", codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        super().__init__(message)


class ImproperlyConfigured(BaseError):
    """ MitteProError. Configuração inapropriada. Razão: {0} """
    def __init__(self, message="MitteProError. Configuração inapropriada. Razão: {0}", codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(ImproperlyConfigured, self).__init__(message)
        else:
            super().__init__(message)
