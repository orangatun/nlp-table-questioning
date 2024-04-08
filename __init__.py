import os

from flask import Flask

from .config import ( DevConfig, ProdConfig )

def create_app(test_config=None):
    """ creates and configures the app. 
    Loads configuration from `config.py` based on `FLASK_ENV` value in `.flaskenv` file in repository root.
    """
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists(app.instance_path+"/uploads"):
        os.mkdir(app.instance_path+"/uploads")

    if test_config is None:
        # load the instance config from `config.py`, when not testing
        run_env = os.environ.get('FLASK_ENV')
        if run_env=='production':
            app.config.from_object(ProdConfig())
        elif run_env=='development':
            app.config.from_object(DevConfig())
        else:
            pass
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    app.config['instance_path'] = app.instance_path

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from .sqlite import sqlite_db
    sqlite_db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)


    from . import home
    app.register_blueprint(home.bp)

    return app