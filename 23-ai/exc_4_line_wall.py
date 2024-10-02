# refer to README.org to learn about
# ultrasound & color sensors 

while active():
    l = 50
    r = 50
    if get_ultrasound()[2] < 130:   # avoid right wall
        l = -40
        r = 100
    elif get_color()[0][0] >= 50:   # avoid red line via leftmost sensor
        l = 100
        r = -40
    go(l, r, 0.5)
