from os import getcwd
from pathlib import Path
from typing import Optional

from flask import Flask

from .api import API
from .context import Context
from .handle_error import handle_error


def create_app(context: Context, static_folder_path: Optional[str]) -> Flask:
    api: API = API(context)

    static_folder: str = static_folder_path if static_folder_path else Path(getcwd()).joinpath('static')

    app = Flask(import_name=__name__,
                static_folder=static_folder,
                static_url_path='/static')

    app.register_blueprint(api.blueprint, url_prefix='/api/v1')
    app.register_error_handler(Exception, lambda error: handle_error(app.logger, error))

    return app
