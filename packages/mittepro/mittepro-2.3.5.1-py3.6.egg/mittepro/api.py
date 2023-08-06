import json
import logging
import arrow
import requests
from apysignature.query_encoder import QueryEncoder
from apysignature.signature import Request as Request_sig, Token
from requests import Request, Session, ReadTimeout, ConnectTimeout, HTTPError
from .utils import is_json
from .mitte_exceptions import APIError, TimeOutError

__version__ = '2.3.5.1'
logging.basicConfig(format='%(asctime)s %(message)s')


def endpoint(method, endpoint):
    """ endpoint-decorator """
    def decorator(func):
        def wrapped(self, *args, **kwargs):
            self.http_method = method
            self.endpoint = endpoint
            return func(self, *args, **kwargs)
        return wrapped
    return decorator


class Api(object):
    """ Classe base para envio de requisições """

    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'

    server_uri = ''
    urls = {}
    headers = {}
    endpoint = ''
    http_method = ''

    _api_key = ''
    _api_secret = ''

    def __init__(self, fail_silently=False, timeout_read=15):
        self._session = Session()
        self.timeout_read = timeout_read
        self.fail_silently = fail_silently

    def set_header(self, header):
        """
        :type header: dict
        :return:
        """
        self.headers.update(header)

    def get_headers(self):
        return self.headers

    def query_encode(self, url, payload):
        if '?' not in url:
            url += '?'
        else:
            url += '&'
        for key, value in payload.items():
            url += QueryEncoder.encode_param(key, str(value)) + '&'
        return url.rstrip('&')

    def sign_request(self, auth_timestamp=None):
        request = Request_sig(self.http_method, self.endpoint, {})
        token = Token(self._api_key, self._api_secret)
        auth = request.sign(token)
        return auth

    def correct_auth_timestamp(self, msg_error, payload):
        substring = 'Server time: '
        server_timestamp = msg_error[msg_error.index(substring) + len(substring):]
        server_arw = arrow.get(int(server_timestamp))
        right_timestamp = arrow.now().replace(hour=int(server_arw.format('HH'))).timestamp
        return self.request(payload=payload, auth_timestamp=right_timestamp)

    def send_request(self, url, payload):
        timeout = (10, self.timeout_read)
        if payload and self.http_method == 'GET':
            response = requests.get(url, payload, timeout=timeout)
        else:
            request = Request(
                self.http_method, url,
                json=payload,
                headers=self.headers
            )
            prepped = request.prepare()
            response = self._session.send(prepped, timeout=timeout)

        valid_codes = (200, 201)
        if hasattr(response, 'status'):
            status_code = response.status
        else:
            status_code = response.status_code

        if response and status_code in valid_codes and response.text:
            return json.loads(response.text)
        else:
            log = f"EXTERNAL API: request error: {response.reason}"
            logging.info(log)
            if is_json(response.text):
                content = json.loads(response.text)
                msg = content['error'] if 'error' in content else content['detail']
            else:
                msg = response.text[0:response.text.index('Request Method')].strip()
            if 'Timestamp expired' in msg:
                return self.correct_auth_timestamp(msg, payload)
            elif not self.fail_silently:
                raise APIError(message_values=(msg.encode('utf8'),))
            else:
                return {'error': msg.encode('utf8')}

    def request(self, payload=None, auth_timestamp=None):
        url = self.server_uri + self.endpoint
        # Generate and sign request URL
        auth = self.sign_request(auth_timestamp)
        if auth:
            url = self.query_encode(url, auth)

        log = f'EXTERNAL API: sending request on {url}'
        logging.info(log)
        try:
            return self.send_request(url, payload)
        except ReadTimeout as err:
            log = f"EXTERNAL API: request error: {err}"
            logging.info(log)
            if not self.fail_silently:
                raise TimeOutError(message_values=(str(self.timeout_read),))
            return {'error': f"""The server did not respond within the time you stipulated.
                    The time was {str(self.timeout_read)} second(s)"""}
        except (ConnectTimeout, HTTPError) as err:
            log = f"EXTERNAL API: request error: {err}"
            logging.info(log)
            if not self.fail_silently:
                raise err
            else:
                return {'error': f"{err}"}
