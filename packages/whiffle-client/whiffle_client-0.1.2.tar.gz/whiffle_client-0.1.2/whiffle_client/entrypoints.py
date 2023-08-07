import click
import yaml

from whiffle_client import Client, CONFIG_FILE_PATH


@click.group()
def whiffle():
    pass


@whiffle.command()
@click.argument("file_path")
def run(file_path) -> str:
    """Run task type given a set of parameters.

    \b
    Parameters
    ----------
    file_path : str
        Path to (json|yaml) file containing parameters

    \b
    Returns
    -------
    str
        Name of the launched task
    """
    click.echo(f"run task with params: file_path={file_path}")
    client = Client()
    return client.process(file_path)


@whiffle.command()
@click.argument("key")
@click.argument("value")
def config_edit(key, value) -> str:
    """Edit Whiffle configuration file

    \b
    Parameters
    ----------
    key : str
        Dot separated key value (e.g.: user.token)
    value : str
        Value to fill the configuration key with
    """
    config_key = key.split(".")
    with open(CONFIG_FILE_PATH) as file_object:
        config = yaml.safe_load(file_object)

    sub_config = config
    for sub_key in config_key[:-1]:
        if sub_key in sub_config:
            sub_config = sub_config[sub_key]
        else:
            raise KeyError(f"Key {sub_key} does not exist")
    try:
        if config_key[-1] not in sub_config:
            raise KeyError
        sub_config[config_key[-1]] = value
    except KeyError:
        raise KeyError(f"Key {config_key[-1]} does not exist")

    with open(CONFIG_FILE_PATH, "w") as file_object:
        yaml.safe_dump(config, file_object)

    click.echo(f"{key} changed to {value}")


@whiffle.command()
def config_list():
    """List configuration values"""

    with open(CONFIG_FILE_PATH) as file_object:
        config = yaml.safe_load(file_object)

    click.echo("Current configuration:\n-----\n")
    click.echo(yaml.safe_dump(config))
    click.echo("-----")
