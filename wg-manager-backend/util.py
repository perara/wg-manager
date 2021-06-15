from loguru import logger
from fastapi import HTTPException
import os
from jinja2 import Environment, FileSystemLoader

templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
jinja_env = Environment(loader=FileSystemLoader(templates_path))


class WGMHTTPException(HTTPException):

    def __init__(self, status_code: int, detail: str = None):
        HTTPException.__init__(self, status_code, detail)
        logger.opt(depth=1).error(detail)
