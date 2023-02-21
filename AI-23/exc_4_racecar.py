while active(): #idk why but active() only works in exp 1-7 and 1-8           
    if get_ultrasound()[0] - get_ultrasound()[1] > 30:
        go(-20,80,0.05)                                   
    elif get_ultrasound()[1] - get_ultrasound()[0] > 30:
        go(80,-20,0.05)                                    
    else:
        go(90,90,0.05)
