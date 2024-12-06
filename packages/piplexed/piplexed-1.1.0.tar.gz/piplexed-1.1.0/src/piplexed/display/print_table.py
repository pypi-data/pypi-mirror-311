from __future__ import annotations

from collections.abc import Iterable

from rich import print as rich_print
from rich.table import Table
from rich.text import Text

from piplexed.venvs import PackageInfo


def print_installed_table(packages: Iterable[PackageInfo], tool: str) -> None:
    table = Table(title=f"{tool.upper()} Packages")
    table.add_column("Package Name", justify="right", style="dark_orange", no_wrap=True)
    table.add_column("Installed Version", justify="right", style="deep_sky_blue1", no_wrap=True)
    table.add_column("Python Version", justify="right", style="green4", no_wrap=True)

    for pkg in packages:
        table.add_row(f"{pkg.name}", f"{pkg.version}", f"{pkg.python}")

    rich_print(table)


def print_outdated_table(package_data: Iterable[PackageInfo], tool: str) -> None:
    table = Table(title=f"{tool.upper()} Outdated Packages")
    table.add_column("Package Name", justify="right", style="dark_orange", no_wrap=True)
    table.add_column("Installed Version", justify="right", style="deep_sky_blue1", no_wrap=True)
    table.add_column("PyPI Version", justify="right", style="red3", no_wrap=True)

    for pkg in package_data:
        pypi_info = Text(f"{pkg.latest_pypi_version}", "green1")
        if pkg.latest_pypi_version is not None and pkg.latest_pypi_version.is_prerelease:
            pypi_info.append(" ⚠", "bright_yellow")

        table.add_row(pkg.name, f"{pkg.version}", pypi_info)

    rich_print(table)
