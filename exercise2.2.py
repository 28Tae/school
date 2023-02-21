t = 0
set(173,780,30) #sets the car to southwest corner

def move(l,r,time):
	go(l,r,time)
	return time

for i in range(3):
	t += move(100,100,2.83) #moves in a line
	t += move(100,-100,0.88) #pivots 120 deg
	"very importantly, at this point things should be TRIED, tested and experimented."
   
print("Time taken:",t)
