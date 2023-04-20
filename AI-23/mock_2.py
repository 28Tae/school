"Q1 - car reverse rightward 90 deg, then travel straight"
while angle() == 0 or angle() >= 270:   # since car moves from 0, then 359, then down to 270.
    go(-80, -20, 1/24)
    go(0, 0, 1/24)
while get_ultrasound()[2] > 100:
    go(80, 80, 1/24)
    go(0, 0, 1/24)

"Q2 - increasing pivot speed"
for i in range(1, 101, 2):    # i will be 1, 3, 5, 7, ..., 97, finally 99.
    go(i, -i, 0.5) 

"Q3 - half travel then full burst"
start = get_ultrasound()[2]
while start - get_ultrasound()[2] < 500:   # for front sensor, DIST = START - FINAL
    if dist < 250:
        go(50, 50, 1/24)
    else:
        go(100, 100, 1/24)
go(0, 0, 1)

"Q4 - detect color strips. if 2, reverse southward. if 4, continue northward."
set(521, 950, 0)
count = 0
x = 100
while get_ultrasound()[2] > 50:
    go(power, power, 1/24)
    # given the tarmac is black with ZERO intensity
    # if it detects a color strip, the intensity
    # must be greater than 0, then we give it a
    # speed burst so that it doesnt over-detect
    if get_intensity()[0] > 0:
        x += 1
        go(power, power, 0.6)
    if x == 2:
        if power > 0:
            power = -100
    if x == 4:
        power = 100

"Q5 - 'levelling up' zigzag" 
go(100, 100, 0.45)
level = 1
while active():
    if get_ultrasound()[1] < 30:    # if detect right wall, turn left 90
        go(-100, 100, 0.5)
    elif get_ultrasound()[0] < 30:  # if detect left wall, turn right 90
        go(100, -100, 0.5)
    else:
        go(level * 10, level * 10, 0.1)
        if get_color()[0][0] > 50:  # detects red line
            level += 1              # level up is by 1, but power is multiplied by 10
            go(100, 100, 0.4)

"Q6 - travel fixed dist using color, ultrasound, intensity in order"
def c_to_km(color):   return color*4
def km_to_i(km):      return km/4

start = get_color()[0][0]
while c_to_km(get_color()[0][0] - start) < 300:
    go(50, 50, 1/24)
go(0, 0, 1)

start = get_ultrasound()[2]
while start - get_ultrasound()[2] < 200:
    go(50, 50, 1/24)
go(0, 0, 1)

start = get_intensity()[0]
while start - get_intensity()[0] < km_to_i(400):
    go(-50, -50, 1/24)
go(0, 0, 1)


