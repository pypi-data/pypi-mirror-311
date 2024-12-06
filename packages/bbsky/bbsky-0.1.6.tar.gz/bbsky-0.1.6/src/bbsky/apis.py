import importlib
import inspect
import os
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

import httpx
import typer

from bbsky.constants import API_BASE_URL
from bbsky.data_cls import URL


def api_name_to_url(api_name: str, base_url: Optional[URL] = None) -> URL:
    """
    Convert an API name to a URL.

    Args:
        api_name (str): The name of the API.

    Returns:
        URL: The URL for the API.
    """
    base_url = base_url or API_BASE_URL

    # Add other API names as needed
    if api_name == "crm_constituent":
        return base_url.with_path("crm-conmg")
    else:
        raise ValueError(f"Invalid API name: {api_name}")


def load_detailed_functions() -> (
    Tuple[Dict[str, Callable[..., httpx.Response]], Dict[str, Callable[..., httpx.Response]]]
):
    """
    Dynamically import `asyncio_detailed` and `sync_detailed` functions
    from all Python files in the given directory.
    """
    asyncio_detailed_functions: Dict[str, Callable[..., httpx.Response]] = {}
    sync_detailed_functions: Dict[str, Callable[..., httpx.Response]] = {}

    # Iterate over all Python files in the directory
    base_path = Path(__file__).parent.parent
    api_base_path = base_path / "bbsky/crm_constituent_client/api"
    for py_file in api_base_path.rglob("*.py"):
        try:
            # Dynamically import the module
            import_path = py_file.relative_to(base_path)
            module_name = str(import_path.with_suffix("")).replace(os.sep, ".")
            module = importlib.import_module(module_name)

            # Extract functions if they exist
            module_name_alias = module_name.split(".")[-1]
            if hasattr(module, "asyncio_detailed"):
                asyncio_detailed_functions[module_name_alias] = getattr(module, "asyncio_detailed")
            if hasattr(module, "sync_detailed"):
                sync_detailed_functions[module_name_alias] = getattr(module, "sync_detailed")

        except ImportError:
            pass

    return sync_detailed_functions, asyncio_detailed_functions


sync_functions, asyncio_functions = load_detailed_functions()


def show_api_functions() -> None:
    """
    Display the API functions and their signatures.
    """
    from rich.console import Console
    from rich.table import Table

    signatures = {}
    for name, func in sync_functions.items():
        sig = inspect.signature(func)
        signatures[name] = (sig, func)

    # Display function signatures
    console = Console()
    table = Table(title="API Functions")
    table.add_column("Module", style="cyan")
    table.add_column("Function", style="magenta")
    table.add_column("Parameters", style="green")
    for name, (sig, func) in signatures.items():  # type: ignore
        table.add_row(name, func.__name__, str(sig))  # type: ignore
    console.print(table)


cli = typer.Typer(help="Create and manage Blackbaud Sky API config.")


@cli.command()
def ls(function_type: str = typer.Argument("sync", help="The function type to list (sync or asyncio)")) -> None:
    """
    List all available API functions.
    """
    if function_type == "sync":
        functions = sync_functions
    elif function_type == "asyncio":
        functions = asyncio_functions
    else:
        typer.echo("Invalid function type. Use 'sync' or 'asyncio'.")
        raise typer.Exit()

    for name in functions:
        typer.echo(name)
