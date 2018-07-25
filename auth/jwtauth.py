from flask import redirect, url_for, current_app, request, make_response, g
from functools import wraps
import jwt
from jwt.exceptions import PyJWTError
import time
import base64
import datetime
import calendar
import uuid

from flask_cot.auth.models.user import User


class Jwt:
    # id is used to validate that a token is valid. After parsing, if id is
    # set then the token is good.
    """
    auto_parse
        on create will look in headers & cookie for a token and parse
        with a silent failure
    allow_expired
        allows a 1yr leeway when parsing any token
    fail_silently
        does the parsing 'in the background'. If False then we throw Exceptions
    """
    def __init__(
            self,
            auto_parse=True,
            allow_expired=False,
            fail_silently=True
            ):
        self.reset()
        if auto_parse:
            self.parse_from_inputs(
                allow_expired=allow_expired,
                fail_silently=fail_silently
            )

    def new(
            self,
            user_id=None,
            org_id=None,
            id=str(uuid.uuid4())
            ):
        self.reset
        self.id = id
        self.user_id = user_id
        self.org_id = org_id

    def reset(self):
        # 'internal' variable types
        # id of the token, think along the lines of a session id
        self.id = None
        # set if the token is valid, apart from being expired
        self._is_expired = False
        # defaul validity is 24hrs
        self._validity_seconds = 86400
        # issued at time - unix epoch
        self.iat = 0
        # expiry epoch
        self.exp = 0
        self._last_error = None

        # universal external variables
        self.user_id = None
        self.org_id = None
        self.groups = []

        # external variable array used
        self.token_data = {}

    def add_token_data(self, key, value):
        self.token_data.update({key: value})

    def merge_token_data(self, data_dict):
        self.token_data.update(data_dict)

    def set_valid_seconds(self, seconds):
        self._validity_seconds = int(seconds)

    def get_user_id(self):
        return self.user_id

    def get_user(self):
        if self.user_id is None:
            return None
        user = User(self.user_id)
        return user

    def build(self):
        print('build='+self.id)
        params = {
            'id': self.id,
            'iat': self.iat,
            'exp': self.exp,
            'org_id': self.org_id,
            'user_id': self.user_id,
            'groups': self.groups,
            'token_data': {}
        }
        params['token_data'].update(self.token_data)
        future = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=self._validity_seconds
            )
        params["exp"] = calendar.timegm(future.timetuple())
        self.exp = params["exp"]
        params["iat"] = datetime.datetime.utcnow()
        self.iat = params["iat"]

        token = str(jwt.encode(
            params,
            current_app.secret_key,
            algorithm='HS256'
        ))
        # trim the b' and ' from the string'
        return token[2:-1]

    def parse_from_inputs(self, allow_expired=True, fail_silently=False):
        auth = None
        # could be in a header
        if "Authorization" in request.headers:
            auth = request.headers.get('Authorization')
        # could also be in a cookie
        elif "Authorization" in request.cookies:
            auth = request.cookies.get('Authorization')

        if auth is None:
            # how are we reporting this failure
            if fail_silently:
                # we leave id as None
                self.id = None
                self._last_error = 'MISSING_AUTH_HEADER'
                return
            else:
                raise MissingTokenException(
                    'Authorization not in header or cookie'
                )

        # we have a possible auth string.
        if auth.startswith("Basic "):
            auth = base64.b64decode(auth[6:]).decode('utf-8')
        if auth.startswith("Bearer: "):
            auth = auth[8:]
        elif auth.startswith("Bearer:"):
            auth = auth[7:]
        else:
            if fail_silently:
                self.id = None
                self._last_error = 'AUTH_HEADER_MALFORMED'
                return
            else:
                raise MalformedAuthorizationException(
                    'Authorization malformed'
                )
        self.parse_token(auth, allow_expired, fail_silently)

    def parse_token(self, token, allow_expired=False, fail_silently=False):
        try:
            decoded = jwt.decode(
                token,
                current_app.config['JWTAUTH_SECRET'],
                algorithm='HS256',
                verify_signature=True
            )
            self._decoded_to_object(decoded)
        except jwt.exceptions.InvalidSignatureError:
            if fail_silently:
                self.id = None
                self._last_error = 'INVALID_SIGNATURE'
                return
            else:
                raise MalformedTokenException(
                    'Token malformed'
                )
        except jwt.exceptions.ExpiredSignatureError:
            if allow_expired:
                self.parse_expired_token(token, fail_silently=fail_silently)
                return

            if fail_silently:
                self.id = None
                self._last_error = 'EXPIRED_SIGNATURE'
                return
            else:
                raise ExpiredTokenException(
                    'Token Expired'
                )
        except PyJWTError as e:
            if fail_silently:
                self.id = None
                self._last_error = 'PARSE_ERROR'
                return
            else:
                raise JwtauthException(
                    'Token Parse Problem'
                )

    def parse_expired_token(self, token, fail_silently):
        try:
            decoded = jwt.decode(
                token,
                current_app.config['JWTAUTH_SECRET'],
                algorithm='HS256',
                verify_signature=True,
                leeway=31536000
            )
            self._decoded_to_object(decoded)
            self._is_expired = True
        except jwt.exceptions.InvalidSignatureError:
            if fail_silently:
                # we leave id as None
                self.id = None
                self._last_error = 'INVALID_SIGNATURE'
                return
            else:
                raise MalformedTokenException(
                    'Token malformed'
                )
        except jwt.exceptions.ExpiredSignatureError:
            if fail_silently:
                self.id = None
                self._last_error = 'EXPIRED_SIGNATURE'
                return
            else:
                raise ExpiredTokenException(
                    'Token Expired'
                )
        except PyJWTError as e:
            if fail_silently:
                self.id = None
                self._last_error = 'PARSE_ERROR'
                return
            else:
                raise JwtauthException(
                    'Token Parse Problem'
                )

    def _decoded_to_object(self, decoded):
        self.token_data = decoded['token_data']
        self.id = decoded['id']
        self.user_id = decoded['user_id']
        self.org_id = decoded['org_id']
        self.groups = decoded['groups']
        self.iat = decoded['iat']
        self.exp = decoded['exp']

    def is_group_member(self, group_required):
        if not self.id:
            return False
        if str(group_required) in self.groups:
            return True
        else:
            return False


