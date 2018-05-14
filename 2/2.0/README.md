# MultiAgent 2.0
In a typical instance of the simulation using MultiAgent 2.0,
one need to instantiate the <b>Simulator</b> and call its <b>simulate</b> method.

	sim = Simulator(...)
	sim.simulate(...)

When calling method <b>simulate</b>, several arguments can be configured to custom the simulation,
like <b>graphics</b> and <b>filename</b>.

The argument <b>graphics</b> takes boolean values and by default it have value <b>False</b>,
which means the simulation will run without any graphical display (i.e.\ no graphical window).
If you want to watch the simulating process and manually interact with it, the argument <b>graphics</b>
should be explicitly set to <b>True</b>.

 	sim.simulate(graphics = True)

# Class Reference

## Simulator
