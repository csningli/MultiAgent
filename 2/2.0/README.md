# MultiAgent 2.0
In a typical instance of the simulation using MultiAgent 2.0,
one need to instantiate the <b>Simulator</b> and call its <b>simulate</b> method.

	sim = Simulator(...)
	sim.simulate(...)

When calling method <b>simulate</b>, several arguments can be configured to custom the simulation,
like <b>graphics</b> and <b>filename</b>.

The argument <b>graphics</b> takes boolean values and by default it has value <b>False</b>,
which means the simulation will run without any graphical display (i.e.\ no graphical window).
If you want to watch the simulating process and manually interact with it, the argument <b>graphics</b>
should be explicitly set to <b>True</b>.

 	sim.simulate(graphics = True)

The argument <b>filename</b> takes string values or <b>None</b> (the default value).
If the <b>filename</b> is set to a non-empty string, then the simulator will treat it as
the path of preferred data file and look for the file (the simulator will create the file
if it doesn't exist). Then the simulation will be restored according to the valid data
in the file (nothing restored if there is no valid records).
If you continue with the restored simulation,
all the new generated data will be saved in the given file.

 	sim.simulate(filename = "multiagent.data")

If <b>filename</b> is left (or set to) <b>None</b>, then a file will be automatically generated and
named with the information of the beginning time.

 	sim.simulate(filename = None)

If <b>filename</b> is set to empty, i.e.\ <b>""</b>, then the simulation data will not be saved.

 	sim.simulate(filename = "")

When a new instance of <b>Simulator</b> is created, you must provide a valid value for the argument
<b>driver</b>, which takes instances of <b>Driver</b> as values.

	driver = Driver(...)
	sim = Simulator(driver = driver)

To instantiate <b>Driver</b>, the values for two arguments <b>context</b> and <b>schedule</b> should
be provided. Briefly speaking, <b>context</b> is an instance of <b>Context</b> and it contains
all the statical information about the physical environment for the simulation (like objects with
physical bodies and obstacles). The other argument <b>schedule</b> is an instance of <b>Schedule</b> and
contains the objects/obstacles/agents that will be dynamically added during the simulation.

	context = Context(...)
	schedule = Schedule(...)
	driver = Driver(context = context, schedule = schedule)

# Class Reference

## Simulator
