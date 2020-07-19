import os
from os.path import isdir
DEFAULT_MODULE_LOCATIONS = [("app.main", "/app/app/main.py"), ("main", "/app/main.py")]
DEFAULT_GUNICORN_CONF = [(None, "/app/gunicorn_config.py"), (None, "/app/startup/gunicorn_config.py")]


def get_location(pot):
    for i in pot:
        if not isdir(i[1]):
            continue
    # Last record will be "defauilt"
    return i[0] if i[0] else i[1]


if __name__ == "__main__":
    MODULE_NAME = os.getenv("MODULE_LOCATION", get_location(DEFAULT_MODULE_LOCATIONS))
    VARIABLE_NAME = os.getenv("VARIABLE_NAME", "app")
    APP_MODULE = os.getenv("APP_MODULE", f"{MODULE_NAME}:{VARIABLE_NAME}")
    GUNICORN_CONF = os.getenv("GUNICORN_CONF", get_location(DEFAULT_GUNICORN_CONF))
    OPTIONS = [
        "--preload",
        "-k",
        "uvicorn.workers.UvicornWorker",
        "-c",
        f"{GUNICORN_CONF} {APP_MODULE}"
    ]

    # Set envs
    os.putenv("VARIABLE_NAME", VARIABLE_NAME)
    os.putenv("APP_MODULE", APP_MODULE)
    os.putenv("GUNICORN_CONF", GUNICORN_CONF)

    os.system(f"gunicorn -k uvicorn.workers.UvicornWorker -c {GUNICORN_CONF} {APP_MODULE}")
