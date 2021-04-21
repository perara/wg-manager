from loguru import logger
from fastapi import HTTPException
from jinja2 import Environment, PackageLoader
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))


class WGMHTTPException(HTTPException):

    def __init__(self, status_code: int, detail: str = None):
        HTTPException.__init__(self, status_code, detail)
        logger.opt(depth=1).error(detail)