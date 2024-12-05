import click

from playbook.__version__ import __version__ as version


@click.group()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.version_option(version, "-v", "--version", prog_name="YouQu3", help="查看版本号")
def cli(): ...


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("-pp", "--playbook-json-path", default=None, type=click.STRING,
              help="工作目录")
def playbook(playbook_json_path):
    from playbook.main import playbook
    playbook(playbook_json_path)


if __name__ == '__main__':
    cli()
