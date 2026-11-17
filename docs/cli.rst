Command Line Usage
==================

This library comes with a command line interface.
Once this library is pip installed, a new binary executable will be available with the name ``scprop``.
The command has a help argument with output similar to this (execute manually to verify latest syntax)::

    $ scprop --help
    Usage: scprop [OPTIONS]

    Options:
      -f, --fluid [water|ethyl_alcohol|ethylene_glycol|methyl_alcohol|propylene_glycol]
                                      Which fluid to use?  [required]
      -x, --concentration FLOAT RANGE
                                      Mixture concentration fraction. Default 0.0.
                                      [0.0<=x<=1.0]
      -p, --property [viscosity|specific_heat|density|conductivity|prandtl|thermal_diffusivity|freeze_point|all]
                                      Which fluid property to evaluate, or "all"
                                      to report every property.
                                      [required]
      -t, --temperature FLOAT         Fluid temperature, in degrees Celsius. Required
                                      unless evaluating freeze_point.
      -q, --quick                     Just report the value(s), good for scripts
      --help                          Show this message and exit.

Some example usages::

    $ scprop --fluid water --property density --temperature 25
    Fluid:    water
    Property: density
    Value:    997.0448954179155
    Units:    [kg/m3]

    $ scprop --fluid water --property density --temperature 25 --quick
    997.0448954179155

    $ scprop --fluid ethylene_glycol --concentration 0.3 --property specific_heat --temperature 40
    Fluid:    ethylene_glycol
    Property: specific_heat
    Value:    3775.3537088494118
    Units:    [J/kg-K]

    $ scprop --fluid propylene_glycol --concentration 0.4 --property freeze_point --quick
    -20.567737840000002

    $ scprop --fluid propylene_glycol --concentration 0.4 --temperature 20 --property all
    Fluid:         propylene_glycol
    Temperature:   20.0 [C]
    Concentration: 0.4
    Properties:
      viscosity: 0.004383780258156793 [Pa-s]
      specific_heat: 3706.7225654037834 [J/kg-K]
      density: 1032.2726598927813 [kg/m3]
      conductivity: 0.4002618298979319 [W/m-K]
      prandtl: 40.59706919549404 [-]
      thermal_diffusivity: 1.0460674042783235e-07 [m2/s]
      freeze_point: -20.567777108809345 [C]

Note that the fluid argument must be from the list of supported fluids, and the property must be from the list of supported properties.
Both of these are available from the help message.
For glycol mixtures, the glycol concentration is a decimal value.
The temperature input value is in Celsius and is required for all properties except ``freeze_point``.
Use ``--property all`` to evaluate every supported property in one command.  The temperature is used for the
temperature-dependent properties, and the concentration is used for ``freeze_point``.

By default the output is a nice summary, but there is a quick option that just reports the value.
For ``--property all``, quick output contains one labeled property per line.
The quick output is a nice integration into some workflows that would require the CLI.

For interactive bash sessions, there is a tab-completion capability available.
Simply add the following line to the ``.bashrc`` file, or execute it manually in the current session to apply it temporarily::

    eval "$(_SCPROP_COMPLETE=bash_source scprop)"

Enabling this will turn on tab completion for the different argument names, as well as the supported fluid and property names.
