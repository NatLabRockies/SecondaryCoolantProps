from io import StringIO

import pytest
from click.testing import CliRunner

import scp.cli
from scp.api import available_properties
from scp.cli import cli
from scp.water import Water


def test_cli_reports_verbose_property_output() -> None:
    result = CliRunner().invoke(cli, ["--fluid", "water", "--property", "density", "--temperature", "25"])

    assert result.exit_code == 0
    assert "Fluid:    water" in result.output
    assert "Property: density" in result.output
    assert "Units:    [kg/m3]" in result.output


def test_cli_reports_quick_property_output() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--concentration",
            "0.4",
            "--property",
            "density",
            "--temperature",
            "20",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert float(result.output) == pytest.approx(1032.3, rel=0.001)


def test_cli_uses_freeze_point_concentration() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--concentration",
            "0.4",
            "--property",
            "freeze_point",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert float(result.output) == pytest.approx(-20.568, abs=0.01)


def test_cli_reports_all_properties() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--concentration",
            "0.4",
            "--property",
            "all",
            "--temperature",
            "20",
        ],
    )

    assert result.exit_code == 0
    assert "Fluid:         propylene_glycol" in result.output
    assert "Temperature:   20.0 [C]" in result.output
    assert "Concentration: 0.4" in result.output
    for property_name in available_properties():
        assert f"  {property_name}:" in result.output
    assert "  density: 1032." in result.output
    assert "  freeze_point: -20.5" in result.output


def test_cli_reports_all_properties_in_quick_format() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "water",
            "--property",
            "all",
            "--temperature",
            "25",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert "Fluid:" not in result.output
    lines = result.output.splitlines()
    assert len(lines) == len(available_properties())
    assert lines[0].startswith("viscosity: ")
    assert lines[-1] == "freeze_point: 0.0 [C]"


def test_cli_requires_temperature_for_temperature_dependent_property() -> None:
    result = CliRunner().invoke(cli, ["--fluid", "water", "--property", "density"])

    assert result.exit_code == 2
    assert "--temperature is required unless --property is freeze_point" in result.output


def test_cli_zero_mixture_concentration_uses_water(monkeypatch) -> None:
    stderr = StringIO()
    monkeypatch.setattr(scp.cli, "stderr", stderr)

    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "propylene_glycol",
            "--property",
            "density",
            "--temperature",
            "25",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert "Mixture requested, but concentration zero" in stderr.getvalue()
    assert float(result.output) == pytest.approx(Water().density(25.0))


def test_cli_nonzero_water_concentration_uses_water(monkeypatch) -> None:
    stderr = StringIO()
    monkeypatch.setattr(scp.cli, "stderr", stderr)

    result = CliRunner().invoke(
        cli,
        [
            "--fluid",
            "water",
            "--concentration",
            "0.4",
            "--property",
            "density",
            "--temperature",
            "25",
            "--quick",
        ],
    )

    assert result.exit_code == 0
    assert "Pure water requested, but nonzero concentration entered" in stderr.getvalue()
    assert float(result.output) == pytest.approx(Water().density(25.0))
