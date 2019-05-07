# MultiAgent
MultiAgent is an open source framework for the simulation of the multiagent systems in the 2D plane.

# Features
- Agents are implemented as abstract controlling units. They can work without being associated
with any objects that have physical bodies.
- While running the simulation, all data will be automatically saved under the current working directory.
These data can be used to restore the simulation, and they are obviously the perfect resource for further
analysis.

# Documents
Besides the overall README file, you can find the class reference in "mas/",
and the corresponding introduction or tutorial in the independent folder of each examples.

# Get Started
To work with MultiAgent, at first you need to prepare the developing environment according to the following instructions.


## Download MultiAgent
Download MultiAgent and step inside the folder.

	[user @ ~] git clone https://github.com/csningli/MultiAgent.git
	[user @ ~] cd MultiAgent/

## Python Environment
MultiAgent works with Python 3.6. You also need Pygame 1.9.3, Pymunk 5.3.2 and Numpy.

## User Anaconda Environment
If you want to use virtual environment, like Anaconda. It is recommended to create the environment with Python 2.7,
Pygame 1.9.3 and Pymunk 5.3.1. The following command will create and activate environment "mas",
with the necessary packages installed.

	[user @ MultiAgent/] conda env create -f env-py27.yml
	[user @ MultiAgent/] source activate mas

* When using Python without Anaconda, MultiAgent also works under Python 3.6,
in which case you should install the the necessary packages given in env-py36.yml.

## Basic Usage

In a typical instance of the simulation using MultiAgent,
you need to import classses from the mas.multiagent module and instantiate the <b>Simulator</b>
and call its <b>simulate</b> method.

    # you should include the path to MultiAgent, in order to import from "mas"
    # e.x. sys.path.append("path/to/MultiAgent")
    # you need to replace "path/to/MultiAgent" with the actural absolute/relative path to MultiAgent,

	import mas.multiagent

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

The objects and obstacles can be added into an instance of <b>Context</b> when the instance is created.

	obj0 = Object(name = "0")
	obj1 = Object(name = "1")
	context = Context(objs = [obj0, obj1])

It is also convenient to add more objects to <b>context</b> after the instantiation.

	obj2 = Object(name = "2")
	context.add_obj(obj2)

The obstacles can be added in the similar patterns.

	obt0 = Obstacle(name = "0", a = (0.0, 200.0), b = (200.0, 0.0), radius = 2.0)
	obt1 = Obstacle(name = "1", a = (200.0, 0.0), b = (0.0, 200.0), radius = 4.0)
	context = Context(obts = [obt0, obt1])

and

	obt2 = Obstacle(name = "2", a = (0.0, 0.0), b = (200.0, 200.0), radius = 2.0)
	context.add_obt(obt2)

<b>Agent</b> is the core component in MultiAgent 2.0. The instances of <b>Agent</b> can only
be involved in the simulation through <b>schedule</b>.

	schedule = Schedule()
	agent0 = Agent(name = "0")
	schedule.add_agent(agent0)

The instance <b>agent0</b> is associated with the object which has the same name, i.e.\ <b>obj0</b>.
In order to change the states of <b>obj0</b>, <b>agent0</b> should be equipped with
the proper modules. More details can be found in the reference of <b>Agent</b> and <b>Module</b>.


## Follow The Examples
You can explore more details of the usage by looking into the tests (in "tests/") or following the examples (in "examples/").
