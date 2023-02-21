"""
ULTRASOUND SENSORS (relative distance to an obstacle)
0 - ↖ frontleft 
1 - ↗ frontright 
2 - ↑ front 
3 - ↓ back

COLOUR SENSORS
given get_color()[i][j],
[i] represents the sensor 0 to 3
[j] represents either R, G, or B
"""

while active():
    l = 50
    r = 50
    if get_ultrasound()[2] < 130: # avoids the right wall
        l = -40
        r = 100
    elif get_color()[0][0] >= 50: # avoids the red line via sensor 0
        l = 100
        r = -40
    go(l, r, 0.5)
