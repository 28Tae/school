while active():       
    if get_ultrasound()[0] - get_ultrasound()[1] > 30:     # relatively closer to left wall
        go(-20, 80, 0.05)                                   
    elif get_ultrasound()[1] - get_ultrasound()[0] > 30:   # relatively closer to right wall
        go(80, -20, 0.05)                                    
    else:
        go(90, 90, 0.05)
