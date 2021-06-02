class SmorestProductionConfig:
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/api"

    # OpenAPI Documentation renderers:
    OPENAPI_REDOC_PATH = "/redoc/"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )

    OPENAPI_RAPIDOC_PATH = "/rapidoc/"
    OPENAPI_RAPIDOC_URL = "https://cdn.jsdelivr.net/npm/rapidoc/dist/rapidoc-min.js"
    # mor config options: https://mrin9.github.io/RapiDoc/api.html
    OPENAPI_RAPIDOC_CONFIG = {"use-path-in-nav-bar": "true"}
    
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


class SmorestDebugConfig(SmorestProductionConfig):
    # do not propagate exceptions in debug mode
    # this makes it hard to test the api and an api client at the same time
    PROPAGATE_EXCEPTIONS = False
