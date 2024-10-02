for i in range(4):
    a = (i + 1) * 90
    
    while get_ultrasound()[2] >= 69:    # draw trajectory
        go(85, 85, 0.01)
        
    if a != 360:    # refrain from pivoting once ending
        while a - angle() > 25: # quick pivot
            go(70, -70, 0.05)
        while a - angle() >= 1: # slow down
            go(10, -10, 0.05)
