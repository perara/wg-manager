import os
from jinja2 import Environment, FileSystemLoader
templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
jinja_env = Environment(loader=FileSystemLoader(templates_path))
