"""
This type stub file was generated by pyright.
"""

def encode_access_token(identity, secret, algorithm, expires_delta, fresh, user_claims, csrf, identity_claim_key, user_claims_key, json_encoder=..., headers=...):
    """
    Creates a new encoded (utf-8) access token.

    :param identity: Identifier for who this token is for (ex, username). This
                     data must be json serializable
    :param secret: Secret key to encode the JWT with
    :param algorithm: Which algorithm to encode this JWT with
    :param expires_delta: How far in the future this token should expire
                          (set to False to disable expiration)
    :type expires_delta: datetime.timedelta or False
    :param fresh: If this should be a 'fresh' token or not. If a
                  datetime.timedelta is given this will indicate how long this
                  token will remain fresh.
    :param user_claims: Custom claims to include in this token. This data must
                        be json serializable
    :param csrf: Whether to include a csrf double submit claim in this token
                 (boolean)
    :param identity_claim_key: Which key should be used to store the identity
    :param user_claims_key: Which key should be used to store the user claims
    :param headers: valid dict for specifying additional headers in JWT header section
    :return: Encoded access token
    """
    ...

def encode_refresh_token(identity, secret, algorithm, expires_delta, user_claims, csrf, identity_claim_key, user_claims_key, json_encoder=..., headers=...):
    """
    Creates a new encoded (utf-8) refresh token.

    :param identity: Some identifier used to identify the owner of this token
    :param secret: Secret key to encode the JWT with
    :param algorithm: Which algorithm to use for the toek
    :param expires_delta: How far in the future this token should expire
                          (set to False to disable expiration)
    :type expires_delta: datetime.timedelta or False
    :param user_claims: Custom claims to include in this token. This data must
                        be json serializable
    :param csrf: Whether to include a csrf double submit claim in this token
                 (boolean)
    :param identity_claim_key: Which key should be used to store the identity
    :param user_claims_key: Which key should be used to store the user claims
    :param headers: valid dict for specifying additional headers in JWT header section
    :return: Encoded refresh token
    """
    ...

def decode_jwt(encoded_token, secret, algorithms, identity_claim_key, user_claims_key, csrf_value=..., audience=..., leeway=..., allow_expired=..., issuer=...):
    """
    Decodes an encoded JWT

    :param encoded_token: The encoded JWT string to decode
    :param secret: Secret key used to encode the JWT
    :param algorithms: Algorithms allowed to decode the token
    :param identity_claim_key: expected key that contains the identity
    :param user_claims_key: expected key that contains the user claims
    :param csrf_value: Expected double submit csrf value
    :param audience: expected audience in the JWT
    :param issuer: expected issuer in the JWT
    :param leeway: optional leeway to add some margin around expiration times
    :param allow_expired: Options to ignore exp claim validation in token
    :return: Dictionary containing contents of the JWT
    """
    ...

