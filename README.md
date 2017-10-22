# TurnSimulator
This Turn simulator are designed to be used in Micomouse tournament.

# Function
The aim of this simulator are to generate an angular velocity list,which is based on clothoid curve at the begging and at the end,
 in to c or h file in a given parameters.

Currently this program are under construction and can only display the trace of the robot.

# system requirement
Uses PyQT for GUI. Python3 are been used.
Haven't checked the environment thoroughly but should work with any OS unless it doesn't have python and pyQT.
The writer are using windows for development

# done
- Be able to create a window with pyQT
- Be able to select desired angle for Turn
- Be able to draw the trace of the turn in the graphic window
- Be able to draw the trace of the tire in the graphic window

# ToDo
- Clear up the programm so that parameter are not fixed and be changed through GUI
- Create a function that it can save the relative angular velocity
- Create a function that the parameter which the user input can be saved as txt file
- Calculate the trace by given side G
- Calculate the slip angle and implement
- Implement a function which can generate the angular velocity based other than clothoid.

The list are not in order. It can go back and forward.

# details
The angular velocity are calculated reletive to 1mm/s. so in real situation,
just multiply the target robot velocity to the angular velocity. In this case,
the angular velosity which is required are calculated on desired velosity.

In the future, this angular velocity relative to 1mm/s will be gone.