class JwtauthException(Exception):
    # Base class for all exceptions
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_string(self):
        return "Exception message=" + self.message


class ExpiredTokenException(JwtauthException):
    # Token is valid but has expired
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )


class MissingTokenException(JwtauthException):
    # Token is valid but has expired
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )


class MalformedTokenException(JwtauthException):
    # Token is valid but has expired
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )


class MalformedAuthorizationException(JwtauthException):
    # Token is valid but has expired
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )


class InsufficientGroupMembershipException(JwtauthException):
    # Token is valid but has expired
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )


def requires_login(allow_expired=False, group_required=None):
    """
    To be used be web pages where a redirection to a login page is required
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.jwtauth.id:
                if allow_expired:
                    g.jwtauth = Jwt(allow_expired=True)
                    if not g.jwtauth.id:
                        return redirect_handler()
                else:
                    return redirect_handler()
            if group_required:
                if not g.jwtauth.is_group_member(group_required):
                    return redirect_handler(is_group_member=True)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def requires_token(allow_expired=False, group_required=None):
    """
    To be used by a jsonapi endpoint
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.jwtauth.id:
                if allow_expired:
                    g.jwtauth = Jwt(allow_expired=True)
                    if not g.jwtauth.id:
                        return exception_handler()
                else:
                    return exception_handler()

            return f(*args, **kwargs)
        return wrapped
    return wrapper


def exception_handler():
    return g.response_wrapper()


def redirect_handler(is_expired=False, is_group_member=False):
    return redirect(
        redirect_builder(
            is_expired=is_expired,
            is_group_member=is_group_member
        )
    )


def redirect_builder(is_expired=False, is_group_member=False):
    """ Builds the URL for the page to redirect to, complete with extra
    params to help construct
    """
    query_params = {}
    if current_app.config['JWTAUTH_LOGIN_FAIL_REDIRECT_APPEND_REDIRECT']:
        query_params.update(
          {'redirect': url_for(request.endpoint, **request.args.to_dict())}
        )
    if current_app.config['JWTAUTH_LOGIN_FAIL_REDIRECT_APPEND_CODE']:
        if is_expired:
            query_params.update(
              {'code': 'LOGIN_EXPIRED'}
            )
        elif is_group_member:
            query_params.update(
              {'code': 'INSUFFICIENT_SECURITY'}
            )
        else:
            query_params.update(
              {'code': 'LOGIN_REQUIRED'}
            )
    if current_app.config['JWTAUTH_LOGIN_FAIL_REDIRECT_APPEND_TIMESTAMP']:
        query_params.update(
          {'timestamp': int(time.time())}
        )
    return url_for(
        current_app.config['JWTAUTH_LOGIN_FAIL_REDIRECT_ROUTE'],
        **query_params)
