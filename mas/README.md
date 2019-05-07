# Class Reference

## (class) LookMixin

<b>LookMixin</b> is the mixin class designed to organize the object's
(or the obstacle's) attributes related to the display. The colors are
represented in RGBA tuples.

### Initialization

	look = LookMixin()

### Properties
- <b>stroke_color</b> : A tuple of four integers to indicate the color of the shape stroke.

		look.stroke_color = (0, 0, 0, 255)

- <b>pointer_color</b> : A tuple of four integers to indicate the color of the object's pointer.

		look.pointer_color = (0, 255, 0, 255)

- <b>fill_color</b> : A tuple of four integers to indicate the color of the object's solid center.

		look.fill_color = (255, 255, 255, 255)

- <b>visible</b> : A boolean variable that indicates whether the object/obstacle is visible (drawn in the display).

		look.visible = False

### Methods

None.

## (class) Object

<b>Object</b> is the most primary class in MultiAgent 2.0. It has a rigid body,
and hence responsible for interacting with the physical context. In MultiAgent 2.0,
there is only one shape for the objects, which is <i>circle</i>. The radius of the
circle can only be configured while the initializing. For the other properties,
you can change them through the corresponding interfaces.

### Initialization

	obj = Object(name = "0", mass = 1.0, radius = 10.0)
	# 'name' is mandatory.
	# 'mass' is 1.0 by default.
	# 'radius' is 10.0 by default.

### Properties
- <b>name</b> : A <b>non-empty</b> string to identify the Object instance.
Objects' names will be the only identification while binding to the corresponding agents,
and hence you should be cautious.

		obj.name = "0"

- <b>mass</b> : A single float number to indicate the mass.

		obj.mass = 5.0

- <b>radius</b> [read only]: A single float number to indicate the radius of the circle shape.

		print(obj.radius) # 10.0

- <b>pos</b> : A pair of float numbers to indicate the current position.

		obj.pos = (1.0, 0.0)

- <b>vel</b> : A pair of float numbers to indicate the current velocity.

		obj.vel = (0.0, 1.0)

- <b>force</b> : A pair of float numbers to indicate the force applied to the center of mass.

		obj.force = (0.5, 0.5)

- <b>angle</b> : A single float number to indicate the current orientation (angle from the east).

		obj.angle = 0.785  # 0.785 = pi/4.0

- <b>avel</b> : A single float number to indicate the angular velocity (counter-clockwise).

		obj.avel = 0.1

- Object inherits LookMixin, and hence the object instance has all LookMixin properties.

### Methods

- <b>info(<i>self</i>)</b> : return a string that encapsulates the instance information (class name and instance name).

		info = obj.info # 'info' is "<<multiagent.Object name=0>>"

- <b>draw(<i>self</i>, screen)</b> : draw the Object instance on the given screen.

		screen = pygame.display.set_mode((800, 600))
		obj.draw(screen = screen)

## (class) Obstacle
All <b>Obstacle</b>s in MultiAgent 2.0 are represendted by the segments with configurable thickness.

You can define an obstacle by specifying the starting point and the
finishing point. If you want the segment thicker, you can explicitly indicate the 'radius' parameter in the initialization.

In MultiAgent 2.0, all obstacles are static, which means they can not be moved (and resized) once they are created.

### Initialization

	obt = Obstacle(name = "0", a = (0.0, 0.0), b = (0.0, 0.0), radius = 1.0)
	# 'name' is mandatory.
	# 'a' is (0.0, 0.0) by default.
	# 'b' is (0.0, 0.0) by default.
	# 'radius' is 1.0 by default.

### Properties
- <b>name</b> : A <b>non-empty</b> string to identify the Obstacle instance.
The namespace of obstacles is different from the one used by the objects. Hence, you can use the same name for an obstacle and an object, and cause no conflicts.

		obt.name = "0"

- <b>a</b> [read only]: A pair of float numbers to indicate the starting point of the segment.

		print(obt.a) # (0.0, 0.0)

- <b>b</b> [read only]: A pair of float numbers to indicate the finishing point of the segment.

		print(obt.b) # (0.0, 0.0)

- <b>radius</b> [read only]: A single float number to indicate the thickness of the segment.

		print(obt.radius) # 1.0

- Obstacle inherits LookMixin, and hence the obstacle instance has all LookMixin properties.

### Methods

- <b>info(<i>self</i>)</b> : return a string that encapsulates the instance information (class name and instance name).

		info = obt.info # 'info' is "<<multiagent.Obstacle name=0>>"

- <b>draw(<i>self</i>, screen)</b> : draw the Obstacle instance on the given screen.

		screen = pygame.display.set_mode((800, 600))
		obt.draw(screen = screen)

## (class) OracleSpace

<b>OracleSpace</b> is where the objects and the obstacles stored. You can specify the objects and the obstacles in separate lists while initializing. You can also add or clear the objects or obstacles after the initialization.

### Initialization

	oracle = OracleSpace(objs = [obj0, obj1], obts = [obt0, obt1, obt2])
	# 'objs' is [] by default.
	# 'obts' is [] by default.

### Properties
- <b>objs</b> [read only]: A list of object instances.

		for obj in oracle.objs :
			print(obj.info())

		# <<multiagent.Object name=0>>
		# <<multiagent.Object name=1>>

- <b>obts</b> [read only]: A list of obstacle instances.

		for obt in oracle.obts :
			print(obt.info())

		# <<multiagent.Obstacle name=0>>
		# <<multiagent.Obstacle name=1>>
		# <<multiagent.Obstacle name=2>>

### Methods

- <b>info(<i>self</i>)</b> : return a string that encapsulates the instance information (class name and instance name).

		info = oracle.info # 'info' is "<<multiagent.OracleSpace objs_num=2 obts_num=3>>"

- <b>add_obj(<i>self</i>, obj)</b> : add an object.

		obj = Object(name = "2")
		oracle.add_obj(obj = obj)

- <b>add_obt(<i>self</i>, obt)</b> : add an obstacle.

		obt = Obstacle(name = "3", a = (0, 0), b = (1.0, 1.0))
		oracle.add_obt(obt = obt)

- <b>clear(<i>self</i>)</b> : clear all the <b>objects</b>.

		oracle.clear() # obj0 and obj1 are removed.

- <b>get_obj_with(<i>self</i>, name)</b> : get the object with the given name.

		obj = oracle.get_obj_with(name = "0")  # obj is <<multiagent.Object name=0>>

- <b>get_obt_with(<i>self</i>, name)</b> : get the obstacle with the given name.

		obt = oracle.get_obt_with(name = "0")  # obt is <<multiagent.Obstacle name=0>>

- <b>get_objs_at(<i>self</i>, c, d = 0, dist = ppdist_l2)</b> : get the object within a distance d (inclusively) from the given center point.

		# c : the center point, e.g. (0, 0)
		# d : the distance limit, with default value 0.
		# dist : the distance function, with default value ppdist_l2 (point-to-point distance in l2 norm.)

		# assume obj0 at (0, 0); obj1 at (10, 10)
		objs = oracle.get_objs_at(c = (0, 0), d = 5, dist = ppdist_l2)  # objs contains only obj0.

- <b>get_obts_at(<i>self</i>, c, d = 0, dist = pldist_l2)</b> : get the obstacle within a distance d (inclusively) from the given center point.

		# c : the center point, e.g. (0, 0)
		# d : the distance limit, with default value 0.
		# dist : the distance function, with default value pldist_l2 (point-to-line distance in l2 norm.)

		# assume obt0 from (-1, 1) to (1, 1); obt1 from (-1, 5) to (1, 5); obt2 from (-1, 10) to (1, 10)
		obts = oracle.get_obts_at(c = (0, 0), d = 5, dist = pldist_l2)  # obts contains only obt0 and obt1.

- <b>touch(<i>self</i>, c, d = 0)</b> : return the objects and the obstacle within a distance d (inclusively) from the given center point, in a list of blocks.

		# ppdist_l2 is used when check the distance between an object and the center.
		# pldist_l2 is used when check the distance between an obstacle and the center.
		# the block for the object has form: ("Object", obj.name, obj.pos[0], obj.pos[1], obj.radius)
        # the block for the obstacle has form ("Obstacle", obt.name, obt.start[0], obt.start[1], obt.end[0], obt.end[1], obt.radius)


		blocks = oracle.touch(c = (0, 0), d = 5)
		# [
		#	("Object", "0", 0.0, 0.0, 10),
		# 	("Obstacle", "0", -1, 1, 1, 1, 1),
		#	("Obstacle", "1", -1, 5, 1, 5, 1),
		# ]

- <b>draw(<i>self</i>, screen)</b> : draw the oracle (objects and obstacles) instance on the given screen.

		screen = pygame.display.set_mode((800, 600))
		oracle.draw(screen = screen)


## (class) Context
## (class) Agent
## (class) Schedule
## (class) Driver
## (class) Simulator
