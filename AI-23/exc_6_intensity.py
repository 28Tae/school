# this function MUST be memorised.
def ultrasound(i):
	return (get_ultrasound()[i] + get_ultrasound()[i] + get_ultrasound()[i])/3

# surprisingly enough, if you look at exc 6.1 and 6.2 instructions,
# intensity would be directly proportional to the power of the car
# in other words, you can DIRECTLY get the power FROM finding intensity

# obviously there's the issue of "exceeding power range"
# where the raw power exceeds 100
# so you MUST reduce the intensity value first (i.e. by dividing)

def myFunction():
	while ultrasound(2) > 30:
		i = get_intensity()[0] / 2.5
		go(i,i,0.1)

def exercise_6_1():
	"as intensity increases, speed increases"
	myFunction()

def exercise_6_2():
	"as intensity decreases, speed decreases"
	set(500, 60, 180)
	myFunction()
	
	
	
