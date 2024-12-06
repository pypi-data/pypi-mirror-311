from _pytest.capture import CaptureFixture
from packaging.version import Version

from piplexed.display.print_table import print_installed_table
from piplexed.display.print_table import print_outdated_table
from piplexed.venvs.pipx_venvs import PackageInfo


def test_print_installed_table(capsys: CaptureFixture[str]):
    packages = [
        PackageInfo("A", Version("1.0.1"), python="3.11.3"),
        PackageInfo("B", Version("2.2.1"), python="3.11.3"),
    ]
    print_installed_table(packages, "pipx")

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "Python Version",
    )
    assert output[0].startswith("PIPX Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│            A │             1.0.1 │         3.11.3 │"
    assert output[5] == "│            B │             2.2.1 │         3.11.3 │"
    assert output[6] == "└──────────────┴───────────────────┴────────────────┘"


def test_print_list_outdated(capsys: CaptureFixture[str]):
    packages = [
        PackageInfo("B", Version("1.5.0"), python="3.11.3", latest_pypi_version=Version("1.6.0")),
        PackageInfo("C", Version("2.6.0"), python="3.11.3", latest_pypi_version=Version("3.0a.0")),
    ]

    print_outdated_table(packages, "pipx")

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "PyPI Version",
    )

    assert output[0] == "PIPX Outdated Packages"
    assert all(header in output[2] for header in headers)
    assert output[4] == "│            B │             1.5.0 │        1.6.0 │"
    assert output[5] == "│            C │             2.6.0 │      3.0a0 ⚠ │"
    assert output[6] == "└──────────────┴───────────────────┴──────────────┘"
