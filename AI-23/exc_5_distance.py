time = 1.0
power = 20

go(0,0,.1) # initialize
dist_start = get_ultrasound()[3]

go(power,power,time)
dist_final = get_ultrasound()[3]

dist = dist_final - dist_start
print('distance',dist)

"""
on ultrasound sensor 3 (BACK),

- moving forward -> FURTHER from the back obstacle,
- reading will INCREASE,
- therefore, must subtract 'start' from 'final'.


but if you use sensor 2 (FRONT),
- moving forward -> CLOSER to front obstacle,
- reading will DECREASE,
- therefore, must subtract 'final' from 'start' >>
  dist = dist_start - dist_final

"""
