t = 0
set(173, 780, 30)

def move(l, r, time):
	go(l, r, time)
	return time

for i in range(3):
	# at this juncture, this is pure EXPERIMENTATION.
	t += move(100, 100, 2.83)	# moves forward
	t += move(100, -100, 0.88)	# pivots 120 deg
   
print("Time taken:", t)
