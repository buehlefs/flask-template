"""
This type stub file was generated by pyright.
"""

def verify_jwt_in_request():
    """
    Ensure that the requester has a valid access token. This does not check the
    freshness of the access token. Raises an appropiate exception there is
    no token or if the token is invalid.
    """
    ...

def verify_jwt_in_request_optional():
    """
    Optionally check if this request has a valid access token.  If an access
    token in present in the request, :func:`~flask_jwt_extended.get_jwt_identity`
    will return  the identity of the access token. If no access token is
    present in the request, this simply returns, and
    :func:`~flask_jwt_extended.get_jwt_identity` will return `None` instead.

    If there is an invalid access token in the request (expired, tampered with,
    etc), this will still raise the appropiate exception.
    """
    ...

def verify_fresh_jwt_in_request():
    """
    Ensure that the requester has a valid and fresh access token. Raises an
    appropiate exception if there is no token, the token is invalid, or the
    token is not marked as fresh.
    """
    ...

def verify_jwt_refresh_token_in_request():
    """
    Ensure that the requester has a valid refresh token. Raises an appropiate
    exception if there is no token or the token is invalid.
    """
    ...

def jwt_required(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called. This
    does not check the freshness of the access token.

    See also: :func:`~flask_jwt_extended.fresh_jwt_required`
    """
    ...

def jwt_optional(fn):
    """
    A decorator to optionally protect a Flask endpoint

    If an access token in present in the request, this will call the endpoint
    with :func:`~flask_jwt_extended.get_jwt_identity` having the identity
    of the access token. If no access token is present in the request,
    this endpoint will still be called, but
    :func:`~flask_jwt_extended.get_jwt_identity` will return `None` instead.

    If there is an invalid access token in the request (expired, tampered with,
    etc), this will still call the appropriate error handler instead of allowing
    the endpoint to be called as if there is no access token in the request.
    """
    ...

def fresh_jwt_required(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid and fresh access token before allowing the endpoint to be
    called.

    See also: :func:`~flask_jwt_extended.jwt_required`
    """
    ...

def jwt_refresh_token_required(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid refresh token before allowing the endpoint to be called.
    """
    ...

