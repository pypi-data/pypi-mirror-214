import typer
from rich.panel import Panel
from rich import print
from thipstercli.config import state, update_config_file
from thipstercli.helpers import (
    get_auth_provider_class,
    get_thipster_module_class_list,
    check_thipster_module_exists,
)

app = typer.Typer(no_args_is_help=True)


@app.command('list')
def _list():
    """List all the supported providers
    """
    state['providers'] = get_thipster_module_class_list('auth')
    provider_display = ''
    for provider in state['providers']:
        provider_display += f'[green]{provider[:-3]}[/green]\n'
    print(Panel(provider_display, title='Providers'))
    __more_info_provider()


@app.command('info')
def info(provider: str):
    """Get information about a provider
    """
    provider = check_provider_exists(provider)

    provider_class = get_auth_provider_class(provider)
    print(Panel(provider_class.__doc__, title=provider))


@app.command('set')
def set(provider: str):
    """Set the provider to use
    """
    provider = check_provider_exists(provider)

    update_config_file(
        {'auth_provider': provider},
    )

    print(f'Provider set to [green]{provider}[/green]')
    __more_info_provider()


@app.command('display')
def display():
    """Display the current provider
    """
    if not state.get('auth_provider', None):
        print('No provider set.\nPlease use [bold]thipster providers set <provider>\
[/bold] to set a provider')
        return
    print(f"Provider set to [green]{state['auth_provider']}[/green]")


def check_provider_exists(provider: str) -> str:
    """Checks if the given provider exists in the providers list
    """
    if not check_thipster_module_exists('auth', provider):
        print(f'Provider [red]{provider.capitalize()}[/red] not found. \
Please use one of the following providers:')
        _list()
        raise typer.Exit(1)

    return provider


def __more_info_provider():
    print(
        Panel('For more information about a provider, run: thipster providers info \
<provider>'),
    ) if state.get('verbose') else None


if __name__ == '__main__':
    app()
