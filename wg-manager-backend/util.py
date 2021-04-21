from jinja2 import Environment, PackageLoader
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))
