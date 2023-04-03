t = 1.0

go(0, 0, 0.1) # initialize
dist_start = get_ultrasound()[3]
go(20, 20, t)
dist_final = get_ultrasound()[3]

dist = dist_final - dist_start
print('distance', dist)

# on rear sensor (3)
# dist = dist_final - dist_start

# but on front sensor (2)
# dist = dist_start - dist_final
