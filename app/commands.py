# commands.py --------------------------------------------------------------------------------------
#
# Description:
#    Commands module. Each command is initialized in the app factory located in app.py
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Commands table of contents
# ==================================================================================================
# Search the Commands based on the following patterns (comments)
#
# | Pattern              | Command | Description
# |----------------------|---------|---------------------------------------------------------------
# | --- (command 01) --- | clean   | Removes all python's binary files from the project
# | --- (command 02) --- | urls    | Prints all the Flask Routes


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
import os
# Installed
import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound
# Custom
from app.config.settings import Config


# ==================================================================================================
# Main
# ==================================================================================================
#
# --- (command 01) ---
@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at project's directory"""
    # Find all files inside the project directory
    for dirpath, _, filenames in os.walk(Config.PROJECT_ROOT):
        # Iterate through each file
        for filename in filenames:
            # If file's extension is python's binary remove it
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


# --- (command 02) ---
@click.command()
@click.option('-u', '--url', default=None, help='Url to test (ex. /static/image.png)')
@click.option('-o', '--order', default='rule', help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project"""
    # Initialize Parameters
    results = []
    header = ('Rule', 'Endpoint', 'Arguments')
    # If argument url is given change the searging scope
    if url:
        try:
            rule, arguments = (current_app.url_map.bind('localhost').match(url, return_rule=True))
            results.append((rule.rule, rule.endpoint, arguments))
            no_of_colums = 3
        except (NotFound, MethodNotAllowed) as e:
            results.append(('<{}>'.format(e), None, None))
            no_of_colums = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        for rule in rules:
            results.append((rule.rule, rule.endpoint, None))
        no_of_colums = 2

    # Initialize Table
    str_template = ''
    table_width = 0
    # Initialize Rule Column
    if no_of_colums >= 1:
        max_rule_length = max(len(r[0]) for r in results)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length
    # Initialize Endpoint Column
    if no_of_colums >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in results)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length
    # Initialize Arguments Column
    if no_of_colums >= 3:
        max_arguments_length = max(len(str(r[2])) for r in results)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    # Print Results
    click.echo('')
    # Print Header
    click.echo(str_template.format(*header[:no_of_colums]))
    click.echo('-' * table_width)
    for row in results:
        # Stringify dictionaries (arguments column)
        stringify = [str(x) for x in row]
        click.echo(str_template.format(*stringify[:no_of_colums]))
    click.echo('')
