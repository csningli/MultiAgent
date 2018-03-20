# MultiAgent
An open source framework for simulating the multiagent system with mobile objects.

# Environment
## Download Multiagent
Download MultiAgent and step inside the folder.

	[user @ ~] git clone https://github.com/csningli/MultiAgent.git
	[user @ ~] cd MultiAgent
	
## Create Anaconda Environment
The following command will create and activate environment "multiagent_1_0", together with the necessary packages.
	
	[user @ MultiAgent] conda env create -f environment.yml
	[user @ MultiAgent] source activate multiagent_1_0
	
## Test MultiAgent
Go into the directory /1.0/unit_tests
	
	(multiagent_1_0)[user @ MultiAgent] cd 1.0/unit_tests

and run the following command to start the tests. 
	
	(multiagent_1_0)[user @ unit_tests] python test_multiagent.py	

If everything is correct, you will see something like

	(multiagent_1_0)[user @ unit_tests] python test_multiagent.py 
	--------------------------------------------------
	[Module Test] attempted/failed tests: 6/0
	--------------------------------------------------
	[Object Test] attempted/failed tests: 1/0
	--------------------------------------------------
	[Unit Test] attempted/failed tests: 2/0
	--------------------------------------------------
	[Context Test] attempted/failed tests: 1/0
	--------------------------------------------------
	[Driver Test] attempted/failed tests: 2/0
	--------------------------------------------------
	[Zipper Test] attempted/failed tests: 2/0

# Examples
In directory /1.0/examples, there are a series of examples. For example, let's see the example "patrol_car".
	
	(multiagent_1_0)[user @ MultiAgent] cd 1.0/examples/patrol_car

## Simulate
To start the simulator, execute "patrol_car.py" with argument "simulate".
	
	(multiagent_1_0)[user @ patrol_car] python patrol_car.py simulate

Then a pygame window will pop up to the desktop, and the simulation is started. 
Press "space" key on the keyboard to pause or resume the simulation, and "ESC"
to stop and quit the simulation. When finished, the simulation will
create a ".data" file under the current directory. The filename will include 
a label to indicate the time when the simulation is started, and thus will
differ for every run. In my case, the resulting file is
	
	multiagent_20170904223121_682503.data

## Replay with Data
The simulation can be replayed, as long as the corresponding ".data" file is on your hand.
	
	(multiagent_1_0)[user @ patrol_car] python patrol_car.py play multiagent_20170904223121_682503.data

## Clear the Data
The simulation data can be removed by simply deletion. When there are a lot of them, the script
"clear.sh" under "examples/" can offer some help.
	
	(multiagent_1_0)[user @ patrol_car] ../clear.sh

You can also remove the ".data" files inside an example from "examples/".
	
	(multiagent_1_0)[user @ examples] ./clear.sh patrol_car
	
