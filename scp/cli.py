from sys import stderr

import click

from scp.api import available_fluids, available_properties, get_fluid
from scp.base_fluid import BaseFluid

# Add this to .bashrc for nice completion: eval "$(_SCPROP_COMPLETE=bash_source scprop)"

fluid_options = click.Choice(available_fluids(include_user_defined=False))
prop_options = click.Choice((*available_properties(), "all"))
x_range = click.FloatRange(min=0.0, max=1.0)


def _property_result(
    fluid: BaseFluid,
    fluid_prop: str,
    temperature: float | None,
    concentration: float,
) -> tuple[float, str]:
    if fluid_prop == "freeze_point":
        value = getattr(fluid, fluid_prop)(concentration)
    else:
        value = getattr(fluid, fluid_prop)(temperature)
    units = getattr(fluid, f"{fluid_prop}_units")()
    return value, units


@click.command(name="SecondaryCoolantPropsCommandLine")
@click.option(
    "-f",
    "--fluid",
    type=fluid_options,
    required=True,
    default="water",
    help="Which fluid to use?",
)
@click.option(
    "-x",
    "--concentration",
    type=x_range,
    required=False,
    default=0.0,
    help="Mixture concentration fraction. Default 0.0.",
)
@click.option(
    "-p",
    "--property",
    "fluid_prop",
    type=prop_options,
    required=True,
    help='Which fluid property to evaluate, or "all" to report every property.',
)
@click.option(
    "-t",
    "--temperature",
    type=float,
    required=False,
    help="Fluid temperature, in degrees Celsius. Required unless evaluating freeze_point.",
)
@click.option(
    "-q",
    "--quick",
    is_flag=True,
    show_default=True,
    default=False,
    help="Just report the value(s), good for scripts",
)
def cli(fluid: str, concentration: float, fluid_prop: str, temperature: float | None, quick: bool):
    if fluid_prop != "freeze_point" and temperature is None:
        raise click.UsageError("--temperature is required unless --property is freeze_point")

    if concentration == 0.0 and fluid != "water":
        print(
            "Mixture requested, but concentration zero, assuming water and continuing",
            file=stderr,
        )
    elif concentration > 0.0 and fluid == "water":
        print(
            "Pure water requested, but nonzero concentration entered, assuming water and continuing",
            file=stderr,
        )
    if fluid == "water" or concentration == 0.0:
        f = get_fluid("water")
        fluid = "water"
    else:
        f = get_fluid(fluid, concentration=concentration)

    if fluid_prop == "all":
        results = [
            (property_name, *_property_result(f, property_name, temperature, concentration))
            for property_name in available_properties()
        ]
        if quick:
            for property_name, value, units in results:
                print(f"{property_name}: {value} [{units}]")
        else:
            print(f"Fluid:         {fluid}")
            print(f"Temperature:   {temperature} [C]")
            print(f"Concentration: {concentration}")
            print("Properties:")
            for property_name, value, units in results:
                print(f"  {property_name}: {value} [{units}]")
        return

    value, units = _property_result(f, fluid_prop, temperature, concentration)
    if quick:
        print(value)
    else:
        print(f"Fluid:    {fluid}\nProperty: {fluid_prop}\nValue:    {value}\nUnits:    [{units}]")
