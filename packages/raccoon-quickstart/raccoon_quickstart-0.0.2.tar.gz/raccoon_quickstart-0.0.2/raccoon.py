import click

import application

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('-t', '--type', type=click.Choice(['extract', 'run', 'strict']),
              help='''Type of api project\n
              1 - Extract API\n
              2 - Run API\n
              3 - Strict API''')
@click.option('-l', '--language', type=click.Choice(['node', 'python', 'go']), default='python',
              help='''Options\n
              1 - Node JS Server\n
              2 - Python Fast API server\n
              3 - Go server''')
def setup(type, language):
    application.setup_server(type, language)
    click.echo(get_log_string(type, language))


def get_log_string(api_type, language):
    if language == "node":
        project_string = "Node.js"
        extension_string = ".js"
        directory_string = "raccoon-node-server"
    elif language == "python":
        project_string = "Python"
        extension_string = ".py"
        directory_string = "raccoon-python-server"
    else:
        project_string = "Go"
        extension_string = ".go"
        directory_string = "raccoon-go-server"

    return f"{project_string} project setup complete in '{directory_string}/' with server{extension_string} configured for {api_type.capitalize()} API."
