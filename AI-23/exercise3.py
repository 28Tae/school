"""This is a nested loop, with three while loops in a for loop.
Each side of the square is accounted for in the for loop.
The 1st while loop draws the trajectory.
The 2nd and 3rd while loops pivot the car about 90 degree.
"""


for i in range(4):
    a = (i + 1) * 90
    
    while get_ultrasound()[2] >= 69: # remember sensor 2 is the FRONT sensor
        go(85, 85, 0.01)
        
    if a != 360: # just ensures the car doesn't pivot at the end
        
        while a - angle() > 25: # quickly pivot until approaching 90 deg turn
            go(70, -70, 0.05)
        while a - angle() >= 1: # slowly pivot until a close 90 deg
            go(10, -10, 0.05)
