import sqlite3

import click
from flask import current_app, g


def get_db():
    """Connects to db if a connection is not already present in app context
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_URI'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

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

    with current_app.open_resource('sqlite/sqlite_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)