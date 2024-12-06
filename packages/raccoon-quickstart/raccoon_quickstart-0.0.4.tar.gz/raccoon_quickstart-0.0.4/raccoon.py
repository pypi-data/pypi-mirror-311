import os
import shutil
import subprocess

import click

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
    setup_server(type, language)
    click.echo(get_log_string(type, language))


def setup_server(api_type, language):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    project_dir = f"raccoon-{language}-server"
    source_dir = os.path.join(BASE_DIR, f"examples/{language}/{language}-{api_type}-server")

    shutil.copytree(source_dir, project_dir, dirs_exist_ok=True)

    if language == "node":
        os.chdir(project_dir)
        subprocess.run(["npm", "install"])
    elif language == "python":
        os.chdir(project_dir)
        subprocess.run(["python3", "-m", "venv", "venv"])
        subprocess.run(["./venv/bin/pip", "install", "-r", "requirements.txt"])


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
