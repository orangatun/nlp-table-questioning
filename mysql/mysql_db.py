import pymysql

import click
from flask import current_app, g


def get_db():
    """Connects to db if a connection is not already present in app context
    """
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['DATABASE_HOST'], 
            user=current_app.config['DATABASE_USER'], 
            password=current_app.config['DATABASE_PASS'],
            database=current_app.config['DATABASE_DB'],
            charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
        )

    return g.db


def close_db(e=None):
    """Closes db connection
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Executes dropping of tables and creation as per schema.
    """
    db = get_db()

    with current_app.open_resource('mysql/mysql_schema.sql') as f:
        for line in f:
            db.cursor().execute(line)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)