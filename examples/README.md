# MultiAgent Examples

\* Before running any example, make sure you have created and activated the Anaconda environment
"mas" as instructed in "MultiAgent/README.md".

## Run An Example
To run an example, say "amoebot", you need to at first change directory into "examples/amoebot".
There is a README file for each of the examples. With it, you can find more information about
the example. To run the example, you can simply "python" with the "\_sim.py" script.

	(mas) [user @ MultiAgent/examples/amoebot/] python amoebot_sim.py

Then a Pygame window will show up, inside which you can control the simulation using keybord keys.

## Run without Any Argument

Without any argument, the simulation will automatically generate a saving file, which records all
the necessary data to continue the simulation later. For example, if you started the "amoebot" example
without any argument, and closed it with "ESC" key, a new file of extension ".data" appears in the
current directory, like "multiagent_20180406093531_320529.data".

Since the data are saved into the file at the end of the simulation, you may need to wait for a while
if you have run a complex simulation for a long period of time.

## Run with An Argument

The "\_sim.py" script accept at most one argument, which is restricted to be a saving file of the multiagent simulation
(the only exception is "", the empty string).
If you go with such an argument, the simulation saved in the file will be restored, and you can replay or
continue the simulation. For example, the following command

	(mas) [user @ MultiAgent/examples/amoebot/] python amoebot_sim.py multiagent_20180406093531_320529.data

will restore the simulation saved in "multiagent_20180406093531_320529.data".
To remove the ".data" files, you can call the "clear.sh" script in the example's directory.

## "NO DATA" Option

There is a special case when you provide the argument with the empty string, i.e. "".

	(mas) [user @ MultiAgent/examples/amoebot/] python amoebot_sim.py ""

In such case, a new simulation will be started just like the cases without any arguments. However,
when the simulation is closed, the saving process is ignored, and hence there is no ".data" file generated.
This design will make things easier during the development of a new simulation.

## Test

You can run the tests (in "test.py" under the example folder) of the example by

	(mas) [user @ MultiAgent/examples/amoebot/] python test.py

## The List of Examples

- steering_move
- range_detect
